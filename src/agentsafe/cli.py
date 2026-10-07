"""Explicit checks and an approachable private synthetic demo."""

from enum import Enum
from pathlib import Path
from typing import Annotated
import webbrowser

from rich.console import Console
import typer

from .config import load_policy
from .extract import check_ocr
from .models import FileResult, ScanError, ScanResult
from .output import render
from .scan import scan_files
from .preview import ReviewGroup, save_preview, tr
from .output import safe_path


class Language(str, Enum):
    en = "en"
    zh = "zh"


def show_preview(groups: list[ReviewGroup], console: Console, lang: str, no_open: bool, *, synthetic: bool = False) -> None:
    path = save_preview(groups, lang=lang, synthetic=synthetic)
    console.print(tr(lang, "Private local preview (unredacted images / masked log excerpts; originals unchanged):", "私密本地预览（图片未打码／日志片段脱敏，原件未修改）："), markup=False)
    console.print(safe_path(str(path)), markup=False)
    if not no_open:
        try:
            opened = webbrowser.open(path.as_uri())
        except (OSError, webbrowser.Error):
            opened = False
        if not opened:
            console.print(tr(lang, "Open the HTML file above in your browser.", "请用浏览器打开上面的 HTML 文件。"), markup=False)

app = typer.Typer(no_args_is_help=True, pretty_exceptions_enable=False, help="Check explicit screenshots and logs locally before sharing. No Git hook or upload interception.")


@app.command()
def scan(
    paths: Annotated[list[str], typer.Argument(help="PNG/JPEG or UTF-8 .log/.txt paths; no directory recursion.")],
    config: Annotated[str | None, typer.Option("--config", help="Explicit TOML sensitivity configuration.")] = None,
    preview: Annotated[bool, typer.Option("--preview", help="Save and open a private page with unredacted image regions and masked log excerpts; originals unchanged.")] = False,
    no_open: Annotated[bool, typer.Option("--no-open", help="With --preview, save the page without opening a browser.")] = False,
    lang: Annotated[Language, typer.Option("--lang", help="Preview language; terminal scan output remains English.")] = Language.en,
) -> None:
    """Report masked evidence and coverage. Exit 0 / HIGH 1 / incomplete 2."""
    console = Console(highlight=False)
    try:
        policy = load_policy(Path(config) if config else None)
        report = scan_files(paths, policy, config_loaded=config is not None, capture_previews=preview)
    except ScanError as error:
        report = ScanResult([FileResult(p, notes=[f"Configuration error: {error}"]) for p in paths])
    render(report, console)
    if preview:
        try:
            show_preview([ReviewGroup(tr(lang.value, "Your files", "你的文件"), tr(lang.value, "Markers identify evidence, not redactions. Review the source, then scan again after edits.", "标记框用于定位证据，不是打码。请审阅原件，修改后重新扫描。"), report)], console, lang.value, no_open)
        except ScanError as error:
            console.print(f"ERROR  {error}", style="red", markup=False)
            raise typer.Exit(2)
    raise typer.Exit(report.exit_code)


@app.command()
def demo(
    lang: Annotated[Language, typer.Option("--lang", help="Demo summary and preview language.")] = Language.en,
    no_open: Annotated[bool, typer.Option("--no-open", help="Save the local page without opening a browser.")] = False,
) -> None:
    """Scan bundled fictional originals, reviewed copies and a known OCR miss."""
    from .demo import demo_groups

    console = Console(highlight=False)
    console.print(tr(lang.value, "AgentSafe · Fictional local demo", "AgentSafe · 虚构素材本地演示"), style="bold cyan", markup=False)
    try:
        groups = demo_groups(lang.value)
        for group in groups:
            high = sum(f.severity == "HIGH" for item in group.report.files for f in item.findings)
            warn = sum(f.severity == "WARN" for item in group.report.files for f in item.findings)
            console.print(f"{group.title}: {high} HIGH, {warn} WARN | Scan exit: {group.report.exit_code}", markup=False)
            for item in group.report.files:
                if item.coverage != "inspected":
                    for note in item.notes:
                        console.print(f"ERROR  {note}", markup=False)
        show_preview(groups, console, lang.value, no_open, synthetic=True)
    except ScanError as error:
        console.print(f"ERROR  {error}", style="red", markup=False)
        raise typer.Exit(2)
    incomplete = any(g.report.exit_code == 2 for g in groups)
    console.print(tr(lang.value, "Demo uses separately prepared reviewed copies, not automatic redaction. Completion does not certify privacy.", "修改后的样本是预先制作的对照文件，并非自动打码。演示完成不代表隐私保证。"), markup=False)
    raise typer.Exit(2 if incomplete else 0)


@app.command()
def gui(
    lang: Annotated[Language, typer.Option("--lang", help="Local GUI language.")] = Language.en,
) -> None:
    """Open a local browser GUI for file selection, scanning and review."""
    from .gui import run_gui

    console = Console(highlight=False)
    console.print(tr(lang.value, "Opening AgentSafe on this device. Use End session in the page to stop, or Ctrl+C here.", "正在本机打开 AgentSafe。在页面点击「结束使用」关闭，或在这里按 Ctrl+C。"), markup=False)
    try:
        run_gui(lang=lang.value)
    except (OSError, ScanError, webbrowser.Error):
        console.print(tr(lang.value, "Could not start the local GUI. No files were scanned.", "本地界面启动失败，未扫描任何文件。"), markup=False)
        raise typer.Exit(2)


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
        console.print(f"Policy: {len(policy.sensitive_domains)} sensitive domains, {len(policy.session_cookie_names)} session cookie names, {len(policy.sensitive_terms)} sensitive terms", markup=False)
    except ScanError as error:
        errors.append(str(error))
    for error in errors:
        console.print(f"ERROR  {error}", style="red", markup=False)
    console.print("No network requests were made. Only explicit local files will be scanned.", markup=False)
    raise typer.Exit(2 if errors else 0)


def main() -> None:
    app()
