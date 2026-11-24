# AGENTS.md — build source for Software Engineering 201, Lesson 9

This folder holds the source used to make the lesson video “Agents That Operate Enterprise Systems”. Read `BUILD.md` first.

- To change what the lesson says, edit `make_se201_09_operate.py`, regenerate the JSON, re-narrate only changed scenes, re-render, run `finish_se201.sh` with its arguments, then run `sitegen/stamp_versions.py` and `sitegen/gen.py` as `REBUILD.md` describes. Open a pull request into `next-revision`. Only Clark merges to `main`.
- `se201_layouts_09.py` must sit beside `render_se101.py` on the build machine, with one import line in `render_se101.py`. It imports helpers from `se201_layouts_58b.py` (in `lesson-sources/se201-08/`).
- Every factual claim must stay true; check `facts.md` and update it with any new claim.
- The billing system, the agent and its name, the 3 a.m. refund, the night's numbers and times, and the near miss are made up for the illustration. They describe no real company and no real incident. Keep them labelled as made up, aloud and on screen.
- Lessons 8 and 10 are recorded and hand off to this one: lesson 8 closes on the three questions this lesson answers, and the capstone shows the same operator (`billing-ops-agent`, the same access). Keep them consistent if any of the three changes.
- The worked example, the diagrams and rule 9 are teaching ideas written by the scriptwriter. They are not quotes from Clark.
- The script was drafted and critiqued in two independent rounds by Claude Code (model `claude-fable-5-2`) and reviewed by LegacyBot; the narration was checked by speech-to-text. Nobody has listened to the final audio yet before staging; do not describe it as listened to or approved.
- Never write the xAI API key to a file, log, or command line. No laugh or chuckle tags. No invented stories or quotes in Clark's voice, no company-internal details, no other people's names.
