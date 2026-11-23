"""Layouts added for Software Engineering 201, Lessons 2 and 3. Imported by render_se101.py.

graph     nodes and arrows (a DAG): optional bands that group nodes, labels on the arrows for what
          crosses, and a highlighted path (the longest chain) with a dot running along it
crossing  the dependency test, row by row: two steps and "what crosses?" between them
lanes     a shared contract, parallel lanes that each finish on their own, one merge point,
          and one whole-system check
"""
import math
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


def _tone(name):
    """(line colour, fill colour, text colour) for a tone name"""
    return {"accent": (ACCENT, ACCENT_D, TEXT), "amber": (AMBER, AMBER_D, TEXT),
            "dim": (DIMMER, BG, DIM), "hi": (DIM, PANEL_HI, TEXT)}.get(name, (DIMMER, PANEL, TEXT))


def _lines_centered(d, cx, cy, text, f, fill, lead=1.22):
    lines = text.split("\n")
    lh = int(f.size * lead)
    y = cy - (len(lines) * lh) // 2 - int(f.size * 0.08)
    for k, ln in enumerate(lines):
        ctext(d, cx, y + k * lh, ln, f, fill)


def _arrow(d, p0, p1, col, width=4, head=15, prog=1.0, dashed=False):
    """a straight arrow from p0 to p1 at any angle; prog draws it part of the way"""
    (x0, y0), (x1, y1) = p0, p1
    L = math.hypot(x1 - x0, y1 - y0)
    if L < 1 or prog <= 0:
        return
    ux, uy = (x1 - x0) / L, (y1 - y0) / L
    ex, ey = x0 + (x1 - x0) * prog, y0 + (y1 - y0) * prog
    if dashed:
        n = max(int(L * prog / 22), 1)
        for k in range(n):
            a, b = k * 22, min(k * 22 + 12, L * prog)
            d.line([(x0 + ux * a, y0 + uy * a), (x0 + ux * b, y0 + uy * b)], fill=col, width=width)
    else:
        d.line([(x0, y0), (ex - ux * head * 0.6, ey - uy * head * 0.6)], fill=col, width=width)
    if prog > 0.85 and not dashed:
        px, py = -uy, ux
        bx, by = ex - ux * head, ey - uy * head
        d.polygon([(ex, ey), (bx + px * head * 0.55, by + py * head * 0.55),
                   (bx - px * head * 0.55, by - py * head * 0.55)], fill=col)


def _anchors(a, b, gap=8):
    """where an arrow leaves box a and enters box b"""
    if b["x"] - b["w"] / 2 >= a["x"] + a["w"] / 2 - 1:
        return (a["x"] + a["w"] / 2 + 2, a["y"]), (b["x"] - b["w"] / 2 - gap, b["y"])
    if b["x"] + b["w"] / 2 <= a["x"] - a["w"] / 2 + 1:
        return (a["x"] - a["w"] / 2 - 2, a["y"]), (b["x"] + b["w"] / 2 + gap, b["y"])
    lo, hi = max(a["x"] - a["w"] / 2, b["x"] - b["w"] / 2) + 24, min(a["x"] + a["w"] / 2, b["x"] + b["w"] / 2) - 24
    ax = bx = (lo + hi) / 2 if lo <= hi else None   # overlapping in x: one straight vertical arrow
    if ax is None:
        ax, bx = a["x"], b["x"]
    if b["y"] > a["y"]:
        return (ax, a["y"] + a["h"] / 2 + 2), (bx, b["y"] - b["h"] / 2 - gap)
    return (ax, a["y"] - a["h"] / 2 - 2), (bx, b["y"] + b["h"] / 2 + gap)


def scene_graph(d, t, dur, data):
    """a dependency graph. nodes: {id, text, sub, x, y, w, h, tone, tag, at, size}; edges: [from, to] or
    {from, to, label, tone, dashed}; bands: {x, y, w, h, label, tone, at}; path: node ids to light
    in order (path_at, path_tone, dim_rest); static: everything already on screen at t=0"""
    static = data.get("static", False)
    a0 = 1.0 if static else ease(t / 0.4)
    letterspace(d, (data.get("label_x", 160), 232), data["label"], font(23), fade(DIMMER, a0), sp=6)
    nodes = []
    N = len(data["nodes"])
    spread = data.get("spread", 0.55)
    for i, n in enumerate(data["nodes"]):
        m = dict(n)
        m.setdefault("w", data.get("node_w", 250))
        m.setdefault("h", data.get("node_h", 92))
        at = n.get("at", 0.03 + spread * i / max(N, 1))
        m["a"] = 1.0 if (static or n.get("held")) else ease((t - at * dur) / 0.5)
        nodes.append(m)
    by = {n["id"]: n for n in nodes}

    path = data.get("path", [])
    p_at = data.get("path_at", 0.62) * dur
    p_tone = data.get("path_tone", "accent")
    pcol, pdark, _ = _tone(p_tone)
    p_static = data.get("path_static", False)
    p_step = min(0.55, max(dur - p_at - 1.2, 0.6) / max(len(path), 1))

    def lit(idx):
        if idx < 0:
            return 0.0
        return 1.0 if p_static else ease((t - p_at - idx * p_step) / 0.45)

    p_idx = {nid: k for k, nid in enumerate(path)}
    p_edges = {(path[k], path[k + 1]): k + 1 for k in range(len(path) - 1)}
    all_lit = lit(len(path) - 1) if path else 0.0
    rest = 1.0 - (0.6 * (lit(0) if path else 0.0) if data.get("dim_rest") else 0.0)

    for b in data.get("bands", []):
        ba = 1.0 if (static or b.get("held")) else ease((t - b.get("at", 0.0) * dur) / 0.6)
        if ba <= 0:
            continue
        col, _, _ = _tone(b.get("tone"))
        d.rounded_rectangle([b["x"], b["y"], b["x"] + b["w"], b["y"] + b["h"]], radius=26,
                            fill=fade(PANEL, ba * 0.32), outline=fade(col, ba * 0.55), width=2)
        letterspace(d, (b["x"] + 24, b["y"] + 16), b["label"], font(19), fade(col if b.get("tone") else DIM, ba), sp=5)

    edges = [{"from": e[0], "to": e[1]} if isinstance(e, (list, tuple)) else dict(e) for e in data.get("edges", [])]
    ends = {}
    for e in edges:   # spread the arrowheads along the edge of a box that several arrows enter
        p0, p1 = _anchors(by[e["from"]], by[e["to"]])
        e["p0"], e["p1"] = p0, p1
        ends.setdefault((e["to"], round(p1[0]), round(p1[1])), []).append(e)
    for (_, _, _), grp in ends.items():
        if len(grp) < 2:
            continue
        tgt = by[grp[0]["to"]]
        horiz = abs(grp[0]["p1"][1] - tgt["y"]) < 1
        grp.sort(key=lambda e: e["p0"][1] if horiz else e["p0"][0])
        gap = min(26, (tgt["h"] if horiz else tgt["w"]) * 0.62 / len(grp))
        for k, e in enumerate(grp):
            off = (k - (len(grp) - 1) / 2) * gap
            e["p1"] = (e["p1"][0], e["p1"][1] + off) if horiz else (e["p1"][0] + off, e["p1"][1])
    for e in edges:
        na, nb = by[e["from"]], by[e["to"]]
        ea = min(na["a"], nb["a"])
        if "at" in e and not static:   # an arrow can land later than the boxes it joins
            ea = min(ea, ease((t - e["at"] * dur) / 0.5))
        if ea <= 0:
            continue
        k = p_edges.get((e["from"], e["to"]), -1)
        la = lit(k) if k >= 0 else 0.0
        col, _, _ = _tone(e.get("tone"))
        base = fade(col if e.get("tone") else DIM, ea * (0.85 if k >= 0 else 0.85 * rest))
        p0, p1 = e["p0"], e["p1"]
        _arrow(d, p0, p1, mix(base, pcol, la), width=3 + int(2 * la), prog=ea, dashed=e.get("dashed", False))
        if e.get("label"):
            f = font(e.get("size", 20))
            mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
            tw = text_w(d, e["label"], f)
            dy = e.get("dy", -34)
            d.text((mx - tw // 2 + e.get("dx", 0), my + dy), e["label"], font=f,
                   fill=mix(fade(DIM, ea * rest), pcol, la * 0.9))

    for n in nodes:
        na = n["a"]
        if na <= 0:
            continue
        col, fill, tcol = _tone(n.get("tone"))
        la = lit(p_idx.get(n["id"], -1))
        dim = 1.0 if n["id"] in p_idx else rest
        x, y = n["x"] - n["w"] // 2, n["y"] - n["h"] // 2 + int((1 - na) * 18)
        box(d, x, y, n["w"], n["h"], mix(fade(fill, na * 0.92 * dim), fade(pdark, 0.75), la),
            mix(fade(col, na * dim), pcol, la), 2 + int(2 * la) + (1 if n.get("tone") in ("accent", "amber") else 0),
            r=n.get("r", 18))
        f = font(n.get("size", data.get("size", 28)), bold=n.get("bold", True))
        if n.get("sub"):
            sf = font(n.get("sub_size", 22), bold=False, mono=n.get("sub_mono", False))
            _lines_centered(d, n["x"], y + n["h"] // 2 - int(sf.size * 0.62), n["text"], f, fade(tcol, na * dim))
            ctext(d, n["x"], y + n["h"] // 2 + int(f.size * 0.42), n["sub"], sf, fade(DIM, na * dim))
        else:
            _lines_centered(d, n["x"], y + n["h"] // 2, n["text"], f, fade(tcol, na * dim))
        if n.get("tag"):
            tf = font(17)
            tw = text_w(d, n["tag"], tf) + len(n["tag"]) * 4
            letterspace(d, (n["x"] - tw // 2, y - 30), n["tag"], tf, mix(fade(DIM, na * dim), pcol, la), sp=4)

    if path and all_lit > 0.98 and data.get("runner", True):
        pts = []
        for k in range(len(path) - 1):
            p0, p1 = _anchors(by[path[k]], by[path[k + 1]])
            pts += [(by[path[k]]["x"], by[path[k]]["y"]), p0, p1]
        pts.append((by[path[-1]]["x"], by[path[-1]]["y"]))
        segs = [math.hypot(pts[k + 1][0] - pts[k][0], pts[k + 1][1] - pts[k][1]) for k in range(len(pts) - 1)]
        total = sum(segs) or 1
        pos = ((t * data.get("runner_speed", 0.22)) % 1.0) * total
        for k, s in enumerate(segs):
            if pos <= s:
                fx = pos / s if s else 0
                px = pts[k][0] + (pts[k + 1][0] - pts[k][0]) * fx
                py = pts[k][1] + (pts[k + 1][1] - pts[k][1]) * fx
                d.ellipse([px - 11, py - 11, px + 11, py + 11], fill=TEXT, outline=pcol, width=3)
                break
            pos -= s

    cap = data.get("caption", "")
    if cap:
        ca = ease((t - data.get("caption_at", 0.7) * dur) / 0.6)
        col = {"amber": AMBER, "accent": ACCENT}.get(data.get("caption_tone", "text"), TEXT)
        f = font(data.get("caption_size", 44))
        for k, ln in enumerate(cap.split("\n")):
            d.text((data.get("caption_x", 160), data.get("caption_y", 880) + k * int(f.size * 1.28)), ln,
                   font=f, fill=fade(col, ca))
    foot = data.get("foot", "")
    if foot:
        fa = ease((t - data.get("caption_at", 0.7) * dur - 0.5) / 0.6)
        letterspace(d, (data.get("caption_x", 160), data.get("foot_y", 960)), foot, font(21), fade(DIMMER, fa), sp=5)


def scene_crossing(d, t, dur, data):
    """the dependency test. rows: {a, b, crosses (text or ""), verdict, sub, at}: when something
    crosses, it rides the arrow from a to b; when nothing does, there is no arrow"""
    a0 = ease(t / 0.4)
    letterspace(d, (180, 232), data["label"], font(23), fade(DIMMER, a0), sp=6)
    rows = data["rows"]
    bw, bh = data.get("box_w", 400), 104
    xa, xb, xv = 180, 180 + bw + 330, 180 + 2 * bw + 330 + 60
    y0, rh = data.get("y0", 356), data.get("row_h", 168)
    q = data.get("question", "WHAT CROSSES?")
    qf = font(21)
    qx = xa + bw + 165 - (text_w(d, q, qf) + len(q) * 5) // 2
    letterspace(d, (qx, y0 - 56), q, qf, fade(AMBER, ease((t - 0.3) / 0.5)), sp=5)
    n = len(rows)
    for i, r in enumerate(rows):
        at = r.get("at", 0.08 + 0.74 * i / max(n, 1)) * dur
        ra = ease((t - at) / 0.5)
        if ra <= 0:
            continue
        y = y0 + i * rh
        real = bool(r.get("crosses"))
        col, dark = (ACCENT, ACCENT_D) if real else (DIM, PANEL)
        for x, s in ((xa, r["a"]), (xb, r["b"])):
            box(d, x, y, bw, bh, fade(PANEL, ra * 0.92), fade(DIMMER, ra), 2)
            _lines_centered(d, x + bw // 2, y + bh // 2, s, font(r.get("size", 32)), fade(TEXT, ra))
        x0, x1, my = xa + bw + 14, xb - 14, y + bh // 2
        ga = ease((t - at - 0.7) / 0.8)
        if real:
            _arrow(d, (x0, my), (x1, my), fade(ACCENT, ga), width=5, head=18, prog=ga)
            pf = font(26)
            pw = text_w(d, r["crosses"], pf) + 44
            px = x0 + (x1 - x0 - pw) / 2 * ease((t - at - 0.9) / 1.0)
            pa = ease((t - at - 0.9) / 0.5)
            if pa > 0:
                box(d, int(px), my - 60, pw, 46, fade(ACCENT_D, pa), fade(ACCENT, pa), 2, r=23)
                d.text((int(px) + 22, my - 52), r["crosses"], font=pf, fill=fade(TEXT, pa))
        else:
            _arrow(d, (x0, my), (x1, my), fade(DIMMER, ga * 0.8), width=3, prog=ga, dashed=True)
            nf = font(26, bold=False)
            ns = r.get("nothing", "nothing")
            ctext(d, (x0 + x1) // 2, my - 52, ns, nf, fade(DIM, ga))
        va = ease((t - at - 1.5) / 0.6)
        vcol = ACCENT if real else AMBER
        d.text((xv, y + 12), r["verdict"], font=font(34), fill=fade(vcol, va))
        if r.get("sub"):
            d.text((xv, y + 58), r["sub"], font=font(25, bold=False), fill=fade(DIM, va))
    cap = data.get("caption", "")
    if cap:
        ca = ease((t - data.get("caption_at", 0.82) * dur) / 0.6)
        f = font(data.get("caption_size", 48))
        for k, ln in enumerate(cap.split("\n")):
            d.text((180, data.get("caption_y", y0 + n * rh + 24) + k * int(f.size * 1.28)), ln, font=f, fill=fade(TEXT, ca))


def scene_lanes(d, t, dur, data):
    """contract -> parallel lanes -> one merge point -> one whole-system check.
    contract/merge/test: {tag, text, tone}; lanes: [{name, sub, frac, tone}];
    focus: "contract" | "lanes" | "merge" | "test" lights one stage; static: everything already on screen;
    hold_lanes: only the lanes are already finished; hold_stages: the boxes are already up and the lanes run;
    idle: the lanes are drawn but have not started; a stage's "at" (fraction of the scene) says when it lands;
    chips: a row of small boxes under the diagram (the real files behind each stage)"""
    static = data.get("static", False)
    lstatic = static or data.get("hold_lanes", False)
    sstatic = static or data.get("hold_stages", False)   # the boxes are already up; only the lanes run
    idle = data.get("idle", False)                        # lanes drawn but not started yet
    focus = data.get("focus")
    a0 = 1.0 if sstatic else ease(t / 0.4)
    letterspace(d, (140, 232), data["label"], font(23), fade(DIMMER, a0), sp=6)
    lanes = data["lanes"]
    n = len(lanes)
    lh, lg = 108, 30
    ly0 = data.get("lanes_y", 320)
    span = n * lh + (n - 1) * lg
    cy = ly0 + span // 2
    cx0, cw = 140, 280
    lx0, lw = 500, 600
    mx0, mw = 1190, 270
    tx0, tw_ = 1540, 250

    def stage(key, x, w, y, h, start):
        s = data.get(key)
        if not s:
            return 0.0
        sa = 1.0 if sstatic else ease((t - (s["at"] * dur if "at" in s else start)) / 0.6)
        tone = s.get("tone")
        if focus:
            tone = "accent" if focus == key else (tone if tone in ("amber", "ghost") else None)
        ghost = tone == "ghost"
        col, fill, tcol = _tone(None if ghost else tone)
        dimk = 0.5 if (focus and focus != key) else 1.0
        if ghost:
            for k in range(0, int(2 * (w + h)), 26):   # dashed outline: nothing is really there
                for (px, py, qx, qy) in _dash_rect(x, y, w, h, k, 14):
                    d.line([(px, py), (qx, qy)], fill=fade(DIMMER, sa * 0.9), width=3)
            tcol = DIM
        else:
            box(d, x, y, w, h, fade(fill, sa * 0.9 * dimk), fade(col, sa * dimk), 4 if tone in ("accent", "amber") else 2, r=20)
        if s.get("tag"):
            tf = font(18)
            tg = s["tag"]
            letterspace(d, (x + w // 2 - (text_w(d, tg, tf) + len(tg) * 4) // 2, y - 34), tg, tf,
                        fade(col if tone in ("accent", "amber") else DIM, sa), sp=4)
        _lines_centered(d, x + w // 2, y + h // 2, s["text"], font(s.get("size", 30)), fade(tcol, sa * dimk))
        return sa

    ca_ = stage("contract", cx0, cw, ly0, span, 0.3)
    lane_dim = 0.5 if (focus and focus != "lanes") else 1.0
    done_all = 1.0
    run_t = data.get("run", 0.5) * dur
    for i, ln in enumerate(lanes):
        y = ly0 + i * (lh + lg)
        la = 1.0 if (lstatic or sstatic) else ease((t - 0.7 - i * 0.25) / 0.5)
        tone = "accent" if focus == "lanes" else ln.get("tone")
        col, fill, tcol = _tone(tone)
        box(d, lx0, y, lw, lh, fade(PANEL, la * 0.92 * lane_dim), fade(col, la * lane_dim), 3 if tone == "accent" else 2, r=18)
        d.text((lx0 + 28, y + 16), ln["name"], font=font(31), fill=fade(TEXT, la * lane_dim))
        if ln.get("sub"):
            st = ln["sub"]
            d.text((lx0 + lw - 86 - text_w(d, st, font(23, bold=False)), y + 22), st, font=font(23, bold=False), fill=fade(DIM, la * lane_dim))
        p = 0.0 if idle else 1.0 if lstatic else max(0.0, min(1.0, (t - 1.3) / max(run_t * ln.get("frac", 1.0), 0.1)))
        bx0, bx1, byy = lx0 + 28, lx0 + lw - 86, y + 70
        d.rounded_rectangle([bx0, byy, bx1, byy + 14], radius=7, fill=fade(BG, la))
        if p > 0.02:
            d.rounded_rectangle([bx0, byy, bx0 + int((bx1 - bx0) * p), byy + 14], radius=7,
                                fill=fade(mix(ACCENT_D, ACCENT, 0.6), la * lane_dim))
        dn = 0.0 if idle else 1.0 if lstatic else ease((t - 1.3 - run_t * ln.get("frac", 1.0)) / 0.4)
        done_all = min(done_all, dn)
        if dn > 0:
            check(d, lx0 + lw - 46, y + lh // 2, 22, dn * lane_dim, ACCENT)
        if ca_ > 0:
            _arrow(d, (cx0 + cw + 6, y + lh // 2), (lx0 - 10, y + lh // 2), fade(DIM, min(ca_, la) * 0.8), width=3, head=12,
                   prog=min(ca_, la), dashed=(data.get("contract", {}).get("tone") == "ghost" and focus != "contract"))
    m = data.get("merge")
    mh = data.get("merge_h", 190)
    if m:
        ms = m["at"] * dur - 0.3 if "at" in m else (0.2 if lstatic else 1.0 if idle else 1.3 + run_t + 0.2)
        for i in range(n):
            y = ly0 + i * (lh + lg) + lh // 2
            ga = 1.0 if sstatic else ease((t - ms) / 0.6)
            _arrow(d, (lx0 + lw + 6, y), (mx0 - 10, cy + (i - (n - 1) / 2) * 40), fade(DIM, ga * 0.85), width=3, head=12, prog=ga)
        stage("merge", mx0, mw, cy - mh // 2, mh, ms + 0.3)
    te = data.get("test")
    if te:
        ts = te["at"] * dur - 0.2 if "at" in te else (0.9 if lstatic else 1.5 if idle else 1.3 + run_t + 1.1)
        ga = 1.0 if sstatic else ease((t - ts) / 0.5)
        _arrow(d, (mx0 + mw + 6, cy), (tx0 - 10, cy), fade(DIM, ga * 0.85), width=3, head=12, prog=ga)
        stage("test", tx0, tw_, cy - mh // 2, mh, ts + 0.2)
    chips = data.get("chips", [])
    if chips:
        cs = data["chips_at"] * dur if "chips_at" in data else (0.2 if static else 1.3 + run_t + 1.6)
        y = data.get("chips_y", ly0 + span + 58)
        f = font(data.get("chip_size", 26), mono=data.get("chip_mono", False))
        x = 140
        step = data.get("chip_step", 0.45)
        for k, c in enumerate(chips):
            ka = ease((t - cs - k * step) / 0.5)
            w = text_w(d, c, f) + 48
            if k > 0:
                _arrow(d, (x + 4, y + 30), (x + 40, y + 30), fade(DIM, ka), width=3, head=11, prog=ka)
                x += 50
            box(d, x, y, w, 60, fade(PANEL_HI, ka * 0.9), fade(ACCENT if data.get("chip_tone") == "accent" else DIMMER, ka), 2, r=14)
            d.text((x + 24, y + 30 - int(f.size * 0.6)), c, font=f, fill=fade(TEXT, ka))
            x += w
    cap = data.get("caption", "")
    if cap:
        ca = ease((t - data.get("caption_at", 0.72) * dur) / 0.6) if not data.get("caption_now") else ease((t - 0.3) / 0.6)
        col = {"amber": AMBER, "accent": ACCENT}.get(data.get("caption_tone", "text"), TEXT)
        f = font(data.get("caption_size", 46))
        for k, lnn in enumerate(cap.split("\n")):
            d.text((data.get("caption_x", 140), data.get("caption_y", ly0 + span + (140 if chips else 60)) + k * int(f.size * 1.28)), lnn,
                   font=f, fill=fade(col, ca))


def _dash_rect(x, y, w, h, k, dash):
    """one dash at distance k along the perimeter of a rectangle"""
    per = [(x, y, x + w, y), (x + w, y, x + w, y + h), (x + w, y + h, x, y + h), (x, y + h, x, y)]
    for (x0, y0, x1, y1) in per:
        L = abs(x1 - x0) + abs(y1 - y0)
        if k < L:
            ux, uy = (x1 - x0) / L, (y1 - y0) / L
            e = min(k + dash, L)
            return [(x0 + ux * k, y0 + uy * k, x0 + ux * e, y0 + uy * e)]
        k -= L
    return []


R.RENDERERS.update({"graph": scene_graph, "crossing": scene_crossing, "lanes": scene_lanes})
