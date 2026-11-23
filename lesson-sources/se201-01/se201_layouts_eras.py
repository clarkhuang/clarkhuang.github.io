"""Layouts added for Software Engineering 201, Lesson 1 (Four Eras of Building Systems). Imported by render_se101.py.

eras       four eras side by side; one arrives per beat, its rows land in turn, and what was scarce lands last.
           data: {label, upto, eras: [{year, ago, rows: [[head, value], ...], scarce, scarce_head?}], static?}
           Based on the "eras" layout drafted in se201_layouts1.py; taller cards, a fourth row, and every string
           is shrunk to fit its card, so nothing can overflow 1920x1080.
constants  what stayed true in every era: one bar per constant, spanning all four era columns, with a check in each.
           data: {label, cols: [..4 era names..], items: [{text, sub}], caption?}
"""
import render as R
from render import (W, H, BG, PANEL, PANEL_HI, TEXT, DIM, DIMMER, ACCENT, ACCENT_D,
                    AMBER, AMBER_D, ease, mix, fade, text_w, letterspace, check)


def font(*a, **k):
    return R.font(*a, **k)


def box(d, x, y, w, h, fill, outline=None, width=2, r=18):
    d.rounded_rectangle([x, y, x + w, y + h], radius=r, fill=fill)
    if outline:
        d.rounded_rectangle([x, y, x + w, y + h], radius=r, outline=outline, width=width)


def fit(d, lines, maxw, size, bold=True, floor=16):
    """the largest font, up to size, at which every line fits maxw"""
    while size > floor and max(text_w(d, ln, font(size, bold=bold)) for ln in lines) > maxw:
        size -= 1
    return font(size, bold=bold)


def spaced_w(d, s, f, sp):
    return sum(text_w(d, ch, f) + sp for ch in s) - sp


def scene_eras(d, t, dur, data):
    """four eras side by side; one arrives per beat, and its scarce resource lands last"""
    static = data.get("static", False)
    letterspace(d, (130, 222), data["label"], font(23), DIMMER, sp=6)
    eras, upto = data["eras"], data["upto"]
    cw, gap, h, y = 400, 20, 700, 278
    x0 = (W - (len(eras) * cw + (len(eras) - 1) * gap)) // 2
    inner = cw - 60
    for i, e in enumerate(eras):
        x = x0 + i * (cw + gap)
        if i >= upto:
            box(d, x, y, cw, h, BG, fade(DIMMER, 0.35))
            d.text((x + 30, y + 26), e["year"], font=font(64), fill=fade(DIMMER, 0.45))
            continue
        cur = (i == upto - 1) and not static
        a = ease((t - 0.2) / 0.55) if cur else 1.0
        dy = int((1 - a) * 26)
        box(d, x, y + dy, cw, h, fade(PANEL_HI if cur else PANEL, a * 0.95),
            fade(ACCENT if cur else DIMMER, a), 3 if cur else 2)
        d.text((x + 30, y + 26 + dy), e["year"], font=font(64), fill=fade(TEXT, a * (1.0 if cur else 0.8)))
        af = font(19)
        while spaced_w(d, e["ago"], af, 4) > inner and af.size > 14:
            af = font(af.size - 1)
        letterspace(d, (x + 30, y + 104 + dy), e["ago"], af, fade(ACCENT if cur else DIM, a), sp=4)
        yy = y + 150 + dy
        rows = e["rows"]
        step = (dur * 0.5) / max(len(rows), 1)
        for k, (head, val) in enumerate(rows):
            ra = ease((t - 0.9 - k * step) / 0.5) if cur else 1.0
            letterspace(d, (x + 30, yy), head, font(17), fade(DIM, ra), sp=4)
            lines = val.split("\n")
            vf = fit(d, lines, inner, 26, bold=False)
            for j, ln in enumerate(lines):
                d.text((x + 30, yy + 26 + j * 32), ln, font=vf, fill=fade(TEXT, ra * (1.0 if cur else 0.8)))
            yy += 26 + len(lines) * 32 + 14
        sa = ease((t - dur * 0.78) / 0.6) if cur else 1.0
        by = y + h - 118 + dy
        d.rounded_rectangle([x + 20, by, x + cw - 20, by + 98], radius=14,
                            fill=fade(AMBER_D, sa * (0.85 if cur else 0.55)))
        head = e.get("scarce_head", "WHAT WAS SCARCE" if i < len(eras) - 1 else "WHAT IS SCARCE")
        letterspace(d, (x + 40, by + 12), head, font(16), fade(AMBER, sa), sp=4)
        sf = fit(d, [e["scarce"]], cw - 80, 34)
        d.text((x + 40, by + 42), e["scarce"], font=sf, fill=fade(TEXT, sa))
    cap = data.get("caption")
    if cap:
        ca = ease((t - dur * data.get("caption_at", 0.6)) / 0.6)
        d.text((x0, y + h + 22), cap, font=font(34), fill=fade(ACCENT, ca))


def scene_constants(d, t, dur, data):
    """what never changed: a bar per constant running under all four eras, checked in each one"""
    static = data.get("static", False)
    a0 = 1.0 if static else ease(t / 0.4)
    letterspace(d, (160, 232), data["label"], font(23), fade(DIMMER, a0), sp=6)
    cols, items = data["cols"], data["items"]
    cx0, cstep = 1150, 175
    for k, c in enumerate(cols):   # the four eras, as column heads with a faint guide down each
        cx = cx0 + k * cstep
        cf = font(30)
        d.text((cx - text_w(d, c, cf) // 2, 292), c, font=cf, fill=fade(DIM, a0))
        d.line([(cx, 344), (cx, 344 + len(items) * 142 - 30)], fill=fade(DIMMER, a0 * 0.5), width=2)
    step = (dur * 0.8 - 0.6) / max(len(items), 1)
    for i, it in enumerate(items):
        ia = 1.0 if static else ease((t - 0.6 - i * step) / 0.55)
        if ia <= 0:
            continue
        y = 362 + i * 142
        dx = int((1 - ia) * -30)
        box(d, 160 + dx, y, 1600, 112, fade(PANEL, ia * 0.92), fade(DIMMER, ia), 2)
        d.rounded_rectangle([160 + dx, y, 166 + dx, y + 112], radius=3, fill=fade(ACCENT, ia))
        tf = fit(d, [it["text"]], 900, 40)
        d.text((196 + dx, y + 16), it["text"], font=tf, fill=fade(TEXT, ia))
        if it.get("sub"):
            sf = fit(d, [it["sub"]], 900, 26, bold=False)
            d.text((196 + dx, y + 68), it["sub"], font=sf, fill=fade(DIM, ia))
        for k in range(len(cols)):
            ka = 1.0 if static else ease((t - 0.9 - i * step - k * 0.14) / 0.35)
            check(d, cx0 + k * cstep + dx, y + 56, 22, ka * ia)
    cap = data.get("caption")
    if cap:
        ca = 1.0 if static else ease((t - dur * data.get("caption_at", 0.84)) / 0.6)
        d.text((160, 362 + len(items) * 142 + 6), cap, font=font(40), fill=fade(ACCENT, ca))


R.RENDERERS.update({"eras": scene_eras, "constants": scene_constants})
