"""Generate the public history from a complete production checkout (Python 3.12+)."""
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
VIEWS = {"": "Recent", "daily": "Daily", "weekly": "Weekly", "monthly": "Monthly", "archive": "Full archive"}


def read_releases(repo, ref, notes):
    def git(*args):
        return subprocess.check_output(["git", "-C", repo, *args], text=True).strip()

    if git("rev-parse", "--is-shallow-repository") == "true":
        raise ValueError("A full production history is required. Fetch with fetch-depth: 0.")
    rows = git("log", "--first-parent", "--reverse", "--format=%H%x09%cI%x09%s", ref)
    releases = []
    for number, line in enumerate(rows.splitlines(), start=1):
        sha, timestamp, subject = line.split("\t", 2)
        # Only reviewed editorial text goes into the public feed. For new releases
        # preserve the evidence without republishing arbitrary commit subjects.
        note = notes.get(sha[:7])
        pr = re.match(r"Merge pull request #(\d+)\b", subject)
        provisional = f"Production merged pull request #{pr[1]}." if pr else "A direct commit reached production."
        releases.append(dict(sha=sha, sequence=number, published_at=timestamp, url=COMMITS + sha,
                             summary=note or provisional, editorial=bool(note)))
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
            else:
                title = "Production activity"
                summary = "The production archive has the release record for this period. An editorial summary is pending."
                source_urls = [entries[0]["url"]]
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
    return (f'<form hidden data-history-filter="{scale}" data-initial-window="{"all" if show_all else "recent"}"><label>Last <input name="periods" '
            f'type="number" value="{count}" min="1" max="9999" required> {unit}</label> '
            '<button type="submit">Apply</button> <button type="button" data-show-all>Show all</button>'
            '<p role="status"></p></form><script defer src="/assets/change-log.js"></script>', "")


def period_section(period):
    return [(f'<section data-period-number="{period_number(period["period"])}">', ""),
            *period_blocks(period), ("</section>", "")]


def period_blocks(period):
    yield heading(period["period"] + " · " + period["title"])
    yield paragraph(period["summary"])
    if period["unreviewed_count"]:
        count = period["unreviewed_count"]
        yield paragraph(f"{count} production update{'s' if count != 1 else ''} awaiting an editorial note.")
    yield links([link("Commit " + u[-40:-33], u) for u in period["sources"]])


def release_block(release):
    day = datetime.fromisoformat(release["published_at"]).astimezone(ET)
    label = day.strftime("%b %d, %Y · %H:%M %Z")
    h, m = link("Commit " + release["sha"][:7], release["url"])
    summary = release["summary"] + ("" if release["editorial"] else " Editorial note pending.")
    return (f'<li data-period-number="{period_number(day.date().isoformat())}" id="release-{release["sha"]}"><strong>{escape(summary)}</strong>'
            f'<br><time datetime="{escape(release["published_at"])}">{label}</time> · {h}</li>',
            f'- {summary} ({label}) · {m}')


def render(view, blocks):
    name = "Change Log" if not view else VIEWS[view] + " · Change Log"
    path = "change-log/" + (view + "/" if view else "") + "index.html"
    nav = [link(label, "/change-log/" + (k + "/" if k else "")) for k, label in VIEWS.items() if k != view]
    body = [links(nav), *blocks, links([link("Machine-readable history", "/change-log/history.json")])]
    html = f'<h1>{name}</h1>' + "\n".join(h for h, _ in body)
    desc = "Changes to the courses, OpenBook and reader experience, with evidence from the production history."
    gen.page(path, name + " — Clark Huang", desc, html, current="change-log")
    ai_friendly.write_prose_twins(str(ROOT), path, name, "\n\n".join(m for _, m in body if m), desc)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=str(ROOT), help="Repository containing the full main history")
    parser.add_argument("--ref", default="origin/main", help="Verified production branch or production commit")
    args = parser.parse_args()
    notes = json.loads(EDITORIAL.read_text())
    releases = read_releases(args.repo, args.ref, notes["releases"])
    periods_by_scale = periods(releases, notes)
    newest = list(reversed(releases))
    intro = paragraph("Dates follow the production branch in America/Detroit. A release is dated when its commit entered main. Links open the supporting commit.")
    recent = [intro, heading("Latest releases"), ("<ul>", ""),
              *(release_block(r) for r in newest[:5]), ("</ul>", "")]
    for scale in periods_by_scale.values():
        recent.extend(period_blocks(scale[0]))
    render("", recent)
    for scale, records in periods_by_scale.items():
        render(scale, [intro, filter_control(scale), *(block for p in records for block in period_section(p))])
    archive = [intro, filter_control("daily", show_all=True), paragraph(f"{len(releases)} production updates, newest first."), ("<ol reversed>", ""),
               *(release_block(r) for r in newest), ("</ol>", "")]
    render("archive", archive)
    document = {"schema_version": 1, "releases": newest, "periods": periods_by_scale}
    (ROOT / "change-log/history.json").write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n")


if __name__ == "__main__":
    main()
