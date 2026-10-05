"""Render safe explanations only. Never render extracted input strings."""

import unicodedata

from rich.console import Console

from .models import ScanResult


def safe_path(value: str) -> str:
    return "".join(f"\\u{ord(c):04x}" if unicodedata.category(c).startswith("C") else c for c in value)


def render(report: ScanResult, console: Console) -> None:
    console.print("AgentSafe Local Artifact Check", style="bold cyan", markup=False)
    console.print(f"Scope: {len(report.files)} explicit local files | Processing: local", markup=False)
    console.print(f"Policy: {report.domain_count} sensitive domains, {report.cookie_count} session cookie names configured", markup=False)
    if not report.config_loaded:
        console.print("No sensitivity configuration supplied; organization-specific sensitivity is unknown.", markup=False)
    for file in report.files:
        console.print()
        level = "ERROR" if file.coverage != "inspected" else (
            "HIGH" if any(f.severity == "HIGH" for f in file.findings) else "WARN" if file.findings else "CHECKED"
        )
        console.print(f"{level:<8} {safe_path(file.path)}", style={"HIGH": "red", "WARN": "yellow", "ERROR": "bold red"}.get(level, "cyan"), markup=False)
        for finding in file.findings:
            if finding.box:
                b = finding.box
                location = f"region x={b.x} y={b.y} w={b.width} h={b.height} (source pixels)"
            else:
                location = f"line {finding.line}"
            console.print(f"  {finding.severity}  {finding.explanation}", markup=False)
            console.print(f"        {location}" + ("; uncertain OCR extraction" if finding.uncertain else ""), markup=False)
        if file.coverage == "inspected" and not file.findings:
            console.print("  No supported rule matched the inspected content.", markup=False)
        for note in file.notes:
            console.print(f"  {note}", markup=False)
    counts = {state: sum(f.coverage == state for f in report.files) for state in ("inspected", "uninspected", "failed")}
    console.print(f"\nCoverage: {counts['inspected']} inspected, {counts['uninspected']} uninspected, {counts['failed']} failed", markup=False)
    high = sum(x.severity == "HIGH" for f in report.files for x in f.findings)
    warn = sum(x.severity == "WARN" for f in report.files for x in f.findings)
    console.print(f"Findings: {high} HIGH, {warn} WARN | Exit: {report.exit_code}", markup=False)
    if report.exit_code == 2:
        console.print("Inspection incomplete. Resolve the reported errors and scan again.", markup=False)
    else:
        console.print("Review the indicated locations, edit if needed, and scan again before sharing.", markup=False)
    console.print("No upload or Git push was intercepted. This scan does not certify privacy.", markup=False)
