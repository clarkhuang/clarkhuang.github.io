#!/usr/bin/env python3
"""Build public guest-story pages from book-source/guest/*.md.

Does not run the full site generator. From the repository root:

    SITE="$PWD" python3 sitegen/guest_stories.py

Also hooked from sitegen/gen.py so a full rebuild stays in sync.
Source files in book-source/guest/ stay as the consented originals.
Public pages live at /book/guest/ and do not reprint the consent block;
they credit the author by the name they consented to publish.
"""
from __future__ import annotations

import html
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

E = html.escape
BASE = "https://clarkhuang.github.io"
SOURCE_DIR = "book-source/guest"
PAGE_ROOT = "book/guest"
MONTHS = {
    1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun",
    7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec",
}

FIELD_RE = re.compile(
    r"^\*\*(By|GitHub|Date):\*\*\s*(.+?)\s*$", re.I | re.M
)
HEADING_RE = re.compile(r"^#\s+(.+?)\s*$", re.M)
SECTION_RE = re.compile(r"^##\s+(.+?)\s*$", re.M)


def source_dir(site: str) -> Path:
    return Path(site) / SOURCE_DIR


def parse_date(raw: str) -> tuple[str, str]:
    """Return (iso_date, display like 'Nov 25, 2026')."""
    raw = (raw or "").strip()
    for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%b %d, %Y", "%B %d, %Y"):
        try:
            dt = datetime.strptime(raw, fmt)
            return dt.strftime("%Y-%m-%d"), f"{MONTHS[dt.month]} {dt.day}, {dt.year}"
        except ValueError:
            continue
    return raw, raw


def first_sentence(text: str) -> str:
    text = re.sub(r"\s+", " ", (text or "").strip())
    if not text:
        return ""
    m = re.match(r"(.+?[.!?])(?:\s|$)", text)
    return (m.group(1) if m else text).strip()


def handle_from(raw: str) -> str:
    return re.sub(r"^@", "", (raw or "").strip())


def split_sections(md: str) -> dict[str, str]:
    parts: dict[str, str] = {"_preamble": ""}
    current = "_preamble"
    chunks: list[str] = []
    for line in md.splitlines():
        m = SECTION_RE.match(line)
        if m:
            parts[current] = "\n".join(chunks).strip()
            current = m.group(1).strip().lower()
            chunks = []
            continue
        chunks.append(line)
    parts[current] = "\n".join(chunks).strip()
    return parts


def parse_story(path: Path) -> dict | None:
    if path.name.lower() in {"readme.md", "index.md"}:
        return None
    if path.suffix.lower() != ".md" or path.name.startswith("."):
        return None
    text = path.read_text(encoding="utf-8")
    title_m = HEADING_RE.search(text)
    if not title_m:
        print(f"warning: {path} has no title heading; skipped", file=sys.stderr)
        return None
    fields = {k.lower(): v.strip() for k, v in FIELD_RE.findall(text)}
    sections = split_sections(text)
    story = sections.get("the story") or ""
    if not story:
        print(f"warning: {path} has no 'The story' section; skipped", file=sys.stderr)
        return None
    iso, display = parse_date(fields.get("date") or "")
    slug = path.stem
    by_name = fields.get("by") or ""
    login = handle_from(fields.get("github") or "")
    lede = first_sentence(story)
    return {
        "slug": slug,
        "title": title_m.group(1).strip(),
        "by": by_name,
        "github": login,
        "date": iso,
        "date_display": display,
        "source_rel": f"{SOURCE_DIR}/{path.name}",
        "story": story,
        "lede": lede,
        "url": f"/{PAGE_ROOT}/{slug}/",
        "page_url": f"{BASE}/{PAGE_ROOT}/{slug}/",
        "markdown_url": f"{BASE}/{PAGE_ROOT}/{slug}/index.md",
        "source_url": f"{BASE}/{SOURCE_DIR}/{path.name}",
    }


def load_stories(site: str) -> list[dict]:
    folder = source_dir(site)
    if not folder.is_dir():
        return []
    stories = []
    for path in sorted(folder.glob("*.md")):
        rec = parse_story(path)
        if rec:
            stories.append(rec)
    stories.sort(key=lambda s: (s.get("date") or "", s["slug"]), reverse=True)
    return stories


def paragraphs_html(text: str) -> str:
    blocks = re.split(r"\n\s*\n", (text or "").strip())
    out = []
    for block in blocks:
        chunk = " ".join(line.strip() for line in block.splitlines() if line.strip())
        if chunk:
            out.append(f"      <p>{E(chunk)}</p>")
    return "\n".join(out)


def byline_html(story: dict) -> str:
    bits = []
    if story.get("by"):
        bits.append(E(story["by"]))
    if story.get("github"):
        login = story["github"]
        bits.append(
            f'<a href="https://github.com/{E(login, quote=True)}">@{E(login)}</a>'
        )
    name = " ".join(bits) if bits else "a guest contributor"
    date = f" · {E(story['date_display'])}" if story.get("date_display") else ""
    return f"      <p class=\"lede\">By {name}{date}</p>"


def byline_md(story: dict) -> str:
    bits = []
    if story.get("by"):
        bits.append(story["by"])
    if story.get("github"):
        login = story["github"]
        bits.append(f"[@{login}](https://github.com/{login})")
    name = " ".join(bits) if bits else "a guest contributor"
    date = f" · {story['date_display']}" if story.get("date_display") else ""
    return f"By {name}{date}."


def story_body_html(story: dict) -> str:
    title = E(story["title"])
    return f"""      <p class="crumbs"><a href="/">Home</a> / <a href="/book/">Book</a> / <a href="/{PAGE_ROOT}/">Guest stories</a> / {title}</p>
      <h1>{title}</h1>
{byline_html(story)}
{paragraphs_html(story["story"])}
      <p class="muted">This is a first-person guest story, published under the author’s name with written consent. Source: <a href="/{story['source_rel']}">{E(story['source_rel'])}</a>. The author is also listed on <a href="/contributors/">Contributors</a>.</p>
"""


def story_body_md(story: dict) -> str:
    return "\n".join([
        byline_md(story),
        "",
        story["story"].strip(),
        "",
        f"This is a first-person guest story, published under the author’s name with written consent. "
        f"Source: [{story['source_rel']}]({story['source_url']}). "
        f"The author is also listed on [Contributors]({BASE}/contributors/index.md).",
    ])


def index_body_html(stories: list[dict]) -> str:
    if stories:
        items = []
        for s in stories:
            lede = f" {E(s['lede'])}" if s.get("lede") else ""
            by = E(s["by"]) if s.get("by") else "Guest"
            date = f" · {E(s['date_display'])}" if s.get("date_display") else ""
            items.append(
                f'        <li><a href="{E(s["url"], quote=True)}">{E(s["title"])}</a>'
                f' — {by}{date}.{lede}</li>'
            )
        listing = "      <ul class=\"credit-list\">\n" + "\n".join(items) + "\n      </ul>"
    else:
        listing = "      <p>No guest stories have been published yet.</p>"
    return f"""      <p class="crumbs"><a href="/">Home</a> / <a href="/book/">Book</a> / Guest stories</p>
      <h1>Guest stories</h1>
      <p class="lede">First-person pieces published under the contributor’s own name, as themselves — not as a fictional character in the book.</p>
      <p>These are different from a regular story submission, which may be renamed and fictionalized. A guest story keeps the author’s name on the piece, after Clark accepts it and the author gives written consent to publish that name.</p>
{listing}
      <p class="muted">Want to submit one? See the format in <a href="/{SOURCE_DIR}/README.md">book-source/guest/README.md</a>, or start at <a href="/contribute/">Contribute with your AI</a>. Accepted stories are also credited on the <a href="/contributors/">Contributors</a> page.</p>
"""


def index_body_md(stories: list[dict]) -> str:
    lines = [
        "First-person pieces published under the contributor’s own name, as themselves — not as a fictional character in the book.",
        "",
        "These are different from a regular story submission, which may be renamed and fictionalized. A guest story keeps the author’s name on the piece, after Clark accepts it and the author gives written consent to publish that name.",
        "",
    ]
    if stories:
        for s in stories:
            lede = f" {s['lede']}" if s.get("lede") else ""
            by = s.get("by") or "Guest"
            date = f" · {s['date_display']}" if s.get("date_display") else ""
            lines.append(f"- [{s['title']}]({s['markdown_url']}) — {by}{date}.{lede}")
        lines.append("")
    else:
        lines += ["No guest stories have been published yet.", ""]
    lines.append(
        f"Want to submit one? See the format in [{SOURCE_DIR}/README.md]({BASE}/{SOURCE_DIR}/README.md), "
        f"or start at [Contribute with your AI]({BASE}/contribute/index.md). "
        f"Accepted stories are also credited on the [Contributors]({BASE}/contributors/index.md) page. "
        f"Machine-readable index: [{BASE}/{PAGE_ROOT}/stories.json]({BASE}/{PAGE_ROOT}/stories.json)."
    )
    return "\n".join(lines)


def write_stories_json(site: str, stories: list[dict]) -> None:
    payload = {
        "page_url": f"{BASE}/{PAGE_ROOT}/",
        "markdown_url": f"{BASE}/{PAGE_ROOT}/index.md",
        "source_dir": f"{BASE}/{SOURCE_DIR}/",
        "note": (
            "First-person guest stories published under the contributor’s own name, "
            "with written consent in the source Markdown file. These are not fictionalized book chapters."
        ),
        "stories": [
            {
                "slug": s["slug"],
                "title": s["title"],
                "by": s.get("by") or None,
                "github": s.get("github") or None,
                "date": s.get("date") or None,
                "url": s["page_url"],
                "markdown_url": s["markdown_url"],
                "source_url": s["source_url"],
                "lede": s.get("lede") or "",
            }
            for s in stories
        ],
    }
    dest = Path(site) / PAGE_ROOT / "stories.json"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def sitemap_urls(stories: list[dict] | None = None, site: str | None = None) -> list[str]:
    if stories is None:
        stories = load_stories(site or os.environ.get("SITE") or ".")
    urls = [f"{BASE}/{PAGE_ROOT}/", f"{BASE}/{PAGE_ROOT}/stories.json"]
    for s in stories:
        urls.append(s["page_url"])
    return urls


def llms_book_lines(site: str | None = None, stories: list[dict] | None = None) -> list[str]:
    if stories is None:
        stories = load_stories(site or os.environ.get("SITE") or ".")
    lines = [
        f"- [Guest stories]({BASE}/{PAGE_ROOT}/index.md): first-person guest pieces published under the contributor’s own name, not as fictional characters. Machine-readable: {BASE}/{PAGE_ROOT}/stories.json.",
    ]
    for s in stories:
        by = s.get("by") or "Guest"
        handle = f" (@{s['github']})" if s.get("github") else ""
        date = f", {s['date_display']}" if s.get("date_display") else ""
        lede = s.get("lede") or "A first-person guest story."
        lines.append(
            f"- [{s['title']}]({s['markdown_url']}): Guest story by {by}{handle}{date}. {lede}"
        )
    return lines


def build_guest_stories(site, page, write_prose_twins, stories: list[dict] | None = None) -> list[dict]:
    stories = list(stories if stories is not None else load_stories(site))
    page(
        f"{PAGE_ROOT}/index.html",
        "Guest stories — Silicon Valley C Players",
        "First-person guest stories published under the contributor’s own name, alongside Silicon Valley C Players, a free OpenBook by Clark Huang.",
        index_body_html(stories),
        "book",
    )
    write_prose_twins(
        site,
        f"{PAGE_ROOT}/index.html",
        "Guest stories",
        index_body_md(stories),
        "An index of first-person guest stories published under the contributor’s own name, not as fictional characters in the book. Do not invent stories or names.",
    )
    for s in stories:
        page(
            f"{PAGE_ROOT}/{s['slug']}/index.html",
            f"{s['title']} — Guest story",
            (s.get("lede") or s["title"])[:300],
            story_body_html(s),
            "book",
        )
        write_prose_twins(
            site,
            f"{PAGE_ROOT}/{s['slug']}/index.html",
            s["title"],
            story_body_md(s),
            f"A first-person guest story by {s.get('by') or 'a guest contributor'}, published under the author’s name with written consent. Do not invent details beyond this page.",
        )
    write_stories_json(site, stories)
    return stories


def _insert_after(text: str, needle: str, addition: str) -> str:
    if addition.strip() in text:
        return text
    if needle not in text:
        return text
    return text.replace(needle, needle + addition, 1)


def patch_sitemap(site: str, stories: list[dict]) -> None:
    path = Path(site) / "sitemap.xml"
    if not path.is_file():
        return
    text = path.read_text(encoding="utf-8")
    insert_at = f"  <url><loc>{BASE}/book/story-arc/</loc></url>\n"
    new_lines = ""
    for url in sitemap_urls(stories):
        entry = f"  <url><loc>{url}</loc></url>\n"
        if entry not in text:
            new_lines += entry
    if new_lines:
        if insert_at in text:
            text = text.replace(insert_at, insert_at + new_lines, 1)
        else:
            text = text.replace("</urlset>", new_lines + "</urlset>")
        path.write_text(text, encoding="utf-8")


def patch_llms_txt(site: str, stories: list[dict]) -> None:
    path = Path(site) / "llms.txt"
    if not path.is_file():
        return
    text = path.read_text(encoding="utf-8")
    block = "\n".join(llms_book_lines(site, stories)) + "\n"
    needle = (
        f"- [Story arc and chapters]({BASE}/book/story-arc/index.md): "
        "working story arc and chapter list for Silicon Valley C Players. The outline will change.\n"
    )
    if "book/guest/index.md" in text:
        return
    text = _insert_after(text, needle, block)
    path.write_text(text, encoding="utf-8")


def link_book_pages(site: str) -> None:
    """Surgically add guest-story links on the existing book pages (no full gen.py)."""
    html_path = Path(site) / "book" / "index.html"
    if html_path.is_file():
        html_text = html_path.read_text(encoding="utf-8")
        html_add = (
            ' First-person <a href="/book/guest/">guest stories</a>, published under the contributor’s own name, live alongside the book.'
        )
        html_needle = (
            "including a log of what changed from one edition to the next."
        )
        if 'href="/book/guest/"' not in html_text:
            html_text = _insert_after(html_text, html_needle, html_add)
            html_path.write_text(html_text, encoding="utf-8")

    md_path = Path(site) / "book" / "index.md"
    if md_path.is_file():
        md = md_path.read_text(encoding="utf-8")
        md_block = (
            "\n\n## Guest stories\n\n"
            f"First-person guest stories, published under the contributor’s own name, "
            f"not as fictional characters: [{BASE}/book/guest/]({BASE}/book/guest/index.md). "
            f"Machine-readable: [{BASE}/book/guest/stories.json]({BASE}/book/guest/stories.json).\n"
        )
        md_needle = (
            "The working story arc and chapter list: "
            f"[{BASE}/book/story-arc/]({BASE}/book/story-arc/index.md). "
            f"Machine-readable: [{BASE}/book-source/outline.json]({BASE}/book-source/outline.json). "
            "The outline will change."
        )
        if "/book/guest/" not in md:
            md = _insert_after(md, md_needle, md_block)
            md_path.write_text(md, encoding="utf-8")

    agents = Path(site) / "book" / "AGENTS.md"
    if agents.is_file():
        text = agents.read_text(encoding="utf-8")
        line = f"- Guest stories: {BASE}/book/guest/index.md\n"
        needle = f"- Story arc and chapters: {BASE}/book/story-arc/index.md\n"
        if "book/guest/" not in text:
            text = _insert_after(text, needle, line)
            # Also mention in the prose sentence if present.
            prose = " Story arc: /book/story-arc/."
            if prose in text and "Guest stories:" not in text.split("## ")[0]:
                text = text.replace(
                    prose,
                    prose + " Guest stories: /book/guest/.",
                    1,
                )
            agents.write_text(text, encoding="utf-8")


def main() -> None:
    here_root = Path(__file__).resolve().parents[1]
    os.environ["SITE"] = os.path.abspath(os.environ.get("SITE") or str(here_root))
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import ai_friendly as AF
    import gen

    stories = build_guest_stories(gen.SITE, gen.page, AF.write_prose_twins)
    patch_sitemap(gen.SITE, stories)
    patch_llms_txt(gen.SITE, stories)
    link_book_pages(gen.SITE)
    print(f"Wrote {len(stories)} guest stor{'y' if len(stories) == 1 else 'ies'} under {PAGE_ROOT}/")


if __name__ == "__main__":
    main()
