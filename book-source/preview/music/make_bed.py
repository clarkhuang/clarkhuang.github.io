#!/usr/bin/env python3
"""Original instrumental bed for the Silicon Valley C Players preview.

No third-party samples. A dark, slow electronic pad in E minor with a
low pulse and a late rise into the closing hook.
"""
from __future__ import annotations

import math
import numpy as np
from pathlib import Path

SR = 44100
DUR = 182.5  # voice is 179.90s; short tail after "Coming in 2027"


def env(n, atk=0.02, rel=0.08):
    e = np.ones(n, dtype=np.float64)
    a = max(1, int(atk * n))
    r = max(1, int(rel * n))
    e[:a] = np.linspace(0, 1, a)
    e[-r:] = np.linspace(1, 0, r)
    return e


def sine(freq, t, amp=1.0):
    return amp * np.sin(2 * math.pi * freq * t)


def pad(t, freqs, amp, lfo_hz=0.07):
    out = np.zeros_like(t)
    for i, f in enumerate(freqs):
        # slight detune for width
        det = 1 + (0.0015 if i % 2 == 0 else -0.0015)
        tone = sine(f * det, t)
        # slow amplitude shimmer
        tone *= 0.7 + 0.3 * np.sin(2 * math.pi * lfo_hz * t + i)
        out += tone
    out /= max(len(freqs), 1)
    return amp * out


def lowpass(x, cutoff, sr=SR):
    """One-pole lowpass."""
    rc = 1 / (2 * math.pi * cutoff)
    dt = 1 / sr
    a = dt / (rc + dt)
    y = np.empty_like(x)
    acc = 0.0
    for i, v in enumerate(x):
        acc = acc + a * (v - acc)
        y[i] = acc
    return y


def pluck(freq, t0, dur, t, amp):
    out = np.zeros_like(t)
    mask = (t >= t0) & (t < t0 + dur)
    if not np.any(mask):
        return out
    tt = t[mask] - t0
    tone = np.sin(2 * math.pi * freq * tt) * np.exp(-tt * 3.2)
    # a little odd harmonic
    tone += 0.18 * np.sin(2 * math.pi * freq * 2 * tt) * np.exp(-tt * 5.0)
    out[mask] = amp * tone
    return out


def main():
    n = int(SR * DUR)
    t = np.arange(n) / SR
    L = np.zeros(n)
    R = np.zeros(n)

    # --- form: sparse open, mid pulse, late rise ---
    # opening drone (E1 / E2)
    drone = pad(t, [41.20, 82.41], amp=0.22, lfo_hz=0.05)
    # main pad E minor: E3 G3 B3 D4, later add A3 F#4
    pad_a = pad(t, [164.81, 196.00, 246.94, 293.66], amp=0.28, lfo_hz=0.08)
    # rise pad from ~2:10
    rise_gate = np.clip((t - 125) / 25, 0, 1)
    rise_gate = rise_gate * rise_gate * (3 - 2 * rise_gate)
    pad_b = pad(t, [329.63, 392.00, 493.88], amp=0.20, lfo_hz=0.11) * rise_gate

    # soft pulse at 60 bpm (one hit per second), very quiet early, a bit more later
    pulse = np.zeros(n)
    for k in range(int(DUR) + 2):
        t0 = k * 1.0
        if t0 >= DUR:
            break
        # heartbeat-ish: two close sines, decaying
        mask = (t >= t0) & (t < t0 + 0.45)
        tt = t[mask] - t0
        hit = (np.sin(2 * math.pi * 55 * tt) + 0.4 * np.sin(2 * math.pi * 82.4 * tt)) * np.exp(-tt * 8)
        # intensity curve
        if t0 < 20:
            a = 0.04
        elif t0 < 130:
            a = 0.07
        else:
            a = 0.11
        pulse[mask] += a * hit

    # sparse high plucks — a simple E-minor motif, more frequent near the hook
    motif = [659.25, 493.88, 587.33, 523.25]  # E5 B4 D5 C5
    plucks = np.zeros(n)
    # early: occasional, every ~8s starting after the disclaimer
    starts = list(np.arange(18, 120, 8.0))
    # late: every 4s, then a rising run into the close
    starts += list(np.arange(124, 165, 4.0))
    # closing figure ~2:48 onward (more chapters / 2027)
    starts += [168.0, 170.0, 172.0, 174.0, 176.0, 177.5]
    close_freqs = [329.63, 392.00, 493.88, 587.33, 659.25, 783.99]  # rising
    for i, t0 in enumerate(starts):
        if t0 >= 168:
            f = close_freqs[min(i - starts.index(168.0), len(close_freqs) - 1)]
            amp = 0.11
            durp = 2.4
        elif t0 >= 124:
            f = motif[i % len(motif)]
            amp = 0.07
            durp = 1.8
        else:
            f = motif[i % len(motif)]
            amp = 0.045
            durp = 1.6
        plucks += pluck(f, t0, durp, t, amp)

    # a held high fifth under the last card
    last = np.zeros(n)
    mask = t >= 170
    if np.any(mask):
        tt = t[mask] - 170
        fade = np.clip(tt / 2.0, 0, 1) * np.clip((DUR - 1.2 - t[mask]) / 2.5, 0, 1)
        last[mask] = 0.08 * fade * (
            np.sin(2 * math.pi * 659.25 * t[mask]) + 0.6 * np.sin(2 * math.pi * 987.77 * t[mask])
        )

    mono = drone + pad_a + pad_b + pulse + plucks + last
    # gentle overall fade in/out
    fade_in = np.clip(t / 5.0, 0, 1)
    fade_out = np.clip((DUR - 0.15 - t) / 3.0, 0, 1)
    mono *= fade_in * fade_out

    # stereo: slight delay / pan on pad and plucks
    delay = int(0.012 * SR)
    L[:] = mono
    R[:] = mono
    R[delay:] += 0.18 * (pad_a + pad_b + plucks)[:-delay]
    L[delay:] += 0.12 * plucks[:-delay]
    # normalize to about -22 dBFS peak before mix (room to duck)
    peak = max(np.max(np.abs(L)), np.max(np.abs(R)), 1e-9)
    gain = 0.25 / peak  # conservative
    L *= gain
    R *= gain

    stereo = np.stack([L, R], axis=1)
    # 24-bit wav
    out = Path(__file__).parent / "preview-bed.wav"
    import wave
    pcm = np.clip(stereo, -1, 1)
    pcm = (pcm * 8388607).astype(np.int32)
    # pack 24-bit little-endian
    raw = bytearray()
    for s in pcm.reshape(-1):
        v = int(s) & 0xFFFFFF
        raw += bytes((v & 0xFF, (v >> 8) & 0xFF, (v >> 16) & 0xFF))
    with wave.open(str(out), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(3)
        w.setframerate(SR)
        w.writeframes(bytes(raw))
    print("wrote", out, "dur", DUR, "peak", float(peak * gain))


if __name__ == "__main__":
    main()
