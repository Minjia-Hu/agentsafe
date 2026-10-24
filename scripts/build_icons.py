"""Build the original geometric favicon candidates; no fonts or remote assets."""

from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1] / "src/agentsafe/ui/icons"
INK, PAPER, MINT, SAND = "#173f39", "#fffaf0", "#dcebe0", "#f0debb"


def build():
    ROOT.mkdir(parents=True, exist_ok=True)
    shapes = {
        "monogram": f'<rect width="64" height="64" rx="14" fill="{INK}"/><path fill="{PAPER}" fill-rule="evenodd" d="M14 50 27 14H37L50 50H40L37 41H27L24 50ZM29 33H35L32 23Z"/>',
        "frame": f'<rect width="64" height="64" rx="14" fill="{MINT}"/><path d="M24 13H13V24M40 13H51V24M13 40V51H24M51 40V51H40" fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/><rect x="14" y="27" width="36" height="11" rx="2" fill="{INK}"/>',
        "document": f'<rect width="64" height="64" rx="14" fill="{SAND}"/><path d="M16 10H35L49 24V54H16Z" fill="{INK}"/><path d="M35 10V24H49" fill="#87a89a"/><rect x="22" y="31" width="21" height="7" rx="1" fill="{PAPER}"/><rect x="22" y="43" width="14" height="4" rx="1" fill="{PAPER}"/>',
    }
    for name, markup in shapes.items():
        (ROOT / f"{name}.svg").write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">{markup}</svg>\n')
        scale = 8
        im = Image.new("RGBA", (64 * scale, 64 * scale))
        d = ImageDraw.Draw(im)
        def box(coords): return tuple(round(n * scale) for n in coords)
        def poly(points, fill): d.polygon([(x * scale, y * scale) for x, y in points], fill=fill)
        d.rounded_rectangle(box((0, 0, 64, 64)), radius=14 * scale, fill={"monogram": INK, "frame": MINT, "document": SAND}[name])
        if name == "monogram":
            poly([(14,50),(27,14),(37,14),(50,50),(40,50),(37,41),(27,41),(24,50)], PAPER)
            poly([(29,33),(35,33),(32,23)], INK)
        elif name == "frame":
            for points in [[(24,13),(13,13),(13,24)],[(40,13),(51,13),(51,24)],[(13,40),(13,51),(24,51)],[(51,40),(51,51),(40,51)]]:
                d.line([(x * scale, y * scale) for x, y in points], fill=INK, width=5 * scale, joint="curve")
                for x,y in points: d.ellipse(box((x-2.5,y-2.5,x+2.5,y+2.5)),fill=INK)
            d.rounded_rectangle(box((14,27,50,38)),radius=2*scale,fill=INK)
        else:
            poly([(16,10),(35,10),(49,24),(49,54),(16,54)], INK)
            poly([(35,10),(35,24),(49,24)], "#87a89a")
            d.rounded_rectangle(box((22,31,43,38)),radius=scale,fill=PAPER)
            d.rounded_rectangle(box((22,43,36,47)),radius=scale,fill=PAPER)
        for size in (32, 180):
            im.resize((size,size),Image.Resampling.LANCZOS).save(ROOT / f"{name}-{size}.png")
        im.save(ROOT / f"{name}.ico",sizes=[(16,16),(32,32),(48,48)])


if __name__ == "__main__":
    build()
