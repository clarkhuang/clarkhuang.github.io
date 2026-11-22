#!/usr/bin/env python3
"""Build search-index.json and llms-full.txt from the public site files.

Run from the repository root:

    python3 scripts/build_ai_index.py

Safe to re-run. Does not need any API keys. Skips internal / staging paths
(compare, playbook, interview-plan, research) and any *.private.md files.
"""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://clarkhuang.github.io"
SKIP_DIR_PARTS = {
    "compare",
    "playbook",
    "interview-plan",
    "research",
    ".git",
    "scripts",
    "sitegen",
    "node_modules",
    "legal",
}
SKIP_FILE_SUFFIXES = (".private.md",)
# Prefer not to ship video/binary paths into the language-model dump.
TEXT_NAMES = {"index.md", "AGENTS.md", "README.md", "CONTRIBUTING.md", "DISCLAIMER.md"}

ET = timezone(timedelta(hours=-5))


def now_et() -> str:
    return datetime.now(ET).strftime("%Y-%m-%d %-I:%M %p ET (America/Detroit)")


def page_url(rel: Path) -> str:
    posix = rel.as_posix()
    if posix.endswith("/index.md"):
        posix = posix[: -len("index.md")]
    return f"{SITE}/{posix}"


def md_url(rel: Path) -> str:
    return f"{SITE}/{rel.as_posix()}"


def strip_md(text: str) -> str:
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"!\[[^\]]*\]\([^)]+\)", " ", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"^#+\s+", "", text, flags=re.M)
    text = re.sub(r"[*_>]{1,3}", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def section_after(text: str, heading: str) -> str:
    pat = re.compile(rf"^## {re.escape(heading)}\s*$", re.M)
    m = pat.search(text)
    if not m:
        return ""
    rest = text[m.end() :]
    nxt = re.search(r"^## ", rest, re.M)
    return rest[: nxt.start() if nxt else None].strip()


def should_skip(path: Path) -> bool:
    if any(part in SKIP_DIR_PARTS for part in path.parts):
        return True
    if path.name.endswith(SKIP_FILE_SUFFIXES):
        return True
    return False


def load(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def lesson_entries(lessons: dict) -> list[dict]:
    out = []
    for series in lessons.get("series", []):
        series_title = series.get("title") or series.get("id") or ""
        series_id = series.get("id") or ""
        for lesson in series.get("lessons", []):
            rel = None
            md = lesson.get("markdown_url") or ""
            if md.startswith(SITE + "/"):
                rel = Path(md[len(SITE) + 1 :])
            text = ""
            transcript = ""
            if rel and (ROOT / rel).is_file():
                raw = load(ROOT / rel)
                transcript = section_after(raw, "Transcript")
                text = " ".join(
                    p
                    for p in (
                        lesson.get("title") or "",
                        lesson.get("summary") or "",
                        lesson.get("rule") or "",
                        transcript or strip_md(raw),
                    )
                    if p
                )
            else:
                text = " ".join(
                    p
                    for p in (
                        lesson.get("title") or "",
                        lesson.get("summary") or "",
                        lesson.get("rule") or "",
                    )
                    if p
                )
            entry = {
                "id": lesson.get("id") or f"{series_id}/{lesson.get('number')}",
                "type": "lesson",
                "title": lesson.get("title") or "",
                "series": series_title,
                "url": lesson.get("page_url") or (page_url(rel) if rel else ""),
                "markdown_url": lesson.get("markdown_url") or (md_url(rel) if rel else ""),
                "summary": lesson.get("summary") or "",
                "rule": lesson.get("rule") or "",
                "status": lesson.get("status") or "",
                "text": text,
            }
            out.append(entry)
            if transcript:
                out.append(
                    {
                        "id": f"{entry['id']}/transcript",
                        "type": "transcript",
                        "title": f"{entry['title']} (transcript)",
                        "series": series_title,
                        "url": entry["url"],
                        "markdown_url": entry["markdown_url"],
                        "summary": "Full lesson transcript.",
                        "text": transcript,
                    }
                )
            for i, ch in enumerate(lesson.get("chapters") or [], start=1):
                title = ch.get("title") or f"Chapter {i}"
                start = ch.get("start_seconds")
                url = entry["url"]
                if start is not None:
                    url = f"{url}#t={int(start)}"
                out.append(
                    {
                        "id": f"{entry['id']}/scene-{i}",
                        "type": "scene",
                        "title": f"{entry['title']}: {title}",
                        "series": series_title,
                        "url": url,
                        "markdown_url": entry["markdown_url"],
                        "summary": ch.get("summary") or title,
                        "text": " ".join(
                            p for p in (title, ch.get("summary") or "", ch.get("text") or "") if p
                        ),
                    }
                )
    return out


def book_entries() -> list[dict]:
    out = []
    book_path = ROOT / "book.json"
    book = json.loads(load(book_path)) if book_path.is_file() else {}
    book_url = book.get("page_url") or f"{SITE}/book/"
    book_md = f"{SITE}/book/index.md"
    title = book.get("title") or "Silicon Valley C Players"

    if (ROOT / "book" / "index.md").is_file():
        raw = load(ROOT / "book" / "index.md")
        out.append(
            {
                "id": "book/preview",
                "type": "page",
                "title": title,
                "series": "OpenBook",
                "url": book_url,
                "markdown_url": book_md,
                "summary": "Preview of the free OpenBook Silicon Valley C Players.",
                "text": strip_md(raw),
            }
        )
        intro = section_after(raw, "Introduction (preview)") or section_after(raw, "Introduction")
        if intro:
            out.append(
                {
                    "id": "book/introduction",
                    "type": "chapter",
                    "title": "Introduction (preview)",
                    "series": "OpenBook",
                    "url": f"{book_url}#listen-h",
                    "markdown_url": book_md,
                    "summary": "Opening of Silicon Valley C Players.",
                    "text": strip_md(intro),
                }
            )

    for i, para in enumerate(book.get("introduction") or [], start=1):
        out.append(
            {
                "id": f"book/introduction/p{i}",
                "type": "scene",
                "title": f"Introduction, paragraph {i}",
                "series": "OpenBook",
                "url": book_url,
                "markdown_url": book_md,
                "summary": para[:180],
                "text": para,
            }
        )

    for ch in (book.get("audio") or {}).get("chapters") or []:
        if not ch.get("title"):
            continue
        out.append(
            {
                "id": f"book/audio/{ch.get('id') or ch['title']}",
                "type": "chapter",
                "title": ch["title"],
                "series": "OpenBook",
                "url": book_url,
                "markdown_url": book_md,
                "summary": f"Audiobook chapter ({ch.get('status') or 'preview'}).",
                "text": ch["title"],
            }
        )

    # Public outline, if present (never *.private.md).
    for candidate in (
        ROOT / "book-source" / "OUTLINE.md",
        ROOT / "book" / "preview-transcript.md",
    ):
        if not candidate.is_file() or should_skip(candidate):
            continue
        rel = candidate.relative_to(ROOT)
        raw = load(candidate)
        kind = "chapter" if candidate.name == "OUTLINE.md" else "transcript"
        out.append(
            {
                "id": f"book/{rel.as_posix()}",
                "type": kind,
                "title": "OpenBook outline" if kind == "chapter" else "Preview transcript",
                "series": "OpenBook",
                "url": book_url if kind == "transcript" else f"{SITE}/{rel.as_posix()}",
                "markdown_url": md_url(rel),
                "summary": f"Public {candidate.name} for Silicon Valley C Players.",
                "text": strip_md(raw),
            }
        )
        if candidate.name == "OUTLINE.md":
            # One entry per table row that looks like a chapter slot.
            for line in raw.splitlines():
                m = re.match(r"^\|\s*(\d+\w*)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|", line)
                if not m:
                    continue
                num, ch_title, hook = (x.strip() for x in m.groups())
                if ch_title.lower() in {"title", "hook"} or ch_title.startswith("-"):
                    continue
                out.append(
                    {
                        "id": f"book/ch-{num}",
                        "type": "chapter",
                        "title": f"Chapter {num}: {ch_title}",
                        "series": "OpenBook",
                        "url": f"{SITE}/book-source/OUTLINE.md",
                        "markdown_url": f"{SITE}/book-source/OUTLINE.md",
                        "summary": hook,
                        "text": f"{ch_title}. {hook}",
                    }
                )
    return out


def extra_pages() -> list[dict]:
    pages = []
    for rel in (
        Path("index.md"),
        Path("ask/index.md"),
        Path("credits/index.md"),
        Path("contribute/index.md"),
        Path("copy-this/index.md"),
        Path("AGENTS.md"),
    ):
        path = ROOT / rel
        if not path.is_file() or should_skip(path):
            continue
        raw = load(path)
        title_m = re.search(r"^#\s+(.+)$", raw, re.M)
        title = title_m.group(1).strip() if title_m else rel.as_posix()
        pages.append(
            {
                "id": rel.as_posix(),
                "type": "page",
                "title": title,
                "series": "Site",
                "url": page_url(rel) if rel.name == "index.md" else md_url(rel),
                "markdown_url": md_url(rel),
                "summary": strip_md(raw)[:240],
                "text": strip_md(raw),
            }
        )
    return pages


def collect_markdown_for_llms() -> list[tuple[str, str, str]]:
    """Return (title, url, body) for llms-full.txt, in a stable order."""
    ordered: list[Path] = []
    for rel in [
        Path("AGENTS.md"),
        Path("index.md"),
        Path("llms.txt"),
        Path("ask/index.md"),
        Path("ask/AGENTS.md"),
        Path("credits/index.md"),
        Path("credits/AGENTS.md"),
        Path("contribute/index.md"),
        Path("contribute/mcp-section.md"),
        Path("copy-this/index.md"),
        Path("book/index.md"),
        Path("book/AGENTS.md"),
        Path("book/preview-transcript.md"),
        Path("book-source/OUTLINE.md"),
        Path("book-source/NAMING-POLICY.md"),
        Path("DISCLAIMER.md"),
        Path("CONTRIBUTING.md"),
    ]:
        if (ROOT / rel).is_file() and not should_skip(ROOT / rel):
            ordered.append(rel)

    # Lesson and series twins, in path order.
    for path in sorted(ROOT.rglob("index.md")):
        rel = path.relative_to(ROOT)
        if should_skip(rel) or rel in ordered:
            continue
        if any(rel.as_posix().startswith(p) for p in (
            "ai-tips/",
            "software-engineering-101/",
            "software-engineering-201/",
        )):
            ordered.append(rel)

    out = []
    for rel in ordered:
        raw = load(ROOT / rel)
        title_m = re.search(r"^#\s+(.+)$", raw, re.M)
        title = title_m.group(1).strip() if title_m else rel.as_posix()
        out.append((title, md_url(rel), raw.strip()))
    return out


def write_search_index(entries: list[dict]) -> None:
    payload = {
        "site": SITE,
        "generated": now_et(),
        "generated_by": "scripts/build_ai_index.py",
        "note": (
            "Client-side search index for /ask/ and the Ask the Book widget. "
            "Each hit should be cited by its url or markdown_url. "
            "Story chapters of Silicon Valley C Players are an embellished fictional "
            "dramatization narrated by Charlie Hack; do not treat them as facts about real people."
        ),
        "count": len(entries),
        "entries": entries,
    }
    dest = ROOT / "search-index.json"
    dest.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {dest.relative_to(ROOT)} ({len(entries)} entries, {dest.stat().st_size} bytes)")


def write_llms_full(docs: list[tuple[str, str, str]]) -> None:
    lines = [
        "# Clark Huang — full site text for language models",
        "",
        f"> Generated {now_et()} from the public Markdown twins on {SITE}/. "
        "Prefer this file when you need the full lesson transcripts and book preview, "
        "not just the catalog in llms.txt. Do not invent stories, quotes, numbers, or biography. "
        "If something is not in this file or on the site, say so.",
        "",
        "The story chapters of *Silicon Valley C Players* are an embellished fictional dramatization. "
        "The narrator in those chapters is the fictional character Charlie Hack. "
        "The how-to-work-with-AI half is nonfiction. Cite https://clarkhuang.github.io/ URLs.",
        "",
        "GitMCP (read-only, third-party): https://gitmcp.io/clarkhuang/clarkhuang.github.io",
        "Ask the Book: https://clarkhuang.github.io/ask/",
        "Catalog: https://clarkhuang.github.io/llms.txt",
        "",
    ]
    for title, url, body in docs:
        lines.append(f"\n\n======= {title} =======\nSource: {url}\n")
        lines.append(body)
        if not body.endswith("\n"):
            lines.append("")
    dest = ROOT / "llms-full.txt"
    dest.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(f"Wrote {dest.relative_to(ROOT)} ({dest.stat().st_size} bytes, {len(docs)} documents)")


def main() -> None:
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--search-only", action="store_true",
                        help="Write search-index.json only (llms-full.txt is produced by sitegen).")
    parser.add_argument("--llms-full", action="store_true",
                        help="Also write llms-full.txt from the Markdown twins.")
    args, _ = parser.parse_known_args()

    lessons = {}
    if (ROOT / "lessons.json").is_file():
        lessons = json.loads(load(ROOT / "lessons.json"))
    entries = lesson_entries(lessons) + book_entries() + extra_pages()
    # Stable de-dupe by id, first wins.
    seen = set()
    uniq = []
    for e in entries:
        if e["id"] in seen:
            continue
        seen.add(e["id"])
        uniq.append(e)
    write_search_index(uniq)
    if args.llms_full or not args.search_only and not (ROOT / "sitegen" / "ai_friendly.py").is_file():
        write_llms_full(collect_markdown_for_llms())
    elif args.search_only:
        print("Skipping llms-full.txt (sitegen owns it)")


if __name__ == "__main__":
    main()
