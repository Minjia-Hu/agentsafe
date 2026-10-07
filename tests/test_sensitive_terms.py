"""User-supplied business context: literal matches, locations and privacy."""

from io import StringIO
import time

import pytest
from rich.console import Console
from typer.testing import CliRunner

from agentsafe.cli import app
from agentsafe.config import Policy, validate_policy
from agentsafe.models import Box, ScanError, Segment, Word
from agentsafe.output import render
from agentsafe.preview import render_cards
from agentsafe.rules import inspect_segment, inspect_segments
from agentsafe.scan import scan_buffers


@pytest.mark.parametrize("term,text,count", [
    ("Project Cedar", "Project: PROJECT   CEDAR", 1),
    ("Project Cedar", "Project Cedarwood", 0),
    ("Ann", "annual planning", 0),
    ("Ann", "Owner: Ann; reviewer: ann", 2),
    ("Cedar", "XCedar CedarX _Cedar Cedar_", 0),
    ("Project .*", "Project Cedar", 0),
    ("Project .*", "Literal: Project .*", 1),
    ("Acme, Inc.", "Customer: Acme, Inc.", 1),
    ("华星演示客户", "客户：华星演示客户；状态：处理中", 1),
    ("Acme Training", "Acme\tTraining", 1),
])
def test_literal_phrase_decisions(term, text, count):
    policy = validate_policy({"sensitive_terms": [term]})
    findings = inspect_segment(Segment(text, line=7), policy)
    assert len(findings) == count
    assert all((f.rule, f.severity, f.line) == ("sensitive-term", "HIGH", 7) for f in findings)
    assert term not in repr(findings) and term not in repr(policy)


@pytest.mark.parametrize("value", [
    [], ["x"], [" "], ["x" * 129], ["hidden\nphrase"], ["hidden\tphrase"],
    ["hidden\x1bphrase"], ["hidden\u2028phrase"], ["hidden\u200bphrase"],
    [1], "hidden-phrase", ["private phrase"] * 101,
])
def test_invalid_terms_are_rejected_without_echo(value):
    # An empty list is valid and keeps the default detector behavior.
    if value == []:
        assert validate_policy({"sensitive_terms": value}).sensitive_terms == ()
        return
    with pytest.raises(ScanError) as error:
        validate_policy({"sensitive_terms": value})
    assert "hidden" not in str(error.value).replace("values hidden", "")
    assert "private phrase" not in str(error.value)


def test_trim_deduplicate_and_keep_phrase_and_punctuation():
    policy = validate_policy({"sensitive_terms": ["  Project   Cedar  ", "project cedar", "Acme, Inc."]})
    assert policy.sensitive_terms == ("Project Cedar", "Acme, Inc.")


def test_ocr_phrase_box_spans_only_matched_words_and_keeps_uncertainty():
    text = "Project: Project Cedar"
    words = (
        Word(0, 8, Box(5, 10, 60, 20), 10),
        Word(9, 16, Box(80, 10, 70, 20), 95),
        Word(17, 22, Box(160, 10, 50, 20), 96),
    )
    policy = Policy(sensitive_terms=("Project Cedar",))
    finding, = inspect_segment(Segment(text, words=words), policy)
    assert finding.severity == "HIGH" and finding.box == Box(80, 10, 130, 20)
    uncertain_words = (*words[:2], Word(17, 22, words[2].box, 40))
    finding, = inspect_segment(Segment(text, words=uncertain_words), policy)
    assert finding.severity == "WARN" and finding.uncertain and finding.box == Box(80, 10, 130, 20)


def test_term_report_is_masked_and_newline_phrases_do_not_match():
    phrase = "Fictional Customer Canary"
    report = scan_buffers([("context.log", f"Client: {phrase}\nProject\nCedar".encode())],
                          Policy(sensitive_terms=(phrase, "Project Cedar")))
    assert report.exit_code == 1 and report.term_count == 2
    assert len(report.files[0].findings) == 1 and report.files[0].findings[0].line == 1
    stream = StringIO()
    render(report, Console(file=stream, color_system=None))
    for output in (repr(report), stream.getvalue(), render_cards(report, lang="en"), render_cards(report, lang="zh")):
        assert phrase not in output and "Project Cedar" not in output
    assert "2 sensitive terms" in stream.getvalue()


def test_terms_respect_finding_budget_without_partial_success():
    policy = Policy(sensitive_terms=("Cedar",))
    with pytest.raises(ScanError, match="Finding limit"):
        inspect_segments([Segment("Cedar " * 201)], policy, time.monotonic() + 5, 200)
    report = scan_buffers([("context.log", b"Cedar " * 201)], policy)
    assert report.exit_code == 2 and report.files[0].coverage == "failed"
    assert report.files[0].findings == []


def test_cli_uses_explicit_terms_config_and_masks_invalid_settings(tmp_path):
    log = tmp_path / "fictional.log"
    log.write_text("客户：华星演示客户\nProject: Project Cedar", encoding="utf-8")
    config = tmp_path / "policy.toml"
    config.write_text('sensitive_terms = ["华星演示客户", "Project Cedar"]', encoding="utf-8")
    runner = CliRunner()
    result = runner.invoke(app, ["scan", str(log), "--config", str(config)])
    assert result.exit_code == 1 and "2 HIGH" in result.output
    assert "华星演示客户" not in result.output and "Project Cedar" not in result.output
    health = runner.invoke(app, ["doctor", "--config", str(config)])
    assert "2 sensitive terms" in health.output
    assert "华星演示客户" not in health.output and "Project Cedar" not in health.output
    assert runner.invoke(app, ["scan", str(log)]).exit_code == 0
    config.write_text('sensitive_terms = ["never-echo-this-canary\\nphrase"]')
    result = runner.invoke(app, ["scan", str(log), "--config", str(config)])
    assert result.exit_code == 2 and "never-echo-this-canary" not in result.output
