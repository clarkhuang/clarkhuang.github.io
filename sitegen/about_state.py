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
            'Study the public courses in the format that works for you. Watch a video, follow the captions in SE 201, read a lesson transcript, or give the Markdown page to your assistant. The published courses are ' + ', '.join(courses) + '.',
            book_text,
            'The [Change Log](/change-log/) records what reached production. Its [full archive](/change-log/archive/) links each update to the public commit.'
        ]),
        ("Hands-on training in SE 301", [
            '[SE 301](/software-engineering-301/) is the playbook for running this workflow on local compute. [Lesson 1](/software-engineering-301/01-size-the-model-run-the-first-endpoint/) is available now: size a model from its weight floor, start a local endpoint and save the smoke test as a baseline on a Mac, Windows PC or Linux machine. The planned February 2027 Studio build will replay that work and add measured results; the larger machine and shared local inference remain future work.'
        ]),
        ("A possible first cohort with a nonprofit", [
            'The [SE 401 proposal](/software-engineering-401/) now defines a seven-step field build plan that starts with hosted AI and later replays the same measured work on the project’s ordered Studio. It also describes a GitHub-only member dashboard, project-scoped data and credentials, usage limits, and optional email, payment and phone adapters. That build plan, the shared hosting service and provider adapters are designs, not operating services. The site’s signed-in Reader is the current working example.',
            'The [nonprofit programs guide](/about/nonprofit-programs.md) records possible software and infrastructure benefits and the provider terms that must be confirmed before sponsoring an independently run member app. One candidate cohort is work a nonprofit and its advisor could explore with eCIO. Staff would trace a gift from receipt to allocation, count follow-ups on real cases and see whether a second nonprofit can repeat the process with a standard file import.',
            'A nonprofit would help choose the problem and decide which results to share. A possible ending for the book is a first funded cohort showing its work to the staff who use it. That scene depends on what the cohort actually builds.'
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
