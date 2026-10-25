"""Bounded line-local auth fields; no JSON/HAR document interpretation."""

from dataclasses import dataclass
import re

NAMES = r"Proxy-Authorization|Authorization|Set-Cookie|Cookie"
KEY = re.compile(r"(?<![\w\"'\\-])(?P<quote>[\"']?)(?P<name>" + NAMES + r")(?P=quote)\s*[:=]\s*", re.I)
MENTION = re.compile(r"(?<![\w-])(?:" + NAMES + r")(?![\w-])", re.I)


@dataclass(frozen=True)
class AuthField:
    name: str
    start: int
    end: int
    value_start: int
    value_end: int
    quoted: bool


def fields(text: str) -> list[AuthField]:
    """Keep original offsets, including escaped characters inside quoted values.

    Plain HTTP-style values extend to end of line. Quoted scalar values end at
    their unescaped closing quote, allowing multiple fields on the same line.
    Malformed or structured values are not guessed into detection evidence.
    """
    result = []
    consumed = 0
    for match in KEY.finditer(text):
        if match.start() < consumed:
            continue
        start = match.end()
        quoted = start < len(text) and text[start] in "\"'"
        if quoted:
            quote = text[start]
            end = start + 1
            while end < len(text):
                if text[end] == "\\":
                    end += 2
                elif text[end] == quote:
                    break
                else:
                    end += 1
            if end >= len(text) or (end + 1 < len(text) and not (text[end + 1].isspace() or text[end + 1] in ",;} ]")):
                continue
            value_start, value_end, consumed = start + 1, end, end + 1
        else:
            if match.group("quote"):
                continue
            value_start, value_end, consumed = start, len(text), len(text)
        result.append(AuthField(match.group("name").lower(), match.start(), consumed,
                                value_start, value_end, quoted))
    return result


def context_is_bounded(text: str, parsed: list[AuthField]) -> bool:
    """Withhold context if an auth/cookie label could not be safely bounded."""
    return all(any(field.start <= match.start() < field.end for field in parsed)
               for match in MENTION.finditer(text))
