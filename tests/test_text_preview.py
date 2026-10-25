"""Private log context is useful without preserving detected secret values."""

from dataclasses import replace
from io import StringIO

import pytest
from rich.console import Console

from agentsafe.config import Policy
from agentsafe.models import Limits
from agentsafe.output import render
from agentsafe.preview import ReviewGroup, render_cards, render_page
from agentsafe.scan import scan_buffers, scan_files


def check(text, policy=Policy()):
    return scan_buffers([("fictional.log", text.encode())], policy)


def test_auth_cookie_values_are_hidden_but_field_names_and_locations_remain():
    values = ["FICT_AUTH_CANARY", "FICT_SESSION_CANARY", "FICT_PREFERENCE_CANARY", "FICT_PROXY_CANARY"]
    text = f"Not retained: unrelated canary\n[DEBUG] Authorization: Bearer {values[0]}\nCookie: sid={values[1]}; theme={values[2]}\nProxy-Authorization: Basic {values[3]}"
    report = check(text, Policy(session_cookie_names=("sid",)))
    file = report.files[0]
    assert report.exit_code == 1 and len(file.findings) == 4
    assert [line.line for line in file.preview_lines] == [2, 3, 4]
    assert [line.text for line in file.preview_lines] == [
        "[DEBUG] Authorization: [HIDDEN]", "Cookie: sid=[HIDDEN]; theme=[HIDDEN]", "Proxy-Authorization: [HIDDEN]",
    ]
    for lang in ("en", "zh"):
        html = render_cards(report, lang=lang)
        assert 'id="scan-f0-line-2"' in html and 'data-target="scan-f0-line-3"' in html
        assert "Authorization:" in html and "sid=" in html and "theme=" in html
        assert "脱敏日志预览" in html if lang == "zh" else "Masked log preview" in html
        assert "unrelated canary" not in html
        assert all(value not in html for value in values)
    assert all(value not in repr(report) for value in values)
    # The terminal never prints excerpt content even when the GUI captured it.
    stream = StringIO()
    render(report, Console(file=stream, color_system=None))
    assert "sid=" not in stream.getvalue() and "FICT_" not in stream.getvalue()


def test_detected_domains_emails_terms_and_overlapping_values_are_all_masked():
    text = "Project: Project Cedar; Client: 华星演示客户; contact: worker@private.demo; https://console.private.test/path?q=fictional; host: private.test\nCookie: sid=Project Cedar"
    policy = Policy(("private.test",), ("sid",), ("Project Cedar", "Cedar", "华星演示客户"))
    report = check(text, policy)
    assert report.exit_code == 1
    html = render_cards(report, lang="zh")
    for value in ("Project Cedar", "Cedar", "华星演示客户", "worker@private.demo", "private.test", "path?q=fictional"):
        assert value not in html
    assert "Project:" in html and "contact:" in html and "host:" in html
    assert report.files[0].preview_lines[-1].text == "Cookie: sid=[HIDDEN]"


@pytest.mark.parametrize("header", [
    "Cookie: sid=FICT_COOKIE; malformed-FICT_TAIL",
    "Cookie: sid=FICT_COOKIE; spaced name=FICT_TAIL",
    "Set-Cookie: sid=FICT_COOKIE; Path=/FICT_TAIL; HttpOnly",
    "Cookie: sid=[REDACTED]; theme=FICT_TAIL",
])
def test_cookie_context_hides_malformed_parts_placeholders_and_attributes(header):
    report = check(header)
    assert report.files[0].preview_lines
    html = render_cards(report)
    assert "FICT_COOKIE" not in html and "FICT_TAIL" not in html
    assert "sid=" in html and "[HIDDEN]" in html


def test_placeholder_auth_value_is_hidden_when_another_rule_matches_its_line():
    report = check("[Project Cedar] Authorization: [REDACTED]", Policy(sensitive_terms=("Project Cedar",)))
    assert len(report.files[0].findings) == 1
    assert report.files[0].preview_lines[0].text == "[[HIDDEN]] Authorization: [HIDDEN]"


def test_html_and_control_characters_are_data_not_active_content():
    report = check('[INFO] <img src=x onerror=attack()>\x1b Project Cedar', Policy(sensitive_terms=("Project Cedar",)))
    html = render_cards(report, lang="zh")
    assert "Project Cedar" not in html and "<img " not in html
    assert "&lt;img " in html and "\\u001b" in html and "\x1b" not in html
    assert 'href="https://bad.test/' not in html


def test_long_line_shows_all_match_windows_not_just_a_prefix():
    text = "x" * 1200 + " Project Cedar " + "y" * 1200 + " Project Cedar " + "z" * 1200
    report = check(text, Policy(sensitive_terms=("Project Cedar",)))
    assert len(report.files[0].findings) == 2
    line, = report.files[0].preview_lines
    assert line.excerpted and line.text.count("[HIDDEN]") == 2
    assert len(line.text) < 230 and "Project Cedar" not in line.text
    html = render_cards(report)
    assert html.count('data-target="scan-f0-line-1"') == 2


def test_preview_uses_the_same_snapshot_and_is_off_for_ordinary_scans(tmp_path):
    path = tmp_path / "session.log"
    original = b"Client: Project Cedar\nAuthorization: Bearer FICT_SECRET"
    path.write_bytes(original)
    policy = Policy(sensitive_terms=("Project Cedar",))
    normal = scan_files([str(path)], policy)
    captured = scan_files([str(path)], policy, capture_previews=True)
    assert not normal.files[0].preview_lines and captured.files[0].preview_lines
    assert captured.exit_code == normal.exit_code == 1 and path.read_bytes() == original
    path.write_text("Changed after scanning")
    path.unlink()
    html = render_page([ReviewGroup("Snapshot", "", captured)])
    assert "Client:" in html and "Authorization:" in html
    assert "FICT_SECRET" not in html and "Project Cedar" not in html and "Changed after scanning" not in html


def test_no_findings_does_not_retain_full_log_or_create_a_click_target():
    report = check("Unrecognized private context\nAuthorization: [REDACTED]\nCookie: theme=<hidden>")
    assert report.exit_code == 0 and not report.files[0].preview_lines
    html = render_cards(report)
    assert "Unrecognized private context" not in html and 'data-target=' not in html
    assert "No finding lines to preview" in html


@pytest.mark.parametrize("text", ["Project Cedar\n" + "x" * 32769, "Project Cedar " * 201])
def test_incomplete_inspections_have_no_partial_excerpts(text):
    report = check(text, Policy(sensitive_terms=("Project Cedar",)))
    file = report.files[0]
    assert report.exit_code == 2 and file.coverage == "failed"
    assert not file.findings and not file.preview_lines
    assert "Project Cedar" not in render_cards(report)


def test_text_preview_budget_is_explicit_failure_not_partial_success(monkeypatch):
    monkeypatch.setattr("agentsafe.text_preview.MAX_PREVIEW_BYTES", 5)
    report = check("Customer: Project Cedar", Policy(sensitive_terms=("Project Cedar",)))
    assert report.exit_code == 2 and not report.files[0].findings and not report.files[0].preview_lines
    assert "budget" in report.files[0].notes[-1]


def test_text_input_byte_limit_still_applies_before_preview():
    report = scan_buffers([("small.txt", b"Authorization: FICT_SECRET")], Policy(), limits=replace(Limits(), text_bytes=2))
    assert report.exit_code == 2 and not report.files[0].preview_lines


@pytest.mark.parametrize("text", [
    '{"client":"Cedar","Authorization":"FICT_AUTH","Cookie":"sid=FICT_COOKIE"}',
    "{'client':'Cedar','Proxy-Authorization':'FICT_AUTH','Set-Cookie':'sid=FICT_COOKIE; Path=/'}",
    'Cedar Authorization="FICT_AUTH" Cookie="sid=FICT_COOKIE"',
    'Cedar Authorization=FICT_AUTH',
])
def test_quoted_and_equals_auth_fields_are_detected_and_hidden(text):
    report = check(text, Policy(sensitive_terms=("Cedar",), session_cookie_names=("sid",)))
    assert report.exit_code == 1
    assert any(f.rule == "authorization" for f in report.files[0].findings)
    assert report.files[0].preview_lines
    for html in (render_cards(report), render_page([ReviewGroup("Synthetic", "", report)])):
        assert "FICT_AUTH" not in html and "FICT_COOKIE" not in html and "Cedar" not in html


def test_quoted_fields_work_without_another_finding_and_keep_offsets():
    text = 'prefix {"Authorization":"FICT_AUTH","Cookie":"sid=FICT_COOKIE; theme=dark"}'
    report = check(text, Policy(session_cookie_names=("sid",)))
    file = report.files[0]
    assert report.exit_code == 1 and len(file.findings) == 3
    assert [text[slice(*f.mask_span)] for f in file.findings] == ["FICT_AUTH", "FICT_COOKIE", "dark"]
    assert file.preview_lines[0].text == 'prefix {"Authorization":"[HIDDEN]","Cookie":"[HIDDEN]"}'


@pytest.mark.parametrize("value", ['', 'Bearer', '[REDACTED]', 'null'])
def test_quoted_empty_and_placeholder_auth_does_not_create_high(value):
    assert check(f'{{"Authorization":"{value}"}}').exit_code == 0
    report = check(f'{{"client":"Cedar","Authorization":"{value}"}}', Policy(sensitive_terms=("Cedar",)))
    assert len(report.files[0].findings) == 1
    expected = '[HIDDEN]' if value else ''
    assert f'"Authorization":"{expected}"' in report.files[0].preview_lines[0].text


def test_escaped_quote_does_not_end_auth_mask_early():
    text = r'{"client":"Cedar","Authorization":"FICT_\"TAIL","Cookie":"sid=FICT_COOKIE"}'
    report = check(text, Policy(sensitive_terms=("Cedar",)))
    assert len(report.files[0].findings) == 3
    assert 'FICT_' not in render_cards(report)
    assert 'TAIL' not in render_cards(report)


@pytest.mark.parametrize("text", [
    'Cedar "Authorization": "FICT_UNCLOSED',
    'Cedar "Cookie": {"sid":"FICT_NESTED"}',
    'Cedar "Authorization": ["FICT_ARRAY"]',
    'Cedar "Authorization": "FICT_VALUE"FICT_TAIL',
    r'Cedar \"Authorization\":\"FICT_ESCAPED\"',
])
def test_ambiguous_auth_context_falls_back_to_noninteractive_location(text):
    report = check(text, Policy(sensitive_terms=("Cedar",)))
    assert report.exit_code == 1 and report.files[0].coverage == "inspected"
    assert report.files[0].findings and not report.files[0].preview_lines
    for lang in ("en", "zh"):
        html = render_cards(report, lang=lang)
        assert 'FICT_' not in html and 'Cedar' not in html and 'data-target=' not in html
        assert 'line 1' in html.lower() if lang == "en" else '第 1 行' in html
