# How Software Engineering 201, Lesson 10 was built

Lesson: **Capstone: One Feature, End to End** — Software Engineering 201: From Loop to Enterprise Systems.
Page: https://clarkhuang.github.io/software-engineering-201/10-capstone-one-feature-end-to-end/

This folder is the source for the lesson video, so a person or an agent can read, check, change, and rebuild it.

| File | What it is |
|---|---|
| `make_se201_10_capstone.py` | The script source: narration text and the on-screen visual spec for every scene. Edit this, not the JSON. |
| `se201-10-capstone.json` | The generated scene script that the narrator and renderer read. |
| `se201_layouts_10.py` | Renderer layout added for this lesson: `buildmap` (one map of the feature, held on screen across the lesson; each element carries the number of the lesson it comes from and lights up when that lesson is applied). |
| `finish_se201.sh` | The finish step: loudness, faststart MP4, poster, captions, and the copy into a site checkout. Takes arguments, so one script serves every Software Engineering 201 lesson. |
| `make_vtt.py` | Writes the WebVTT captions from the scene script and the render timeline. |
| `render-timeline.log` | Scene start times and lengths from the render (used for chapters and captions). |
| `facts.md` | Every factual claim in the lesson, spoken or on screen, with its source. Teaching framings and made-up examples are marked as such. |
| `brief.md` | The brief (prompt) the lesson was written from. |
| `review-round1.md`, `review-round2.md` | The two rounds of critique on the draft script, and what changed after each. |
| `claims-removed.md` | Claims from the draft that were removed or toned down, and why. |

## Kept as written

`brief.md`, `facts.md`, the review files and `claims-removed.md` were written during the build and use the working file names: `se201-10-facts.md` is `facts.md` here, `se201-10-claims-toned-down.md` is `claims-removed.md`, and `se201-10-review-round1.md` and `-round2.md` are the two review files. `se201-10-page.md`, which they mention, is the working draft of the lesson page; its summary, rule and notes are on the lesson page and in its `index.md` (“What the video simplifies”). The owner's brief and the reviewers' briefs (`briefA.md`, `brief-common.md`), the working notes for the series page and the lesson 9 outline (`series-update.md`, `lesson9-outline.md`), the preview stills and the round-1 copy of the generator stayed on the build machine and are not in this repository. `brief.md` and `facts.md` give the length as an estimate (852 spoken words, about 5:28) made before narration; the measured length is below. Where any of these files differs from the recorded lesson, the scene script is what was recorded.

## Rebuild

The renderer is the same one used for every Software Engineering 101 and 201 video (`render_se101.py` on top of the AI Tips `render.py`). It lives on the build machine, not in this repository. `se201_layouts_10.py` must sit beside `render_se101.py`, which needs one import line to register the new layout:

```python
import se201_layouts_10  # registers the SE201 Lesson 10 layout: buildmap
```

`se201_layouts_10.py` imports its drawing helpers from `se201_layouts_58b.py` (in `lesson-sources/se201-08/`), so that file must sit beside it too. This lesson also uses `title`, `quiz`, `rule_card`, `statement` and `outro`, which are already part of the renderer on the build machine.

```bash
python3 make_se201_10_capstone.py         # writes scripts/se201-10-capstone.json
python3 narrate.py --script scripts/se201-10-capstone.json    # xAI text-to-speech, Clark's voice, speed 1.05
SE_SERIES="SOFTWARE ENGINEERING 201" python3 render_se101.py --script scripts/se201-10-capstone.json > ../../logs/s201_10_capstone.log
# finish_se201.sh <lesson-folder> <video-file> <name> <render-log> <scene-script> <site-checkout>
./finish_se201.sh 10-capstone-one-feature-end-to-end SE201_10_Capstone-One-Feature-End-To-End_public.mp4 \
  se201-10-capstone-one-feature-end-to-end ../../logs/s201_10_capstone.log scripts/se201-10-capstone.json /path/to/site-checkout
python3 sitegen/stamp_versions.py                            # from the site checkout: new media version for watched state
SITE="$PWD" python3 sitegen/gen.py                           # pages, twins, llms.txt, lessons.json
```

`REBUILD.md` in the site root says how to run the generator without rewriting other sections' pages.

- Voice: xAI custom voice `4lbl0krw73vf`, speed 1.05. Speech tags used: `[pause]`, `<emphasis>`. No laugh or chuckle tags.
- The xAI API key is read from the `XAI_API_KEY` environment variable at call time. It is never written to a file, a log, or a command line.
- Audio: loudness-normalized to about -16 LUFS integrated, AAC 160 kbps. Video: H.264, `+faststart`. Length 5:09 (309.2 s).
- Captions: `videos/se201-10-capstone-one-feature-end-to-end.vtt`. `make_vtt.py` wrote them; “I.D.” was then made readable as ID by hand, with the timing unchanged. The transcript is in the lesson's `index.md`, with the text-to-speech spellings made readable the same way (for example “A.I.” as AI, “I.D.” as ID and “two oh one” as 201).
- The example: the billing system, the plans and prices, the quote, the file names, the agent's name and the double charge are made up for the illustration, and called made up aloud and on screen. They describe no real company and no real incident. The numbers leave tax out; the lesson page says what else the video simplifies.
- Lesson 9 was recorded after this lesson (source in `lesson-sources/se201-09/`). When the capstone was written it had no video, so the capstone refers to its ideas as “lesson nine's question”, never as something the viewer has watched; the brief, facts and review files here were written then and are kept as written.
- Authorship: the script was drafted and critiqued in two independent rounds by Claude Code (model `claude-fable-5-2`; `review-round1.md`, `review-round2.md`, `claims-removed.md`), checked against `facts.md`, and reviewed by LegacyBot. The feature, the build map, the plan-first rule and its wording are teaching ideas written by the scriptwriter. They are not quotes from Clark.
- Review status: the narration was checked by speech-to-text against the script. Nobody has listened to the final audio yet before staging. It ships to production only when Clark merges.
