# Three builds, one brief

HTML page: https://clarkhuang.github.io/compare/

The HTML version of this page has a “Use this page with your AI” box at the top. Copy the prompt below into ChatGPT, Claude, Grok, Grok Bot, or any other chat tool:

> Read https://clarkhuang.github.io/llms.txt and https://clarkhuang.github.io/compare/index.md (plus https://clarkhuang.github.io/compare/AGENTS.md). Summarize this page, then act as my guide to Clark Huang's site: list related lessons, answer my questions citing page URLs, and quiz me if I ask.

# Three builds, one brief

One brief, three independent builds of this learning site: the current Grok-built baseline, and two rebuilds made by Claude Code running Claude Opus 5.5 and Claude Fable 5.2. Same content, same media, same rules: plain HTML, one CSS file, a little vanilla JavaScript, cookie-based watched tracking and listening bookmarks. Each variant keeps its own cookies, so you can try them side by side.

## The builds

### Grok baseline (Grok Bot)

The site as it was first published: dark theme matching the lesson videos, one shared script for watched progress and the audiobook bookmark.

- Dark palette that matches the videos
- Watched cookie and audiobook bookmark
- SE 201 outlines with a static placeholder
- No videobook teaser yet

Open: [Home](/compare/grok/), [AI Tips lesson 1](/compare/grok/ai-tips/01-paste-first-ask-second/), [SE 201](/compare/grok/software-engineering-201/), [Book](/compare/grok/book/)

### Opus rebuild (Claude Opus 5.5)

A light and dark rebuild with resume points for every video and track, an 'Up next' progress panel, and the clearest diagrams of the three.

- Light and dark themes, system fonts
- Resume video and audio from a cookie bookmark
- Labelled loop-to-graph SE 201 teaser
- Six-scene stick-figure videobook teaser with keyword overlays and a seekable transcript
- Leanest build of the two rebuilds

Open: [Home](/compare/opus/), [AI Tips lesson 1](/compare/opus/ai-tips/01-paste-first-ask-second/), [SE 201 teaser](/compare/opus/software-engineering-201/), [Book](/compare/opus/book/), [Videobook teaser](/compare/opus/book/videobook/), [Build notes](/compare/opus/NOTES.md)

### Fable rebuild (Claude Fable 5.2)

A bookish light and dark rebuild with serif headings, poster thumbnails on series pages, a manual 'mark as watched' toggle and the most detailed caption track.

- Serif headings, poster thumbnails on series pages
- Mark as watched by hand, plus automatic at 90 percent
- Resume video and audio from a cookie bookmark
- Two animated SE 201 placeholders
- 27-cue stick-figure videobook teaser with a crowd scene

Open: [Home](/compare/fable/), [AI Tips lesson 1](/compare/fable/ai-tips/01-paste-first-ask-second/), [SE 201 teaser](/compare/fable/software-engineering-201/), [Book](/compare/fable/book/), [Videobook teaser](/compare/fable/book/videobook/), [Build notes](/compare/fable/NOTES.md)

## Verdict

Opus by a narrow margin. Both rebuilds clearly beat the baseline on accessibility, light and dark themes, and resume points. Opus's diagrams and videobook scenes say what the narration means at a glance, and its progress panel makes 'what next' obvious. Fable's series pages, with poster thumbnails, are the nicest of the three, and its caption track is the most detailed. Its progress bars are faint in dark mode, though, and it was the heavier build.

How it was judged: every page was crawled in Chrome to check links and media paths. A lesson was played to the end to confirm the watched cookie, and video and audio were paused mid-way to confirm the resume bookmark after a reload. Pages were checked on mobile and in dark mode, and the videobook teaser was sampled at several points in the audio. Caption timings in both teasers are estimated from the script, not measured, so they may drift by a second or so.

## For agents

- This page: https://clarkhuang.github.io/compare/index.md
- This folder’s agents file: https://clarkhuang.github.io/compare/AGENTS.md
- Site index: https://clarkhuang.github.io/llms.txt
- Site agents: https://clarkhuang.github.io/AGENTS.md
