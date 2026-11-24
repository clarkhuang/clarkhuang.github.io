#!/usr/bin/env python3
"""Stamp a per-file version on every tracked video/audio so "watched" and saved positions reset when media changes.

Version = first 8 hex chars of the SHA-256 of the media file (the MP4 or MP3 the page plays).
assets/site.js keys its cookies on "<id>@<version>" (for example "se201/01@1a2b3c4d"), so a re-rendered
file gets a new version and shows as unwatched, with no stale resume position.

What gets stamped (attribute-only edits to committed HTML, idempotent):
  <video data-lesson-id="ID">, <video|audio data-chapter="ID">   data-video-version = hash of its first <source src>
  data-watch-id / data-toggle-watched / data-lesson-link="ID"    data-video-version = hash of lesson ID's video
  data-progress="ID1,ID2,..."                                    data-video-versions = "V1,V2,..." (same order)
  lessons.json, each lesson with a video                         "video_version" and "watched_key" ("<id>@<version>")
Lesson ID -> file comes from the lesson pages' own <video data-lesson-id> + <source>.

Usage (from the repo root):
  python3 sitegen/stamp_versions.py [SITE_DIR]           rewrite pages in place (prints what changed)
  python3 sitegen/stamp_versions.py --check [SITE_DIR]   exit 1 if any page is out of date
Run it after re-rendering ANY video or audio file. sitegen/gen.py calls stamp_site() at the end of a build,
and sitegen/check_site.py calls verify() so a re-render without re-stamping fails the check.
"""
import hashlib, json, os, re, sys

VERSION_LEN = 8
ID_ATTRS = ("data-lesson-id", "data-chapter", "data-watch-id", "data-toggle-watched", "data-lesson-link")
MEDIA_RE = re.compile(r"(<(video|audio)\b[^>]*>)(.*?)</\2>", re.S | re.I)
SOURCE_RE = re.compile(r'<source\b[^>]*\bsrc="([^"]+)"', re.I)
TAG_RE = re.compile(r"<[a-zA-Z][^<>]*>")
_cache = {}


def media_version(path):
    """Short content hash of a media file: first 8 hex chars of its SHA-256."""
    path = os.path.abspath(path)
    st = os.stat(path)
    key = (path, st.st_size, st.st_mtime_ns)
    if key not in _cache:
        h = hashlib.sha256()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(1 << 20), b""):
                h.update(chunk)
        _cache[key] = h.hexdigest()[:VERSION_LEN]
    return _cache[key]


def _attr(tag, name):
    m = re.search(r'\s' + re.escape(name) + r'="([^"]*)"', tag)
    return m.group(1) if m else None


def _set_attr(tag, name, value, after):
    """Set name="value" on a start tag: replace it if present, else insert it right after attribute `after`."""
    if _attr(tag, name) is not None:
        return re.sub(r'(\s' + re.escape(name) + r'=")[^"]*(")', lambda m: m.group(1) + value + m.group(2), tag, count=1)
    return re.sub(r'(\s' + re.escape(after) + r'="[^"]*")', lambda m: m.group(1) + f' {name}="{value}"', tag, count=1)


def _html_files(site):
    for root, dirs, files in os.walk(site):
        dirs[:] = sorted(d for d in dirs if not d.startswith(".") and d not in ("node_modules", "sitegen"))
        for f in sorted(files):
            if f.endswith(".html"):
                yield os.path.join(root, f)


def _src_file(site, src):
    return os.path.join(site, src.split("#", 1)[0].split("?", 1)[0].lstrip("/"))


def _media_tags(site, text, rel, errors):
    """(start_tag, version) for each <video>/<audio> start tag that carries a tracked id."""
    out = []
    for m in MEDIA_RE.finditer(text):
        tag = m.group(1)
        if _attr(tag, "data-lesson-id") is None and _attr(tag, "data-chapter") is None:
            continue
        s = SOURCE_RE.search(m.group(3)) or re.search(r'\ssrc="([^"]+)"', tag)
        if not s:
            errors.append(f"{rel}: {tag[:80]}... has no <source src>"); continue
        path = _src_file(site, s.group(1))
        if not os.path.isfile(path):
            errors.append(f"{rel}: media {s.group(1)} not found"); continue
        out.append((tag, media_version(path)))
    return out


def lesson_versions(site, errors=None):
    """Lesson id -> version, read from every page's <video data-lesson-id> and its first <source>."""
    errors = [] if errors is None else errors
    site = os.path.abspath(site)
    found = {}
    for path in _html_files(site):
        text = open(path, encoding="utf-8").read()
        if "data-lesson-id" not in text:
            continue
        rel = os.path.relpath(path, site)
        for tag, ver in _media_tags(site, text, rel, errors):
            lid = _attr(tag, "data-lesson-id")
            if lid is None:
                continue
            if lid in found and found[lid] != ver:
                errors.append(f"{rel}: lesson {lid} plays a different file than another page ({ver} vs {found[lid]})")
            found.setdefault(lid, ver)
    return found


def stamp_text(site, text, rel, lessons, errors):
    """Return text with every version attribute brought up to date."""
    media = dict(_media_tags(site, text, rel, errors))

    def fix(m):
        tag = m.group(0)
        if tag in media:
            after = "data-lesson-id" if _attr(tag, "data-lesson-id") is not None else "data-chapter"
            tag = _set_attr(tag, "data-video-version", media[tag], after)
        else:
            for a in ID_ATTRS[2:]:
                lid = _attr(tag, a)
                if lid is None:
                    continue
                if lid not in lessons:
                    errors.append(f"{rel}: {a}={lid!r} has no lesson video to version"); break
                tag = _set_attr(tag, "data-video-version", lessons[lid], a)
                break
        ids = _attr(tag, "data-progress")
        if ids is not None:
            ids = [i for i in ids.split(",") if i]
            missing = [i for i in ids if i not in lessons]
            if missing:
                errors.append(f"{rel}: data-progress ids without a lesson video: {', '.join(missing)}")
            else:
                tag = _set_attr(tag, "data-video-versions", ",".join(lessons[i] for i in ids), "data-progress")
        return tag

    if not any(a in text for a in ID_ATTRS + ("data-progress",)):
        return text
    return TAG_RE.sub(fix, text)


def stamp_catalog(text, lessons):
    """lessons.json with "video_version" and "watched_key" set right after "video_url" for every lesson that has a
    video, so agents can match a reader's watched cookie without scraping HTML or hashing the MP4."""
    data = json.loads(text)
    for series in data.get("series", []):
        for i, l in enumerate(series.get("lessons", [])):
            ver = lessons.get(l.get("id"))
            want = {"video_version": ver, "watched_key": f"{l['id']}@{ver}"} if ver and l.get("video_url") else {}
            rebuilt = {}
            for k, v in l.items():
                if k in ("video_version", "watched_key"):
                    continue
                rebuilt[k] = v
                if k == "video_url":
                    rebuilt.update(want)
            series["lessons"][i] = rebuilt
    return json.dumps(data, indent=2, ensure_ascii=False)


def _run(site, write):
    site = os.path.abspath(site)
    errors = []
    lessons = lesson_versions(site, errors)
    changed = []
    catalog = os.path.join(site, "lessons.json")
    if os.path.isfile(catalog):
        text = open(catalog, encoding="utf-8").read()
        new = stamp_catalog(text, lessons)
        if new != text:
            changed.append("lessons.json")
            if write:
                with open(catalog, "w", encoding="utf-8") as f:
                    f.write(new)
    for path in _html_files(site):
        text = open(path, encoding="utf-8").read()
        rel = os.path.relpath(path, site)
        new = stamp_text(site, text, rel, lessons, errors)
        if new != text:
            changed.append(rel)
            if write:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(new)
    return changed, errors


def stamp_site(site):
    """Rewrite version attributes in place. Returns (changed_files, errors)."""
    return _run(site, True)


def verify(site):
    """Error strings for pages whose version attributes do not match their media files (nothing is written)."""
    changed, errors = _run(site, False)
    return errors + [f"{rel}: video version attributes are stale or missing (run python3 sitegen/stamp_versions.py)"
                     for rel in changed]


def main(argv):
    check = "--check" in argv
    args = [a for a in argv if a != "--check"]
    site = args[0] if args else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
    if check:
        errs = verify(site)
        for e in errs: print("ERROR " + e)
        print(f"video versions: {len(errs)} error(s)")
        return 1 if errs else 0
    changed, errors = stamp_site(site)
    for rel in changed: print("stamped " + rel)
    for e in errors: print("ERROR " + e)
    print(f"video versions: {len(changed)} file(s) updated, {len(errors)} error(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
