# Cover brief — Silicon Valley C Players

Use this brief (and `render_cover.py`) to regenerate the cover. Do not invent a new concept unless Clark approves a redesign.

## What the cover must say

- Title: **SILICON VALLEY C PLAYERS**
- Author byline: **CLARK HUANG** (the real author; do not replace this with the fictional narrator)
- Kicker, at the top: **A FREE OPENBOOK** (never “A memoir”)
- Subtitle, between the title and the author: **AN EMBELLISHED FICTIONAL DRAMATIZATION**
- Do not put real company names, real people’s names, or “guess who” jokes on the cover.
- Charlie Hack is the fictional narrator inside the book, not the cover author.

## Visual

- Portrait, 864 × 1152 px (3:4), RGB.
- Deep navy field (`#0b1423`).
- A large mint brush-stroke letter **C** (`#9ed8bf` range) over faint circuit-board traces that form rolling mountain / valley shapes. No photographs, no logos.
- Kicker in copper-orange small caps, widely tracked, centered near the top.
- Title in large white sans-serif, two lines: SILICON VALLEY / C PLAYERS.
- Subtitle and author in smaller, tracked, centered type.
- Mood: serious, a little playful, first-party, no stock-photo sheen.

## Machine-readable description

A portrait book cover on a deep navy background. Across the top, small copper-orange lettering reads “A FREE OPENBOOK.” In the center, a large mint-green brush-stroke letter C sits over faint circuit-board traces shaped like rolling mountains. Below, large white sans-serif type reads “SILICON VALLEY” and “C PLAYERS.” A smaller, muted line reads “AN EMBELLISHED FICTIONAL DRAMATIZATION.” At the bottom, the author name “CLARK HUANG” appears in white. There are no photographs and no real company logos.

## How to rebuild

From the repository root:

```bash
python3 book-source/cover/render_cover.py
# writes book/cover.jpg and book-source/cover/cover.jpg
```

`base-art.png` is the circuit-and-C artwork without the kicker or the dramatization line. The script paints those two typographic lines on top. To change wording, edit the constants in `render_cover.py` and the brief above, then rerun.
