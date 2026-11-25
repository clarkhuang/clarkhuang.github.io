# Rebuilding the Silicon Valley C Players preview

An agent can regenerate the teaser from the files in this folder. Earlier editions are in `archive/book-v0.1` (opening teaser), `archive/book-v0.2` (mid-book preview before the 24 November 2026 re-record), and `archive/book-v0.3` (the mid-book preview of 24 November 2026, 2:59). This folder is the 25 November 2026 start-to-finish preview (3:04). Do not invent new story details. Keep the fiction framing, Charlie Hack as the story narrator, and Clark Huang as the author. Follow [NAMING-POLICY.md](../NAMING-POLICY.md).

## What this preview is

A three-minute start-to-finish arc, built from lines in the drafted book, the story arc, Building Blocks, Chapter 36, and the 75th-percentile C-player thesis. It is not a mid-book excerpt. It opens on the green-screen dream, pays off the 75th-percentile idea, and ends with “More chapters are coming.”

There is no music bed. The soundtrack is a single mono voice track.

## Published media

- `/audio/book-preview.mp3` and `/audio/book-preview.vtt`, `/audio/book-preview-chapters.json`
- `/videos/book-preview.mp4`, `/videos/book-preview.vtt`, `/videos/book-preview-chapters.json`, `/videos/posters/book-preview.jpg`

Voice: xAI custom voice `4lbl0krw73vf`, speed 1.05. Narrate each scene from `script.json` (use the `tts` field when present, so “A-players” is spoken correctly; captions keep “A players”). Concatenate the scene MP3s in script order (no padding). Then two-pass `loudnorm` to about −16 LUFS, true peak at or below −1 dBTP. Do not apply extra makeup gain if it would clip the true peak. Write `scene-times.json` from the source scene durations *before* loudnorm (they should match the concat). Copy the normalized file to `audio/book-preview.mp3` and to the videobook renderer’s input.

The stick-figure renderer is `work/videobook/render.py` on the build machine (Python 3, Pillow, ffmpeg). It reads `script.json` and `scene-times.json` next to it, and muxes `book-preview.mp3`.

```
python3 render.py --stills   # contact sheets
python3 render.py            # outputs book-preview.mp4 (1280×720, 24 fps, H.264 yuv420p, AAC, +faststart),
                             # book-preview.vtt, chapters.ffmeta, and a poster JPEG
```

Copy the mp4, vtt, poster, and `chapters.json` into `videos/` as above. Regenerating captions from the script + `scene-times.json` is fine if they stay in sync. After replacing media, run `python3 sitegen/stamp_versions.py` and `python3 sitegen/check_site.py .`.

Do not run a full `gen.py` just to refresh this preview. The book-page mid-book strings in `sitegen/gen.py` must stay updated so a later generation does not revert the start-to-finish copy.
