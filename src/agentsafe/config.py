"""Only an explicitly supplied, small TOML file can configure sensitivity."""

from dataclasses import dataclass
from pathlib import Path
import re
import tomllib

from .inputs import read_snapshot
from .models import ScanError

HOST = re.compile(r"(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z](?:[a-z0-9-]{0,61}[a-z0-9])?", re.I)
COOKIE_NAME = re.compile(r"[!#$%&'*+.^_`|~0-9A-Za-z-]{1,128}")


@dataclass(frozen=True)
class Policy:
    sensitive_domains: tuple[str, ...] = ()
    session_cookie_names: tuple[str, ...] = ()

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
    if set(data) - {"sensitive_domains", "session_cookie_names"}:
        raise ScanError("Unknown configuration key; use sensitive_domains and session_cookie_names only.")
    for value in data.values():
        if not isinstance(value, list) or len(value) > 100 or any(not isinstance(x, str) for x in value):
            raise ScanError("Each configuration field must be an array of at most 100 strings.")
    domains = data.get("sensitive_domains", [])
    cookies = data.get("session_cookie_names", [])
    if any(len(d) > 253 or not HOST.fullmatch(d) for d in domains):
        raise ScanError("Sensitive domains must be ASCII hostnames, without URLs, paths or wildcards.")
    if any(not COOKIE_NAME.fullmatch(c) for c in cookies):
        raise ScanError("Session cookie names must be valid HTTP cookie names of at most 128 characters.")
    return Policy(tuple(sorted({d.lower() for d in domains})), tuple(sorted(set(cookies))))
