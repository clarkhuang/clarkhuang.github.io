# How Software Engineering 201, Lesson 2 was built

Lesson: **Build the Whole System, AI-Native** — Software Engineering 201: From Loop to Enterprise Systems.
Page: https://clarkhuang.github.io/software-engineering-201/02-build-the-whole-system-ai-native/

This folder is the source for the lesson video, so a person or an agent can read, check, change, and rebuild it.

| File | What it is |
|---|---|
| `make_se201_02_ai_native.py` | The script source: narration text and the on-screen visual spec for every scene. Edit this, not the JSON. |
| `se201-02-ai-native.json` | The generated scene script that the narrator and renderer read. |
| `finish_se201.sh` | The finish step: loudness, faststart MP4, poster, captions, and the copy into a site checkout. Takes arguments, so one script serves every Software Engineering 201 lesson. |
| `make_vtt.py` | Writes the WebVTT captions from the scene script and the render timeline. |
| `render-timeline.log` | Scene start times and lengths from the render (used for chapters and captions). |
| `facts.md` | Every claim the lesson makes about this site, with where to check it in the repo. |
| `brief.md` | The brief (prompt) the lesson was written from. |

## Renumbered

This lesson was lesson 1 until “Four Eras of Building Systems” became Software Engineering 201, Lesson 1 (November 2026). It was re-rendered for the new numbering, and only the title, rule and closing clips (`01_title`, `12_rule` and `14_close`) were re-narrated, to say the new lesson numbers. The path list in `11_path` also gained “Four eras of building systems” as row 1 (on screen only; no narration change). The rest of the narration and every other scene are unchanged. The new video is `videos/se201-02-build-the-whole-system-ai-native.mp4`; the old page `/software-engineering-201/01-build-the-whole-system-ai-native/` redirects to `/software-engineering-201/02-build-the-whole-system-ai-native/`. `brief.md`, `facts.md` and the review files were written when this was lesson 1, so they use the old lesson numbers, folder names (`lesson-sources/se201-01/` and so on) and script names; they are kept as written. The old generator and scene script are in the git history.

## Re-narrated on Nov 23, 2026

Scene `11_path` was re-narrated and the lesson re-rendered on Nov 23, 2026, because the series grew from nine lessons to ten. The path on screen now lists ten lessons, with “Capstone: one feature, end to end” as the last row, and rows 2 and 3 now use the lesson titles (“Build the whole system, AI-native” and “Decompose the system into a graph”). The narration ends “Then, agents that operate enterprise systems, with real permissions, and a full audit trail. And last, a capstone: one feature, built end to end.” instead of “And finally, agents that operate enterprise systems, with real permissions, and a full audit trail.” No other scene's narration changed. The scene is about 4.6 seconds longer, so every chapter after “The path” starts later and the video is now 3:58 (238.9 s). The generator, the scene script, the render timeline, the captions and the video in this repository all carry the new line; the brief and the facts file are kept as written, so they describe the earlier path. `make_vtt.py` here is now the same copy the other Software Engineering 201 lessons use.

## Rebuild

The renderer is the same one used for every Software Engineering 101 and 201 video (`render_se101.py` on top of the AI Tips `render.py`). It lives on the build machine, not in this repository.

```bash
python3 make_se201_02_ai_native.py                                  # writes scripts/se201-02-ai-native.json
python3 narrate.py --script scripts/se201-02-ai-native.json   # xAI text-to-speech, Clark's voice, speed 1.05
SE_SERIES="SOFTWARE ENGINEERING 201" python3 render_se101.py --script scripts/se201-02-ai-native.json > ../../logs/s201_02_ainative.log
# finish_se201.sh <lesson-folder> <video-file> <name> <render-log> <scene-script> <site-checkout>
./finish_se201.sh 02-build-the-whole-system-ai-native SE201_02_Build-The-Whole-System-AI-Native_public.mp4 \
  se201-02-build-the-whole-system-ai-native ../../logs/s201_02_ainative.log scripts/se201-02-ai-native.json /path/to/site-checkout
python3 sitegen/stamp_versions.py                         # from the site checkout: new media version for watched state
SITE="$PWD" python3 sitegen/gen.py                        # pages, twins, llms.txt, lessons.json
```

`REBUILD.md` in the site root says how to run the generator without rewriting other sections' pages.

- Voice: xAI custom voice `4lbl0krw73vf`, speed 1.05. Speech tags used: `[pause]`, `<emphasis>`. No laugh or chuckle tags.
- The xAI API key is read from the `XAI_API_KEY` environment variable at call time. It is never written to a file, a log, or a command line.
- Audio: loudness-normalized to about -16 LUFS integrated, AAC 160 kbps. Video: 1920×1080 H.264, `+faststart`. Length 3:58 (238.9 s).
- Captions: `videos/se201-02-build-the-whole-system-ai-native.vtt`. The transcript is in the lesson's `index.md`, with the text-to-speech spellings made readable the same way `make_vtt.py` does for the captions.
- Review: the script was checked line by line against `facts.md`. It was not reviewed by Clark before it went to staging; it ships to production only when he merges.
