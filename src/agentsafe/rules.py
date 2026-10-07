"""Small structural rules, not a catalog of provider credential patterns."""

import re
import time
from urllib.parse import urlsplit

from .config import Policy
from .models import Box, Finding, ScanError, Segment

EMAIL = re.compile(r"(?<![\w.+-])[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@(?P<host>(?:[A-Za-z0-9-]+\.)+[A-Za-z]{2,63})(?![\w.-])")
URL = re.compile(r"https?://[^\s<>\"']+", re.I)
DOMAIN = re.compile(r"(?<![\w.@/-])(?:[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?\.)+[A-Za-z]{2,63}(?![\w.-])")
HEADER = re.compile(r"(?:^|\s)(?P<name>Proxy-Authorization|Authorization|Set-Cookie|Cookie)\s*:\s*(?P<value>.*)$", re.I)
PAIR = re.compile(r"\s*([^=;\s]+)\s*=\s*([^;]*)")
RESERVED = ("example.com", "example.net", "example.org", "test", "invalid", "localhost", "example")
PLACEHOLDERS = {"", "redacted", "hidden", "masked", "removed", "none", "null", "undefined", "placeholder", "token", "your_token", "your-token", "your_api_key", "your-api-key", "..."}


def placeholder(value: str) -> bool:
    value = value.strip().strip('"\'')
    value = re.sub(r"^(?:Bearer|Basic|Token)\s+", "", value, flags=re.I).strip()
    if value.lower() in PLACEHOLDERS:
        return True
    if (value.startswith("<") and value.endswith(">")) or (value.startswith("${") and value.endswith("}")):
        return True
    if value.startswith("[") and value.endswith("]"):
        return value[1:-1].strip().lower() in PLACEHOLDERS
    return bool(value) and (set(value) <= {"*"} or (len(value) >= 3 and set(value.lower()) <= {"x"}))


def evidence(segment: Segment, start: int, end: int, rule: str, message: str, high: bool, *, mask_span: tuple[int, int] | None = None) -> Finding:
    words = [w for w in segment.words if w.start < end and w.end > start]
    uncertain = bool(segment.words) and (not words or any(w.confidence < 80 for w in words))
    box = None
    if words:
        x = min(w.box.x for w in words)
        y = min(w.box.y for w in words)
        box = Box(x, y, max(w.box.x + w.box.width for w in words) - x, max(w.box.y + w.box.height for w in words) - y)
    return Finding(rule, "HIGH" if high and not uncertain else "WARN", message, segment.line, box, uncertain,
                   mask_span if mask_span is not None else (start, end))


def inspect_segment(segment: Segment, policy: Policy, *, max_findings: int = 200) -> list[Finding]:
    text = segment.text
    findings = []

    def add(finding: Finding) -> None:
        if len(findings) >= max_findings:
            raise ScanError("Finding limit exceeded; inspection is incomplete. Use a smaller input.")
        findings.append(finding)

    for pattern in policy.term_patterns:
        for match in pattern.finditer(text):
            add(evidence(segment, *match.span(), "sensitive-term", "Configured sensitive term or phrase; value hidden", True))
    occupied: list[tuple[int, int]] = []
    for match in URL.finditer(text):
        occupied.append(match.span())
        try:
            host = urlsplit(match.group().rstrip(".,);]}")).hostname
        except ValueError:
            host = None
        if host and policy.sensitive(host):
            add(evidence(segment, *match.span(), "sensitive-domain", "Configured sensitive domain; value hidden", True))
    for match in EMAIL.finditer(text):
        occupied.append(match.span())
        host = match.group("host").lower()
        sensitive = policy.sensitive(host)
        if sensitive:
            add(evidence(segment, *match.span(), "sensitive-domain", "Email uses a configured sensitive domain; value hidden", True))
        elif not any(host == d or host.endswith("." + d) for d in RESERVED):
            add(evidence(segment, *match.span(), "email", "Possible email address; sensitivity unknown; value hidden", False))
    for match in DOMAIN.finditer(text):
        if any(start <= match.start() < end for start, end in occupied):
            continue
        if policy.sensitive(match.group()):
            add(evidence(segment, *match.span(), "sensitive-domain", "Configured sensitive hostname; value hidden", True))
    for match in HEADER.finditer(text):
        name, value = match.group("name").lower(), match.group("value")
        if name.endswith("authorization"):
            if not placeholder(value) and value.strip().lower() not in {"bearer", "basic", "token"}:
                add(evidence(segment, *match.span(), "authorization", "Populated Authorization field; value hidden (validity not checked)", True, mask_span=match.span("value")))
            continue
        # Set-Cookie attributes such as Path/SameSite are not independent cookies.
        pairs = value.split(";") if name == "cookie" else value.split(";", 1)[:1]
        offset = match.start("value")
        for part in pairs:
            pair = PAIR.fullmatch(part)
            if pair and not placeholder(pair.group(2)):
                sensitive = pair.group(1) in policy.session_cookie_names
                message = "Configured session cookie; value hidden" if sensitive else "Populated cookie; sensitivity unknown; value hidden"
                add(evidence(segment, offset, offset + len(part), "session-cookie" if sensitive else "cookie", message, sensitive,
                             mask_span=(offset + pair.start(2), offset + pair.end(2))))
            offset += len(part) + 1
    return findings


def preview_mask_spans(segment: Segment, findings: list[Finding]) -> list[tuple[int, int]]:
    """Reuse detector offsets, hiding header values even when parsing is partial.

    This only prepares private finding-line context, not a sanitized export or
    a new detection rule. Names remain visible unless another rule masks them.
    """
    spans = [f.mask_span for f in findings if f.mask_span is not None]
    for match in HEADER.finditer(segment.text):
        name, value = match.group("name").lower(), match.group("value")
        if name.endswith("authorization"):
            spans.append(match.span("value"))
            continue
        offset = match.start("value")
        parts = value.split(";") if name == "cookie" else value.split(";", 1)
        for index, part in enumerate(parts):
            # Set-Cookie attributes are unnecessary context; hide the tail.
            pair = PAIR.fullmatch(part) if name == "cookie" or index == 0 else None
            spans.append((offset + pair.start(2), offset + pair.end(2)) if pair else (offset, offset + len(part)))
            offset += len(part) + 1
    return spans


def inspect_segments(segments: list[Segment], policy: Policy, deadline: float, max_findings: int) -> list[Finding]:
    findings: list[Finding] = []
    for segment in segments:
        if time.monotonic() >= deadline:
            raise ScanError("Invocation time budget exceeded; inspection is incomplete.")
        # Bound any one regex input as well as the total input size. No prefix scan.
        if len(segment.text) > 32_768:
            raise ScanError("A text line exceeds 32,768 characters; inspection is incomplete.")
        findings.extend(inspect_segment(segment, policy, max_findings=max_findings - len(findings)))
        if len(findings) > max_findings:
            raise ScanError("Finding limit exceeded; inspection is incomplete. Use a smaller input.")
    if time.monotonic() >= deadline:
        raise ScanError("Invocation time budget exceeded; inspection is incomplete.")
    return findings
