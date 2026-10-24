"""Verify exported pixels and preservation, rather than preview overlays."""

import hashlib
from io import BytesIO

from PIL import Image
from PIL.PngImagePlugin import PngInfo
import pytest

from agentsafe.models import ScanError
from agentsafe.redaction import FILL, copy_name, redact_png


def source_png():
    image = Image.new("RGBA", (40, 30), (230, 240, 250, 255))
    image.putpixel((1, 1), (255, 0, 0, 0))
    metadata = PngInfo()
    metadata.add_text("private", "SYNTHETIC_METADATA_CANARY")
    out = BytesIO()
    image.save(out, format="PNG", pnginfo=metadata)
    return out.getvalue()


def test_export_replaces_pixels_and_drops_hidden_channels_and_metadata():
    source = source_png()
    digest = hashlib.sha256(source).digest()
    result = redact_png(source, [{"x": 5, "y": 7, "w": 10, "h": 8}, {"x": 38, "y": 28, "w": 2, "h": 2}])
    assert hashlib.sha256(source).digest() == digest
    assert b"SYNTHETIC_METADATA_CANARY" not in result
    with Image.open(BytesIO(result)) as image:
        assert image.size == (40, 30) and image.mode == "RGB" and not image.info
        assert image.getpixel((1, 1)) == (255, 255, 255)
        for x in range(5, 15):
            for y in range(7, 15):
                assert image.getpixel((x, y)) == FILL
        assert image.getpixel((39, 29)) == FILL
        assert image.getpixel((15, 14)) == (230, 240, 250)
        assert image.getpixel((14, 15)) == (230, 240, 250)


@pytest.mark.parametrize("regions", [[], None, "bad", [{}], [{"x": -1, "y": 0, "w": 2, "h": 2}], [{"x": 39, "y": 0, "w": 2, "h": 2}], [{"x": 0, "y": 29, "w": 2, "h": 2}], [{"x": 0, "y": 0, "w": 0, "h": 2}], [{"x": True, "y": 0, "w": 2, "h": 2}], [{"x": 0.5, "y": 0, "w": 2, "h": 2}], [{"x": 0, "y": 0, "w": 2, "h": 2, "url": "https://example.org"}], [{"x": 0, "y": 0, "w": 2, "h": 2}] * 101])
def test_invalid_regions_are_rejected_without_source_changes(regions):
    source = source_png()
    with pytest.raises(ScanError):
        redact_png(source, regions)
    assert source == source_png()


def test_invalid_source_has_only_a_fixed_error():
    with pytest.raises(ScanError, match="original is unchanged"):
        redact_png(b"SYNTHETIC_PRIVATE_CANARY", [{"x": 0, "y": 0, "w": 2, "h": 2}])


def test_copy_name_always_has_a_new_png_suffix():
    assert copy_name("screenshot.jpeg") == "screenshot-redacted.png"
    assert copy_name("demo.png") != "demo.png"
    assert copy_name("x" * 240 + ".jpg").endswith("-redacted.png")
