# Claims in Lesson 3 about this site and its build, and where to check them

Paths starting `sitegen/` or `.github/` are in the site repository. Paths starting `pipeline/` are in the video build directory (`/workspace/legacy/build/se101/pipeline` on the build machine). Times are the files' modification times on the build machine, US Eastern, Nov 21, 2026.

## Checked

| Claim in the lesson | Where it is true |
|---|---|
| Lessons 3, 4 and 5 of Software Engineering 101 were built at the same time | `pipeline/scripts/se101-03.json`, `-04.json`, `-05.json` were all written at 20:44:30. The first narration clip of each (`pipeline/audio/se101-0N/01_title.mp3`) was written at 20:44:31. Within each folder the clips land in order while the three folders fill side by side. |
| Three scripts | `pipeline/make_se101_03.py`, `_04.py`, `_05.py` and the three script JSON files |
| The three finished videos landed within forty seconds of each other | Final MP4s in `/workspace/legacy/build/se101/`: lesson 5 at 20:46:32.4, lesson 3 at 20:46:36.1, lesson 4 at 20:47:10.0. Spread: 37.6 s. These are the times the finished files (after the loudness pass) were written. |
| On screen: "done 8:46:36 pm", "8:47:10 pm", "8:46:32 pm" | The same three timestamps |
| The contract already existed: the same script format the first two lessons used | `pipeline/scripts/se101-01.json` to `-05.json` have the same top-level keys (`id`, `title`, `output`, `voice`, `language`, `speed`, `scenes`) and the same scene keys (`id`, `text`, `visual`, `chapter`, `data`); lesson 4 also uses the optional `group` |
| ...and the same page fields | In `sitegen/content.json`, the entries for Software Engineering 101 lessons 1 to 5 have the same keys: `n`, `slug`, `id`, `title`, `summary`, `rule`, `video`, `script`, `log` |
| One content file, read by one generator | All three lessons are entries in `sitegen/content.json`; `sitegen/gen.py` builds their pages from it |
| Today: one check that walks the whole site: every link, and every file a page points to | `sitegen/check_site.py SITE_DIR` checks, for every HTML page, that internal `href`, `src` and `poster` targets exist, that `#fragment` ids exist, that tags balance and ids are unique; it exits 1 on any error |
| Today: a pull request to staging, for me to approve | `REBUILD.md` and `AGENTS.md`: pull requests target `next-revision` (published at `/staging/`); only Clark merges `next-revision` into `main` |
| This lesson and the one before it were drafted in parallel | The two scripts, `pipeline/make_se201_02.py` and `make_se201_03.py`, were drafted in one working session and previewed through the same renderer |

## Resolved before recording (reviewed by LegacyBot)

- "Each with its own independent review" was removed: no review output survives, so it can't be shown. Scene 6 now says "Three scripts, three renders, running side by side", which the render logs show (`/workspace/legacy/build/logs/r03.log`, `r04.log`, `r05.log`, written 20:46 to 20:47) and the MP4 timestamps above.
- Lessons 3 to 5 shipped to the site together in one commit, `c55caba` ("SE 101 lessons 3-10 and SE 201 lesson 1"), before staging and `check_site.py` existed (`check_site.py` and the staging deploy were added in `34e1f86` on Nov 22). So scene 7 says they "shipped together, in one change", and presents the whole-site check and the pull request to staging as "today" gates; the on-screen label says "plus today's gates" and "Today: whole-site check".

## Found while checking

`lesson-sources/se201-01/facts.md` lists `sitegen/check_site.py` in the row "Checks run on every deploy". `deploy-pages.yml` runs its own checks (staging `noindex`, `robots.txt`, sitemap and `llms.txt` not listing `/staging/`) and does not call `check_site.py`.

## Not claims about a specific system

The quiz; the "picture a team" scene (screen, service, database), labelled as such on screen and in the narration; the three things (contract, merge point, whole-system test); the bars, labelled "an illustration, not a measurement"; the recap; the rule; the reply ask.
