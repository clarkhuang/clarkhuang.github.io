#!/usr/bin/env python3
"""Write WebVTT captions for a rendered lesson from its scene script and render log.
usage: python3 make_vtt.py scripts/se201-01-ai-native.json ../../logs/s201_01_ainative.log out.vtt
Each scene's narration is split into sentences; cue times are spread across the scene in proportion to
sentence length (the per-scene start and length come from the render log, so cues never cross scenes)."""
import json, re, sys
spec = json.load(open(sys.argv[1])); log = open(sys.argv[2]).read()
tl = {m.group(1): (float(m.group(2)), float(m.group(3)))
      for m in re.finditer(r"^\s+(\d\d\w*?_\w+)\s+([\d.]+)s\s+\+\s*([\d.]+)s", log, re.M)}
def spoken(t):
    t = re.sub(r"\[[a-z ]+\]", " ", t); t = re.sub(r"</?[a-z]+>", "", t)
    t = re.sub(r"\s+", " ", t).strip()
    for a, b in READABLE: t = t.replace(a, b)
    return t
READABLE = [("A.I.", "AI"), ("L L M S dot T X T", "llms.txt"), ("index dot M D", "index.md"),
            ("agents dot M D", "AGENTS.md"), ("two oh one", "201"), ("one oh one", "101")]
def ts(x):
    h, r = divmod(x, 3600); m, s = divmod(r, 60); return f"{int(h):02d}:{int(m):02d}:{s:06.3f}"
out = ["WEBVTT", "", f"NOTE {spec['title']} — captions generated from the narration script", ""]
k = 0
for sc in spec["scenes"]:
    start, dur = tl[sc["id"]]; text = spoken(sc["text"])
    sents = [s for s in re.split(r"(?<=[.?!])\s+", text) if s]
    # merge very short sentences into the next cue so captions stay readable
    cues = []
    for s in sents:
        if cues and len(cues[-1]) < 28: cues[-1] += " " + s
        else: cues.append(s)
    speak = max(dur - 0.35, 0.5); total = sum(len(c) for c in cues); t = start
    for c in cues:
        d = speak * len(c) / total; k += 1
        out += [str(k), f"{ts(t)} --> {ts(t + d)}", c, ""]; t += d
open(sys.argv[3], "w").write("\n".join(out))
print(k, "cues ->", sys.argv[3])
