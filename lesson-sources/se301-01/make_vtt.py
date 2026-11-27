#!/usr/bin/env python3
"""WebVTT captions for SE 301 Lesson 1.

usage: python3 make_vtt.py se301-01-first-endpoint.json render-timeline.log out.vtt

Scene starts and lengths come from the render log, so a cue never crosses a scene.
The log line shape matches the other lesson scripts:

    01_title  0.00s + 3.20s
"""
import json, re, sys

READABLE = [
    ("one two seven point zero point zero point one", "127.0.0.1"),
    ("Qwen two point five", "Qwen2.5"),
    ("Qwen three", "Qwen3"),
    ("five point three", "5.3"),
    ("four eighty B", "480B"),
    ("gpt oss twenty b", "gpt-oss-20b"),
    ("thirty two K", "32K"),
    ("sixteen K", "16K"),
    ("three oh one", "301"),
    ("four bit", "four-bit"),
    ("eight bit", "eight-bit"),
    ("four K", "4K"),
    ("seven B", "7B"),
    ("code fast", "code-fast"),
    ("V four", "V4"),
    ("A.I.", "AI"),
    ("M.L.X.", "MLX"),
    ("G.L.M.", "GLM"),
    ("C.P.U.", "CPU"),
    ("G.P.U.", "GPU"),
    ("P.C.", "PC"),
]

def readable(text):
    text = re.sub(r"\[[a-z -]+\]", " ", text)
    text = re.sub(r"</?[a-z]+>", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    for a, b in READABLE:
        # Abbreviations already end in a period. When that period is also the
        # sentence period, keep one in the transcript ("PC. It").
        if a.endswith("."):
            text = re.sub(re.escape(a) + r"(?=\s+[A-Z])", b + ".", text)
        text = text.replace(a, b)
    return text

def ts(x):
    h, r = divmod(max(x, 0), 3600)
    m, s = divmod(r, 60)
    return f"{int(h):02d}:{int(m):02d}:{s:06.3f}"

def parse_log(log):
    return {m.group(1): (float(m.group(2)), float(m.group(3)))
            for m in re.finditer(r"^\s+(\d\d\w*?_\w+)\s+([\d.]+)s\s+\+\s*([\d.]+)s", log, re.M)}

def cues_for(spec, timeline):
    rows = []
    for sc in spec["scenes"]:
        if sc["id"] not in timeline:
            raise SystemExit(f"render log has no timing for {sc['id']}")
        start, dur = timeline[sc["id"]]
        text = readable(sc["text"])
        sents = [s for s in re.split(r"(?<=[.?!])\s+", text) if s]
        cues = []
        for s in sents:
            if cues and len(cues[-1]) < 28:
                cues[-1] += " " + s
            else:
                cues.append(s)
        if not cues:
            continue
        speak = max(dur - 0.35, 0.5)
        total = sum(len(c) for c in cues) or 1
        t = start
        for c in cues:
            d = speak * len(c) / total
            rows.append((t, t + d, c))
            t += d
    return rows

def write_vtt(spec, log_text, dest):
    timeline = parse_log(log_text)
    rows = cues_for(spec, timeline)
    out = ["WEBVTT", "", f"NOTE {spec['title']} — captions generated from the narration script", ""]
    for i, (a, b, c) in enumerate(rows, start=1):
        out += [str(i), f"{ts(a)} --> {ts(b)}", c, ""]
    open(dest, "w").write("\n".join(out))
    return len(rows)

def main():
    spec = json.load(open(sys.argv[1]))
    log = open(sys.argv[2]).read()
    n = write_vtt(spec, log, sys.argv[3])
    print(n, "cues ->", sys.argv[3])

if __name__ == "__main__":
    main()
