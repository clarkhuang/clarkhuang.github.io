# How Software Engineering 201, Lesson 3 was built

Lesson: **Decompose the System into a Graph** — Software Engineering 201: From Loop to Enterprise Systems.
Page: https://clarkhuang.github.io/software-engineering-201/03-decompose-the-system-into-a-graph/

This folder is the source for the lesson video, so a person or an agent can read, check, change, and rebuild it.

| File | What it is |
|---|---|
| `make_se201_03_decompose.py` | The script source: narration text and the on-screen visual spec for every scene. Edit this, not the JSON. |
| `se201-03-decompose.json` | The generated scene script that the narrator and renderer read. |
| `se101_layouts6.py` | Renderer layouts added for lessons 3 and 4 (then numbered 2 and 3): `graph`, `crossing`, and `lanes`. This lesson uses `graph` and `crossing`. |
| `finish_se201.sh` | The finish step: loudness, faststart MP4, poster, captions, and the copy into a site checkout. Takes arguments, so one script serves every Software Engineering 201 lesson. |
| `make_vtt.py` | Writes the WebVTT captions from the scene script and the render timeline. |
| `render-timeline.log` | Scene start times and lengths from the render (used for chapters and captions). |
| `facts.md` | Every claim the lesson makes about this site, with where to check it in the repo. |
| `brief.md` | The brief (prompt) the lesson was written from. |
| `review-round1.md`, `review-round2.md` | The two rounds of critique on the draft script, and what changed after each. |

## Renumbered

This lesson was lesson 2 until “Four Eras of Building Systems” became Software Engineering 201, Lesson 1 (November 2026). It was re-rendered for the new numbering, and only the title, rule and closing clips (`01_title`, `10_rule` and `12_close`) were re-narrated, to say the new lesson numbers. The rest of the narration and every other scene are unchanged. The new video is `videos/se201-03-decompose-the-system-into-a-graph.mp4`; the old page `/software-engineering-201/02-decompose-the-system-into-a-graph/` redirects to `/software-engineering-201/03-decompose-the-system-into-a-graph/`. `brief.md`, `facts.md` and the review files were written when this was lesson 2, so they use the old lesson numbers, folder names (`lesson-sources/se201-02/` and so on) and script names; they are kept as written. The old generator and scene script are in the git history.

## Rebuild

The renderer is the same one used for every Software Engineering 101 and 201 video (`render_se101.py` on top of the AI Tips `render.py`). It lives on the build machine, not in this repository. `se101_layouts6.py` must sit beside `render_se101.py`, which needs one import line to register the new layouts:

```python
import se101_layouts6  # registers the SE201 Lesson 3 and 4 layouts: graph, crossing, lanes
```

```bash
python3 make_se201_03_decompose.py                                  # writes scripts/se201-03-decompose.json
python3 narrate.py --script scripts/se201-03-decompose.json   # xAI text-to-speech, Clark's voice, speed 1.05
SE_SERIES="SOFTWARE ENGINEERING 201" python3 render_se101.py --script scripts/se201-03-decompose.json > ../../logs/s201_03_decompose.log
# finish_se201.sh <lesson-folder> <video-file> <name> <render-log> <scene-script> <site-checkout>
./finish_se201.sh 03-decompose-the-system-into-a-graph SE201_03_Decompose-The-System-Into-A-Graph_public.mp4 \
  se201-03-decompose-the-system-into-a-graph ../../logs/s201_03_decompose.log scripts/se201-03-decompose.json /path/to/site-checkout
SITE="$PWD" python3 sitegen/gen.py                        # from the site checkout: pages, twins, llms.txt, lessons.json
```

`REBUILD.md` in the site root says how to run the generator without rewriting other sections' pages.

- Voice: xAI custom voice `4lbl0krw73vf`, speed 1.05. Speech tags used: `[pause]`, `<emphasis>`, `<slow>`. No laugh or chuckle tags.
- The xAI API key is read from the `XAI_API_KEY` environment variable at call time. It is never written to a file, a log, or a command line.
- Audio: loudness-normalized to about -16 LUFS integrated, AAC 160 kbps. Video: H.264, `+faststart`.
- Captions: `videos/se201-03-decompose-the-system-into-a-graph.vtt`. The transcript is in the lesson's `index.md`, with the text-to-speech spellings made readable the same way `make_vtt.py` does for the captions.
- Review: the script was drafted and critiqued in two rounds by Claude Code (`review-round1.md`, `review-round2.md`), checked against `facts.md`, and reviewed by LegacyBot. Nobody has listened to the final audio yet before staging. It ships to production only when Clark merges.
