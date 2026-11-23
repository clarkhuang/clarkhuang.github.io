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
