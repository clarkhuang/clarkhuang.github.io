#!/usr/bin/env python3
"""Render Software Engineering 301, Lesson 1.

1920×1080, 30 fps, H.264. Narration is xAI text-to-speech, voice 4lbl0krw73vf,
speed 1.05. Audio is normalized to -16 LUFS integrated with true peak at or
below -1 dBTP. Writes an MP4, WebVTT captions, a poster frame, chapter
timestamps, and a render timeline.

The API key is read from the XAI_API_KEY environment variable. It is never
written to a file, a log, or a command line, and it is never printed.

This script refuses to write a silent or dummy MP4. Until Clark approves the
script and facts.md, do not run the full render.

    python3 render_se301_01.py --check          # draw one frame per scene, no network
    XAI_API_KEY=... python3 render_se301_01.py  # narrate, render, normalize
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request

import numpy as np
from PIL import Image, ImageDraw, ImageFont

import make_vtt

HERE = os.path.dirname(os.path.abspath(__file__))
W, H, FPS = 1920, 1080, 30
BG = (12, 18, 23)
PANEL = (23, 32, 40)
PANEL_HI = (30, 42, 52)
TEXT = (243, 247, 249)
DIM = (194, 204, 212)
DIMMER = (138, 154, 168)
ACCENT = (74, 222, 128)
ACCENT_D = (26, 107, 60)
AMBER = (240, 177, 74)
LINE = (42, 56, 70)
VOICE = "4lbl0krw73vf"
SPEED = 1.05
TTS_URL = "https://api.x.ai/v1/tts"

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(size, bold=False, serif=False):
    name = "DejaVuSerif" if serif else "DejaVuSans"
    if bold:
        name += "-Bold"
    path = os.path.join(FONT_DIR, name + ".ttf")
    if not os.path.isfile(path) and sys.platform == "darwin":
        family = "Georgia" if serif else "Arial"
        path = "/System/Library/Fonts/Supplemental/" + family + (" Bold" if bold else "") + ".ttf"
    return ImageFont.truetype(path, size)


def ease(x):
    x = 0 if x < 0 else 1 if x > 1 else x
    return 1 - (1 - x) ** 3


def mix(a, b, t):
    t = 0 if t < 0 else 1 if t > 1 else t
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def fade(color, alpha):
    return mix(BG, color, alpha)


def new_frame():
    img = Image.new("RGB", (W, H), BG)
    return img, ImageDraw.Draw(img)


def wrap(draw, text, fnt, width):
    lines = []
    for para in str(text).split("\n"):
        words = para.split()
        if not words:
            lines.append("")
            continue
        cur = words[0]
        for word in words[1:]:
            trial = cur + " " + word
            if draw.textlength(trial, font=fnt) <= width:
                cur = trial
            else:
                lines.append(cur)
                cur = word
        lines.append(cur)
    return lines


def kicker(draw, label, alpha=1):
    draw.text((120, 78), label, font=font(22, bold=True), fill=fade(DIMMER, alpha))


def footer_bar(draw, text, alpha=1):
    if not text:
        return
    draw.rounded_rectangle((120, 930, 1800, 1004), radius=16, fill=fade(PANEL, alpha))
    draw.text((148, 952), text, font=font(28), fill=fade(TEXT, alpha))


def card(draw, box, fill, outline, width=2):
    draw.rounded_rectangle(box, radius=18, fill=fill, outline=outline, width=width)


def draw_title(draw, t, dur, data):
    a = ease(t / 0.45)
    kicker(draw, data["kicker"], a)
    y = 280
    fnt = font(84, bold=True, serif=True)
    for line in data["headline"].split("\n"):
        draw.text((120, y), line, font=fnt, fill=fade(TEXT, a))
        y += 100
    draw.text((120, y + 36), data["sub"], font=font(32), fill=fade(DIM, a))


def draw_quiz(draw, t, dur, data):
    a = ease(t / 0.35)
    kicker(draw, "QUICK QUESTION", a)
    y = 160
    fnt = font(54, bold=True, serif=True)
    for line in wrap(draw, data["question"], fnt, 1680):
        draw.text((120, y), line, font=fnt, fill=fade(TEXT, a))
        y += 70
    opts = data["options"]
    reveal = ease((t - dur * 0.55) / 0.35)
    top = 430
    for i, opt in enumerate(opts):
        x = 120 + i * 580
        chosen = i == data["answer"] and reveal > 0.05
        fill = fade(ACCENT_D if chosen else PANEL, a)
        outline = fade(ACCENT if chosen else LINE, a)
        card(draw, (x, top, x + 540, top + 220), fill, outline, 3 if chosen else 2)
        draw.text((x + 28, top + 28), f"{i + 1}", font=font(22, bold=True), fill=fade(DIMMER, a))
        for j, line in enumerate(wrap(draw, opt, font(32, bold=True), 480)):
            draw.text((x + 28, top + 80 + j * 42), line, font=font(32, bold=True), fill=fade(TEXT, a))
    if reveal > 0.05:
        yy = 700
        for line in data["why"].split("\n"):
            draw.text((120, yy), line, font=font(36, bold=True), fill=fade(AMBER, reveal))
            yy += 46


def draw_floor(draw, t, dur, data):
    a = ease(t / 0.35)
    kicker(draw, data["label"], a)
    draw.text((120, 160), data["formula"], font=font(64, bold=True, serif=True), fill=fade(TEXT, a))
    draw.text((120, 250), data["note"], font=font(32), fill=fade(DIM, a))
    for i, (name, value) in enumerate(data["cards"]):
        ca = ease((t - 0.35 - i * 0.18) / 0.3)
        x = 120 + i * 580
        card(draw, (x, 380, x + 540, 760), fade(PANEL_HI, ca), fade(ACCENT, ca), 3)
        draw.text((x + 36, 430), name, font=font(28, bold=True), fill=fade(DIM, ca))
        draw.text((x + 36, 520), value, font=font(72, bold=True, serif=True), fill=fade(TEXT, ca))
        draw.text((x + 36, 640), "weights only", font=font(26), fill=fade(DIMMER, ca))


def draw_headroom(draw, t, dur, data):
    a = ease(t / 0.35)
    kicker(draw, data["label"], a)
    draw.text((120, 160), data["host"], font=font(48, bold=True, serif=True), fill=fade(TEXT, a))
    bar = (120, 280, 1800, 360)
    draw.rounded_rectangle(bar, radius=12, fill=fade(PANEL, a))
    frac = data["used"] / data["total"]
    fill_w = int((bar[2] - bar[0]) * frac * ease((t - 0.2) / 0.6))
    if fill_w > 8:
        draw.rounded_rectangle((bar[0], bar[1], bar[0] + fill_w, bar[3]), radius=12, fill=fade(AMBER, a))
    draw.text((120, 390), f"{data['floor']} of {data['total']} GB", font=font(32, bold=True), fill=fade(AMBER, a))
    draw.text((120, 450), data["left"], font=font(30), fill=fade(TEXT, a))
    for i, item in enumerate(data["adds"]):
        ca = ease((t - 0.5 - i * 0.08) / 0.25)
        x = 120 + (i % 3) * 560
        y = 580 + (i // 3) * 90
        card(draw, (x, y, x + 520, y + 70), fade(PANEL, ca), fade(LINE, ca))
        draw.text((x + 24, y + 18), item, font=font(26), fill=fade(TEXT, ca))


def draw_rows(draw, t, data, tone="accent"):
    a = ease(t / 0.3)
    kicker(draw, data["label"], a)
    color = ACCENT if tone == "accent" else AMBER
    for i, (name, value) in enumerate(data["rows"]):
        ca = ease((t - 0.25 - i * 0.16) / 0.28)
        y = 200 + i * 180
        card(draw, (120, y, 1800, y + 150), fade(PANEL, ca), fade(color, ca), 3)
        draw.text((160, y + 28), name, font=font(24, bold=True), fill=fade(DIMMER, ca))
        draw.text((160, y + 70), value, font=font(36, bold=True), fill=fade(TEXT, ca))
    if data.get("foot"):
        footer_bar(draw, data["foot"], ease((t - 1.1) / 0.3))


def draw_ladder(draw, t, dur, data):
    draw_rows(draw, t, data, "accent")


def draw_candidates(draw, t, dur, data):
    draw_rows(draw, t, data, "amber")


def draw_contexts(draw, t, dur, data):
    a = ease(t / 0.3)
    kicker(draw, data["label"], a)
    for i, label in enumerate(data["cards"]):
        ca = ease((t - 0.2 - i * 0.18) / 0.3)
        x = 120 + i * 580
        card(draw, (x, 200, x + 540, 460), fade(PANEL_HI, ca), fade(ACCENT, ca), 3)
        draw.text((x + 36, 280), label, font=font(80, bold=True, serif=True), fill=fade(TEXT, ca))
    for i, item in enumerate(data["record"]):
        ca = ease((t - 0.9 - i * 0.08) / 0.25)
        x = 120 + (i % 2) * 860
        y = 520 + (i // 2) * 100
        card(draw, (x, y, x + 820, y + 80), fade(PANEL, ca), fade(LINE, ca))
        draw.text((x + 28, y + 22), item, font=font(28), fill=fade(TEXT, ca))
    footer_bar(draw, data["foot"], ease((t - 1.3) / 0.3))


def draw_checklist(draw, t, dur, data):
    a = ease(t / 0.3)
    kicker(draw, data["label"], a)
    for i, (n, text) in enumerate(data["items"]):
        ca = ease((t - 0.25 - i * 0.16) / 0.28)
        y = 190 + i * 160
        card(draw, (120, y, 1800, y + 140), fade(PANEL, ca), fade(ACCENT, ca), 3)
        draw.text((160, y + 42), n, font=font(36, bold=True), fill=fade(ACCENT, ca))
        draw.text((240, y + 46), text, font=font(34, bold=True), fill=fade(TEXT, ca))
    footer_bar(draw, data["foot"], ease((t - 1.2) / 0.3))


def draw_steps(draw, t, dur, data):
    a = ease(t / 0.3)
    kicker(draw, data["label"], a)
    for i, (n, title, sub) in enumerate(data["steps"]):
        ca = ease((t - 0.2 - i * 0.12) / 0.25)
        y = 170 + i * 140
        card(draw, (120, y, 1800, y + 124), fade(PANEL, ca), fade(ACCENT, ca), 3)
        draw.text((156, y + 36), n, font=font(32, bold=True), fill=fade(ACCENT, ca))
        draw.text((230, y + 22), title, font=font(32, bold=True), fill=fade(TEXT, ca))
        draw.text((230, y + 68), sub, font=font(26), fill=fade(DIM, ca))


def draw_stop(draw, t, dur, data):
    a = ease(t / 0.3)
    kicker(draw, data["label"], a)
    for i, text in enumerate(data["stops"]):
        ca = ease((t - 0.2 - i * 0.12) / 0.25)
        x = 120 + i * 580
        card(draw, (x, 200, x + 540, 420), fade(PANEL_HI, ca), fade(AMBER, ca), 3)
        for j, line in enumerate(wrap(draw, text, font(32, bold=True), 460)):
            draw.text((x + 32, 280 + j * 42), line, font=font(32, bold=True), fill=fade(TEXT, ca))
    for i, text in enumerate(data["nevers"]):
        ca = ease((t - 0.8 - i * 0.1) / 0.25)
        y = 480 + i * 120
        card(draw, (120, y, 1800, y + 100), fade(PANEL, ca), fade(ACCENT, ca), 3)
        draw.text((160, y + 30), text, font=font(32, bold=True), fill=fade(TEXT, ca))
    footer_bar(draw, data["foot"], ease((t - 1.2) / 0.3))


def draw_rule(draw, t, dur, data):
    a = ease(t / 0.35)
    kicker(draw, data["kicker"], a)
    y = 180
    for i, line in enumerate(data["lines"]):
        ca = ease((t - 0.15 - i * 0.12) / 0.25)
        tone = ACCENT if line.get("tone") == "accent" else TEXT
        fnt = font(40, bold=True, serif=True)
        draw.text((140, y), line["text"], font=fnt, fill=fade(tone, ca))
        y += 78
    draw.text((140, 900), data["foot"], font=font(22, bold=True), fill=fade(DIMMER, a))


def draw_statement(draw, t, dur, data):
    a = ease(t / 0.4)
    y = 220
    fnt = font(64, bold=True, serif=True)
    for line in data["headline"].split("\n"):
        draw.text((120, y), line, font=fnt, fill=fade(TEXT, a))
        y += 84
    draw.text((120, y + 30), data.get("sub", ""), font=font(30), fill=fade(DIM, a))


def draw_outro(draw, t, dur, data):
    a = ease(t / 0.4)
    y = 300
    for line in data["headline"].split("\n"):
        draw.text((120, y), line, font=font(84, bold=True, serif=True), fill=fade(TEXT, a))
        y += 100
    draw.text((120, y + 24), data["sub"], font=font(32), fill=fade(ACCENT, a))


DRAW = {
    "title": draw_title,
    "quiz": draw_quiz,
    "floor": draw_floor,
    "headroom": draw_headroom,
    "ladder": draw_ladder,
    "candidates": draw_candidates,
    "contexts": draw_contexts,
    "checklist": draw_checklist,
    "steps": draw_steps,
    "stop": draw_stop,
    "rule": draw_rule,
    "statement": draw_statement,
    "outro": draw_outro,
}


def render_frame(scene, t, dur):
    img, draw = new_frame()
    DRAW[scene["visual"]](draw, t, dur, scene["data"])
    # NumPy is the buffer the encoder reads. Keep the array contiguous RGB.
    arr = np.asarray(img, dtype=np.uint8)
    if arr.shape != (H, W, 3):
        raise RuntimeError(f"frame shape {arr.shape}")
    return arr


def check(spec):
    dur = 8.0
    for scene in spec["scenes"]:
        if scene["visual"] not in DRAW:
            raise SystemExit(f"no drawer for {scene['visual']}")
        arr = render_frame(scene, dur * 0.72, dur)
        if int(arr.mean()) < 8:
            raise SystemExit(f"{scene['id']} frame is blank")
        print(f"  frame {scene['id']} {arr.shape} mean {arr.mean():.1f}")
    print(f"check ok: {len(spec['scenes'])} scenes, no video written")


def redact(blob):
    text = blob.decode("utf-8", "replace") if isinstance(blob, (bytes, bytearray)) else str(blob)
    key = os.environ.get("XAI_API_KEY") or ""
    if key and key in text:
        text = text.replace(key, "[redacted]")
    text = re.sub(r"Bearer\s+\S+", "Bearer [redacted]", text)
    text = re.sub(r"xai-[A-Za-z0-9_\-]{8,}", "[redacted]", text)
    return text[:400]


def tts_scene(text, dest):
    key = os.environ.get("XAI_API_KEY")
    if not key:
        raise SystemExit("XAI_API_KEY is not set. Refusing to write a silent or dummy video.")
    payload = json.dumps({
        "text": text,
        "voice_id": VOICE,
        "language": "en",
        "speed": SPEED,
        "output_format": {"codec": "mp3", "sample_rate": 44100, "bit_rate": 128000},
    }).encode()
    req = urllib.request.Request(
        TTS_URL,
        data=payload,
        method="POST",
        headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            ctype = resp.headers.get("Content-Type", "")
            data = resp.read()
    except urllib.error.HTTPError as err:
        body = redact(err.read() if err.fp else b"")
        raise SystemExit(f"TTS HTTP {err.code} for a scene. Redacted body: {body}") from None
    if b"json" in ctype.encode() or data[:1] in (b"{", b"["):
        parsed = json.loads(data)
        raw = parsed.get("audio") or parsed.get("audio_base64")
        if not raw:
            raise SystemExit("TTS JSON had no audio field. The key was not logged.")
        data = base64.b64decode(raw)
    if len(data) < 100:
        raise SystemExit("TTS returned too little audio. Refusing to continue.")
    open(dest, "wb").write(data)


def run(cmd, **kwargs):
    proc = subprocess.run(cmd, **kwargs)
    if proc.returncode != 0:
        raise SystemExit(f"command failed ({proc.returncode}): {cmd[0]}")
    return proc


def probe_duration(path):
    proc = run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
        check=False, capture_output=True, text=True,
    )
    return float(proc.stdout.strip())


def measure_loudness(path):
    proc = subprocess.run(
        ["ffmpeg", "-hide_banner", "-i", path, "-af", "loudnorm=I=-16:TP=-1.5:LRA=11:print_format=summary",
         "-f", "null", "-"],
        capture_output=True, text=True,
    )
    text = proc.stderr
    integrated = re.search(r"Input Integrated:\s+(-?[\d.]+)", text)
    peak = re.search(r"Input True Peak:\s+(-?[\d.]+)", text)
    if not integrated or not peak:
        raise SystemExit("Could not read loudnorm summary.")
    return float(integrated.group(1)), float(peak.group(1))


def _loudnorm_json(text):
    start = text.rfind("{")
    end = text.rfind("}")
    if start == -1 or end <= start:
        raise SystemExit("Could not read loudnorm measurement.")
    return json.loads(text[start:end + 1])


def loudnorm(src, dest):
    """Two-pass loudnorm to -16 LUFS, true peak held to -1.5 dBTP (within ≤ -1).

    A single-pass filter often undershoots on this voice, and a loose limiter
    (0.89) can let true peak exceed -1 dBTP after a trim. This matches
    finish_se201.sh's tighter limiter (0.82) when a small gain pass is needed.
    """
    proc = subprocess.run(
        ["ffmpeg", "-hide_banner", "-i", src, "-af",
         "loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"],
        capture_output=True, text=True,
    )
    m = _loudnorm_json(proc.stderr)
    filt = (
        "loudnorm=I=-16:TP=-1.5:LRA=11:"
        f"measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
        f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:"
        f"offset={m['target_offset']}:linear=true"
    )
    run(["ffmpeg", "-v", "error", "-y", "-i", src, "-af", filt,
         "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-ar", "44100", "-movflags", "+faststart", dest])
    for _ in range(3):
        integrated, peak = measure_loudness(dest)
        print(f"loudness integrated {integrated:.2f} LUFS, true peak {peak:.2f} dBTP")
        if abs(integrated - (-16)) < 0.4 and peak <= -1.0:
            return integrated, peak
        # A small trim only. Do not print the filter graph with any secret in it.
        gain = max(-3.0, min(3.0, -16 - integrated))
        tmp = dest + ".gain.mp4"
        run(["ffmpeg", "-v", "error", "-y", "-i", dest,
             "-af", f"volume={gain:.2f}dB,alimiter=limit=0.82:attack=2:release=40:level=false",
             "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-ar", "44100", "-movflags", "+faststart", tmp])
        os.replace(tmp, dest)
    integrated, peak = measure_loudness(dest)
    if peak > -1.0 or abs(integrated - (-16)) > 1.0:
        raise SystemExit(f"Loudness out of range: {integrated:.2f} LUFS, true peak {peak:.2f} dBTP")
    return integrated, peak


def write_timeline(spec, spans, dest):
    lines = [spec["title"], ""]
    for scene, start, dur in spans:
        lines.append(f"  {scene['id']:<16} {start:7.2f}s + {dur:6.2f}s  {scene['visual']}")
    lines.append("")
    open(dest, "w").write("\n".join(lines))


def render(spec, out_dir):
    if not os.environ.get("XAI_API_KEY"):
        raise SystemExit("XAI_API_KEY is not set. Refusing to write a silent or dummy video.")
    os.makedirs(out_dir, exist_ok=True)
    audio_dir = os.path.join(out_dir, "audio")
    os.makedirs(audio_dir, exist_ok=True)
    spans = []
    cursor = 0.0
    list_path = os.path.join(audio_dir, "concat.txt")
    with open(list_path, "w") as handle:
        for scene in spec["scenes"]:
            dest = os.path.join(audio_dir, scene["id"] + ".mp3")
            print("narrate", scene["id"])
            tts_scene(scene["text"], dest)
            dur = probe_duration(dest)
            if dur < 0.3:
                raise SystemExit(f"{scene['id']} audio is too short")
            spans.append((scene, cursor, dur))
            cursor += dur
            handle.write(f"file '{dest}'\n")
    concat = os.path.join(audio_dir, "all.m4a")
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", list_path,
         "-c:a", "aac", "-b:a", "160k", "-ar", "44100", concat])
    raw_video = os.path.join(out_dir, "lesson.prenorm.mp4")
    cmd = [
        "ffmpeg", "-y", "-v", "error",
        "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "pipe:0",
        "-i", concat,
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
        "-c:a", "aac", "-b:a", "160k", "-ar", "44100", "-shortest", raw_video,
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    try:
        for scene, _start, dur in spans:
            n = max(1, int(round(dur * FPS)))
            last = None
            i = 0
            while i < n:
                t = i / FPS
                # Fade the open of each scene at full frame rate, then hold.
                step = 1 if t < 1.2 else 6
                last = render_frame(scene, t, dur).tobytes()
                for _ in range(min(step, n - i)):
                    proc.stdin.write(last)
                i += step
    finally:
        proc.stdin.close()
        code = proc.wait()
    if code != 0:
        raise SystemExit(f"ffmpeg encode failed ({code})")
    final = os.path.join(out_dir, "se301-01-size-the-model-run-the-first-endpoint.mp4")
    integrated, peak = loudnorm(raw_video, final)
    poster = os.path.join(out_dir, "poster.jpg")
    run(["ffmpeg", "-v", "error", "-y", "-ss", "0.8", "-i", final, "-frames:v", "1", "-q:v", "3", poster])
    log_path = os.path.join(out_dir, "render-timeline.log")
    write_timeline(spec, spans, log_path)
    vtt = os.path.join(out_dir, "se301-01-size-the-model-run-the-first-endpoint.vtt")
    make_vtt.write_vtt(spec, open(log_path).read(), vtt)
    chapters = [{"title": scene["chapter"] or scene["id"], "start_seconds": round(start, 3)}
                for scene, start, _dur in spans if scene["chapter"]]
    json.dump(chapters, open(os.path.join(out_dir, "chapters.json"), "w"), indent=2)
    open(os.path.join(out_dir, "chapters.json"), "a").write("\n")
    print(f"wrote {final}")
    print(f"loudness {integrated:.2f} LUFS, true peak {peak:.2f} dBTP")
    print(f"poster {poster}")
    print(f"captions {vtt}")
    print("Media stays in build/. Do not commit it. Wire the public player only after Clark approves.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Draw one frame per scene. No network, no MP4.")
    parser.add_argument("--script", default=os.path.join(HERE, "se301-01-first-endpoint.json"))
    parser.add_argument("--out", default=os.path.join(HERE, "build"))
    args = parser.parse_args()
    spec = json.load(open(args.script))
    if spec.get("voice") != VOICE or spec.get("speed") != SPEED:
        raise SystemExit("Scene script voice or speed does not match this renderer.")
    if args.check:
        check(spec)
        return
    render(spec, args.out)


if __name__ == "__main__":
    main()
