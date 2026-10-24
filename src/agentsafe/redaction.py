"""Explicit opaque pixel replacement into a bounded new PNG, never a path."""

from io import BytesIO
from pathlib import Path
from PIL import Image, ImageDraw

from .models import Limits, ScanError
from .output import safe_path

MAX_REGIONS = 100
FILL = (23, 63, 57)


def redact_png(source: bytes, regions: object) -> bytes:
    if not isinstance(regions, list) or not 1 <= len(regions) <= MAX_REGIONS:
        raise ScanError("Select between 1 and 100 cover regions; no copy was created.")
    # The source is an already normalized, bounded PNG from this session's scan.
    try:
        with Image.open(BytesIO(source)) as image:
            w, h = image.size
            if image.format != "PNG" or w * h > Limits().pixels:
                raise ScanError("The image cannot be edited in this session.")
            boxes = []
            for region in regions:
                if not isinstance(region, dict) or set(region) != {"x", "y", "w", "h"}:
                    raise ScanError("Cover regions are invalid; no copy was created.")
                x, y, width, height = (region[k] for k in ("x", "y", "w", "h"))
                if any(type(n) is not int for n in (x, y, width, height)) or x < 0 or y < 0 or width < 1 or height < 1 or x + width > w or y + height > h:
                    raise ScanError("A cover region is outside the image; no copy was created.")
                boxes.append((x, y, x + width - 1, y + height - 1))
            # A fresh RGB image flattens alpha and drops source metadata. The
            # saved bytes contain solid pixels, not removable SVG/CSS overlays.
            output = Image.new("RGB", image.size, "white")
            if image.mode == "RGBA":
                output.paste(image, mask=image.getchannel("A"))
            else:
                output.paste(image.convert("RGB"))
            draw = ImageDraw.Draw(output)
            for box in boxes:
                draw.rectangle(box, fill=FILL)
            buffer = BytesIO()
            output.save(buffer, format="PNG")
            result = buffer.getvalue()
            if len(result) > Limits().image_bytes:
                raise ScanError("The PNG copy exceeds the 10 MiB image limit; no copy was created.")
            return result
    except ScanError:
        raise
    except Exception:
        raise ScanError("The image copy could not be created; the original is unchanged.") from None


def copy_name(name: str) -> str:
    stem = safe_path(Path(name).stem)[:180] or "screenshot"
    return f"{stem}-redacted.png"
