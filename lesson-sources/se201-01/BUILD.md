# How Software Engineering 201, Lesson 1 was built

Lesson: **Four Eras of Building Systems** — Software Engineering 201: From Loop to Enterprise Systems.
Page: https://clarkhuang.github.io/software-engineering-201/01-four-eras-of-building-systems/

This folder is the source for the lesson video, so a person or an agent can read, check, change, and rebuild it.

| File | What it is |
|---|---|
| `make_se201_01_four_eras.py` | The script source: narration text and the on-screen visual spec for every scene. Edit this, not the JSON. |
| `se201-01-four-eras.json` | The generated scene script that the narrator and renderer read. |
| `se201_layouts_eras.py` | Renderer layouts added for this lesson: `eras` (four eras side by side, built up one beat at a time) and `constants` (what stayed true in every era). |
| `se101_layouts6.py` | Renderer layouts from lessons 3 and 4. This lesson uses `graph` (the roles, and the billing illustration). |
| `finish_se201.sh` | The finish step: loudness, faststart MP4, poster, captions, and the copy into a site checkout. Takes arguments, so one script serves every Software Engineering 201 lesson. |
| `make_vtt.py` | Writes the WebVTT captions from the scene script and the render timeline. |
| `render-timeline.log` | Scene start times and lengths from the render (used for chapters and captions). |
| `facts.md` | Every factual claim in the lesson, spoken or on screen, with its source. Teaching framings are marked as such. |
| `brief.md` | The brief (prompt) the lesson was written from. |
| `review-round1.md`, `review-round2.md` | The two rounds of critique on the draft script, and what changed after each. |
| `claims-removed.md` | Claims from the first draft that were removed or toned down, and why. |

## Rebuild

The renderer is the same one used for every Software Engineering 101 and 201 video (`render_se101.py` on top of the AI Tips `render.py`). It lives on the build machine, not in this repository. `se101_layouts6.py` and `se201_layouts_eras.py` must sit beside `render_se101.py`, which needs one import line for each to register the layouts:

```python
import se101_layouts6      # registers graph, crossing, lanes
import se201_layouts_eras  # registers eras, constants
```

```bash
python3 make_se201_01_four_eras.py                           # writes scripts/se201-01-four-eras.json
python3 narrate.py --script scripts/se201-01-four-eras.json  # xAI text-to-speech, Clark's voice, speed 1.05
SE_SERIES="SOFTWARE ENGINEERING 201" python3 render_se101.py --script scripts/se201-01-four-eras.json > ../../logs/s201_01_foureras.log
# finish_se201.sh <lesson-folder> <video-file> <name> <render-log> <scene-script> <site-checkout>
./finish_se201.sh 01-four-eras-of-building-systems SE201_01_Four-Eras-Of-Building-Systems_public.mp4 \
  se201-01-four-eras-of-building-systems ../../logs/s201_01_foureras.log scripts/se201-01-four-eras.json /path/to/site-checkout
python3 sitegen/stamp_versions.py                            # from the site checkout: new media version for watched state
SITE="$PWD" python3 sitegen/gen.py                           # pages, twins, llms.txt, lessons.json
```

`REBUILD.md` in the site root says how to run the generator without rewriting other sections' pages.

- Voice: xAI custom voice `4lbl0krw73vf`, speed 1.05. Speech tags used: `[pause]`, `<emphasis>`, `<slow>`. No laugh or chuckle tags.
- The xAI API key is read from the `XAI_API_KEY` environment variable at call time. It is never written to a file, a log, or a command line.
- Audio: loudness-normalized to about -16 LUFS integrated, AAC 160 kbps. Video: H.264, `+faststart`. Length 4:21 (260.8 s).
- Captions: `videos/se201-01-four-eras-of-building-systems.vtt`. The transcript is in the lesson's `index.md`, with the text-to-speech spellings made readable the same way `make_vtt.py` does for the captions.
- Authorship: the script was drafted by a scriptwriter on Clark's Mac, then revised and critiqued in two rounds by Claude Code (`review-round1.md`, `review-round2.md`, `claims-removed.md`), checked against `facts.md`, and reviewed by LegacyBot. The lens ("architecture bends around whatever is scarcest"), the era labels, the four constants and the opening quiz are the scriptwriter's teaching ideas, presented as a lens; they are not quotes from Clark.
- Review status: the narration was checked by speech-to-text against the script. Nobody has listened to the final audio yet before staging. It ships to production only when Clark merges.
