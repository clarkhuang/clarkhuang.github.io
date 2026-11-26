"""Refresh the About page's current-state section from the catalogs in this checkout."""
import argparse
from html import escape
import json
from pathlib import Path
import re
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
START = "<!-- BEGIN generated project state -->"
END = "<!-- END generated project state -->"
INLINE_LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")


def read(relative):
    return json.loads((ROOT / relative).read_text())


def public_path(url):
    address = urlsplit(url)
    if address.netloc != "clarkhuang.github.io" or not address.path.startswith("/"):
        raise ValueError(f"Unexpected public catalog URL: {url}")
    return address.path


def as_html(line):
    # The source uses just ordinary paragraphs and local Markdown links.
    return INLINE_LINK.sub(r'<a href="\2">\1</a>', escape(line, quote=True))


def current_state():
    catalog = read("lessons.json")
    courses = []
    for series in catalog["series"]:
        count = sum(lesson.get("status") == "available" and bool(lesson.get("video_url"))
                    for lesson in series["lessons"])
        courses.append(f'[{series["title"]}]({public_path(series["page"])}) ({count} available)')
    book = read("book.json")
    chapters = ", ".join(f'[{chapter["title"]}]({public_path(chapter["page_url"])})'
                         for chapter in book["chapters"])
    book_text = f'The [OpenBook](/book/) is listed as a {book["status"]}.'
    if book["status"] == "preview":
        book_text += f' Its first complete edition is targeted for {book["release"]}.'
    if chapters:
        book_text += f' The chapter catalog links to {chapters}.'
    book_text += ' The [story arc](/book/story-arc/) follows the career stories into the engineering lessons and the making of this site.'
    entries = [
        ("What you can use today", [
            'Watch a lesson, read its transcript, or give the Markdown page to your assistant. The published video courses are ' + ', '.join(courses) + '.',
            book_text,
            'The [Change Log](/change-log/) records what reached production. Its [full archive](/change-log/archive/) links each update to the public commit.'
        ]),
        ("The next experiment", [
            '[SE 301](/software-engineering-301/) is the playbook for running this workflow on local compute. The planned February 2027 Studio build will test it against a real site change. Readers can already try the laptop path and share what they measure.'
        ]),
        ("What a first cohort could prove", [
            'The [SE 401 proposal](/software-engineering-401/) asks whether a team can build an affordable application that another organization can operate. One candidate comes from the work a nonprofit and an advisor may share: identifying a gift and reconciling its allocation. Staff could count the follow-ups on real cases, then see whether a second nonprofit can repeat the process with a standard file import.',
            'That pilot, an education foundation and an eCIO advisory role are ideas to test. A possible ending for the book is a funded cohort showing what it built. That scene depends on a cohort actually doing the work and its partners agreeing to share the result.'
        ])
    ]
    return entries


def update(path, body, check):
    content = path.read_text()
    if content.count(START) != 1 or content.count(END) != 1:
        raise ValueError(f"Expected one generated project state section in {path}")
    prefix, rest = content.split(START)
    _, suffix = rest.split(END)
    updated = prefix + START + "\n" + body + "\n" + END + suffix
    if updated == content:
        return
    if check:
        raise SystemExit(f"{path.name} is stale. Run python3 sitegen/about_state.py")
    path.write_text(updated)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    sections = current_state()
    html, markdown = [], []
    for title, paragraphs in sections:
        html.append(f"<h2>{escape(title)}</h2>")
        html.extend(f"<p>{as_html(p)}</p>" for p in paragraphs)
        markdown.extend([f"## {title}", *paragraphs])
    update(ROOT / "about/index.html", "\n".join(html), args.check)
    update(ROOT / "about/index.md", "\n\n".join(markdown), args.check)


if __name__ == "__main__":
    main()
