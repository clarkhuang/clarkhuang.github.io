# AGENTS.md — build source for AI Tips, lesson 17

This folder holds the source used to make the lesson video “Don't Paste Secrets”. Read `BUILD.md` first.

- To change what the lesson says, edit `ai-tip-17.json`, re-narrate only changed scenes, re-render, rebuild captions with `make_vtt.py`, then run `sitegen/stamp_versions.py` and `sitegen/gen.py` as `REBUILD.md` describes. Open a pull request into `next-revision`. Only Clark merges to `main`.
- Every factual claim must stay true; check `facts.md` and update it with any new claim.
- The failing-deploy paste and the `DATABASE_URL` line are a made-up illustration. They describe no real company and no real incident. Keep it labelled as generic, aloud and on screen.
- The script was reviewed by Claude Code (model `claude-fable-5-2`) before narration.
- Never write the xAI API key to a file, log, or command line. No laugh or chuckle tags. No invented stories or quotes in Clark's voice, no company-internal details, no other people's names.
