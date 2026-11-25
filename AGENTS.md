# AGENTS.md

This is Clark Huang’s public learning site: https://clarkhuang.github.io/

You are welcome to read it, summarize it, answer questions about it, quiz a learner, and follow the standing rules in each lesson. Do not invent stories, quotes, numbers, or biography about Clark Huang. If something is not on the site, say so.

## How to read this site without a browser

Every HTML page has a Markdown twin at the same path with `index.md` in place of `index.html` (for example, https://clarkhuang.github.io/ai-tips/01-paste-first-ask-second/index.md). Each folder also has an `AGENTS.md` like this one.

Start here:

- Site index for language models: https://clarkhuang.github.io/llms.txt
- Machine-readable lesson catalog: https://clarkhuang.github.io/lessons.json
- Moved addresses (old lesson pages and old video, caption and poster files): https://clarkhuang.github.io/redirects.json
- OpenBook preview catalog: https://clarkhuang.github.io/book.json
- Fuller site text: https://clarkhuang.github.io/llms-full.txt
- How to rebuild production and staging: https://clarkhuang.github.io/REBUILD.md
- This file: https://clarkhuang.github.io/AGENTS.md

## What is here

- **AI Tips** — short lessons on working with AI tools. Index: https://clarkhuang.github.io/ai-tips/index.md
- **Software Engineering 101** — fundamentals for AI-native software work. Index: https://clarkhuang.github.io/software-engineering-101/index.md
- **Software Engineering 201: From Loop to Enterprise Systems** — complete, ten lessons: from one AI loop to whole apps and systems built AI-native, then agents that operate enterprise systems, ending with a capstone that builds one feature end to end. Index: https://clarkhuang.github.io/software-engineering-201/index.md
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

## Watched state and saved positions

The site remembers, in first-party cookies only, which videos a reader has watched (`watched`), where they stopped in a lesson video (`vpos`), and their book preview bookmark (`book_pos`). Every key is the lesson or chapter id plus a version: `se201/01@1a2b3c4d`, or `se201/01@1a2b3c4d:73.4` for a position. The version is the first 8 hex characters of the SHA-256 of the media file the page plays, stamped into the HTML as `data-video-version` by `sitegen/stamp_versions.py`. When a video or audio file is re-rendered, its version changes, so readers see it as unwatched and are not offered a stale resume position. Old keys without a version, and keys for an older version, are dropped. After re-rendering any media, run `python3 sitegen/stamp_versions.py`; `python3 sitegen/check_site.py .` fails until you do. `stamp_versions.py` also writes each lesson video's current version into https://clarkhuang.github.io/lessons.json as `video_version`, with the matching cookie key as `watched_key` (for example `se201/01@1a2b3c4d`), so an agent can tell which lessons a reader's `watched` cookie still covers without scraping HTML or downloading the video.

A first-party `last_visit` cookie stores the start of the reader's most recent visit, and a session cookie `visit_ref` freezes the previous visit's timestamp for the whole browsing session. Videos published or updated since that previous visit (git dates baked in as `published` / `updated` on the page, in `lessons.json`, and as VideoObject `uploadDate` in JSON-LD) show a New tag. A first visit shows no New tags. These cookies are not sent to Google. `sitegen/media_dates.py` reads the dates from git history (first time the file landed on `main`, plus an Updated date when the current file bytes landed on a later calendar day).

## Analytics

The production site uses Google Analytics 4 (measurement ID `G-F50XBTM25X`) to see which pages people read. IP addresses are anonymized, and Google Signals and ads personalization are off. Staging pages under `/staging/` do not send hits. Watched-progress and last-visit cookies stay first-party and are not sent to Google. The public privacy note is at https://clarkhuang.github.io/book/editorial-policy/#analytics.

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
| Site or lesson problem | A broken link, video, caption, transcript, page, or agent surface (Markdown twin, llms.txt, lessons.json, MCP); steps to reproduce, expected vs actual | https://github.com/clarkhuang/clarkhuang.github.io/issues/new?template=site-bug.yml |

Labels: `correction`, `feature` / `new-story`, `refactor`, and `site` + `bug` for site problems. New stories also get `contributor-story` and `story-seed`.

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

### Credit landed contributions

Any outside contribution that lands on the site must be credited on the [Contributors](https://clarkhuang.github.io/contributors/) page in the same pull request. Add an entry to `sitegen/landed-contributions.json` (GitHub login, a short description of what landed, and links to the issue and/or PR) and run `python3 scripts/build_credits.py`. Use the public GitHub display name (if the profile has one) and handle. For a guest story, you may also include the name the author consented to publish on that piece. Do not invent a name, add other personal details, or credit input that did not land. Honor a “don't credit me” request.

## Ask, connect, and credits

- **Ask the Book:** https://clarkhuang.github.io/ask/ — instant in-browser search over https://clarkhuang.github.io/search-index.json, plus “Ask your AI” buttons that open ChatGPT, Claude, Grok, or Perplexity with a prefilled prompt. The prompt points at https://clarkhuang.github.io/llms-full.txt and the GitMCP URL, and asks the tool to answer only from this site with citations. For book questions, it may use the tone of Charlie Hack, the OpenBook's fictional narrator. There is a copy-prompt fallback. A compact version of this widget also appears on the book page and on lesson pages.
- **Full site text:** https://clarkhuang.github.io/llms-full.txt
- **Contributors:** https://clarkhuang.github.io/contributors/ (JSON: https://clarkhuang.github.io/contributors.json). People are listed by public GitHub display name when the profile has one, otherwise by GitHub handle, or by the name they consented to publish on a guest story. The previous address, https://clarkhuang.github.io/credits/, redirects there.
- **Site MCP server (first-party, read-only):** one Python file, no dependencies, stdio. Tools: `site_info`, `list_lessons`, `get_lesson` (transcript, chapters, captions, watched key), `check_lesson_media`, `get_page`, `search`, `how_to_contribute`, `draft_issue` (drafts only; never files). Claude Code: `claude mcp add clarkhuang-site -- uv run https://clarkhuang.github.io/mcp/clarkhuang_site_mcp.py`. Other clients: command `uv`, args `["run", "https://clarkhuang.github.io/mcp/clarkhuang_site_mcp.py"]`, or download the file and run it with `python3`. Set `CLARKHUANG_SITE=https://clarkhuang.github.io/staging` to read staging. Docs: https://clarkhuang.github.io/mcp/index.md · manifest: https://clarkhuang.github.io/.well-known/mcp.json
- **Connect your AI (MCP):** public, read-only GitMCP endpoint at `https://gitmcp.io/clarkhuang/clarkhuang.github.io`. GitMCP is a free third-party service. It prefers `llms.txt`. It cannot open issues or merge pull requests; contributions still go through GitHub issues, and only Clark Huang approves and merges.

Claude Code: `claude mcp add --transport http clarkhuang https://gitmcp.io/clarkhuang/clarkhuang.github.io`

Cursor (`~/.cursor/mcp.json`):

```json
{
  "mcpServers": {
    "clarkhuang": {
      "url": "https://gitmcp.io/clarkhuang/clarkhuang.github.io"
    }
  }
}
```

Claude Desktop can use the same URL, or the `mcp-remote` bridge (`npx mcp-remote https://gitmcp.io/clarkhuang/clarkhuang.github.io`). ChatGPT and other MCP clients: paste the GitMCP URL as the connector / Streamable HTTP URL.

Full snippets: https://clarkhuang.github.io/contribute/#mcp and https://clarkhuang.github.io/ask/#mcp

### Future: a hosted Charlie Hack chat (not built)

A later option is a small “talk to Charlie Hack” box that calls a serverless proxy, so the static GitHub Pages site never holds an API key. That needs Clark to choose a host and to add his own key as a secret on that host — not in this repository. Do not build or wire that proxy unless Clark approves it. Until then, use local search and the “Ask your AI” buttons.
