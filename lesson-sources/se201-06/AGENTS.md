# AGENTS.md — build source for Software Engineering 201, Lesson 6

This folder holds the source used to make the lesson video “Quality, Feedback, and Observability”. Read `BUILD.md` first.

- To change what the lesson says, edit `make_se201_06_quality.py`, regenerate the JSON, re-narrate only changed scenes, re-render, run `finish_se201.sh` with its arguments, then run `sitegen/stamp_versions.py` and `sitegen/gen.py` as `REBUILD.md` describes. Open a pull request into `next-revision`. Only Clark merges to `main`.
- `se201_layouts_58a.py` must sit beside `render_se101.py` on the build machine, with one import line in `render_se101.py`.
- Every factual claim must stay true; check `facts.md` and update it with any new claim. History stays approximate and hedged.
- The billing system, the renewals table, the three wrong renewals, the record of the double charge and the service level target are made up for the illustration. They describe no real company and no real incident. Keep it labelled as made up, aloud and on screen.
- “Define right, watch every run, feed it back” and “write the check once, run it twice” are teaching ideas written by the scriptwriter. They are not quotes from Clark.
- The script was drafted and critiqued in two independent rounds by Claude Code (model `claude-fable-5-2`) and reviewed by LegacyBot; the narration was checked by speech-to-text. Nobody has listened to the final audio yet before staging; do not describe it as listened to or approved.
- Never write the xAI API key to a file, log, or command line. No laugh or chuckle tags. No invented stories or quotes in Clark's voice, no company-internal details, no other people's names.
