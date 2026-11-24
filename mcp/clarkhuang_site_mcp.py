#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""clarkhuang-site: a read-only MCP server for https://clarkhuang.github.io

Zero dependencies (Python 3.9+ standard library). Speaks MCP over stdio
(newline-delimited JSON-RPC 2.0). It reads the site's own public, AI-native
files (lessons.json, search-index.json, Markdown twins, AGENTS.md, WebVTT
captions) so an agent can see the site the way a reader does, then helps it
draft a GitHub issue like an outside contributor would. It never writes
anything: draft_issue returns text and a prefilled GitHub URL; a person (or
their own GitHub tooling) files it.

Run it (any one):
  uv run https://clarkhuang.github.io/mcp/clarkhuang_site_mcp.py
  python3 clarkhuang_site_mcp.py            # after downloading the file

Environment:
  CLARKHUANG_SITE   base URL or local folder to read (default
                    https://clarkhuang.github.io). Use
                    https://clarkhuang.github.io/staging to see staging, or a
                    path to a local clone to test a change before it ships.

Docs: https://clarkhuang.github.io/mcp/index.md
"""
import json, os, re, sys, urllib.request, urllib.parse, urllib.error

PROD = "https://clarkhuang.github.io"
REPO = "clarkhuang/clarkhuang.github.io"
BASE = os.environ.get("CLARKHUANG_SITE", PROD).rstrip("/")
VERSION = "1.0.1"
PROTOCOL_VERSIONS = ["2025-06-18", "2025-03-26", "2024-11-05"]
UA = "clarkhuang-site-mcp/" + VERSION
_cache = {}


def _local(base):
    return not re.match(r"^https?://", base)


def to_source(url):
    """Map a production URL (as written in lessons.json) onto BASE. Staging's own files already carry
    /staging/ URLs, so anything already under BASE is left alone."""
    if url.startswith(BASE + "/") or url == BASE:
        return url
    if url.startswith(PROD):
        url = BASE + url[len(PROD):]
    elif url.startswith("/"):
        url = BASE + url
    return url


def fetch(url, binary=False):
    url = to_source(url)
    if url in _cache:
        return _cache[url]
    if _local(BASE):
        path = urllib.parse.unquote(url[len(BASE):]).lstrip("/")
        full = os.path.join(BASE, path)
        if os.path.isdir(full) or full.endswith("/"):
            full = os.path.join(full, "index.md")
        with open(full, "rb") as f:
            data = f.read()
    else:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=30) as r:
            data = r.read()
    out = data if binary else data.decode("utf-8")
    if not binary:
        _cache[url] = out
    return out


def status_of(url):
    url = to_source(url)
    if _local(BASE):
        path = os.path.join(BASE, urllib.parse.unquote(url[len(BASE):]).lstrip("/"))
        return 200 if os.path.exists(path) else 404
    try:
        req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception as e:  # network error
        return "error: %s" % e


def catalog():
    return json.loads(fetch(PROD + "/lessons.json"))


def all_lessons():
    for s in catalog()["series"]:
        for l in s["lessons"]:
            yield s, l


def find_lesson(lesson_id):
    key = lesson_id.strip().strip("/").lower()
    for s, l in all_lessons():
        page = l.get("page_url", "").rstrip("/")
        if key in (l["id"].lower(), page.lower(), page.split("/")[-1].lower()) or page.lower().endswith("/" + key):
            return s, l
    raise ValueError("No lesson %r. Call list_lessons for ids like 'se201/02' or 'ai-tips/01'." % lesson_id)


def fmt(sec):
    sec = int(sec)
    return "%d:%02d" % (sec // 60, sec % 60)


def video_version(lesson):
    """The watched-progress version (first 8 hex of the media SHA-256): from lessons.json, else the lesson page."""
    if lesson.get("video_version"):
        return lesson["video_version"]
    try:
        html = fetch(lesson["page_url"] + "index.html" if lesson["page_url"].endswith("/") else lesson["page_url"])
        m = re.search(r'data-video-version="([0-9a-f]{8})"', html)
        return m.group(1) if m else None
    except Exception:
        return None


# ---------------------------------------------------------------- tools

def t_site_info(_):
    c = catalog()
    lines = ["# clarkhuang.github.io (read through the clarkhuang-site MCP server %s)" % VERSION,
             "Reading from: %s" % BASE, "",
             "Clark Huang's public learning site: short narrated video lessons (AI Tips, Software Engineering 101 and 201) and a preview of the free OpenBook *Silicon Valley C Players*. Everything is AI-native: every page has a Markdown twin (index.md) and an AGENTS.md.", ""]
    for s in c["series"]:
        avail = sum(1 for l in s["lessons"] if l.get("status") == "available")
        lines.append("- %s (%s): %d of %d lessons available. %s" % (s["title"], s["id"], avail, len(s["lessons"]), s["page"]))
    lines += ["", "Discovery files:"]
    for k, v in c.get("ai_readable", {}).items():
        if k != "note":
            lines.append("- %s: %s" % (k, v))
    lines += ["- lessons_json: %s/lessons.json" % PROD, "- search_index: %s/search-index.json" % PROD,
              "- redirects (moved addresses): %s/redirects.json" % PROD,
              "- mcp_manifest: %s/.well-known/mcp.json" % PROD, "- mcp_docs: %s/mcp/index.md" % PROD, "",
              "Watched progress (first-party cookies, per browser; an agent cannot read a person's cookies):"]
    for k, v in c.get("cookies", {}).items():
        lines.append("- %s: %s" % (k, v))
    lines += ["", "Staging: %s/staging/ is the next-revision branch (noindex). Production is main. Only Clark Huang merges to main." % PROD,
              "Rules for agents: do not invent stories, quotes, numbers, or biography about Clark Huang; if something is not on the site, say so."]
    return "\n".join(lines)


def t_list_lessons(a):
    series = (a.get("series") or "").lower()
    status = (a.get("status") or "").lower()
    out = []
    for s, l in all_lessons():
        if series and series not in (s["id"].lower(), s["title"].lower()):
            continue
        if status and l.get("status", "").lower() != status:
            continue
        out.append({"id": l["id"], "series": s["id"], "number": l.get("number"), "title": l["title"],
                    "status": l.get("status"), "duration": fmt(l["duration_seconds"]) if l.get("duration_seconds") else None,
                    "page_url": l.get("page_url"), "markdown_url": l.get("markdown_url")})
    return json.dumps({"count": len(out), "lessons": out}, indent=1, ensure_ascii=False)


def t_get_lesson(a):
    s, l = find_lesson(a["id"])
    include = a.get("include") or ["transcript", "chapters"]
    info = {k: v for k, v in l.items() if k not in ("chapters",)}
    info["series_title"] = s["title"]
    if l.get("duration_seconds"):
        info["duration"] = fmt(l["duration_seconds"])
    if l.get("video_url"):
        v = video_version(l)
        info["video_version"] = v
        if v:
            info["watched_key"] = "%s@%s" % (l["id"], v)
    if "chapters" in include and l.get("chapters"):
        info["chapters"] = [{"start": fmt(c["start_seconds"]), "start_seconds": c["start_seconds"], "title": c["title"]} for c in l["chapters"]]
    parts = ["```json\n" + json.dumps(info, indent=1, ensure_ascii=False) + "\n```"]
    if "transcript" in include:
        try:
            parts.append("## Markdown twin (includes the full transcript)\n\n" + fetch(l["markdown_url"]))
        except Exception as e:
            parts.append("Markdown twin unavailable: %s" % e)
    if "captions" in include and l.get("captions_url"):
        try:
            parts.append("## Captions (WebVTT)\n\n" + fetch(l["captions_url"]))
        except Exception as e:
            parts.append("Captions unavailable: %s" % e)
    if "agents" in include and l.get("agents_url"):
        try:
            parts.append("## AGENTS.md\n\n" + fetch(l["agents_url"]))
        except Exception as e:
            parts.append("AGENTS.md unavailable: %s" % e)
    return "\n\n".join(parts)


def t_check_lesson_media(a):
    ids = [a["id"]] if a.get("id") else [l["id"] for _, l in all_lessons() if l.get("video_url")]
    rows, bad = [], 0
    for i in ids:
        _, l = find_lesson(i)
        for k in ("page_url", "markdown_url", "agents_url", "video_url", "captions_url", "poster_url"):
            if l.get(k):
                st = status_of(l[k])
                if st != 200:
                    bad += 1
                rows.append({"lesson": l["id"], "field": k, "url": l[k], "status": st})
    if not a.get("id"):
        rows = [r for r in rows if r["status"] != 200]
    return json.dumps({"checked_lessons": len(ids), "problems": bad, "results": rows}, indent=1)


def t_get_page(a):
    p = a["url_or_path"].strip()
    if p.startswith(PROD):
        p = p[len(PROD):]
    if not p.startswith("/"):
        p = "/" + p
    if p.endswith(".html"):
        p = p[:-len("index.html")] if p.endswith("index.html") else p
    if p.endswith("/"):
        p += "index.md"
    return fetch(PROD + p)


def _score(q_terms, e):
    title = (e.get("title") or "").lower()
    body = " ".join(str(e.get(k) or "") for k in ("summary", "rule", "text", "series")).lower()
    sc = 0
    for t in q_terms:
        if t in title:
            sc += 5
        sc += min(body.count(t), 5)
    return sc


def t_search(a):
    q = a["query"].lower()
    terms = [t for t in re.findall(r"[a-z0-9]+", q) if len(t) > 1] or [q]
    entries = json.loads(fetch(PROD + "/search-index.json"))["entries"]
    hits = sorted(((_score(terms, e), e) for e in entries), key=lambda x: -x[0])
    out = []
    for sc, e in hits[: int(a.get("limit") or 8)]:
        if sc <= 0:
            break
        out.append({"score": sc, "id": e.get("id"), "type": e.get("type"), "title": e.get("title"),
                    "series": e.get("series"), "status": e.get("status"), "url": e.get("url"),
                    "markdown_url": e.get("markdown_url"), "summary": (e.get("summary") or "")[:300]})
    return json.dumps({"query": a["query"], "results": out}, indent=1, ensure_ascii=False)


TEMPLATES = {
    "site-bug": ("site-bug.yml", "A broken link, video, caption, page, or agent surface on the site", ["site", "bug", "needs-clark-review"]),
    "correction": ("correction.yml", "An edit to existing book text, or your side of a story already in the book", ["correction", "needs-clark-review", "openbook"]),
    "new-story": ("new-story.yml", "A new story or chapter idea for the book", ["feature", "new-story", "needs-clark-review", "openbook"]),
    "refactor": ("refactor.yml", "Cleanup or improvement that does not change facts", ["refactor", "needs-clark-review", "openbook"]),
    "takedown": ("takedown-request.yml", "Something identifies you or includes private information (agents never build these)", ["takedown-request"]),
}


def t_how_to_contribute(_):
    agents = fetch(PROD + "/AGENTS.md")
    m = re.search(r"(## How to contribute.*?)(?=\n## )", agents, re.S)
    lines = [m.group(1).strip() if m else agents, "", "## Issue templates (use draft_issue to fill one)"]
    for k, (f, d, labels) in TEMPLATES.items():
        lines.append("- %s: %s. https://github.com/%s/issues/new?template=%s (labels: %s)" % (k, d, REPO, f, ", ".join(labels)))
    lines += ["", "## Pull requests", "- Branch from `next-revision` and open the pull request into `next-revision`, never `main`. Put `Fixes #N` in the description.",
              "- Sign off every commit (`git commit -s`, DCO). Keep each page's Markdown twin (index.md), AGENTS.md and llms.txt in sync with the HTML.",
              "- Run `python3 sitegen/check_site.py .` (0 errors) and `python3 sitegen/test_watched_versions.py` before asking for review.",
              "- Staging (%s/staging/) updates when next-revision changes. Only Clark Huang merges next-revision into main." % PROD,
              "- Full rules: %s/blob/main/CONTRIBUTING.md" % ("https://github.com/" + REPO)]
    return "\n".join(lines)


def t_draft_issue(a):
    kind = a.get("kind", "site-bug")
    if kind not in TEMPLATES:
        raise ValueError("kind must be one of: %s" % ", ".join(TEMPLATES))
    f, _, labels = TEMPLATES[kind]
    title = a["title"].strip()
    sections = [("Where", a.get("page_url")), ("Steps to reproduce", a.get("steps")),
                ("Expected", a.get("expected")), ("Actual", a.get("actual")), ("Suggested fix", a.get("suggested_fix"))]
    body = "\n\n".join("### %s\n\n%s" % (h, v.strip()) for h, v in sections if v)
    if a.get("found_with"):
        body += "\n\n### Found with\n\n" + a["found_with"].strip()
    body += "\n\n_Drafted with the clarkhuang-site MCP server %s, reading %s._" % (VERSION, BASE)
    params = {"template": f, "title": title, "labels": ",".join(labels)}
    if kind == "site-bug":
        # GitHub issue forms prefill by field id.
        for fid, key in (("page", "page_url"), ("steps", "steps"), ("expected", "expected"), ("actual", "actual"), ("fix", "suggested_fix"), ("found_with", "found_with")):
            if a.get(key):
                params[fid] = a[key]
    url = "https://github.com/%s/issues/new?%s" % (REPO, urllib.parse.urlencode(params, quote_via=urllib.parse.quote))
    gh = "gh issue create -R %s --title %s --label %s --body-file issue.md" % (REPO, json.dumps(title), ",".join(labels))
    return ("This server never files issues. Review the draft, remove anything private, then either open the prefilled URL "
            "or file it with your own GitHub tooling.\n\nPrefilled URL:\n%s\n\nCLI (save the body below as issue.md):\n%s\n\n"
            "Title: %s\nLabels: %s\n\nBody:\n\n%s") % (url, gh, title, ", ".join(labels), body)


TOOLS = [
    ("site_info", "What the site is, its series and lesson counts, the machine-readable discovery files, how watched progress is keyed, and how staging and production work. Call this first.", {}, [], t_site_info),
    ("list_lessons", "List lessons across AI Tips (ai-tips), Software Engineering 101 (se101) and 201 (se201): id, title, status (available / coming soon), duration, page and Markdown URLs.",
     {"series": {"type": "string", "description": "Optional series id: ai-tips, se101 or se201."},
      "status": {"type": "string", "description": "Optional: available or 'coming soon'."}}, [], t_list_lessons),
    ("get_lesson", "Everything about one lesson: summary, standing rule, video/captions/poster URLs, duration, chapters, the watched-progress key (lesson id @ video version), and, by default, the Markdown twin with the full transcript.",
     {"id": {"type": "string", "description": "Lesson id such as 'se201/10' or 'ai-tips/01', or the lesson's page URL or slug."},
      "include": {"type": "array", "items": {"type": "string", "enum": ["transcript", "chapters", "captions", "agents"]},
                  "description": "What to add beyond the metadata. Default: transcript and chapters."}}, ["id"], t_get_lesson),
    ("check_lesson_media", "Check that a lesson's page, Markdown twin, AGENTS.md, video, captions and poster all load (HTTP status). With no id, checks every lesson with a video and returns only the problems.",
     {"id": {"type": "string", "description": "Optional lesson id."}}, [], t_check_lesson_media),
    ("get_page", "Read any page on the site as Markdown (its index.md twin), for example '/', '/book/', '/contribute/', '/software-engineering-201/' or '/AGENTS.md'.",
     {"url_or_path": {"type": "string"}}, ["url_or_path"], t_get_page),
    ("search", "Keyword search over the site's own search index (lessons, rules, book preview, pages). Returns titles, URLs and Markdown URLs to cite.",
     {"query": {"type": "string"}, "limit": {"type": "integer", "description": "Max results (default 8)."}}, ["query"], t_search),
    ("how_to_contribute", "How an outside contributor or agent files issues and opens pull requests here: templates, labels, branches (next-revision), checks, and who merges.", {}, [], t_how_to_contribute),
    ("draft_issue", "Draft a GitHub issue the way an outside contributor would (steps to reproduce, expected vs actual). Returns the body, a prefilled new-issue URL with the right template and labels, and a gh command. It does not file anything.",
     {"kind": {"type": "string", "enum": list(TEMPLATES), "description": "Default site-bug."},
      "title": {"type": "string"}, "page_url": {"type": "string"}, "steps": {"type": "string"},
      "expected": {"type": "string"}, "actual": {"type": "string"}, "suggested_fix": {"type": "string"},
      "found_with": {"type": "string", "description": "Optional: the agent and tool that found it."}}, ["title"], t_draft_issue),
]


def tool_list():
    return [{"name": n, "description": d, "inputSchema": {"type": "object", "properties": p, "required": r},
             "annotations": {"readOnlyHint": True, "openWorldHint": True}} for n, d, p, r, _ in TOOLS]


def handle(msg):
    method, mid = msg.get("method"), msg.get("id")
    if mid is None:
        return None  # notification
    if method == "initialize":
        want = (msg.get("params") or {}).get("protocolVersion")
        return {"protocolVersion": want if want in PROTOCOL_VERSIONS else PROTOCOL_VERSIONS[0],
                "capabilities": {"tools": {"listChanged": False}},
                "serverInfo": {"name": "clarkhuang-site", "version": VERSION},
                "instructions": "Read-only tools for clarkhuang.github.io. Start with site_info, then list_lessons / get_lesson / search. Use how_to_contribute and draft_issue to report problems like an outside contributor. Never invent facts about Clark Huang."}
    if method == "ping":
        return {}
    if method == "tools/list":
        return {"tools": tool_list()}
    if method == "tools/call":
        p = msg.get("params") or {}
        for n, _, _, _, fn in TOOLS:
            if n == p.get("name"):
                try:
                    return {"content": [{"type": "text", "text": fn(p.get("arguments") or {})}], "isError": False}
                except Exception as e:
                    return {"content": [{"type": "text", "text": "Error: %s" % e}], "isError": True}
        raise KeyError("Unknown tool %r" % p.get("name"))
    if method in ("resources/list", "prompts/list"):
        return {method.split("/")[0]: []}
    raise NotImplementedError(method)


def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except ValueError:
            continue
        try:
            result = handle(msg)
            if result is None:
                continue
            out = {"jsonrpc": "2.0", "id": msg.get("id"), "result": result}
        except NotImplementedError as e:
            out = {"jsonrpc": "2.0", "id": msg.get("id"), "error": {"code": -32601, "message": "Method not found: %s" % e}}
        except Exception as e:
            out = {"jsonrpc": "2.0", "id": msg.get("id"), "error": {"code": -32602, "message": str(e)}}
        sys.stdout.write(json.dumps(out, ensure_ascii=False) + "\n")
        sys.stdout.flush()


if __name__ == "__main__":
    main()
