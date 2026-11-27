#!/usr/bin/env python3
"""Write the public Lesson 1 page from the scene script and install-prompt.md.

If the lesson MP4, captions, and poster are in the site tree, the page is a
full video lesson (player, chapters, duration, captions, VideoObject). If they
are not, the page stays a draft with no video element.

    python3 publish_page.py
"""
from __future__ import annotations

import html
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
SLUG = "01-size-the-model-run-the-first-endpoint"
PAGE = f"software-engineering-301/{SLUG}/index.html"
URL = "https://clarkhuang.github.io/software-engineering-301/" + SLUG + "/"
LESSON_ID = "se301/01"
VIDEO_NAME = "se301-01-size-the-model-run-the-first-endpoint.mp4"
CAPTIONS_NAME = "se301-01-size-the-model-run-the-first-endpoint.vtt"
POSTER_PATH = "/videos/posters/se301-01-size-the-model-run-the-first-endpoint.jpg"
VPATH = f"/videos/{VIDEO_NAME}"
SOURCE_URL = "https://github.com/clarkhuang/clarkhuang.github.io/tree/next-revision/lesson-sources/se301-01"
E = html.escape

SUMMARY = (
    "Before you download a local model, size it to the machine you have. "
    "The weight floor is the parameter count times the bits per weight, divided by eight. "
    "That number is weights only. Add the runtime, the operating system, your other programs, and a context cache. "
    "On the playbook's 48 GB laptop, the first fixture is Qwen2.5-Coder-7B-Instruct in a four-bit build. "
    "Larger names for the ordered 512 GB Studio are candidates, not measurements. "
    "Then run one local endpoint on loopback and keep the reply. A chat reply does not, by itself, prove tool calls. "
    "The page includes one copy-paste prompt for a Mac with Apple silicon and for a Windows or Linux PC. "
    "The agent stops for a named yes before an admin install, a firewall change, or a sign-in. "
    "It does not take secrets, and it does not send local files off the machine."
)
RULE = (
    "Before a model is downloaded, write three things where the agent can read them: "
    "the weight floor, the memory you can spare, and the check that says the endpoint answered. "
    "If a step needs admin rights, a firewall change, or a sign-in, stop and ask. "
    "Do not paste secrets, and do not send local files off the machine."
)
NOTES = [
    "The 40 GB, 160 GB, and 240 GB figures are weight floors from the playbook's formula. They are not measured file sizes.",
    "Qwen3-Coder-Next, GLM-5.3-Flash, DeepSeek-V4-Flash, and Qwen3-Coder-480B are the playbook's November candidates for the ordered Studio. Throughput, power, and usable context are not measured yet.",
    "The playbook's named machines are Apple silicon. The Windows and Linux path in the prompt applies the same weight floor, using LM Studio's headless docs or Ollama's local OpenAI-compatible API.",
    "The prompt's first request is one chat completion. The playbook's endpoint lab still asks for a stream, a cancelled request, and a structured tool call after that. A chat reply does not prove tool calls.",
    "gpt-oss-20b is a comparison only when it is already installed. The prompt does not download it.",
]
DRAFT_NOTE = (
    "The video is not rendered. The script and facts.md are waiting for Clark's review. "
    "Do not treat this page as a recording."
)


def transcript(spec, readable):
    blocks = []
    current = None
    buf = []

    def flush():
        if buf:
            blocks.append((current, " ".join(buf)))
            buf.clear()

    for scene in spec["scenes"]:
        chapter = scene.get("chapter") or ""
        if chapter != current:
            flush()
            current = chapter
        buf.append(readable(scene["text"]))
    flush()
    return blocks


SERIES_SUMMARY = (
    "Learn to run a local AI studio on hardware you own. "
    "Size the model to the machine you have, run one local endpoint, "
    "and measure a real job before you upgrade."
)


def site_root():
    return os.path.abspath(os.environ.get("SITE") or ROOT)


def media_paths():
    root = site_root()
    video = os.path.join(root, "videos", VIDEO_NAME)
    captions = os.path.join(root, "videos", CAPTIONS_NAME)
    poster = os.path.join(root, POSTER_PATH.lstrip("/"))
    return video, captions, poster


def media_ready():
    video, captions, poster = media_paths()
    return all(os.path.isfile(p) for p in (video, captions, poster))


def load_chapters():
    """Chapter list for the public player. The first title starts at 0.0, as other lessons do."""
    for path in (
        os.path.join(HERE, "chapters.json"),
        os.path.join(HERE, "build", "chapters.json"),
    ):
        if os.path.isfile(path):
            raw = json.load(open(path, encoding="utf-8"))
            seen = []
            out = []
            for row in raw:
                title = (row.get("title") or "").strip()
                if not title or title in seen:
                    continue
                seen.append(title)
                out.append([float(row["start_seconds"]), title])
            if out:
                out[0][0] = 0.0
            return out
    return []


def catalog_series(dur=None, dates=None, chapters=None):
    """A lessons.json series object for SE 301 Lesson 1, or None if media is missing."""
    if not media_ready():
        return None
    import gen
    import media_dates
    video_file, _, _ = media_paths()
    if dur is None:
        dur = gen.probe(video_file)
    if dates is None:
        dates = media_dates.dates_for(f"videos/{VIDEO_NAME}", repo=ROOT, site=site_root())
    if chapters is None:
        chapters = load_chapters()
    lesson = {
        "id": LESSON_ID,
        "number": 1,
        "title": "Size the model, then run the first endpoint",
        "status": "available",
        "summary": SUMMARY,
        "rule": RULE,
        "page_url": URL,
        "video_url": "https://clarkhuang.github.io" + VPATH,
        "poster_url": "https://clarkhuang.github.io" + POSTER_PATH,
        "markdown_url": URL + "index.md",
        "agents_url": URL + "AGENTS.md",
        "duration_seconds": round(dur, 1) if dur else None,
        **gen.catalog_dates(dates),
        "chapters": [{"start_seconds": round(t, 1), "title": c} for t, c in (chapters or [])],
        "captions_url": f"https://clarkhuang.github.io/videos/{CAPTIONS_NAME}",
        "source_url": SOURCE_URL,
    }
    return {
        "id": "se301",
        "title": "Software Engineering 301",
        "subtitle": "Run Your Own AI Studio",
        "page": "https://clarkhuang.github.io/software-engineering-301/",
        "markdown_url": "https://clarkhuang.github.io/software-engineering-301/index.md",
        "agents_url": "https://clarkhuang.github.io/software-engineering-301/AGENTS.md",
        "status": "in progress",
        "summary": SERIES_SUMMARY,
        "lessons": [lesson],
    }


def update_lessons_json(data=None, write=True):
    """Insert or replace the SE 301 series in lessons.json. Used by this script and by gen.py."""
    path = os.path.join(site_root(), "lessons.json")
    if data is None:
        data = json.load(open(path, encoding="utf-8"))
    series = catalog_series()
    if not series:
        return data
    data["series"] = [s for s in data.get("series", []) if s.get("id") != "se301"]
    ids = [s.get("id") for s in data["series"]]
    if "se201" in ids:
        data["series"].insert(ids.index("se201") + 1, series)
    else:
        data["series"].append(series)
    if write:
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(data, handle, indent=2, ensure_ascii=False)
            handle.write("\n")
    return data


def main():
    os.environ["SITE"] = ROOT
    sys.path.insert(0, os.path.join(ROOT, "sitegen"))
    sys.path.insert(0, HERE)
    import gen
    import make_vtt
    import media_dates

    spec = json.load(open(os.path.join(HERE, "se301-01-first-endpoint.json"), encoding="utf-8"))
    prompt = open(os.path.join(HERE, "install-prompt.md"), encoding="utf-8").read().strip() + "\n"
    blocks = transcript(spec, make_vtt.readable)
    has_video = media_ready()
    video_file, captions_file, poster_file = media_paths()
    chapters = load_chapters() if has_video else []
    dur = gen.probe(video_file) if has_video else None
    dates = media_dates.dates_for(f"videos/{VIDEO_NAME}", repo=ROOT, site=ROOT) if has_video else None
    notes = NOTES if has_video else [DRAFT_NOTE] + NOTES

    md = [
        "# Size the model, then run the first endpoint",
        "",
        "_Software Engineering 301 · Lesson 1_" + ("" if has_video else " · draft, video not rendered"),
        "",
        f"HTML page: {URL}",
        "",
        "The HTML version of this page has a “Use this page with your AI” box at the top. "
        "Copy the prompt below into ChatGPT, Claude, Grok, or any other chat tool:",
        "",
        f"> Read https://clarkhuang.github.io/llms.txt and {URL}index.md "
        f"(plus {URL}AGENTS.md). Summarize this page, then act as my guide to Clark Huang's site: "
        "list related lessons, answer my questions citing page URLs, and quiz me if I ask.",
        "",
        "- Series: [Software Engineering 301](https://clarkhuang.github.io/software-engineering-301/index.md)",
        "- Series agents file: [https://clarkhuang.github.io/software-engineering-301/AGENTS.md](https://clarkhuang.github.io/software-engineering-301/AGENTS.md)",
        "- Site index: [https://clarkhuang.github.io/llms.txt](https://clarkhuang.github.io/llms.txt)",
        f"- This folder’s agents file: [{URL}AGENTS.md]({URL}AGENTS.md)",
    ]
    if has_video:
        md += [f"- Video (MP4): https://clarkhuang.github.io{VPATH}"]
        if dur:
            md += [f"- Duration: {gen.mmss(dur)} ({round(dur, 1)} seconds)"]
        dline = media_dates.md_line(dates)
        if dline:
            md += [f"- {dline}"]
        md += [
            f"- Poster: https://clarkhuang.github.io{POSTER_PATH}",
            f"- Captions (WebVTT): https://clarkhuang.github.io/videos/{CAPTIONS_NAME}",
            f"- How it was built (script source, facts, install prompt): {SOURCE_URL}",
            "",
            "## Chapters",
            "",
        ]
        for t, title in chapters:
            md.append(f"- [{gen.mmss(t)}] {title}")
    else:
        md += [
            "- Video: not rendered. Narration waits on approval of the script and facts file.",
            "- How it was built (script source, facts, install prompt): "
            f"{SOURCE_URL}",
            "",
            "## Planned chapters",
            "",
            "These are the chapter titles in the scene script. There is no video to seek yet.",
            "",
        ]
        for title, _text in blocks:
            if title:
                md.append(f"- {title}")
    md += [
        "",
        "## The lesson",
        "",
        SUMMARY,
        "",
        "## The rule",
        "",
        RULE,
        "",
        "This rule is written so an AI agent can follow it as a standing instruction.",
        "",
        f"## {'What this lesson does not claim' if has_video else 'What this draft does not claim'}",
        "",
    ]
    for note in notes:
        md.append(f"- {note}")
    md += ["", "## On-screen summary of the install prompt", ""]
    md.append("The prompt, pasted into a computer-use or terminal agent, does five things:")
    md.append("")
    steps_scene = next(s for s in spec["scenes"] if s["visual"] == "steps")
    for step in steps_scene["data"]["steps"]:
        md.append(f"{step[0]}. **{step[1]}.** {step[2]}")
    md += [
        "",
        "It waits for a named yes before an admin install, a firewall change, or a sign-in. "
        "Silence is not a yes. It does not take secrets, and it does not send local files off the machine.",
        "",
        "## Copy-paste install prompt",
        "",
        "The same text is in `lesson-sources/se301-01/install-prompt.md`. Paste it as a whole.",
        "",
        prompt.rstrip(),
        "",
        "## Transcript",
        "",
        "This is the script, with text-to-speech spellings made readable."
        + (" It matches the captions." if has_video else " It has not been narrated."),
        "",
    ]
    for title, text in blocks:
        if title:
            md += [f"### {title}", ""]
        md += [text, ""]
    md += [
        "## Related",
        "",
        "- Playbook: [Software Engineering 301](https://clarkhuang.github.io/software-engineering-301/index.md)",
        "- Sizing lab on that page: [Size the model before downloading it](https://clarkhuang.github.io/software-engineering-301/index.md#1-size-the-model-before-downloading-it)",
        "- Endpoint lab: [Build the first endpoint](https://clarkhuang.github.io/software-engineering-301/index.md#2-build-the-first-endpoint)",
        "- Next lab in the playbook: [Put a router in front of the models](https://clarkhuang.github.io/software-engineering-301/index.md#3-put-a-router-in-front-of-the-models)",
        "- [Don't Paste Secrets](https://clarkhuang.github.io/ai-tips/17-dont-paste-secrets/index.md)",
        "",
        "## For agents",
        "",
        f"Read [AGENTS.md]({URL}AGENTS.md) in this folder, "
        "[https://clarkhuang.github.io/software-engineering-301/AGENTS.md](https://clarkhuang.github.io/software-engineering-301/AGENTS.md) "
        "for the series, and [https://clarkhuang.github.io/llms.txt](https://clarkhuang.github.io/llms.txt) for the whole site.",
        "",
    ]
    page_dir = os.path.join(ROOT, "software-engineering-301", SLUG)
    os.makedirs(page_dir, exist_ok=True)
    open(os.path.join(page_dir, "index.md"), "w", encoding="utf-8").write("\n".join(md))

    agents_intro = (
        "This folder is the public lesson “Size the model, then run the first endpoint” on Clark Huang’s learning site."
        if has_video
        else "This folder is the public draft of “Size the model, then run the first endpoint” on Clark Huang’s learning site. The video is not rendered."
    )
    agents = f"""# AGENTS.md — Software Engineering 301, lesson 1: Size the model, then run the first endpoint

{agents_intro}

- HTML: {URL}
- Markdown twin (summary, rule, transcript, install prompt): {URL}index.md
- This file: {URL}AGENTS.md
- Series index: https://clarkhuang.github.io/software-engineering-301/index.md
- Series agents: https://clarkhuang.github.io/software-engineering-301/AGENTS.md
- Site index: https://clarkhuang.github.io/llms.txt
- Site agents: https://clarkhuang.github.io/AGENTS.md
- Build source, facts, and the canonical prompt file: {SOURCE_URL}

Read `index.md` in this folder for the lesson. Treat the rule below as a standing instruction. Do not invent stories, quotes, numbers, or biography about Clark Huang. Do not present the Studio model names as measured results. Cite page URLs when you answer questions.

The HTML version of this page has a “Use this page with your AI” box at the top. Copy the prompt below into ChatGPT, Claude, Grok, or any other chat tool:

> Read https://clarkhuang.github.io/llms.txt and {URL}index.md (plus {URL}AGENTS.md). Summarize this page, then act as my guide to Clark Huang's site: list related lessons, answer my questions citing page URLs, and quiz me if I ask.

## The rule

{RULE}

## Copy-paste install prompt

Paste this into a computer-use or terminal agent on the machine where the model should run. Do not weaken the stops.

{prompt}"""
    open(os.path.join(page_dir, "AGENTS.md"), "w", encoding="utf-8").write(agents)

    steps = "".join(
        f"<li><strong>{E(title)}.</strong> {E(sub)}</li>"
        for _n, title, sub in steps_scene["data"]["steps"]
    )
    notes_html = "".join(f"<li>{E(note)}</li>" for note in notes)
    trans = []
    for title, text in blocks:
        if title:
            trans.append(f"          <h3>{E(title)}</h3>")
        trans.append(f"          <p>{E(text)}</p>")
    transcript_html = "\n".join(trans)
    prompt_html = E(prompt.rstrip())
    notes_heading = "What this lesson does not claim" if has_video else "What this draft does not claim"
    vld = None

    if has_video:
        if chapters:
            chh = (
                '<h2 class="label">Chapters</h2><ol class="chapters">'
                + "".join(
                    f'<li><a href="{VPATH}#t={t:.1f}" data-seek="{t:.1f}" data-target="lesson-video">'
                    f'<span class="ts">{gen.mmss(t)}</span><span>{E(c)}</span></a></li>'
                    for t, c in chapters
                )
                + '</ol><p class="chapter-hint">Select a chapter to jump there in the video.</p>'
            )
        else:
            chh = '<h2 class="label">Length</h2><p class="muted">One short lesson.</p>'
        dur_txt = gen.mmss(dur) if dur else ""
        dur_meta = f'<span><time datetime="{gen.iso_dur(dur)}">{dur_txt}</time></span><span aria-hidden="true">·</span>' if dur else ""
        date_meta = (
            f'<span class="dates" {media_dates.attrs(dates)}>{media_dates.label_html(dates)}</span><span aria-hidden="true">·</span>'
            if dates else media_dates.NEW_BADGE
        )
        body = f"""      <p class="crumbs"><a href="/">Home</a> / <a href="/software-engineering-301/">Software Engineering 301</a> / Lesson 1</p>
      <h1>Size the model, then run the first endpoint</h1>
      <div class="player"><video id="lesson-video" controls preload="metadata" playsinline width="1280" height="720" poster="{POSTER_PATH}" data-lesson-id="{LESSON_ID}" aria-label="Lesson video: Size the model, then run the first endpoint">
        <source src="{VPATH}" type="video/mp4">
        <track kind="captions" srclang="en" label="English" src="/videos/{CAPTIONS_NAME}" default>
        Your browser can't play this video. <a href="{VPATH}">Download the MP4</a>.
      </video></div>
      <div class="lesson-meta" data-watch-id="{LESSON_ID}" data-status-scope>{dur_meta}{date_meta}<span>Narrated in Clark's AI voice</span><span aria-hidden="true">·</span><a href="{VPATH}" download>Download MP4</a><span aria-hidden="true">·</span><a href="/videos/{CAPTIONS_NAME}">Captions (VTT)</a><span aria-hidden="true">·</span><a href="{SOURCE_URL}">How it was built</a>{gen.watch_state(LESSON_ID)}<span class="status" role="status" data-status></span></div>
      <p class="resume" data-resume="lesson-video" hidden><button type="button" class="btn" data-go>Resume</button><button type="button" class="linkish" data-dismiss>Start from the beginning</button></p>
      <p class="upnext-after">Next in the playbook: <a href="/software-engineering-301/#3-put-a-router-in-front-of-the-models">Put a router in front of the models</a>. <a href="/software-engineering-301/">Back to Software Engineering 301</a></p>
      <div class="grid2">
        <section>
          <h2 class="label">The lesson</h2>
          <p>{E(SUMMARY)}</p>
          <div class="rulecard" data-status-scope><p class="label">The rule · for your agents</p><p id="rule-se301-01">{E(RULE)}</p><p class="tools"><button type="button" class="btn ghost" data-copy="rule-se301-01" hidden>Copy rule</button><span class="status" role="status" data-status></span></p></div>
          <h2 class="label notes-label">{E(notes_heading)}</h2>
          <ul class="notes">{notes_html}</ul>
        </section>
        <aside>{chh}</aside>
      </div>
      <h2 id="install-prompt">Copy-paste install prompt</h2>
      <p>For a computer-use agent or a terminal agent, on a Mac with Apple silicon or on a Windows or Linux PC. On screen, and here, the prompt does five things:</p>
      <ol>{steps}</ol>
      <p>It waits for a named yes before an admin install, a firewall change, or a sign-in. Silence is not a yes. It does not take secrets, and it does not send local files off the machine.</p>
      <div class="prompt-box" data-status-scope>
        <pre id="install-prompt-text" tabindex="0">{prompt_html}</pre>
        <p class="tools"><button type="button" class="btn ghost" data-copy="install-prompt-text" hidden>Copy prompt</button><span class="status" role="status" data-status></span></p>
      </div>
      <h2>Related</h2>
      <ul>
        <li><a href="/software-engineering-301/">Software Engineering 301 playbook</a></li>
        <li><a href="/software-engineering-301/#1-size-the-model-before-downloading-it">Size the model before downloading it</a></li>
        <li><a href="/software-engineering-301/#2-build-the-first-endpoint">Build the first endpoint</a></li>
        <li><a href="/software-engineering-301/#3-put-a-router-in-front-of-the-models">Put a router in front of the models</a></li>
        <li><a href="/ai-tips/17-dont-paste-secrets/">Don't Paste Secrets</a></li>
      </ul>
      <nav class="pager" aria-label="Lesson navigation"><a class="prev" href="/software-engineering-301/"><small>Back</small>All Software Engineering 301 labs</a><a class="next" href="/software-engineering-301/#3-put-a-router-in-front-of-the-models"><small>Next</small>Put a router in front of the models</a></nav>
      <h2>Transcript</h2>
      <p class="muted">The script, with text-to-speech spellings made readable. It matches the captions.</p>
{transcript_html}
"""
        vld = gen.video_ld(
            "Size the model, then run the first endpoint",
            SUMMARY[:155],
            VPATH,
            POSTER_PATH,
            dur,
            dates,
            captions=f"/videos/{CAPTIONS_NAME}",
        )
    else:
        chapters_html = "".join(f"<li>{E(title)}</li>" for title, _text in blocks if title)
        body = f"""      <p class="crumbs"><a href="/">Home</a> / <a href="/software-engineering-301/">Software Engineering 301</a> / Lesson 1</p>
      <h1>Size the model, then run the first endpoint <span class="badge soon">Draft</span></h1>
      <div class="placeholder"><div><strong>Video not rendered</strong>The script and the facts file are ready for review. Narration runs after that review. This page is the lesson a reader can follow without the video.</div></div>
      <div class="grid2" style="margin-top:34px">
        <section>
          <h2 class="label">The lesson</h2>
          <p>{E(SUMMARY)}</p>
          <div class="rulecard" data-status-scope><p class="label">The rule · for your agents</p><p id="rule-se301-01">{E(RULE)}</p><p class="tools"><button type="button" class="btn ghost" data-copy="rule-se301-01" hidden>Copy rule</button><span class="status" role="status" data-status></span></p></div>
          <h2>What this draft does not claim</h2>
          <ul>{notes_html}</ul>
        </section>
        <aside>
          <h2 class="label">Planned chapters</h2>
          <ol class="chapters">{chapters_html}</ol>
          <p class="chapter-hint">No video to seek yet. The titles are the scene script's chapters.</p>
          <p><a href="/software-engineering-301/">Back to the playbook</a></p>
          <p><a href="{SOURCE_URL}">How it was built</a></p>
        </aside>
      </div>
      <h2 id="install-prompt">Copy-paste install prompt</h2>
      <p>For a computer-use agent or a terminal agent, on a Mac with Apple silicon or on a Windows or Linux PC. On screen, and here, the prompt does five things:</p>
      <ol>{steps}</ol>
      <p>It waits for a named yes before an admin install, a firewall change, or a sign-in. Silence is not a yes. It does not take secrets, and it does not send local files off the machine.</p>
      <div class="prompt-box" data-status-scope>
        <pre id="install-prompt-text" tabindex="0">{prompt_html}</pre>
        <p class="tools"><button type="button" class="btn ghost" data-copy="install-prompt-text" hidden>Copy prompt</button><span class="status" role="status" data-status></span></p>
      </div>
      <h2>Related</h2>
      <ul>
        <li><a href="/software-engineering-301/">Software Engineering 301 playbook</a></li>
        <li><a href="/software-engineering-301/#1-size-the-model-before-downloading-it">Size the model before downloading it</a></li>
        <li><a href="/software-engineering-301/#2-build-the-first-endpoint">Build the first endpoint</a></li>
        <li><a href="/software-engineering-301/#3-put-a-router-in-front-of-the-models">Put a router in front of the models</a></li>
        <li><a href="/ai-tips/17-dont-paste-secrets/">Don't Paste Secrets</a></li>
      </ul>
      <h2>Transcript</h2>
      <p class="muted">The script, with text-to-speech spellings made readable. It has not been narrated.</p>
{transcript_html}
"""

    desc = SUMMARY[:155]
    gen.page(
        PAGE,
        "Size the model, then run the first endpoint — Software Engineering 301 — Clark Huang",
        desc,
        body,
        "software-engineering-301",
        main_class="lesson",
        video=vld,
    )
    if has_video:
        update_lessons_json()
        print("updated lessons.json with se301/01")
    print("wrote", PAGE, "with video" if has_video else "as draft")


if __name__ == "__main__":
    main()
