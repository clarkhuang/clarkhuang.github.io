"""SE201 lesson 10 (capstone) layouts. Imported by render_se101.py.

buildmap   one small feature, built end to end on one map that is held across the whole lesson. Each element of
           the map carries the number of the lesson it comes from and lights up when that lesson is applied:
             1 the "right means" banner          2 the files in the repo        3 the graph (parts + the shared node)
             4 agents on the parts, one merge    5 the person who decides       6 checks, before and after
             7 the part that is already a skill  8 the routine in production    9 the agent that operates it
           The lower half shows what was written down for the current step (a panel), then the build as it runs
           (a log), then production (a row of steps plus the operator). The four constants land last.
           data: {label, map: {right, files, parts, quote, quote_sub, merge, gate, gate_sub},
                  show: [names], lit: [names], ats: {name: fraction}, ghost?,
                  built?: True | "go", go?: {parts, parts_end, merge, checks, gate, ship},
                  build_dim?, build_dim_from?,
                  lower?: {kind: panel | days | log | prod, ...}, consts?: {items, at, step},
                  pulse?: [[[names], fraction], ...], caption?, caption_at?, caption_y?, caption_size?, static?}
           names: right files parts quote agents merge gate checks skill prod op
"""
import render as R
from render import (W, H, BG, PANEL, PANEL_HI, TEXT, DIM, DIMMER, ACCENT, ACCENT_D,
                    AMBER, AMBER_D, ease, mix, fade, text_w, letterspace, check)
from se201_layouts_58b import (font, ctext, box, fit, spaced_w, fit_spaced, dashed_box, harrow, varrow,
                               lines_centered, caption)

X0, X1 = 115, 1805
BAN_Y, BAN_H = 268, 62          # 1: what right means
TAG_Y = 356                     # lesson tags over the build row
BY, BH = 396, 150               # the build row
PART_X, PART_W = [425, 620, 812, 1004], [175, 171, 171, 171]
PART_Y, PART_H = 474, 72
QX, QW, QH = 620, 555, 52       # the shared node
MX, MW = 1245, 255              # the merge point
GX, GW = 1570, 235              # the person who decides
SUB_Y = 556                     # tags under the build row
LY, LH = 606, 236               # lower area: panel, log, or production
CAP_Y = 868


def _chip(d, cx, cy, n, a, mode, r=15):
    """the number of the lesson an element comes from"""
    f = font(17 if r >= 15 else 15)
    if mode == "lit":
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fade(ACCENT, a))
        col = fade(BG, 1.0) if a > 0.5 else fade(ACCENT, a)
    elif mode == "on":
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=fade(DIM, a), width=2)
        col = fade(TEXT, a * 0.85)
    else:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=fade(DIMMER, a), width=2)
        col = fade(DIMMER, a)
    s = str(n)
    ctext(d, cx, cy - int(f.size * 0.6), s, f, col)


def _tag(d, x, y, n, text, a, mode, size=16):
    _chip(d, x + 15, y + 14, n, a, mode)
    col = ACCENT if mode == "lit" else DIM if mode == "on" else DIMMER
    return letterspace(d, (x + 40, y + 5), text, font(size), fade(col, a), sp=3)


def _person(d, cx, cy, col, s=1.0):
    r = int(13 * s)
    d.ellipse([cx - r, cy - int(30 * s), cx + r, cy - int(30 * s) + 2 * r], outline=col, width=3)
    d.arc([cx - int(24 * s), cy + int(2 * s), cx + int(24 * s), cy + int(50 * s)], 180, 360, fill=col, width=3)


def _fill_bar(d, x, y, w, h, prog, col, r=12):
    """a box filling left to right: work in progress"""
    pw = int(w * max(0.0, min(1.0, prog)))
    if pw > 2 * r:
        d.rounded_rectangle([x, y, x + pw, y + h], radius=r, fill=col)


def _lines(d, x, y, lines, f, col_of, lead=1.36):
    lh = int(f.size * lead)
    for j, ln in enumerate(lines):
        c = col_of(j, ln)
        if c is not None:
            d.text((x, y + j * lh), ln.lstrip("!+~"), font=f, fill=c)


def _tone(ln, a):
    return fade(AMBER if ln.startswith("!") else ACCENT if ln.startswith("+") else DIM if ln.startswith("~") else TEXT, a)


# ------------------------------------------------------------------ lower area: what was written down
def _frame(d, a, lw, col=DIMMER):
    fa = 1.0 if lw.get("frame_held") else a
    box(d, X0, LY, X1 - X0, LH, fade(PANEL, fa * 0.55), fade(col, fa), 2, r=20)


def _lower_panel(d, t, dur, lw, static):
    a = 1.0 if static else ease((t - lw.get("at", 0.04) * dur) / 0.5)
    _frame(d, a, lw)
    cols = lw["cols"]
    tot = sum(c.get("w", 1) for c in cols)
    inner = X1 - X0 - 60
    x = X0 + 30
    for k, c in enumerate(cols):
        cw = int(inner * c.get("w", 1) / tot) - 24
        c_at = c.get("at", lw.get("at", 0.04))
        ca = 1.0 if static else ease((t - c_at * dur) / 0.5)
        if k > 0:
            d.line([(x - 18, LY + 22), (x - 18, LY + LH - 22)], fill=fade(DIMMER, a * 0.8), width=2)
        hcol = ACCENT if c.get("tone") == "accent" else AMBER if c.get("tone") == "amber" else DIM
        letterspace(d, (x, LY + 20), c["head"], fit_spaced(d, c["head"], cw, 16, 3), fade(hcol, ca), sp=3)
        lines = c["lines"]
        f = fit(d, [ln.lstrip("!+~") for ln in lines], cw, c.get("size", 30), bold=c.get("bold", True), mono=c.get("mono", False))
        ats = c.get("ats")
        step = c.get("step", 0.07)

        def col_of(j, ln, ats=ats, c_at=c_at, step=step):
            la = 1.0 if static else ease((t - (ats[j] if ats else c_at + 0.03 + j * step) * dur) / 0.45)
            return _tone(ln, la) if la > 0 else None
        _lines(d, x, LY + 62 + c.get("dy", 0), lines, f, col_of, lead=c.get("lead", 1.4))
        x += cw + 24 + 12


def _lower_days(d, t, dur, lw, static):
    """a billing period as a row of days: the days used, the days paid for and not used, and what that is worth"""
    a = 1.0 if static else ease((t - lw.get("at", 0.04) * dur) / 0.5)
    _frame(d, a, lw)
    letterspace(d, (X0 + 30, LY + 20), lw["head"], font(16), fade(DIM, a), sp=3)
    n, used = lw.get("days", 30), lw.get("used", 10)
    cw, cg, ch = 25, 5, 50
    bx, by = X0 + 30, LY + 62
    ua = 1.0 if static else ease((t - lw.get("used_at", 0.1) * dur) / 0.5)
    fa = 1.0 if static else ease((t - lw.get("free_at", 0.3) * dur) / 0.6)
    for k in range(n):
        x = bx + k * (cw + cg)
        if k < used:
            box(d, x, by, cw, ch, fade(PANEL_HI, a), fade(mix(DIMMER, DIM, ua), a), 2, r=6)
        else:
            ka = 1.0 if static else ease((t - lw.get("free_at", 0.3) * dur - (k - used) * 0.03) / 0.35)
            box(d, x, by, cw, ch, mix(fade(BG, a), ACCENT_D, ka * 0.85), mix(fade(DIMMER, a), ACCENT, ka), 2, r=6)
    f = font(17)
    letterspace(d, (bx, by + ch + 14), lw["used_label"], f, fade(DIM, ua), sp=3)
    letterspace(d, (bx + used * (cw + cg), by + ch + 14), lw["free_label"], f, fade(ACCENT, fa), sp=3)
    ra = 1.0 if static else ease((t - lw.get("rule_at", 0.2) * dur) / 0.5)
    d.text((bx, by + ch + 60), lw["rule"], font=fit(d, [lw["rule"]], n * (cw + cg), 30), fill=fade(TEXT, ra))
    # the sum, on the right
    sx0, sx1 = bx + n * (cw + cg) + 56, X1 - 34
    d.line([(sx0 - 28, LY + 22), (sx0 - 28, LY + LH - 22)], fill=fade(DIMMER, a * 0.8), width=2)
    rows = lw["sum"]
    rf, af = font(27, bold=False), font(29, mono=True)
    for j, r in enumerate(rows):
        la = 1.0 if static else ease((t - r.get("at", 0.5 + 0.1 * j) * dur) / 0.45)
        y = LY + 40 + j * 54
        last = j == len(rows) - 1
        if last:
            d.line([(sx0, y - 4), (sx1, y - 4)], fill=fade(DIMMER, la), width=2)
            y += 8
        col = ACCENT if last else TEXT
        d.text((sx0, y), r["label"], font=font(27) if last else rf, fill=fade(col, la))
        d.text((sx1 - text_w(d, r["amount"], af), y - 2), r["amount"], font=af, fill=fade(col, la))


def _lower_log(d, t, dur, lw, static):
    """the build as it runs: one line per thing that happened, ticked as it lands"""
    a = 1.0 if static else ease((t - lw.get("at", 0.02) * dur) / 0.5)
    _frame(d, a, lw)
    letterspace(d, (X0 + 30, LY + 20), lw["head"], font(16), fade(DIM, a), sp=3)
    rows = lw["rows"]
    per = lw.get("per_col", 3)
    ncol = (len(rows) + per - 1) // per
    cw = (X1 - X0 - 60) // ncol
    f = fit(d, [r["text"] for r in rows], cw - 80, 32 if per <= 3 else 29)
    for k, r in enumerate(rows):
        la = 1.0 if static else ease((t - r["at"] * dur) / 0.45)
        if la <= 0:
            continue
        x = X0 + 30 + (k // per) * cw
        y = LY + 62 + (k % per) * ((LH - 74) // per)
        col = ACCENT if r.get("tone") == "accent" else TEXT
        check(d, x + 15, y + 17, 13, la)
        d.text((x + 46, y), r["text"], font=f, fill=fade(col, la))


def _lower_prod(d, t, dur, lw, static, lit, show, al):
    """production: a trigger, a row of steps with what each one leaves, and the agent that operates it"""
    a = 1.0 if (static or lw.get("held")) else ease((t - lw.get("at", 0.04) * dur) / 0.5)
    on = "prod" in lit
    _frame(d, a, lw, ACCENT if on else DIMMER)
    x = _tag(d, X0 + 22, LY + 12, 8, lw["tag"], a, "lit" if on else "on")
    trig = lw.get("trigger")
    if trig:
        ta = 1.0 if (static or lw.get("held")) else ease((t - lw.get("trigger_at", 0.12) * dur) / 0.5)
        tf = font(17)
        tw = spaced_w(d, trig, tf, 3) + 40
        box(d, x + 22, LY + 10, tw, 36, fade(AMBER_D, ta * 0.7), fade(AMBER, ta), 2, r=18)
        letterspace(d, (x + 42, LY + 18), trig, tf, fade(TEXT, ta), sp=3)
    stages = lw["stages"]
    n = len(stages)
    sx0, sw, sg, sy, sh = X0 + 25, 200, 38, LY + 74, 76
    xs = [sx0 + i * (sw + sg) for i in range(n)]
    foc = lw.get("focus")
    for i, s in enumerate(stages):
        sa = 1.0 if (static or lw.get("held")) else ease((t - s.get("at", 0.15 + 0.1 * i) * dur) / 0.5)
        if sa <= 0:
            continue
        hot = foc == i
        tone = s.get("tone")
        col = ACCENT if hot else AMBER if tone == "amber" else DIMMER
        if i > 0 and not s.get("apart"):
            harrow(d, xs[i - 1] + sw + 6, sy + sh // 2, xs[i] - 8, fade(DIM, sa * 0.85), width=3, head=11, prog=sa)
        if s.get("apart"):
            lx = xs[i] - sg // 2
            for yy in range(LY + 16, LY + LH - 16, 16):
                d.line([(lx, yy), (lx, yy + 8)], fill=fade(DIMMER, sa), width=2)
        if s.get("trigger"):
            tf2 = font(17)
            tw2 = spaced_w(d, s["trigger"], tf2, 3) + 40
            box(d, xs[i], LY + 10, tw2, 36, fade(AMBER_D, sa * 0.7), fade(AMBER, sa), 2, r=18)
            letterspace(d, (xs[i] + 20, LY + 18), s["trigger"], tf2, fade(TEXT, sa), sp=3)
        box(d, xs[i], sy, sw, sh, fade(ACCENT_D if hot else PANEL, sa * (0.7 if hot else 0.92)), fade(col, sa), 3 if (hot or tone) else 2, r=14)
        lines = s["name"].split("\n")
        lines_centered(d, xs[i] + sw // 2, sy + sh // 2, lines, fit(d, lines, sw - 24, 27), fade(TEXT, sa))
        notes = s.get("notes", [])
        na = 1.0 if (static or lw.get("held") and not s.get("notes_at")) else ease((t - s.get("notes_at", s.get("at", 0.2) + 0.06) * dur) / 0.5)
        nf = fit(d, [x_.lstrip("!+~") for x_ in notes] or [""], sw + sg - 14, 21, bold=False, floor=15)
        for j, ln in enumerate(notes):
            ctext(d, xs[i] + sw // 2, sy + sh + 12 + j * 28, ln.lstrip("!+~"), nf, _tone(ln, na))
    # 9: the agent that operates it
    op = lw.get("op")
    if op:
        ox = xs[-1] + sw + 44
        ow = X1 - 20 - ox
        oy, oh = LY + 10, LH - 20
        if "op" in show:
            oa = al("op")
            on9 = "op" in lit
            box(d, ox, oy, ow, oh, fade(ACCENT_D if on9 else PANEL, oa * (0.35 if on9 else 0.9)), fade(ACCENT if on9 else DIMMER, oa), 3 if on9 else 2, r=16)
            _tag(d, ox + 14, oy + 8, 9, op["tag"], oa, "lit" if on9 else "on")
            ac, ay_, ax_ = fade(ACCENT if on9 else DIM, oa), sy + sh // 2, xs[-1] + sw + 8   # the operator runs the last step
            d.line([(ax_ + 8, ay_), (ox - 4, ay_)], fill=ac, width=3)
            d.polygon([(ax_, ay_), (ax_ + 11, ay_ - 7), (ax_ + 11, ay_ + 7)], fill=ac)
            idf = fit(d, [op["id"]], ow - 36, 23, mono=True)
            ia = 1.0 if static else ease((t - op.get("id_at", 0.1) * dur) / 0.5)
            d.text((ox + 18, oy + 46), op["id"], font=idf, fill=fade(TEXT, min(oa, ia)))
            lf = fit(d, [x_.lstrip("!+~") for x_ in op["lines"]], ow - 36, 21, bold=False, floor=15)
            ats = op.get("ats")
            for j, ln in enumerate(op["lines"]):
                la = 1.0 if static or not ats else ease((t - ats[j] * dur) / 0.45)
                d.text((ox + 18, oy + 82 + j * 25), ln.lstrip("!+~"), font=lf, fill=_tone(ln, min(oa, la)))
        else:
            dashed_box(d, ox, oy, ow, oh, fade(DIMMER, a * 0.8), width=2)
            _chip(d, ox + 29, oy + 22, 9, a, "ghost")


# ------------------------------------------------------------------ the map
def scene_buildmap(d, t, dur, data):
    """one small feature built end to end; every element lights up with the lesson it comes from"""
    static = data.get("static", False)
    m = data["map"]
    show, ats = set(data.get("show", [])), data.get("ats", {})
    lit = set(data.get("lit", []))
    for names, at in data.get("pulse", []):      # the recap: the map lights up again, in order
        if static or t >= at * dur:
            lit |= set(names)
    ghost = data.get("ghost", True)

    def al(name):
        if name not in show:
            return 0.0
        if static or name not in ats:
            return 1.0
        return ease((t - ats[name] * dur) / 0.5)

    def mode(name):
        return "lit" if name in lit else "on"

    built, go = data.get("built"), data.get("go", {})

    def bp(name, span=0.5):
        if built is True or (built and static):
            return 1.0
        if built == "go":
            return ease((t - go.get(name, 0.5) * dur) / span)
        return 0.0

    bd1 = data.get("build_dim", 1.0)
    bd0 = data.get("build_dim_from", bd1)
    bd = bd1 if static else bd0 + (bd1 - bd0) * ease(t / 0.7)

    a0 = 1.0 if static else ease(t / 0.4)
    letterspace(d, (X0, 226), data["label"], font(21), fade(mix(DIMMER, DIM, 0.6), 1.0 if data.get("label_held") else a0), sp=5)

    # ---- 1: what right means
    a = al("right")
    if ghost and a < 1:
        dashed_box(d, X0, BAN_Y, X1 - X0, BAN_H, fade(DIMMER, (1 - a) * 0.7), width=2)
        _chip(d, X0 + 34, BAN_Y + BAN_H // 2, 1, (1 - a) * 0.9, "ghost")
    if a > 0:
        on = "right" in lit
        box(d, X0, BAN_Y, X1 - X0, BAN_H, fade(PANEL, a * 0.92 * bd), fade(ACCENT if on else DIMMER, a * bd), 3 if on else 2, r=16)
        _chip(d, X0 + 34, BAN_Y + BAN_H // 2, 1, a * bd, mode("right"))
        x = letterspace(d, (X0 + 62, BAN_Y + 21), "RIGHT MEANS", font(17), fade(ACCENT if on else DIM, a * bd), sp=4)
        d.text((x + 18, BAN_Y + 12), m["right"], font=fit(d, [m["right"]], X1 - x - 18 - 360, 31), fill=fade(TEXT, a * bd))
        ca = al("checks")
        if ca > 0:
            lab = m.get("right_checks", "AS CHECKS")
            lw_ = spaced_w(d, lab, font(16), 3)
            _tag(d, X1 - 26 - lw_ - 40, BAN_Y + 17, 6, lab, ca * bd, mode("checks"))

    # ---- 2: readable
    a = al("files")
    fw = 260
    if ghost and a < 1:
        dashed_box(d, X0, BY, fw, BH, fade(DIMMER, (1 - a) * 0.7), width=2)
        _chip(d, X0 + 15, TAG_Y + 14, 2, (1 - a) * 0.9, "ghost")
    if a > 0:
        on = "files" in lit
        _tag(d, X0, TAG_Y, 2, m.get("files_tag", "READABLE"), a * bd, mode("files"))
        box(d, X0, BY, fw, BH, fade(PANEL, a * 0.92 * bd), fade(ACCENT if on else DIMMER, a * bd), 3 if on else 2)
        ff = font(23, mono=True)
        for j, ln in enumerate(m["files"]):
            fa = 1.0 if (static or "files" not in ats) else ease((t - (ats["files"] + 0.06 + j * data.get("file_step", 0.1)) * dur) / 0.45)
            d.text((X0 + 24, BY + 16 + j * 31), ln, font=ff, fill=fade(DIM if j == 0 else TEXT, a * fa * bd))

    # ---- 3: the graph. Four parts, and the one thing three of them share
    a = al("parts")
    qa = al("quote")
    if ghost and a < 1:
        for k in range(4):
            dashed_box(d, PART_X[k], PART_Y, PART_W[k], PART_H, fade(DIMMER, (1 - a) * 0.7), width=2)
        _chip(d, PART_X[0] + 15, TAG_Y + 14, 3, (1 - a) * 0.9, "ghost")
    if ghost and qa < 1:
        dashed_box(d, QX, BY, QW, QH, fade(DIMMER, (1 - qa) * 0.7), width=2)
    if a > 0:
        on = "parts" in lit
        _tag(d, PART_X[0], TAG_Y, 3, m.get("parts_tag", "THE GRAPH"), a * bd, mode("parts"))
        pstep = data.get("part_step", 0.08)
        skill_on = "skill" in lit
        agents_on = "agents" in lit
        for k, p in enumerate(m["parts"]):
            pa = 1.0 if (static or "parts" not in ats) else ease((t - (ats["parts"] + k * pstep) * dur) / 0.5)
            if pa <= 0:
                continue
            x, w = PART_X[k], PART_W[k]
            hot = on or (k == 0 and skill_on) or (k > 0 and agents_on)
            prog = bp("parts", span=max(0.3, (go.get("parts_end", 0.3) - go.get("parts", 0.1)) * dur)) if built else 0.0
            box(d, x, PART_Y, w, PART_H, fade(PANEL, pa * 0.92 * bd), None, r=12)
            if prog > 0:
                _fill_bar(d, x, PART_Y, w, PART_H, prog, fade(ACCENT_D, 0.8 * bd))
            done = prog >= 0.999
            d.rounded_rectangle([x, PART_Y, x + w, PART_Y + PART_H], radius=12,
                                outline=fade(ACCENT if (hot or done) else DIMMER, pa * bd), width=3 if hot else 2)
            lines = p["name"].split("\n")
            lines_centered(d, x + w // 2, PART_Y + PART_H // 2, lines, fit(d, lines, w - 22, 23), fade(TEXT, pa * bd))
    if qa > 0:
        on = "quote" in lit
        box(d, QX, BY, QW, QH, fade(ACCENT_D if on else PANEL, qa * (0.55 if on else 0.92) * bd), fade(ACCENT if on else DIMMER, qa * bd), 3 if on else 2, r=14)
        qf, sf = font(25), font(21, bold=False)
        sub = data.get("quote_sub", m.get("quote_sub", ""))
        tw = text_w(d, m["quote"], qf) + (22 + text_w(d, sub, sf) if sub else 0)
        qx = QX + (QW - tw) // 2
        d.text((qx, BY + 11), m["quote"], font=qf, fill=fade(TEXT, qa * bd))
        if sub:
            d.text((qx + text_w(d, m["quote"], qf) + 22, BY + 14), sub, font=sf, fill=fade(ACCENT if on else DIM, qa * bd))
        ac = fade(ACCENT if on else DIM, qa * bd)
        ux = PART_X[1] + PART_W[1] // 2      # "calculate" writes the quote: its arrow points up into it
        d.line([(ux, PART_Y - 4), (ux, BY + QH + 10)], fill=ac, width=3)
        d.polygon([(ux, BY + QH + 3), (ux - 6, BY + QH + 12), (ux + 6, BY + QH + 12)], fill=ac)
        for k in (2, 3):                     # the other two read it
            varrow(d, PART_X[k] + PART_W[k] // 2, BY + QH + 3, PART_Y - 4, ac, width=3, head=9, prog=qa)

    # ---- 4: one agent per new part, and one merge point
    a = al("agents")
    if a > 0:
        on = "agents" in lit
        af = font(17)
        for k in (1, 2, 3):
            lab = m["agents"][k - 1]
            ka = a if (static or "agents" not in ats) else ease((t - (ats["agents"] + (k - 1) * 0.05) * dur) / 0.45)
            letterspace(d, (PART_X[k] + PART_W[k] // 2 - spaced_w(d, lab, af, 3) // 2, SUB_Y + 5), lab, af, fade(ACCENT if on else DIM, ka * bd), sp=3)
    a = al("merge")
    if ghost and a < 1:
        dashed_box(d, MX, BY, MW, BH, fade(DIMMER, (1 - a) * 0.7), width=2)
        _chip(d, MX + 15, TAG_Y + 14, 4, (1 - a) * 0.9, "ghost")
    if a > 0:
        on = "merge" in lit
        mp = bp("merge")
        tx = _tag(d, MX, TAG_Y, 4, m.get("merge_tag", "ONE MERGE POINT"), a * bd, mode("merge"))
        harrow(d, PART_X[3] + PART_W[3] + 8, PART_Y + PART_H // 2, MX - 8, fade(mix(DIM, ACCENT, mp), a * 0.9 * bd), width=3, head=11, prog=a)
        if built == "go" and not static:     # the parts arrive at the merge point
            pk = (t - (go.get("merge", 0.4) * dur - 0.7)) / 0.7
            if 0 < pk < 1:
                px = PART_X[3] + PART_W[3] + 8 + (MX - 16 - PART_X[3] - PART_W[3]) * ease(pk)
                d.ellipse([px - 8, PART_Y + PART_H // 2 - 8, px + 8, PART_Y + PART_H // 2 + 8], fill=ACCENT)
        box(d, MX, BY, MW, BH, mix(fade(PANEL, a * 0.92 * bd), fade(ACCENT_D, 0.8 * bd), mp), fade(ACCENT if (on or mp >= 1) else DIMMER, a * bd), 3 if on else 2)
        lines = m["merge"]
        d.text((MX + 22, BY + 22), lines[0], font=fit(d, [lines[0]], MW - 44, 28), fill=fade(TEXT, a * bd))
        sf = fit(d, lines[1:], MW - 44, 21, bold=False)
        for j, ln in enumerate(lines[1:]):
            d.text((MX + 22, BY + 70 + j * 29), ln, font=sf, fill=fade(mix(DIM, TEXT, mp), a * bd))
        if mp > 0:
            check(d, tx + 16, TAG_Y + 14, 11, mp * bd)
    # ---- 6: the checks, run before it ships
    a = al("checks")
    if a > 0:
        cp = bp("checks")
        on = "checks" in lit
        x = _tag(d, MX, SUB_Y - 6, 6, m.get("checks_tag", "CHECKS, BEFORE"), a * bd, "lit" if on else "on", size=15)
        if cp > 0:
            check(d, x + 18, SUB_Y + 8, 11, cp * bd)
    # ---- 7: the part that is already a skill
    a = al("skill")
    if al("agents") > 0 and a < 1 and m.get("plan_note"):
        na_ = al("agents") * (1 - a)
        lab = m["plan_note"]
        letterspace(d, (PART_X[0] + PART_W[0] // 2 - spaced_w(d, lab, font(17), 3) // 2, SUB_Y + 5), lab, font(17), fade(DIM, na_ * bd), sp=3)
    if ghost and a < 1 and al("agents") <= 0:
        _chip(d, PART_X[0] + 49, SUB_Y + 8, 7, (1 - a) * 0.9, "ghost")
    if ghost and al("checks") < 1:
        _chip(d, MX + 15, SUB_Y + 8, 6, (1 - al("checks")) * 0.9, "ghost")
    if a > 0:
        _tag(d, PART_X[0] + 34, SUB_Y - 6, 7, m.get("skill_tag", "A SKILL"), a * bd, mode("skill"), size=15)

    # ---- 5: the person who decides
    a = al("gate")
    if ghost and a < 1:
        dashed_box(d, GX, BY, GW, BH, fade(DIMMER, (1 - a) * 0.7), width=2)
        _chip(d, GX + 15, TAG_Y + 14, 5, (1 - a) * 0.9, "ghost")
    if a > 0:
        on = "gate" in lit
        gp = bp("gate")
        _tag(d, GX, TAG_Y, 5, m.get("gate_tag", "WHO DECIDES"), a * bd, mode("gate"))
        harrow(d, MX + MW + 8, BY + BH // 2, GX - 8, fade(mix(DIM, ACCENT, gp), min(a, al("merge")) * 0.9 * bd), width=3, head=11, prog=a)
        box(d, GX, BY, GW, BH, mix(fade(AMBER_D if on else PANEL, a * (0.6 if on else 0.92) * bd), fade(ACCENT_D, 0.8 * bd), gp),
            mix(fade(AMBER if on else DIMMER, a * bd), fade(ACCENT, bd), gp), 3 if (on or gp > 0) else 2)
        _person(d, GX + 44, BY + 58, mix(fade(AMBER if on else DIM, a * bd), fade(ACCENT, bd), gp))
        lines = m["gate"].split("\n")
        gf = fit(d, lines, GW - 100, 27)
        for j, ln in enumerate(lines):
            d.text((GX + 82, BY + 20 + j * 33), ln, font=gf, fill=fade(TEXT, a * bd))
        sub = m.get("gate_yes", "Says yes") if gp > 0.5 else m.get("gate_sub", "")
        d.text((GX + 22, BY + 104), sub, font=fit(d, [sub], GW - 44, 21, bold=gp > 0.5), fill=fade(ACCENT if gp > 0.5 else DIM, a * bd))
        if gp > 0:
            check(d, GX + GW - 28, BY + 118, 13, gp * bd)
        sp_ = bp("ship")
        if sp_ > 0:
            varrow(d, GX + GW // 2, BY + BH + 6, LY - 6, fade(ACCENT, sp_ * bd), width=4, head=13, prog=sp_)
            lab = m.get("ship", "SHIPS")
            letterspace(d, (GX + GW // 2 - 24 - spaced_w(d, lab, font(16), 3), BY + BH + 22), lab, font(16), fade(ACCENT, sp_ * bd), sp=3)

    # ---- the lower area
    lw = data.get("lower")
    if lw:
        kind = lw.get("kind", "panel")
        if kind == "panel":
            _lower_panel(d, t, dur, lw, static)
        elif kind == "days":
            _lower_days(d, t, dur, lw, static)
        elif kind == "log":
            _lower_log(d, t, dur, lw, static)
        elif kind == "prod":
            _lower_prod(d, t, dur, lw, static, lit, show, al)

    # ---- what never changes: the four constants, under all of it
    cs = data.get("consts")
    if cs:
        items = cs["items"]
        n = len(items)
        g = 18
        cw = (X1 - X0 - (n - 1) * g) // n
        hsz = min(fit(d, [it["head"]], cw - 40, 24).size for it in items)
        for k, it in enumerate(items):
            ca = 1.0 if (static or cs.get("held")) else ease((t - (it.get("at", cs.get("at", 0.1) + k * cs.get("step", 0.2))) * dur) / 0.5)
            if ca <= 0:
                continue
            x = X0 + k * (cw + g)
            box(d, x, CAP_Y, cw, 108, fade(PANEL, ca * 0.92), fade(ACCENT, ca), 2, r=16)
            d.text((x + 20, CAP_Y + 16), it["head"], font=font(hsz), fill=fade(TEXT, ca))
            ba = 1.0 if (static or cs.get("held")) else ease((t - (it.get("text_at", it.get("at", 0) + 0.05)) * dur) / 0.5)
            d.text((x + 20, CAP_Y + 58), it["text"], font=fit(d, [it["text"]], cw - 40, 26), fill=fade(ACCENT, min(ca, ba)))
    caption(d, t, dur, data, X0, CAP_Y, 42)


R.RENDERERS.update({"buildmap": scene_buildmap})
