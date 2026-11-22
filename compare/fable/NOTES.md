# Notes — fable variant

Built by Claude Fable 5.2 (`claude-fable-5-2`). Plain static files: semantic HTML, one hand-written
`styles.css` (about 19 KB), one vanilla `site.js` (about 13 KB). No frameworks, CDNs, web fonts,
analytics or network calls. All copy comes from `_ref`; nothing about Clark was added.

## What changed vs the baseline, and why

- **Works under `/compare/fable/`.** All internal links are relative; shared media stay absolute
  (`/videos/…`, `/audio/…`, `/book/cover.jpg`).
- **Light and dark themes** from `prefers-color-scheme` (baseline was dark only), system fonts,
  serif headings, visible focus rings, skip link, breadcrumb and landmark navigation.
- **No-JS first.** Progress badges, meters, resume and copy buttons are `hidden` in the HTML and only
  revealed by the script, so nothing dead shows without JS. Chapter and scene lists are real links
  (`…mp4#t=22.7`) that the script upgrades to in-page seeking.
- **Cookies, renamed and extended:** `fable_watched`, `fable_book_pos`, and a new `fable_video_pos`
  (path=/, SameSite=Lax, Secure on https, one year). Lessons are marked watched at 90 % or on end, and
  can also be toggled by hand. Video and audio offer a "Resume from m:ss" button instead of jumping
  silently. Reset clears watched state and video resume points. Meters use native `<progress>`.
- **Lesson pages:** current chapter is highlighted during playback; "Copy the rule" button, since the
  rules are written to be pasted into agents; MP4 download link.
- **Series pages:** available lessons shown with poster thumbnails and watched state; upcoming titles
  listed separately.
- **SE 201:** animated SVG/CSS placeholders labeled "Coming soon" (loop to graph; "and then" versus
  "at the same time") on the series page and both outlines.
- **Book page:** both preview tracks with bookmarks, a chapter list, a per-track scene list, the
  Math 1A transcript (from the script), downloads, and the dramatization disclaimers unchanged.
- **Videobook teaser** (`book/videobook/`): 27 caption cues across six stick-figure scenes in one inline
  SVG, driven by the audio element's clock, so pause and seek stay in step. Captions are split from
  `book-preview.json` by the generator, which asserts they rejoin to the script text word for word.
  With `prefers-reduced-motion` the scenes change as cuts with no looping movement. If the MP3 cannot
  load, it plays silently with captions.
- **Footer** drops the baseline's company links (the bio keeps its own); adds the data file links.
- `lessons.json` / `book.json`: page URLs point at this variant, cookie names updated, teaser URL added.

`tools/build.py` (outside `out/`) stamped the pages from `_ref` so header, footer and data stay
consistent. The site itself has no build step; the output is committed as-is.

## Checked

Headless Chrome screenshots (desktop, 390 px mobile, dark, reduced motion), every teaser cue rendered
as a contact sheet, cookie-driven states (watched badges, meters, resume buttons), `node --check`,
tag balance, duplicate ids, and all internal links and fragments.

## Known issues

- **Caption timing is estimated, not measured.** No timing data ships with the recordings and the
  audio was outside this directory, so cue and scene times are apportioned by character count plus
  fixed weights for `[pause]` and scene breaks. Expect drift of a second or so in places. This also
  applies to the "approximate times" scene lists on the book page. Fix: replace the `data-t` values
  with measured ones.
- **Not tested with real media.** Video, audio and the cover image were not available locally, so
  playback, 90 % watched marking, and position saving were not exercised end to end; only the
  cookie-reading side and the silent fallback were.
- No captions or transcripts for the four lesson videos: none exist in `_ref`.
- HTML was not run through the W3C validator (offline); only structural checks were done.
- The videobook page is about 40 KB uncompressed because the crowd scene is drawn figure by figure.
