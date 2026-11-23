"""Layouts added for Software Engineering 201, Lessons 5 and 6. Imported by render_se101.py.

gates          where people decide (lesson 5). Two modes:
               intro: the sorting questions as big cards, one per beat of narration, then the two verdicts.
                 data: {label, intro: True, tests: [{q, eg}], tests_at?: [frac..], verdicts: [{text, tone, at}]}
               rows: the questions as a strip of chips, and one row per change. A dot carries each change along
               a track: it either runs straight through ("ships on its checks") or stops at an amber gate with
               a named person, waits, gets a yes, and goes on. The chip a gated row trips lights up.
                 data: {label, tests: [chip text..], rows: [{change, note?, gate?: {why, who}, hits?: [chip idx],
                        result?, at?: frac, hold?: seconds}], upto, new_from, caption?, caption_at?, caption_tone?,
                        static?}   rows before new_from are already finished; rows from upto on are ghosts.
decision_card  the stop made quick (lesson 5): a wall of diff on the left, and on the right the one-page decision
               request an agent prepares; its fields land in turn, then the approver says yes.
                 data: {label, left: {tag, foot}, card: {tag, title, fields: [[key, value]..], who, buttons: [yes, no]},
                        card_at?, fields_at?: [frac..], approve_at?, caption?, caption_at?}
renewals       the real check (lesson 6): last night's renewals as a table, beside what "right" means.
               phase "green": the build is green and the table looks fine. phase "define": right, written as
               checks, one per beat. phase "run": the checks sweep the table; rows get a tick or an amber flag,
               each check gets its tally, and the totals land last.
                 data: {label, phase, table_tag, cols: [5 heads], rows: [{id, plan, price, charged, times, flag?,
                        bad?: "charged"|"times"}], totals: [[key, value]..], totals_note?, banner: {title, sub},
                        ask?: text, answer?: text, checks_tag, checks: [{text, failed?: n}], checks_at?: [frac..],
                        sweep?: [frac, frac], caption?, caption_at?, caption_tone?}
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


def fit(d, lines, maxw, size, bold=True, floor=16, mono=False):
    """the largest font, up to size, at which every line fits maxw"""
    while size > floor and max(text_w(d, ln, font(size, bold=bold, mono=mono)) for ln in lines) > maxw:
        size -= 1
    return font(size, bold=bold, mono=mono)


def clamp(v):
    return max(0.0, min(1.0, v))


def _tone_col(name, default=TEXT):
    return {"amber": AMBER, "accent": ACCENT, "dim": DIM}.get(name, default)


def _person(d, cx, cy, s, col):
    """a small head-and-shoulders mark"""
    d.ellipse([cx - s * 0.44, cy - s, cx + s * 0.44, cy - s * 0.12], fill=col)
    d.chord([cx - s * 0.82, cy + s * 0.02, cx + s * 0.82, cy + s * 1.66], 180, 360, fill=col)


def _caption(d, t, dur, data, x, y, size=42):
    cap = data.get("caption")
    if not cap:
        return
    ca = 1.0 if data.get("static") else ease((t - data.get("caption_at", 0.78) * dur) / 0.6)
    f = font(data.get("caption_size", size))
    col = _tone_col(data.get("caption_tone"))
    for k, ln in enumerate(cap.split("\n")):
        f2 = fit(d, [ln], W - x - 120, f.size)
        d.text((x, y + k * int(f.size * 1.25)), ln, font=f2, fill=fade(col, ca))


# ------------------------------------------------------------------ gates
def _gates_intro(d, t, dur, data):
    a0 = ease(t / 0.4)
    letterspace(d, (140, 226), data["label"], font(23), fade(DIMMER, a0), sp=6)
    tests = data["tests"]
    n = len(tests)
    gap = 20
    cw = (W - 280 - gap * (n - 1)) // n
    y, h = 290, data.get("card_h", 410)
    ats = data.get("tests_at") or [0.1 + 0.55 * k / n for k in range(n)]
    for k, c in enumerate(tests):
        x = 140 + k * (cw + gap)
        ta = ease((t - ats[k] * dur) / 0.55)
        if ta <= 0:
            box(d, x, y, cw, h, BG, fade(DIMMER, 0.3))
            d.text((x + 32, y + 26), str(k + 1), font=font(72), fill=fade(DIMMER, 0.4))
            continue
        nxt = ats[k + 1] * dur if k + 1 < n else data.get("verdicts", [{}])[0].get("at", 0.8) * dur
        cur = t < nxt
        dy = int((1 - ta) * 24)
        box(d, x, y + dy, cw, h, fade(PANEL_HI if cur else PANEL, ta * 0.95), fade(AMBER if cur else DIMMER, ta), 3 if cur else 2, r=22)
        d.rounded_rectangle([x, y + dy, x + cw, y + 8 + dy], radius=4, fill=fade(AMBER, ta * (1.0 if cur else 0.6)))
        d.text((x + 32, y + 30 + dy), str(k + 1), font=font(72), fill=fade(AMBER, ta * (1.0 if cur else 0.7)))
        ql = c["q"].split("\n")
        qf = fit(d, ql, cw - 60, 46)
        for j, ln in enumerate(ql):
            d.text((x + 32, y + 136 + j * 58 + dy), ln, font=qf, fill=fade(TEXT, ta))
        el = c["eg"].split("\n") if c.get("eg") else []
        ef = fit(d, el or [""], cw - 60, 27, bold=False)
        for j, ln in enumerate(el):
            d.text((x + 32, y + h - 34 - (len(el) - j) * 36 + dy), ln, font=ef, fill=fade(DIM, ta))
    yy = y + h + 44
    for v in data.get("verdicts", []):
        va = ease((t - v.get("at", 0.8) * dur) / 0.6)
        vf = fit(d, [v["text"]], W - 280, 52)
        d.text((140, yy + int((1 - va) * 18)), v["text"], font=vf, fill=fade(_tone_col(v.get("tone")), va))
        yy += 74


def scene_gates(d, t, dur, data):
    """where people decide: each change runs straight through, or stops at a gate for a named person"""
    if data.get("intro"):
        return _gates_intro(d, t, dur, data)
    static = data.get("static", False)
    X0 = 130
    letterspace(d, (X0, 222), data["label"], font(23), DIMMER, sp=6)
    rows, upto, new_from = data["rows"], data.get("upto", len(data["rows"])), data.get("new_from", 0)
    rh = data.get("row_h", 104)
    y0, bh = 368, rh - 20
    cx, cw = X0, 600                 # the change
    tx0, tx1 = 752, 1440             # the track
    gx, gw = 930, 350                # the gate
    n_new = max(upto - new_from, 1)

    st = []                          # per-row animation state
    for i, r in enumerate(rows):
        if i >= upto:
            st.append(None)
            continue
        done = static or i < new_from
        t0 = r["at"] * dur if "at" in r else 0.3 + (i - new_from) * dur * 0.8 / n_new
        tl = 99.0 if done else t - t0
        hold = r.get("hold", 1.6)
        s = {"card": ease(tl / 0.5), "track": ease((tl - 0.3) / 0.5)}
        if r.get("gate"):
            s["p1"] = clamp((tl - 0.8) / 0.7)
            s["gate"] = ease((tl - 1.2) / 0.5)
            s["yes"] = ease((tl - 1.6 - hold) / 0.4)
            s["p2"] = clamp((tl - 1.9 - hold) / 0.7)
            s["done"] = ease((tl - 2.5 - hold) / 0.4)
        else:
            s["p"] = clamp((tl - 0.8) / 1.2)
            s["done"] = ease((tl - 1.9) / 0.4)
        st.append(s)

    # the questions, as chips; one lights when a change trips it
    tests = data.get("tests", [])
    lit = [0.0] * len(tests)
    for r, s in zip(rows, st):
        if s and r.get("gate"):
            for k in r.get("hits", []):
                lit[k] = max(lit[k], s["gate"])
    px = letterspace(d, (X0, 288), data.get("tests_tag", "A PERSON DECIDES IF IT"), font(20), DIM, sp=5) + 18
    size = 26
    while size > 16 and sum(text_w(d, s_, font(size)) + 44 for s_ in tests) + 14 * (len(tests) - 1) > W - 130 - px:
        size -= 1
    cf = font(size)
    for k, s_ in enumerate(tests):
        w = text_w(d, s_, cf) + 44
        box(d, px, 270, w, 54, mix(fade(PANEL, 0.9), fade(AMBER_D, 0.9), lit[k]), mix(DIMMER, AMBER, lit[k]), 2 + int(lit[k] > 0.5), r=27)
        d.text((px + 22, 270 + 27 - int(cf.size * 0.6)), s_, font=cf, fill=mix(DIM, TEXT, lit[k]))
        px += w + 14

    for i, r in enumerate(rows):
        y = y0 + i * rh
        my = y + bh // 2
        s = st[i]
        if s is None:
            box(d, cx, y, cw, bh, BG, fade(DIMMER, 0.3))
            d.line([(tx0, my), (tx1, my)], fill=fade(DIMMER, 0.25), width=2)
            continue
        ca = s["card"]
        if ca <= 0:
            continue
        gated = bool(r.get("gate"))
        box(d, cx, y + int((1 - ca) * 14), cw, bh, fade(PANEL, ca * 0.92), fade(DIMMER, ca), 2)
        f = fit(d, [r["change"]], cw - 56, 31)
        d.text((cx + 28, my - int(f.size * 0.6) + int((1 - ca) * 14)), r["change"], font=f, fill=fade(TEXT, ca))
        ta = s["track"]
        if ta <= 0:
            continue
        d.line([(tx0, my), (tx0 + int((tx1 - tx0) * ta), my)], fill=fade(DIMMER, ta * 0.9), width=3)
        if gated:
            g = r["gate"]
            stop_x, go_x = gx - 16, gx + gw + 16
            p1, ga, ya, p2 = s["p1"], s["gate"], s["yes"], s["p2"]
            d.line([(tx0, my), (tx0 + int((stop_x - tx0) * p1), my)], fill=fade(ACCENT, 0.75), width=4)
            if p2 > 0:
                d.line([(go_x, my), (go_x + int((tx1 - go_x) * p2), my)], fill=fade(ACCENT, 0.75), width=4)
            if ga > 0:
                box(d, gx, y, gw, bh, fade(AMBER_D, ga * 0.9), fade(AMBER, ga), 3, r=16)
                _person(d, gx + 40, my - 4, 17, fade(AMBER, ga))
                letterspace(d, (gx + 74, y + bh // 2 - 30), g["why"], font(15), fade(AMBER, ga), sp=3)
                wf = fit(d, [g["who"]], gw - 74 - 56, 28)
                d.text((gx + 74, y + bh // 2 - 6), g["who"], font=wf, fill=fade(TEXT, ga))
                if ya > 0:
                    check(d, gx + gw - 30, y + bh - 26, 13, ya, ACCENT)
            tokx = tx0 + (stop_x - tx0) * p1 if p2 <= 0 else go_x + (tx1 - go_x) * p2
            if 0 < p1 and s["done"] < 1:
                if p1 >= 1 and ya < 1 and not static:      # waiting for a yes
                    ph = (t * 0.9) % 1.0
                    rr = 11 + int(16 * ph)
                    d.ellipse([tokx - rr, my - rr, tokx + rr, my + rr], outline=fade(AMBER, (1 - ph) * 0.9), width=3)
                d.ellipse([tokx - 11, my - 11, tokx + 11, my + 11], fill=TEXT, outline=AMBER if ya < 1 else ACCENT, width=3)
        else:
            p = s["p"]
            d.line([(tx0, my), (tx0 + int((tx1 - tx0) * p), my)], fill=fade(ACCENT, 0.75), width=4)
            if r.get("note"):
                nf = font(22, bold=False)
                ctext(d, (tx0 + tx1) // 2, my - 38, r["note"], nf, fade(DIM, ta))
            if 0 < p and s["done"] < 1:
                tokx = tx0 + (tx1 - tx0) * p
                d.ellipse([tokx - 11, my - 11, tokx + 11, my + 11], fill=TEXT, outline=ACCENT, width=3)
        da = s["done"]
        if da > 0:
            check(d, tx1 + 40, my, 20, da, ACCENT)
            res = r.get("result", "Ships after a yes" if gated else "Ships on its checks")
            rf = fit(d, [res], W - 110 - (tx1 + 76), 27, bold=not gated)
            d.text((tx1 + 76, my - int(rf.size * 0.6)), res, font=rf, fill=fade(TEXT if gated else ACCENT, da))
    _caption(d, t, dur, data, X0, y0 + len(rows) * rh + 14, 42)


# ------------------------------------------------------------------ decision_card
_DIFF = [0.62, 0.8, 0.45, 0.9, 0.7, 0.3, 0.84, 0.56, 0.74, 0.4, 0.88, 0.66, 0.5, 0.78, 0.36, 0.92, 0.6, 0.72]
_DIFF_TONE = {1: "add", 3: "del", 4: "add", 8: "add", 10: "del", 11: "add", 15: "add", 16: "del"}


def scene_decision_card(d, t, dur, data):
    """a wall of diff, and the one-page decision request the agent prepares instead"""
    static = data.get("static", False)
    a0 = 1.0 if static else ease(t / 0.4)
    letterspace(d, (130, 222), data["label"], font(23), fade(DIMMER, a0), sp=6)
    L, C = data["left"], data["card"]
    card_t = data.get("card_at", 0.22) * dur
    ca = 1.0 if static else ease((t - card_t) / 0.6)
    y, h = 282, 600
    # left: the wall of diff
    lx, lw = 130, 430
    ldim = 1.0 - 0.5 * ca
    box(d, lx, y, lw, h, fade(PANEL, a0 * 0.9 * ldim), fade(DIMMER, a0 * ldim), 2)
    letterspace(d, (lx + 28, y + 24), L["tag"], font(18), fade(DIM, a0 * ldim), sp=4)
    foot = L.get("foot", "").split("\n")
    rows_h = h - 76 - 30 - len(foot) * 40
    step_y = rows_h / len(_DIFF)
    for k, wv in enumerate(_DIFF):
        la = 1.0 if static else ease((t - 0.25 - k * 0.05) / 0.3)
        yy = y + 68 + k * step_y
        tone = _DIFF_TONE.get(k)
        col = ACCENT_D if tone == "add" else AMBER_D if tone == "del" else (52, 68, 82)
        d.rounded_rectangle([lx + 28, yy, lx + 28 + int((lw - 56) * wv), yy + max(10, int(step_y * 0.5))], radius=5,
                            fill=fade(col, la * ldim * 0.95))
    for j, ln in enumerate(foot):
        d.text((lx + 28, y + h - 24 - (len(foot) - j) * 40), ln, font=fit(d, [ln], lw - 56, 30), fill=fade(AMBER, a0 * ldim))
    # arrow
    ax0, ax1, ay = lx + lw + 14, lx + lw + 66, y + h // 2
    if ca > 0:
        d.line([(ax0, ay), (ax0 + int((ax1 - ax0 - 8) * ca), ay)], fill=fade(ACCENT, ca), width=5)
        if ca > 0.85:
            d.polygon([(ax1, ay), (ax1 - 16, ay - 10), (ax1 - 16, ay + 10)], fill=fade(ACCENT, ca))
    # right: the decision request
    x = lx + lw + 80
    w = W - 130 - x
    if ca > 0:
        dx = int((1 - ca) * 30)
        box(d, x + dx, y, w, h, fade(PANEL_HI, ca * 0.95), fade(ACCENT, ca), 3, r=22)
        letterspace(d, (x + 36 + dx, y + 26), C["tag"], font(19), fade(ACCENT, ca), sp=5)
        tf = fit(d, [C["title"]], w - 72, 42)
        d.text((x + 36 + dx, y + 56), C["title"], font=tf, fill=fade(TEXT, ca))
        d.line([(x + 36, y + 122), (x + w - 36, y + 122)], fill=fade(DIMMER, ca), width=2)
        fields = C["fields"]
        n = len(fields)
        fh = min(80, (h - 122 - 96) // n)
        ats = data.get("fields_at") or [data.get("card_at", 0.22) + 0.08 + 0.5 * k / n for k in range(n)]
        kw = 250
        for k, (key, val) in enumerate(fields):
            fa = 1.0 if static else ease((t - ats[k] * dur) / 0.5)
            if fa <= 0:
                continue
            fy = y + 136 + k * fh
            fx = int((1 - fa) * 18)
            d.rounded_rectangle([x + 28, fy, x + w - 28, fy + fh - 10], radius=12, fill=fade(PANEL, fa * 0.75))
            d.rounded_rectangle([x + 28, fy, x + 34, fy + fh - 10], radius=3, fill=fade(ACCENT, fa))
            kf = font(18)
            letterspace(d, (x + 54 + fx, fy + (fh - 10) // 2 - 11), key, kf, fade(ACCENT, fa), sp=4)
            lines = val.split("\n")
            vf = fit(d, lines, w - 56 - kw - 30, 28 if len(lines) == 1 else 25, bold=False)
            lh = int(vf.size * 1.22)
            vy = fy + (fh - 10) // 2 - (len(lines) * lh) // 2 - 2
            for j, ln in enumerate(lines):
                d.text((x + 28 + kw + fx, vy + j * lh), ln, font=vf, fill=fade(TEXT, fa))
        # the decision
        ba = 1.0 if static else ease((t - (ats[-1] * dur + 0.5)) / 0.5)
        ya = 1.0 if static else ease((t - data.get("approve_at", 0.88) * dur) / 0.5)
        by = y + h - 82
        _person(d, x + 58, by + 24, 17, fade(AMBER, ba))
        d.text((x + 92, by + 12), C["who"], font=font(28), fill=fade(TEXT, ba))
        yes, no = C.get("buttons", ["Approve", "Send back"])
        bw_, bh_ = 210, 56
        nx = x + w - 36 - bw_
        yx = nx - 20 - bw_
        box(d, nx, by, bw_, bh_, fade(PANEL, ba * 0.9), fade(DIMMER, ba), 2, r=28)
        ctext(d, nx + bw_ // 2, by + 13, no, font(25, bold=False), fade(DIM, ba))
        box(d, yx, by, bw_, bh_, mix(fade(ACCENT_D, ba * 0.7), ACCENT_D, ya), fade(ACCENT, ba), 2 + int(2 * ya), r=28)
        if ya > 0.05:
            check(d, yx + 34, by + bh_ // 2, 14, ya, ACCENT)
        ctext(d, yx + bw_ // 2 + int(14 * ya), by + 13, yes, font(25), fade(TEXT, ba))
    _caption(d, t, dur, data, 130, y + h + 28, 42)


# ------------------------------------------------------------------ renewals
_PHASES = {"green": 0, "define": 1, "run": 2}


def scene_renewals(d, t, dur, data):
    """last night's renewals beside what 'right' means: green build, then the checks, then the checks run"""
    ph = _PHASES[data.get("phase", "green")]
    static = data.get("static", False)
    a0 = ease(t / 0.4) if (ph == 0 and not static) else 1.0
    letterspace(d, (130, 222), data["label"], font(23), fade(DIMMER, a0), sp=6)
    rows = data["rows"]
    n = len(rows)
    # ---- the table
    tx, ty, tw_, th = 130, 276, 1060, 610
    box(d, tx, ty, tw_, th, fade(PANEL, a0 * 0.45), fade(DIMMER, a0 * 0.8), 2, r=22)
    letterspace(d, (tx + 30, ty + 22), data["table_tag"], font(19), fade(DIM, a0), sp=5)
    colx = [tx + 30, tx + 196, tx + 372, tx + 542, tx + 716]
    resx = tx + 812
    for cxh, hd in zip(colx, data["cols"]):
        letterspace(d, (cxh, ty + 66), hd, font(16), fade(DIMMER if ph else DIM, a0), sp=4)
    y0, rh, bh = ty + 100, 70, 58
    sw0, sw1 = [v * dur for v in data.get("sweep", [0.1, 0.55])]
    run = ph == 2
    sweep = 1.0 if (static or not run) else clamp((t - sw0) / max(sw1 - sw0, 0.1))
    fm = font(26, bold=False, mono=True)
    for i, r in enumerate(rows):
        ra = 1.0 if (ph > 0 or static) else ease((t - 0.3 - i * 0.12) / 0.45)
        if ra <= 0:
            continue
        y = y0 + i * rh
        hit = 0.0
        if run:
            hit = 1.0 if static else ease((t - (sw0 + (sw1 - sw0) * (i + 0.5) / n)) / 0.35)
        bad = bool(r.get("flag"))
        box(d, tx + 16, y, tw_ - 32, bh, mix(fade(PANEL, ra * 0.9), fade(AMBER_D, 0.75), hit if bad else 0.0),
            mix(fade(DIMMER, ra * 0.7), AMBER, hit) if bad else fade(DIMMER, ra * 0.7), 2 + int(bad and hit > 0.5), r=12)
        vals = [r["id"], r["plan"], r["price"], r["charged"], r["times"]]
        keys = ["id", "plan", "price", "charged", "times"]
        for cxv, v, key in zip(colx, vals, keys):
            col = fade(TEXT if key != "plan" else DIM, ra)
            if bad and r.get("bad") == key:
                col = mix(col, AMBER, hit)
            d.text((cxv, y + 13), v, font=fm if key != "plan" else font(26, bold=False), fill=col)
        if hit > 0:
            if bad:
                ff = fit(d, [r["flag"]], tw_ - 32 - (resx - tx) - 40, 24)
                fw = text_w(d, r["flag"], ff) + 32
                box(d, resx, y + 9, fw, bh - 18, fade(BG, hit * 0.6), fade(AMBER, hit), 2, r=20)
                d.text((resx + 16, y + bh // 2 - int(ff.size * 0.62)), r["flag"], font=ff, fill=fade(AMBER, hit))
            else:
                check(d, resx + 22, y + bh // 2, 16, hit, ACCENT)
    if run and not static and 0 < sweep < 1:
        sy = y0 + (n * rh - (rh - bh)) * sweep
        d.rectangle([tx + 8, sy - 2, tx + tw_ - 8, sy + 2], fill=ACCENT)
        d.rectangle([tx + 8, sy - 10, tx + tw_ - 8, sy - 3], fill=fade(ACCENT, 0.18))
    # totals
    fy = y0 + n * rh + 12
    d.line([(tx + 30, fy), (tx + tw_ - 30, fy)], fill=fade(DIMMER, a0 * 0.8), width=2)
    ta = 1.0 if (ph > 0 or static) else ease((t - 0.3 - n * 0.12) / 0.5)
    px = tx + 30
    for key, val in data.get("totals", []):
        px = letterspace(d, (px, fy + 30), key, font(17), fade(DIM, ta), sp=4) + 14
        d.text((px, fy + 18), val, font=font(32, mono=True), fill=fade(TEXT, ta))
        px += text_w(d, val, font(32, mono=True)) + 54
    note = data.get("totals_note")
    if note and run:
        na = 1.0 if static else ease((t - data.get("totals_at", 0.74) * dur) / 0.5)
        nf = fit(d, [note], tx + tw_ - 30 - px, 28)
        d.text((px, fy + 22), note, font=nf, fill=fade(AMBER, na))
    # ---- the right-hand panel
    rx, rw = 1230, W - 130 - 1230
    b = data["banner"]
    if ph == 0:
        box(d, rx, ty, rw, 230, fade(ACCENT_D, a0 * 0.55), fade(ACCENT, a0), 3, r=22)
        check(d, rx + 78, ty + 115, 44, ease((t - 0.5) / 0.5) if not static else 1.0, ACCENT)
        d.text((rx + 150, ty + 58), b["title"], font=fit(d, [b["title"]], rw - 180, 50), fill=fade(TEXT, a0))
        d.text((rx + 150, ty + 126), b["sub"], font=fit(d, [b["sub"]], rw - 180, 34, bold=False), fill=fade(TEXT, a0 * 0.85))
        yy = ty + 290
        for key, tone, at in (("ask", None, 0.4), ("answer", "amber", 0.72)):
            s = data.get(key)
            if not s:
                continue
            sa = 1.0 if static else ease((t - data.get(key + "_at", at) * dur) / 0.6)
            lines = s.split("\n")
            sf = fit(d, lines, rw, 46)
            for ln in lines:
                d.text((rx, yy + int((1 - sa) * 16)), ln, font=sf, fill=fade(_tone_col(tone), sa))
                yy += 58
            yy += 26
    else:
        sh = ease(t / 0.5) if (ph == 1 and not static) else 1.0   # the green banner steps back
        box(d, rx, ty, rw, 68, fade(ACCENT_D, 0.3), fade(ACCENT, 0.55), 2, r=20)
        check(d, rx + 38, ty + 34, 15, 0.8, ACCENT)
        bl = b["title"] + "  ·  " + b["sub"]
        d.text((rx + 68, ty + 34 - 17), bl, font=fit(d, [bl], rw - 90, 27, bold=False), fill=fade(TEXT, 0.75))
        letterspace(d, (rx, ty + 98), data["checks_tag"], font(19), fade(ACCENT, sh), sp=5)
        checks = data["checks"]
        m = len(checks)
        ats = data.get("checks_at") or [0.12 + 0.6 * k / m for k in range(m)]
        ch, cg = 138, 18
        for k, c in enumerate(checks):
            ka = 1.0 if (ph == 2 or static) else ease((t - ats[k] * dur) / 0.55)
            if ka <= 0:
                box(d, rx, ty + 134 + k * (ch + cg), rw, ch, BG, fade(DIMMER, 0.3))
                continue
            cy = ty + 134 + k * (ch + cg)
            res = 0.0
            if run:
                res = 1.0 if static else ease((t - sw1 - 0.2 - k * 0.3) / 0.45)
            failed = c.get("failed", 0)
            dx = int((1 - ka) * 24)
            box(d, rx + dx, cy, rw, ch, fade(PANEL_HI, ka * 0.95),
                mix(fade(ACCENT, ka * 0.8), AMBER if failed else ACCENT, res), 2 + int(res > 0.5), r=18)
            d.text((rx + 24 + dx, cy + ch // 2 - 30), str(k + 1), font=font(48), fill=fade(ACCENT, ka))
            lines = c["text"].split("\n")
            cf = fit(d, lines, rw - 78 - 150, 30)
            lh = int(cf.size * 1.26)
            for j, ln in enumerate(lines):
                d.text((rx + 78 + dx, cy + ch // 2 - (len(lines) * lh) // 2 + j * lh - 2), ln, font=cf, fill=fade(TEXT, ka))
            if res > 0:
                if failed:
                    s = f"{failed} failed"
                    sf = font(26)
                    d.text((rx + rw - 22 - text_w(d, s, sf), cy + ch // 2 - 16), s, font=sf, fill=fade(AMBER, res))
                else:
                    check(d, rx + rw - 46, cy + ch // 2, 18, res, ACCENT)
    _caption(d, t, dur, data, 130, ty + th + 22, 42)


R.RENDERERS.update({"gates": scene_gates, "decision_card": scene_decision_card, "renewals": scene_renewals})
