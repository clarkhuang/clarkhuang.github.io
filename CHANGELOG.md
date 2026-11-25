# Changelog

## book-v0.1 — 2026-11-22

First public teaser for a smaller test audience, before a wider social launch.

- Production site: learning series (AI Tips, Software Engineering 101 and 201) plus the Silicon Valley C Players preview.
- Narrator in the story chapters is the fictional Charlie Hack (initials C.H.), with Clark Huang as author. Takedown requests: clark75-7bw9ct@mail.grokbot.com.
- Videobook and audiobook preview (about 2:33), narrated in Clark's AI voice. Names of private people and real companies have been removed from the teaser; the book is framed as an embellished fictional dramatization.
- OpenBook contribution path: "Contribute with your AI" and "Copy this for yourself" pages, issue templates, and contributor terms.
- Corrections and takedown policy published. Previous editions will be kept as named tagged releases.

All notable changes to the site and to *Silicon Valley C Players* are listed here. The book is versioned like software. Edition tags look like `book-v0.1`.

## [Unreleased]

Work in progress on the `next-revision` branch, until Clark approves cutting the next edition.

- Book chapter 17b, **Building Blocks**, drafted as a text-only v0: a nonfiction interlude in Clark's own voice, in “Themes along the way,” after Chapter 17 and before reserved Chapter 18. Numbered 17b so existing chapter numbers and the Chapter 36 URL stay put. No videobook yet. Builds on [issue #67](https://github.com/clarkhuang/clarkhuang.github.io/issues/67) without closing it. Clark later confirmed the Age-Group Quarterfinals year as 2024 and filled in the vision board (guitar, piano, retiring by 50, and some business-specific things). The home page now also mentions the Chapter 36 pre-release and links to it.

- Every video now shows a publish date (from git history: when it first landed on `main`). Re-rendered videos also show an Updated date when the current file landed on a later day. A New tag marks videos published or updated since the visitor's previous visit, using first-party `last_visit` and `visit_ref` cookies (a first visit shows no New tags; the cutoff stays for the whole browsing session). The same dates are in JSON-LD, `lessons.json`, `book.json`, and the Markdown twins. Staging only until Clark approves production.

- Contributors page at `/contributors/` (machine-readable `contributors.json`, `CONTRIBUTORS.md`, and `index.md` / `AGENTS.md` twins). `/credits/` now redirects there. [@himanshu112-wq](https://github.com/himanshu112-wq) is credited for the [issue #80](https://github.com/clarkhuang/clarkhuang.github.io/issues/80) feedback that led to the reworded “AI writes essentially all the code” claim and the book's editorial policy. Any outside contribution that lands is credited on this page in the same pull request.

- Book preview follow-up: struck “Stay humble. Stay curious,” and in that passage added the better father, brother, sister, and daughter. A new scene, with a new videobook ladder graphic, adds that software engineering was never about writing code: writing code was the tedious part of building your ideas, abstraction is key, and each part is data in, some logic, and data out. About 2:59. Staging only until Clark approves production.

- Added Google Analytics 4 on the production site (property `clarkhuang.github.io`, measurement ID `G-F50XBTM25X`), with IP anonymization and no ads signals. Staging pages under `/staging/` do not send hits. The footer no longer says “No analytics, no third-party scripts”; it links to a privacy note on the [editorial policy](https://clarkhuang.github.io/book/editorial-policy/#analytics) page.

- Mid-book preview re-recorded (about 2:39) so the narration matches the own-workflow wording and flows more like Clark talking. A follow-up re-record makes the letter A in “A Things,” “A players,” and “an A thing” sound like the letter (/eɪ/), not “eye,” and fully re-renders the videobook so the pictures, captions, and timing match. Staging only until Clark approves production.

- Clarified the book preview claim: “AI writes essentially all of the code” is Clark's own workflow (the code he ships), not a measured team result or a prediction. Chapter 20 of the outline no longer says “100% of the code.” That claim is now also in the mid-book preview narration and captions ([issue #80](https://github.com/clarkhuang/clarkhuang.github.io/issues/80)). Fixed a staging rewrite bug that left some `AGENTS.md` Markdown URLs pointing at production.

- Public story arc and chapter list for Silicon Valley C Players (`/book/story-arc/`), with a machine-readable outline at `book-source/outline.json`. The book is framed as two halves: the career arc, then the site and future directions. Chapter 32 now describes Software Engineering 201 as ten lessons, with lesson 10 a capstone and lesson 9 still an outline.
- Public editorial policy for the book (`/book/editorial-policy/`): how conflicting recollections are handled, how claims and sources are tracked, and a per-edition changelog of changed claims and sources. Book backlog started in `book-source/BACKLOG.md`. Guest-story path added in `book-source/guest/` and CONTRIBUTING.md ([issue #80](https://github.com/clarkhuang/clarkhuang.github.io/issues/80))

- Book teaser rewrite and matching videobook preview
- OpenBook working source, issue templates, and self-updating agent workflow
- Site design upgrade
- Software Engineering 201 retitled “From Loop to Enterprise Systems”: new intro and a re-planned eight-lesson path from one AI loop to AI-native enterprise systems
- New Software Engineering 201 lesson 1, “Build the Whole System, AI-Native” (video, captions, transcript, and build source in `lesson-sources/se201-01/`). The earlier lesson 1, “From Loop to Graph”, is folded into lesson 2 (outline); old lesson URLs redirect to their new pages
- Software Engineering 201 path tightened: lesson 2 is now “Decompose the System into a Graph” (old address redirects), lesson 1, 6, and 7 summaries tie each step to the path from one loop to enterprise systems, and lesson 1's chapter sources in `sitegen/content.json` point at `lesson-sources/se201-01/`
- Software Engineering 201 lessons 2 and 3 recorded: “Decompose the System into a Graph” and “Parallel Agents, One Integration” (video, captions, chapters, rule, transcript, and build source in `lesson-sources/se201-02/` and `lesson-sources/se201-03/`). The series now has 3 of 8 lessons available; lesson 2 keeps its related-reading credit and the link to the earlier recording
- Workflow fixes: `cut-edition.yml` parse error; contributor-credits PRs now target `next-revision`
- Software Engineering 201 restructured into nine lessons. New lesson 1, “Four Eras of Building Systems” (video, captions, chapters, rule, transcript, and build source in `lesson-sources/se201-01/`): how building whole systems changed over thirty years, one lens, and four things that never changed
- Software Engineering 201 lessons renumbered: the recorded lessons are now 2 (“Build the Whole System, AI-Native”), 3 (“Decompose the System into a Graph”) and 4 (“Parallel Agents, One Integration”), re-rendered with only the title, rule and closing clips re-narrated; their build sources moved to `lesson-sources/se201-02/` to `se201-04/`. Outlines 5–9 rewritten. Every old lesson address redirects straight to its new page. The series now has 4 of 9 lessons available
- Software Engineering 101 lesson 10 re-rendered with a new “What's next” ending that hands off to 201, and now has captions
- Watched ticks and saved positions are now keyed per video version (`se201/01@<first 8 hex of the file's SHA-256>`), so a re-rendered video or audio shows as unwatched again; older unversioned entries are dropped. After re-rendering media, run `python3 sitegen/stamp_versions.py` (`check_site.py` now fails if a version is stale)
- Software Engineering 201 lessons 5 to 8 recorded: “Governance: Where People Decide”, “Quality, Feedback, and Observability”, “Skills as Building Blocks” and “Routines, Pipelines, and Integration” (video, captions, chapters, rule, transcript, and build source in `lesson-sources/se201-05/` to `lesson-sources/se201-08/`). The series now has 8 of 9 lessons available; lesson 9 is still an outline
- Software Engineering 201 lesson 10 recorded: “Capstone: One Feature, End to End” (video, captions, chapters, rule, transcript, notes on what the video simplifies, and build source in `lesson-sources/se201-10/`). The series is now ten lessons with 9 of 10 available; lesson 9 is still an outline, and its text now leads into the capstone
- Software Engineering 201 lesson 9 recorded: “Agents That Operate Enterprise Systems” (video, captions, chapters, rule, transcript, notes on what the video simplifies, and build source in `lesson-sources/se201-09/`). The series now has 10 of 10 lessons available; lesson 10's note about lesson 9 now says it covers the operator in full, and the story arc's “Also planned” list no longer says lesson 9 is an outline
- Software Engineering 201 lessons 1 and 8 re-rendered with one scene re-narrated each for the ten-lesson series (lesson 1's path now lists the capstone; lesson 8's close says “That's next” instead of “That's the last lesson”); captions for lessons 1, 8 and 10 spell EDI, CTO and ID without dots
- Software Engineering 201 lesson 2 re-rendered with its path scene re-narrated so it ends on the lesson 10 capstone (video now 3:58); the series wording in `AGENTS.md`, the home page and the AI-readable files now ends “with a capstone that builds one feature end to end”; lesson 10's rule card uses the “In full:” format; a missing period restored in lesson 7's captions (PR #86)
- Agent dogfooding fixes (issues #88–#94): a first-party, read-only site MCP server (`/mcp/`, `/.well-known/mcp.json`) with lesson, transcript, caption, media-check, search and issue-draft tools; `/redirects.json` and a 404-page redirect for old Software Engineering 201 video, caption and poster addresses; a “Site or lesson problem” issue form; `video_version` and `watched_key` for every lesson video in `lessons.json`; `<time datetime>` durations that match the visible text; and lesson 9's summary now calls it “the last step before the capstone”

## [v0.1-wip] — 2026-11-22

What is live on [clarkhuang.github.io](https://clarkhuang.github.io) today, before the first tagged book edition.

### Added

- AI Tips, lessons 1–16
- Software Engineering 101, lessons 1–10
- Software Engineering 201, lesson 1 (lesson 2 is still an outline)
- AI-friendly layer: `llms.txt`, `AGENTS.md` at every level, Markdown `index.md` twins, and a copy-paste “Use this page with your AI” prompt
- Public book teaser page for *Silicon Valley C Players*

### Changed

- AI Tips lessons 1–2 and Software Engineering 101 lessons 1–2 re-recorded in the current Clark voice, so the series sound consistent

## Unreleased: fiction framing (Nov 22, 2026)

- The book is now framed as an **embellished fictional dramatization** that may or may not be based on true stories. Added `DISCLAIMER.md`, `TAKEDOWN.md`, `book-source/NAMING-POLICY.md`, a `takedown-request` issue template, and contributor terms (DCO sign-off, warranties, consent to fictionalization) in `CONTRIBUTING.md`.
- Story-world names in the outline and issues replaced with fictional ones.
