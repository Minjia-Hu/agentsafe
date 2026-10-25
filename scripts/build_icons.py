"""Build the original A monogram favicon; no fonts or remote assets."""

from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1] / "src/agentsafe/ui/icons"
INK, PAPER = "#173f39", "#fffaf0"


def build():
    ROOT.mkdir(parents=True, exist_ok=True)
    markup = f'<rect width="64" height="64" rx="14" fill="{INK}"/><path fill="{PAPER}" fill-rule="evenodd" d="M14 50 27 14H37L50 50H40L37 41H27L24 50ZM29 33H35L32 23Z"/>'
    (ROOT / "monogram.svg").write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">{markup}</svg>\n')
    scale = 8
    im = Image.new("RGBA", (64 * scale, 64 * scale))
    draw = ImageDraw.Draw(im)
    draw.rounded_rectangle((0, 0, 64 * scale, 64 * scale), radius=14 * scale, fill=INK)
    for points, color in (
        ([(14,50),(27,14),(37,14),(50,50),(40,50),(37,41),(27,41),(24,50)], PAPER),
        ([(29,33),(35,33),(32,23)], INK),
    ):
        draw.polygon([(x * scale, y * scale) for x, y in points], fill=color)
    for size in (32, 180):
        im.resize((size,size), Image.Resampling.LANCZOS).save(ROOT / f"monogram-{size}.png")
    im.save(ROOT / "monogram.ico", sizes=[(16,16),(32,32),(48,48)])


if __name__ == "__main__":
    build()
