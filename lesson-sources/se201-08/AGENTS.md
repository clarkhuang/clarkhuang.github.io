# AGENTS.md — build source for Software Engineering 201, Lesson 8

This folder holds the source used to make the lesson video “Routines, Pipelines, and Integration”. Read `BUILD.md` first.

- To change what the lesson says, edit `make_se201_08_pipelines.py`, regenerate the JSON, re-narrate only changed scenes, re-render, run `finish_se201.sh` with its arguments, then run `sitegen/stamp_versions.py` and `sitegen/gen.py` as `REBUILD.md` describes. Open a pull request into `next-revision`. Only Clark merges to `main`.
- `se201_layouts_58b.py` must sit beside `render_se101.py` on the build machine, with one import line in `render_se101.py`.
- Every factual claim must stay true; check `facts.md` and update it with any new claim. History stays approximate and hedged.
- The billing system, the nightly run, the counts on screen (called made up aloud) and the partner's file are made up for the illustration. They describe no real company and no real incident. Keep it labelled as made up, aloud and on screen.
- “A skill plus a trigger is a routine; routines chained make a pipeline” is this series' own vocabulary, introduced with “call” in the narration. The four things to write down are a teaching idea written by the scriptwriter. They are not quotes from Clark.
- The script was drafted and critiqued in two independent rounds by Claude Code (model `claude-fable-5-2`) and reviewed by LegacyBot; the narration was checked by speech-to-text. Nobody has listened to the final audio yet before staging; do not describe it as listened to or approved.
- Never write the xAI API key to a file, log, or command line. No laugh or chuckle tags. No invented stories or quotes in Clark's voice, no company-internal details, no other people's names.
- The quiz answer in `02_quiz` was softened after round 2 (“Quite possibly, charged twice. Some processors catch a quick duplicate, but don't count on it.”). The two review files quote the earlier wording and are kept as written.
