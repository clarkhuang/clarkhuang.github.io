"""Generate the public history from a complete production checkout (Python 3.12+).

For the next production merge, edit release_note in change_log_editorial.json.
Its summary describes the change to a learner. Its technical_summary is shown
with implementation evidence. Unchanged notes are never repeated on later releases.
"""
import argparse
from collections import defaultdict
from datetime import date, datetime
from html import escape
import json
from pathlib import Path
import re
import subprocess
from zoneinfo import ZoneInfo

import ai_friendly
import gen

ROOT = Path(__file__).resolve().parents[1]
EDITORIAL = Path(__file__).with_name("change_log_editorial.json")
ET = ZoneInfo("America/Detroit")
COMMITS = "https://github.com/clarkhuang/clarkhuang.github.io/commit/"
VIEWS = {"daily": "Daily", "weekly": "Weekly", "monthly": "Monthly", "archive": "Full Archive"}


def affected_areas(paths):
    groups = {
        "the learning profile": ("integrations/reader-sync/templates/profile", "integrations/reader-sync/static/profile"),
        "account sign-in": ("integrations/reader-sync/pages_login.py",),
        "the Change Log": ("sitegen/change_log", "assets/change-log.js"),
        "My learning": ("my-learning/", "sitegen/my_learning.py"),
        "the OpenBook": ("book-source/", "sitegen/book_chapters.py"),
        "the courses": ("lesson-sources/", "sitegen/content.json", "software-engineering-", "ai-tips/"),
        "reader accounts": ("integrations/reader-sync/",),
        "site navigation and display": ("assets/site.js", "sitegen/site.js", "styles.css", "sitegen/site.css"),
    }
    return [label for label, prefixes in groups.items() if any(path.startswith(prefixes) for path in paths)]


def release_note(repo, rev):
    # Read the note as it existed in this specific production revision.
    path = "sitegen/change_log_editorial.json"
    result = subprocess.run(["git", "-C", repo, "show", f"{rev}:{path}"],
                            capture_output=True, text=True)
    if result.returncode:
        return {}
    note = json.loads(result.stdout).get("release_note", {})
    if not isinstance(note, dict) or not isinstance(note.get("summary"), str):
        return {}
    return note


def read_releases(repo, ref, notes, technical_notes):
    def git(*args):
        return subprocess.check_output(["git", "-C", repo, *args], text=True).strip()

    if git("rev-parse", "--is-shallow-repository") == "true":
        raise ValueError("A full production history is required. Fetch with fetch-depth: 0.")
    rows = git("log", "--first-parent", "--reverse", "--format=%H%x09%cI%x09%s", ref)
    releases = []
    for number, line in enumerate(rows.splitlines(), start=1):
        sha, timestamp, subject = line.split("\t", 2)
        note = notes.get(sha[:7])
        pr = re.match(r"Merge pull request #(\d+)\b", subject)
        authored = bool(note)
        technical = technical_notes.get(sha[:7], "")
        if not note:
            paths = (git("diff", "--name-only", f"{sha}^1", sha) if number > 1
                     else git("diff-tree", "--root", "--no-commit-id", "--name-only", "-r", sha)).splitlines()
            if "sitegen/change_log_editorial.json" in paths:
                upcoming = release_note(repo, sha)
                previous = release_note(repo, f"{sha}^1") if number > 1 else {}
                if upcoming and upcoming != previous:
                    note = upcoming["summary"].strip()
                    technical = upcoming.get("technical_summary", "")
                    authored = bool(note)
            if not note:
                areas = affected_areas(paths)
                note = ("This update includes changes to " + " and ".join(areas[:2]) + "."
                        if areas else "The site received a maintenance update.")
        record = dict(sha=sha, sequence=number, published_at=timestamp, url=COMMITS + sha,
                      summary=note, editorial=authored, technical_summary=technical,
                      pull_request=int(pr[1]) if pr else None)
        releases.append(record)
    return releases


def periods(releases, notes):
    grouped = {scale: defaultdict(list) for scale in ("daily", "weekly", "monthly")}
    for release in reversed(releases):
        day = datetime.fromisoformat(release["published_at"]).astimezone(ET).date()
        iso_year, iso_week, _ = day.isocalendar()
        keys = [day.isoformat(), f"{iso_year}-W{iso_week:02}", day.strftime("%Y-%m")]
        for groups, key in zip(grouped.values(), keys):
            groups[key].append(release)
    result = {}
    for scale, groups in grouped.items():
        result[scale] = []
        for key in sorted(groups, reverse=True):
            entries = groups[key]
            by_id = {r["sha"][:7]: r for r in entries}
            note = notes[scale].get(key)
            # A staging preview can target an earlier production ref. Never
            # imply that an outcome has shipped before its cited evidence lands.
            reviewed = bool(note and all(prefix in by_id for prefix in note[2]))
            if reviewed:
                title, summary, sources = note
                source_urls = [by_id[prefix]["url"] for prefix in sources]
                covered = max(by_id[prefix]["sequence"] for prefix in sources)
                newer = [r for r in entries if r["sequence"] > covered and r["editorial"]]
                if newer:
                    summary += " " + newer[0]["summary"]
                    source_urls.append(newer[0]["url"])
            else:
                title = "Updates to the learning site"
                highlights = []
                for entry in entries:
                    if entry["summary"] not in {r["summary"] for r in highlights}:
                        highlights.append(entry)
                    if len(highlights) == 2:
                        break
                summary = " ".join(entry["summary"] for entry in highlights)
                source_urls = [entry["url"] for entry in highlights]
            result[scale].append(dict(period=key, title=title, summary=summary, sources=source_urls,
                                      release_count=len(entries), editorial=reviewed,
                                      unreviewed_count=sum(not r["editorial"] for r in entries)))
    return result


def link(label, url):
    return (f'<a href="{escape(url, quote=True)}">{escape(label)}</a>', f'[{label}]({url})')


def paragraph(text):
    return (f"<p>{escape(text)}</p>", text)


def heading(text, anchor=None):
    attr = f' id="{escape(anchor)}"' if anchor else ""
    return (f"<h2{attr}>{escape(text)}</h2>", f"## {text}")


def links(items):
    return ("<p>" + " · ".join(h for h, m in items) + "</p>", " · ".join(m for h, m in items))


def period_number(key):
    if "-W" in key:
        year, week = key.split("-W")
        start = date.fromisocalendar(int(year), int(week), 1)
        return ((start - date(1970, 1, 1)).days + 3) // 7
    if len(key) == 7:
        year, month = map(int, key.split("-"))
        return year * 12 + month - 1
    return (date.fromisoformat(key) - date(1970, 1, 1)).days


def filter_control(scale, show_all=False):
    unit, count = {"daily": ("days", 7), "weekly": ("weeks", 4), "monthly": ("months", 3)}[scale]
    return (f'<form hidden class="history-filter" data-history-filter="{scale}" data-initial-window="{"all" if show_all else "recent"}">'
            '<div class="history-filter-controls"><label for="periods">Show the last</label>'
            f'<span class="history-quantity"><input id="periods" name="periods" aria-label="Number of {unit}" '
            f'type="number" inputmode="numeric" value="{count}" min="1" max="9999" required>'
            f'<span>{unit}</span></span>'
            '<button class="btn" type="submit">Apply</button>'
            '<button class="btn ghost" type="button" data-show-all>Show all</button></div>'
            '<p role="status" class="small muted"></p></form><script defer src="/assets/change-log.js"></script>', "")


def date_label(key):
    if "-W" in key:
        year, week = map(int, key.split("-W"))
        start = date.fromisocalendar(year, week, 1)
        return "Week of " + start.strftime("%B %-d, %Y")
    if len(key) == 7:
        return date.fromisoformat(key + "-01").strftime("%B %Y")
    return date.fromisoformat(key).strftime("%A, %B %-d, %Y")


def period_section(period):
    sources = links([link("Commit " + u[-40:-33], u) for u in period["sources"]])
    return [(f'<section class="history-period" data-period-number="{period_number(period["period"])}">', ""),
            (f'<p class="history-date">{date_label(period["period"])}</p>', date_label(period["period"])),
            heading(period["title"]), paragraph(period["summary"]),
            ('<details class="history-details"><summary>Sources and release details</summary>'
             + sources[0] + '</details></section>', sources[1])]


def release_block(release):
    day = datetime.fromisoformat(release["published_at"]).astimezone(ET)
    label = day.strftime("%b %d, %Y · %H:%M %Z")
    items = [link("Commit " + release["sha"][:7], release["url"])]
    if release["pull_request"]:
        pr = release["pull_request"]
        items.append(link(f"Pull request #{pr}", f"https://github.com/clarkhuang/clarkhuang.github.io/pull/{pr}"))
    source_html, source_md = links(items)
    tech = release["technical_summary"]
    if not tech and not release["editorial"]:
        tech = "The summary is based on the files changed in this release."
    summary = release["summary"]
    return (f'<li class="history-release" data-period-number="{period_number(day.date().isoformat())}" id="release-{release["sha"]}">'
            f'<p class="history-date"><time datetime="{escape(release["published_at"])}">{label}</time></p>'
            f'<p>{escape(summary)}</p><details class="history-details"><summary>Sources and release details</summary>'
            + (f'<p>{escape(tech)}</p>' if tech else '') + source_html + '</details></li>',
            f'- {summary} ({label}) · {source_md}' + (f' · {tech}' if tech else ""))


def render(view, active, blocks):
    path = "change-log/" + (view + "/" if view else "") + "index.html"
    title = VIEWS[active] + " · Change Log"
    nav = []
    for slug, label in VIEWS.items():
        href = "/change-log/" + slug + "/"
        current = ' aria-current="page"' if slug == active else ''
        nav.append((f'<a href="{href}"{current}>{label}</a>', f'[{label}]({href})'))
    tabs = ('<nav class="history-tabs" aria-label="Change Log views">' + "".join(h for h, _ in nav) + "</nav>",
            " · ".join(m for _, m in nav))
    feed = link("Machine-readable release history", "/change-log/history.json")
    body = [tabs, *blocks, (f'<p class="history-feed">{feed[0]}</p>', feed[1])]
    html = '<div class="history-page"><h1>Change Log</h1>' + "\n".join(h for h, _ in body) + "</div>"
    desc = "Changes to the courses, OpenBook and reader experience, with evidence from the production history."
    gen.page(path, title + " — Clark Huang", desc, html, current="change-log")
    ai_friendly.write_prose_twins(str(ROOT), path, title, "\n\n".join(m for _, m in body if m), desc)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=str(ROOT), help="Repository containing the full main history")
    parser.add_argument("--ref", default="origin/main", help="Verified production branch or production commit")
    args = parser.parse_args()
    notes = json.loads(EDITORIAL.read_text())
    releases = read_releases(args.repo, args.ref, notes["releases"], notes.get("technical", {}))
    periods_by_scale = periods(releases, notes)
    newest = list(reversed(releases))
    intro = paragraph("Browse updates to the courses, book and learning tools. Dates use Detroit time.")
    for scale, records in periods_by_scale.items():
        blocks = [intro, filter_control(scale), *(block for record in records for block in period_section(record))]
        render(scale, scale, blocks)
        if scale == "daily":
            render("", "daily", blocks)
    archive = [intro, filter_control("daily", show_all=True), ('<ol class="history-releases">', ""),
               *(release_block(r) for r in newest), ("</ol>", "")]
    render("archive", "archive", archive)
    document = {"schema_version": 1, "releases": newest, "periods": periods_by_scale}
    (ROOT / "change-log/history.json").write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n")


if __name__ == "__main__":
    main()
