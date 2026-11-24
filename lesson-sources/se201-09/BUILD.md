# How Software Engineering 201, Lesson 9 was built

Lesson: **Agents That Operate Enterprise Systems** — Software Engineering 201: From Loop to Enterprise Systems.
Page: https://clarkhuang.github.io/software-engineering-201/09-agents-that-operate-enterprise-systems/

This folder is the source for the lesson video, so a person or an agent can read, check, change, and rebuild it.

| File | What it is |
|---|---|
| `make_se201_09_operate.py` | The script source: narration text and the on-screen visual spec for every scene. Edit this, not the JSON. |
| `se201-09-operate.json` | The generated scene script that the narrator and renderer read. |
| `se201_layouts_09.py` | Renderer layouts added for this lesson: `accessmap` (one agent, what it can reach, and the line where access is enforced), `trail` (one night's work and the log it leaves) and `access_review` (one row per permission: needed? used?). |
| `finish_se201.sh` | The finish step: loudness, faststart MP4, poster, captions, and the copy into a site checkout. Takes arguments, so one script serves every Software Engineering 201 lesson. |
| `make_vtt.py` | Writes the WebVTT captions from the scene script and the render timeline. |
| `render-timeline.log` | Scene start times and lengths from the render (used for chapters and captions). |
| `facts.md` | Every factual claim in the lesson, spoken or on screen, with its source. Teaching framings and made-up examples are marked as such. |
| `brief.md` | The brief (prompt) the lesson was written from. |
| `review-round1.md`, `review-round2.md` | The two rounds of critique on the draft script, and what changed after each. |
| `claims-removed.md` | Claims from the draft that were removed or toned down, and why. |

## Kept as written

`brief.md`, `facts.md`, the review files and `claims-removed.md` were written during the build and use the working file names: `se201-09-facts.md` is `facts.md` here, `se201-09-claims-toned-down.md` is `claims-removed.md`, and `se201-09-review-round1.md` and `-round2.md` are the two review files. `se201-09-page.md`, which they mention, is the working draft of the lesson page; its summary, rule and notes are on the lesson page and in its `index.md` (“What the video simplifies”). The reviewers' briefs and the shared brief (`briefA.md`, `briefC.md`, `brief-common.md`), the hand-off check against the other recorded lessons (`handoffs.md`), the preview stills and the round-1 copies of the generator and scene script (`make_se201_09_operate.round1.py`, `se201-09-operate.round1.json`) stayed on the build machine and are not in this repository. `brief.md` and `facts.md` give the length as an estimate (705 spoken words, about 4:31) made before narration; the measured length is below. Three small edits were made to these public copies: the owner's request in `brief.md` is paraphrased, a private company name is left out of `brief.md` and `facts.md`, and one citation gives the idea without its authors' names. Where any of these files differs from the recorded lesson, the scene script is what was recorded.

## Rebuild

The renderer is the same one used for every Software Engineering 101 and 201 video (`render_se101.py` on top of the AI Tips `render.py`). It lives on the build machine, not in this repository. `se201_layouts_09.py` must sit beside `render_se101.py`, which needs one import line to register the new layouts:

```python
import se201_layouts_09  # registers the SE201 Lesson 9 layouts: accessmap, trail, access_review
```

`se201_layouts_09.py` imports its drawing helpers from `se201_layouts_58b.py` (in `lesson-sources/se201-08/`), so that file must sit beside it too. This lesson also uses `title`, `quiz`, `graph`, `rule`, `rule_card`, `statement` and `outro`, which are already part of the renderer on the build machine.

```bash
python3 make_se201_09_operate.py          # writes scripts/se201-09-operate.json
python3 narrate.py --script scripts/se201-09-operate.json     # xAI text-to-speech, Clark's voice, speed 1.05
SE_SERIES="SOFTWARE ENGINEERING 201" python3 render_se101.py --script scripts/se201-09-operate.json > ../../logs/s201_09_operate.log
# finish_se201.sh <lesson-folder> <video-file> <name> <render-log> <scene-script> <site-checkout>
./finish_se201.sh 09-agents-that-operate-enterprise-systems SE201_09_Agents-That-Operate-Enterprise-Systems_public.mp4 \
  se201-09-agents-that-operate-enterprise-systems ../../logs/s201_09_operate.log scripts/se201-09-operate.json /path/to/site-checkout
python3 sitegen/stamp_versions.py                            # from the site checkout: new media version for watched state
SITE="$PWD" python3 sitegen/gen.py                           # pages, twins, llms.txt, lessons.json
```

`REBUILD.md` in the site root says how to run the generator without rewriting other sections' pages.

- Voice: xAI custom voice `4lbl0krw73vf`, speed 1.05. Speech tags used: `[pause]`, `<emphasis>`. No laugh or chuckle tags.
- The xAI API key is read from the `XAI_API_KEY` environment variable at call time. It is never written to a file, a log, or a command line.
- Audio: `finish_se201.sh` normalizes loudness to about -16 LUFS integrated, AAC 160 kbps. Video: H.264, `+faststart`. Length 4:19 (259.7 s).
- Captions: `videos/se201-09-agents-that-operate-enterprise-systems.vtt`. `make_vtt.py` wrote them, with “A.I.” made readable as AI and “two oh one” as 201; no cue text or timing was changed by hand. The transcript is in the lesson's `index.md` and matches the captions word for word. “A.M.” is kept as spoken, as in lessons 6 and 8.
- The example: the billing system, the agent and its name, the 3 a.m. refund, the night's numbers and times, and the near miss are made up for the illustration, and called made up aloud and on screen. They describe no real company and no real incident. Nothing went wrong in the near miss. The lesson page says what else the video simplifies.
- Lessons 8 and 10 were recorded first. This lesson answers the three questions lesson 8 closes on and uses the same operator as the capstone (`billing-ops-agent`, the same access), on a different night, so nothing in the other lessons needed re-recording.
- Authorship: the script was drafted and critiqued in two independent rounds by Claude Code (model `claude-fable-5-2`; `review-round1.md`, `review-round2.md`, `claims-removed.md`), checked against `facts.md`, and reviewed by LegacyBot. The worked example, the three diagrams, rule 9 and its wording are teaching ideas written by the scriptwriter. They are not quotes from Clark.
- Review status: the narration was checked by speech-to-text against the script. Nobody has listened to the final audio yet before staging. It ships to production only when Clark merges.
