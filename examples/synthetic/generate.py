"""Rebuild fictional OCR fixtures. Never captures a screen or contacts a server."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent


def screenshot(title: str, lines: list[str], *, font_size: int = 25, width: int = 1280) -> Image.Image:
    image = Image.new("RGB", (width, 760), "#f0f3f8")
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, width, 76), fill="#182a44")
    draw.text((40, 24), "SYNTHETIC DEMO / NO REAL DATA", font=ImageFont.load_default(size=25), fill="white")
    draw.rounded_rectangle((36, 106, width - 36, 704), radius=18, fill="white")
    draw.text((64, 136), title, font=ImageFont.load_default(size=34), fill="#172b47")
    draw.line((64, 198, width - 64, 198), fill="#d7deea", width=2)
    for i, line in enumerate(lines):
        draw.text((64, 234 + i * 68), line, font=ImageFont.load_default(size=font_size), fill="#172b47")
    draw.text((64, 658), "Fictional sample for a local privacy-check experiment", font=ImageFont.load_default(size=18), fill="#52657d")
    return image


def main() -> None:
    ROOT.mkdir(parents=True, exist_ok=True)
    screenshot("Northstar / account dashboard", [
        "Workspace: fictional training organization",
        "URL: https://console.northstar.test/dashboard",
        "Account: maya@northstar.test",
        "Open items: 12     Completed: 36",
    ]).save(ROOT / "dashboard.png")
    screenshot("Public demo / account dashboard", [
        "Workspace: synthetic public example",
        "URL: https://example.org/demo",
        "Account: demo@example.org",
        "Open items: 12     Completed: 36",
    ]).save(ROOT / "dashboard-reviewed.png")
    public = screenshot("Public documentation", [
        "Quickstart for the fictional sample project",
        "URL: https://example.org/docs",
        "Contact: support@example.org",
        "This page contains only public example data.",
    ])
    public.save(ROOT / "public-page.png")
    public.save(ROOT / "public-page.jpg", quality=90)
    # Separate layout/font variants for later evaluation, not rule tuning.
    heldout = Image.new("RGB", (1180, 420), "white")
    draw = ImageDraw.Draw(heldout)
    draw.text((46, 36), "FICTIONAL STATUS REPORT", font=ImageFont.load_default(size=32), fill="black")
    draw.text((92, 154), "https://status.northstar.test/overview", font=ImageFont.load_default(size=30), fill="black")
    draw.text((92, 240), "No real accounts or customer records", font=ImageFont.load_default(size=22), fill="black")
    heldout.save(ROOT / "heldout-summary.jpg", quality=85)
    small = Image.new("RGB", (900, 240), "white")
    ImageDraw.Draw(small).text((32, 70), "https://console.northstar.test/dashboard", font=ImageFont.load_default(size=9), fill="#777777")
    small.filter(ImageFilter.GaussianBlur(1.2)).save(ROOT / "small-blurred.png")
    Image.new("RGB", (320, 180), "white").save(ROOT / "blank.png")


if __name__ == "__main__":
    main()
