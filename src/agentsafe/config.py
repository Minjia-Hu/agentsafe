"""Only an explicitly supplied, small TOML file can configure sensitivity."""

from dataclasses import dataclass, field
from functools import cached_property
from pathlib import Path
import re
import tomllib
import unicodedata

from .inputs import read_snapshot
from .models import ScanError

HOST = re.compile(r"(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z](?:[a-z0-9-]{0,61}[a-z0-9])?", re.I)
COOKIE_NAME = re.compile(r"[!#$%&'*+.^_`|~0-9A-Za-z-]{1,128}")


@dataclass(frozen=True)
class Policy:
    sensitive_domains: tuple[str, ...] = ()
    session_cookie_names: tuple[str, ...] = ()
    sensitive_terms: tuple[str, ...] = field(default=(), repr=False)

    @cached_property
    def term_patterns(self) -> tuple[re.Pattern, ...]:
        # Literal phrases only. Preserve offsets in the original text for OCR
        # boxes/line numbers; never normalize the evidence itself or cache policy
        # globally. ASCII word edges avoid matching "Ann" inside "annual".
        patterns = []
        for term in self.sensitive_terms:
            parts = [re.escape(part) for part in term.split(" ")]
            pattern = r"[^\S\r\n]+".join(parts)
            if term[0].isascii() and (term[0].isalnum() or term[0] == "_"):
                pattern = r"(?<![A-Za-z0-9_])" + pattern
            if term[-1].isascii() and (term[-1].isalnum() or term[-1] == "_"):
                pattern += r"(?![A-Za-z0-9_])"
            patterns.append(re.compile(pattern, re.I))
        return tuple(patterns)

    def sensitive(self, host: str) -> bool:
        host = host.lower().rstrip(".")
        return any(host == d or host.endswith("." + d) for d in self.sensitive_domains)


def load_policy(path: Path | None) -> Policy:
    if path is None:
        return Policy()
    try:
        data = tomllib.loads(read_snapshot(path, 64 * 1024).decode("utf-8"))
    except (UnicodeError, tomllib.TOMLDecodeError):
        raise ScanError("Configuration must be valid UTF-8 TOML; content is hidden.") from None
    return validate_policy(data)


def validate_policy(data: dict) -> Policy:
    """Validate both explicit TOML and GUI session configuration."""
    if not isinstance(data, dict) or set(data) - {"sensitive_domains", "session_cookie_names", "sensitive_terms"}:
        raise ScanError("Unknown configuration key; use sensitive_domains, session_cookie_names and sensitive_terms only.")
    for value in data.values():
        if not isinstance(value, list) or len(value) > 100 or any(not isinstance(x, str) for x in value):
            raise ScanError("Each configuration field must be an array of at most 100 strings.")
    domains = data.get("sensitive_domains", [])
    cookies = data.get("session_cookie_names", [])
    if any(len(d) > 253 or not HOST.fullmatch(d) for d in domains):
        raise ScanError("Sensitive domains must be ASCII hostnames, without URLs, paths or wildcards.")
    if any(not COOKIE_NAME.fullmatch(c) for c in cookies):
        raise ScanError("Session cookie names must be valid HTTP cookie names of at most 128 characters.")
    terms = {}
    for value in data.get("sensitive_terms", []):
        if any(unicodedata.category(c).startswith("C") or c in "\u2028\u2029" for c in value):
            raise ScanError("Sensitive terms must be single-line literal text without control characters; values hidden.")
        term = re.sub(r" +", " ", value.strip())
        if not 2 <= len(term) <= 128:
            raise ScanError("Sensitive terms must contain 2 to 128 characters after trimming; values hidden.")
        terms.setdefault(term.casefold(), term)
    return Policy(tuple(sorted({d.lower() for d in domains})), tuple(sorted(set(cookies))), tuple(terms.values()))
