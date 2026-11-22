# Claims in Lesson 1 about this site, and where to check them

| Claim in the lesson | Where it is true |
|---|---|
| Every page has an `index.md` twin | Each HTML page has `index.md` beside it; see `AGENTS.md` (“How to read this site without a browser”) |
| Every folder has an `AGENTS.md` | `AGENTS.md` at the root and in each section and lesson folder |
| An `llms.txt` indexes the whole site | `/llms.txt` (and the longer `/llms-full.txt`) |
| A machine-readable lesson catalog | `/lessons.json` |
| A read-only connector AI tools can plug into | GitMCP endpoint `https://gitmcp.io/clarkhuang/clarkhuang.github.io`, documented in `AGENTS.md` and `/contribute/#mcp` |
| Pages are generated from one content file | `sitegen/gen.py` reads `sitegen/content.json` |
| The rebuild steps are written down | `REBUILD.md` |
| Agents open pull requests into a staging branch | `REBUILD.md` and `AGENTS.md`: agent PRs target `next-revision` |
| Staging is a full preview, hidden from search | `.github/workflows/deploy-pages.yml` publishes `next-revision` at `/staging/` with `noindex`; `robots.txt` disallows `/staging/` |
| Checks run on every deploy | `deploy-pages.yml` checks staging noindex, `robots.txt`, and that the sitemap and `llms.txt` do not list `/staging/`; `sitegen/check_site.py` checks links and media |
| Only the owner merges to production | `REBUILD.md` and `AGENTS.md`: only Clark merges `next-revision` into `main` |

Lines that are general teaching, not claims about a specific system: the definition of AI-native, the four things, the kitchen analogy, the enterprise-scale paragraph, the series path, the rule, and the reply ask.
