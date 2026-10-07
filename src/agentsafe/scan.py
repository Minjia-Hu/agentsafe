"""One explicit-input scan; no Git state, persistent report or network client."""

import hashlib
from collections.abc import Callable
from pathlib import Path
import time

from .config import Policy
from .extract import image_segments, text_segments
from .inputs import read_snapshot
from .models import FileResult, Limits, ScanError, ScanResult
from .rules import inspect_segments
from .text_preview import masked_lines


def scan_files(paths: list[str], policy: Policy, *, config_loaded: bool = False, limits: Limits = Limits(), capture_previews: bool = False) -> ScanResult:
    return _scan(paths, lambda i, limit: read_snapshot(Path(paths[i]), limit), policy,
                 config_loaded=config_loaded, limits=limits, capture_previews=capture_previews)


def scan_buffers(inputs: list[tuple[str, bytes]], policy: Policy, *, limits: Limits = Limits(), progress: Callable | None = None) -> ScanResult:
    """Inspect explicitly selected browser snapshots without writing raw files."""
    return _scan([name for name, _ in inputs], lambda i, limit: inputs[i][1], policy,
                 config_loaded=True, limits=limits, capture_previews=True, progress=progress)


def _scan(paths: list[str], read: Callable, policy: Policy, *, config_loaded: bool, limits: Limits, capture_previews: bool, progress: Callable | None = None) -> ScanResult:
    results = [FileResult(path) for path in paths]
    report = ScanResult(results, config_loaded, len(policy.sensitive_domains), len(policy.session_cookie_names), len(policy.sensitive_terms))
    if len(paths) > limits.files:
        for result in results:
            result.notes.append("Too many inputs (maximum 20); no files were inspected. Split the invocation.")
        return report
    deadline = time.monotonic() + limits.total_seconds
    captured_bytes = 0
    for index, result in enumerate(results):
        if progress:
            progress(index + 1, len(results), result.path)
        if time.monotonic() >= deadline:
            result.notes.append("Invocation time budget exceeded; this input was not inspected.")
            continue
        path = Path(result.path)
        suffix = path.suffix.lower()
        if suffix not in {".png", ".jpg", ".jpeg", ".log", ".txt"}:
            result.notes.append("Unsupported format; select PNG/JPEG or UTF-8 .log/.txt. Input not inspected.")
            continue
        try:
            image = suffix in {".png", ".jpg", ".jpeg"}
            byte_limit = limits.image_bytes if image else limits.text_bytes
            data = read(index, byte_limit)
            if len(data) > byte_limit:
                raise ScanError("Input exceeds the byte limit; nothing was truncated or inspected.")
            result.digest = hashlib.sha256(data).hexdigest()
            if image:
                segments, preview_png = image_segments(data, suffix, limits, deadline)
            else:
                segments = text_segments(data)
            result.findings = inspect_segments(segments, policy, deadline, limits.findings)
            if not image and capture_previews:
                result.preview_lines = masked_lines(segments, result.findings)
            result.coverage = "inspected"
            if image:
                if capture_previews:
                    captured_bytes += len(preview_png)
                    if captured_bytes > limits.preview_bytes:
                        raise ScanError("Preview image budget exceeded; rerun without --preview or with fewer images.")
                    result.preview_png = preview_png
                result.notes.append("OCR: English, rendered pixels only; small/blurred text may be missed.")
                if not segments:
                    result.notes.append("No readable text extracted; this does not establish that the image is harmless.")
        except ScanError as error:
            result.coverage = "failed"
            result.findings.clear()
            result.preview_png = None
            result.preview_lines = ()
            result.notes.append(str(error))
        except Exception:
            # Do not print exception repr/tracebacks: parser errors can embed input.
            result.coverage = "failed"
            result.findings.clear()
            result.preview_png = None
            result.preview_lines = ()
            result.notes.append("Unexpected inspection failure; details hidden to protect input content.")
    return report
