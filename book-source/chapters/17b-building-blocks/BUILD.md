# Chapter 17b, Building Blocks — build notes

Text-only v0 draft for staging. There is no videobook or audio track yet.

## Source

- Clark's own fitness journey, drafted from `/workspace/legacy/interviews/fitness-journey-notes.md` (private working notes, not in this repo) and the official results those notes cite.
- Thread and issue: [issue #67](https://github.com/clarkhuang/clarkhuang.github.io/issues/67). This chapter references that issue; it does not close it.
- Placement: first half, “Themes along the way,” after Chapter 17, “Falling and Getting Up,” and before reserved Chapter 18. Numbered **17b** so existing chapter numbers and the live Chapter 36 URL do not change. The outline already uses 7a and 7b, so 17b follows that scheme.
- Genre: nonfiction, in Clark's own voice, not Charlie Hack's. Employer described generically. No private names, no family, therapy, or relationship detail.

## Open questions

See `OPEN-QUESTIONS.md` in this folder. The Quarterfinals year (2024) and the vision-board items Clark has given are now in the chapter. The business-specific items on the board are mentioned only as such.

## How to add video later

When Clark wants a videobook, follow the Chapter 36 path in `book-source/chapters/36-sick-well-fit/BUILD.md`: write a scene script from this chapter text, narrate it, render, then add `video`, `audio`, `captions`, `poster`, and `transcript.md` here and rebuild the chapter pages with:

```bash
SITE=. python3 sitegen/book_chapters.py
SITE=. python3 sitegen/story_arc.py
```

Do not run a full `sitegen/gen.py` in place. After media lands, run `python3 sitegen/stamp_versions.py` and `python3 sitegen/check_site.py .`.

## Rebuild the pages only

```bash
SITE=. python3 sitegen/book_chapters.py
SITE=. python3 sitegen/story_arc.py
```

Then keep `book.json`, `llms.txt`, `llms-full.txt`, `sitemap.xml`, `search-index.json`, and the book landing-page mentions in sync with those outputs (the scoped path updates them directly).
