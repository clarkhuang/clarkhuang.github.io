# AGENTS.md — build source for Software Engineering 201, Lesson 1

This folder holds the source used to make the lesson video “Four Eras of Building Systems”. Read `BUILD.md` first.

- To change what the lesson says, edit `make_se201_01_four_eras.py`, regenerate the JSON, re-narrate only changed scenes, re-render, run `finish_se201.sh` with its arguments, then run `sitegen/stamp_versions.py` and `sitegen/gen.py` as `REBUILD.md` describes. Open a pull request into `next-revision`. Only Clark merges to `main`.
- `se201_layouts_eras.py` and `se101_layouts6.py` must sit beside `render_se101.py` on the build machine, with one import line each in `render_se101.py`.
- Every factual claim must stay true; check `facts.md` and update it with any new claim. History stays approximate and sourced. Clark's career facts are only the public record listed in `facts.md`.
- The lens, the era labels, the four constants and the quiz were written by a scriptwriter as a teaching lens. Do not present them as Clark's quotes or settled fact. The agent-era design list is where thinking is heading, not a settled answer. The subscription-billing picture is a made-up example, not any company's real design.
- The script was revised and critiqued in two rounds by Claude Code and reviewed by LegacyBot; the narration was checked by speech-to-text. Nobody has listened to the final audio yet before staging; do not describe it as listened to or approved.
- Never write the xAI API key to a file, log, or command line. No laugh or chuckle tags. No invented stories or quotes in Clark's voice, no company-internal details, no other people's names.
