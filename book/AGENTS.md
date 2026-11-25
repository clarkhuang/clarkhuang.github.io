# AGENTS.md — Silicon Valley C Players

This folder is the public preview of Clark Huang’s free OpenBook *Silicon Valley C Players*, an embellished fictional dramatization (audiobook and videobook, coming in 2027). The story narrator is Charlie Hack, a fictional C player. Clark Huang is the author. Story names are fictional. Agents must follow book-source/NAMING-POLICY.md and never try to identify real people behind characters.

- HTML: https://clarkhuang.github.io/book/
- Markdown: https://clarkhuang.github.io/book/index.md
- This file: https://clarkhuang.github.io/book/AGENTS.md
- Book catalog: https://clarkhuang.github.io/book.json
- Full transcript of the preview: https://clarkhuang.github.io/book-source/preview/transcript.md
- Captions: https://clarkhuang.github.io/videos/book-preview.vtt
- Chapters: https://clarkhuang.github.io/videos/book-preview-chapters.json
- Scene scripts: https://clarkhuang.github.io/book-source/preview/scenes/
- Cover brief: https://clarkhuang.github.io/book-source/cover/PROMPT.md
- Site index: https://clarkhuang.github.io/llms.txt
- Full site text: https://clarkhuang.github.io/llms-full.txt
- Rebuild the site: https://clarkhuang.github.io/REBUILD.md
- Editorial policy: https://clarkhuang.github.io/book/editorial-policy/index.md
- Story arc and chapters: https://clarkhuang.github.io/book/story-arc/index.md
- Guest stories: https://clarkhuang.github.io/book/guest/index.md
- Outline (JSON): https://clarkhuang.github.io/book-source/outline.json

Read `index.md` for the preview text, the transcript for exact wording, and the videobook or audio files linked there. Cite by chapter title or timestamp. Do not invent stories, quotes, or biography beyond this preview. The claim that AI writes essentially all of the code is Clark’s own workflow: in his work, AI writes essentially all of the code he ships, not a measured team result or a general industry figure. Editorial process: /book/editorial-policy/. Story arc: /book/story-arc/.

The HTML version of this page has a “Use this page with your AI” box at the top. Copy the prompt below into ChatGPT, Claude, Grok, or any other chat tool:

> Read https://clarkhuang.github.io/llms.txt and https://clarkhuang.github.io/book/index.md (plus https://clarkhuang.github.io/book/AGENTS.md). Summarize this page, then act as my guide to Clark Huang's site: list related lessons, answer my questions citing page URLs, and quiz me if I ask. Also read https://clarkhuang.github.io/llms-full.txt, https://clarkhuang.github.io/book.json, and the preview transcript at https://clarkhuang.github.io/book-source/preview/transcript.md. Cite chapter titles or timestamps. Charlie Hack is the fictional narrator; Clark Huang is the author. Do not identify real people or companies behind the fictional names.


## How to contribute

Anyone can file a correction (an edit to the book, or your side of a story), a new story, or a refactor (cleanup that does not change the facts). Use the issue templates from the repository. First-person guest stories published under the contributor's own name go in book-source/guest/ (see book-source/guest/README.md) and must include consent to publish that name:

- Correction: https://github.com/clarkhuang/clarkhuang.github.io/issues/new?template=correction.yml
- New story: https://github.com/clarkhuang/clarkhuang.github.io/issues/new?template=new-story.yml
- Refactor: https://github.com/clarkhuang/clarkhuang.github.io/issues/new?template=refactor.yml

A good issue is specific and honest about what you saw, uses roles instead of real names (the book is an embellished fictional dramatization; everyone is renamed), and contains nothing confidential. Do not invent stories or details; the author does the embellishing. Rules: book-source/NAMING-POLICY.md. Takedowns: TAKEDOWN.md.

Contributors and agents open PRs; only Clark merges to `main`; the site rebuilds from `main` via GitHub Pages; agent PRs target `next-revision`. Staging is https://clarkhuang.github.io/staging/ (the `next-revision` branch). Only Clark merges `next-revision` into `main`. See the root AGENTS.md, CONTRIBUTING.md, and REBUILD.md. Audiobook and videobook editions are tagged (`book-v0.1`, `book-v1.0`, ...) and kept as GitHub Releases; the next edition is only rebuilt when Clark approves that cut.

## How to rebuild the cover and previews

The cover and the audiobook/videobook preview are reproducible from files in this repository:

- Cover: https://clarkhuang.github.io/book-source/cover/PROMPT.md and https://clarkhuang.github.io/book-source/cover/render_cover.py
- Preview narration, captions, chapters, and videobook: https://clarkhuang.github.io/book-source/preview/REBUILD.md

Do not invent new story details when regenerating. Keep the fiction framing and the Charlie Hack narrator. The xAI API key, if needed for narration, stays in the environment and is never written to a file.
