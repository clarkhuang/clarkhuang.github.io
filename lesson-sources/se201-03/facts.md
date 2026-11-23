# Claims in Lesson 2 about this site and its build, and where to check them

Paths starting `sitegen/`, `.github/`, `lesson-sources/` or a section folder are in the site repository. Paths starting `pipeline/` are in the video build directory (`/workspace/legacy/build/se101/pipeline` on the build machine); for Lesson 1 the same files are copied into `lesson-sources/se201-01/`.

| Claim in the lesson | Where it is true |
|---|---|
| The site has four parts: AI Tips, Software Engineering 101, Software Engineering 201, the book | `AGENTS.md` ("What is here"); folders `ai-tips/`, `software-engineering-101/`, `software-engineering-201/`, `book/` |
| Each part has its own folder and its own pages | The four folders above, each with its own `index.html` and `index.md` |
| A new lesson in one part needs nothing from the others | `sitegen/content.json` has one separate key per series (`ai-tips`, `software-engineering-101`, `software-engineering-201`); the book is built by `build_book()` in `sitegen/gen.py` from its own text |
| All four are built by one generator | `sitegen/gen.py` builds the three series from `sitegen/content.json` and the book through `build_book()` |
| ...with one stylesheet | `sitegen/gen.py` copies `sitegen/site.css` to `/styles.css`, and its `page()` template links `/styles.css` on every page |
| Change the shared node and everything moves | Follows from the two rows above: every page comes out of `gen.py` and links `/styles.css` |
| The narration clips need the script | `pipeline/narrate.py` reads the script JSON and writes `audio/<id>/<scene_id>.mp3`, one clip per scene |
| The render needs those clips, because the length of the audio sets the timing | `build_timeline` in `pipeline/render.py` runs `ffprobe` on every scene's clip; each scene lasts its clip plus a 0.38 s gap |
| Captions need the timeline the render writes out | `pipeline/make_vtt.py` takes the script JSON and the render log and reads each scene's start and length from the log; `lesson-sources/se201-01/render-timeline.log` is one such log |
| Captions need only the timeline | Same file: `make_vtt.py` does not open the MP4 |
| The sound level and the poster need only the video | `pipeline/finish_se201_01.sh`: the loudness passes and the poster frame both take the rendered MP4 as their only input |
| Nothing crosses between captions and sound level/poster | Same script: neither step reads the other's output |
| The build script happens to run them one after the other | `pipeline/finish_se201_01.sh` runs loudness, then poster, then captions, in sequence |
| The page needs all of it | A lesson entry in `sitegen/content.json` points at the video, the script and the log; `gen.py` reads the transcript from the script and the chapters from the log, and warns if the poster is missing |
| ...before a pull request to staging | `REBUILD.md` and `AGENTS.md`: agent pull requests target `next-revision`, published at `/staging/` |
| Only I merge to production | `REBUILD.md` and `AGENTS.md`: only Clark merges `next-revision` into `main` |

## Differences from the brief's list of facts

- The brief said the sections share `sitegen/content.json`. The book is not in that file, so the lesson says the four parts share one generator and one stylesheet, and does not say they share one content file.
- The brief said captions need the render timeline as part of a single "finish" step. In the code, captions and the sound-level/poster work are independent of each other after the render. The lesson uses that fork.

## Not claims about a specific system

The quiz, the dinner example, the loop and the graph, the bars (labelled "an illustration"), the enterprise picture (orders, billing, shipping, support, customer data; labelled "picture an enterprise system"), the four moves, the rule, and the reply ask.

The line "the longest chain sets the minimum" is the standard critical-path result for any dependency graph.
