#!/usr/bin/env python3
"""Generate credits.json, credits/index.md, and credits/index.html from GitHub.

Run from the repository root (needs `gh` authenticated, or GH_TOKEN):

    python3 scripts/build_credits.py

No ANTHROPIC_API_KEY. Credits people by GitHub handle only. Honors a
'credit me as / don't credit me' answer in an issue form field. Excludes bots.
Seeds Clark Huang (@clarkhuang) as the author even when there are no
merged contributions yet.
"""
from __future__ import annotations

import html
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://clarkhuang.github.io"
REPO = os.environ.get("REPO") or os.environ.get("GITHUB_REPOSITORY") or "clarkhuang/clarkhuang.github.io"
AUTHOR_LOGIN = "clarkhuang"
ET = timezone(timedelta(hours=-5))

TYPE_LABELS = {
    "stories": {"feature", "new-story", "contributor-story", "story-seed"},
    "corrections": {"correction"},
    "refactors": {"refactor"},
    "fitness-health": {"fitness-health"},
    "code/site": {"site", "code"},
}
TYPE_ORDER = ["stories", "corrections", "refactors", "fitness-health", "code/site"]
TYPE_TITLES = {
    "stories": "Stories",
    "corrections": "Corrections",
    "refactors": "Refactors",
    "fitness-health": "Fitness and health",
    "code/site": "Code and site",
}

BOT_LOGINS = {
    "github-actions",
    "github-actions[bot]",
    "dependabot",
    "dependabot[bot]",
    "copilot",
    "copilot[bot]",
    "claude",
    "claude[bot]",
    "cursor",
    "cursor[bot]",
    "web-flow",
    "ghost",
}
BOT_PATTERNS = (re.compile(r"\[bot\]$", re.I), re.compile(r"(^|-)bot$", re.I))

DECLINE_RE = re.compile(
    r"\b(don't credit me|do not credit me|dont credit me|no credit|"
    r"please don't credit|prefer not to be credited|anonymous|"
    r"omit me|don't list me|do not list me|no attribution)\b",
    re.I,
)
CREDIT_AS_RE = re.compile(r"credit me as[:\s]+@?([A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?)", re.I)
HANDLE_RE = re.compile(r"^@?([A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?)$")
# Issue form headings GitHub renders in the issue body.
CREDIT_FIELD_RE = re.compile(
    r"###\s+Credit(?:\s+\(optional\))?.*?^\s*\n(.*?)(?=^###\s|\Z)",
    re.I | re.M | re.S,
)


def now_et() -> str:
    return datetime.now(ET).strftime("%Y-%m-%d %-I:%M %p ET (America/Detroit)")


def gh_json(args: list[str]):
    env = os.environ.copy()
    # Prefer GH_TOKEN already in the environment.
    try:
        out = subprocess.check_output(["gh", *args], text=True, env=env)
    except subprocess.CalledProcessError as e:
        print(f"gh {' '.join(args)} failed: {e}", file=sys.stderr)
        raise
    out = out.strip()
    return json.loads(out) if out else []


def is_bot(login: str | None, extra: dict | None = None) -> bool:
    if not login:
        return True
    low = login.lower()
    if low in BOT_LOGINS:
        return True
    if extra and (extra.get("is_bot") or extra.get("type") == "Bot"):
        return True
    return any(p.search(low) for p in BOT_PATTERNS)


def parse_credit_field(body: str | None) -> tuple[str | None, bool]:
    """Return (override_handle or None, declined).

    Public credits are GitHub handles only. A free-text real name in the
    credit field is ignored (never published). 'credit me as @handle' is
    honored when the value looks like a handle. Decline phrases omit the person.
    """
    if not body:
        return None, False
    field = ""
    m = CREDIT_FIELD_RE.search(body)
    if m:
        field = m.group(1).strip()
        if field in {"", "_No response_", "None", "n/a", "N/A"}:
            field = ""
    blob = field or ""
    # Also glance at a trailing 'Credit:' line if the form heading isn't present.
    if not blob:
        m2 = re.search(r"^(?:Credit|credit me as)\s*:\s*(.+)$", body, re.I | re.M)
        if m2:
            blob = m2.group(1).strip()
    if not blob:
        return None, False
    if DECLINE_RE.search(blob):
        return None, True
    as_m = CREDIT_AS_RE.search(blob)
    if as_m:
        return as_m.group(1), False
    hm = HANDLE_RE.match(blob.strip().lstrip("@"))
    # If the whole field is a single handle-like token, treat it as a handle.
    # Otherwise ignore (do not publish a real name).
    if hm and " " not in blob.strip():
        return hm.group(1), False
    return None, False


def types_for_labels(labels: list) -> list[str]:
    names = {((l.get("name") if isinstance(l, dict) else l) or "").lower() for l in labels or []}
    found = [t for t, wanted in TYPE_LABELS.items() if names & wanted]
    return found or ["code/site"]


def gh_login(user) -> str | None:
    if not user:
        return None
    if isinstance(user, str):
        return user
    return user.get("login") or user.get("name")


def collect() -> dict:
    issues = gh_json(
        [
            "issue",
            "list",
            "-R",
            REPO,
            "--state",
            "all",
            "--limit",
            "500",
            "--json",
            "number,title,url,state,author,labels,body",
        ]
    )
    # Pull comments for approved / merged-contribution story issues only, later.
    prs = gh_json(
        [
            "pr",
            "list",
            "-R",
            REPO,
            "--state",
            "all",
            "--limit",
            "500",
            "--json",
            "number,title,url,state,author,labels,mergedAt,isDraft",
        ]
    )

    # people[login_lower] = {login, types: {type: [contribs]}, declined}
    people: dict[str, dict] = {}

    def ensure(login: str) -> dict:
        key = login.lower()
        if key not in people:
            people[key] = {"login": login, "types": {t: [] for t in TYPE_ORDER}, "declined": False}
        return people[key]

    def add(login: str, typ: str, item: dict, role: str):
        if not login or is_bot(login):
            return
        person = ensure(login)
        if person["declined"]:
            return
        person["types"].setdefault(typ, [])
        rec = {
            "number": item.get("number"),
            "title": item.get("title"),
            "url": item.get("url"),
            "role": role,
        }
        # De-dupe by number+role
        if any(c["number"] == rec["number"] and c["role"] == rec["role"] for c in person["types"][typ]):
            return
        person["types"][typ].append(rec)

    def credit_login(default_login: str, body: str | None) -> str | None:
        override, declined = parse_credit_field(body)
        if declined:
            if default_login and not is_bot(default_login):
                person = ensure(default_login)
                person["declined"] = True
            return None
        return override or default_login

    approved_story_numbers = []
    for issue in issues:
        labels = issue.get("labels") or []
        names = {((l.get("name") if isinstance(l, dict) else l) or "").lower() for l in labels}
        author = gh_login(issue.get("author"))
        # Count contributions that Clark has approved, or that are closed
        # after review. "Clark's Decisions" and similar process issues are skipped.
        title = (issue.get("title") or "").strip()
        if title in {"Clark's Decisions"} or title.lower().startswith("decide ") or title.lower().startswith("confirm "):
            continue
        if "takedown-request" in names or "takedown" in names:
            continue
        is_approved = "approved" in names or "merged-contribution" in names
        # Closed issues with a contribution label also count once they are done.
        is_done = issue.get("state") == "CLOSED" and bool(names & set().union(*TYPE_LABELS.values()))
        if not (is_approved or is_done):
            continue
        types = types_for_labels(labels)
        login = credit_login(author, issue.get("body"))
        if login:
            for typ in types:
                add(login, typ, issue, "author")
        if is_approved and names & (TYPE_LABELS["stories"] | TYPE_LABELS["fitness-health"] | TYPE_LABELS["corrections"]):
            approved_story_numbers.append(issue["number"])

    # Commenters on approved story / correction / fitness issues.
    for number in approved_story_numbers:
        try:
            comments = gh_json(
                [
                    "api",
                    f"repos/{REPO}/issues/{number}/comments",
                    "--paginate",
                ]
            )
        except subprocess.CalledProcessError:
            comments = []
        if isinstance(comments, dict):
            comments = [comments]
        issue_hit = next((i for i in issues if i["number"] == number), None)
        types = types_for_labels(issue_hit.get("labels") if issue_hit else [])
        for c in comments or []:
            user = c.get("user") or {}
            login = user.get("login")
            if is_bot(login, user):
                continue
            # Don't re-parse decline from a comment unless the comment itself asks.
            body = c.get("body") or ""
            if DECLINE_RE.search(body):
                continue
            for typ in types:
                add(login, typ, issue_hit or {"number": number, "title": "", "url": c.get("html_url")}, "commenter")

    for pr in prs:
        if not pr.get("mergedAt"):
            continue
        author = gh_login(pr.get("author"))
        if is_bot(author, pr.get("author") if isinstance(pr.get("author"), dict) else None):
            continue
        types = types_for_labels(pr.get("labels") or [])
        # Merged PRs without a book-contribution label count as code/site.
        if types == ["code/site"] or not pr.get("labels"):
            types = types if pr.get("labels") else ["code/site"]
        for typ in types:
            add(author, typ, pr, "pr-author")

    # Always seed the author.
    author = ensure(AUTHOR_LOGIN)
    author["login"] = AUTHOR_LOGIN
    author["is_author"] = True

    return people


def serialize(people: dict) -> dict:
    contributors = []
    for key in sorted(people, key=lambda k: (k != AUTHOR_LOGIN, k)):
        person = people[key]
        if person.get("declined"):
            continue
        types_present = []
        grouped = {}
        for typ in TYPE_ORDER:
            items = person["types"].get(typ) or []
            if not items:
                continue
            types_present.append(typ)
            grouped[typ] = items
        if not types_present and not person.get("is_author"):
            continue
        contributors.append(
            {
                "login": person["login"],
                "url": f"https://github.com/{person['login']}",
                "roles": (["author"] if person.get("is_author") else []) + types_present,
                "contributions": grouped,
            }
        )
    return {
        "site": SITE,
        "repository": f"https://github.com/{REPO}",
        "generated": now_et(),
        "generated_by": "scripts/build_credits.py",
        "note": (
            "Credits are generated from GitHub issues and pull requests. "
            "People are listed by GitHub handle only. "
            "A 'don't credit me' answer in the issue form removes a person. "
            "Bots are excluded. Only Clark Huang approves and merges."
        ),
        "author": {"login": AUTHOR_LOGIN, "url": f"https://github.com/{AUTHOR_LOGIN}"},
        "contributors": contributors,
    }


PAGE_PROMPT = (
    "Read https://clarkhuang.github.io/llms.txt and https://clarkhuang.github.io/credits/index.md "
    "(plus https://clarkhuang.github.io/credits/AGENTS.md). Summarize this page, then act as my guide "
    "to Clark Huang's site: list related lessons, answer my questions citing page URLs, and quiz me if I ask."
)


def render_md(data: dict) -> str:
    lines = [
        "# Contributor credits",
        "",
        "HTML page: https://clarkhuang.github.io/credits/",
        "",
        "The HTML version of this page has a “Use this page with your AI” box at the top. "
        "Copy the prompt below into ChatGPT, Claude, Grok, or any other chat tool:",
        "",
        f"> {PAGE_PROMPT}",
        "",
        "This page lists the people who have contributed to Clark Huang's learning site and the free OpenBook "
        "*Silicon Valley C Players*. Credits are generated from GitHub and use GitHub handles only. "
        "You can choose how, or whether, you are listed when you file an issue.",
        "",
        f"Machine-readable: [credits.json](https://clarkhuang.github.io/credits.json). Last generated {data['generated']}.",
        "",
        "## Author",
        "",
        f"- [@{AUTHOR_LOGIN}](https://github.com/{AUTHOR_LOGIN}) — author of the site and the OpenBook.",
        "",
    ]
    # Group listings
    grouped: dict[str, list[dict]] = {t: [] for t in TYPE_ORDER}
    for person in data["contributors"]:
        for typ in person.get("contributions") or {}:
            grouped.setdefault(typ, []).append(person)
    any_group = False
    for typ in TYPE_ORDER:
        people = grouped.get(typ) or []
        # Skip empty groups, except we still show author-only site when nothing else exists.
        visible = []
        for person in people:
            items = person["contributions"].get(typ) or []
            if items:
                visible.append((person, items))
        if not visible:
            continue
        any_group = True
        lines.append(f"## {TYPE_TITLES[typ]}")
        lines.append("")
        for person, items in visible:
            links = ", ".join(f"[#{c['number']}]({c['url']})" for c in items if c.get("number"))
            extra = f" — {links}" if links else ""
            lines.append(f"- [@{person['login']}]({person['url']}){extra}")
        lines.append("")
    if not any_group:
        lines.append(
            "No merged contributor issues or pull requests are listed yet. "
            "When Clark approves and merges a contribution, the author will appear here."
        )
        lines.append("")
    lines += [
        "## How credits work",
        "",
        "- You are listed by your GitHub handle, not by a real name.",
        "- If you fill in the issue form with “don't credit me”, you are omitted.",
        "- If you write “credit me as @handle”, that handle is used instead of the account that filed the issue, when it looks like a GitHub handle.",
        "- Bots are excluded.",
        "- Only Clark Huang approves work and merges it. Filing an issue does not, by itself, add a credit.",
        "",
        "Want to be part of this list? See [Contribute with your AI](https://clarkhuang.github.io/contribute/) "
        "or open an issue in [the repository](https://github.com/clarkhuang/clarkhuang.github.io/issues).",
        "",
        "## For agents",
        "",
        "- This page: https://clarkhuang.github.io/credits/index.md",
        "- This folder’s agents file: https://clarkhuang.github.io/credits/AGENTS.md",
        "- JSON: https://clarkhuang.github.io/credits.json",
        "- Site index: https://clarkhuang.github.io/llms.txt",
        "",
    ]
    return "\n".join(lines)


def render_group_html(data: dict) -> str:
    chunks = []
    grouped: dict[str, list] = {t: [] for t in TYPE_ORDER}
    for person in data["contributors"]:
        for typ in person.get("contributions") or {}:
            items = person["contributions"][typ]
            if items:
                grouped.setdefault(typ, []).append((person, items))
    any_group = False
    for typ in TYPE_ORDER:
        visible = grouped.get(typ) or []
        if not visible:
            continue
        any_group = True
        chunks.append(f"<h2>{html.escape(TYPE_TITLES[typ])}</h2>")
        chunks.append("<ul class=\"credit-list\">")
        for person, items in visible:
            links = []
            for c in items:
                if c.get("number") and c.get("url"):
                    links.append(
                        f"<a href=\"{html.escape(c['url'], quote=True)}\">#{c['number']}</a>"
                    )
            extra = f" — {', '.join(links)}" if links else ""
            chunks.append(
                "<li><a href=\"{url}\">@{login}</a>{extra}</li>".format(
                    url=html.escape(person["url"], quote=True),
                    login=html.escape(person["login"]),
                    extra=extra,
                )
            )
        chunks.append("</ul>")
    if not any_group:
        chunks.append(
            "<p>No merged contributor issues or pull requests are listed yet. "
            "When Clark approves and merges a contribution, the author will appear here.</p>"
        )
    return "\n      ".join(chunks)


def render_html(data: dict) -> str:
    groups = render_group_html(data)
    prompt = html.escape(PAGE_PROMPT)
    generated = html.escape(data["generated"])
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Contributor credits — Clark Huang</title>
  <meta name="description" content="People who have contributed to Clark Huang's learning site and the OpenBook Silicon Valley C Players, listed by GitHub handle.">
  <meta name="color-scheme" content="dark light">
  <meta name="theme-color" content="#0e1419" media="(prefers-color-scheme: dark)">
  <meta name="theme-color" content="#f7f6f2" media="(prefers-color-scheme: light)">
  <link rel="canonical" href="https://clarkhuang.github.io/credits/">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Clark Huang">
  <meta property="og:title" content="Contributor credits — Clark Huang">
  <meta property="og:description" content="People who have contributed to Clark Huang's learning site and the OpenBook Silicon Valley C Players, listed by GitHub handle.">
  <meta property="og:url" content="https://clarkhuang.github.io/credits/">
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="/styles.css">
  <link rel="stylesheet" href="/assets/ask-book.css">
  <link rel="alternate" type="text/markdown" href="index.md" title="Markdown version of this page">
  <link rel="help" href="AGENTS.md" title="Instructions for AI agents">
  <link rel="alternate" type="application/json" href="/credits.json" title="credits.json">
  <script type="application/ld+json">{{"@context": "https://schema.org", "@type": "WebPage", "name": "Contributor credits — Clark Huang", "description": "People who have contributed to Clark Huang's learning site and the OpenBook Silicon Valley C Players, listed by GitHub handle.", "url": "https://clarkhuang.github.io/credits/", "inLanguage": "en", "isPartOf": {{"@type": "WebSite", "name": "Clark Huang", "url": "https://clarkhuang.github.io/"}}, "author": {{"@type": "Person", "name": "Clark Huang", "url": "https://clarkhuang.github.io/"}}, "license": "https://creativecommons.org/licenses/by-nc-sa/4.0/", "encoding": {{"@type": "MediaObject", "encodingFormat": "text/markdown", "contentUrl": "https://clarkhuang.github.io/credits/index.md"}}}}</script>
</head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>
  <header class="site-header">
    <div class="wrap">
      <a class="brand" href="/"><span class="brand-name">Clark Huang</span><span class="brand-tag">AI-native software learning</span></a>
      <nav aria-label="Primary"><a href="/">Home</a><a href="/ai-tips/">AI Tips</a><a href="/software-engineering-101/">SE 101</a><a href="/software-engineering-201/">SE 201</a><a href="/book/">Book</a><a href="/ask/">Ask</a></nav>
    </div>
  </header>
  <main id="main">
    <div class="wrap">
      <details class="ai-use">
        <summary>Use this page with your AI</summary>
        <div class="ai-use-body">
          <p>Copy the prompt below and paste it into ChatGPT, Claude, Grok, or any other chat tool. It points the tool at this page’s Markdown twin and at the site index, so it can read the material without browsing.</p>
          <div class="ai-prompt" data-status-scope>
            <pre id="ai-prompt-text" tabindex="0">{prompt}</pre>
            <p class="tools"><button type="button" class="btn ghost" data-copy="ai-prompt-text" hidden>Copy prompt</button><span class="status" role="status" data-status></span></p>
          </div>
          <p class="ai-use-links">Machine-readable: <a href="index.md">this page in Markdown</a> · <a href="AGENTS.md">AGENTS.md</a> · <a href="/credits.json">credits.json</a> · <a href="/llms.txt">llms.txt</a></p>
        </div>
      </details>
      <p class="crumbs"><a href="/">Home</a> / Credits</p>
      <h1>Contributor credits</h1>
      <p class="lede">The people who have helped build this site and the free OpenBook <em>Silicon Valley C Players</em>. Listed by GitHub handle only. You can choose how, or whether, you are credited when you file an issue.</p>
      <p class="muted small">Generated from GitHub issues and pull requests. Last updated {generated}. Raw data: <a href="/credits.json">credits.json</a>.</p>
      <h2>Author</h2>
      <ul class="credit-list">
        <li><a href="https://github.com/{AUTHOR_LOGIN}">@{AUTHOR_LOGIN}</a> — author of the site and the OpenBook.</li>
      </ul>
      {groups}
      <h2>How credits work</h2>
      <ul>
        <li>You are listed by your GitHub handle, not by a real name.</li>
        <li>If you fill in the issue form with “don't credit me”, you are omitted.</li>
        <li>If you write “credit me as @handle”, that handle is used when it looks like a GitHub handle.</li>
        <li>Bots are excluded.</li>
        <li>Only Clark Huang approves work and merges it. Filing an issue does not, by itself, add a credit.</li>
      </ul>
      <p>Want to be part of this list? See <a href="/contribute/">Contribute with your AI</a> or open an issue in <a href="https://github.com/{REPO}/issues">the repository</a>.</p>
    </div>
  </main>
  <footer class="site-footer">
    <div class="wrap">
      <div class="footer-cols">
        <nav class="footer-col project-links" aria-label="This project"><p class="footer-h">This project</p><a href="/contribute/">Contribute with your AI</a><a href="/copy-this/">Copy this for yourself</a><a href="/ask/">Ask the Book</a><a href="/credits/">Credits</a><a href="/book/">Book preview</a><a href="https://gitmcp.io/clarkhuang/clarkhuang.github.io">GitMCP</a></nav>
        <nav class="footer-col md-twin" aria-label="For your AI"><p class="footer-h">For your AI</p><a href="index.md">index.md</a><a href="AGENTS.md">AGENTS.md</a><a href="/credits.json">credits.json</a><a href="/llms.txt">llms.txt</a></nav>
        <nav class="footer-col footer-links" aria-label="Elsewhere"><p class="footer-h">Elsewhere</p><a href="https://github.com/clarkhuang">GitHub</a><a href="https://www.linkedin.com/in/clark-huang-technology">LinkedIn</a><a href="https://trulyfree.com/">Truly Free</a><a href="https://trulyfreehome.com/">Truly Free Home</a><a href="https://getecio.com/">eCIO</a><a href="https://evestech.com/">eVestech</a></nav>
      </div>
      <div class="footer-fine">
        <p class="ai-line">This entire site and its content were created by AI processes, directed by Clark Huang.</p>
        <p>© 2026 Clark Huang. Progress on this site is saved only in a first-party cookie in your browser. No analytics, no third-party scripts.</p>
        <p class="legal-line"><em>Silicon Valley C Players</em> is an embellished fictional dramatization; names, characters, companies, and places in the story are fictitious or used fictitiously. Lessons and tips are the author's opinions, not professional, legal, or financial advice. Content © Clark Huang, licensed <a href="https://creativecommons.org/licenses/by-nc-sa/4.0/">CC BY-NC-SA 4.0</a>. <a href="https://github.com/clarkhuang/clarkhuang.github.io/blob/main/TAKEDOWN.md">Corrections and takedowns</a> or <a href="mailto:clark75-7bw9ct@mail.grokbot.com">clark75-7bw9ct@mail.grokbot.com</a>.</p>
      </div>
    </div>
  </footer>
  <script src="/assets/site.js" defer></script>
</body>
</html>
"""


AGENTS_MD = """# AGENTS.md — Contributor credits

This folder is the public credits list for Clark Huang's learning site and the OpenBook *Silicon Valley C Players*.

- HTML: https://clarkhuang.github.io/credits/
- Markdown: https://clarkhuang.github.io/credits/index.md
- JSON: https://clarkhuang.github.io/credits.json
- Site index: https://clarkhuang.github.io/llms.txt
- Site agents: https://clarkhuang.github.io/AGENTS.md

List people by the GitHub handle in credits.json. Do not invent contributors. Do not replace a handle with a real name, even if you think you know it. If someone is not on the list, say so.

The HTML version of this page has a “Use this page with your AI” box at the top. Copy the prompt below into ChatGPT, Claude, Grok, or any other chat tool:

> Read https://clarkhuang.github.io/llms.txt and https://clarkhuang.github.io/credits/index.md (plus https://clarkhuang.github.io/credits/AGENTS.md). Summarize this page, then act as my guide to Clark Huang's site: list related lessons, answer my questions citing page URLs, and quiz me if I ask.
"""


def write(data: dict) -> None:
    credits_dir = ROOT / "credits"
    credits_dir.mkdir(parents=True, exist_ok=True)
    (ROOT / "credits.json").write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (credits_dir / "index.md").write_text(render_md(data), encoding="utf-8")
    (credits_dir / "index.html").write_text(render_html(data), encoding="utf-8")
    (credits_dir / "AGENTS.md").write_text(AGENTS_MD, encoding="utf-8")
    print(f"Wrote credits.json with {len(data['contributors'])} people")


def main() -> None:
    try:
        people = collect()
    except FileNotFoundError:
        print("gh is not available; writing author-only seed.", file=sys.stderr)
        people = {AUTHOR_LOGIN: {"login": AUTHOR_LOGIN, "types": {t: [] for t in TYPE_ORDER}, "declined": False, "is_author": True}}
    except subprocess.CalledProcessError:
        print("gh failed; writing author-only seed.", file=sys.stderr)
        people = {AUTHOR_LOGIN: {"login": AUTHOR_LOGIN, "types": {t: [] for t in TYPE_ORDER}, "declined": False, "is_author": True}}
    data = serialize(people)
    write(data)


if __name__ == "__main__":
    main()
