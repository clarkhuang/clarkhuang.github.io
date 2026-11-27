# AGENTS.md — build source for Software Engineering 301, Lesson 1

This folder holds the source for “Size the model, then run the first endpoint”. Read `BUILD.md` first.

- To change what the lesson says, edit `make_se301_01.py`, run it to regenerate the JSON, update `facts.md` for any new claim, and run `python3 publish_page.py` so the public page, its `index.md`, and its `AGENTS.md` stay in step. Open a pull request into `next-revision`. Only Clark merges to `main`.
- The copy-paste prompt’s canonical text is `install-prompt.md`. The public page embeds that file. Do not let the two copies drift. `publish_page.py` is what writes the page copies.
- Clark approved the script and `facts.md`, and Lesson 1 has been narrated and rendered. To rebuild the video, run `render_se301_01.py` with `XAI_API_KEY` already in the environment (never on the command line), then copy the MP4, captions, and poster into `/videos/` and `/videos/posters/` and run `publish_page.py`. The renderer refuses to write a silent or dummy video when `XAI_API_KEY` is unset.
- Never write the xAI API key to a file, a log, or a command line. No laugh or chuckle tags.
- Every factual claim must stay true. Check `facts.md`. Writer-added lines are listed there for a yes or no. Do not add a measured speed, a price, or a biography.
- The 40 GB, 160 GB, and 240 GB figures are weight floors from the playbook, not measured files. Studio model names stay candidates.
- The Windows and Linux path is part of the prompt. The playbook’s named machines are Apple silicon. Keep that distinction.
- No invented stories or quotes in Clark’s voice, no company-internal details, no other people’s names.
