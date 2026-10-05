"""Two commands for the private local experiment."""

from pathlib import Path
from typing import Annotated

from rich.console import Console
import typer

from .config import load_policy
from .extract import check_ocr
from .models import FileResult, ScanError, ScanResult
from .output import render
from .scan import scan_files

app = typer.Typer(no_args_is_help=True, pretty_exceptions_enable=False, help="Check explicit screenshots and logs locally before sharing. No Git hook or upload interception.")


@app.command()
def scan(
    paths: Annotated[list[str], typer.Argument(help="PNG/JPEG or UTF-8 .log/.txt paths; no directory recursion.")],
    config: Annotated[str | None, typer.Option("--config", help="Explicit TOML sensitivity configuration.")] = None,
) -> None:
    """Report masked evidence and coverage. Exit 0 / HIGH 1 / incomplete 2."""
    console = Console(highlight=False)
    try:
        policy = load_policy(Path(config) if config else None)
        report = scan_files(paths, policy, config_loaded=config is not None)
    except ScanError as error:
        report = ScanResult([FileResult(p, notes=[f"Configuration error: {error}"]) for p in paths])
    render(report, console)
    raise typer.Exit(report.exit_code)


@app.command()
def doctor(
    config: Annotated[str | None, typer.Option("--config", help="Optionally validate a sensitivity configuration.")] = None,
) -> None:
    """Check local OCR and optional configuration without uploading anything."""
    console = Console(highlight=False)
    console.print("AgentSafe Local Health Check", style="bold cyan", markup=False)
    console.print("UTF-8 text scanning is available. Image scanning requires Tesseract + eng data.", markup=False)
    errors = []
    try:
        version = check_ocr()
        console.print(f"READY  Tesseract {version}; English OCR (eng)", markup=False)
    except ScanError as error:
        errors.append(str(error))
    try:
        policy = load_policy(Path(config) if config else None)
        console.print(f"Policy: {len(policy.sensitive_domains)} sensitive domains, {len(policy.session_cookie_names)} session cookie names", markup=False)
    except ScanError as error:
        errors.append(str(error))
    for error in errors:
        console.print(f"ERROR  {error}", style="red", markup=False)
    console.print("No network requests were made. Only explicit local files will be scanned.", markup=False)
    raise typer.Exit(2 if errors else 0)


def main() -> None:
    app()
