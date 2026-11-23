"""SE201 lessons 7-8 layouts (se201_layouts_58b). Imported by render_se101.py.

drift       the same job run several times: one row per run, one column per step. A step can be done, done
            differently ("odd") or skipped; each run ends in a result. With a header, the runs all hang off one
            skill, which is the repaired version of the same picture.
            data: {label, steps: [..], runs: [{name, sub, at, cells: [{text, state: ok|odd|skip}], result, tone}],
                   header?: {text, tag, at}, cell_step?, caption?, caption_at?, caption_tone?, static?}
skill_card  a skill as a page: a file tab, then sections in two columns. Sections are hidden (placeholder bars),
            shown, or active (lit, lines landing one by one), so the page fills in over several beats.
            data: {label, path, version?, cols: [[{head, lines: [..]}], [..]], active: [heads], shown: [heads],
                   at?: {head: fraction}, held?, caption?, caption_at?, static?}
pipeline    work that runs on its own: a trigger, a row of stages, what crosses at each hand-off, the record
            each stage leaves, an alert under one stage, and a look inside one stage while it fails and is retried.
            data: {label, trigger?, stages: [{name, tag, tone, at}], hold?, focus?,
                   handoffs?: [..], handoffs_at?, handoffs_held?,
                   records?: [[lines]], records_at?, records_step?, records_held?, record_check?,
                   alert?: {stage, text, at},
                   fail?: {stage, title, blocks, brk, try_label, retry_label, at, break_at, retry_at, key, key_at,
                           note1, sub1, note2, sub2},
                   caption?, caption_at?, caption_y?, caption_tone?, static?}
"""
import render as R
from render import (W, H, BG, PANEL, PANEL_HI, TEXT, DIM, DIMMER, ACCENT, ACCENT_D,
                    AMBER, AMBER_D, ease, mix, fade, text_w, letterspace, check)


def font(*a, **k):
    return R.font(*a, **k)


def ctext(d, cx, y, s, f, fill):
    d.text((cx - text_w(d, s, f) // 2, y), s, font=f, fill=fill)


def box(d, x, y, w, h, fill, outline=None, width=2, r=18):
    d.rounded_rectangle([x, y, x + w, y + h], radius=r, fill=fill)
    if outline:
        d.rounded_rectangle([x, y, x + w, y + h], radius=r, outline=outline, width=width)


def fit(d, lines, maxw, size, bold=True, floor=15, mono=False):
    """the largest font, up to size, at which every line fits maxw"""
    while size > floor and max(text_w(d, ln, font(size, bold=bold, mono=mono)) for ln in lines) > maxw:
        size -= 1
    return font(size, bold=bold, mono=mono)


def spaced_w(d, s, f, sp):
    return sum(text_w(d, ch, f) + sp for ch in s) - sp


def fit_spaced(d, s, maxw, size, sp, floor=12):
    f = font(size)
    while spaced_w(d, s, f, sp) > maxw and f.size > floor:
        f = font(f.size - 1)
    return f


def dashed_box(d, x, y, w, h, col, width=3, dash=14, gap=10):
    for (x0, y0, x1, y1) in ((x, y, x + w, y), (x + w, y, x + w, y + h), (x + w, y + h, x, y + h), (x, y + h, x, y)):
        L = abs(x1 - x0) + abs(y1 - y0)
        ux, uy = (x1 - x0) / L, (y1 - y0) / L
        k = 0
        while k < L:
            e = min(k + dash, L)
            d.line([(x0 + ux * k, y0 + uy * k), (x0 + ux * e, y0 + uy * e)], fill=col, width=width)
            k += dash + gap


def harrow(d, x0, y, x1, col, width=4, head=14, prog=1.0):
    if prog <= 0:
        return
    xe = x0 + (x1 - x0) * prog
    d.line([(x0, y), (xe - head * 0.5, y)], fill=col, width=width)
    if prog > 0.85:
        d.polygon([(xe, y), (xe - head, y - head * 0.6), (xe - head, y + head * 0.6)], fill=col)


def varrow(d, x, y0, y1, col, width=3, head=11, prog=1.0):
    if prog <= 0:
        return
    ye = y0 + (y1 - y0) * prog
    d.line([(x, y0), (x, ye - head * 0.5)], fill=col, width=width)
    if prog > 0.85:
        d.polygon([(x, ye), (x - head * 0.6, ye - head), (x + head * 0.6, ye - head)], fill=col)


def lines_centered(d, cx, cy, lines, f, fill, lead=1.2):
    lh = int(f.size * lead)
    y = cy - (len(lines) * lh) // 2 - int(f.size * 0.06)
    for k, ln in enumerate(lines):
        ctext(d, cx, y + k * lh, ln, f, fill)


def caption(d, t, dur, data, x, y, size=44):
    cap = data.get("caption")
    if not cap:
        return
    ca = 1.0 if data.get("static") else ease((t - data.get("caption_at", 0.75) * dur) / 0.6)
    col = {"amber": AMBER, "accent": ACCENT}.get(data.get("caption_tone", "text"), TEXT)
    f = font(data.get("caption_size", size))
    for k, ln in enumerate(cap.split("\n")):
        d.text((x, data.get("caption_y", y) + k * int(f.size * 1.26)), ln, font=f, fill=fade(col, ca))


# ------------------------------------------------------------------ drift
def scene_drift(d, t, dur, data):
    """the same job, run several times: where the runs differ, and what each one cost"""
    static = data.get("static", False)
    a0 = 1.0 if static else ease(t / 0.4)
    letterspace(d, (140, 232), data["label"], font(23), fade(DIMMER, a0), sp=6)
    steps, runs = data["steps"], data["runs"]
    n = len(steps)
    nx, sx0, gap, resw = 140, 420, 18, 300
    rx = W - 140 - resw
    cw = (rx - 34 - sx0 - (n - 1) * gap) // n
    y0 = 296
    for k, s in enumerate(steps):
        x = sx0 + k * (cw + gap)
        letterspace(d, (x + 4, y0), s.upper(), fit_spaced(d, s.upper(), cw - 8, 17, 3), fade(DIM, a0), sp=3)
    rh_ = fit_spaced(d, "RESULT", resw, 17, 3)
    letterspace(d, (rx + 4, y0), data.get("result_head", "RESULT"), rh_, fade(DIM, a0), sp=3)
    y0 += 42
    head = data.get("header")
    if head:
        ha = 1.0 if static else ease((t - head.get("at", 0.04) * dur) / 0.6)
        hw = n * cw + (n - 1) * gap
        box(d, sx0, y0, hw, 82, fade(ACCENT_D, ha * 0.6), fade(ACCENT, ha), 3)
        sw_ = 0.0   # the skill is fixed mid-scene: its name swaps to the next version and the arrows fire again
        if head.get("text2"):
            sw_ = 1.0 if static else ease((t - head.get("swap_at", 0.6) * dur) / 0.5)
        hf = fit(d, [head["text"], head.get("text2", "")], hw - 60, 32, mono=head.get("mono", False))
        if sw_ < 1.0:
            ctext(d, sx0 + hw // 2, y0 + 41 - int(hf.size * 0.62), head["text"], hf, fade(TEXT, ha * (1 - sw_)))
        if sw_ > 0:
            ctext(d, sx0 + hw // 2, y0 + 41 - int(hf.size * 0.62) - int((1 - sw_) * 14), head["text2"], hf, fade(TEXT, sw_))
            if head.get("note2"):
                nf = fit(d, [head["note2"]], resw, 26)
                d.text((rx + 4, y0 + 41 - int(nf.size * 0.62)), head["note2"], font=nf, fill=fade(ACCENT, sw_))
        if head.get("tag"):
            tf = font(19)
            lines = head["tag"].split("\n")
            for j, ln in enumerate(lines):
                letterspace(d, (nx, y0 + 41 - len(lines) * 14 + j * 28), ln, tf, fade(ACCENT, ha), sp=4)
        for k in range(n):
            pr = ha if (sw_ <= 0 or sw_ >= 1 or static) else max(0.05, sw_)
            varrow(d, sx0 + k * (cw + gap) + cw // 2, y0 + 88, y0 + 122, fade(ACCENT, ha * 0.85), prog=pr)
        y0 += 128
    rh, rg = data.get("row_h", 112), data.get("row_gap", 24)
    cstep = data.get("cell_step", 0.45)
    for i, r in enumerate(runs):
        at = r.get("at", 0.1 + 0.25 * i) * dur
        ra = 1.0 if static else ease((t - at) / 0.5)
        if ra <= 0:
            continue
        y = y0 + i * (rh + rg)
        d.text((nx, y + rh // 2 - 40), r["name"], font=fit(d, [r["name"]], sx0 - nx - 24, 34), fill=fade(TEXT, ra))
        if r.get("sub"):
            d.text((nx, y + rh // 2 + 6), r["sub"], font=fit(d, [r["sub"]], sx0 - nx - 24, 23, bold=False), fill=fade(DIM, ra))
        for k, c in enumerate(r["cells"]):
            ca = 1.0 if static else ease((t - at - 0.35 - k * cstep) / 0.45)
            if ca <= 0:
                continue
            x = sx0 + k * (cw + gap)
            state = c.get("state", "ok")
            lines = c["text"].split("\n")
            if state == "skip":
                dashed_box(d, x + 2, y + 2, cw - 4, rh - 4, fade(AMBER, ca), width=3)
                f = fit(d, lines, cw - 36, 26)
                lines_centered(d, x + cw // 2, y + rh // 2, lines, f, fade(AMBER, ca))
                continue
            if state == "odd":
                box(d, x, y, cw, rh, fade(AMBER_D, ca * 0.7), fade(AMBER, ca), 3, r=14)
                f = fit(d, lines, cw - 36, 26)
                lines_centered(d, x + cw // 2, y + rh // 2, lines, f, fade(TEXT, ca))
                continue
            box(d, x, y, cw, rh, fade(PANEL, ca * 0.92), fade(DIMMER, ca), 2, r=14)
            if not c["text"]:   # a step done right needs no words: just the tick
                check(d, x + cw // 2, y + rh // 2, 22, ca)
                continue
            f = fit(d, lines, cw - 84, 26, bold=False)
            lh = int(f.size * 1.2)
            ty = y + rh // 2 - (len(lines) * lh) // 2 - 2
            for j, ln in enumerate(lines):
                d.text((x + 20, ty + j * lh), ln, font=f, fill=fade(TEXT, ca))
            check(d, x + cw - 34, y + rh // 2, 17, ca)
        resa = 1.0 if static else ease((t - at - 0.35 - n * cstep - 0.15) / 0.5)
        if resa > 0:
            col = AMBER if r.get("tone") == "amber" else ACCENT
            lines = r["result"].split("\n")
            f = fit(d, lines, resw - 8, 30)
            lh = int(f.size * 1.2)
            ty = y + rh // 2 - (len(lines) * lh) // 2 - 2
            for j, ln in enumerate(lines):
                d.text((rx + 4, ty + j * lh), ln, font=f, fill=fade(col, resa))
    caption(d, t, dur, data, nx, y0 + len(runs) * (rh + rg) + 30, 46)


# ------------------------------------------------------------------ skill card
def scene_skill_card(d, t, dur, data):
    """a skill as one page in the repo; its sections fill in over several beats"""
    static = data.get("static", False)
    held = static or data.get("held", False)
    a0 = 1.0 if held else ease(t / 0.5)
    letterspace(d, (140, 232), data["label"], font(23), fade(DIMMER, 1.0 if held else ease(t / 0.4)), sp=6)
    cx, cy, cw, ch = 140, 282, 1640, data.get("card_h", 520)
    dy = int((1 - a0) * 20)
    box(d, cx, cy + dy, cw, ch, fade(PANEL, a0 * 0.9), fade(DIMMER, a0), 2, r=22)
    d.rounded_rectangle([cx, cy + dy, cx + cw, cy + 58 + dy], radius=22, fill=fade(PANEL_HI, a0))
    d.rectangle([cx + 2, cy + 36 + dy, cx + cw - 2, cy + 58 + dy], fill=fade(PANEL_HI, a0))
    for i, c in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        d.ellipse([cx + 24 + i * 26, cy + 22 + dy, cx + 38 + i * 26, cy + 36 + dy], fill=fade(c, a0 * 0.75))
    d.text((cx + 124, cy + 14 + dy), data["path"], font=font(24, bold=False, mono=True), fill=fade(DIM, a0))
    if data.get("version"):
        vf = font(20)
        vw = text_w(d, data["version"], vf) + 36
        box(d, cx + cw - vw - 22, cy + 12 + dy, vw, 34, fade(ACCENT_D, a0 * 0.8), fade(ACCENT, a0), 2, r=17)
        d.text((cx + cw - vw - 4, cy + 17 + dy), data["version"], font=vf, fill=fade(TEXT, a0))
    d.line([(cx + cw // 2, cy + 84 + dy), (cx + cw // 2, cy + ch - 26 + dy)], fill=fade(DIMMER, a0 * 0.5), width=2)
    active, shown, ats = data.get("active", []), data.get("shown", []), data.get("at", {})
    size, lh = data.get("size", 28), data.get("line_h", 38)
    inner = cw // 2 - 96
    for ci, col in enumerate(data["cols"]):
        x = cx + 48 + ci * (cw // 2)
        y = cy + 84 + dy
        for s in col:
            key, lines = s["head"], s["lines"]
            hh = 32 + len(lines) * lh + 10
            is_act = (key in active) and not static
            vis = static or key in shown or key in active
            if is_act:
                at = ats.get(key, 0.06 + 0.4 * active.index(key) / max(len(active), 1)) * dur
                sa = ease((t - at) / 0.5)
                span = s.get("span", 0.3) * dur
            else:
                sa, at, span = (1.0 if vis else 0.0), 0.0, 0.0
            if is_act and sa > 0:
                d.rounded_rectangle([x - 22, y - 10, x + inner + 22, y + hh - 6], radius=12, fill=fade(ACCENT_D, a0 * sa * 0.38))
                d.rounded_rectangle([x - 22, y - 10, x - 16, y + hh - 6], radius=3, fill=fade(ACCENT, a0 * sa))
            hcol = mix(fade(DIMMER, 0.9), ACCENT, sa) if is_act else (DIM if vis else fade(DIMMER, 0.9))
            letterspace(d, (x, y), key, font(18), fade(hcol, a0), sp=5)
            f = fit(d, lines, inner, size, bold=False)
            for j, ln in enumerate(lines):
                ly = y + 32 + j * lh
                la = ease((t - at - 0.25 - j * span / max(len(lines), 1)) / 0.45) if is_act else sa
                if la < 1.0:   # placeholder bar: the page has a slot here, not yet written
                    bw = int(inner * (0.42 + 0.13 * ((j * 3 + len(key)) % 4)))
                    d.rounded_rectangle([x, ly + 11, x + bw, ly + 23], radius=6, fill=fade(DIMMER, a0 * 0.3 * (1 - la)))
                if la > 0:
                    d.text((x, ly), ln, font=f, fill=fade(TEXT, a0 * la * (1.0 if (is_act or static) else 0.78)))
            y += hh + data.get("sec_gap", 12)
    cap = data.get("caption")
    if cap:
        ca = 1.0 if static else ease((t - data.get("caption_at", 0.3) * dur) / 0.6)
        col = {"amber": AMBER, "accent": ACCENT}.get(data.get("caption_tone", "text"), TEXT)
        f = font(data.get("caption_size", 44))
        for k, ln in enumerate(cap.split("\n")):
            d.text((cx, data.get("caption_y", cy + ch + 38) + k * int(f.size * 1.26)), ln, font=f, fill=fade(col, ca))


# ------------------------------------------------------------------ pipeline
def _clock(d, cx, cy, r, col):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=col, width=3)
    d.line([(cx, cy), (cx, cy - r * 0.6)], fill=col, width=3)
    d.line([(cx, cy), (cx + r * 0.5, cy + r * 0.15)], fill=col, width=3)


def scene_pipeline(d, t, dur, data):
    """a pipeline that starts on its own: stages, hand-offs, run records, and a safe retry inside one stage"""
    static = data.get("static", False)
    hold = static or data.get("hold", False)
    a0 = 1.0 if hold else ease(t / 0.4)
    letterspace(d, (115, 232), data["label"], font(23), fade(DIMMER, a0), sp=6)
    stages = data["stages"]
    n = len(stages)
    span, x0 = 1690, 115
    sw = data.get("stage_w", 250)
    sg = (span - n * sw) // max(n - 1, 1)
    sy, sh = data.get("stage_y", 400), data.get("stage_h", 116)
    focus = data.get("focus")
    xs = [x0 + i * (sw + sg) for i in range(n)]

    trig = data.get("trigger")
    if trig:
        ta = 1.0 if hold else ease((t - 0.25) / 0.5)
        tf = font(21)
        tw = spaced_w(d, trig, tf, 3) + 84
        ty = sy - 94
        box(d, xs[0], ty, tw, 46, fade(AMBER_D, ta * 0.7), fade(AMBER, ta), 2, r=23)
        _clock(d, xs[0] + 28, ty + 23, 12, fade(AMBER, ta))
        letterspace(d, (xs[0] + 54, ty + 11), trig, tf, fade(TEXT, ta), sp=3)
        varrow(d, xs[0] + 28, ty + 50, sy - 8, fade(AMBER, ta), prog=ta)

    sas = []
    for i, s in enumerate(stages):
        sa = 1.0 if hold else ease((t - s.get("at", 0.08 + 0.6 * i / n) * dur) / 0.5)
        sas.append(sa)
        if sa <= 0:
            continue
        x = xs[i]
        dim = 0.5 if (focus is not None and focus != i) else 1.0
        lit = focus == i
        tone = s.get("tone")
        col = ACCENT if lit else AMBER if tone == "amber" else DIMMER
        fill = ACCENT_D if lit else PANEL
        ddy = int((1 - sa) * 18)
        if i > 0:
            harrow(d, xs[i - 1] + sw + 8, sy + sh // 2, x - 10, fade(DIM, min(sas[i - 1], sa) * 0.85), prog=sa)
        box(d, x, sy + ddy, sw, sh, fade(fill, sa * (0.7 if lit else 0.92) * dim), fade(col, sa * dim), 3 if (lit or tone) else 2)
        lines = s["name"].split("\n")
        lines_centered(d, x + sw // 2, sy + sh // 2 + ddy, lines, fit(d, lines, sw - 30, 30), fade(TEXT, sa * dim))
        if s.get("tag"):
            tf = fit_spaced(d, s["tag"], sw + sg - 30, 16, 3)
            letterspace(d, (x + sw // 2 - spaced_w(d, s["tag"], tf, 3) // 2, sy - 30 + ddy), s["tag"], tf,
                        fade(AMBER if tone == "amber" else DIM, sa * dim), sp=3)

    hs = data.get("handoffs")
    if hs:
        h_at, h_step = data.get("handoffs_at", 0.1), data.get("handoffs_step", 0.12)
        for k, lab in enumerate(hs):
            ha = 1.0 if (static or data.get("handoffs_held")) else ease((t - (h_at + k * h_step) * dur) / 0.5)
            if ha <= 0:
                continue
            gx0, gx1 = xs[k] + sw, xs[k + 1]
            mx = (gx0 + gx1) // 2
            lines = lab.split("\n")
            f = fit(d, lines, sg + 90, 26)
            hd = 0.5 if (focus is not None and not data.get("handoffs_lit")) else 1.0
            for j, ln in enumerate(lines):
                ctext(d, mx, sy + sh + 12 + j * 31, ln, f, fade(ACCENT, ha * hd))
            if not (static or data.get("handoffs_held")):   # a packet crosses as the label lands
                p = ease((t - (h_at + k * h_step) * dur - 0.1) / 0.9)
                if 0 < p < 1:
                    px = gx0 + 8 + (gx1 - gx0 - 30) * p
                    d.ellipse([px - 9, sy + sh // 2 - 9, px + 9, sy + sh // 2 + 9], fill=ACCENT)

    ry = sy + sh + data.get("records_dy", 96)
    recs = data.get("records")
    if recs:
        r_at, r_step = data.get("records_at", 0.1), data.get("records_step", 0.14)
        for k, lines in enumerate(recs):
            ra = 1.0 if (static or data.get("records_held")) else ease((t - (r_at + k * r_step) * dur) / 0.5)
            if ra <= 0 or not lines:
                continue
            x = xs[k]
            dim = 0.55 if (focus is not None and focus != k) else 1.0
            rh = 44 + len(lines) * 36 + 12
            box(d, x, ry, sw, rh, fade(BG, ra), fade(DIMMER, ra * dim), 2, r=12)
            letterspace(d, (x + 18, ry + 12), "RECORD", font(15), fade(DIM, ra * dim), sp=4)
            f = fit(d, lines, sw - 36, 25)
            for j, ln in enumerate(lines):
                amber = ln.startswith("!")
                d.text((x + 18, ry + 40 + j * 36), ln.lstrip("!"), font=f, fill=fade(AMBER if amber else TEXT, ra * dim))
            if data.get("record_check") == k:
                check(d, x + sw - 30, ry + 24, 14, ra * dim)
    al = data.get("alert")
    if al:
        aa = 1.0 if static else ease((t - al.get("at", 0.5) * dur) / 0.6)
        if aa > 0:
            k = al["stage"]
            lines = al["text"].split("\n")
            aw = al.get("w", 420)
            ax = min(xs[k] + sw - aw, W - 115 - aw) if k == n - 1 else xs[k]
            ay = al.get("y", ry + 190)
            ah = 30 + len(lines) * 42
            varrow(d, xs[k] + sw // 2, ay - 44, ay - 6, fade(AMBER, aa), prog=aa)
            box(d, ax, ay, aw, ah, fade(AMBER_D, aa * 0.75), fade(AMBER, aa), 3, r=16)
            f = fit(d, lines, aw - 48, 32)
            for j, ln in enumerate(lines):
                d.text((ax + 24, ay + 15 + j * 42), ln, font=f, fill=fade(TEXT, aa))

    fl = data.get("fail")
    if fl:
        pa = 1.0 if static else ease((t - fl.get("panel_at", 0.02) * dur) / 0.6)
        px, py, pw, ph = 115, sy + sh + 52, 1690, 340
        k = fl["stage"]
        sxc = xs[k] + sw // 2
        d.polygon([(sxc, py - 22), (sxc - 22, py + 2), (sxc + 22, py + 2)], fill=fade(DIMMER, pa))
        box(d, px, py, pw, ph, fade(PANEL, pa * 0.55), fade(DIMMER, pa), 2, r=20)
        letterspace(d, (px + 30, py + 18), fl["title"], font(17), fade(DIM, pa), sp=4)
        nb, brk = fl.get("blocks", 10), fl["brk"]
        bx0, bw, bg, bh = px + 250, 84, 12, 64
        nx_ = bx0 + nb * (bw + bg) + 24
        t1, tb, t2 = fl["at"] * dur, fl["break_at"] * dur, fl["retry_at"] * dur
        tend = fl.get("retry_end", 0.9) * dur
        # ---- first try
        y1 = py + 62
        l1 = ease((t - t1 + 0.3) / 0.4) if not static else 1.0
        d.text((px + 30, y1 + 14), fl.get("try_label", "First try"), font=font(30), fill=fade(TEXT, pa * l1))
        for b in range(nb):
            x = bx0 + b * (bw + bg)
            box(d, x, y1, bw, bh, fade(BG, pa), fade(DIMMER, pa * 0.8), 2, r=10)
            if b < brk:
                ba = 1.0 if static else ease((t - t1 - (tb - t1) * b / max(brk, 1)) / 0.3)
                if ba > 0:
                    box(d, x, y1, bw, bh, fade(ACCENT_D, pa * ba * 0.75), fade(ACCENT, pa * ba), 2, r=10)
                    check(d, x + bw // 2, y1 + bh // 2, 15, pa * ba)
            elif b == brk:
                ba = 1.0 if static else ease((t - tb) / 0.35)
                if ba > 0:
                    box(d, x, y1, bw, bh, fade(AMBER_D, pa * ba * 0.85), fade(AMBER, pa * ba), 3, r=10)
                    ctext(d, x + bw // 2, y1 + 8, "?", font(42), fade(AMBER, pa * ba))
        na = 1.0 if static else ease((t - tb - 0.2) / 0.5)
        d.text((nx_, y1 - 2), fl["note1"], font=fit(d, [fl["note1"]], px + pw - nx_ - 24, 30), fill=fade(AMBER, pa * na))
        d.text((nx_, y1 + 38), fl["sub1"], font=fit(d, [fl["sub1"]], px + pw - nx_ - 24, 23, bold=False), fill=fade(DIM, pa * na))
        # ---- retry
        y2 = py + 62 + bh + 34
        l2 = 1.0 if static else ease((t - t2 + 0.2) / 0.4)
        d.text((px + 30, y2 + 14), fl.get("retry_label", "Retry"), font=font(30), fill=fade(TEXT, pa * l2))
        skip_span = fl.get("skip_span", 0.3) * (tend - t2)
        key_t = fl.get("key_at", fl["retry_at"] + 0.12) * dur
        for b in range(nb):
            x = bx0 + b * (bw + bg)
            box(d, x, y2, bw, bh, fade(BG, pa * l2), fade(DIMMER, pa * l2 * 0.8), 2, r=10)
            if b < brk:
                ba = 1.0 if static else ease((t - t2 - skip_span * b / max(brk, 1)) / 0.3)
                if ba > 0:
                    ctext(d, x + bw // 2, y2 + 20, "skip", font(21), fade(DIM, pa * ba))
            elif b == brk:
                ba = 1.0 if static else ease((t - key_t) / 0.4)
                da = 1.0 if static else ease((t - key_t - 1.2) / 0.4)
                if ba > 0:
                    box(d, x, y2, bw, bh, mix(fade(AMBER_D, pa * ba * 0.85), fade(ACCENT_D, pa * 0.75), da),
                        mix(fade(AMBER, pa * ba), fade(ACCENT, pa), da), 3, r=10)
                    if da > 0:
                        check(d, x + bw // 2, y2 + bh // 2, 15, pa * da)
                    else:
                        ctext(d, x + bw // 2, y2 + 18, "key", font(23), fade(TEXT, pa * ba))
            else:
                start = key_t + 1.6
                ba = 1.0 if static else ease((t - start - (tend - start) * (b - brk - 1) / max(nb - brk - 1, 1)) / 0.3)
                if ba > 0:
                    box(d, x, y2, bw, bh, fade(ACCENT_D, pa * ba * 0.75), fade(ACCENT, pa * ba), 2, r=10)
                    check(d, x + bw // 2, y2 + bh // 2, 15, pa * ba)
        na2 = 1.0 if static else ease((t - tend - 0.1) / 0.5)
        d.text((nx_, y2 - 2), fl["note2"], font=fit(d, [fl["note2"]], px + pw - nx_ - 24, 30), fill=fade(ACCENT, pa * na2))
        d.text((nx_, y2 + 38), fl["sub2"], font=fit(d, [fl["sub2"]], px + pw - nx_ - 24, 23, bold=False), fill=fade(DIM, pa * na2))
        # ---- the key, pointing at the one uncertain charge
        ka = 1.0 if static else ease((t - key_t) / 0.5)
        if ka > 0:
            kx = bx0 + brk * (bw + bg) + bw // 2
            ky = y2 + bh + 30
            d.line([(kx, y2 + bh + 4), (kx, ky + 16)], fill=fade(AMBER, pa * ka), width=3)
            kf = font(23, mono=True)
            ktw = text_w(d, fl["key"], kf) + 40
            kx0 = max(px + 30, min(kx - ktw // 2, px + pw - ktw - 30))
            box(d, kx0, ky + 16, ktw, 44, fade(BG, pa * ka), fade(AMBER, pa * ka), 2, r=10)
            d.text((kx0 + 20, ky + 24), fl["key"], font=kf, fill=fade(TEXT, pa * ka))
            if fl.get("key_note"):
                d.text((kx0 + ktw + 22, ky + 24), fl["key_note"], font=font(23, bold=False), fill=fade(DIM, pa * ka))
        caption(d, t, dur, data, px, py + ph + 26, 40)
        return
    caption(d, t, dur, data, 115, ry + 200, 44)


R.RENDERERS.update({"drift": scene_drift, "skill_card": scene_skill_card, "pipeline": scene_pipeline})
