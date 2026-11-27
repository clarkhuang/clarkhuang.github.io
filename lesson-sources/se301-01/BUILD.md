# How to build Software Engineering 301, Lesson 1

Lesson: **Size the model, then run the first endpoint** — Software Engineering 301.
Page: https://clarkhuang.github.io/software-engineering-301/01-size-the-model-run-the-first-endpoint/

This folder is the source for the lesson. The public page is a full video lesson. To rebuild the video, follow the render steps below, then copy the media into the site tree and run `publish_page.py`.

| File | What it is |
|---|---|
| `make_se301_01.py` | Narration and the on-screen spec. Edit this, then regenerate the JSON. |
| `se301-01-first-endpoint.json` | The scene script the renderer reads. |
| `render_se301_01.py` | Pillow, NumPy, and ffmpeg. 1920×1080, 30 fps. Narrates, normalizes, writes MP4, captions, poster, and chapters. |
| `make_vtt.py` | WebVTT from the scene script and the render timeline. |
| `publish_page.py` | Writes the public `index.html`, `index.md`, and `AGENTS.md` from the script and the prompt. Once the MP4, captions, and poster are in the site tree, it writes a full video lesson page. |
| `install-prompt.md` | The copy-paste Mac and PC install prompt. Canonical text. |
| `facts.md` | Every factual claim, with its source. Writer-added lines are marked for a yes or no. |
| `brief.md` | The brief the lesson was written from. |
| `claims-removed.md` | Claims that were available and left out. |

## Before you narrate

Clark reviews `facts.md` and the scene script before any narration. The first render was approved on November 26, 2026. `render_se301_01.py` will not write a silent or dummy MP4. It reads `XAI_API_KEY` from the environment at call time and never writes that key to a file, a log, or a command line.

## Check the drawings without a key

```bash
python3 make_se301_01.py
python3 render_se301_01.py --check
python3 publish_page.py
python3 sitegen/check_site.py .
```

`--check` draws one frame per scene and exits. It does not open a network connection and does not write an MP4.

## Render, after approval (or to rebuild)

From this folder, on the build machine:

```bash
python3 make_se301_01.py
# XAI_API_KEY must already be in the environment. Do not put it in the command.
python3 render_se301_01.py
```

Outputs land in `lesson-sources/se301-01/build/` (gitignored):

- `se301-01-size-the-model-run-the-first-endpoint.mp4`
- `se301-01-size-the-model-run-the-first-endpoint.vtt`
- `poster.jpg`
- `chapters.json`
- `render-timeline.log`
- per-scene MP3 files under `audio/`

- Voice: xAI `POST https://api.x.ai/v1/tts`, custom voice `4lbl0krw73vf`, language `en`, speed `1.05`.
- Speech tags in the script: `[pause]`, `<emphasis>`, `<slow>`. No laugh or chuckle tags.
- Picture: 1920×1080, 30 fps, H.264, `+faststart`. The encoder reads a contiguous NumPy RGB array from each Pillow frame.
- Audio: AAC 160 kbps, 44.1 kHz. Loudness is normalized to about −16 LUFS integrated. The limiter target is −1.5 dBTP, which is inside the −1 dBTP ceiling. The script stops if the measured true peak is hotter than −1 dBTP.
- Captions: `make_vtt.py`, using scene times from `render-timeline.log`. The public transcript uses the same readable spellings (for example “A.I.” as AI and “three oh one” as 301).

## After the media exists

Copy the MP4, VTT, and poster into the site tree as `videos/se301-01-size-the-model-run-the-first-endpoint.mp4`, the matching `.vtt`, and `videos/posters/se301-01-size-the-model-run-the-first-endpoint.jpg`. Then run `python3 publish_page.py` from this folder so the public player, captions, chapters, and catalog entry are written. Do not add Software Engineering 301 to `sitegen/content.json` as a series: that generator would replace the playbook page. Keep the playbook, and point the lesson page at the new files. Run `python3 sitegen/stamp_versions.py` and `python3 sitegen/check_site.py .`. Open the pull request against `next-revision`. Only Clark merges to `main`.

`REBUILD.md` in the site root says how to run the generator without rewriting other sections' pages.

## Authorship

The script, the on-screen summary, the install prompt, and rule 1 were written for this lesson from the SE 301 playbook and the public docs listed in `facts.md`. They are not quotes from Clark. The first narration and render were completed after Clark approved the script. Listen to the final audio before merging to production if that review is still outstanding.
