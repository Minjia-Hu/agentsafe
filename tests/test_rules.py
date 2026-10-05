import time

import pytest

from agentsafe.config import Policy
from agentsafe.models import Box, Segment, Word, ScanError
from agentsafe.rules import inspect_segment, inspect_segments

POLICY = Policy(("northstar.test",), ("demo_session",))


@pytest.mark.parametrize("text,expected", [
    ("https://console.northstar.test/dashboard", [("sensitive-domain", "HIGH")]),
    ("maya@northstar.test", [("sensitive-domain", "HIGH")]),
    ("Host: northstar.test", [("sensitive-domain", "HIGH")]),
    ("Host: console.NORTHSTAR.TEST", [("sensitive-domain", "HIGH")]),
    ("https://northstar.test.evil.example.org/path", []),
    ("https://notnorthstar.test/path", []),
    ("https://example.org/path/northstar.test?q=northstar.test", []),
    ("https://northstar.test@example.org/", []),
    ("support@example.org", []),
    ("support@public-project.demo", [("email", "WARN")]),
    ("http://localhost:3000", []),
    ("Authorization", []),
    ("Authorization:", []),
    ("Authorization: Bearer", []),
    ("Authorization: Bearer <token>", []),
    ("Authorization: [REDACTED]", []),
    ("Authorization: ********", []),
    ("Proxy-Authorization: Basic made-up-nonvalid-value", [("authorization", "HIGH")]),
    ("[DEBUG] Authorization: Bearer made-up-nonvalid-value", [("authorization", "HIGH")]),
    ("Cookie: demo_session=nonvalid-demo; theme=light", [("session-cookie", "HIGH"), ("cookie", "WARN")]),
    ("Cookie: demo_session=[REDACTED]", []),
    ("Cookie: theme=light", [("cookie", "WARN")]),
    ("Set-Cookie: demo_session=nonvalid-demo; Path=/; Secure; SameSite=Lax", [("session-cookie", "HIGH")]),
    ("Set-Cookie: theme=light; Path=/; SameSite=Lax", [("cookie", "WARN")]),
    ("Standalone password: not-in-scope", []),
])
def test_decision_boundaries(text, expected):
    findings = inspect_segment(Segment(text, line=8), POLICY)
    assert [(f.rule, f.severity) for f in findings] == expected
    assert all(f.line == 8 for f in findings)
    assert all(text not in f.explanation for f in findings)


def test_low_confidence_matched_word_warns_with_exact_box():
    text = "Host: northstar.test"
    box = Box(80, 40, 180, 24)
    segment = Segment(text, words=(Word(0, 5, Box(10, 40, 60, 24), 96), Word(6, len(text), box, 51)))
    finding, = inspect_segment(segment, POLICY)
    assert (finding.severity, finding.uncertain, finding.box) == ("WARN", True, box)


def test_low_confidence_unrelated_word_does_not_downgrade_domain():
    text = "Header northstar.test"
    segment = Segment(text, words=(Word(0, 6, Box(0, 0, 20, 10), 20), Word(7, len(text), Box(40, 0, 100, 10), 95)))
    finding, = inspect_segment(segment, POLICY)
    assert finding.severity == "HIGH"


def test_limits_never_return_a_partial_clean_scan():
    with pytest.raises(ScanError, match="line exceeds"):
        inspect_segments([Segment("x" * 32_769)], POLICY, time.monotonic() + 10, 200)
    with pytest.raises(ScanError, match="Finding limit"):
        inspect_segments([Segment("Host: northstar.test")] * 3, POLICY, time.monotonic() + 10, 2)
    with pytest.raises(ScanError, match="time budget"):
        inspect_segments([Segment("anything")], POLICY, time.monotonic() - 1, 200)
