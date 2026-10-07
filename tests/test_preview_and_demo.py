from dataclasses import replace
from importlib.resources import files
from io import BytesIO
import os
from pathlib import Path
import time

from PIL import Image
import pytest
from typer.testing import CliRunner

from agentsafe import cli, extract, preview
from agentsafe.cli import app
from agentsafe.config import Policy
from agentsafe.models import Box, FileResult, Finding, Limits, ScanError, ScanResult
from agentsafe.preview import ReviewGroup, render_page, save_preview
from agentsafe.scan import scan_files


def group():
    buffer = BytesIO()
    Image.new("RGB", (80, 40), "white").save(buffer, format="PNG")
    file = FileResult("fictional.png", "inspected", [Finding("email", "WARN", "Possible email address; value hidden", box=Box(10, 10, 30, 15))], preview_png=buffer.getvalue())
    return ReviewGroup("Original", "Fictional content", ScanResult([file]))


@pytest.fixture
def storage(tmp_path, monkeypatch):
    monkeypatch.setattr(preview.tempfile, "gettempdir", lambda: str(tmp_path))
    return tmp_path


def test_page_uses_captured_pixels_not_changed_source(tmp_path, monkeypatch):
    source = tmp_path / "original.png"
    captured = group().report.files[0].preview_png
    source.write_bytes(captured)
    monkeypatch.setattr("agentsafe.scan.image_segments", lambda *args: ([], captured))
    normal = scan_files([str(source)], Policy())
    report = scan_files([str(source)], Policy(), capture_previews=True)
    assert source.read_bytes() == captured
    assert normal.files[0].preview_png is None
    source.unlink()
    html = render_page([ReviewGroup("Source", "Snapshot", report)])
    assert "data:image/png;base64," in html
    assert report.files[0].preview_png == captured


def test_preview_budget_is_incomplete_not_a_pass(tmp_path, monkeypatch):
    source = tmp_path / "original.png"
    captured = group().report.files[0].preview_png
    source.write_bytes(captured)
    monkeypatch.setattr("agentsafe.scan.image_segments", lambda *args: ([], captured))
    report = scan_files([str(source)], Policy(), capture_previews=True, limits=replace(Limits(), preview_bytes=1))
    assert report.exit_code == 2 and report.files[0].preview_png is None
    assert "budget" in report.files[0].notes[-1]


def test_html_escapes_names_masks_logs_and_contains_only_local_assets(tmp_path):
    log = tmp_path / "auth.log"
    log.write_text("Authorization: Bearer fictional-canary-do-not-echo\n")
    report = scan_files([str(log)], Policy())
    report.files[0].path = '<img src=x onerror=alert(1)>.log'
    html = render_page([ReviewGroup("<script>bad</script>", "", report)], lang="zh")
    assert "fictional-canary-do-not-echo" not in html
    assert "<img src=x" not in html and "&lt;img src=x" in html
    assert "<script>bad</script>" not in html
    assert "connect-src &#x27;none&#x27;" in html
    assert "sha256-" in html and '<script src=' not in html and '<link ' not in html
    assert "未打码" in html and "第 1 行" in html


def test_bad_region_cannot_be_presented_as_valid():
    review = group()
    review.report.files[0].findings[0] = Finding("email", "WARN", "Hidden", box=Box(70, 30, 30, 15))
    with pytest.raises(ScanError, match="outside"):
        render_page([review])


def test_private_storage_and_conservative_cleanup(storage):
    old = save_preview([group()])
    preserved = save_preview([group()])
    (preserved.parent / "keep.txt").write_text("User-owned addition")
    corrupt = save_preview([group()])
    (corrupt.parent / ".owner").write_bytes(b"\xff")
    for p in [old, preserved, corrupt]:
        os.utime(p.parent, (time.time() - 90000,) * 2)
    new = save_preview([group()])
    assert not old.exists() and preserved.exists() and corrupt.exists()
    assert new.is_file() and storage in new.parents
    if os.name == "posix":
        assert new.stat().st_mode & 0o777 == 0o600
        assert new.parent.stat().st_mode & 0o777 == 0o700


def test_storage_inside_repository_is_rejected(storage):
    (storage / ".git").mkdir()
    with pytest.raises(ScanError, match="inside a repository"):
        save_preview([group()])


def test_symlink_preview_root_is_rejected(storage):
    destination = storage / "other"
    destination.mkdir()
    root = storage / f"agentsafe-previews-{os.getuid() if hasattr(os, 'getuid') else 'local'}"
    root.symlink_to(destination, target_is_directory=True)
    with pytest.raises(ScanError, match="owned regular directory"):
        save_preview([group()])
    assert list(destination.iterdir()) == []


@pytest.mark.parametrize("content,expected", [("Public example", 0), ("Authorization: Bearer fictional-session", 1)])
def test_preview_preserves_scan_exit_and_open_is_explicit(storage, monkeypatch, content, expected):
    path = storage / "session.log"
    path.write_text(content)
    opened = []
    monkeypatch.setattr(cli.webbrowser, "open", lambda uri: opened.append(uri) or True)
    runner = CliRunner()
    assert runner.invoke(app, ["scan", str(path)]).exit_code == expected
    assert opened == [] and not list(storage.glob("agentsafe-previews-*"))
    assert runner.invoke(app, ["scan", str(path), "--preview", "--no-open"]).exit_code == expected
    assert opened == []
    assert runner.invoke(app, ["scan", str(path), "--preview"]).exit_code == expected
    assert len(opened) == 1 and opened[0].startswith("file:")


def test_preview_failure_overrides_findings(storage, monkeypatch):
    path = storage / "session.log"
    path.write_text("Authorization: Bearer fictional-session")
    def fail(*args, **kwargs):
        raise ScanError("Could not save a private local preview.")
    monkeypatch.setattr(cli, "save_preview", fail)
    result = CliRunner().invoke(app, ["scan", str(path), "--preview", "--no-open"])
    assert result.exit_code == 2 and "Could not save" in result.output


def test_packaged_demo_assets_match_reviewed_sources():
    source = Path(__file__).resolve().parents[1] / "examples" / "synthetic"
    assets = files("agentsafe").joinpath("demo_assets")
    for name in ["dashboard.png", "dashboard-reviewed.png", "session.log", "session-reviewed.log", "small-blurred.png", "policy.toml"]:
        assert assets.joinpath(name).read_bytes() == (source / name).read_bytes()


def test_demo_runs_without_checkout_and_reports_missing_ocr(storage, monkeypatch):
    monkeypatch.chdir(storage)
    monkeypatch.setenv("AGENTSAFE_TESSERACT", str(storage / "missing-ocr"))
    monkeypatch.setattr(cli.webbrowser, "open", lambda *args: pytest.fail("Browser must not open"))
    result = CliRunner().invoke(app, ["demo", "--no-open", "--lang", "zh"])
    assert result.exit_code == 2
    assert "修改前" in result.output and "ERROR" in result.output
    assert len(list(storage.glob("agentsafe-previews-*/*/index.html"))) == 1


def test_standard_macos_tesseract_discovery_respects_override(monkeypatch):
    monkeypatch.delenv("AGENTSAFE_TESSERACT", raising=False)
    monkeypatch.setattr(extract.sys, "platform", "darwin")
    monkeypatch.setattr(extract.shutil, "which", lambda value: value if value == "/opt/homebrew/bin/tesseract" else None)
    assert extract.tesseract_command() == "/opt/homebrew/bin/tesseract"
    monkeypatch.setenv("AGENTSAFE_TESSERACT", "/missing/explicit-tool")
    with pytest.raises(ScanError):
        extract.tesseract_command()


@pytest.mark.ocr
def test_real_demo_from_unrelated_directory(storage, monkeypatch):
    try:
        extract.check_ocr()
    except ScanError as exc:
        pytest.skip(str(exc))
    monkeypatch.chdir(storage)
    result = CliRunner().invoke(app, ["demo", "--lang", "zh", "--no-open"])
    assert result.exit_code == 0, result.output
    assert "修改前: 4 HIGH, 2 WARN" in result.output
    assert "修改后: 0 HIGH, 1 WARN" in result.output
    page = next(storage.glob("agentsafe-previews-*/*/index.html")).read_text()
    assert page.count('data:image/png;base64,') == 3
    with Image.open(BytesIO(files("agentsafe").joinpath("demo_assets/dashboard.png").read_bytes())) as original:
        width, height = original.size
    assert f'viewBox="0 0 {width} {height}"' in page
    assert "已知漏检" in page and "可能漏掉敏感内容" in page


def test_browser_open_failure_preserves_findings_and_prints_fallback(storage, monkeypatch):
    path = storage / "session.log"
    path.write_text("Authorization: Bearer fictional-session")
    monkeypatch.setattr(cli.webbrowser, "open", lambda *args: False)
    result = CliRunner().invoke(app, ["scan", str(path), "--preview"])
    assert result.exit_code == 1
    assert "Open the HTML file above" in result.output


@pytest.mark.parametrize("lang", ["en", "zh"])
def test_empty_ocr_prompts_manual_review_without_changing_scan_decision(lang):
    review = group()
    file = review.report.files[0]
    file.findings = []
    file.notes = [
        "OCR: English, rendered pixels only; small/blurred text may be missed.",
        "No readable text extracted; this does not establish that the image is harmless.",
    ]
    html = render_page([review], lang=lang)
    assert review.report.exit_code == 0  # Completed extraction; no invented finding.
    assert "0 HIGH · 0 WARN" in html
    assert "CHECKED" not in html and "No supported rule matched" not in html
    assert "未命中已支持的规则" not in html
    assert '<input class="overlay-control"' not in html
    if lang == "zh":
        assert "未识别出文字，需人工检查图片" in html
        assert "张图片需人工检查" in html
        assert "OCR: English" not in html and "No readable text extracted" not in html
        assert html.count("0 条发现不代表安全") == 1
    else:
        assert "No readable text — review the image manually" in html
        assert "1 OCR review" in html


def test_overlay_control_only_exists_when_there_are_regions():
    review = group()
    assert '<input class="overlay-control"' in render_page([review])
    review.report.files[0].findings = []
    html = render_page([review])
    assert '<input class="overlay-control"' not in html
    assert "No supported rule matched" in html


def test_text_report_without_preview_has_no_click_targets_or_raw_log_content(tmp_path):
    log = tmp_path / "session.log"
    log.write_text("Authorization: Bearer synthetic-canary-not-for-preview\nCookie: theme=light\n")
    report = scan_files([str(log)], Policy())
    html = render_page([ReviewGroup("Log", "", report)], lang="zh")
    assert "synthetic-canary-not-for-preview" not in html
    assert "第 1 行" in html and "第 2 行" in html
    assert "请按所示行号检查原件" in html
    assert ' data-target=' not in html and '<button class="finding' not in html
    assert "text-placeholder" not in html
    assert report.exit_code == 1


def test_failed_image_stays_incomplete_not_an_empty_ocr_result():
    report = ScanResult([FileResult("broken.png", "failed", notes=["Image could not be decoded safely."])])
    html = render_page([ReviewGroup("Failed", "", report)], lang="zh")
    assert report.exit_code == 2
    assert "检查未完成" in html and "ERROR" in html
    assert "CHECKED" not in html and "张图片需人工检查" not in html
