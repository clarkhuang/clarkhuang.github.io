# AGENTS.md — build source for Software Engineering 201, Lesson 3

This folder holds the source used to make the lesson video “Decompose the System into a Graph”. Read `BUILD.md` first.

- To change what the lesson says, edit `make_se201_03_decompose.py`, regenerate the JSON, re-narrate only changed scenes, re-render, run `finish_se201.sh` with its arguments, then run `sitegen/stamp_versions.py` and `sitegen/gen.py` as `REBUILD.md` describes. Open a pull request into `next-revision`. Only Clark merges to `main`.
- `se101_layouts6.py` must sit beside `render_se101.py` on the build machine, with one import line in `render_se101.py`.
- Every claim about this site must stay true; check `facts.md` and update it with any new claim.
- The script went through two rounds of critique by Claude Code and a review by LegacyBot. Nobody has listened to the final audio yet before staging; do not describe it as listened to or approved.
- Never write the xAI API key to a file, log, or command line. No laugh or chuckle tags. No invented stories or quotes in Clark's voice, no company-internal details, no other people's names.
- This lesson was renumbered from 2 to 3 and re-rendered; only the title, rule and closing clips were re-narrated. `brief.md`, `facts.md` and the review files keep the old numbers as a historical record.
