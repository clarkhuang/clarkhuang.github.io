# AGENTS.md

This is Clark Huang’s public learning site: https://clarkhuang.github.io/

You are welcome to read it, summarize it, answer questions about it, quiz a learner, and follow the standing rules in each lesson. Do not invent stories, quotes, numbers, or biography about Clark Huang. If something is not on the site, say so.

## How to read this site without a browser

Every HTML page has a Markdown twin at the same path with `index.md` in place of `index.html` (for example, https://clarkhuang.github.io/ai-tips/01-paste-first-ask-second/index.md). Each folder also has an `AGENTS.md` like this one.

Start here:

- Site index for language models: https://clarkhuang.github.io/llms.txt
- Machine-readable lesson catalog: https://clarkhuang.github.io/lessons.json
- OpenBook preview catalog: https://clarkhuang.github.io/book.json
- Fuller site text: https://clarkhuang.github.io/llms-full.txt
- How to rebuild production and staging: https://clarkhuang.github.io/REBUILD.md
- This file: https://clarkhuang.github.io/AGENTS.md

## What is here

- **AI Tips** — short lessons on working with AI tools. Index: https://clarkhuang.github.io/ai-tips/index.md
- **Software Engineering 101** — fundamentals for AI-native software work. Index: https://clarkhuang.github.io/software-engineering-101/index.md
- **Software Engineering 201** — the next series, in progress. Index: https://clarkhuang.github.io/software-engineering-201/index.md
- **Silicon Valley C Players** — a free OpenBook, with an audiobook and videobook preview, coming in 2027. https://clarkhuang.github.io/book/index.md

Each available lesson has a video, a one-paragraph rule written so an agent can follow it as a standing instruction, and a full transcript in its `index.md`. The book page has a short videobook and audio preview of Silicon Valley C Players.

## How to help a reader

If someone pastes a page URL or the copy-paste prompt from the “Use this page with your AI” box on any HTML page:

1. Fetch `llms.txt` and the page’s `index.md` (and that folder’s `AGENTS.md`).
2. Summarize the page they started from.
3. List related lessons, with full `https://clarkhuang.github.io/...` URLs.
4. Answer questions by citing those URLs. Prefer the Markdown twins and the lesson rules.
5. Quiz them if they ask.

Work through the site by following links in `llms.txt` and in each `index.md`. You do not need to render HTML, play video, or run JavaScript.

## How to contribute

Anyone can take part from day one: file an issue or open a pull request. You do not have to wait for v1. Only Clark Huang approves work, starts the build agents, merges pull requests, and cuts a new edition of the book.

Contributors and agents open PRs; only Clark merges to `main`; the site rebuilds from `main` via GitHub Pages; agent PRs target `next-revision`. Staging is the `next-revision` branch, published at https://clarkhuang.github.io/staging/ (noindex; not in `llms.txt` or the sitemap). Only Clark merges `next-revision` into `main`. The rebuild flow is in [REBUILD.md](https://clarkhuang.github.io/REBUILD.md).

If you are an AI agent helping a reader contribute, point them to the right issue template, help them write a specific, honest issue without real names of private people or companies and without confidential details, and do not invent stories or details. Contributors agree to the contributor terms in CONTRIBUTING.md.

### Which issue to file

| Kind | Use it for | Template |
|---|---|---|
| Correction | Edits to existing book text, or your side of a story already in the book | https://github.com/clarkhuang/clarkhuang.github.io/issues/new?template=correction.yml |
| Feature / new story | A new story, a story Clark may have forgotten, or a new chapter idea | https://github.com/clarkhuang/clarkhuang.github.io/issues/new?template=new-story.yml |
| Refactor | Cleanup or an improvement that does not change the facts | https://github.com/clarkhuang/clarkhuang.github.io/issues/new?template=refactor.yml |

Labels: `correction`, `feature` / `new-story`, and `refactor`. New stories also get `contributor-story` and `story-seed`.

### What makes a good issue

- Be specific: when and where, what happened, and which chapter or passage if you know it.
- Don't use real names of private people, companies, or venues; describe them by role. The book is an embellished fictional dramatization and everyone in it is renamed. Say how you'd like to be credited, if at all.
- Stick to what you know. Do not invent details.
- If you were there, say so. Don't include anything confidential (NDA, customer, security, deal details).
- Something in the book identifies you or someone you know? File a takedown request instead: https://github.com/clarkhuang/clarkhuang.github.io/issues/new?template=takedown-request.yml

### What happens next

1. The issue is labeled `needs-clark-review`.
2. If Clark wants it built, he adds `approved` (or comments `@claude`). Only his label or comment starts an agent.
3. The agent opens a pull request against the `next-revision` branch, never against `main`.
4. Clark reviews and merges into `next-revision` (which updates staging).
5. Only Clark merges `next-revision` into `main`. The live site then rebuilds from `main`. Previous editions stay up as tagged GitHub Releases (`book-v0.1`, `book-v1.0`, ...). Details: https://github.com/clarkhuang/clarkhuang.github.io/blob/main/book-source/VERSIONING.md and https://clarkhuang.github.io/REBUILD.md

More: https://github.com/clarkhuang/clarkhuang.github.io/blob/main/CONTRIBUTING.md
