# Video and site production playbook

HTML page: https://clarkhuang.github.io/playbook/

The HTML version of this page has a “Use this page with your AI” box at the top. Copy the prompt below into ChatGPT, Claude, Grok, Grok Bot, or any other chat tool:

> Read https://clarkhuang.github.io/llms.txt and https://clarkhuang.github.io/playbook/index.md (plus https://clarkhuang.github.io/playbook/AGENTS.md). Summarize this page, then act as my guide to Clark Huang's site: list related lessons, answer my questions citing page URLs, and quiz me if I ask.

# Video and site production playbook

How the lessons, audiobook previews and pages on this site are made. It is a working method, written so that a person or an AI agent can pick it up and produce the next lesson at the same standard. No secrets, no company-internal details.

## 1. The pipeline

Every lesson is code: a script file goes in, a finished video comes out. Nothing is edited by hand on a timeline.

1. **Gather real material.** A lesson starts from something that actually happened or a position the author actually holds. Agents never invent stories, quotes, numbers or biography.
2. **Write the script as data.** One JSON file per lesson: a list of scenes, each with the narration text and a visual spec (layout name plus its data). Shared helpers keep the structure consistent.
3. **Write a facts file.** List the author's own statements the lesson may assert, and separately list every line the writer added, so the author can say yes or no to each.
4. **Independent review before narration.** A separate agent, on a different model where possible, reviews the script cold: facts beyond the source, names or identifiers, invented statistics, lines that try too hard, speech-tag problems, and whether the video's own examples pass its own rule. Fix the majors and repeat until none remain. Narration is the first step that costs anything, so review comes first.
5. **Narrate.** A small script sends each scene's text to a text-to-speech API in the author's cloned voice and caches one clip per scene, so editing one line only re-synthesizes that line. The API key is read from the environment or the OS keychain at the moment of use and is never written to a file, a log, a prompt or a command line.
6. **Render.** Frames are drawn in code (Python, Pillow, NumPy) at 1920x1080, 30 fps, and muxed with ffmpeg. Timing is derived from the measured length of each narration clip, so pictures can never drift from the words.
7. **Check stills and the runtime table.** Pull a few frames, read every on-screen string, confirm nothing is cut off and that quote cards are read aloud.
8. **Finish.** Normalize audio to about -16 LUFS, write chapter timestamps from the scene timings, save a poster frame and the final script next to the video.
9. **Publish.** Add the lesson to the static site and to the machine-readable index (`lessons.json`), push, wait for the deploy, and verify every URL returns 200.

## 2. Narration style

- Sound like a good university professor: engaging, concrete, warm. Never jokey, never forced.
- Expressive delivery: vary pace and weight with the meaning. Use only these tags: `[pause]`, `<emphasis>…</emphasis>`, `<slow>…</slow>`.
- **No laugh or chuckle tags.** They sound canned and get old fast.
- Second person, short sentences, contractions. No hype words.
- Budget about 2.6 words per second including pauses. Every first draft runs long; expect to cut a quarter, mostly lines that repeat what is already on screen.
- If a card shows a quote, the voice reads it aloud.

## 3. Lesson structure and layouts

- A title card is the first frame, so the poster and the first second already say what the lesson is.
- Hook, one real story, the mechanism (why it happens), a few more instances, the tell, the habit, one rule, one reply ask about the viewer's own work, and a short close.
- One palette with semantic colours: green for the right way or what was reported, amber for the gap or what was missed, greys for hierarchy, dark slate background.
- A library of named layouts (title, statement, split, checklist, timeline, rule card, quiz with reveal, diagram that persists across beats). Each new lesson should add or improve at least one layout so the bar keeps rising. Motion must mean something: a reveal is timed to the sentence that explains it.

## 4. The site: plain HTML done well

- Static files only: semantic HTML, one hand-written CSS file, one small vanilla script. No framework, no build step, no CDN, no web fonts, no analytics, no third-party scripts.
- One directory per page with an `index.html`, so URLs are clean and the site works on any static host.
- Native `<video>` and `<audio>` elements with posters, `preload="metadata"`, a download link, and chapter buttons that seek the player.
- Accessibility basics: skip link, landmarks, visible focus styles, alt text, good contrast, responsive layout, and `prefers-reduced-motion` respected by every animation.
- Animated teasers (a coming-soon series, a stick-figure videobook teaser) are SVG or canvas driven by a few lines of script and synced to the audio element's `currentTime`, with the captions taken verbatim from the narration script.
- A machine-readable index (`lessons.json`, `book.json`) next to the human pages, so other agents can load the lessons.
- An "AI-created" line in the footer of every page.

### Cookie patterns (first-party, no tracking)

- **Watched:** when a video passes about 90 percent or ends, add its id to a `watched` cookie (comma list). Series pages and the home page read it to paint check marks and "n of m watched" progress bars. Provide a reset button.
- **Listening bookmark:** every few seconds while playing, and on pause, store `track:seconds` pairs in a bookmark cookie; on load, offer "Resume from m:ss". Clear the bookmark when the track ends.
- Cookie attributes: `path=/`, `max-age` about one year, `SameSite=Lax`, `Secure` on https. Keep values tiny. Everything still plays without JavaScript.

## 5. Review process

1. The builder self-checks: every link and media path resolves, the HTML parses, cookies set and read back in a real browser, and nothing breaks with JavaScript off.
2. An independent reviewer reads the script or page cold with an explicit checklist and returns PASS or CHANGES NEEDED with major and minor items. The builder never grades its own work as the last word.
3. Personal material is published only with the author's explicit yes.
4. After deploy, fetch every URL and confirm HTTP 200; click through the home page links.
5. Keep what worked: each finished lesson leaves its script, review notes and stills beside the video, and the playbook is updated when a better approach wins.

## 6. How this page was chosen

Three builds of the same site, by three AI models, are compared side by side on the [comparison page](/compare/). The patterns above are the ones that held up best in that review.

## For agents

- This page: https://clarkhuang.github.io/playbook/index.md
- This folder’s agents file: https://clarkhuang.github.io/playbook/AGENTS.md
- Site index: https://clarkhuang.github.io/llms.txt
- Site agents: https://clarkhuang.github.io/AGENTS.md
