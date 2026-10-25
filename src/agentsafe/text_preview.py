"""Bounded, masked finding-line excerpts from the inspected text snapshot."""

from collections import defaultdict

from .models import Finding, ScanError, Segment, TextPreviewLine
from .rules import preview_mask_spans

HIDDEN = "[HIDDEN]"
CONTEXT = 48
MAX_PREVIEW_BYTES = 64 * 1024


def _merge(spans: list[tuple[int, int]], length: int) -> list[tuple[int, int]]:
    merged: list[tuple[int, int]] = []
    for start, end in sorted(spans):
        if not 0 <= start <= end <= length:
            raise ScanError("Text preview location is invalid; no preview was generated.")
        if start == end:
            continue
        if merged and start <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(end, merged[-1][1]))
        else:
            merged.append((start, end))
    return merged


def masked_lines(segments: list[Segment], findings: list[Finding]) -> tuple[TextPreviewLine, ...]:
    """Include only finding lines; mask before omitting unrelated context.

    Every retained window includes complete masking spans. No prefix scan, raw
    cache, omitted match or dependency error is converted into a privacy pass.
    """
    by_line: dict[int, list[Finding]] = defaultdict(list)
    for finding in findings:
        if finding.line is None or finding.mask_span is None:
            raise ScanError("Text preview location is unavailable; no preview was generated.")
        by_line[finding.line].append(finding)
    result, size, located = [], 0, 0
    for segment in segments:
        if segment.line not in by_line:
            continue
        text = segment.text
        located += 1
        spans = preview_mask_spans(segment, by_line[segment.line])
        if spans is None:
            # Findings and line numbers remain; ambiguous context is not kept.
            continue
        masks = _merge(spans, len(text))
        windows = _merge([(max(0, start - CONTEXT), min(len(text), end + CONTEXT)) for start, end in masks], len(text))
        parts = []
        cursor = 0
        excerpted = False
        for start, end in windows:
            if start > cursor:
                parts.append(" … ")
                excerpted = True
            position = start
            for left, right in masks:
                if right <= start or left >= end:
                    continue
                parts.extend((text[position:left], HIDDEN))
                position = right
            parts.append(text[position:end])
            cursor = end
        if cursor < len(text):
            parts.append(" … ")
            excerpted = True
        safe_text = "".join(parts)
        size += len(safe_text.encode("utf-8"))
        if size > MAX_PREVIEW_BYTES:
            raise ScanError("Masked text preview exceeds its 64 KiB budget; select a smaller input or scan without --preview.")
        result.append(TextPreviewLine(segment.line, safe_text, excerpted))
    if located != len(by_line):
        raise ScanError("Text preview location is unavailable; no preview was generated.")
    return tuple(result)
