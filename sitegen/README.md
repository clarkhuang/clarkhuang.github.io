# Site generator

These scripts build the static HTML, CSS, Markdown twins, and `llms.txt` for this site.

```bash
# from the repository root
SITE=. python3 sitegen/gen.py
```

There is no build step on GitHub Pages: the generated files in the repo root are what gets published. Run the generator when you change lesson data, book copy, or styles, then commit the output.

The production site loads Google Analytics 4 (`G-F50XBTM25X` in `sitegen/gen.py`) with IP anonymization and ads personalization / Google Signals turned off. The tag must not fire on `/staging/` pages (the snippet skips them by path). Keep the “Use this page with your AI” prompt, `AGENTS.md`, and `llms.txt` so other people (and their AIs) can read the site without a browser. The public privacy note is at `/book/editorial-policy/#analytics`.
