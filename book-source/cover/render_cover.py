#!/usr/bin/env python3
"""Paint the OpenBook kicker and dramatization line onto base-art.png and write cover.jpg."""
import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
# When this file lives in book-source/cover/, the site root is two levels up.
SITE = Path(os.environ.get("SITE", HERE.parents[1]))
BASE_ART = HERE / "base-art.png"
FONT = os.environ.get(
    "COVER_FONT",
    "/usr/share/fonts/truetype/sand-box/google/Montserrat/Montserrat-VariableFont_wght.ttf",
)
KICKER = "A FREE OPENBOOK"
TAGLINE = "AN EMBELLISHED FICTIONAL DRAMATIZATION"
NAVY_FALLBACK = (11, 20, 35)
COPPER = (214, 148, 78)
MUTED = (168, 176, 186)
KICKER_Y = 96
TAGLINE_Y = 970


def draw_tracked(draw, text, cy, font, fill, tracking, width):
    glyphs = list(text)
    widths = [font.getbbox(g)[2] - font.getbbox(g)[0] for g in glyphs]
    total = sum(widths) + tracking * (len(glyphs) - 1)
    x = width / 2 - total / 2
    box = font.getbbox("A")
    y = cy - (box[1] + box[3]) / 2
    for g, w in zip(glyphs, widths):
        draw.text((x, y), g, font=font, fill=fill)
        x += w + tracking


def main():
    if not BASE_ART.exists():
        raise SystemExit(f"missing {BASE_ART}")
    im = Image.open(BASE_ART).convert("RGB")
    W, H = im.size
    font_k = ImageFont.truetype(FONT, 22)
    font_t = ImageFont.truetype(FONT, 16)
    draw = ImageDraw.Draw(im)
    draw_tracked(draw, KICKER, KICKER_Y, font_k, COPPER, 6, W)
    draw_tracked(draw, TAGLINE, TAGLINE_Y, font_t, MUTED, 3, W)
    out_preview = HERE / "cover.jpg"
    out_site = SITE / "book" / "cover.jpg"
    out_site.parent.mkdir(parents=True, exist_ok=True)
    for dest in (out_preview, out_site, HERE / "cover.png"):
        if dest.suffix.lower() == ".png":
            im.save(dest)
        else:
            im.save(dest, quality=92, subsampling=0, optimize=True)
        print(f"wrote {dest}")


if __name__ == "__main__":
    main()
