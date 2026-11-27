#!/usr/bin/env python3
"""Publish and update dates for lesson and book media, from git history.

published: the first time this path landed on origin/main (or on HEAD if it
is not on main yet — staging-only videos).
updated:   the first time the current file bytes landed on origin/main (or
HEAD). Shown only when that calendar date in America/New_York is later than
the published date.

Dates are baked into HTML, JSON-LD, lessons.json, and Markdown twins at
generate time, so new videos pick them up automatically. check_site.py
verifies the stamps when git history is available.

  python3 sitegen/media_dates.py            # print a table
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from functools import lru_cache

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_DEFAULT = os.path.abspath(os.path.join(HERE, ".."))
ZONE_NAME = "America/New_York"
MONTHS = ("Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")

try:
    from zoneinfo import ZoneInfo
    ET = ZoneInfo(ZONE_NAME)
except Exception:  # pragma: no cover
    ET = timezone.utc


def repo_root(start=None):
    """Git root for date lookups. Prefers the generator's repository, not a temp SITE copy."""
    env = os.environ.get("MEDIA_DATES_REPO")
    if env and os.path.isdir(os.path.join(env, ".git")):
        return os.path.abspath(env)
    for cand in (start, REPO_DEFAULT, os.getcwd()):
        if not cand:
            continue
        try:
            out = subprocess.run(
                ["git", "-C", cand, "rev-parse", "--show-toplevel"],
                capture_output=True, text=True, check=True,
            ).stdout.strip()
            if out:
                return out
        except (OSError, subprocess.CalledProcessError):
            continue
    return None


def _git(repo, *args):
    r = subprocess.run(["git", "-C", repo, *args], capture_output=True, text=True)
    if r.returncode != 0:
        return ""
    return r.stdout.strip()


def _main_ref(repo):
    for ref in ("origin/main", "main"):
        if _git(repo, "rev-parse", "--verify", ref):
            return ref
    return "HEAD"


def _parse_iso(ts):
    if not ts:
        return None
    ts = ts.strip()
    if ts.endswith("Z"):
        ts = ts[:-1] + "+00:00"
    try:
        dt = datetime.fromisoformat(ts)
    except ValueError:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=ET)
    return dt.astimezone(ET)


def _date(dt):
    return dt.strftime("%Y-%m-%d") if dt else None


def display(date_s):
    """'2026-11-22' -> 'Nov 22, 2026'."""
    if not date_s:
        return ""
    y, m, d = (int(x) for x in date_s.split("-"))
    return f"{MONTHS[m - 1]} {d}, {y}"


@lru_cache(maxsize=1)
def _first_adds(repo, ref):
    """path -> earliest ISO timestamp when that path was added on ref."""
    raw = _git(repo, "log", ref, "--diff-filter=A", "--format=COMMIT %aI",
               "--name-only", "--", "videos/", "audio/")
    adds, cur = {}, None
    for line in raw.splitlines():
        if line.startswith("COMMIT "):
            cur = line[len("COMMIT "):].strip()
        elif line and cur:
            # log is newest-first, so the last time we see a path is the first add
            adds[line] = cur
    return adds


def _blob_first(repo, ref, blob, path=None):
    args = ["log", ref, "--find-object", blob, "--format=%aI"]
    if path:
        args += ["--", path]
    log = _git(repo, *args)
    if not log:
        return None
    return log.splitlines()[-1].strip()  # oldest


def _file_blob(repo, path, site=None):
    file_path = None
    if site:
        cand = os.path.join(site, path)
        if os.path.isfile(cand):
            file_path = cand
    if file_path is None:
        cand = os.path.join(repo, path)
        if os.path.isfile(cand):
            file_path = cand
    if file_path:
        h = _git(repo, "hash-object", file_path)
        if h:
            return h
    return _git(repo, "rev-parse", f"HEAD:{path}")


def dates_for(path, repo=None, site=None):
    """Return a date info dict for a repo-relative media path, or None."""
    path = path.lstrip("/")
    repo = repo or repo_root()
    if not repo or not path:
        return None
    ref = _main_ref(repo)
    adds = _first_adds(repo, ref)
    published_ts = adds.get(path)
    if not published_ts:
        # Staging-only (or not yet on main): first add on HEAD
        if ref != "HEAD":
            published_ts = _first_adds(repo, "HEAD").get(path)
        if not published_ts:
            # last resort: first commit that touched the path
            log = _git(repo, "log", "--follow", "--diff-filter=A", "--format=%aI", "--", path)
            if log:
                published_ts = log.splitlines()[-1].strip()
    pub_dt = _parse_iso(published_ts)
    if not pub_dt:
        return None

    blob = _file_blob(repo, path, site)
    updated_ts = _blob_first(repo, ref, blob, path) if blob else None
    if not updated_ts and blob:
        updated_ts = _blob_first(repo, "HEAD", blob, path) or _blob_first(repo, "HEAD", blob)
    upd_dt = _parse_iso(updated_ts) if updated_ts else None
    if upd_dt and upd_dt < pub_dt:
        upd_dt = None  # shouldn't happen; don't show an "update" before publish

    show_updated = bool(upd_dt and _date(upd_dt) != _date(pub_dt))
    newness = upd_dt or pub_dt
    info = {
        "path": path,
        "published": _date(pub_dt),
        "published_at": pub_dt.isoformat(),
        "newness_at": newness.isoformat(),
        "updated": _date(upd_dt) if show_updated else None,
        "updated_at": upd_dt.isoformat() if show_updated else None,
    }
    return info


def latest(infos):
    """The most recently published-or-updated info among a list (skips None)."""
    ok = [i for i in infos if i and i.get("newness_at")]
    if not ok:
        return None
    return max(ok, key=lambda i: i["newness_at"])


def attrs(info, prefix="data-"):
    """HTML attributes: data-published, data-published-at, data-new-at, optional updated."""
    if not info:
        return ""
    parts = [
        f'{prefix}published="{info["published"]}"',
        f'{prefix}published-at="{info["published_at"]}"',
        f'{prefix}new-at="{info["newness_at"]}"',
    ]
    if info.get("updated"):
        parts.append(f'{prefix}updated="{info["updated"]}"')
        parts.append(f'{prefix}updated-at="{info["updated_at"]}"')
    return " ".join(parts)


NEW_BADGE = '<span class="badge new" data-new hidden>New</span>'


def label_html(info, kind="published"):
    """Visible date + New badge. kind is 'published' (lesson/book) or 'latest' (series/home cards)."""
    if not info:
        return NEW_BADGE
    if kind == "latest":
        d = info.get("updated") or info["published"]
        text = f'<span class="pub-date">Latest <time datetime="{d}">{display(d)}</time></span>'
        return f'{text}{NEW_BADGE}'
    pub = f'<time datetime="{info["published"]}">{display(info["published"])}</time>'
    text = f'<span class="pub-date">Published {pub}</span>'
    if info.get("updated"):
        upd = f'<time datetime="{info["updated"]}">{display(info["updated"])}</time>'
        text += f'<span aria-hidden="true"> · </span><span class="upd-date">Updated {upd}</span>'
    return f'{text}{NEW_BADGE}'


def md_line(info, kind="published"):
    if not info:
        return ""
    if kind == "latest":
        line = f"Latest video: {display(info['published'])}"
    else:
        line = f"Published: {display(info['published'])}"
    if info.get("updated"):
        line += f". Updated: {display(info['updated'])}"
    return line


def md_clause(info):
    """Short parenthetical for catalog lists: 'published Nov 22, 2026; updated Nov 24, 2026'."""
    if not info:
        return ""
    bits = [f"published {display(info['published'])}"]
    if info.get("updated"):
        bits.append(f"updated {display(info['updated'])}")
    return "; ".join(bits)


def schema_dates(info):
    if not info:
        return {}
    out = {"uploadDate": info["published"]}
    if info.get("updated"):
        out["dateModified"] = info["updated"]
    return out


DATE_ATTR_RE = re.compile(r'data-published="(\d{4}-\d{2}-\d{2})"')
JSONLD_UPLOAD_RE = re.compile(r'"uploadDate"\s*:\s*"(\d{4}-\d{2}-\d{2})"')


def verify(site, repo=None):
    """Return error strings. Skips git comparisons when history is unavailable."""
    errors = []
    site = os.path.abspath(site)
    repo = repo or repo_root(site) or repo_root()
    html_files = []
    for root, dirs, files in os.walk(site):
        dirs[:] = [d for d in dirs if d not in {".git", "node_modules"}]
        for f in files:
            if f.endswith(".html"):
                html_files.append(os.path.join(root, f))

    lesson_pages = []
    chapter_pages = []
    book_page = None
    series_pages = []
    home = None
    for path in html_files:
        rel = os.path.relpath(path, site)
        if rel == "index.html":
            home = path
        elif rel == os.path.join("book", "index.html"):
            book_page = path
        elif rel in {
            os.path.join("ai-tips", "index.html"),
            os.path.join("software-engineering-101", "index.html"),
            os.path.join("software-engineering-201", "index.html"),
        }:
            series_pages.append(path)
        elif re.match(r"(ai-tips|software-engineering-101|software-engineering-201|software-engineering-301)/[^/]+/index.html$", rel):
            lesson_pages.append((rel, path))
        elif re.match(r"book/chapters/[^/]+/index.html$", rel):
            chapter_pages.append((rel, path))

    def _has_published(text):
        return bool(DATE_ATTR_RE.search(text) and "Published " in text)

    for rel, path in lesson_pages:
        text = open(path, encoding="utf-8").read()
        if 'id="lesson-video"' not in text:
            continue  # outline pages have no video
        if not _has_published(text):
            errors.append(f"{rel}: lesson video is missing a publish date")
        if '"@type": "VideoObject"' not in text and '"@type":"VideoObject"' not in text:
            errors.append(f"{rel}: lesson page is missing VideoObject JSON-LD")
        elif not JSONLD_UPLOAD_RE.search(text):
            errors.append(f"{rel}: VideoObject JSON-LD is missing uploadDate")
        if "data-new-at=" not in text or 'data-new hidden' not in text:
            errors.append(f"{rel}: lesson is missing a New-tag hook (data-new-at / data-new)")

    for rel, path in chapter_pages:
        text = open(path, encoding="utf-8").read()
        if 'id="chapter-video"' not in text:
            continue
        if not _has_published(text):
            errors.append(f"{rel}: chapter video is missing a publish date")
        if '"@type": "VideoObject"' not in text and '"@type":"VideoObject"' not in text:
            errors.append(f"{rel}: chapter page is missing VideoObject JSON-LD")
        elif not JSONLD_UPLOAD_RE.search(text):
            errors.append(f"{rel}: VideoObject JSON-LD is missing uploadDate")
        if "data-new-at=" not in text or 'data-new hidden' not in text:
            errors.append(f"{rel}: chapter video is missing a New-tag hook (data-new-at / data-new)")

    if book_page:
        text = open(book_page, encoding="utf-8").read()
        if 'id="book-video"' in text:
            if not _has_published(text):
                errors.append("book/index.html: videobook is missing a publish date")
            if '"@type": "VideoObject"' not in text and '"@type":"VideoObject"' not in text:
                errors.append("book/index.html: missing VideoObject JSON-LD")
            elif not JSONLD_UPLOAD_RE.search(text):
                errors.append("book/index.html: VideoObject JSON-LD is missing uploadDate")
            if "data-new-at=" not in text or 'data-new hidden' not in text:
                errors.append("book/index.html: videobook is missing a New-tag hook")

    for path in series_pages:
        rel = os.path.relpath(path, site)
        text = open(path, encoding="utf-8").read()
        if 'class="vid"' in text and "data-published=" not in text:
            errors.append(f"{rel}: series lesson cards are missing publish dates")

    if home:
        text = open(home, encoding="utf-8").read()
        if "data-new-at=" not in text:
            errors.append("index.html: home series/book cards are missing data-new-at")

    # Catalog
    catalog = os.path.join(site, "lessons.json")
    if os.path.isfile(catalog):
        import json
        data = json.loads(open(catalog, encoding="utf-8").read())
        for series in data.get("series", []):
            for l in series.get("lessons", []):
                if l.get("video_url") and l.get("status") == "available" and not l.get("published"):
                    errors.append(f"lessons.json: {l.get('id')} is missing published")

    # Git comparison, only when we can resolve dates (keeps temp test copies green).
    if repo and _git(repo, "rev-parse", "--is-inside-work-tree") == "true":
        # Sample a few known files if present; full compare via stamped ISO dates.
        samples = [
            ("videos/book-preview.mp4", "book/index.html"),
            ("videos/se201-01-four-eras-of-building-systems.mp4",
             "software-engineering-201/01-four-eras-of-building-systems/index.html"),
        ]
        for media, rel in samples:
            info = dates_for(media, repo=repo, site=site)
            page = os.path.join(site, rel)
            if not info or not os.path.isfile(page):
                continue
            text = open(page, encoding="utf-8").read()
            m = DATE_ATTR_RE.search(text)
            if m and m.group(1) != info["published"]:
                errors.append(f"{rel}: data-published={m.group(1)} but git says {info['published']}")
            ju = JSONLD_UPLOAD_RE.search(text)
            if ju and ju.group(1) != info["published"]:
                errors.append(f"{rel}: JSON-LD uploadDate={ju.group(1)} but git says {info['published']}")

    return errors


def main():
    repo = repo_root()
    if not repo:
        print("no git repository found", file=sys.stderr)
        return 1
    paths = []
    for root, _, files in os.walk(os.path.join(repo, "videos")):
        for f in files:
            if f.endswith(".mp4"):
                paths.append(os.path.relpath(os.path.join(root, f), repo))
    audio = "audio/book-preview.mp3"
    if os.path.isfile(os.path.join(repo, audio)):
        paths.append(audio)
    for path in sorted(paths):
        info = dates_for(path, repo=repo)
        if not info:
            print(f"{path}: no date")
            continue
        extra = f"  updated {info['updated']}" if info.get("updated") else ""
        print(f"{path}: published {info['published']}{extra}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
