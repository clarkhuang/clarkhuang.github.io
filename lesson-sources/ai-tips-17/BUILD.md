# How AI Tips lesson 17 was built

Lesson: **Don't Paste Secrets** — AI Tips, lesson 17.
Page: https://clarkhuang.github.io/ai-tips/17-dont-paste-secrets/

This folder is the source for the lesson video, so a person or an agent can read, check, change, and rebuild it.

| File | What it is |
|---|---|
| `ai-tip-17.json` | The scene script the narrator and renderer read. |
| `make_vtt.py` | Writes the WebVTT captions from the scene script and the render timeline. |
| `render-timeline.log` | Scene start times and lengths from the render (used for chapters and captions). |
| `facts.md` | Every factual claim in the lesson, spoken or on screen, with its source. The teaching example is marked as made up. |
| `brief.md` | The brief the lesson was written from. |
| `notes.md` | Why this tip, how it differs from earlier lessons, and post-review wording changes. |
| `review.md` | Independent review by Claude Code (model `claude-fable-5-2`) and the majors that were fixed. |

The renderer is the existing AI Tips `render.py` on the build machine (layouts used: `title`, `terminal_mock`, `statement`, `timeline`, `split`, `rule`, `outro`). No new layout file was added.

```bash
# On the build machine, with XAI_API_KEY in the environment only:
python3 narrate.py --script scripts/ai-tip-17.json
python3 render.py --script scripts/ai-tip-17.json
# then loudness-normalize to about -16 LUFS with a limiter (true peak <= -1 dBTP),
# write the poster, and:
python3 make_vtt.py ai-tip-17.json render-timeline.log /path/to/site/videos/ai-tips-17-dont-paste-secrets.vtt
SITE=/path/to/site-checkout python3 sitegen/gen.py
python3 sitegen/check_site.py .
```

- Voice: xAI custom voice `4lbl0krw73vf`, speed 1.05. Speech tags used: `[pause]`, `<emphasis>`. No laugh or chuckle tags.
- The xAI API key is read from the `XAI_API_KEY` environment variable at call time. It is never written to a file, a log, or a command line.
- Audio: loudness-normalized to -16.0 LUFS integrated, true peak -1.6 dBTP, AAC 128 kbps. Video: H.264, `+faststart`. Length 1:33 (93.0 s).
- The script was reviewed by Claude Code (model `claude-fable-5-2`) before narration. The deploy example is a generic illustration, not a story about Clark or a real company.
