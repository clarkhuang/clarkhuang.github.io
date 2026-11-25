#!/usr/bin/env python3
"""Markdown twins, AGENTS.md, llms.txt, and the 'Use this page with your AI' panel.

Imported by gen.py and gen_extra.py. No secrets, no network.
"""
import html, json, os, re

BASE = "https://clarkhuang.github.io"
E = html.escape


def _book_chapters():
    import importlib
    return importlib.import_module("book_chapters")


def _chapters_twin_section(site):
    bc = _book_chapters()
    chs = bc.load_chapters(site)
    if not chs:
        return []
    c0 = chs[-1]
    out = ["## New: a finished chapter", "",
           f"Chapter {c0['n']}, **{c0['title']}: {c0.get('subtitle') or ''}**, is finished as a v0 draft, with the full text, a videobook of the whole chapter, an audio track, captions and a transcript.", ""]
    if c0.get("thesis"):
        out += [f"> “{c0['thesis']}” — {c0.get('thesis_by') or 'Clark Huang'} (his belief, not a measured result)", ""]
    out += [c0.get("preview") or c0["summary"], ""]
    try:
        m = bc.media(site, c0)
        if m.get("vpath"):
            out += [f"- Video: {BASE}{m['vpath']}"]
    except Exception:
        pass
    out += [f"- Read it: {BASE}{c0['_url']}index.md"]
    if c0.get("_feat_text"):
        out += [f"- Includes “{c0['_feat_title']}”, adapted from Greg Glassman's “World-Class Fitness in 100 Words”, and a prompt to score your company against it."]
    out += [""]
    if len(chs) > 1:
        out += ["Other chapters you can read now:", ""]
        for ch in chs[:-1]:
            out.append(f"- [Chapter {ch['n']}: {ch['title']}]({BASE}{ch['_url']}index.md) ({ch.get('part')}): {ch['summary']}")
        out += [""]
    out += [f"All of them: {BASE}/book/chapters/index.md", ""]
    return out


def _chapter_llms_lines(site):
    """llms.txt lines for book chapters that can be read now (book-source/chapters/*/chapter.json)."""
    try:
        return _book_chapters().llms_lines(site)
    except Exception:
        return []

def dir_of(path):
    """Return the site-relative directory for a generated page, always ending in / except at root ('')."""
    path = path.replace("\\", "/").lstrip("/")
    if path.endswith("/index.html") or path == "index.html":
        d = path[:-10]  # drop index.html, may be empty
    elif path.endswith(".html"):
        d = os.path.dirname(path)
        d = (d + "/") if d else ""
    else:
        d = path if path.endswith("/") else path + "/"
    return d

def urls(path):
    d = dir_of(path)
    page = f"{BASE}/" if d == "" else f"{BASE}/{d}"
    md = f"{BASE}/index.md" if d == "" else f"{BASE}/{d}index.md"
    agents = f"{BASE}/AGENTS.md" if d == "" else f"{BASE}/{d}AGENTS.md"
    parent_agents = f"{BASE}/AGENTS.md" if d.count("/") <= 1 else f"{BASE}/{'/'.join(d.strip('/').split('/')[:-1])}/AGENTS.md"
    return {
        "dir": d,
        "page": page,
        "md": md,
        "agents": agents,
        "parent_agents": parent_agents,
        "llms": f"{BASE}/llms.txt",
        "llms_full": f"{BASE}/llms-full.txt",
        "lessons_json": f"{BASE}/lessons.json",
        "book_json": f"{BASE}/book.json",
        "rel_md": "index.md",
        "rel_agents": "AGENTS.md",
        "rel_llms": "/llms.txt",
        "rel_llms_full": "/llms-full.txt",
        "rel_root_agents": "/AGENTS.md",
        "rel_rebuild": "/REBUILD.md",
    }

def prompt_for(path):
    u = urls(path)
    extra = ""
    if path.startswith("book/chapters/") and path != "book/chapters/index.html":
        src = f"{BASE}/book-source/chapters/{path.split('/')[2]}/"
        extra = (
            f" Also read the chapter's transcript at {src}transcript.md and {BASE}/book.json. "
            "Cite section headings or video timestamps. This chapter is nonfiction: Clark Huang's views, with the sources it lists. "
            "Then help me apply it to my own team, and do not invent facts about my team; ask."
        )
    elif path.startswith("book/"):
        extra = (
            f" Also read {BASE}/llms-full.txt, {BASE}/book.json, and the preview transcript at "
            f"{BASE}/book-source/preview/transcript.md. Cite chapter titles or timestamps. "
            "Charlie Hack is the fictional narrator; Clark Huang is the author. "
            "Do not identify real people or companies behind the fictional names."
        )
    return (f"Read {u['llms']} and {u['md']} (plus {u['agents']}). "
            "Summarize this page, then act as my guide to Clark Huang's site: "
            "list related lessons, answer my questions citing page URLs, and quiz me if I ask."
            + extra)

def md_prompt_blurb(path):
    return (
        "The HTML version of this page has a “Use this page with your AI” box at the top. "
        "Copy the prompt below into ChatGPT, Claude, Grok, or any other chat tool:\n\n"
        f"> {prompt_for(path)}\n"
    )

def panel_html(path):
    u = urls(path)
    prompt = prompt_for(path)
    return f'''      <details class="ai-use">
        <summary>Use this page with your AI</summary>
        <div class="ai-use-body">
          <p>Copy the prompt below and paste it into ChatGPT, Claude, Grok, or any other chat tool. It points the tool at this page’s Markdown twin and at the site index, so it can read the material without browsing.</p>
          <div class="ai-prompt" data-status-scope>
            <pre id="ai-prompt-text" tabindex="0">{E(prompt)}</pre>
            <p class="tools"><button type="button" class="btn ghost" data-copy="ai-prompt-text" hidden>Copy prompt</button><span class="status" role="status" data-status></span></p>
          </div>
          <p class="ai-use-links">Machine-readable: <a href="{u['rel_md']}">this page in Markdown</a> · <a href="{u['rel_agents']}">AGENTS.md</a> · <a href="{u['rel_llms']}">llms.txt</a> · <a href="{u['rel_llms_full']}">llms-full.txt</a></p>
        </div>
      </details>
'''

def head_links():
    return ('  <link rel="alternate" type="text/markdown" href="index.md" title="Markdown version of this page">\n'
            '  <link rel="help" href="AGENTS.md" title="Instructions for AI agents">\n')

def footer_twins():
    return ('        <nav class="footer-col md-twin" aria-label="For your AI"><p class="footer-h">For your AI</p>'
            '<a href="index.md">index.md</a><a href="AGENTS.md">AGENTS.md</a><a href="/llms.txt">llms.txt</a>'
            '<a href="/llms-full.txt">llms-full.txt</a></nav>\n')

def write(site, rel, text):
    full = os.path.join(site, rel)
    os.makedirs(os.path.dirname(full) or site, exist_ok=True)
    if not text.endswith("\n"):
        text += "\n"
    open(full, "w").write(text)
    return full

def spoken(text):
    t = re.sub(r"</?(?:emphasis|slow)>", "", text or "")
    t = re.sub(r"\[(?:pause|chuckle|laugh)\]", " ", t)
    return re.sub(r"\s+", " ", t).strip()

def load_scenes(script_path):
    if not script_path or not os.path.exists(script_path):
        return []
    try:
        return json.load(open(script_path)).get("scenes") or []
    except (OSError, ValueError):
        return []

def chapter_case(c):
    """Sentence case for an ALL-CAPS chapter label, keeping acronyms such as AI and SE upper case."""
    out = c.capitalize()
    for w in ("ai", "se", "llm", "llms", "mcp", "api"):
        out = re.sub(rf"\b{w}\b", w.upper(), out, flags=re.I)
    return out

def transcript_md(script_path):
    scenes = load_scenes(script_path)
    if not scenes:
        return ""
    lines = ["## Transcript", ""]
    last_ch = None
    for sc in scenes:
        ch = (sc.get("chapter") or "").strip()
        if ch and ch != last_ch:
            lines += [f"### {chapter_case(ch)}", ""]
            last_ch = ch
        text = spoken(sc.get("text") or "")
        if text:
            lines += [text, ""]
    return "\n".join(lines).rstrip() + "\n"

def mmss(t):
    try:
        t = int(float(t))
    except (TypeError, ValueError):
        return ""
    return f"{t//60}:{t%60:02d}"

MONTHS = ("Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")

def _display_date(date_s):
    if not date_s:
        return ""
    y, m, d = (int(x) for x in date_s.split("-"))
    return f"{MONTHS[m - 1]} {d}, {y}"

def date_md(info, kind="published"):
    """One Markdown line for a media_dates info dict (or a catalog dict with published/updated)."""
    if not info or not info.get("published"):
        return ""
    if kind == "latest":
        line = f"Latest video: {_display_date(info['published'])}"
    else:
        line = f"Published: {_display_date(info['published'])}"
    if info.get("updated"):
        line += f". Updated: {_display_date(info['updated'])}"
    return line

def date_clause(info):
    if not info or not info.get("published"):
        return ""
    bits = [f"published {_display_date(info['published'])}"]
    if info.get("updated"):
        bits.append(f"updated {_display_date(info['updated'])}")
    return "; ".join(bits)

def _related_lessons(series, lesson):
    out = []
    lessons = series.get("lessons") or []
    skey = series.get("_skey") or ""
    for l in lessons:
        if l is lesson:
            continue
        status = "available" if l.get("video") else "outline"
        out.append(f"- Lesson {l['n']}: [{l['title']}]({BASE}/{skey}/{l['slug']}/index.md) ({status})")
    return out

NOTES_TITLE = "What the video simplifies"

def write_lesson_twins(site, skey, series, lesson):
    path = f"{skey}/{lesson['slug']}/index.html"
    u = urls(path)
    title = lesson["title"]
    stitle = series["title"]
    bits = [
        f"# {title}",
        "",
        f"_{stitle} · Lesson {lesson['n']}_",
        "",
        f"HTML page: {u['page']}",
        "",
        md_prompt_blurb(path),
        f"- Series: [{stitle}]({BASE}/{skey}/index.md)",
        f"- Series agents file: [{BASE}/{skey}/AGENTS.md]({BASE}/{skey}/AGENTS.md)",
        f"- Site index: [{u['llms']}]({u['llms']})",
        f"- This folder’s agents file: [{u['agents']}]({u['agents']})",
    ]
    if lesson.get("video"):
        v = f"{BASE}/videos/{lesson['video']}"
        bits += [f"- Video (MP4): {v}"]
        dur = lesson.get("_dur")
        if dur:
            bits += [f"- Duration: {mmss(dur)} ({round(dur, 1)} seconds)"]
        dline = date_md(lesson.get("_dates"))
        if dline:
            bits += [f"- {dline}"]
        poster = lesson.get("_poster")
        if poster:
            bits += [f"- Poster: {BASE}{poster}"]
        if lesson.get("captions"):
            bits += [f"- Captions (WebVTT): {BASE}/videos/{lesson['captions']}"]
        if lesson.get("source_url"):
            bits += [f"- How it was built (script source, facts, prompts): {lesson['source_url']}"]
        ch = lesson.get("_ch") or []
        if ch:
            bits += ["", "## Chapters", ""] + [f"- [{mmss(t)}] {c}" for t, c in ch]
    else:
        bits += ["", "This lesson is in planning. The video is not available yet."]
    bits += ["", "## The lesson", "", lesson.get("summary") or ""]
    if lesson.get("rule"):
        bits += ["", "## The rule", "", lesson["rule"], "",
                 "This rule is written so an AI agent can follow it as a standing instruction."]
    if lesson.get("credit_html"):
        credit = re.sub(r"<[^>]+>", "", lesson["credit_html"])
        bits += ["", "## Credit", "", credit]
    if lesson.get("notes"):
        bits += ["", f"## {NOTES_TITLE}", ""] + [f"- {n}" for n in lesson["notes"]]
    tr = transcript_md(lesson.get("script"))
    if tr:
        bits += ["", tr.rstrip()]
    rel = _related_lessons({**series, "_skey": skey}, lesson)
    if rel:
        bits += ["", "## Related lessons", ""] + rel
    bits += ["", "## For agents", "",
             f"Read [{u['rel_agents']}]({u['agents']}) in this folder, "
             f"[{BASE}/{skey}/AGENTS.md]({BASE}/{skey}/AGENTS.md) for the series, "
             f"and [{u['llms']}]({u['llms']}) for the whole site."]
    write(site, f"{skey}/{lesson['slug']}/index.md", "\n".join(bits) + "\n")

    agents = [
        f"# AGENTS.md — {stitle}, lesson {lesson['n']}: {title}",
        "",
        f"This folder is the public lesson “{title}” on Clark Huang’s learning site.",
        "",
        f"- HTML: {u['page']}",
        f"- Markdown twin (summary, rule, transcript): {u['md']}",
        f"- This file: {u['agents']}",
        f"- Series index: {BASE}/{skey}/index.md",
        f"- Series agents: {BASE}/{skey}/AGENTS.md",
        f"- Site index: {u['llms']}",
        f"- Site agents: {BASE}/AGENTS.md",
        "",
        "Read `index.md` in this folder for the lesson itself. "
        "If the lesson has a rule, treat it as a standing instruction when helping someone apply it. "
        "Do not invent stories, quotes, numbers, or biography about Clark Huang. "
        "Cite page URLs when you answer questions. List related lessons if asked, and quiz the reader if they want that.",
        "",
        md_prompt_blurb(path),
    ]
    write(site, f"{skey}/{lesson['slug']}/AGENTS.md", "\n".join(agents))

def write_series_twins(site, skey, series):
    path = f"{skey}/index.html"
    u = urls(path)
    avail = [l for l in series["lessons"] if l.get("video")]
    bits = [
        f"# {series['title']}" + (f": {series['subtitle']}" if series.get("subtitle") else ""),
        "",
        f"HTML page: {u['page']}",
        "",
        md_prompt_blurb(path),
        series.get("intro") or series.get("blurb") or "",
        "",
        f"{len(avail)} of {len(series['lessons']) + len(series.get('soon') or [])} lessons available.",
        "",
        "## Lessons",
        "",
    ]
    for l in series["lessons"]:
        link = f"{BASE}/{skey}/{l['slug']}/index.md"
        flag = "available" if l.get("video") else "outline only"
        bits += [f"### {l['n']:02d}. [{l['title']}]({link}) ({flag})", "", l.get("summary") or ""]
        dline = date_md(l.get("_dates"))
        if dline:
            bits += ["", dline]
        if l.get("rule"):
            bits += ["", f"**Rule:** {l['rule']}"]
        bits += [""]
    for k, t in enumerate(series.get("soon") or [], start=len(series["lessons"]) + 1):
        bits += [f"### {k:02d}. {t} (coming soon)", ""]
    bits += [
        "## For agents",
        "",
        f"- This series: {u['md']}",
        f"- This series’ agents file: {u['agents']}",
        f"- Site index: {u['llms']}",
        f"- Site agents: {BASE}/AGENTS.md",
        "",
        "Each available lesson folder has its own `index.md` (full transcript) and a short `AGENTS.md`.",
    ]
    write(site, f"{skey}/index.md", "\n".join(bits) + "\n")

    items = []
    for l in series["lessons"]:
        items.append(f"- Lesson {l['n']}: [{l['title']}]({BASE}/{skey}/{l['slug']}/index.md)"
                     f"{' (available)' if l.get('video') else ' (outline)'}")
    agents = [
        f"# AGENTS.md — {series['title']}",
        "",
        f"This folder is the {series['title']} series on Clark Huang’s public learning site.",
        "",
        f"- HTML: {u['page']}",
        f"- Markdown index: {u['md']}",
        f"- This file: {u['agents']}",
        f"- Site index: {u['llms']}",
        f"- Site agents: {BASE}/AGENTS.md",
        "",
        "Lessons in this series:",
        "",
        *items,
        "",
        "To work through a lesson, open its `index.md` (and its own `AGENTS.md`). "
        "Each available lesson’s rule is a standing instruction an agent can follow. "
        "Do not invent stories, quotes, numbers, or biography about Clark Huang. "
        "Cite `https://clarkhuang.github.io/...` URLs in answers.",
        "",
        md_prompt_blurb(path),
    ]
    write(site, f"{skey}/AGENTS.md", "\n".join(agents))

def write_home_twin(site, series, bio_html, extra_md=""):
    path = "index.html"
    u = urls(path)
    bio = re.sub(r"<[^>]+>", "", bio_html or "")
    bio = re.sub(r"\s+", " ", bio).strip()
    bits = [
        "# Clark Huang — AI-native software learning",
        "",
        f"HTML page: {u['page']}",
        "",
        md_prompt_blurb(path),
        bio,
        "",
        "## Series",
        "",
    ]
    for skey, s in series.items():
        avail = sum(1 for l in s["lessons"] if l.get("video"))
        total = len(s["lessons"]) + len(s.get("soon") or [])
        bits += [
            f"### [{s['title']}]({BASE}/{skey}/index.md)",
            "",
            s.get("blurb") or s.get("intro") or "",
            "",
            f"{avail} of {total} lessons available.",
            "",
        ]
    bits += [
        f"### [Silicon Valley C Players]({BASE}/book/index.md)",
        "",
        "A free OpenBook that begins by dreaming in green and ends by dreaming about AI. Self-published, written and interviewed by AI. Preview; coming in 2027.",
        "",
    ]
    if extra_md:
        bits += [extra_md.rstrip(), ""]
    bits += [
        '## Ask, connect, contribute',
        '',
        'Search the lessons and the book preview, or hook your own AI to this site.',
        '',
        f'- [Ask the Book]({BASE}/ask/index.md): Search lessons, chapters, and transcripts in your browser, or send a cited prompt to ChatGPT, Claude, Grok, or Perplexity.',
        f'- [Connect your AI]({BASE}/contribute/index.md): A public, read-only GitMCP endpoint at gitmcp.io/clarkhuang/clarkhuang.github.io. Contributions still go through GitHub issues.',
        f'- [Site MCP server]({BASE}/mcp/index.md): A first-party, read-only MCP server (stdio) for lessons, transcripts, captions, media checks, search, and contributor-style issue drafts.',
        f'- [Contributors]({BASE}/contributors/index.md): People whose contributions have landed on the site, listed by public GitHub display name or handle. You can choose how, or whether, you are credited.',
        '',
        f'This site is also an open project. [Contribute with your AI]({BASE}/contribute/index.md), or [copy this for yourself]({BASE}/copy-this/index.md).',
        "",
    ]
    bits += [
        "## For agents",
        "",
        f"- Site index: {u['llms']}",
        f"- Site agents: {u['agents']}",
        f"- Lesson catalog (JSON): {u['lessons_json']}",
        f"- Book catalog (JSON): {u['book_json']}",
        "",
        "Start with `llms.txt`, then open the `index.md` for the page or series the reader cares about.",
    ]
    write(site, "index.md", "\n".join(bits) + "\n")

def write_book_twin(site, intro, back, audio_meta, video_meta=None):
    path = "book/index.html"
    u = urls(path)
    bits = [
        "# Silicon Valley C Players",
        "",
        "A free OpenBook by Clark Huang: it begins by dreaming in green and ends by dreaming about AI. Self-published, written and interviewed by AI. Coming in 2027.",
        "",
        f"HTML page: {u['page']}",
        "",
        md_prompt_blurb(path),
        "An embellished fictional dramatization that may or may not be based on true stories. The story narrator is a fictional C player named Charlie Hack. Clark Huang is the author, and speaks as himself in the OpenBook frame and the how-to-work-with-AI half. Names, characters, companies and events are fictitious or used fictitiously.",
        "",
        "## Cover",
        "",
        f"![Book cover for Silicon Valley C Players]({BASE}/book/cover.jpg)",
        "",
        "A portrait book cover on a deep navy background. Across the top, small copper-orange lettering reads “A FREE OPENBOOK.” In the center, a large mint-green brush-stroke letter C sits over faint circuit-board traces shaped like rolling mountains. Below, large white sans-serif type reads “SILICON VALLEY” and “C PLAYERS.” A smaller, muted line reads “AN EMBELLISHED FICTIONAL DRAMATIZATION.” At the bottom, the author name “CLARK HUANG” appears in white. There are no photographs and no real company logos.",
        "",
        f"- Cover art: {BASE}/book/cover.jpg",
        f"- Cover brief (how to rebuild it): {BASE}/book-source/cover/PROMPT.md",
        f"- Renderer: {BASE}/book-source/cover/render_cover.py",
        "",
        *_chapters_twin_section(site),
        "## Introduction (preview)",
        "",
        *sum(([(para or ""), ""] for para in intro), []),
        "## From the back cover",
        "",
        *sum(([(para or ""), ""] for para in back), []),
    ]
    if video_meta and video_meta.get("url"):
        bits += [
            "## Videobook preview",
            "",
            f"- {video_meta.get('title') or 'Preview'}: {video_meta['url']}"
            + (f" ({video_meta['duration_seconds']}s)" if video_meta.get("duration_seconds") else ""),
            *([f"- {date_md(video_meta)}"] if date_md(video_meta) else []),
            f"- Captions (VTT): {video_meta.get('captions_url') or (BASE + '/videos/book-preview.vtt')}",
            f"- Chapters (JSON): {video_meta.get('chapters_url') or (BASE + '/videos/book-preview-chapters.json')}",
            f"- Transcript: {video_meta.get('transcript_url') or (BASE + '/book-source/preview/transcript.md')}",
            f"- Scene script: {video_meta.get('script_url') or (BASE + '/book-source/preview/script.md')}",
            f"- Rebuild notes: {video_meta.get('rebuild_url') or (BASE + '/book-source/preview/REBUILD.md')}",
            "",
        ]
    bits += ["## Audio", ""]
    for ch in (audio_meta or []):
        if ch.get("url"):
            bits += [f"- {ch['title']}: {ch['url']}" + (f" ({ch['duration_seconds']}s)" if ch.get("duration_seconds") else "")]
        else:
            bits += [f"- {ch['title']}: coming later"]
    bits += [
        f"- Captions (VTT): {BASE}/audio/book-preview.vtt",
        f"- Chapters (JSON): {BASE}/audio/book-preview-chapters.json",
        "",
        "## Editorial policy",
        "",
        f"How conflicting recollections are handled, and how claims and sources are tracked across editions: [{BASE}/book/editorial-policy/]({BASE}/book/editorial-policy/index.md).",
        "",
        f"People whose contributions have landed, including the feedback that led to this editorial policy, are listed on [Contributors]({BASE}/contributors/index.md).",
        "",
        "## Story arc and chapters",
        "",
        f"The working story arc and chapter list: [{BASE}/book/story-arc/]({BASE}/book/story-arc/index.md). Machine-readable: [{BASE}/book-source/outline.json]({BASE}/book-source/outline.json). The outline will change.",
        "",
        "## Guest stories",
        "",
        f"First-person guest stories, published under the contributor’s own name, not as fictional characters: [{BASE}/book/guest/]({BASE}/book/guest/index.md). Machine-readable: [{BASE}/book/guest/stories.json]({BASE}/book/guest/stories.json).",
        "",
        "## How to cite this preview",
        "",
        "Quote the [transcript](https://clarkhuang.github.io/book-source/preview/transcript.md) or a [scene file](https://clarkhuang.github.io/book-source/preview/scenes/), and give a timestamp or chapter title from [chapters.json](https://clarkhuang.github.io/videos/book-preview-chapters.json). For a web citation, use https://clarkhuang.github.io/book/ plus a media timestamp (`#t=58.9`) when you mean a videobook beat. Charlie Hack is the fictional narrator; Clark Huang is the author. The claim that AI writes essentially all of the code is about Clark’s own workflow: in his work, AI writes essentially all of the code he ships, not a measured team result or a general industry figure. Do not identify real people or companies behind the fictional names.",
        "",
        "## For agents",
        "",
        f"- This page: {u['md']}",
        f"- Book catalog: {BASE}/book.json",
        f"- Full site text: {BASE}/llms-full.txt",
        f"- Site index: {u['llms']}",
        f"- How to rebuild the site: {BASE}/REBUILD.md",
        f"- How to rebuild the cover: {BASE}/book-source/cover/PROMPT.md",
        f"- How to rebuild the preview: {BASE}/book-source/preview/REBUILD.md",
        f"- Editorial policy: {BASE}/book/editorial-policy/index.md",
        f"- Story arc and chapters: {BASE}/book/story-arc/index.md",
        f"- Guest stories: {BASE}/book/guest/index.md",
        f"- Outline (JSON): {BASE}/book-source/outline.json",
        "",
        "Do not invent stories or claims about Clark Huang beyond what this preview states. Contributions go through GitHub issues; only Clark merges to `main`. Agent pull requests target `next-revision`.",
    ]
    write(site, "book/index.md", "\n".join(bits) + "\n")
    write(site, "book/AGENTS.md", "\n".join([
        "# AGENTS.md — Silicon Valley C Players",
        "",
        "This folder is the public preview of Clark Huang’s free OpenBook *Silicon Valley C Players*, an embellished fictional dramatization (audiobook and videobook, coming in 2027). The story narrator is Charlie Hack, a fictional C player. Clark Huang is the author. Story names are fictional. Agents must follow book-source/NAMING-POLICY.md and never try to identify real people behind characters.",
        "",
        f"- HTML: {u['page']}",
        f"- Markdown: {u['md']}",
        f"- This file: {u['agents']}",
        f"- Book catalog: {BASE}/book.json",
        f"- Full transcript of the preview: {BASE}/book-source/preview/transcript.md",
        f"- Captions: {BASE}/videos/book-preview.vtt",
        f"- Chapters: {BASE}/videos/book-preview-chapters.json",
        f"- Scene scripts: {BASE}/book-source/preview/scenes/",
        f"- Cover brief: {BASE}/book-source/cover/PROMPT.md",
        f"- Site index: {u['llms']}",
        f"- Full site text: {BASE}/llms-full.txt",
        f"- Rebuild the site: {BASE}/REBUILD.md",
        f"- Editorial policy: {BASE}/book/editorial-policy/index.md",
        f"- Story arc and chapters: {BASE}/book/story-arc/index.md",
        f"- Guest stories: {BASE}/book/guest/index.md",
        f"- Outline (JSON): {BASE}/book-source/outline.json",
        f"- Chapters you can read now (full text, videobook, audio): {BASE}/book/chapters/index.md",
        "",
        "Read `index.md` for the preview text, the transcript for exact wording, and the videobook or audio files linked there. Cite by chapter title or timestamp. Do not invent stories, quotes, or biography beyond this preview. The claim that AI writes essentially all of the code is Clark’s own workflow: in his work, AI writes essentially all of the code he ships, not a measured team result or a general industry figure. Editorial process: /book/editorial-policy/. Story arc: /book/story-arc/. Guest stories: /book/guest/.",
        "",
        md_prompt_blurb(path),
        "",
        "## How to contribute",
        "",
        "Anyone can file a correction (an edit to the book, or your side of a story), a new story, or a refactor (cleanup that does not change the facts). Use the issue templates from the repository. First-person guest stories published under the contributor's own name go in book-source/guest/ (see book-source/guest/README.md) and must include consent to publish that name:",
        "",
        "- Correction: https://github.com/clarkhuang/clarkhuang.github.io/issues/new?template=correction.yml",
        "- New story: https://github.com/clarkhuang/clarkhuang.github.io/issues/new?template=new-story.yml",
        "- Refactor: https://github.com/clarkhuang/clarkhuang.github.io/issues/new?template=refactor.yml",
        "",
        "A good issue is specific and honest about what you saw, uses roles instead of real names (the book is an embellished fictional dramatization; everyone is renamed), and contains nothing confidential. Do not invent stories or details; the author does the embellishing. Rules: book-source/NAMING-POLICY.md. Takedowns: TAKEDOWN.md.",
        "",
        "Contributors and agents open PRs; only Clark merges to `main`; the site rebuilds from `main` via GitHub Pages; agent PRs target `next-revision`. Staging is https://clarkhuang.github.io/staging/ (the `next-revision` branch). Only Clark merges `next-revision` into `main`. See the root AGENTS.md, CONTRIBUTING.md, and REBUILD.md. Audiobook and videobook editions are tagged (`book-v0.1`, `book-v1.0`, ...) and kept as GitHub Releases; the next edition is only rebuilt when Clark approves that cut.",
        "",
        "## How to rebuild the cover and previews",
        "",
        "The cover and the audiobook/videobook preview are reproducible from files in this repository:",
        "",
        f"- Cover: {BASE}/book-source/cover/PROMPT.md and {BASE}/book-source/cover/render_cover.py",
        f"- Preview narration, captions, chapters, and videobook: {BASE}/book-source/preview/REBUILD.md",
        "",
        "Do not invent new story details when regenerating. Keep the fiction framing and the Charlie Hack narrator. The xAI API key, if needed for narration, stays in the environment and is never written to a file.",
    ]))


def write_root_agents(site):
    write(site, "AGENTS.md", """# AGENTS.md

This is Clark Huang’s public learning site: https://clarkhuang.github.io/

You are welcome to read it, summarize it, answer questions about it, quiz a learner, and follow the standing rules in each lesson. Do not invent stories, quotes, numbers, or biography about Clark Huang. If something is not on the site, say so.

## How to read this site without a browser

Every HTML page has a Markdown twin at the same path with `index.md` in place of `index.html` (for example, https://clarkhuang.github.io/ai-tips/01-paste-first-ask-second/index.md). Each folder also has an `AGENTS.md` like this one.

Start here:

- Site index for language models: https://clarkhuang.github.io/llms.txt
- Machine-readable lesson catalog: https://clarkhuang.github.io/lessons.json
- Moved addresses (old lesson pages and old video, caption and poster files): https://clarkhuang.github.io/redirects.json
- OpenBook preview catalog: https://clarkhuang.github.io/book.json
- Fuller site text: https://clarkhuang.github.io/llms-full.txt
- How to rebuild production and staging: https://clarkhuang.github.io/REBUILD.md
- This file: https://clarkhuang.github.io/AGENTS.md

## What is here

- **AI Tips** — short lessons on working with AI tools. Index: https://clarkhuang.github.io/ai-tips/index.md
- **Software Engineering 101** — fundamentals for AI-native software work. Index: https://clarkhuang.github.io/software-engineering-101/index.md
- **Software Engineering 201: From Loop to Enterprise Systems** — complete, ten lessons: from one AI loop to whole apps and systems built AI-native, then agents that operate enterprise systems, ending with a capstone that builds one feature end to end. Index: https://clarkhuang.github.io/software-engineering-201/index.md
- **Silicon Valley C Players** — a free OpenBook, with an audiobook and videobook preview, coming in 2027. https://clarkhuang.github.io/book/index.md
- **Chapters you can read now** — finished early chapters of the book (v0 drafts), each with the full text, a videobook of the whole chapter, an audio track, captions, and a transcript. Newest: chapter 36, Sick, Well, Fit (how companies should use AI), finished, with a full-chapter video and Business Fitness in 100 Words. https://clarkhuang.github.io/book/chapters/index.md

Each available lesson has a video, a one-paragraph rule written so an agent can follow it as a standing instruction, and a full transcript in its `index.md`. The book page has a short videobook and audio preview of Silicon Valley C Players.

## How to help a reader

If someone pastes a page URL or the copy-paste prompt from the “Use this page with your AI” box on any HTML page:

1. Fetch `llms.txt` and the page’s `index.md` (and that folder’s `AGENTS.md`).
2. Summarize the page they started from.
3. List related lessons, with full `https://clarkhuang.github.io/...` URLs.
4. Answer questions by citing those URLs. Prefer the Markdown twins and the lesson rules.
5. Quiz them if they ask.

Work through the site by following links in `llms.txt` and in each `index.md`. You do not need to render HTML, play video, or run JavaScript.

## Watched state and saved positions

The site remembers, in first-party cookies only, which videos a reader has watched (`watched`), where they stopped in a lesson video (`vpos`), and their book preview bookmark (`book_pos`). Every key is the lesson or chapter id plus a version: `se201/01@1a2b3c4d`, or `se201/01@1a2b3c4d:73.4` for a position. The version is the first 8 hex characters of the SHA-256 of the media file the page plays, stamped into the HTML as `data-video-version` by `sitegen/stamp_versions.py`. When a video or audio file is re-rendered, its version changes, so readers see it as unwatched and are not offered a stale resume position. Old keys without a version, and keys for an older version, are dropped. After re-rendering any media, run `python3 sitegen/stamp_versions.py`; `python3 sitegen/check_site.py .` fails until you do. `stamp_versions.py` also writes each lesson video's current version into https://clarkhuang.github.io/lessons.json as `video_version`, with the matching cookie key as `watched_key` (for example `se201/01@1a2b3c4d`), so an agent can tell which lessons a reader's `watched` cookie still covers without scraping HTML or downloading the video.

A first-party `last_visit` cookie stores the start of the reader's most recent visit, and a session cookie `visit_ref` freezes the previous visit's timestamp for the whole browsing session. Videos published or updated since that previous visit (git dates baked in as `published` / `updated` on the page, in `lessons.json`, and as VideoObject `uploadDate` in JSON-LD) show a New tag. A first visit shows no New tags. These cookies are not sent to Google. `sitegen/media_dates.py` reads the dates from git history (first time the file landed on `main`, plus an Updated date when the current file bytes landed on a later calendar day).

## Analytics

The production site uses Google Analytics 4 (measurement ID `G-F50XBTM25X`) to see which pages people read. IP addresses are anonymized, and Google Signals and ads personalization are off. Staging pages under `/staging/` do not send hits. Watched-progress and last-visit cookies stay first-party and are not sent to Google. The public privacy note is at https://clarkhuang.github.io/book/editorial-policy/#analytics.

## How to contribute

Anyone can take part from day one: file an issue or open a pull request. You do not have to wait for v1. Only Clark Huang approves work, starts the build agents, merges pull requests, and cuts a new edition of the book.

Contributors and agents open PRs; only Clark merges to `main`; the site rebuilds from `main` via GitHub Pages; agent PRs target `next-revision`. Staging is the `next-revision` branch, published at https://clarkhuang.github.io/staging/ (noindex; not in `llms.txt` or the sitemap). Only Clark merges `next-revision` into `main`. The rebuild flow is in [REBUILD.md](https://clarkhuang.github.io/REBUILD.md).

If you are an AI agent helping a reader contribute, point them to the right issue template, help them write a specific, honest issue without real names of private people or companies and without confidential details, and do not invent stories or details. Contributors agree to the contributor terms in CONTRIBUTING.md.

### Which issue to file

| Kind | Use it for | Template |
|---|---|---|
| Correction | Edits to existing book text, or your side of a story already in the book | https://github.com/clarkhuang/clarkhuang.github.io/issues/new?template=correction.yml |
| Feature / new story | A new story, a story Clark may have forgotten, or a new chapter idea | https://github.com/clarkhuang/clarkhuang.github.io/issues/new?template=new-story.yml |
| Refactor | Cleanup or an improvement that does not change the facts | https://github.com/clarkhuang/clarkhuang.github.io/issues/new?template=refactor.yml |
| Site or lesson problem | A broken link, video, caption, transcript, page, or agent surface (Markdown twin, llms.txt, lessons.json, MCP); steps to reproduce, expected vs actual | https://github.com/clarkhuang/clarkhuang.github.io/issues/new?template=site-bug.yml |

Labels: `correction`, `feature` / `new-story`, `refactor`, and `site` + `bug` for site problems. New stories also get `contributor-story` and `story-seed`.

### What makes a good issue

- Be specific: when and where, what happened, and which chapter or passage if you know it.
- Don't use real names of private people, companies, or venues; describe them by role. The book is an embellished fictional dramatization and everyone in it is renamed. Say how you'd like to be credited, if at all.
- Stick to what you know. Do not invent details.
- If you were there, say so. Don't include anything confidential (NDA, customer, security, deal details).
- Something in the book identifies you or someone you know? File a takedown request instead: https://github.com/clarkhuang/clarkhuang.github.io/issues/new?template=takedown-request.yml

### What happens next

1. The issue is labeled `needs-clark-review`.
2. If Clark wants it built, he adds `approved` (or comments `@claude`). Only his label or comment starts an agent.
3. The agent opens a pull request against the `next-revision` branch, never against `main`.
4. Clark reviews and merges into `next-revision` (which updates staging).
5. Only Clark merges `next-revision` into `main`. The live site then rebuilds from `main`. Previous editions stay up as tagged GitHub Releases (`book-v0.1`, `book-v1.0`, ...). Details: https://github.com/clarkhuang/clarkhuang.github.io/blob/main/book-source/VERSIONING.md and https://clarkhuang.github.io/REBUILD.md

More: https://github.com/clarkhuang/clarkhuang.github.io/blob/main/CONTRIBUTING.md

### Credit landed contributions

Any outside contribution that lands on the site must be credited on the [Contributors](https://clarkhuang.github.io/contributors/) page in the same pull request. Add an entry to `sitegen/landed-contributions.json` (GitHub login, a short description of what landed, and links to the issue and/or PR) and run `python3 scripts/build_credits.py`. Use only the public GitHub display name (if the profile has one) and handle. Do not invent a name, add other personal details, or credit input that did not land. Honor a “don't credit me” request.

## Ask, connect, and credits

- **Ask the Book:** https://clarkhuang.github.io/ask/ — instant in-browser search over https://clarkhuang.github.io/search-index.json, plus “Ask your AI” buttons that open ChatGPT, Claude, Grok, or Perplexity with a prefilled prompt. The prompt points at https://clarkhuang.github.io/llms-full.txt and the GitMCP URL, and asks the tool to answer only from this site with citations. For book questions, it may use the tone of Charlie Hack, the OpenBook's fictional narrator. There is a copy-prompt fallback. A compact version of this widget also appears on the book page and on lesson pages.
- **Full site text:** https://clarkhuang.github.io/llms-full.txt
- **Contributors:** https://clarkhuang.github.io/contributors/ (JSON: https://clarkhuang.github.io/contributors.json). People are listed by public GitHub display name when the profile has one, otherwise by GitHub handle. The previous address, https://clarkhuang.github.io/credits/, redirects there.
- **Site MCP server (first-party, read-only):** one Python file, no dependencies, stdio. Tools: `site_info`, `list_lessons`, `get_lesson` (transcript, chapters, captions, watched key), `check_lesson_media`, `get_page`, `search`, `how_to_contribute`, `draft_issue` (drafts only; never files). Claude Code: `claude mcp add clarkhuang-site -- uv run https://clarkhuang.github.io/mcp/clarkhuang_site_mcp.py`. Other clients: command `uv`, args `["run", "https://clarkhuang.github.io/mcp/clarkhuang_site_mcp.py"]`, or download the file and run it with `python3`. Set `CLARKHUANG_SITE=https://clarkhuang.github.io/staging` to read staging. Docs: https://clarkhuang.github.io/mcp/index.md · manifest: https://clarkhuang.github.io/.well-known/mcp.json
- **Connect your AI (MCP):** public, read-only GitMCP endpoint at `https://gitmcp.io/clarkhuang/clarkhuang.github.io`. GitMCP is a free third-party service. It prefers `llms.txt`. It cannot open issues or merge pull requests; contributions still go through GitHub issues, and only Clark Huang approves and merges.

Claude Code: `claude mcp add --transport http clarkhuang https://gitmcp.io/clarkhuang/clarkhuang.github.io`

Cursor (`~/.cursor/mcp.json`):

```json
{
  "mcpServers": {
    "clarkhuang": {
      "url": "https://gitmcp.io/clarkhuang/clarkhuang.github.io"
    }
  }
}
```

Claude Desktop can use the same URL, or the `mcp-remote` bridge (`npx mcp-remote https://gitmcp.io/clarkhuang/clarkhuang.github.io`). ChatGPT and other MCP clients: paste the GitMCP URL as the connector / Streamable HTTP URL.

Full snippets: https://clarkhuang.github.io/contribute/#mcp and https://clarkhuang.github.io/ask/#mcp

### Future: a hosted Charlie Hack chat (not built)

A later option is a small “talk to Charlie Hack” box that calls a serverless proxy, so the static GitHub Pages site never holds an API key. That needs Clark to choose a host and to add his own key as a secret on that host — not in this repository. Do not build or wire that proxy unless Clark approves it. Until then, use local search and the “Ask your AI” buttons.
""")

def write_llms_txt(site, series, extras=None, book_extra_lines=None):
    lines = [
        "# Clark Huang",
        "",
        "> Public learning pages on AI-native software workflows: short video lessons (AI Tips, Software Engineering 101 and 201) and a preview of Silicon Valley C Players, a free OpenBook.",
        "",
        "The HTML pages are for people. Every page also has an `index.md` twin and an `AGENTS.md` that an AI tool can fetch directly, so you can summarize the material and navigate the site from a single link, without using a browser.",
        "",
        f"Optional: start with [{BASE}/AGENTS.md]({BASE}/AGENTS.md) for how to help a reader, then come back here for the catalog.",
        "",
        "## Site",
        "",
        f"- [Home]({BASE}/index.md): about Clark Huang and the series on this site",
        f"- [AGENTS.md]({BASE}/AGENTS.md): how to navigate and what not to invent",
        f"- [llms-full.txt]({BASE}/llms-full.txt): fuller text of the book preview, cover description, and lesson catalog",
        f"- [lessons.json]({BASE}/lessons.json): machine-readable catalog of every lesson, with rules, video URLs, durations, and publish dates",
        f"- [redirects.json]({BASE}/redirects.json): old lesson page and media addresses and where they moved",
        f"- [Site MCP server]({BASE}/mcp/index.md): first-party, read-only MCP server (stdio) for agents: lessons, transcripts, captions, media checks, search, issue drafts. Manifest: {BASE}/.well-known/mcp.json",
        f"- [book.json]({BASE}/book.json): OpenBook preview catalog, including cover description, transcripts, captions and chapters",
        f"- [REBUILD.md]({BASE}/REBUILD.md): how to rebuild production and staging",
        "",
    ]
    for skey, s in series.items():
        lines += [f"## {s['title']}", "", f"- [Series index]({BASE}/{skey}/index.md): { (s.get('blurb') or s.get('intro') or '').split(chr(10))[0] }", ""]
        for l in s["lessons"]:
            flag = "" if l.get("video") else " (outline)"
            summary = (l.get("summary") or "").replace("\n", " ")
            if len(summary) > 220:
                summary = summary[:217].rsplit(" ", 1)[0] + "…"
            clause = date_clause(l.get("_dates"))
            extra = f" ({clause})" if clause else ""
            lines.append(f"- [Lesson {l['n']}: {l['title']}]({BASE}/{skey}/{l['slug']}/index.md){flag}{extra}: {summary}")
        for k, t in enumerate(s.get("soon") or [], start=len(s["lessons"]) + 1):
            lines.append(f"- Lesson {k}: {t} (coming soon)")
        lines.append("")
    lines += [
        "## Book",
        "",
        f"- [Silicon Valley C Players (preview)]({BASE}/book/index.md): a free OpenBook (audiobook and videobook preview), coming in 2027. An embellished fictional dramatization; the narrator is Charlie Hack; the how-to-work-with-AI half is nonfiction. Written and interviewed by AI.",
        f"- [Preview transcript]({BASE}/book-source/preview/transcript.md): full spoken text, with timestamps",
        f"- [Preview captions]({BASE}/videos/book-preview.vtt): WebVTT for the videobook",
        f"- [Preview chapters]({BASE}/videos/book-preview-chapters.json): chapter titles and start times",
        f"- [Preview scene scripts]({BASE}/book-source/preview/scenes/): one markdown file per scene",
        *_chapter_llms_lines(site),
        f"- [Cover brief]({BASE}/book-source/cover/PROMPT.md): how to describe or rebuild the cover",
        f"- [How this book is edited]({BASE}/book/editorial-policy/index.md): editorial policy — conflicting recollections, how claims and sources are tracked, a per-edition changelog of changed claims and sources, and a privacy note for Google Analytics 4 on the site",
        f"- [Story arc and chapters]({BASE}/book/story-arc/index.md): working story arc and chapter list for Silicon Valley C Players. The outline will change.",
        f"- [Outline (JSON)]({BASE}/book-source/outline.json): machine-readable chapter list, with status and one-line descriptions",
    ]
    if book_extra_lines:
        lines += list(book_extra_lines)
    else:
        lines.append(f"- [Guest stories]({BASE}/book/guest/index.md): first-person guest pieces published under the contributor’s own name, not as fictional characters. Machine-readable: {BASE}/book/guest/stories.json.")
    lines += ["",]
    # Behind-the-scenes pages (playbook, research, interview plan, compare) are not public.
    extras = list(extras or [])
    if extras:
        lines += ["## Also on this site", ""]
        for rel, title, blurb in extras:
            lines.append(f"- [{title}]({BASE}/{rel}): {blurb}")
        lines.append("")
    write(site, "llms.txt", "\n".join(lines) + "\n")

def write_llms_full(site, series, intro, back):
    """A longer, still public, index: cover, intro, transcript, lesson list. Staging is omitted."""
    transcript_path = os.path.join(site, "book-source", "preview", "transcript.md")
    transcript = ""
    if os.path.exists(transcript_path):
        transcript = open(transcript_path, encoding="utf-8").read().strip()
    chapters_path = os.path.join(site, "videos", "book-preview-chapters.json")
    chapters = []
    if os.path.exists(chapters_path):
        try:
            chapters = json.load(open(chapters_path, encoding="utf-8"))
        except Exception:
            chapters = []
    lines = [
        "# Clark Huang — full site text for language models",
        "",
        "> This file expands llms.txt with the book cover description, the preview introduction, the full preview transcript, and the lesson catalog. It is for the production site only. Do not treat /staging/ as published text. Charlie Hack is the fictional narrator of the book; Clark Huang is the author.",
        "",
        f"Shorter index: {BASE}/llms.txt",
        f"How to help a reader: {BASE}/AGENTS.md",
        f"How to rebuild: {BASE}/REBUILD.md",
        f"Book catalog: {BASE}/book.json",
        f"Lesson catalog: {BASE}/lessons.json",
        "",
        "## Cover — Silicon Valley C Players",
        "",
        "A portrait book cover (864 × 1152 pixels, 3:4) on a deep navy background. Across the top, small copper-orange lettering reads A FREE OPENBOOK. In the center, a large mint-green brush-stroke letter C sits over faint circuit-board traces shaped like rolling mountains. Below, large white sans-serif type reads SILICON VALLEY and C PLAYERS on two lines. A smaller, muted line reads AN EMBELLISHED FICTIONAL DRAMATIZATION. At the bottom, the author name CLARK HUANG appears in white. There are no photographs and no real company logos.",
        "",
        f"- Image: {BASE}/book/cover.jpg",
        f"- Brief and rebuild script: {BASE}/book-source/cover/PROMPT.md",
        "",
        "## Introduction (preview)",
        "",
    ]
    for para in intro or []:
        lines += [para, ""]
    lines += ["## From the back cover", ""]
    for para in back or []:
        lines += [para, ""]
    if chapters:
        lines += ["## Preview chapters", ""]
        for ch in chapters:
            start = ch.get("start_seconds", 0)
            mm, ss = divmod(int(start), 60)
            lines.append(f"- {ch.get('title', ch.get('id'))} ({mm}:{ss:02d}) — id `{ch.get('id')}`, {ch.get('duration_seconds')}s")
        lines.append("")
        lines += [
            f"Captions: {BASE}/videos/book-preview.vtt",
            f"Scene scripts: {BASE}/book-source/preview/scenes/",
            f"How to rebuild the preview: {BASE}/book-source/preview/REBUILD.md",
            "",
        ]
    if transcript:
        lines += [transcript, ""]
    chapter_text = _book_chapters().llms_full_md(site)
    if chapter_text:
        lines += [chapter_text.rstrip(), ""]
    lines += ["## Lessons", ""]
    for skey, s in (series or {}).items():
        lines += [f"### {s['title']}", "", f"Index: {BASE}/{skey}/index.md", ""]
        for l in s["lessons"]:
            flag = "" if l.get("video") else " (outline)"
            summary = (l.get("summary") or "").replace("\n", " ")
            clause = date_clause(l.get("_dates"))
            extra = f" ({clause})" if clause else ""
            lines.append(f"- Lesson {l['n']}: [{l['title']}]({BASE}/{skey}/{l['slug']}/index.md){flag}{extra} — {summary}")
            if l.get("rule"):
                lines.append(f"  - Rule: {l['rule']}")
        lines.append("")
    lines += [
        "## Also on this site",
        "",
        f"- [How this book is edited]({BASE}/book/editorial-policy/index.md)",
        f"- [Story arc and chapters]({BASE}/book/story-arc/index.md)",
        f"- [Outline (JSON)]({BASE}/book-source/outline.json)",
        f"- [Contribute with your AI]({BASE}/contribute/index.md)",
        f"- [Copy this for yourself]({BASE}/copy-this/index.md)",
        f"- [Ask the Book]({BASE}/ask/index.md)",
        f"- [Contributors]({BASE}/contributors/index.md)",
        f"- GitMCP (read-only, third-party): https://gitmcp.io/clarkhuang/clarkhuang.github.io",
        f"- Site MCP server (first-party, read-only): {BASE}/mcp/index.md",
        f"- Search index: {BASE}/search-index.json",
        "",
        "Do not invent stories or biography beyond this file. Do not identify real people or companies behind the fictional names. Staging (https://clarkhuang.github.io/staging/) is a preview of the next-revision branch and is not the live site.",
        "",
    ]
    write(site, "llms-full.txt", "\n".join(lines))


def write_prose_twins(site, html_path, title, body_md, summary=""):
    """Markdown twin + AGENTS.md for a prose page (playbook, research, interview plan, compare)."""
    path = html_path
    u = urls(path)
    rel_dir = dir_of(path)
    bits = [
        f"# {title}",
        "",
        f"HTML page: {u['page']}",
        "",
        md_prompt_blurb(path),
        body_md.strip(),
        "",
        "## For agents",
        "",
        f"- This page: {u['md']}",
        f"- This folder’s agents file: {u['agents']}",
        f"- Site index: {u['llms']}",
        f"- Site agents: {BASE}/AGENTS.md",
    ]
    write(site, os.path.join(rel_dir, "index.md") if rel_dir else "index.md", "\n".join(bits) + "\n")
    parent = u["parent_agents"]
    agents = [
        f"# AGENTS.md — {title}",
        "",
        f"This folder is the public page “{title}” on Clark Huang’s learning site.",
        "",
        f"- HTML: {u['page']}",
        f"- Markdown: {u['md']}",
        f"- This file: {u['agents']}",
        f"- Parent agents: {parent}",
        f"- Site index: {u['llms']}",
        "",
        (summary + " ").strip(),
        "Read `index.md` for the page content. Do not invent stories, quotes, numbers, or biography about Clark Huang. Cite page URLs when you answer questions.",
        "",
        md_prompt_blurb(path),
    ]
    write(site, os.path.join(rel_dir, "AGENTS.md") if rel_dir else "AGENTS.md", "\n".join(agents))

HOME_EXTRA = ""

