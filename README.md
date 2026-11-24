# Clark Huang

Public learning pages on AI-native software work, and a free OpenBook, *Silicon Valley C Players*.

**Live site:** [https://clarkhuang.github.io/](https://clarkhuang.github.io/)

This repository is a [template](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template). You can [copy it for yourself](https://clarkhuang.github.io/copy-this/) or [contribute with your AI](https://clarkhuang.github.io/contribute/).

## What's here

- [AI Tips](https://clarkhuang.github.io/ai-tips/) — short video lessons on working with AI tools.
- [Software Engineering 101](https://clarkhuang.github.io/software-engineering-101/) — fundamentals for AI-native software work.
- [Software Engineering 201: From Loop to Enterprise Systems](https://clarkhuang.github.io/software-engineering-201/) — the next series: from one AI loop to whole apps and systems built AI-native, then agents that operate enterprise systems, ending with a capstone that builds one feature end to end (all ten lessons are out, starting with “Four Eras of Building Systems”).
- [Silicon Valley C Players](https://clarkhuang.github.io/book/) — a free OpenBook (audiobook and videobook preview), coming in 2027. An embellished fictional dramatization that may or may not be based on true stories.

## For people and for AI

Every page has a Markdown twin (`index.md`) and an `AGENTS.md`. Start at [`llms.txt`](https://clarkhuang.github.io/llms.txt). There is a copy-paste prompt at the top of each page.

- [`lessons.json`](https://clarkhuang.github.io/lessons.json): every series and lesson, with its rule, page URL, and video URL.
- [`book.json`](https://clarkhuang.github.io/book.json): the book preview catalog.
- [`llms.txt`](https://clarkhuang.github.io/llms.txt) and [`llms-full.txt`](https://clarkhuang.github.io/llms-full.txt): catalogs and full text for language models.
- [Ask the Book](https://clarkhuang.github.io/ask/): in-browser search and “Ask your AI” prompts.
- [Contributors](https://clarkhuang.github.io/contributors/): people whose contributions have landed, by public GitHub display name or handle ([`contributors.json`](https://clarkhuang.github.io/contributors.json)).
- GitMCP (read-only, third-party): `https://gitmcp.io/clarkhuang/clarkhuang.github.io`. See [the MCP section](https://clarkhuang.github.io/contribute/#mcp).
- Site MCP server (first-party, read-only, stdio): `uv run https://clarkhuang.github.io/mcp/clarkhuang_site_mcp.py`. See [the MCP page](https://clarkhuang.github.io/mcp/).

## How this project runs

Issues, pull requests, and tagged editions work like a software project. Anyone can open an issue from day one. Only Clark Huang approves work, starts the build agents, and merges. See [CONTRIBUTING.md](CONTRIBUTING.md), [DISCLAIMER.md](DISCLAIMER.md), [TAKEDOWN.md](TAKEDOWN.md), and [book-source/VERSIONING.md](book-source/VERSIONING.md).

The live site is static: plain HTML, CSS, and a small script (`assets/site.js`), served from the `main` branch root. The generator is in [`sitegen/`](sitegen/). Watched progress and bookmarks are first-party cookies in your browser. There are no analytics and no third-party scripts.

This entire site and its content were created by AI processes, directed by Clark Huang.

Book text is licensed [CC BY-NC-SA 4.0](book-source/LICENSE).
