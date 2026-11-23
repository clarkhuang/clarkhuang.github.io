# How Software Engineering 201, Lesson 8 was built

Lesson: **Routines, Pipelines, and Integration** — Software Engineering 201: From Loop to Enterprise Systems.
Page: https://clarkhuang.github.io/software-engineering-201/08-routines-pipelines-and-integration/

This folder is the source for the lesson video, so a person or an agent can read, check, change, and rebuild it.

| File | What it is |
|---|---|
| `make_se201_08_pipelines.py` | The script source: narration text and the on-screen visual spec for every scene. Edit this, not the JSON. |
| `se201-08-pipelines.json` | The generated scene script that the narrator and renderer read. |
| `se201_layouts_58b.py` | Renderer layouts added for lessons 7 and 8: `drift`, `skill_card`, and `pipeline`. This lesson uses `pipeline` (the nightly billing run, its hand-offs, records, retry and reconcile step). |
| `finish_se201.sh` | The finish step: loudness, faststart MP4, poster, captions, and the copy into a site checkout. Takes arguments, so one script serves every Software Engineering 201 lesson. |
| `make_vtt.py` | Writes the WebVTT captions from the scene script and the render timeline. |
| `render-timeline.log` | Scene start times and lengths from the render (used for chapters and captions). |
| `facts.md` | Every factual claim in the lesson, spoken or on screen, with its source. Teaching framings and made-up examples are marked as such. |
| `brief.md` | The brief (prompt) the lesson was written from. |
| `review-round1.md`, `review-round2.md` | The two rounds of critique on the draft script, and what changed after each. |
| `claims-removed.md` | Claims from the draft that were removed or toned down, and why. |

## Kept as written

`brief.md`, `facts.md`, the review files and `claims-removed.md` were written during the build and use the working file names: `se201-08-facts.md` is `facts.md` here, `se201-08-claims-toned-down.md` is `claims-removed.md`, and `se201-08-review-round1.md` and `-round2.md` are the two review files. The owner's brief for lessons 5 to 8 (`briefA.md`), the preview stills (`stills-08/`) and `changed-after-render.md` stayed on the build machine and are not in this repository. `brief.md` is the prompt as it was given, so where it differs from the recorded lesson, the scene script is what was recorded.

## Changed after round 2

The quiz answer in scene `02_quiz` first said “Charged twice.” Round 2 noted that some payment processors catch an immediate duplicate by default, so the line was softened to “Quite possibly, charged twice. Some processors catch a quick duplicate, but don't count on it.” Only that scene was re-narrated; the lesson was then re-rendered and finished again. The generator, the scene script, the render timeline, the captions and the video in this repository all carry the softened line. `review-round1.md` and `review-round2.md` are kept as written, so they quote the earlier wording.

## Rebuild

The renderer is the same one used for every Software Engineering 101 and 201 video (`render_se101.py` on top of the AI Tips `render.py`). It lives on the build machine, not in this repository. `se201_layouts_58b.py` must sit beside `render_se101.py`, which needs one import line to register the new layouts:

```python
import se201_layouts_58b  # registers the SE201 Lesson 7 and 8 layouts: drift, skill_card, pipeline
```

This lesson also uses `graph` from `se101_layouts6.py` (in `lesson-sources/se201-04/`), and `quiz`, which is already part of the renderer on the build machine.

```bash
python3 make_se201_08_pipelines.py        # writes scripts/se201-08-pipelines.json
python3 narrate.py --script scripts/se201-08-pipelines.json   # xAI text-to-speech, Clark's voice, speed 1.05
SE_SERIES="SOFTWARE ENGINEERING 201" python3 render_se101.py --script scripts/se201-08-pipelines.json > ../../logs/s201_08-pipelines.log
# finish_se201.sh <lesson-folder> <video-file> <name> <render-log> <scene-script> <site-checkout>
./finish_se201.sh 08-routines-pipelines-and-integration SE201_08_Routines-Pipelines-And-Integration_public.mp4 \
  se201-08-routines-pipelines-and-integration ../../logs/s201_08-pipelines.log scripts/se201-08-pipelines.json /path/to/site-checkout
python3 sitegen/stamp_versions.py                            # from the site checkout: new media version for watched state
SITE="$PWD" python3 sitegen/gen.py                           # pages, twins, llms.txt, lessons.json
```

`REBUILD.md` in the site root says how to run the generator without rewriting other sections' pages.

- Voice: xAI custom voice `4lbl0krw73vf`, speed 1.05. Speech tags used: `[pause]`, `<emphasis>`. No laugh or chuckle tags.
- The xAI API key is read from the `XAI_API_KEY` environment variable at call time. It is never written to a file, a log, or a command line.
- Audio: loudness-normalized to about -16 LUFS integrated, AAC 160 kbps. Video: H.264, `+faststart`. Length 4:15 (255.5 s).
- Captions: `videos/se201-08-routines-pipelines-and-integration.vtt`. The transcript is in the lesson's `index.md`, with the text-to-speech spellings made readable (for example “A.I.” as AI and “two oh one” as 201).
- The example: The billing system, the nightly run, the counts on screen (called made up aloud) and the partner's file are made up for the illustration. They describe no real company and no real incident.
- Authorship: the script was drafted and critiqued in two independent rounds by Claude Code (model `claude-fable-5-2`; `review-round1.md`, `review-round2.md`, `claims-removed.md`), checked against `facts.md`, and reviewed by LegacyBot. “A skill plus a trigger is a routine; routines chained make a pipeline” is this series' own vocabulary, introduced with “call” in the narration. The four things to write down are a teaching idea written by the scriptwriter. They are not quotes from Clark.
- Review status: the narration was checked by speech-to-text against the script. Nobody has listened to the final audio yet before staging. It ships to production only when Clark merges.
