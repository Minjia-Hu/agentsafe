"""Local text/OCR extraction. Image bytes and OCR output stay in memory."""

import csv
from io import BytesIO, StringIO
import math
import os
import shutil
import subprocess
import sys
import time
import warnings

from PIL import Image, UnidentifiedImageError

from .models import Box, Limits, ScanError, Segment, Word


def tesseract_command() -> str:
    override = os.environ.get("AGENTSAFE_TESSERACT")
    command = shutil.which(override if override is not None else "tesseract")
    # Respect an explicit override, even if invalid. Only use standard Homebrew
    # locations when PATH discovery failed and no override was supplied.
    if not command and override is None and sys.platform == "darwin":
        for candidate in ("/opt/homebrew/bin/tesseract", "/usr/local/bin/tesseract"):
            command = shutil.which(candidate)
            if command:
                break
    if not command:
        raise ScanError("Tesseract was not found. Install it and add it to PATH, or set AGENTSAFE_TESSERACT.")
    return command


def check_ocr() -> str:
    command = tesseract_command()
    try:
        version = subprocess.run([command, "--version"], capture_output=True, timeout=5, check=True)
        languages = subprocess.run([command, "--list-langs"], capture_output=True, timeout=5, check=True)
        if b"eng" not in languages.stdout.splitlines():
            raise ScanError("Tesseract English language data (eng) is missing.")
        # Only expose a version-shaped numeric token, never arbitrary stderr.
        import re
        match = re.search(rb"tesseract\s+(\d+\.\d+(?:\.\d+)?)", version.stdout)
        return match.group(1).decode("ascii") if match else "available"
    except (OSError, subprocess.SubprocessError):
        raise ScanError("Tesseract could not complete its local health check; diagnostics hidden.") from None


def text_segments(data: bytes) -> list[Segment]:
    try:
        text = data.decode("utf-8-sig")
    except UnicodeError:
        raise ScanError("Text is not valid UTF-8; no partial scan was performed.") from None
    if "\x00" in text:
        raise ScanError("Text contains NUL bytes; binary input is not supported.")
    if text.count("\n") >= 100_000:
        raise ScanError("Text exceeds the 100,000-line limit; no partial scan was performed.")
    # split on actual line endings; other controls must not silently shift locations.
    return [Segment(line.rstrip("\r"), line=i) for i, line in enumerate(text.split("\n"), 1)]


def prepare_image(data: bytes, suffix: str, limits: Limits) -> bytes:
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("error", Image.DecompressionBombWarning)
            with Image.open(BytesIO(data), formats=("PNG", "JPEG")) as image:
                expected = "PNG" if suffix == ".png" else "JPEG"
                if image.format != expected:
                    raise ScanError("Image bytes do not match the PNG/JPEG extension.")
                if image.width * image.height > limits.pixels:
                    raise ScanError("Image exceeds the 20-megapixel limit; no downsampling was performed.")
                if getattr(image, "n_frames", 1) != 1:
                    raise ScanError("Animated/multi-frame images are not supported; no frame was silently skipped.")
                if image.getexif().get(274, 1) != 1:
                    raise ScanError("EXIF-rotated images are not supported yet; export an upright copy and rescan.")
                image.load()
                # Scan rendered pixels against white; transparent/hidden content is
                # explicitly outside coverage. Re-encode without source metadata.
                rgba = image.convert("RGBA")
                rendered = Image.new("RGB", image.size, "white")
                rendered.paste(rgba, mask=rgba.getchannel("A"))
                rendered.info.clear()
                output = BytesIO()
                rendered.save(output, format="PNG")
                return output.getvalue()
    except (UnidentifiedImageError, OSError, ValueError, SyntaxError, Image.DecompressionBombError, Image.DecompressionBombWarning):
        raise ScanError("Image could not be decoded safely; details hidden, inspection failed.") from None


def parse_tsv(raw: bytes) -> list[Segment]:
    try:
        rows = csv.DictReader(StringIO(raw.decode("utf-8")), delimiter="\t", quoting=csv.QUOTE_NONE)
        required = {"level", "page_num", "block_num", "par_num", "line_num", "left", "top", "width", "height", "conf", "text"}
        if not required <= set(rows.fieldnames or ()):
            raise ValueError("Invalid OCR schema")
        grouped: dict[tuple[str, ...], list[dict]] = {}
        for row in rows:
            if row["level"] != "5" or not row["text"] or not row["text"].strip():
                continue
            key = tuple(row[k] for k in ("page_num", "block_num", "par_num", "line_num"))
            grouped.setdefault(key, []).append(row)
        segments = []
        for rows_in_line in grouped.values():
            parts, words = [], []
            offset = 0
            for row in rows_in_line:
                word = row["text"].strip()
                confidence = float(row["conf"])
                coords = [int(row[k]) for k in ("left", "top", "width", "height")]
                if not math.isfinite(confidence) or not 0 <= confidence <= 100 or any(n < 0 for n in coords):
                    raise ValueError("Invalid OCR values")
                words.append(Word(offset, offset + len(word), Box(*coords), confidence))
                parts.append(word)
                offset += len(word) + 1
            segments.append(Segment(" ".join(parts), words=tuple(words)))
        return segments
    except (ValueError, KeyError, TypeError, UnicodeError, csv.Error):
        raise ScanError("OCR returned malformed output; inspection failed, content hidden.") from None


def image_segments(data: bytes, suffix: str, limits: Limits, deadline: float) -> tuple[list[Segment], bytes]:
    encoded = prepare_image(data, suffix, limits)
    remaining = min(limits.ocr_seconds, deadline - time.monotonic())
    if remaining <= 0:
        raise ScanError("Invocation time budget exceeded before OCR; input was not inspected.")
    try:
        completed = subprocess.run(
            [tesseract_command(), "stdin", "stdout", "-l", "eng", "--psm", "11", "tsv"],
            input=encoded, capture_output=True, timeout=remaining, check=False,
        )
    except subprocess.TimeoutExpired:
        raise ScanError("OCR timed out; input was not fully inspected.") from None
    except OSError:
        raise ScanError("OCR could not start; run agentsafe doctor. Diagnostics hidden.") from None
    if completed.returncode:
        raise ScanError("OCR failed; check Tesseract and eng language data. Diagnostics hidden.")
    return parse_tsv(completed.stdout), encoded
