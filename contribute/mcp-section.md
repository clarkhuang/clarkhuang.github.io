# Connect your AI (MCP)

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
