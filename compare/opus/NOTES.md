# Opus variant: notes

Built by Claude Opus 5.5 (`claude-opus-5-5`). Served at `/compare/opus/`. It uses plain HTML, one stylesheet (`styles.css`, about 19 KB), one script (`site.js`, about 11 KB) and an SVG favicon. There are no frameworks, fonts, CDNs or third-party requests. All content comes from `_ref/`. Pages were written by a one-off helper (`../tools/build.py`). The output is static and does not need it.

## Changes from the baseline and why
- **Relative links everywhere** so the variant works under a subpath. Shared media use absolute root paths (`/videos/…`, `/audio/…`, `/book/cover.jpg`).
- **Light and dark themes** follow `prefers-color-scheme`. Before, the site was dark only. System fonts. AA-contrast palette. A visible `:focus-visible` ring. Skip link, landmarks, breadcrumbs as `<nav><ol>`, `aria-current` in nav and chapters. Works down to 320 px wide, with no horizontal overflow at 390 px.
- **Chapters are real links** (`video.mp4#t=…`). Without JS they open the media at that time. With JS they seek the in-page player. The current chapter is highlighted while it plays.
- **Cookies are namespaced:** `opus_watched`, `opus_vpos` (video resume) and `opus_book_pos` (audio bookmarks). All use `path=/; SameSite=Lax`, `Secure` on https, and a 1-year max-age. Writes are throttled to every 5 s and forced on pause, seek and `pagehide`.
- **Resume is offered, not forced.** A "Resume from m:ss" button appears for videos and both audio tracks. It is cleared once the media ends.
- **Progress UI:** a native `<progress>` and a count on the home and series pages, plus an "Up next" link to the first unwatched lesson. "Reset progress" clears watched lessons and video positions. "Forget my listening bookmarks" clears audio bookmarks. Changes are announced through a `role="status"` region. Progress widgets stay hidden without JS, so nobody sees a false "0 watched".
- **"Copy rule" button** on each lesson. The rule is written for agents. The button appears only when the Clipboard API is available.
- **Book page:** both preview tracks, each with a seekable scene list and a collapsible transcript. The transcript is the script text verbatim, with the markup removed. The dramatization disclaimers are kept word for word. Formats that are not out yet are plain text instead of fake disabled links.
- **Videobook teaser (`book/videobook/`):** six SVG stick-figure scenes, driven each frame by `audio.currentTime`. Elements appear sentence by sentence. Captions are the `book-preview.json` text verbatim, minus `[pause]`, `<emphasis>` and `<slow>`. A full transcript sits below and doubles as a seek list. Figures move only while the audio plays. Under `prefers-reduced-motion` all animation stops and only the scenes change. Without JS, the audio and transcript still work and scene 1 is shown.
- **SE 201:** an animated SVG/CSS "loop → graph" teaser labelled "Coming soon", on the series page and both outline pages.
- **`lessons.json` / `book.json`:** page URLs point to this variant and media URLs stay at the site root. Cookie names are updated. `book.json` gains the teaser URL and estimated scene starts.
- **Branding:** the footer links to the company sites were removed. The bio text is unchanged from `_ref`, but the company names are no longer links.

## Known issues
- **Caption and scene timings are estimates.** No alignment data exists, so they come from a proportional model in `tools/timing.py` (characters, punctuation, `[pause]` beats, scaled to the track length). They can be off by about a second. A forced-alignment pass on the real MP3 would fix that.
- **Testing used silent stand-in media** in headless Chrome, not the real MP4/MP3 files. The checks covered links, cookies, resume, chapter seek, teaser sync, no-JS, reduced motion, and mobile overflow. Scenes have not been checked against the real narration by ear.
- **There is no 404 page.** GitHub Pages only uses the root one.
- **`../tools/_preview` and `../tools/_shots`** are local QA leftovers (silent media, screenshots). They are not part of the site.
