# AGENTS.md — Contributors

This folder is the public contributors list for Clark Huang's learning site and the OpenBook *Silicon Valley C Players*.

- HTML: https://clarkhuang.github.io/contributors/
- Markdown: https://clarkhuang.github.io/contributors/index.md
- JSON: https://clarkhuang.github.io/contributors.json
- Alias (redirect): https://clarkhuang.github.io/credits/
- Alias JSON: https://clarkhuang.github.io/credits.json
- Site index: https://clarkhuang.github.io/llms.txt
- Site agents: https://clarkhuang.github.io/AGENTS.md

List people as they appear in contributors.json. Use the public GitHub display name when the JSON has a `name` field, otherwise the handle. Do not invent contributors or names. Do not add other personal details. If someone is not on the list, their work has not landed on the site (or they asked not to be credited); say so.

Any outside contribution that lands must be credited on this page in the same pull request: add an entry to `sitegen/landed-contributions.json` and run `python3 scripts/build_credits.py`.

The HTML version of this page has a “Use this page with your AI” box at the top. Copy the prompt below into ChatGPT, Claude, Grok, or any other chat tool:

> Read https://clarkhuang.github.io/llms.txt and https://clarkhuang.github.io/contributors/index.md (plus https://clarkhuang.github.io/contributors/AGENTS.md). Summarize this page, then act as my guide to Clark Huang's site: list related lessons, answer my questions citing page URLs, and quiz me if I ask.
