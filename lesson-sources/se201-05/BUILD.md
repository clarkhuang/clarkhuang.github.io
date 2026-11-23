# How Software Engineering 201, Lesson 5 was built

Lesson: **Governance: Where People Decide** — Software Engineering 201: From Loop to Enterprise Systems.
Page: https://clarkhuang.github.io/software-engineering-201/05-governance-where-people-decide/

This folder is the source for the lesson video, so a person or an agent can read, check, change, and rebuild it.

| File | What it is |
|---|---|
| `make_se201_05_governance.py` | The script source: narration text and the on-screen visual spec for every scene. Edit this, not the JSON. |
| `se201-05-governance.json` | The generated scene script that the narrator and renderer read. |
| `se201_layouts_58a.py` | Renderer layouts added for lessons 5 and 6: `gates`, `decision_card`, and `renewals`. This lesson uses `gates` (the four questions, and the six pieces of work) and `decision_card` (the decision an agent prepares). |
| `finish_se201.sh` | The finish step: loudness, faststart MP4, poster, captions, and the copy into a site checkout. Takes arguments, so one script serves every Software Engineering 201 lesson. |
| `make_vtt.py` | Writes the WebVTT captions from the scene script and the render timeline. |
| `render-timeline.log` | Scene start times and lengths from the render (used for chapters and captions). |
| `facts.md` | Every factual claim in the lesson, spoken or on screen, with its source. Teaching framings and made-up examples are marked as such. |
| `brief.md` | The brief (prompt) the lesson was written from. |
| `review-round1.md`, `review-round2.md` | The two rounds of critique on the draft script, and what changed after each. |
| `claims-removed.md` | Claims from the draft that were removed or toned down, and why. |

## Kept as written

`brief.md`, `facts.md`, the review files and `claims-removed.md` were written during the build and use the working file names: `se201-05-facts.md` is `facts.md` here, `se201-05-claims-toned-down.md` is `claims-removed.md`, and `se201-05-review-round1.md` and `-round2.md` are the two review files. The owner's brief for lessons 5 to 8 (`briefA.md`), the preview stills (`stills-05/`) and `changed-after-render.md` stayed on the build machine and are not in this repository. `brief.md` is the prompt as it was given, so where it differs from the recorded lesson, the scene script is what was recorded. The brief asked for five pieces of work; after round 1 the recorded lesson has six pieces and four stops.

## Rebuild

The renderer is the same one used for every Software Engineering 101 and 201 video (`render_se101.py` on top of the AI Tips `render.py`). It lives on the build machine, not in this repository. `se201_layouts_58a.py` must sit beside `render_se101.py`, which needs one import line to register the new layouts:

```python
import se201_layouts_58a  # registers the SE201 Lesson 5 and 6 layouts: gates, decision_card, renewals
```

This lesson also uses `eras` from `se201_layouts_eras.py` (in `lesson-sources/se201-01/`), and `quiz`, `dial` and `perm_table`, which are already part of the renderer on the build machine.

```bash
python3 make_se201_05_governance.py       # writes scripts/se201-05-governance.json
python3 narrate.py --script scripts/se201-05-governance.json   # xAI text-to-speech, Clark's voice, speed 1.05
SE_SERIES="SOFTWARE ENGINEERING 201" python3 render_se101.py --script scripts/se201-05-governance.json > ../../logs/s201_05-governance.log
# finish_se201.sh <lesson-folder> <video-file> <name> <render-log> <scene-script> <site-checkout>
./finish_se201.sh 05-governance-where-people-decide SE201_05_Governance-Where-People-Decide_public.mp4 \
  se201-05-governance-where-people-decide ../../logs/s201_05-governance.log scripts/se201-05-governance.json /path/to/site-checkout
python3 sitegen/stamp_versions.py                            # from the site checkout: new media version for watched state
SITE="$PWD" python3 sitegen/gen.py                           # pages, twins, llms.txt, lessons.json
```

`REBUILD.md` in the site root says how to run the generator without rewriting other sections' pages.

- Voice: xAI custom voice `4lbl0krw73vf`, speed 1.05. Speech tags used: `[pause]`, `<emphasis>`. No laugh or chuckle tags.
- The xAI API key is read from the `XAI_API_KEY` environment variable at call time. It is never written to a file, a log, or a command line.
- Audio: loudness-normalized to about -16 LUFS integrated, AAC 160 kbps. Video: H.264, `+faststart`. Length 4:13 (253.0 s).
- Captions: `videos/se201-05-governance-where-people-decide.vtt`. The transcript is in the lesson's `index.md`, with the text-to-speech spellings made readable (for example “A.I.” as AI and “two oh one” as 201).
- The example: The billing system, the roles (finance owner, ledger owner, data owner, support lead), the late fee, the refund limit and every row on screen are made up for the illustration. They describe no real company.
- Authorship: the script was drafted and critiqued in two independent rounds by Claude Code (model `claude-fable-5-2`; `review-round1.md`, `review-round2.md`, `claims-removed.md`), checked against `facts.md`, and reviewed by LegacyBot. The four questions, the prepared decision, and “start strict, release one kind at a time” are teaching ideas written by the scriptwriter, presented as a rule of thumb. They are not quotes from Clark.
- Review status: the narration was checked by speech-to-text against the script. Nobody has listened to the final audio yet before staging. It ships to production only when Clark merges.
