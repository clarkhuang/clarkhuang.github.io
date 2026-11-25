#!/usr/bin/env python3
"""Build the public Story arc and chapters page from book-source/outline.json.

Callable from gen.py (build_story_arc) or on its own:

    SITE=. python3 sitegen/story_arc.py

Standalone mode writes only this page, its Markdown twin, and AGENTS.md.
It does not run the full site generator. Callers still need to keep
sitemap.xml, llms.txt, llms-full.txt, book.json, search-index.json,
and the book preview links in sync (gen.py does that on a full build;
the scoped patch path updates those files directly).
"""
from __future__ import annotations

import html
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
E = html.escape

STATUS_CLASS = {
    "drafted": "badge",
    "outlined": "badge dim",
    "planned": "badge soon",
}

PAGE_TITLE = "Story arc and chapters — Silicon Valley C Players"
PAGE_DESC = (
    "Working story arc and chapter list for Silicon Valley C Players, "
    "a free OpenBook by Clark Huang. The outline will change."
)


def load_outline(site):
    path = os.path.join(site, "book-source", "outline.json")
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def hook_text(ch):
    hook = ch.get("hook") or ""
    if ch.get("needs_story") and "needs a story" not in hook.lower():
        if hook.endswith("."):
            hook = hook + " Needs a story."
        else:
            hook = hook + ". Needs a story."
    return hook


GUEST_ROOT = "/book/guest/"


def _guest_title(site, slug):
    try:
        import guest_stories as G
        for st in G.load_stories(site):
            if st["slug"] == slug:
                return st
    except Exception:
        pass
    return None


def guest_refs_html(ch, site=None):
    out = []
    for g in ch.get("guest_refs") or []:
        st = _guest_title(site or ".", g["slug"]) or {}
        title = st.get("title") or g["slug"]
        by = st.get("by") or ""
        handle = f' (@{st["github"]})' if st.get("github") else ""
        label = "Guest sidebar" if g.get("role") == "sidebar" else "Guest story"
        out.append(f'<br><span class="guest-ref"><strong>{E(label)}:</strong> <a href="{GUEST_ROOT}{E(g["slug"])}/">{E(title)}</a>, by {E(by)}{E(handle)}. {E(g.get("note") or "")}</span>')
    return "".join(out)


def guest_refs_md(ch, site=None):
    out = []
    for g in ch.get("guest_refs") or []:
        st = _guest_title(site or ".", g["slug"]) or {}
        title = st.get("title") or g["slug"]
        by = st.get("by") or ""
        handle = f" (@{st['github']})" if st.get("github") else ""
        label = "Guest sidebar" if g.get("role") == "sidebar" else "Guest story"
        out.append(f" {label}: [{title}](https://clarkhuang.github.io{GUEST_ROOT}{g['slug']}/index.md), by {by}{handle}. {g.get('note') or ''}".rstrip())
    return "".join(out)


def status_label(ch):
    status = ch.get("status") or "planned"
    if ch.get("needs_story"):
        return f"{status} · needs a story"
    return status


_SITE = ["."]


def table_html(section):
    chapters = section["chapters"]
    has_lessons = any(c.get("lessons") for c in chapters)
    heads = ["Ch", "Title", "What goes in it"]
    if has_lessons:
        heads.append("Site lessons")
    heads.append("Status")
    rows = ["        <div class=\"table-wrap\">",
            "        <table class=\"chapter-list\">",
            "          <thead><tr>" + "".join(f"<th>{E(h)}</th>" for h in heads) + "</tr></thead>",
            "          <tbody>"]
    for c in chapters:
        n = c.get("n") or "—"
        title = c.get("title") or ""
        hook = hook_text(c)
        status = c.get("status") or "planned"
        badge = STATUS_CLASS.get(status, "badge dim")
        label = status_label(c) + (" · read now" if c.get("url") else "")
        cid = c.get("id") or ""
        cells = [
            f'<th scope="row" class="ch">{E(str(n))}</th>',
            (f'<td class="ch-title"><a href="{E(c["url"])}">{E(title)}</a></td>' if c.get("url") else f'<td class="ch-title">{E(title)}</td>'),
            f'<td class="ch-hook">{E(hook)}{guest_refs_html(c, _SITE[0])}</td>',
        ]
        if has_lessons:
            cells.append(f'<td class="ch-lessons">{E(c.get("lessons") or "—")}</td>')
        cells.append(
            f'<td class="ch-status"><span class="{badge}">{E(label)}</span></td>'
        )
        id_attr = f' id="{E(cid)}"' if cid else ""
        rows.append(f"          <tr{id_attr}>{''.join(cells)}</tr>")
    rows += ["          </tbody>", "        </table>", "        </div>"]
    return "\n".join(rows)


def _counts(data):
    c = {"drafted": 0, "outlined": 0, "planned": 0}
    for half in data["halves"]:
        for sec in half["sections"]:
            for ch in sec["chapters"]:
                c[ch.get("status") or "planned"] = c.get(ch.get("status") or "planned", 0) + 1
    return c


def _readable(data):
    return [ch for half in data["halves"] for sec in half["sections"] for ch in sec["chapters"] if ch.get("url")]


def body_html(data):
    cnt = _counts(data)
    new = _readable(data)
    extra = [f'      <p class="muted">Right now: {cnt["drafted"]} drafted · {cnt["outlined"]} outlined · {cnt["planned"]} planned.</p>']
    for ch in new:
        extra.append(f'      <p class="new-chapter-banner"><span class="badge">New</span> Chapter {E(str(ch.get("n")))}, <a href="{E(ch["url"])}">{E(ch.get("title") or "")}</a>, is finished: text, a full-chapter video and audio. <a href="#{E(ch.get("id") or "")}">See where it sits</a>.</p>')
    parts = [
        '      <p class="crumbs"><a href="/">Home</a> / <a href="/book/">Book</a> / Story arc and chapters</p>',
        "      <h1>Story arc and chapters</h1>",
        f'      <p class="h1-status"><span class="badge soon">Working outline</span></p>',
        f'      <p class="lede">{E(data["throughline"])}</p>',
        *extra,
        f'      <p><strong>This outline will change</strong> as chapters are written, as interviews fill gaps, and as people contribute.</p>',
        f'      <p>{E(data["framing"])} See the <a href="/book/editorial-policy/">editorial policy</a> and the <a href="https://github.com/clarkhuang/clarkhuang.github.io/blob/main/book-source/NAMING-POLICY.md">naming policy</a>.</p>',
        '      <p>The book has two halves. The first follows the career arc: school days, then the jobs in career order, then the turn when AI came for the code writers. The second half is about this site — how to work now, the OpenBook itself, how agents can use and improve the site — and where it goes next.</p>',
        '      <p class="muted">Status: <span class="badge">drafted</span> already on the record · <span class="badge dim">outlined</span> we know what belongs here, but the chapter is not written yet · <span class="badge soon">planned</span> a seed or a slot. “Needs a story” means no source story has been given yet.</p>',
    ]
    for half in data["halves"]:
        hid = E(half["id"])
        parts.append(f'      <section class="arc-half" aria-labelledby="{hid}-h">')
        parts.append(f'        <h2 id="{hid}-h">{E(half["title"])}</h2>')
        parts.append(f'        <p>{E(half["summary"])}</p>')
        if half.get("note"):
            parts.append(f'        <p>{E(half["note"])}</p>')
        for sec in half["sections"]:
            sid = E(sec["id"])
            parts.append(f'        <h3 id="{sid}">{E(sec["title"])}</h3>')
            parts.append(table_html(sec))
        parts.append("      </section>")
    if data.get("future_notes"):
        parts.append('      <section class="arc-notes" aria-labelledby="also-planned-h">')
        parts.append('        <h2 id="also-planned-h">Also planned</h2>')
        parts.append("        <ul>")
        for note in data["future_notes"]:
            parts.append(f"          <li>{E(note)}</li>")
        parts.append("        </ul>")
        parts.append("      </section>")
    parts.append(
        '      <p class="muted">Machine-readable outline: <a href="/book-source/outline.json">book-source/outline.json</a> · Working text: <a href="/book-source/OUTLINE.md">book-source/OUTLINE.md</a> · <a href="/book/">Back to the book preview</a> · <a href="/contribute/">Contribute with your AI</a></p>'
    )
    return "\n".join(parts) + "\n"


def body_md(data):
    cnt = _counts(data)
    lines = [
        data["throughline"],
        "",
        f"Right now: {cnt['drafted']} drafted, {cnt['outlined']} outlined, {cnt['planned']} planned.",
        "",
        *sum(([f"**New:** Chapter {ch.get('n')}, [{ch.get('title')}](https://clarkhuang.github.io{ch['url']}index.md), is finished: text, a full-chapter video and audio.", ""] for ch in _readable(data)), []),
        "**This outline will change** as chapters are written, as interviews fill gaps, and as people contribute.",
        "",
        data["framing"],
        "",
        "See the [editorial policy](https://clarkhuang.github.io/book/editorial-policy/index.md) and the [naming policy](https://github.com/clarkhuang/clarkhuang.github.io/blob/main/book-source/NAMING-POLICY.md).",
        "",
        "The book has two halves. The first follows the career arc: school days, then the jobs in career order, then the turn when AI came for the code writers. The second half is about this site — how to work now, the OpenBook itself, how agents can use and improve the site — and where it goes next.",
        "",
        "Status: **drafted** (already on the record), **outlined** (we know what belongs here, but the chapter is not written yet), **planned** (a seed or a slot). “Needs a story” means no source story has been given yet.",
        "",
    ]
    for half in data["halves"]:
        lines += [f"## {half['title']}", "", half["summary"], ""]
        if half.get("note"):
            lines += [half["note"], ""]
        for sec in half["sections"]:
            lines += [f"### {sec['title']}", ""]
            has_lessons = any(c.get("lessons") for c in sec["chapters"])
            if has_lessons:
                lines.append("| Ch | Title | What goes in it | Site lessons | Status |")
                lines.append("|---|---|---|---|---|")
            else:
                lines.append("| Ch | Title | What goes in it | Status |")
                lines.append("|---|---|---|---|")
            for c in sec["chapters"]:
                n = c.get("n") or "—"
                hook = hook_text(c)
                if c.get("url"):
                    hook = f"{hook} Read it: https://clarkhuang.github.io{c['url']}"
                hook = (hook + guest_refs_md(c, _SITE[0])).replace("|", "/")
                status = status_label(c)
                if has_lessons:
                    lines.append(
                        f"| {n} | {c['title']} | {hook} | {c.get('lessons') or '—'} | {status} |"
                    )
                else:
                    lines.append(f"| {n} | {c['title']} | {hook} | {status} |")
            lines.append("")
    if data.get("future_notes"):
        lines += ["## Also planned", ""]
        for note in data["future_notes"]:
            lines.append(f"- {note}")
        lines.append("")
    lines += [
        "Machine-readable outline: https://clarkhuang.github.io/book-source/outline.json",
        "",
        "Working text: https://clarkhuang.github.io/book-source/OUTLINE.md",
        "",
        "Book preview: https://clarkhuang.github.io/book/index.md",
        "",
    ]
    return "\n".join(lines)


def build_story_arc(site=None, page=None, write_prose_twins=None):
    """Write book/story-arc/index.html, index.md, and AGENTS.md."""
    if site is None:
        import gen as G
        site = G.SITE
        page = G.page
        write_prose_twins = __import__("ai_friendly").write_prose_twins
    data = load_outline(site)
    _SITE[0] = site
    page(
        "book/story-arc/index.html",
        PAGE_TITLE,
        PAGE_DESC,
        body_html(data),
        "book",
    )
    write_prose_twins(
        site,
        "book/story-arc/index.html",
        "Story arc and chapters",
        body_md(data),
        "Working story arc and chapter list for Silicon Valley C Players. The outline will change. Do not invent stories or identify real people or companies behind the fictional names.",
    )
    return data


def main():
    sys.path.insert(0, HERE)
    os.environ.setdefault(
        "SITE",
        os.path.abspath(os.path.join(HERE, "..")),
    )
    import gen as G
    import ai_friendly as AF

    data = build_story_arc(G.SITE, G.page, AF.write_prose_twins)
    print("wrote book/story-arc/ from", len(data["halves"]), "halves")


if __name__ == "__main__":
    main()
