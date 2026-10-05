from dataclasses import replace
import os
import subprocess

from PIL import Image
import pytest
from typer.testing import CliRunner

from agentsafe.cli import app
from agentsafe.config import Policy
from agentsafe.extract import parse_tsv, text_segments
from agentsafe.models import Limits, ScanError
from agentsafe.scan import scan_files

runner = CliRunner()


def test_mixed_result_error_precedes_high_and_masks_values(tmp_path):
    log = tmp_path / "session.log"
    log.write_text("Authorization: Bearer synthetic-secret-canary\n")
    original = log.read_bytes()
    result = runner.invoke(app, ["scan", str(log), str(tmp_path / "missing.log")])
    assert result.exit_code == 2
    assert "HIGH" in result.output and "1 inspected" in result.output and "1 failed" in result.output
    assert "synthetic-secret-canary" not in result.output and "Traceback" not in result.output
    assert log.read_bytes() == original


def test_warn_only_is_zero_and_header_line_is_preserved(tmp_path):
    log = tmp_path / "benign.log"
    log.write_text("Public example\nCookie: theme=light\n")
    result = runner.invoke(app, ["scan", str(log)])
    assert result.exit_code == 0
    assert "WARN" in result.output and "line 2" in result.output
    assert "not certify privacy" in result.output


@pytest.mark.parametrize("name,data,reason", [
    ("bad.png", b"broken image", "decoded safely"),
    ("bad.txt", b"\xff\xfe", "valid UTF-8"),
    ("binary.log", b"a\x00b", "NUL"),
    ("capture.har", b"{}", "Unsupported format"),
    ("movie.mov", b"fictional", "Unsupported format"),
])
def test_failed_or_unsupported_inputs_never_pass(tmp_path, name, data, reason):
    path = tmp_path / name
    path.write_bytes(data)
    result = runner.invoke(app, ["scan", str(path)])
    assert result.exit_code == 2
    assert reason in result.output


def test_symlink_parent_directory_and_fifo_are_not_followed(tmp_path):
    file = tmp_path / "normal.log"
    file.write_text("harmless")
    link = tmp_path / "link.log"
    link.symlink_to(file)
    linked_dir = tmp_path / "linked"
    linked_dir.symlink_to(tmp_path, target_is_directory=True)
    directory = tmp_path / "directory.log"
    directory.mkdir()
    inputs = [str(link), str(linked_dir / "normal.log"), str(directory)]
    if hasattr(os, "mkfifo"):
        fifo = tmp_path / "pipe.log"
        os.mkfifo(fifo)
        inputs.append(str(fifo))
    report = scan_files(inputs, Policy())
    assert report.exit_code == 2
    assert all(f.coverage == "failed" for f in report.files)


def test_extension_mismatch_pixel_limit_rotation_and_animation(tmp_path):
    image = Image.new("RGB", (30, 30), "white")
    wrong = tmp_path / "wrong.png"
    image.save(wrong, format="JPEG")
    assert scan_files([str(wrong)], Policy()).exit_code == 2
    large = tmp_path / "large.png"
    image.save(large)
    report = scan_files([str(large)], Policy(), limits=replace(Limits(), pixels=100))
    assert report.exit_code == 2 and "megapixel" in report.files[0].notes[0]
    rotated = tmp_path / "rotated.jpg"
    exif = Image.Exif()
    exif[274] = 6
    image.save(rotated, exif=exif)
    assert "EXIF-rotated" in scan_files([str(rotated)], Policy()).files[0].notes[0]
    animated = tmp_path / "animated.png"
    image.save(animated, save_all=True, append_images=[Image.new("RGB", (30, 30), "black")], duration=100, loop=0)
    assert "multi-frame" in scan_files([str(animated)], Policy()).files[0].notes[0]


def test_limits_account_for_all_requested_files(tmp_path):
    path = tmp_path / "a.log"
    path.write_text("0123456789")
    for limits, paths in [
        (replace(Limits(), text_bytes=4), [str(path)]),
        (replace(Limits(), files=1), [str(path), str(path)]),
        (replace(Limits(), total_seconds=0), [str(path), str(path)]),
    ]:
        report = scan_files(paths, Policy(), limits=limits)
        assert report.exit_code == 2 and len(report.files) == len(paths)
        assert all(f.coverage != "inspected" for f in report.files)


@pytest.mark.parametrize("body", [
    'sensitive_domains = ["https://northstar.test"]',
    'sensitive_domains = ["*.northstar.test"]',
    'sensitive_domains = "northstar.test"',
    'session_cookie_names = [2]',
    'session_cookie_names = ["a b"]',
    'allow_everything = true',
    'sensitive_domains = ["secret-canary',
])
def test_invalid_config_is_masked_and_fails_before_scanning(tmp_path, body):
    config = tmp_path / "policy.toml"
    config.write_text(body)
    log = tmp_path / "a.log"
    log.write_text("nothing")
    result = runner.invoke(app, ["scan", str(log), "--config", str(config)])
    assert result.exit_code == 2 and "uninspected" in result.output
    assert "secret-canary" not in result.output


def test_only_explicit_config_is_loaded(tmp_path, monkeypatch):
    (tmp_path / "agentsafe.toml").write_text('sensitive_domains = ["northstar.test"]')
    log = tmp_path / "a.log"
    log.write_text("https://northstar.test")
    monkeypatch.chdir(tmp_path)
    assert runner.invoke(app, ["scan", str(log)]).exit_code == 0
    assert runner.invoke(app, ["scan", str(log), "--config", "agentsafe.toml"]).exit_code == 1


def test_terminal_control_and_markup_in_filename_are_inert(tmp_path):
    log = tmp_path / "[red]demo\x1b[2J\n.log"
    log.write_text("Authorization: Bearer do-not-print-this-value")
    result = runner.invoke(app, ["scan", str(log)])
    assert result.exit_code == 1
    assert "\\u001b" in result.output and "\\u000a" in result.output
    assert "[red]demo" in result.output and "do-not-print-this-value" not in result.output


def test_missing_ocr_is_explicit_but_text_still_works(tmp_path, monkeypatch):
    monkeypatch.setenv("AGENTSAFE_TESSERACT", "definitely-not-installed-tesseract")
    png = tmp_path / "a.png"
    Image.new("RGB", (30, 30), "white").save(png)
    report = scan_files([str(png)], Policy())
    assert report.exit_code == 2 and "not found" in report.files[0].notes[0]
    assert runner.invoke(app, ["doctor"]).exit_code == 2
    txt = tmp_path / "a.txt"
    txt.write_text("benign")
    assert runner.invoke(app, ["scan", str(txt)]).exit_code == 0


@pytest.mark.parametrize("failure", ["timeout", "stderr", "unexpected"])
def test_ocr_diagnostics_never_echo_input(tmp_path, monkeypatch, failure):
    png = tmp_path / "a.png"
    Image.new("RGB", (30, 30), "white").save(png)
    monkeypatch.setattr("agentsafe.extract.tesseract_command", lambda: "fake")

    def run(*args, **kwargs):
        if failure == "timeout":
            raise subprocess.TimeoutExpired("fake", 1, stderr=b"secret-canary")
        if failure == "unexpected":
            raise RuntimeError("secret-canary")
        return subprocess.CompletedProcess(args, 1, b"", b"secret-canary")

    monkeypatch.setattr("agentsafe.extract.subprocess.run", run)
    result = runner.invoke(app, ["scan", str(png)])
    assert result.exit_code == 2
    assert "secret-canary" not in result.output and "Traceback" not in result.output


def test_malformed_ocr_output_is_not_an_empty_success():
    with pytest.raises(ScanError, match="malformed"):
        parse_tsv(b"secret-canary")


def test_tiny_lines_cannot_allocate_unbounded_segment_objects():
    with pytest.raises(ScanError, match="line limit"):
        text_segments(b"\n" * 100_000)
