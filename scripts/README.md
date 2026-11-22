# Site feature scripts

Small generators used by the Ask the Book page and the contributor credits page. They need no API keys.

Run from the repository root:

```bash
python3 scripts/build_ai_index.py --search-only   # writes search-index.json
    python3 scripts/build_ai_index.py --llms-full      # also writes llms-full.txt (sitegen usually owns this)
python3 scripts/build_credits.py     # writes credits.json and credits/* (needs `gh`)
```

`build_credits.py` is also run by [`.github/workflows/credits.yml`](../.github/workflows/credits.yml) when an issue or merged pull request is closed, and weekly. That workflow opens a pull request into `main`. It must not use `ANTHROPIC_API_KEY`.

The site generator (`sitegen/gen.py`) already calls `build_ai_index.py --search-only` at the end of a site build, so `search-index.json` stays in sync. `llms-full.txt` is written by sitegen. Run `build_credits.py` separately (or via the credits workflow).

Do not commit `*.private.md` or anything under a private `legal/` tree. The index builder already skips `compare/`, `playbook/`, `interview-plan/`, `research/`, and `*.private.md`.
