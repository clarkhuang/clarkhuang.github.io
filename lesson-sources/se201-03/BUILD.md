# How Software Engineering 201, Lesson 3 was built

Lesson: **Parallel Agents, One Integration** — Software Engineering 201: From Loop to Enterprise Systems.
Page: https://clarkhuang.github.io/software-engineering-201/03-parallel-agents-one-integration/

This folder is the source for the lesson video, so a person or an agent can read, check, change, and rebuild it.

| File | What it is |
|---|---|
| `make_se201_03.py` | The script source: narration text and the on-screen visual spec for every scene. Edit this, not the JSON. |
| `se201-03-parallel.json` | The generated scene script that the narrator and renderer read. |
| `se101_layouts6.py` | Renderer layouts added for lessons 2 and 3: `graph`, `crossing`, and `lanes`. This lesson uses `lanes`. |
| `finish_se201.sh` | The finish step: loudness, faststart MP4, poster, captions, and the copy into a site checkout. Takes arguments, so one script serves every Software Engineering 201 lesson. |
| `make_vtt.py` | Writes the WebVTT captions from the scene script and the render timeline. |
| `render-timeline.log` | Scene start times and lengths from the render (used for chapters and captions). |
| `facts.md` | Every claim the lesson makes about this site, with where to check it in the repo. |
| `brief.md` | The brief (prompt) the lesson was written from. |
| `review-round1.md`, `review-round2.md` | The two rounds of critique on the draft script, and what changed after each. |

## Rebuild

The renderer is the same one used for every Software Engineering 101 and 201 video (`render_se101.py` on top of the AI Tips `render.py`). It lives on the build machine, not in this repository. `se101_layouts6.py` must sit beside `render_se101.py`, which needs one import line to register the new layouts:

```python
import se101_layouts6  # registers the SE201 Lesson 2 and 3 layouts: graph, crossing, lanes
```

```bash
python3 make_se201_03.py                                  # writes scripts/se201-03-parallel.json
python3 narrate.py --script scripts/se201-03-parallel.json   # xAI text-to-speech, Clark's voice, speed 1.05
SE_SERIES="SOFTWARE ENGINEERING 201" python3 render_se101.py --script scripts/se201-03-parallel.json > ../../logs/s201_03_parallel.log
# finish_se201.sh <lesson-folder> <video-file> <name> <render-log> <scene-script> <site-checkout>
./finish_se201.sh 03-parallel-agents-one-integration SE201_03_Parallel-Agents-One-Integration_public.mp4 \
  se201-03-parallel-agents-one-integration ../../logs/s201_03_parallel.log scripts/se201-03-parallel.json /path/to/site-checkout
SITE="$PWD" python3 sitegen/gen.py                        # from the site checkout: pages, twins, llms.txt, lessons.json
```

`REBUILD.md` in the site root says how to run the generator without rewriting other sections' pages.

- Voice: xAI custom voice `4lbl0krw73vf`, speed 1.05. Speech tags used: `[pause]`, `<emphasis>`. No laugh or chuckle tags.
- The xAI API key is read from the `XAI_API_KEY` environment variable at call time. It is never written to a file, a log, or a command line.
- Audio: loudness-normalized to about -16 LUFS integrated, AAC 160 kbps. Video: H.264, `+faststart`.
- Captions: `videos/se201-03-parallel-agents-one-integration.vtt`. The transcript is in the lesson's `index.md`, with the text-to-speech spellings made readable the same way `make_vtt.py` does for the captions.
- Review: the script was drafted and critiqued in two rounds by Claude Code (`review-round1.md`, `review-round2.md`), checked against `facts.md`, and reviewed by LegacyBot. Nobody has listened to the final audio yet before staging. It ships to production only when Clark merges.
