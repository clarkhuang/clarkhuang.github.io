# AGENTS.md — build source for Software Engineering 301, Lesson 1

This folder holds the source for “Size the model, then run the first endpoint”. Read `BUILD.md` first.

- To change what the lesson says, edit `make_se301_01.py`, run it to regenerate the JSON, update `facts.md` for any new claim, and run `python3 publish_page.py` so the public page, its `index.md`, and its `AGENTS.md` stay in step. Open a pull request into `next-revision`. Only Clark merges to `main`.
- The copy-paste prompt’s canonical text is `install-prompt.md`. The public page embeds that file. Do not let the two copies drift. `publish_page.py` is what writes the page copies.
- Do not narrate, and do not commit an MP4, until Clark approves the script and `facts.md`. `render_se301_01.py` refuses to write a silent or dummy video when `XAI_API_KEY` is unset.
- Never write the xAI API key to a file, a log, or a command line. No laugh or chuckle tags.
- Every factual claim must stay true. Check `facts.md`. Writer-added lines are listed there for a yes or no. Do not add a measured speed, a price, or a biography.
- The 40 GB, 160 GB, and 240 GB figures are weight floors from the playbook, not measured files. Studio model names stay candidates.
- The Windows and Linux path is part of the prompt. The playbook’s named machines are Apple silicon. Keep that distinction.
- No invented stories or quotes in Clark’s voice, no company-internal details, no other people’s names.
