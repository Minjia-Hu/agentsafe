"""Transient evidence and opt-in masked context; no raw matched values."""

from dataclasses import dataclass, field
from typing import Literal


class ScanError(Exception):
    """Only fixed, safe explanations may be passed to this exception."""


@dataclass(frozen=True)
class Limits:
    image_bytes: int = 10 * 1024 * 1024
    text_bytes: int = 5 * 1024 * 1024
    pixels: int = 20_000_000
    ocr_seconds: float = 10
    total_seconds: float = 60
    files: int = 20
    findings: int = 200
    preview_bytes: int = 24 * 1024 * 1024


@dataclass(frozen=True)
class Box:
    x: int
    y: int
    width: int
    height: int


@dataclass(frozen=True)
class Word:
    start: int
    end: int
    box: Box
    confidence: float


@dataclass(frozen=True)
class Segment:
    text: str = field(repr=False)
    line: int | None = None
    words: tuple[Word, ...] = ()


@dataclass(frozen=True)
class Finding:
    rule: str
    severity: Literal["HIGH", "WARN"]
    explanation: str
    line: int | None = None
    box: Box | None = None
    uncertain: bool = False
    # Source character offsets for private text previews; never matched values.
    mask_span: tuple[int, int] | None = field(default=None, repr=False)


@dataclass(frozen=True)
class TextPreviewLine:
    line: int
    text: str = field(repr=False)
    excerpted: bool = False


@dataclass
class FileResult:
    path: str
    coverage: Literal["inspected", "uninspected", "failed"] = "uninspected"
    findings: list[Finding] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)
    digest: str | None = None
    # Only populated after an explicit preview request. Excluded from repr.
    preview_png: bytes | None = field(default=None, repr=False, compare=False)
    # Only masked excerpts of finding lines, never a raw log or OCR transcript.
    preview_lines: tuple[TextPreviewLine, ...] = field(default=(), repr=False, compare=False)


@dataclass
class ScanResult:
    files: list[FileResult]
    config_loaded: bool = False
    domain_count: int = 0
    cookie_count: int = 0
    term_count: int = 0

    @property
    def exit_code(self) -> int:
        if any(f.coverage != "inspected" for f in self.files):
            return 2
        return int(any(x.severity == "HIGH" for f in self.files for x in f.findings))
