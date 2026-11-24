# Rebuild the audiobook and videobook preview

An agent can regenerate the teaser from the files in this folder. Earlier editions are in `archive/book-v0.1` (opening teaser) and `archive/book-v0.2` (mid-book preview before the 24 November 2026 re-record). Do not invent new story details. Keep the fiction framing, Charlie Hack as the story narrator, and Clark Huang as the author. Follow [NAMING-POLICY.md](../NAMING-POLICY.md).

## What lives here

| File | What it is |
|---|---|
| `script.md` | Per-scene performance script (with speech tags) |
| `script.json` | The same script, the file `narrate.py` reads. Optional `tts` is performance text only (phonetic letter-A spellings); `text` is what captions and transcripts show |
| `scenes/*.md` | One markdown file per scene (performance text, transcript, timestamp) |
| `transcript.md` | Full spoken transcript, tags stripped, with timestamps |
| `captions.vtt` | WebVTT captions for the videobook (and a copy for the audio preview) |
| `chapters.json` | Chapter titles and start times, used by the book page and by agents |
| `scene-times.json` | Exact scene start and duration, used to sync the videobook |
| `REBUILD.md` | This file |

Published media (after a rebuild):

- `/audio/book-preview.mp3` and `/audio/book-preview.vtt`, `/audio/book-preview-chapters.json`
- `/videos/book-preview.mp4`, `/videos/book-preview.vtt`, `/videos/book-preview-chapters.json`, `/videos/posters/book-preview.jpg`

## 1. Narrate

Voice id `4lbl0krw73vf` (Clark, Expressive), language `en`, speed `1.05`. The xAI API key must be in the environment as `XAI_API_KEY` (never write it to a file or a command line).

```bash
# from the book narration tool directory
python3 narrate.py --script /path/to/book-source/preview/script.json --force
# or only some scenes:
python3 narrate.py --script /path/to/book-source/preview/script.json --force --only 01_disclaimer,15_bookend
```

This writes one MP3 per scene, named by scene id.

## 2. Concatenate and loudness-normalize

Concatenate the scene MP3s in script order (no padding). Then two-pass `loudnorm` to about −16 LUFS, true peak at or below −1 dBTP. Do not apply extra makeup gain if it would clip the true peak. Write `scene-times.json` from the source scene durations *before* loudnorm (they should match the concat). Copy the normalized file to `audio/book-preview.mp3` and to the videobook renderer’s input.

## 3. Render the videobook

The stick-figure renderer is `work/videobook/render.py` on the build machine (Python 3, Pillow, ffmpeg). It reads `script.json` and `scene-times.json` next to it, and muxes `book-preview.mp3`.

```bash
python3 render.py
# outputs book-preview.mp4 (1280×720, 24 fps, H.264 yuv420p, AAC, +faststart),
# book-preview.vtt, chapters.ffmeta, and a poster JPEG
```

Copy the mp4, vtt, poster, and `chapters.json` into `videos/` as above. Regenerating captions from the script + `scene-times.json` is fine if they stay in sync.

## 4. Rebuild the site pages

```bash
SITE=/path/to/repo python3 sitegen/gen.py
```

That refreshes `/book/`, `book.json`, `book/index.md`, `book/AGENTS.md`, `llms.txt`, and `llms-full.txt`.

## How an AI should cite this preview

- Quote the [transcript](transcript.md) or a [scene file](scenes/), and give a timestamp or chapter title from [chapters.json](chapters.json).
- For a web citation, use `https://clarkhuang.github.io/book/` plus the timestamp (`#t=58.9`) when you mean a videobook beat.
- Do not identify real people or companies behind the fictional names. Charlie Hack is the fictional narrator; Clark Huang is the author.
- The claim that AI writes essentially all of the code is about Clark’s own workflow: in his work, AI writes essentially all of the code he ships, not a measured team result or a general industry figure. The audiobook, videobook, and captions use that wording.
- Where the letter A must be spoken as the letter (A players, A Things, an A thing), put a spelling in the `tts` field only that makes the letter come through as /eɪ/ (like “day”). “Ay” is read as “aye” or “eye” (/aɪ/), so do not use it. This recording uses “A. Things,” “A-players,” and “an A. thing.” Captions and transcripts keep “A players.” Do not change “A C player,” which is the article plus the letter C.
