# Rebuild the site

This repository is the public site. `main` is production. `next-revision` is staging.

| Branch | What it is | URL |
|---|---|---|
| `main` | The live site | https://clarkhuang.github.io/ |
| `next-revision` | Staging preview (not the live site) | https://clarkhuang.github.io/staging/ |

A GitHub Actions workflow (`.github/workflows/deploy-pages.yml`) builds both branches on every push to `main` or `next-revision`, and on a manual **Run workflow**. Production files sit at the site root. The `next-revision` tree is copied to `/staging/`, with root-relative links rewritten so the preview is self-contained. Every staging page gets `<meta name="robots" content="noindex, nofollow">` and a visible “Staging preview — not the live site” banner. `/staging/` is disallowed in `robots.txt` and is kept out of `sitemap.xml` and `llms.txt`.

**Contributors and agents open PRs; only Clark merges to `main`; the site rebuilds from `main` via GitHub Pages; agent PRs target `next-revision`.** Only Clark merges `next-revision` into `main`.

## Generator commands

The published pages are static HTML. The generator lives in `sitegen/` (and, on the build machine, `/workspace/legacy/build/sitegen`). It reads lesson data and writes HTML, Markdown twins, `AGENTS.md`, `llms.txt`, `llms-full.txt`, `book.json`, and `lessons.json`.

From a checkout of this repository:

```bash
# Rebuild the public pages into the current tree
SITE="$PWD" python3 sitegen/gen.py
```

On the build machine used for narration and video:

```bash
SITE=/workspace/legacy/site python3 /workspace/legacy/build/sitegen/gen.py
```

Do not run `gen_extra.py` for a public build. It would add private pages that must not ship.

### Lesson video sources

Lessons that ship with their build source keep it in `lesson-sources/<lesson>/` (for example `lesson-sources/se201-01/`): the script generator, the scene script, the brief, a facts file listing every claim and where to check it, the caption builder, and the render timeline. Each folder has `BUILD.md`, `index.md`, and `AGENTS.md`. Lesson captions (`.vtt`) sit next to the MP4 in `videos/` and are set with the lesson's `captions` field in `sitegen/content.json`.

### Media versions (watched state)

`assets/site.js` keys the `watched`, `vpos`, and `book_pos` cookies on `<id>@<version>` (for example `watched=se201/01@1a2b3c4d`, `vpos=se201/01@1a2b3c4d:73.4`, `book_pos=preview@4226615c:31.2`). The version is the first 8 hex characters of the SHA-256 of the media file. It is stamped into the HTML as `data-video-version` on each `<video>`/`<audio>` and on every `data-watch-id`, `data-toggle-watched`, and `data-lesson-link` element, and as `data-video-versions` (same order as the ids) on each `data-progress` meter, so series and home pages can judge versions too. A re-rendered file gets a new version: readers see it as unwatched, with no stale resume offer. Keys without a version, and keys for an old version of media the page shows, are pruned when a page loads. The videobook and audiobook are separate files, so each keeps its own bookmark.

**After re-rendering any video or audio, run:**

```bash
python3 sitegen/stamp_versions.py          # rewrites only the version attributes, idempotent
python3 sitegen/check_site.py .            # fails if any page's version does not match its media file
```

`gen.py` calls the same `stamp_site()` at the end of a build, so both paths agree. `python3 sitegen/test_watched_versions.py` runs a headless-browser test of the whole flow against a temporary copy of the site.

### Publish dates and New tags

Every lesson video and the book videobook shows a publish date taken from git history: the first time that file landed on `main` (or on the current branch, for a staging-only video). If the current file bytes landed on a later calendar day (America/New_York), the page also shows “Updated <date>”. The same dates are written into VideoObject `uploadDate` / `dateModified` in the page JSON-LD, into `lessons.json` / `book.json`, and into the Markdown twins and `llms.txt`. `sitegen/media_dates.py` computes them at generate time, so a new video (for example the next AI Tips lesson) picks them up automatically.

A “New” tag is shown, in the browser only, on any video published or updated since the visitor's previous visit. A first-party `last_visit` cookie stores the start of the most recent visit; a session cookie `visit_ref` freezes the previous visit's timestamp for the whole browsing session so the tags do not vanish on the next page click. A first visit shows no New tags. Nothing is sent to a server. `python3 sitegen/test_new_tags.py` covers this flow. After a rebuild, `python3 sitegen/check_site.py .` also checks that dates and VideoObject `uploadDate` are present and match git when history is available.

When a lesson slug changes, leave a small redirect page (`index.html` with `noindex`, a canonical link, and a refresh to the new page, plus `index.md` and `AGENTS.md` pointing at the new address) in the old folder so live links keep working.

### Cover and book preview

```bash
python3 book-source/cover/render_cover.py
# Preview narration, loudnorm, videobook: see book-source/preview/REBUILD.md
```

The xAI API key, if needed for narration, stays in the environment as `XAI_API_KEY` and is never written to a file.

### Compose production + staging locally (as the workflow does)

```bash
# After both branches exist locally, or using two checkouts:
python3 sitegen/compose_pages.py \
  --prod /path/to/main-checkout \
  --staging-src /path/to/next-revision-checkout \
  --out /tmp/site-out

# Preview locally
python3 -m http.server 8765 --bind 127.0.0.1 --directory /tmp/site-out
# Production: http://127.0.0.1:8765/
# Staging:    http://127.0.0.1:8765/staging/
```

`compose_pages.py` copies prebuilt files; it does not re-run the generator. Run `gen.py` on each branch first if the HTML is stale.

### Publish

1. Clark reviews the pull request and merges it into `next-revision`. Staging updates at https://clarkhuang.github.io/staging/.
2. Clark QAs staging (checklist below).
3. Only Clark merges `next-revision` into `main`. Production updates at https://clarkhuang.github.io/.
4. If the Actions deploy misbehaves, switch GitHub Pages back to the branch source (`main`, `/`) until it is fixed.

A tagged edition (`book-v0.1`, `book-v1.0`, …) is cut only when Clark approves that cut. See [book-source/VERSIONING.md](book-source/VERSIONING.md).

## QA checklist

Run this against production, and against staging after rewriting, before calling a rebuild done.

- [ ] **Links.** Home, series, lessons, book, contribute, copy-this, 404, footer and prompt-box links resolve. Staging links stay under `/staging/` and do not drop visitors onto the live tree by accident (except the “live site” banner).
- [ ] **HTML.** Pages are well-formed enough to open; the book cover renders; players load the preview audio and video.
- [ ] **Desktop and mobile screenshots.** Light and dark, a home page, a lesson, and the book page. Staging shows the banner.
- [ ] **Accessibility basics.** Images have descriptive alt text (especially the cover). The staging banner is visible and marked as a status. Captions are attached to the videobook. Keyboard can reach the prompt box and players.
- [ ] **AI twins / llms / AGENTS.** Every HTML page has `index.md` and `AGENTS.md`. `llms.txt` and `llms-full.txt` match the production tree and do not list `/staging/`. The “Use this page with your AI” box is on each page.
- [ ] **Media versions.** After any re-render, `python3 sitegen/stamp_versions.py` was run and `python3 sitegen/check_site.py .` passes (a re-rendered video must show as unwatched).
- [ ] **Media transcripts and captions.** `book-source/preview/transcript.md`, per-scene scripts, `videos/book-preview.vtt`, and chapter JSON are present and in sync with the audio/video.
- [ ] **Privacy grep.** Search the public tree (not `.git`) against the private name map. No real private-person names, no real company names in book/story context, no “memoir” framing on the book, no private paths (`legal/`, `*.private.md`, `interviews/`). The homepage bio and lesson transcripts may still use factual public details (for example Berkeley in a Software Engineering 101 lesson).
- [ ] **Noindex on staging.** Every staging HTML page has `noindex`. Root `robots.txt` has `Disallow: /staging/`. Staging is absent from the production sitemap and `llms.txt`.

Nothing goes live until Clark merges to `main`.

## Maintaining the public Change Log

Use a full checkout and Python 3.12 or later. Fetch `origin/main`, then run
`python3 sitegen/change_log.py --ref origin/main` from the repository root.
Pass `--repo /path/to/production-checkout --ref HEAD` to preview from a separate
checkout. Both site environments report production history. Direct commits and
merges on the first-parent path each appear once. The sequence begins at the
first commit. Dates use the commit’s integration time in America/Detroit.
The timestamp is independent of when the Pages deployment finished.

At release review, an editor or AI assistant should inspect each new mainline diff,
its merged PR and the resulting public pages. Write one sentence on what changed
for readers in `sitegen/change_log_editorial.json`, keyed by the short production
SHA. Write separate daily, ISO-week and calendar-month retrospectives explaining
the most significant outcome for that period. Cite production SHAs from that
period. Distinguish plans from shipped features. A new release appears immediately
in deployment builds with an editorial note pending until the reviewed copy lands.

Regenerate and inspect `change-log/history.json` plus each HTML and Markdown view.
The JSON is public and contains identical release records for all visitors.
It contains no reader activity. Commit the reviewed notes and generated pages
together, run `python3 sitegen/check_site.py .`, and review the staged result.
