#!/usr/bin/env python3
"""Build readable book chapters (text + videobook + audio) from book-source/chapters/<slug>/.

Each chapter folder holds:
  chapter.json   metadata: id, n, slug, title, subtitle, part, summary, hook, rule, media file names, prev/next
  chapter.md     the chapter text (Markdown; H1 title, italic subtitle, H2 sections, tables, lists, blockquotes)
  transcript.md  the spoken narration, as recorded (captions match it word for word)
  BUILD.md       how the video was made, and how to rebuild it

Writes, for each chapter: book/chapters/<slug>/index.html, index.md (full text + transcript link) and AGENTS.md,
plus the chapter index book/chapters/index.html (+ twins). gen.py calls build_book_chapters() from build_book();
the helpers llms_lines(), llms_full_md(), catalog() and sitemap_urls() keep llms.txt, llms-full.txt, book.json
and sitemap.xml in step. Standalone (writes only the chapter pages and their twins; it does not touch other files):

    SITE=. python3 sitegen/book_chapters.py
"""
from __future__ import annotations

import html
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = "https://clarkhuang.github.io"
E = html.escape
SRC_DIR = os.path.join("book-source", "chapters")


# ------------------------------------------------------------------ data
def load_chapters(site):
    root = os.path.join(site, SRC_DIR)
    out = []
    if not os.path.isdir(root):
        return out
    for slug in sorted(os.listdir(root)):
        meta = os.path.join(root, slug, "chapter.json")
        if not os.path.isfile(meta):
            continue
        ch = json.load(open(meta, encoding="utf-8"))
        ch.setdefault("slug", slug)
        ch["_dir"] = os.path.join(root, slug)
        ch["_text"] = open(os.path.join(root, slug, "chapter.md"), encoding="utf-8").read()
        ch["_url"] = f"/book/chapters/{ch['slug']}/"
        ch["_src_url"] = f"/{SRC_DIR}/{ch['slug']}/".replace(os.sep, "/")
        bf = os.path.join(root, slug, ch.get("featured_file") or "business-fitness-100.md")
        if os.path.isfile(bf):
            raw = [ln.strip() for ln in open(bf, encoding="utf-8").read().strip().splitlines() if ln.strip()]
            ch["_feat_title"], ch["_feat_text"] = raw[0].lstrip("# ").strip(), " ".join(raw[1:])
        out.append(ch)
    return out


def body_markdown(ch):
    """Chapter text without its H1 and italic subtitle (the page supplies those)."""
    lines = ch["_text"].strip().splitlines()
    while lines and (lines[0].startswith("# ") or not lines[0].strip() or re.match(r"^\*[^*].*\*$", lines[0].strip())):
        lines.pop(0)
    return "\n".join(lines).strip() + "\n"


# ------------------------------------------------------------------ tiny Markdown -> HTML (only what chapters use)
def _inline(s):
    s = E(s, quote=False)
    s = re.sub(r"\[([^\]]+)\]\((https?://[^)\s]+|/[^)\s]*)\)", lambda m: f'<a href="{m.group(2)}">{m.group(1)}</a>', s)
    s = re.sub(r"(?<![\"'>=])(https?://[^\s<)]+[^\s<).,;:])", r'<a href="\1">\1</a>', s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![*\w])\*([^*\n]+)\*(?![*\w])", r"<em>\1</em>", s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    return s


def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def md_to_html(md, indent="      "):
    out, para, i = [], [], 0
    lines = md.splitlines()

    def flush():
        if para:
            out.append(f"{indent}<p>{_inline(' '.join(para))}</p>")
            para.clear()

    while i < len(lines):
        ln = lines[i]
        st = ln.strip()
        if not st:
            flush(); i += 1; continue
        m = re.match(r"^(#{2,4})\s+(.*)$", st)
        if m:
            flush()
            lvl = len(m.group(1))
            out.append(f'{indent}<h{lvl} id="{slugify(m.group(2))}">{_inline(m.group(2))}</h{lvl}>')
            i += 1; continue
        if st.startswith("|") and i + 1 < len(lines) and re.match(r"^\|[\s:|-]+\|$", lines[i + 1].strip()):
            flush()
            head = [c.strip() for c in st.strip("|").split("|")]
            i += 2
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            t = [f'{indent}<div class="table-wrap"><table class="chapter-list chapter-table">',
                 f'{indent}  <thead><tr>' + "".join(f'<th scope="col">{_inline(h)}</th>' for h in head) + "</tr></thead>",
                 f"{indent}  <tbody>"]
            for r in rows:
                cells = "".join((f'<th scope="row">{_inline(c)}</th>' if k == 0 else f"<td>{_inline(c)}</td>") for k, c in enumerate(r))
                t.append(f"{indent}    <tr>{cells}</tr>")
            t += [f"{indent}  </tbody>", f"{indent}</table></div>"]
            out += t
            continue
        if re.match(r"^[-*]\s+", st):
            flush()
            items = []
            while i < len(lines) and re.match(r"^\s*[-*]\s+", lines[i]):
                items.append(re.sub(r"^\s*[-*]\s+", "", lines[i]).strip())
                i += 1
                while i < len(lines) and lines[i].startswith("  ") and lines[i].strip() and not re.match(r"^\s*[-*]\s+", lines[i]):
                    items[-1] += " " + lines[i].strip(); i += 1
            out.append(f"{indent}<ul>" + "".join(f"<li>{_inline(x)}</li>" for x in items) + "</ul>")
            continue
        if re.match(r"^\d+\.\s+", st):
            flush()
            items = []
            while i < len(lines) and re.match(r"^\s*\d+\.\s+", lines[i]):
                items.append(re.sub(r"^\s*\d+\.\s+", "", lines[i]).strip()); i += 1
            out.append(f"{indent}<ol>" + "".join(f"<li>{_inline(x)}</li>" for x in items) + "</ol>")
            continue
        if st.startswith(">"):
            flush()
            q = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                q.append(lines[i].strip()[1:].strip()); i += 1
            out.append(f'{indent}<blockquote class="chapter-quote">' + "".join(f"<p>{_inline(x)}</p>" for x in " ".join(q).split("  ") if x) + "</blockquote>")
            continue
        para.append(st)
        i += 1
    flush()
    return "\n".join(out) + "\n"


def try_prompt(ch):
    """The 'Try it with your AI' prompt (the first blockquote after that heading), or ''."""
    m = re.search(r"^##\s+Try it with your AI\s*$(.*?)(?=^##\s|\Z)", ch["_text"], re.M | re.S)
    if not m:
        return ""
    q = [ln.strip()[1:].strip() for ln in m.group(1).splitlines() if ln.strip().startswith(">")]
    return " ".join(q)


def featured_prompt(ch):
    """Copy-paste prompt: score a company against the chapter's featured 100 words."""
    if not ch.get("_feat_text"):
        return ""
    return (f"Read \"{ch['_feat_title']}\" in {BASE}{ch['_url']}index.md (Chapter {ch['n']} of Clark Huang's free OpenBook, "
            "Silicon Valley C Players). Then score my company, or my team, against it, one line at a time. For each line: "
            "is it sick, well, or fit, and what evidence would prove that? Interview me one question at a time before you score; "
            "do not invent facts about my company. Finish with the two lines to work on first, one benchmark I could time every quarter, "
            "and the event I would least like to see come out of the hopper.")


def featured_md(ch):
    if not ch.get("_feat_text"):
        return []
    return [f"## {ch['_feat_title']}", "", f"> {ch['_feat_text']}", "",
            f"An adaptation of Greg Glassman's “World-Class Fitness in 100 Words” (CrossFit Journal, October 2002), written for this book. Source text: {BASE}{ch['_src_url']}{ch.get('featured_file') or 'business-fitness-100.md'}", "",
            "### Score your company against it (copy-paste prompt)", "", "> " + featured_prompt(ch), ""]


# ------------------------------------------------------------------ helpers shared with gen.py
def mmss(t):
    t = int(t or 0); return f"{t // 60}:{t % 60:02d}"


def iso_dur(t):
    t = int(t or 0); return f"PT{t // 60}M{t % 60}S"


def video_chapters(site, ch):
    p = os.path.join(site, "videos", ch.get("chapters_json") or "")
    if ch.get("chapters_json") and os.path.isfile(p):
        try:
            return json.load(open(p, encoding="utf-8"))
        except ValueError:
            return []
    return []


def media(site, ch, G=None):
    """Duration, dates and paths for a chapter's video and audio."""
    probe = (G.probe if G else (lambda p: None))
    v = ch.get("video"); a = ch.get("audio")
    vpath = f"/videos/{v}" if v else None
    apath = f"/audio/{a}" if a else None
    poster = f"/videos/posters/{ch['poster']}" if ch.get("poster") else None
    vdur = probe(site + vpath) if (vpath and os.path.exists(site + vpath)) else None
    vdur = vdur or ch.get("duration_seconds")
    adur = probe(site + apath) if (apath and os.path.exists(site + apath)) else None
    adur = adur or vdur
    dates = None
    if G and vpath and os.path.exists(site + vpath):
        dates = G.media_dates.dates_for(vpath.lstrip("/"), site=site)
    return {"vpath": vpath, "apath": apath, "poster": poster, "vdur": vdur, "adur": adur, "dates": dates,
            "captions": f"/videos/{ch['captions']}" if ch.get("captions") else None,
            "audio_captions": f"/audio/{ch['audio_captions']}" if ch.get("audio_captions") else None,
            "chapters": video_chapters(site, ch)}


def catalog(site, G=None):
    """Entries for book.json "chapters"."""
    out = []
    for ch in load_chapters(site):
        m = media(site, ch, G)
        e = {"id": ch["id"], "number": ch["n"], "title": ch["title"], "subtitle": ch.get("subtitle"),
             "part": ch.get("part"), "status": ch.get("status", "drafted"), "nonfiction": bool(ch.get("nonfiction", True)),
             "summary": ch["summary"], "rule": ch.get("rule"),
             "page_url": BASE + ch["_url"], "markdown_url": BASE + ch["_url"] + "index.md", "agents_url": BASE + ch["_url"] + "AGENTS.md",
             "text_url": BASE + ch["_src_url"] + "chapter.md", "transcript_url": BASE + ch["_src_url"] + "transcript.md",
             "build_url": BASE + ch["_src_url"] + "BUILD.md", "outline_id": ch.get("outline_id")}
        if ch.get("thesis"):
            e["thesis"] = {"text": ch["thesis"], "by": ch.get("thesis_by") or "Clark Huang", "kind": "opinion"}
        if ch.get("_feat_text"):
            e["featured"] = {"title": ch["_feat_title"], "text": ch["_feat_text"],
                             "source_url": BASE + ch["_src_url"] + (ch.get("featured_file") or "business-fitness-100.md"),
                             "adapted_from": "Greg Glassman, “World-Class Fitness in 100 Words,” CrossFit Journal, October 2002: https://library.crossfit.com/free/pdf/CFJ-trial.pdf",
                             "score_prompt": featured_prompt(ch)}
        if m["vpath"]:
            e["video"] = {"url": BASE + m["vpath"], "duration_seconds": round(m["vdur"], 1) if m["vdur"] else None,
                          **({k: m["dates"][k] for k in ("published", "published_at", "updated", "updated_at") if m["dates"] and m["dates"].get(k)}),
                          "poster_url": BASE + m["poster"] if m["poster"] else None,
                          "captions_url": BASE + m["captions"] if m["captions"] else None,
                          "chapters_url": BASE + "/videos/" + ch["chapters_json"] if ch.get("chapters_json") else None,
                          "bookmark_key": f"{ch['bookmark']}@<version>"}
        if m["apath"]:
            e["audio"] = {"url": BASE + m["apath"], "duration_seconds": round(m["adur"], 1) if m["adur"] else None,
                          "captions_url": BASE + m["audio_captions"] if m["audio_captions"] else None,
                          "bookmark_key": f"{ch['bookmark']}-audio@<version>"}
        out.append(e)
    return out


def sitemap_urls(site):
    chs = load_chapters(site)
    return ([BASE + "/book/chapters/"] if chs else []) + [BASE + c["_url"] for c in chs]


def llms_lines(site):
    chs = load_chapters(site)
    if not chs:
        return []
    lines = [f"- [Chapters you can read now]({BASE}/book/chapters/index.md): finished chapters of Silicon Valley C Players, each with the full text, a videobook and an audio track"]
    for ch in chs:
        feat = f" Includes “{ch['_feat_title']}” and a prompt to score your company against it." if ch.get("_feat_text") else ""
        lines.append(f"- [Chapter {ch['n']}: {ch['title']}]({BASE}{ch['_url']}index.md): {ch['summary']}{feat} Video, audio, captions and transcript: {BASE}{ch['_src_url']}transcript.md")
    return lines


def llms_full_md(site):
    chs = load_chapters(site)
    if not chs:
        return ""
    parts = ["## Chapters you can read now", ""]
    for ch in chs:
        parts += [f"### Chapter {ch['n']}: {ch['title']}", "", f"Page: {BASE}{ch['_url']} · Markdown: {BASE}{ch['_url']}index.md", ""]
        if ch.get("subtitle"):
            parts += [f"*{ch['subtitle']}*", ""]
        parts += [re.sub(r"^(#{2,4}) ", lambda mm: "##" + mm.group(1) + " ", body_markdown(ch), flags=re.M), ""]
    return "\n".join(parts) + "\n"


# ------------------------------------------------------------------ pages
def chapter_html(site, ch, m, prev_ch, next_ch):
    vpath, poster, vdur, dates = m["vpath"], m["poster"], m["vdur"], m["dates"]
    import media_dates
    blocks = []
    if vpath:
        cap = (f'\n            <track kind="captions" src="{m["captions"]}" srclang="en" label="English" default>' if m["captions"] else "")
        date_meta = (f'<span class="dates" {media_dates.attrs(dates)}>{media_dates.label_html(dates)}</span><span aria-hidden="true">·</span>'
                     if dates else "")
        blocks.append(
            f'          <div class="player"><video id="chapter-video" controls preload="metadata" playsinline width="1280" height="720"'
            + (f' poster="{poster}"' if poster else "")
            + f' data-chapter="{E(ch["bookmark"])}" aria-label="Videobook: Chapter {E(ch["n"])}, {E(ch["title"])}">\n'
            f'            <source src="{vpath}" type="video/mp4">{cap}\n'
            f'            Your browser cannot play this video. <a href="{vpath}">Download the MP4</a>.\n'
            '          </video></div>\n'
            f'          <div class="lesson-meta"><span><time datetime="{iso_dur(vdur)}">{mmss(vdur)}</time></span><span aria-hidden="true">·</span>'
            f'{date_meta}<span>Narrated in Clark\'s AI voice</span><span aria-hidden="true">·</span><a href="{vpath}" download>Download MP4</a>'
            + (f'<span aria-hidden="true">·</span><a href="{m["captions"]}">Captions (VTT)</a>' if m["captions"] else "")
            + f'<span aria-hidden="true">·</span><a href="{ch["_src_url"]}transcript.md">Transcript</a>'
            + f'<span aria-hidden="true">·</span><a href="{ch["_src_url"]}BUILD.md">How it was built</a></div>\n'
            '          <p class="resume" data-resume="chapter-video" hidden><button type="button" class="btn" data-go>Resume</button><button type="button" class="linkish" data-dismiss>Start from the beginning</button></p>\n')
    chs = m["chapters"]
    chap_list = ""
    if chs:
        items = "".join(
            f'<li><a href="{vpath}#t={c["start_seconds"]:.1f}" data-seek="{c["start_seconds"]:.1f}" data-target="chapter-video">'
            f'<span class="ts">{mmss(c["start_seconds"])}</span><span>{E(c["title"])}</span></a></li>' for c in chs)
        chap_list = (f'          <details class="chapters-wrap"><summary>Video chapters ({len(chs)})</summary>'
                     f'<ol class="chapters">{items}</ol></details>\n')
    audio = ""
    if m["apath"]:
        acap = (f'\n              <track kind="captions" src="{m["audio_captions"]}" srclang="en" label="English">' if m["audio_captions"] else "")
        audio = (
            f'          <section class="audiobox" aria-labelledby="listen-{E(ch["bookmark"])}-h">\n'
            f'            <h2 class="label" id="listen-{E(ch["bookmark"])}-h">Listen without the pictures</h2>\n'
            f'            <p class="muted" style="font-size:14px;margin:0">The same narration as an audio track · {mmss(m["adur"])} · your place is bookmarked automatically on this device</p>\n'
            f'            <audio id="chapter-audio" controls preload="metadata" data-chapter="{E(ch["bookmark"])}-audio">\n'
            f'              <source src="{m["apath"]}" type="audio/mpeg">{acap}\n'
            f'              Your browser cannot play this audio. <a href="{m["apath"]}">Download the MP3</a>.\n'
            '            </audio>\n'
            '            <p class="resume" data-resume="chapter-audio" hidden><button type="button" class="btn" data-go>Resume</button><button type="button" class="linkish" data-dismiss>Start from the beginning</button></p>\n'
            f'            <div class="downloads"><a class="dl" href="{m["apath"]}" download>Chapter MP3<small>Audio · {mmss(m["adur"])}</small></a>'
            + (f'<a class="dl" href="{vpath}" download>Chapter MP4<small>Videobook · {mmss(vdur)}</small></a>' if vpath else "")
            + '</div>\n          </section>\n')
    rule = ""
    if ch.get("rule"):
        rid = "rule-" + slugify(ch["id"])
        rule = (f'          <div class="rulecard" data-status-scope><p class="label">The rule · for you and your agents</p><p id="{rid}">{E(ch["rule"])}</p>'
                f'<p class="tools"><button type="button" class="btn ghost" data-copy="{rid}" hidden>Copy rule</button><span class="status" role="status" data-status></span></p></div>\n')
    pager = '      <nav class="pager" aria-label="Chapters">'
    pager += (f'<a class="prev" href="{prev_ch["_url"]}"><small>Previous chapter</small>Chapter {E(prev_ch["n"])}: {E(prev_ch["title"])}</a>' if prev_ch
              else '<a class="prev" href="/book/chapters/"><small>Back</small>All chapters you can read now</a>')
    pager += (f'<a class="next" href="{next_ch["_url"]}"><small>Next chapter</small>Chapter {E(next_ch["n"])}: {E(next_ch["title"])}</a>' if next_ch
              else '<a class="next" href="/book/story-arc/"><small>The whole book</small>Story arc and chapters</a>')
    pager += "</nav>\n"
    sub = f'      <p class="lede">{E(ch["subtitle"])}</p>\n' if ch.get("subtitle") else ""
    if ch.get("thesis"):
        sub += (f'      <figure class="thesis"><blockquote><p>{E(ch["thesis"])}</p></blockquote>'
                f'<figcaption>{E(ch.get("thesis_by") or "Clark Huang")}, {E(ch.get("thesis_note") or "the belief this chapter is built on")}</figcaption></figure>\n')
    part = E(ch.get("part") or "")
    body = (
        f'      <p class="crumbs"><a href="/">Home</a> / <a href="/book/">Book</a> / <a href="/book/chapters/">Chapters</a> / Chapter {E(ch["n"])}</p>\n'
        f'      <h1>{E(ch["title"])}</h1>\n'
        f'      <p class="h1-status"><span class="badge">Chapter {E(ch["n"])}</span><span class="badge dim">{part}</span><span class="badge soon">Draft · v0</span></p>\n'
        + sub +
        f'      <p class="muted">{E(ch.get("frame") or "")} <a href="/book/story-arc/#{E(ch.get("outline_id") or "")}">Where it sits in the book</a> · <a href="/book/editorial-policy/">Editorial policy</a></p>\n'
        '      <section class="audiobox preview-lead" aria-labelledby="watch-h">\n'
        '        <h2 id="watch-h">Watch the whole chapter</h2>\n'
        f'        <p class="muted" style="font-size:14px;margin:0 0 12px">{E(ch.get("video_blurb") or "")}</p>\n'
        + "".join(blocks) + chap_list +
        '      </section>\n'
        + featured_html(ch) + rule + audio +
        '      <article class="chapter-text" aria-labelledby="text-h">\n'
        '        <h2 id="text-h" class="label">Read the chapter</h2>\n'
        + md_to_html(body_markdown(ch), indent="        ") +
        '      </article>\n'
        '      <section aria-labelledby="ask-ch-h" style="margin-top:36px">\n'
        '        <h2 id="ask-ch-h">Ask, connect, contribute</h2>\n'
        f'        <p>Disagree with a correlation, or know a better one? <a href="https://github.com/clarkhuang/clarkhuang.github.io/issues/new?template=correction.yml">File a correction</a> or <a href="/contribute/">contribute with your AI</a>. If it lands, you are credited on <a href="/contributors/">Contributors</a>.</p>\n'
        '        <div data-ask-book-mount></div>\n'
        '      </section>\n'
        + pager)
    return body


def featured_html(ch):
    if not ch.get("_feat_text"):
        return ""
    pid = "prompt-" + slugify(ch["id"]) + "-score"
    return (
        f'      <section class="rulecard featured-100" aria-labelledby="feat-{E(ch["bookmark"])}-h" data-status-scope>\n'
        f'        <p class="label" id="feat-{E(ch["bookmark"])}-h">{E(ch["_feat_title"])}</p>\n'
        f'        <p class="featured-text">{E(ch["_feat_text"])}</p>\n'
        '        <p class="muted credit">An adaptation of Greg Glassman’s “World-Class Fitness in 100 Words” (<a href="https://library.crossfit.com/free/pdf/CFJ-trial.pdf">CrossFit Journal, October 2002</a>), written for this book. '
        f'Both are side by side in the chapter, under <a href="#{slugify(ch["_feat_title"])}">{E(ch["_feat_title"])}</a>.</p>\n'
        '        <h3 class="label">Score your company against it</h3>\n'
        f'        <div class="prompt-box"><pre id="{pid}" tabindex="0">{E(featured_prompt(ch))}</pre>\n'
        f'        <p class="tools"><button type="button" class="btn ghost" data-copy="{pid}" hidden>Copy prompt</button><span class="status" role="status" data-status></span></p></div>\n'
        '      </section>\n')


def chapter_md(site, ch, m):
    import media_dates
    u = BASE + ch["_url"]
    lines = [f"Chapter {ch['n']} of *Silicon Valley C Players* ({ch.get('part')}). {ch.get('frame') or ''}", ""]
    if ch.get("subtitle"):
        lines += [f"*{ch['subtitle']}*", ""]
    if ch.get("thesis"):
        lines += ["## The belief behind this chapter", "", f"> {ch['thesis']}", ">", f"> {ch.get('thesis_by') or 'Clark Huang'} ({ch.get('thesis_note') or 'the belief this chapter is built on'}). This is his view, not a measured result.", ""]
    lines += ["## Summary", "", ch["summary"], ""]
    if ch.get("rule"):
        lines += ["## The rule", "", ch["rule"], "", "This rule is written so a person or an AI agent can follow it as a standing instruction.", ""]
    lines += featured_md(ch)
    if m["vpath"]:
        lines += ["## Videobook and audio", "",
                  f"- Video (the whole chapter, narrated in Clark's AI voice): {BASE}{m['vpath']} ({mmss(m['vdur'])})"]
        dl = media_dates.md_line(m["dates"]) if m["dates"] else ""
        if dl:
            lines.append(f"- {dl}")
        if m["captions"]:
            lines.append(f"- Captions (VTT): {BASE}{m['captions']}")
        if ch.get("chapters_json"):
            lines.append(f"- Video chapters (JSON): {BASE}/videos/{ch['chapters_json']}")
        if m["apath"]:
            lines.append(f"- Audio (MP3): {BASE}{m['apath']} ({mmss(m['adur'])})")
        if m["audio_captions"]:
            lines.append(f"- Audio captions (VTT): {BASE}{m['audio_captions']}")
        lines += [f"- Transcript (as narrated): {BASE}{ch['_src_url']}transcript.md",
                  f"- How the video was built: {BASE}{ch['_src_url']}BUILD.md",
                  f"- Chapter text (Markdown source): {BASE}{ch['_src_url']}chapter.md", ""]
        if m["chapters"]:
            lines += ["### Video chapters", ""] + [f"- {mmss(c['start_seconds'])} {c['title']}" for c in m["chapters"]] + [""]
    shifted = re.sub(r"^(#{2,5}) ", lambda mm: "#" + mm.group(1) + " ", body_markdown(ch), flags=re.M)
    lines += ["## The chapter", "", shifted.rstrip(), ""]
    lines += ["## How to cite", "", f"Quote the chapter text at {u} (or {u}index.md) and give the section heading, or a video timestamp ({BASE}{m['vpath'] or ''}#t=60). "
              "This chapter is nonfiction: Clark Huang's views, with the sources listed in the chapter. Quotations from CrossFit material are from the cited public sources. "
              "The made-up subscription-billing company is an illustration, not a real company.", ""]
    return "\n".join(lines)


def index_html(chs, metas):
    import media_dates
    rows = []
    for ch, m in zip(chs, metas):
        dates = m["dates"]
        dbit = (f'<span class="dates" {media_dates.attrs(dates)}>{media_dates.label_html(dates)}</span>' if dates else "")
        rows.append(
            f'        <div class="card"><a class="card-body-link" href="{ch["_url"]}"><div class="card-meta"><span class="card-num">Chapter {E(ch["n"])} · {E(ch.get("part") or "")}</span>{dbit}</div>'
            f'<h3>{E(ch["title"])}</h3>' + (f'<p class="thesis-mini">“{E(ch["thesis"])}” — {E(ch.get("thesis_by") or "Clark Huang")}</p>' if ch.get("thesis") else '') + f'<p>{E(ch["summary"])}</p><p class="progress">Text, videobook ({mmss(m["vdur"])}) and audio</p><span class="card-cta">Read or watch</span></a></div>'
            + (f'\n        <blockquote class="chapter-quote featured-mini"><p><strong>{E(ch["_feat_title"])}.</strong> {E(ch["_feat_text"])}</p></blockquote>' if ch.get("_feat_text") else ""))
    return (
        '      <p class="crumbs"><a href="/">Home</a> / <a href="/book/">Book</a> / Chapters</p>\n'
        '      <h1>Chapters you can read now</h1>\n'
        '      <p class="lede">Silicon Valley C Players is coming in 2027. A few chapters are finished early, as v0 drafts, each with the full text, a videobook of the whole chapter, and an audio track.</p>\n'
        '      <p>Drafts can change before version one. The full chapter list, with what is drafted, outlined and planned, is on the <a href="/book/story-arc/">story arc</a> page.</p>\n'
        '      <div class="cards">\n' + "\n".join(rows) + '\n      </div>\n'
        '      <p class="muted"><a href="/book/">Back to the book</a> · <a href="/book/story-arc/">Story arc and chapters</a> · <a href="/contribute/">Contribute with your AI</a></p>\n')


def index_md(chs, metas):
    lines = ["Silicon Valley C Players is coming in 2027. A few chapters are finished early, as v0 drafts, each with the full text, a videobook of the whole chapter, and an audio track. Drafts can change before version one.", ""]
    for ch, m in zip(chs, metas):
        lines += [f"## Chapter {ch['n']}: {ch['title']}", ""] + ([f"> “{ch['thesis']}” — {ch.get('thesis_by') or 'Clark Huang'}", ""] if ch.get("thesis") else []) + [ch["summary"], "",
                  f"- Page: {BASE}{ch['_url']} · Markdown: {BASE}{ch['_url']}index.md",
                  f"- Video: {BASE}{m['vpath']} ({mmss(m['vdur'])})" if m["vpath"] else "- Video: not yet",
                  f"- Transcript: {BASE}{ch['_src_url']}transcript.md", ""]
        if ch.get("_feat_text"):
            lines += [f"### {ch['_feat_title']}", "", f"> {ch['_feat_text']}", "",
                      "Adapted from Greg Glassman's “World-Class Fitness in 100 Words” (CrossFit Journal, October 2002). Score your company against it:", "",
                      "> " + featured_prompt(ch), ""]
    lines += [f"Full chapter list: {BASE}/book/story-arc/index.md", ""]
    return "\n".join(lines)


def build_book_chapters(G):
    """Called from gen.build_book(). G is the gen module (page(), probe(), video_ld(), media_dates, SITE)."""
    import ai_friendly as AF
    site = G.SITE
    chs = load_chapters(site)
    if not chs:
        return []
    metas = [media(site, ch, G) for ch in chs]
    for k, (ch, m) in enumerate(zip(chs, metas)):
        prev_ch = chs[k - 1] if k > 0 else None
        next_ch = chs[k + 1] if k + 1 < len(chs) else None
        vld = None
        if m["vpath"]:
            vld = G.video_ld(f"Videobook: Silicon Valley C Players, Chapter {ch['n']}: {ch['title']}", ch["summary"], m["vpath"],
                             m["poster"], m["vdur"], m["dates"], captions=m["captions"])
        rel = f"book/chapters/{ch['slug']}/index.html"
        G.page(rel, f"Chapter {ch['n']}: {ch['title']} — Silicon Valley C Players", ch["summary"],
               chapter_html(site, ch, m, prev_ch, next_ch), "book", video=vld)
        AF.write_prose_twins(site, rel, f"Chapter {ch['n']}: {ch['title']}", chapter_md(site, ch, m),
                             f"Chapter {ch['n']} of Silicon Valley C Players: {ch['title']}. Nonfiction: Clark Huang's views, with sources. "
                             "The index.md has the summary, the rule, links to the video, audio, captions and transcript, and the full chapter text.")
    G.page("book/chapters/index.html", "Chapters you can read now — Silicon Valley C Players",
           "Finished early chapters of Silicon Valley C Players, a free OpenBook by Clark Huang: full text, a videobook of each chapter, and audio.",
           index_html(chs, metas), "book")
    AF.write_prose_twins(site, "book/chapters/index.html", "Chapters you can read now", index_md(chs, metas),
                         "Finished early chapters of Silicon Valley C Players, each with full text, a videobook and audio.")
    return chs


def main():
    sys.path.insert(0, HERE)
    os.environ.setdefault("SITE", os.path.abspath(os.path.join(HERE, "..")))
    import gen as G
    chs = build_book_chapters(G)
    print("wrote", len(chs), "chapter page(s) under book/chapters/")


if __name__ == "__main__":
    main()
