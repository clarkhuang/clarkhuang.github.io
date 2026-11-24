# Ask the Book

HTML page: https://clarkhuang.github.io/ask/

The HTML version of this page has a “Use this page with your AI” box at the top. Copy the prompt below into ChatGPT, Claude, Grok, or any other chat tool:

> Read https://clarkhuang.github.io/llms.txt and https://clarkhuang.github.io/ask/index.md (plus https://clarkhuang.github.io/ask/AGENTS.md). Summarize this page, then act as my guide to Clark Huang's site: list related lessons, answer my questions citing page URLs, and quiz me if I ask.

Search the lessons, the OpenBook preview, and the transcripts on this site. Instant search runs in your browser over [search-index.json](https://clarkhuang.github.io/search-index.json) and never leaves this page. Each hit is a cited link.

To have your own AI answer a question, use the “Ask your AI” buttons on the HTML page, or copy the prompt below, add your question, and paste it into ChatGPT, Claude, Grok, Perplexity, or any other chat tool.

> You are helping a reader of Clark Huang's site (https://clarkhuang.github.io/).
>
> Question: (type your question)
>
> Instructions:
> 1. Read https://clarkhuang.github.io/llms-full.txt (or https://clarkhuang.github.io/llms.txt if that is too long). If you can connect tools, use the read-only GitMCP endpoint at https://gitmcp.io/clarkhuang/clarkhuang.github.io.
> 2. Answer only from this site. If the answer is not on the site, say so. Do not invent stories, quotes, numbers, or biography.
> 3. Cite full https://clarkhuang.github.io/… URLs (prefer the index.md twins).
> 4. If the question is about the OpenBook Silicon Valley C Players or its narrator, answer in the tone of Charlie Hack, the book's fictional narrator. The story chapters are an embellished fictional dramatization; the how-to-work-with-AI half is nonfiction. Do not treat story events as facts about real people.
> 5. For lesson questions, stay practical and cite the lesson rule.

This page does not run a hosted chatbot and does not use a site API key. A future hosted “talk to Charlie Hack” chat, via a serverless proxy, is documented in [AGENTS.md](https://clarkhuang.github.io/AGENTS.md) and has not been built.

# Connect your AI (MCP)

**First-party option:** this site also ships its own small, read-only [site MCP server](https://clarkhuang.github.io/mcp/) (stdio, one Python file, no dependencies) with tools for lessons, transcripts, captions, media checks, search, and contributor-style issue drafts. Claude Code: `claude mcp add clarkhuang-site -- uv run https://clarkhuang.github.io/mcp/clarkhuang_site_mcp.py`. Details: https://clarkhuang.github.io/mcp/index.md. The GitMCP endpoint below is a remote, third-party alternative; its full-text fetch is current, but its search can lag behind the site.

This project has a public, read-only [GitMCP](https://gitmcp.io) endpoint:

`https://gitmcp.io/clarkhuang/clarkhuang.github.io`

GitMCP is a free third-party service. It is not affiliated with this site. It only reads public documentation (it prefers [`llms.txt`](https://clarkhuang.github.io/llms.txt)) and public code. It cannot open issues, merge pull requests, or change the book. To contribute, file a GitHub issue — see [Contribute with your AI](https://clarkhuang.github.io/contribute/).

Verified against GitMCP 1.1.0 over MCP Streamable HTTP. The tools it exposes for this repository are:

- `fetch_clarkhuang_docs` — loads the primary documentation (currently `llms.txt`)
- `search_clarkhuang_docs` — searches that documentation
- `search_clarkhuang_code` — searches the repository via GitHub code search
- `fetch_generic_url_content` — fetches a specific public URL mentioned in the docs (respects robots.txt)

## Claude Code

```bash
claude mcp add --transport http clarkhuang https://gitmcp.io/clarkhuang/clarkhuang.github.io
```

## Claude Desktop

If your Claude Desktop build supports a remote HTTP MCP server, add the URL above. Otherwise use the `mcp-remote` bridge in `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "clarkhuang": {
      "command": "npx",
      "args": ["mcp-remote", "https://gitmcp.io/clarkhuang/clarkhuang.github.io"]
    }
  }
}
```

## Cursor

Add this to `~/.cursor/mcp.json` (or the project `.cursor/mcp.json`):

```json
{
  "mcpServers": {
    "clarkhuang": {
      "url": "https://gitmcp.io/clarkhuang/clarkhuang.github.io"
    }
  }
}
```

## ChatGPT and other connectors

Paste this as the connector / MCP server URL (Streamable HTTP):

`https://gitmcp.io/clarkhuang/clarkhuang.github.io`

## Example prompts

- “Using the clarkhuang GitMCP tools, what is *Silicon Valley C Players*, and how can I contribute a story without using real names?”
- “Search the docs for the standing rule in AI Tips lesson 1 and quote it, with a link to the Markdown twin.”
- “Fetch the documentation, then list the Software Engineering 101 lessons and their rules.”

More: [Ask the Book](https://clarkhuang.github.io/ask/) · [llms.txt](https://clarkhuang.github.io/llms.txt) · [llms-full.txt](https://clarkhuang.github.io/llms-full.txt) · [AGENTS.md](https://clarkhuang.github.io/AGENTS.md)


## For agents

- This page: https://clarkhuang.github.io/ask/index.md
- This folder’s agents file: https://clarkhuang.github.io/ask/AGENTS.md
- Search index: https://clarkhuang.github.io/search-index.json
- Full site text: https://clarkhuang.github.io/llms-full.txt
- GitMCP: https://gitmcp.io/clarkhuang/clarkhuang.github.io
- Site index: https://clarkhuang.github.io/llms.txt
