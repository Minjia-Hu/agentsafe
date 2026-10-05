import hashlib
from pathlib import Path

import pytest

from agentsafe.config import load_policy
from agentsafe.extract import check_ocr
from agentsafe.models import ScanError
from agentsafe.scan import scan_files

ROOT = Path(__file__).resolve().parents[1] / "examples" / "synthetic"


@pytest.fixture(scope="module")
def ocr_ready():
    try:
        check_ocr()
    except ScanError as exc:
        pytest.skip(str(exc))


@pytest.mark.ocr
@pytest.mark.parametrize("name,expected", [
    ("dashboard.png", 1),
    ("dashboard-reviewed.png", 0),
    ("public-page.png", 0),
    ("public-page.jpg", 0),
    ("heldout-summary.jpg", 1),
    ("blank.png", 0),
])
def test_real_ocr_decisions_and_originals_unchanged(ocr_ready, name, expected):
    path = ROOT / name
    before = hashlib.sha256(path.read_bytes()).hexdigest()
    report = scan_files([str(path)], load_policy(ROOT / "policy.toml"))
    assert report.exit_code == expected
    assert report.files[0].coverage == "inspected"
    if expected == 1:
        assert all(f.box is not None for f in report.files[0].findings)
        assert all(f.box.x >= 0 and f.box.y >= 0 for f in report.files[0].findings)
    if name == "blank.png":
        assert any("No readable text" in note for note in report.files[0].notes)
    assert hashlib.sha256(path.read_bytes()).hexdigest() == before
