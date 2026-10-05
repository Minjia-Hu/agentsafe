"""One explicit-input scan; no Git state, persistent report or network client."""

import hashlib
from pathlib import Path
import time

from .config import Policy
from .extract import image_segments, text_segments
from .inputs import read_snapshot
from .models import FileResult, Limits, ScanError, ScanResult
from .rules import inspect_segments


def scan_files(paths: list[str], policy: Policy, *, config_loaded: bool = False, limits: Limits = Limits()) -> ScanResult:
    results = [FileResult(path) for path in paths]
    report = ScanResult(results, config_loaded, len(policy.sensitive_domains), len(policy.session_cookie_names))
    if len(paths) > limits.files:
        for result in results:
            result.notes.append("Too many inputs (maximum 20); no files were inspected. Split the invocation.")
        return report
    deadline = time.monotonic() + limits.total_seconds
    for result in results:
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
            data = read_snapshot(path, limits.image_bytes if image else limits.text_bytes)
            result.digest = hashlib.sha256(data).hexdigest()
            segments = image_segments(data, suffix, limits, deadline) if image else text_segments(data)
            result.findings = inspect_segments(segments, policy, deadline, limits.findings)
            result.coverage = "inspected"
            if image:
                result.notes.append("OCR: English, rendered pixels only; small/blurred text may be missed.")
                if not segments:
                    result.notes.append("No readable text extracted; this does not establish that the image is harmless.")
        except ScanError as error:
            result.coverage = "failed"
            result.notes.append(str(error))
        except Exception:
            # Do not print exception repr/tracebacks: parser errors can embed input.
            result.coverage = "failed"
            result.notes.append("Unexpected inspection failure; details hidden to protect input content.")
    return report
