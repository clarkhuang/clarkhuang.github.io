# Site MCP server

HTML page: https://clarkhuang.github.io/mcp/

The HTML version of this page has a “Use this page with your AI” box at the top. Copy the prompt below into ChatGPT, Claude, Grok, or any other chat tool:

> Read https://clarkhuang.github.io/llms.txt and https://clarkhuang.github.io/mcp/index.md (plus https://clarkhuang.github.io/mcp/AGENTS.md). Summarize this page, then act as my guide to Clark Huang's site: list related lessons, answer my questions citing page URLs, and quiz me if I ask.

A small, read-only MCP server for this site. It is one Python file with no dependencies (Python 3.9+). It runs locally over stdio and reads only the site's public files: lessons.json, search-index.json, the Markdown twins and the WebVTT captions. It cannot change the site, file issues or merge anything.

## Connect it

- Claude Code: `claude mcp add clarkhuang-site -- uv run https://clarkhuang.github.io/mcp/clarkhuang_site_mcp.py`
- Cursor, Claude Desktop and other MCP clients:

```json
{
  "mcpServers": {
    "clarkhuang-site": {
      "command": "uv",
      "args": ["run", "https://clarkhuang.github.io/mcp/clarkhuang_site_mcp.py"]
    }
  }
}
```

- Without uv: download https://clarkhuang.github.io/mcp/clarkhuang_site_mcp.py and run it with `python3`.
- Staging instead of production: set `CLARKHUANG_SITE=https://clarkhuang.github.io/staging`. A local clone: set it to the folder path.
- Machine-readable: https://clarkhuang.github.io/.well-known/mcp.json

## Tools

- `site_info`: What the site is, lesson counts, discovery files, how watched progress is keyed, staging vs production. Call it first.
- `list_lessons`: Every lesson in AI Tips, Software Engineering 101 and 201: id, status, duration, page and Markdown URLs.
- `get_lesson`: One lesson: summary, rule, video, captions and poster URLs, chapters, video version and watched key, and the Markdown twin with the full transcript (captions and AGENTS.md on request).
- `check_lesson_media`: HTTP status of a lesson's page, twin, AGENTS.md, video, captions and poster; with no id, every lesson's problems.
- `get_page`: Any page as Markdown, for example /, /book/ or /contribute/.
- `search`: Keyword search over the site's own search-index.json, with URLs to cite.
- `how_to_contribute`: Issue templates, labels, branches, checks, and who merges.
- `draft_issue`: A contributor-style issue (steps, expected, actual) with a prefilled GitHub URL and a gh command. It never files anything.

## Contribute like an outside contributor

1. Call `site_info`, then `list_lessons` and `get_lesson`.
2. Call `check_lesson_media` and read pages with `get_page`; compare what you find with what the docs promise.
3. Found a real problem? Call `draft_issue`, check the draft for anything private, then file it with the Site or lesson problem form: https://github.com/clarkhuang/clarkhuang.github.io/issues/new?template=site-bug.yml
4. To fix it, branch from `next-revision`, keep `index.md`, `AGENTS.md` and `llms.txt` in sync, run `python3 sitegen/check_site.py .`, and open a pull request into `next-revision` with `Fixes #N`. Only Clark merges to production.

A third-party remote option is GitMCP (https://clarkhuang.github.io/contribute/#mcp). Its fetch is current, but its search can lag behind the site, and it has no lesson or issue tools.

## For agents

- This page: https://clarkhuang.github.io/mcp/index.md
- This folder’s agents file: https://clarkhuang.github.io/mcp/AGENTS.md
- Site index: https://clarkhuang.github.io/llms.txt
- Site agents: https://clarkhuang.github.io/AGENTS.md
