"""SE201 lesson 9 layouts. Imported by render_se101.py.

accessmap      one agent, and what it can reach. Left: the agent's card (its identity, its job, its owner). Middle:
               one row per action. Right: the system each action would touch. Between them, one vertical line: the
               place where access is enforced. An allowed action crosses the line; a denied one stops at it.
               A strip under the map holds the limits (a cap, a stop switch, an owner).
               data: {label, agent: {tag, id, id_at, lines: [..], ats: [..], sections: [{head, lines, at}], held?},
                      gate?: {text, at, held?},
                      groups: [{head, tone: accent|amber, at, held?, rows: [{verb, target, sub?, state: allow|deny|part, at}]}],
                      row_h?, foot?: [{head, text, sub?, tone, at}], foot_held?,
                      caption?, caption_at?, caption_y?, caption_size?, caption_tone?, static?}
trail          one night's work, and the trail it leaves. Top left: two counts that should match, and what the agent
               found. Top right: what it does next (a tick) and what it can't do (a cross, with the reason).
               Bottom: the audit log, filling in one line per action: when, who, what, why, result.
               data: {label, counts: {left: {head, value, unit}, right: {...}, at, right_at, diff_at,
                                      finding: [lines], finding_at, held?},
                      acts: {head, at, held?, items: [{text, why?, state: ok|no, at}]},
                      log: {head, note?, note_at?, cols: [5 names], at, held?: n rows already shown,
                            rows: [{cells: [5], person?: bool, at}], hi_col?: int, hi_at?},
                      caption?, caption_at?, caption_y?, caption_size?, static?}
access_review  a review of one identity's access: one row per permission, two questions asked of each (does the job
               need it? has it been used?), and a decision. Under it, why a spare permission matters: a line of text
               the agent didn't write, and what happens with the permission, and without it.
               data: {label, head, head_at?, origin?: {text, at}, cols: [4 names], cols_at?: [..],
                      rows: [{cells: [3], state: keep|remove, decision, at, decide_at}],
                      inject?: {head, line, at, with: {head, text, at}, without: {head, text, at}},
                      caption?, caption_at?, caption_y?, caption_size?, static?}
"""
import render as R
from render import (W, H, BG, PANEL, PANEL_HI, TEXT, DIM, DIMMER, ACCENT, ACCENT_D,
                    AMBER, AMBER_D, ease, mix, fade, text_w, letterspace, check)
from se201_layouts_58b import (font, ctext, box, fit, spaced_w, fit_spaced, dashed_box, harrow, lines_centered, caption)

X0, X1 = 115, 1805
LABEL_Y = 226
KO = (14, 20, 26)               # a knock-out behind an icon: nearly BG, but drawn on purpose


class _Clean:
    """Wraps the frame's draw object and skips anything faded all the way out. fade(c, 0) is the flat BG colour,
    which shows as a faint ghost on the gradient plate, so text would be readable before its cue."""
    def __init__(self, d):
        self._d = d

    def __getattr__(self, name):
        return getattr(self._d, name)

    def text(self, xy, s, font=None, fill=None, **k):
        if fill != BG:
            self._d.text(xy, s, font=font, fill=fill, **k)

    def line(self, pts, fill=None, **k):
        if fill != BG:
            self._d.line(pts, fill=fill, **k)

    def arc(self, box_, a0, a1, fill=None, **k):
        if fill != BG:
            self._d.arc(box_, a0, a1, fill=fill, **k)

    def polygon(self, pts, fill=None, outline=None, **k):
        if not (fill in (None, BG) and outline in (None, BG)):
            self._d.polygon(pts, fill=fill, outline=outline, **k)

    def rounded_rectangle(self, box_, radius=0, fill=None, outline=None, **k):
        if not (fill in (None, BG) and outline in (None, BG)):
            self._d.rounded_rectangle(box_, radius=radius, fill=None if fill == BG else fill, outline=None if outline == BG else outline, **k)

    def ellipse(self, box_, fill=None, outline=None, **k):
        if not (fill in (None, BG) and outline in (None, BG)):
            self._d.ellipse(box_, fill=None if fill == BG else fill, outline=None if outline == BG else outline, **k)


def _cross(d, cx, cy, r, a, col=AMBER):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=fade(col, a), width=3)
    k = r * 0.38
    d.line([(cx - k, cy - k), (cx + k, cy + k)], fill=fade(col, a), width=4)
    d.line([(cx - k, cy + k), (cx + k, cy - k)], fill=fade(col, a), width=4)


def _person(d, cx, cy, col, s=1.0):
    r = int(11 * s)
    d.ellipse([cx - r, cy - int(24 * s), cx + r, cy - int(24 * s) + 2 * r], outline=col, width=3)
    d.arc([cx - int(19 * s), cy + int(3 * s), cx + int(19 * s), cy + int(41 * s)], 180, 360, fill=col, width=3)


def _badge(d, x, y, col, bg):
    """an identity badge: a card with a face and two lines"""
    d.rounded_rectangle([x, y, x + 44, y + 32], radius=6, fill=bg, outline=col, width=2)
    d.ellipse([x + 7, y + 8, x + 19, y + 20], outline=col, width=2)
    d.line([(x + 24, y + 11), (x + 37, y + 11)], fill=col, width=2)
    d.line([(x + 24, y + 19), (x + 34, y + 19)], fill=col, width=2)


def _tone(ln, a):
    return fade(AMBER if ln.startswith("!") else ACCENT if ln.startswith("+") else DIM if ln.startswith("~") else TEXT, a)


def _strip(ln):
    return ln.lstrip("!+~")


def _label(d, data, a0):
    letterspace(d, (X0, LABEL_Y), data["label"], fit_spaced(d, data["label"], X1 - X0, 21, 5),
                fade(mix(DIMMER, DIM, 0.6), 1.0 if data.get("label_held") else a0), sp=5)


# ------------------------------------------------------------------ accessmap
AX, AW = X0, 440                # the agent's card
VX, VW = 640, 372               # the action
GATE_X = 1132                   # where access is enforced
TX, TW = 1252, X1 - 1252        # the system it would touch
MAP_Y = 322


def scene_accessmap(d, t, dur, data):
    """one agent: who it is, what it may do, what it can't, and the one line every action has to cross"""
    d = _Clean(d)
    static = data.get("static", False)
    a0 = 1.0 if static else ease(t / 0.4)
    _label(d, data, a0)

    def at(frac, span=0.5, held=False):
        return 1.0 if (static or held) else ease((t - frac * dur) / span)

    groups = data.get("groups", [])
    rh = data.get("row_h", 54)
    rg = data.get("row_gap", 10)
    # ---- where the rows go
    y = MAP_Y
    plan = []
    for g in groups:
        plan.append(("head", g, y))
        y += 34
        for r in g["rows"]:
            plan.append(("row", (g, r), y))
            y += rh + rg
        y += 12
    map_bot = max(y - rg - 12, MAP_Y + data.get("min_h", 454))

    # ---- the agent's card
    ag = data["agent"]
    ah = ag.get("held", False)
    aa = at(ag.get("at", 0.03), held=ah)
    box(d, AX, MAP_Y - 34, AW, map_bot - MAP_Y + 34, fade(PANEL, aa * 0.92), fade(ACCENT if ag.get("lit") else DIMMER, aa), 3 if ag.get("lit") else 2, r=20)
    _badge(d, AX + 24, MAP_Y - 14, fade(ACCENT, aa), fade(ACCENT_D, aa * 0.6))
    letterspace(d, (AX + 82, MAP_Y - 7), ag["tag"], font(18), fade(ACCENT, aa), sp=4)
    ia = at(ag.get("id_at", 0.1), held=ah)
    idf = fit(d, [ag["id"]], AW - 48, 31, mono=True)
    d.text((AX + 24, MAP_Y + 34), ag["id"], font=idf, fill=fade(TEXT, min(aa, ia)))
    lf = fit(d, [_strip(x) for x in ag.get("lines", [""])], AW - 48, 27, bold=False)
    ats = ag.get("ats")
    cy = MAP_Y + 86
    for j, ln in enumerate(ag.get("lines", [])):
        la = at(ats[j], 0.45, ah) if ats else aa
        d.text((AX + 24, cy), _strip(ln), font=lf, fill=_tone(ln, min(aa, la)))
        cy += 36
    for s in ag.get("sections", []):
        sh = ah or s.get("held", False)
        sa = min(aa, at(s.get("at", 0.5), held=sh))
        cy += 12
        d.line([(AX + 24, cy), (AX + AW - 24, cy)], fill=fade(DIMMER, sa * 0.9), width=2)
        cy += 16
        letterspace(d, (AX + 24, cy), s["head"], font(16), fade(ACCENT if s.get("tone") == "accent" else DIM, sa), sp=3)
        cy += 30
        sf = fit(d, [_strip(x) for x in s["lines"]], AW - 48, s.get("size", 25))
        sats = s.get("ats")
        for j, ln in enumerate(s["lines"]):
            la = min(sa, at(sats[j], 0.45, sh)) if sats else sa
            d.text((AX + 24, cy), _strip(ln), font=sf, fill=_tone(ln, la))
            cy += int(sf.size * 1.34)

    # ---- the line every action has to cross
    gate = data.get("gate")
    ga = 0.0
    if gate:
        ga = at(gate.get("at", 0.1), held=gate.get("held", False))
        for yy in range(MAP_Y - 4, int(map_bot) + 6, 16):
            d.line([(GATE_X, yy), (GATE_X, min(yy + 8, map_bot + 6))], fill=fade(DIM, ga * 0.9), width=3)
        gl = gate["text"].split("\n")
        gf = font(16)
        for k, ln in enumerate(gl):
            letterspace(d, (GATE_X - spaced_w(d, ln, gf, 3) // 2, MAP_Y - 34 - (len(gl) - k) * 23 + 21), ln, gf,
                        fade(mix(DIM, ACCENT, at(gate["lit_at"]) if "lit_at" in gate else 0.0), ga), sp=3)

    # ---- the rows
    spine = []
    for kind, item, yy in plan:
        if kind == "head":
            g = item
            ha = at(g.get("at", 0.1), held=g.get("held", False))
            col = AMBER if g.get("tone") == "amber" else ACCENT
            letterspace(d, (VX, yy + 4), g["head"], font(17), fade(col, ha), sp=4)
            if g.get("target_head"):
                letterspace(d, (TX, yy + 4), g["target_head"], font(17), fade(DIM, ha), sp=4)
            continue
        g, r = item
        held = g.get("held", False)
        ra = at(r.get("at", 0.2), held=held)
        if ra <= 0:
            continue
        state = r.get("state", "allow")
        ok = state == "allow"
        col = ACCENT if ok else AMBER
        cyy = yy + rh // 2
        spine.append((cyy, ra))
        # the action
        box(d, VX, yy, VW, rh, fade(PANEL, ra * 0.92), fade(mix(DIMMER, col, 0.75), ra), 2, r=14)
        vf = fit(d, [r["verb"]], VW - 40, 27)
        d.text((VX + 20, cyy - int(vf.size * 0.6)), r["verb"], font=vf, fill=fade(TEXT, ra))
        # the path
        pa = 1.0 if (static or held) else ease((t - (r.get("at", 0.2) * dur + 0.25)) / 0.6)
        if ok:
            harrow(d, VX + VW + 8, cyy, TX - 10, fade(ACCENT, ra * 0.95), width=4, head=14, prog=pa)
            if pa > 0.55:
                d.ellipse([GATE_X - 15, cyy - 15, GATE_X + 15, cyy + 15], fill=KO)
                check(d, GATE_X, cyy, 13, ease((pa - 0.55) / 0.3))
        else:
            xe = VX + VW + 8 + (GATE_X - 22 - VX - VW - 8) * pa
            d.line([(VX + VW + 8, cyy), (xe, cyy)], fill=fade(AMBER, ra * 0.95), width=4)
            if pa > 0.9:
                xa = ease((pa - 0.9) / 0.1)
                d.ellipse([GATE_X - 15, cyy - 15, GATE_X + 15, cyy + 15], fill=KO)
                _cross(d, GATE_X, cyy, 13, xa)
                for xx in range(GATE_X + 26, TX - 10, 18):      # the path that isn't there
                    d.line([(xx, cyy), (min(xx + 8, TX - 10), cyy)], fill=fade(DIMMER, ra * xa), width=3)
        # the system it would touch
        ta = ra if ok else ra * 0.9
        if ok:
            box(d, TX, yy, TW, rh, fade(ACCENT_D, ta * 0.35), fade(ACCENT, ta * (0.4 + 0.6 * pa)), 2, r=14)
        else:
            box(d, TX, yy, TW, rh, fade(PANEL, ta * 0.6), None, r=14)
            dashed_box(d, TX, yy, TW, rh, fade(mix(DIMMER, AMBER, 0.55), ta), width=2, dash=10, gap=8)
        sub = r.get("sub")
        if sub:
            mf = fit(d, [r["target"]], TW - 40, 26)
            sf = fit(d, [sub], TW - 40, 21, bold=False)
            d.text((TX + 20, yy + rh // 2 - mf.size - 4), r["target"], font=mf, fill=fade(TEXT, ta))
            d.text((TX + 20, yy + rh // 2 + 3), sub, font=sf, fill=fade(col if r.get("sub_tone") else DIM, ta))
        else:
            mf = fit(d, [r["target"]], TW - 40, 27)
            d.text((TX + 20, cyy - int(mf.size * 0.6)), r["target"], font=mf, fill=fade(TEXT if ok else mix(DIM, TEXT, 0.6), ta))
    # the agent's card feeds every action
    if spine:
        sx = AX + AW + (VX - AX - AW) // 2
        top, bot = spine[0][0], spine[-1][0]
        sa = max(a for _, a in spine)
        d.line([(AX + AW + 2, top), (sx, top)], fill=fade(DIM, sa * 0.9), width=3)
        d.line([(sx, top), (sx, bot)], fill=fade(DIM, sa * 0.9), width=3)
        for cyy, ra in spine:
            d.line([(sx, cyy), (VX - 6, cyy)], fill=fade(DIM, ra * 0.9), width=3)


    # ---- one login shared, against one identity each
    side = data.get("side")
    if side:
        ph = (map_bot - MAP_Y + 34 - 20) // 2
        mf_ = font(22, mono=True)      # both verdicts in one size: the one that fits beside the longer log line
        vx_max = max(VX + 128 + text_w(d, side[k_]["login"], mf_) + 40 + 44 + text_w(d, side[k_]["log"], mf_) + 40 + 22 for k_ in ("shared", "own"))
        for k, key in enumerate(("shared", "own")):
            p = side[key]
            pa = at(p.get("at", 0.3 + 0.3 * k))
            if pa <= 0:
                continue
            col = AMBER if k == 0 else ACCENT
            px, py, pw = VX, MAP_Y - 34 + k * (ph + 20), X1 - VX
            box(d, px, py, pw, ph, fade(PANEL, pa * 0.6), fade(mix(DIMMER, col, 0.6), pa), 2, r=20)
            letterspace(d, (px + 26, py + 18), p["head"], font(17), fade(col, pa), sp=4)
            cy = py + ph // 2 + 24
            mf = font(22, mono=True)
            lx = px + 128
            lw_ = text_w(d, p["login"], mf) + 40
            who = p["who"]
            for j, w_ in enumerate(who):
                iy = cy + int((j - (len(who) - 1) / 2) * 52)
                ic = fade(mix(DIM, TEXT, 0.5), pa)
                if w_ == "person":
                    _person(d, px + 54, iy - 6, ic)
                else:
                    _badge(d, px + 32, iy - 16, ic, fade(PANEL_HI, pa))
                d.line([(px + 86, iy), (lx - 8, cy)], fill=fade(DIM, pa * 0.9), width=3)
            box(d, lx, cy - 27, lw_, 54, fade(AMBER_D if k == 0 else ACCENT_D, pa * 0.55), fade(col, pa), 2, r=14)
            d.text((lx + 20, cy - 14), p["login"], font=mf, fill=fade(TEXT, pa))
            gx = lx + lw_ + 44
            gw = text_w(d, p["log"], mf) + 40
            harrow(d, lx + lw_ + 8, cy, gx - 8, fade(DIM, pa * 0.9), width=3, head=11, prog=pa)
            box(d, gx, cy - 27, gw, 54, fade(KO, pa) if pa > 0.02 else BG, fade(DIMMER, pa), 2, r=8)
            letterspace(d, (gx + 4, cy - 52), "THE LOG", font(14), fade(DIM, pa), sp=3)
            d.text((gx + 20, cy - 14), p["log"], font=mf, fill=fade(mix(DIM, TEXT, 0.8), pa))
            va = at(p.get("verdict_at", p.get("at", 0.3) + 0.1))
            vx = gx + gw + 22
            vf = fit(d, [side[k_]["verdict"] for k_ in ("shared", "own")], px + pw - 26 - vx_max, 30)
            d.text((vx, cy - int(vf.size * 0.6)), p["verdict"], font=vf, fill=fade(col, min(pa, va)))

    # ---- the limits, under the map
    foot = data.get("foot")
    fy = map_bot + 22
    if foot:
        n = len(foot)
        g_ = 20
        fw = (X1 - X0 - (n - 1) * g_) // n
        for k, it in enumerate(foot):
            fa = at(it.get("at", 0.3 + 0.2 * k), held=data.get("foot_held", False))
            if fa <= 0:
                continue
            x = X0 + k * (fw + g_)
            col = AMBER if it.get("tone") == "amber" else ACCENT
            box(d, x, fy, fw, 114, fade(PANEL, fa * 0.92), fade(col, fa), 2, r=16)
            letterspace(d, (x + 22, fy + 14), it["head"], font(16), fade(col, fa), sp=3)
            d.text((x + 22, fy + 40), it["text"], font=fit(d, [it["text"]], fw - 44, 27), fill=fade(TEXT, fa))
            if it.get("sub"):
                d.text((x + 22, fy + 73), it["sub"], font=fit(d, [it["sub"]], fw - 44, 21, bold=False), fill=fade(DIM, fa))
        fy += 114 + 22
    caption(d, t, dur, data, X0, max(fy + 4, 800), 42)


# ------------------------------------------------------------------ trail
TOP_Y, TOP_H = 276, 262
LOG_Y = 560


def scene_trail(d, t, dur, data):
    """one night's work: what the agent found, what it did and couldn't do, and the log that records all of it"""
    d = _Clean(d)
    static = data.get("static", False)
    a0 = 1.0 if static else ease(t / 0.4)
    _label(d, data, a0)

    def at(frac, span=0.5, held=False):
        return 1.0 if (static or held) else ease((t - frac * dur) / span)

    # ---- the two counts
    c = data["counts"]
    ch_ = c.get("held", False)
    lw_ = 760
    ca = at(c.get("at", 0.03), held=ch_)
    box(d, X0, TOP_Y, lw_, TOP_H, fade(PANEL, ca * 0.55), fade(DIMMER, ca), 2, r=20)
    bw, bh = 300, 122
    bx = [X0 + 26, X0 + lw_ - 26 - bw]
    for k, side in enumerate(("left", "right")):
        s = c[side]
        sa = at(c.get("at", 0.03) if k == 0 else c.get("right_at", 0.2), held=ch_)
        if sa <= 0:
            continue
        box(d, bx[k], TOP_Y + 22, bw, bh, fade(PANEL, sa * 0.95), fade(DIMMER, sa), 2, r=14)
        hf_ = min((fit_spaced(d, c[q]["head"], bw - 40, 16, 3) for q in ("left", "right")), key=lambda f_: f_.size)
        letterspace(d, (bx[k] + 20, TOP_Y + 36), s["head"], hf_, fade(DIM, sa), sp=3)
        vf = font(52, mono=True)
        d.text((bx[k] + 20, TOP_Y + 64), s["value"], font=vf, fill=fade(TEXT, sa))
        d.text((bx[k] + 30 + text_w(d, s["value"], vf), TOP_Y + 86), s["unit"], font=font(24, bold=False), fill=fade(DIM, sa))
    da = at(c.get("diff_at", 0.3), held=ch_)
    mx = X0 + lw_ // 2
    if da > 0:
        nf = font(64)
        ctext(d, mx, TOP_Y + 46, "=", nf, fade(AMBER, da))
        d.line([(mx - 16, TOP_Y + 110), (mx + 16, TOP_Y + 62)], fill=fade(AMBER, da), width=5)
    fa = at(c.get("finding_at", 0.5), held=ch_)
    fl = c.get("finding", [])
    ff = fit(d, [_strip(x) for x in fl] or [""], lw_ - 52, 29)
    for j, ln in enumerate(fl):
        la = fa if not c.get("finding_ats") else at(c["finding_ats"][j], held=ch_)
        d.text((X0 + 26, TOP_Y + 162 + j * 40), _strip(ln), font=ff, fill=_tone(ln, la))

    # ---- the one that differs, in detail (before the agent acts)
    fd = data.get("found")
    if fd and not data.get("acts"):
        ax = X0 + lw_ + 24
        aw = X1 - ax
        fa_ = at(fd.get("at", 0.3))
        box(d, ax, TOP_Y, aw, TOP_H, fade(PANEL, fa_ * 0.55), fade(DIMMER, fa_), 2, r=20)
        letterspace(d, (ax + 26, TOP_Y + 18), fd["head"], fit_spaced(d, fd["head"], aw - 52, 16, 3), fade(DIM, fa_), sp=3)
        fl_ = fd["lines"]
        ff_ = fit(d, [_strip(x_[1]) for x_ in fl_], aw - 300, 30)
        kf_ = font(17)
        ih = (TOP_H - 62) // max(len(fl_), 1)
        for j, (key_, val_) in enumerate(fl_):
            la = at(fd["ats"][j], 0.45) if fd.get("ats") else fa_
            yy = TOP_Y + 58 + j * ih
            letterspace(d, (ax + 26, yy + 9), key_, kf_, fade(DIM, la), sp=3)
            d.text((ax + 250, yy), _strip(val_), font=ff_, fill=_tone(val_, la))

    # ---- what it does next, and what it can't
    ac = data.get("acts")
    if ac:
        ah = ac.get("held", False)
        ax = X0 + lw_ + 24
        aw = X1 - ax
        aa = at(ac.get("at", 0.1), held=ah)
        box(d, ax, TOP_Y, aw, TOP_H, fade(PANEL, aa * 0.55), fade(DIMMER, aa), 2, r=20)
        letterspace(d, (ax + 26, TOP_Y + 18), ac["head"], fit_spaced(d, ac["head"], aw - 52, 16, 3), fade(DIM, aa), sp=3)
        items = ac["items"]
        ih = (TOP_H - 56) // max(len(items), 1)
        tf = fit(d, [it["text"] for it in items], aw - 100, 29)
        wf = fit(d, [it.get("why", "") for it in items], aw - 100, 21, bold=False)
        for j, it in enumerate(items):
            la = at(it.get("at", 0.2 + 0.15 * j), 0.45, ah)
            if la <= 0:
                continue
            yy = TOP_Y + 52 + j * ih
            ok = it.get("state", "ok") == "ok"
            if ok:
                check(d, ax + 44, yy + 20, 14, la)
            else:
                _cross(d, ax + 44, yy + 20, 14, la)
            has_why = bool(it.get("why"))
            d.text((ax + 76, yy + (0 if has_why else 3)), it["text"], font=tf, fill=fade(TEXT if ok else mix(DIM, TEXT, 0.75), la))
            if has_why:
                d.text((ax + 76, yy + tf.size + 5), it["why"], font=wf, fill=fade(ACCENT if ok else AMBER, la))
            if not ok:    # struck through: it isn't going to happen
                sw_ = text_w(d, it["text"], tf) * ease((la - 0.4) / 0.6)
                if sw_ > 0:
                    d.line([(ax + 76, yy + tf.size * 0.62), (ax + 76 + sw_, yy + tf.size * 0.62)], fill=fade(AMBER, la * 0.9), width=3)

    # ---- the audit log
    lg = data.get("log")
    if lg:
        nheld = lg.get("held", 0)
        la0 = at(lg.get("at", 0.05), held=nheld > 0 or lg.get("frame_held", False))
        rows = lg["rows"]
        rh = lg.get("row_h", 50)
        lh_ = 88 + len(rows) * rh + 12
        box(d, X0, LOG_Y, X1 - X0, lh_, fade(PANEL, la0 * 0.55), fade(DIMMER, la0), 2, r=20)
        x = letterspace(d, (X0 + 26, LOG_Y + 16), lg["head"], font(17), fade(ACCENT, la0), sp=4)
        if lg.get("note"):
            na = at(lg.get("note_at", 0.1), held=lg.get("note_held", False))
            letterspace(d, (x + 26, LOG_Y + 16), lg["note"], font(17), fade(DIM, min(la0, na)), sp=4)
        wts = lg.get("widths", [0.07, 0.19, 0.33, 0.29, 0.12])
        inner = X1 - X0 - 52
        xs, acc = [], X0 + 26
        for w_ in wts:
            xs.append(acc)
            acc += int(inner * w_)
        hi, hia = lg.get("hi_col"), at(lg.get("hi_at", 0.5)) if lg.get("hi_col") is not None else 0.0
        for k, name in enumerate(lg["cols"]):
            col = mix(DIM, ACCENT, hia) if k == hi else DIM
            letterspace(d, (xs[k], LOG_Y + 54), name, font(16), fade(col, la0), sp=3)
        d.line([(X0 + 26, LOG_Y + 82), (X1 - 26, LOG_Y + 82)], fill=fade(DIMMER, la0), width=2)
        fonts = []
        for k in range(len(wts)):
            mono = k in (0, 1)
            fonts.append(fit(d, [r["cells"][k] for r in rows], int(inner * wts[k]) - 22, 24 if mono else 25, bold=mono, mono=mono, floor=15))
        if hi is not None and hia > 0:
            box(d, xs[hi] - 12, LOG_Y + 44, int(inner * wts[hi]) - 4, lh_ - 54, fade(ACCENT_D, hia * 0.28), None, r=12)
            letterspace(d, (xs[hi], LOG_Y + 54), lg["cols"][hi], font(16), fade(ACCENT, hia), sp=3)
        for j, r in enumerate(rows):
            ra = 1.0 if (static or j < nheld) else ease((t - r.get("at", 0.2 + 0.15 * j) * dur) / 0.45)
            if ra <= 0:
                continue
            yy = LOG_Y + 92 + j * rh
            person = r.get("person", False)
            if person:
                box(d, X0 + 14, yy - 5, X1 - X0 - 28, rh - 6, fade(PANEL_HI, ra), None, r=10)
                _person(d, X1 - 44, yy + 16, fade(TEXT, ra * 0.9), s=0.62)
            for k, cell in enumerate(r["cells"]):
                last = k == len(wts) - 1
                colr = ACCENT if last else (TEXT if k in (1, 2) else mix(DIM, TEXT, 0.55))
                d.text((xs[k], yy + (rh - 12 - fonts[k].size) // 2), cell, font=fonts[k], fill=fade(colr, ra))
        if hi is not None and hia > 0:
            d.rounded_rectangle([xs[hi] - 12, LOG_Y + 44, xs[hi] - 16 + int(inner * wts[hi]), LOG_Y + lh_ - 10], radius=12, outline=fade(ACCENT, hia * 0.9), width=2)
        cap_y = LOG_Y + lh_ + 20
    else:
        cap_y = TOP_Y + TOP_H + 40
    caption(d, t, dur, data, X0, cap_y, 40)


# ------------------------------------------------------------------ access_review
def scene_access_review(d, t, dur, data):
    """an access review of one identity: two questions for every permission, and the one that goes"""
    d = _Clean(d)
    static = data.get("static", False)
    a0 = 1.0 if static else ease(t / 0.4)
    _label(d, data, a0)

    def at(frac, span=0.5, held=False):
        return 1.0 if (static or held) else ease((t - frac * dur) / span)

    rows = data["rows"]
    rh = data.get("row_h", 62)
    ty = 276
    th = 104 + len(rows) * rh + 14
    held = data.get("held", False)
    ta = at(data.get("at", 0.03), held=held)
    box(d, X0, ty, X1 - X0, th, fade(PANEL, ta * 0.55), fade(DIMMER, ta), 2, r=20)
    x = letterspace(d, (X0 + 26, ty + 18), data["head"], font(18), fade(ACCENT, min(ta, at(data["head_at"], held=held)) if "head_at" in data else ta), sp=4)
    org = data.get("origin")
    if org:
        oa = at(org.get("at", 0.1), held=held)
        of = font(17)
        ow = spaced_w(d, org["text"], of, 3) + 40
        box(d, X1 - 26 - ow, ty + 10, ow, 36, fade(AMBER_D, oa * 0.7), fade(AMBER, oa), 2, r=18)
        letterspace(d, (X1 - 26 - ow + 20, ty + 18), org["text"], of, fade(TEXT, oa), sp=3)
    wts = data.get("widths", [0.34, 0.24, 0.24, 0.18])
    inner = X1 - X0 - 52
    xs, acc = [], X0 + 26
    for w_ in wts:
        xs.append(acc)
        acc += int(inner * w_)
    cats = data.get("cols_at")
    for k, name in enumerate(data["cols"]):
        ca = at(cats[k], held=held) if cats else ta
        q = k in (1, 2)
        letterspace(d, (xs[k], ty + 66), name, fit_spaced(d, name, int(inner * wts[k]) - 20, 17, 3), fade(TEXT if q else DIM, min(ta, ca)), sp=3)
    d.line([(X0 + 26, ty + 98), (X1 - 26, ty + 98)], fill=fade(DIMMER, ta), width=2)
    f0 = fit(d, [r["cells"][0] for r in rows], int(inner * wts[0]) - 24, 29)
    f1 = fit(d, [c_ for r in rows for c_ in r["cells"][1:]], int(inner * min(wts[1:3])) - 24, 28, bold=False)
    f3 = fit(d, [r["decision"] for r in rows], int(inner * wts[3]) - 70, 28)
    for j, r in enumerate(rows):
        ra = at(r.get("at", 0.2 + 0.1 * j), 0.45, held)
        if ra <= 0:
            continue
        yy = ty + 108 + j * rh
        rem = r.get("state") == "remove"
        dc = at(r.get("decide_at", r.get("at", 0.2) + 0.08), 0.5, held)
        if rem and dc > 0:
            box(d, X0 + 14, yy - 2, X1 - X0 - 28, rh - 8, fade(AMBER_D, dc * 0.5), fade(AMBER, dc * 0.9), 2, r=12)
        ty_ = yy + (rh - 10 - f0.size) // 2 - 2
        d.text((xs[0], ty_), r["cells"][0], font=f0, fill=fade(TEXT, ra))
        if rem and dc > 0.5:
            sw_ = text_w(d, r["cells"][0], f0) * ease((dc - 0.5) / 0.5)
            d.line([(xs[0], ty_ + f0.size * 0.62), (xs[0] + sw_, ty_ + f0.size * 0.62)], fill=fade(AMBER, 0.95), width=3)
        cas = r.get("cell_ats")
        for k in (1, 2):
            ka = min(ra, at(cas[k - 1], 0.45, held)) if cas else ra
            d.text((xs[k], ty_ + 1), r["cells"][k], font=f1, fill=fade(AMBER if rem else mix(DIM, TEXT, 0.8), ka))
        if dc > 0:
            if rem:
                _cross(d, xs[3] + 16, yy + (rh - 10) // 2, 14, dc)
            else:
                check(d, xs[3] + 16, yy + (rh - 10) // 2, 14, dc)
            d.text((xs[3] + 44, ty_), r["decision"], font=f3, fill=fade(AMBER if rem else ACCENT, dc))

    # ---- why a spare permission matters
    inj = data.get("inject")
    by = ty + th + 20
    if inj:
        ia = at(inj.get("at", 0.6), held=inj.get("held", False))
        if ia > 0:
            bh = 150
            lw_ = 760
            box(d, X0, by, lw_, bh, fade(PANEL, ia * 0.92), fade(DIMMER, ia), 2, r=18)
            letterspace(d, (X0 + 24, by + 16), inj["head"], fit_spaced(d, inj["head"], lw_ - 48, 16, 3), fade(DIM, ia), sp=3)
            ll = inj["line"].split("\n")
            mf = fit(d, ll, lw_ - 48, 25, mono=True)
            for k, ln in enumerate(ll):
                d.text((X0 + 24, by + 52 + k * 38), ln, font=mf, fill=fade(AMBER, ia))
            ox = X0 + lw_ + 20
            ow = (X1 - ox - 20) // 2
            for k, key in enumerate(("with", "without")):
                o = inj[key]
                oa = at(o.get("at", 0.75 + 0.1 * k), held=inj.get("held", False))
                if oa <= 0:
                    continue
                col = AMBER if k == 0 else ACCENT
                x = ox + k * (ow + 20)
                box(d, x, by, ow, bh, fade(AMBER_D if k == 0 else ACCENT_D, oa * 0.45), fade(col, oa), 2, r=18)
                letterspace(d, (x + 22, by + 16), o["head"], fit_spaced(d, o["head"], ow - 44, 16, 3), fade(col, oa), sp=3)
                tl_ = o["text"].split("\n")
                of_ = fit(d, tl_, ow - 44, 29)
                for q, ln in enumerate(tl_):
                    d.text((x + 22, by + 52 + q * 40), ln, font=of_, fill=fade(TEXT, oa))
        by += 150 + 20
    caption(d, t, dur, data, X0, by + 4, 40)


R.RENDERERS.update({"accessmap": scene_accessmap, "trail": scene_trail, "access_review": scene_access_review})
