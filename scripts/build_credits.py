#!/usr/bin/env python3
"""Generate the public Contributors page and machine-readable twins.

Writes:
  contributors/index.html, contributors/index.md, contributors/AGENTS.md
  contributors.json
  credits.json          (same payload; kept as an alias)
  credits/              (redirect to /contributors/, with Markdown twin)
  CONTRIBUTORS.md

Source of truth for descriptions is sitegen/landed-contributions.json.
The script also discovers outside authors of landed issues (a merged PR
that fixes/closes the issue) and of merged pull requests, but it never
lists Clark Huang in the contributors group (he is the author), never
lists bots, and honors a 'don't credit me' request.

Run from the repository root (needs `gh` authenticated, or GH_TOKEN):

    python3 scripts/build_credits.py

No ANTHROPIC_API_KEY. Public credits use a GitHub display name when the
profile has one, otherwise the handle, or the name a person consented to
publish in writing (for example a guest-story byline in landed-contributions.json).
Never invent a name.
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

GA_MEASUREMENT_ID = "G-F50XBTM25X"
ANALYTICS_HEAD = """  <script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  (function(){
    if (location.pathname.indexOf("/staging/") === 0) return;
    var s = document.createElement("script");
    s.async = true;
    s.src = "https://www.googletagmanager.com/gtag/js?id=%s";
    document.head.appendChild(s);
    gtag("js", new Date());
    gtag("config", "%s", {
      anonymize_ip: true,
      allow_google_signals: false,
      allow_ad_personalization_signals: false
    });
  })();
  </script>""" % (GA_MEASUREMENT_ID, GA_MEASUREMENT_ID)

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://clarkhuang.github.io"
REPO = os.environ.get("REPO") or os.environ.get("GITHUB_REPOSITORY") or "clarkhuang/clarkhuang.github.io"
AUTHOR_LOGIN = "clarkhuang"
ET = timezone(timedelta(hours=-5))
LANDED_PATH = ROOT / "sitegen" / "landed-contributions.json"

TYPE_LABELS = {
    "stories": {"feature", "new-story", "contributor-story", "story-seed"},
    "corrections": {"correction"},
    "feedback": {"feedback"},
    "refactors": {"refactor"},
    "fitness-health": {"fitness-health"},
    "code/site": {"site", "code"},
}
TYPE_ORDER = ["feedback", "stories", "corrections", "refactors", "fitness-health", "code/site"]
TYPE_TITLES = {
    "feedback": "Feedback",
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
CREDIT_FIELD_RE = re.compile(
    r"###\s+Credit(?:\s+\(optional\))?.*?^\s*\n(.*?)(?=^###\s|\Z)",
    re.I | re.M | re.S,
)
FIXES_RE = re.compile(
    r"(?i)\b(?:fix(?:es)?|close[sd]?|resolve[sd]?|refs?|references|related(?:\s+to)?)\s+#(\d+)"
)


def now_et() -> str:
    return datetime.now(ET).strftime("%Y-%m-%d %-I:%M %p ET (America/New_York)")


def gh_json(args: list[str]):
    env = os.environ.copy()
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

    Public credits use a GitHub handle, plus a public profile display name
    when one exists. A free-text real name in the credit field is ignored
    (never published) unless it is a handle. 'credit me as @handle' is
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
    return user.get("login") or None


def display_name_for(login: str, cache: dict[str, str | None]) -> str | None:
    """Public GitHub profile name, or None if the profile has no name."""
    key = login.lower()
    if key in cache:
        return cache[key]
    name = None
    try:
        data = gh_json(["api", f"users/{login}"])
        raw = (data.get("name") if isinstance(data, dict) else None) or None
        if isinstance(raw, str):
            raw = raw.strip()
            name = raw or None
    except (subprocess.CalledProcessError, FileNotFoundError, TypeError):
        name = None
    cache[key] = name
    return name


def load_landed() -> list[dict]:
    if not LANDED_PATH.exists():
        return []
    try:
        data = json.loads(LANDED_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"Could not parse {LANDED_PATH}: {e}", file=sys.stderr)
        return []
    return list(data.get("people") or [])


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
            "number,title,url,state,author,labels,body,mergedAt,isDraft",
        ]
    )
    issues_by_number = {i.get("number"): i for i in issues if i.get("number")}

    people: dict[str, dict] = {}

    def ensure(login: str) -> dict:
        key = login.lower()
        if key not in people:
            people[key] = {
                "login": login,
                "types": {t: [] for t in TYPE_ORDER},
                "declined": False,
                "summaries": [],
            }
        return people[key]

    def add(login: str, typ: str, item: dict, role: str, summary: str | None = None):
        if not login or is_bot(login):
            return
        if login.lower() == AUTHOR_LOGIN:
            # Clark is listed only as the author, not in the contributors group.
            person = ensure(login)
            person["is_author"] = True
            person["login"] = AUTHOR_LOGIN
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
        if summary:
            rec["summary"] = summary
        if item.get("page_url"):
            rec["page_url"] = item["page_url"]
        existing = person["types"][typ]
        for c in existing:
            if c.get("number") == rec["number"] and c.get("role") == rec["role"]:
                if summary and not c.get("summary"):
                    c["summary"] = summary
                if rec.get("page_url") and not c.get("page_url"):
                    c["page_url"] = rec["page_url"]
                return
        existing.append(rec)
        if summary and summary not in person["summaries"]:
            person["summaries"].append(summary)

    def credit_login(default_login: str, body: str | None) -> str | None:
        override, declined = parse_credit_field(body)
        if declined:
            if default_login and not is_bot(default_login):
                person = ensure(default_login)
                person["declined"] = True
            return None
        return override or default_login

    # Curated landed contributions (written in the same PR that lands the work).
    for entry in load_landed():
        login = (entry.get("login") or "").strip()
        if not login or is_bot(login):
            continue
        # A curated decline flag, if present.
        if entry.get("declined"):
            ensure(login)["declined"] = True
            continue
        consented = (entry.get("name") or "").strip() or None
        if consented:
            # Only a name the person consented to publish in writing (e.g. a guest-story byline).
            ensure(login)["consented_name"] = consented
        for contrib in entry.get("contributions") or []:
            typ = contrib.get("type") or "feedback"
            if typ not in TYPE_ORDER:
                typ = "feedback"
            issue_num = contrib.get("issue")
            issue = issues_by_number.get(issue_num) if issue_num else None
            body = (issue or {}).get("body") if issue else None
            # Honor a decline on the source issue even for curated entries.
            credited = credit_login(login, body)
            if not credited:
                continue
            item = {
                "number": issue_num or (contrib.get("pull_requests") or [None])[0],
                "title": (issue or {}).get("title") or contrib.get("summary") or "",
                "url": contrib.get("issue_url")
                or (issue or {}).get("url")
                or (f"https://github.com/{REPO}/issues/{issue_num}" if issue_num else None)
                or (f"https://github.com/{REPO}/pull/{(contrib.get('pull_requests') or [None])[0]}"
                    if (contrib.get("pull_requests") or [None])[0] else None)
                or contrib.get("page_url"),
            }
            if contrib.get("page_url"):
                item["page_url"] = contrib["page_url"]
            add(credited, typ, item, "author", contrib.get("summary"))
            for pr_num in contrib.get("pull_requests") or []:
                add(
                    credited,
                    typ,
                    {
                        "number": pr_num,
                        "title": f"Pull request #{pr_num}",
                        "url": f"https://github.com/{REPO}/pull/{pr_num}",
                    },
                    "landed-in",
                )

    # Outside authors of closed, labeled contribution issues, or approved issues.
    for issue in issues:
        labels = issue.get("labels") or []
        names = {((l.get("name") if isinstance(l, dict) else l) or "").lower() for l in labels}
        author = gh_login(issue.get("author"))
        title = (issue.get("title") or "").strip()
        if title in {"Clark's Decisions"} or title.lower().startswith("decide ") or title.lower().startswith("confirm "):
            continue
        if "takedown-request" in names or "takedown" in names:
            continue
        is_approved = "approved" in names or "merged-contribution" in names
        is_done = issue.get("state") == "CLOSED" and bool(names & set().union(*TYPE_LABELS.values()))
        if not (is_approved or is_done):
            continue
        types = types_for_labels(labels)
        login = credit_login(author, issue.get("body"))
        if login:
            for typ in types:
                add(login, typ, issue, "author")

    # Outside authors of issues that actually landed via a merged PR.
    for pr in prs:
        if not pr.get("mergedAt"):
            continue
        body = pr.get("body") or ""
        for num_s in FIXES_RE.findall(body):
            number = int(num_s)
            issue = issues_by_number.get(number)
            if not issue:
                continue
            author = gh_login(issue.get("author"))
            login = credit_login(author, issue.get("body"))
            if not login:
                continue
            types = types_for_labels(issue.get("labels") or [])
            # Unlabeled feedback that a merged PR fixed is still a landed contribution.
            if types == ["code/site"] and not (issue.get("labels") or []):
                types = ["feedback"]
            # A curated landed entry may already have recorded this PR under a
            # different type (for example a guest story that only mentions an issue).
            person = people.get(login.lower()) if login else None
            already = False
            if person:
                for items in person["types"].values():
                    if any(c.get("number") == pr.get("number") for c in items):
                        already = True
                        break
            if already:
                continue
            for typ in types:
                add(login, typ, issue, "author")
                add(login, typ, pr, "landed-in")

    # Outside authors of merged pull requests they opened themselves.
    for pr in prs:
        if not pr.get("mergedAt"):
            continue
        author = gh_login(pr.get("author"))
        if is_bot(author, pr.get("author") if isinstance(pr.get("author"), dict) else None):
            continue
        types = types_for_labels(pr.get("labels") or [])
        if types == ["code/site"] or not pr.get("labels"):
            types = types if pr.get("labels") else ["code/site"]
        login = credit_login(author, pr.get("body"))
        if login:
            # A curated landed entry already recorded this PR (for example a guest story).
            # Don't also file it under code/site just because the PR has no labels.
            already = False
            person = people.get(login.lower())
            if person:
                for items in person["types"].values():
                    if any(c.get("number") == pr.get("number") for c in items):
                        already = True
                        break
            if already and types == ["code/site"]:
                continue
            for typ in types:
                add(login, typ, pr, "pr-author")

    author = ensure(AUTHOR_LOGIN)
    author["login"] = AUTHOR_LOGIN
    author["is_author"] = True
    return people


def serialize(people: dict) -> dict:
    name_cache: dict[str, str | None] = {}
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
        rec = {
            "login": person["login"],
            "url": f"https://github.com/{person['login']}",
            "roles": (["author"] if person.get("is_author") else []) + types_present,
            "contributions": grouped,
        }
        if person.get("summaries"):
            rec["summaries"] = person["summaries"]
        if not person.get("is_author") or types_present:
            consented = (person.get("consented_name") or "").strip() or None
            public_name = display_name_for(person["login"], name_cache)
            if consented:
                rec["name"] = consented
            elif public_name:
                rec["name"] = public_name
        contributors.append(rec)
    return {
        "site": SITE,
        "repository": f"https://github.com/{REPO}",
        "canonical_page": f"{SITE}/contributors/",
        "canonical_json": f"{SITE}/contributors.json",
        "aliases": [f"{SITE}/credits/", f"{SITE}/credits.json"],
        "generated": now_et(),
        "generated_by": "scripts/build_credits.py",
        "note": (
            "Credits list outside contributions that actually landed on the site. "
            "People are listed by public GitHub display name when the profile has one, "
            "otherwise by GitHub handle, or by the name they consented to publish on a guest story. A name is never invented. "
            "A 'don't credit me' answer in the issue form removes a person. "
            "Bots are excluded. Only Clark Huang approves and merges. "
            "Filing an issue does not, by itself, add a credit."
        ),
        "author": {"login": AUTHOR_LOGIN, "url": f"https://github.com/{AUTHOR_LOGIN}"},
        "contributors": contributors,
    }


PAGE_PROMPT = (
    "Read https://clarkhuang.github.io/llms.txt and https://clarkhuang.github.io/contributors/index.md "
    "(plus https://clarkhuang.github.io/contributors/AGENTS.md). Summarize this page, then act as my guide "
    "to Clark Huang's site: list related lessons, answer my questions citing page URLs, and quiz me if I ask."
)


def label_for(person: dict) -> str:
    name = person.get("name")
    login = person["login"]
    if name:
        return f"{name} (@{login})"
    return f"@{login}"


def md_person_line(person: dict, items: list[dict]) -> str:
    label = label_for(person)
    url = person["url"]
    summaries = [c.get("summary") for c in items if c.get("summary")]
    # Also use page-level summaries if items have none.
    if not summaries:
        summaries = list(person.get("summaries") or [])
    summary = " ".join(dict.fromkeys(summaries))  # unique, stable order
    # Links: prefer the source issue, then PRs.
    links = []
    seen = set()
    seen_pages = set()
    for c in items:
        page = c.get("page_url")
        if page and page not in seen_pages:
            seen_pages.add(page)
            links.append(f"[guest story]({page})")
        n = c.get("number")
        u = c.get("url")
        if not n or not u or n in seen:
            continue
        if u in seen_pages:
            continue
        seen.add(n)
        if "/pull/" in (u or ""):
            links.append(f"[PR #{n}]({u})")
        else:
            links.append(f"[#{n}]({u})")
    bits = [f"- [{label}]({url})"]
    if summary:
        bits.append(f" — {summary}")
    if links:
        bits.append(f" — {', '.join(links)}")
    return "".join(bits)


def render_md(data: dict) -> str:
    lines = [
        "# Contributors",
        "",
        "HTML page: https://clarkhuang.github.io/contributors/",
        "",
        "The HTML version of this page has a “Use this page with your AI” box at the top. "
        "Copy the prompt below into ChatGPT, Claude, Grok, or any other chat tool:",
        "",
        f"> {PAGE_PROMPT}",
        "",
        "This page lists the people whose contributions have landed on Clark Huang's learning site and the free OpenBook "
        "*Silicon Valley C Players*. Credits use a public GitHub display name when the profile has one, otherwise the GitHub handle, or the name the person consented to publish on a guest story. "
        "A name is never invented. You can choose how, or whether, you are listed when you file an issue.",
        "",
        f"Machine-readable: [contributors.json](https://clarkhuang.github.io/contributors.json) "
        f"(also [credits.json](https://clarkhuang.github.io/credits.json)). Last generated {data['generated']}.",
        "",
        "## Author",
        "",
        f"- [@{AUTHOR_LOGIN}](https://github.com/{AUTHOR_LOGIN}) — author of the site and the OpenBook.",
        "",
    ]
    grouped: dict[str, list[dict]] = {t: [] for t in TYPE_ORDER}
    for person in data["contributors"]:
        if person.get("login") == AUTHOR_LOGIN and not person.get("contributions"):
            continue
        for typ in person.get("contributions") or {}:
            grouped.setdefault(typ, []).append(person)
    any_group = False
    for typ in TYPE_ORDER:
        people = grouped.get(typ) or []
        visible = []
        for person in people:
            if person.get("login") == AUTHOR_LOGIN:
                continue
            items = person["contributions"].get(typ) or []
            if items:
                visible.append((person, items))
        if not visible:
            continue
        any_group = True
        lines.append(f"## {TYPE_TITLES[typ]}")
        lines.append("")
        for person, items in visible:
            lines.append(md_person_line(person, items))
        lines.append("")
    if not any_group:
        lines.append(
            "No outside contributions have landed on the site yet. "
            "When a contribution is approved and merged, the author will appear here."
        )
        lines.append("")
    lines += [
        "## How credits work",
        "",
        "- Only work that actually landed on the site is listed. Filing an issue or opening a pull request does not, by itself, add a credit.",
        "- You are listed by your public GitHub display name when your profile has one, otherwise by your GitHub handle, or by the name you consented to publish on a guest story. A name is never invented, and no other personal details are added.",
        "- If you fill in the issue form with “don't credit me”, you are omitted.",
        "- If you write “credit me as @handle”, that handle is used instead of the account that filed the issue, when it looks like a GitHub handle.",
        "- Bots are excluded.",
        "- Any outside contribution that lands is credited on this page in the same pull request (see [CONTRIBUTING.md](https://github.com/clarkhuang/clarkhuang.github.io/blob/main/CONTRIBUTING.md) and [AGENTS.md](https://clarkhuang.github.io/AGENTS.md)).",
        "- Only Clark Huang approves work and merges it.",
        "",
        "The previous address of this page, [/credits/](https://clarkhuang.github.io/credits/), redirects here.",
        "",
        "Want to be part of this list? See [Contribute with your AI](https://clarkhuang.github.io/contribute/) "
        "or open an issue in [the repository](https://github.com/clarkhuang/clarkhuang.github.io/issues).",
        "",
        "## For agents",
        "",
        "- This page: https://clarkhuang.github.io/contributors/index.md",
        "- This folder’s agents file: https://clarkhuang.github.io/contributors/AGENTS.md",
        "- JSON: https://clarkhuang.github.io/contributors.json",
        "- Alias JSON: https://clarkhuang.github.io/credits.json",
        "- Site index: https://clarkhuang.github.io/llms.txt",
        "",
    ]
    return "\n".join(lines)


def site_href(url: str | None) -> str:
    """Root-relative href for this-site pages so staging link rewriting works."""
    if not url:
        return ""
    if url.startswith(SITE + "/"):
        return url[len(SITE):]
    if url.startswith(SITE):
        return url[len(SITE):] or "/"
    return url


def html_person_item(person: dict, items: list[dict]) -> str:
    label = html.escape(label_for(person))
    url = html.escape(person["url"], quote=True)
    summaries = [c.get("summary") for c in items if c.get("summary")]
    if not summaries:
        summaries = list(person.get("summaries") or [])
    summary = " ".join(dict.fromkeys(summaries))
    links = []
    seen = set()
    seen_pages = set()
    for c in items:
        page = c.get("page_url")
        if page and page not in seen_pages:
            seen_pages.add(page)
            links.append(
                f"<a href=\"{html.escape(site_href(page), quote=True)}\">guest story</a>"
            )
        n = c.get("number")
        u = c.get("url")
        if not n or not u or n in seen:
            continue
        if u in seen_pages:
            continue
        seen.add(n)
        kind = "PR " if "/pull/" in (u or "") else ""
        links.append(
            f"<a href=\"{html.escape(u, quote=True)}\">#{kind}{n}</a>".replace("#PR ", "PR #")
        )
    extra_bits = []
    if summary:
        extra_bits.append(html.escape(summary))
    if links:
        extra_bits.append(", ".join(links))
    extra = f" — {' — '.join(extra_bits)}" if extra_bits else ""
    return f"<li><a href=\"{url}\">{label}</a>{extra}</li>"


def render_group_html(data: dict) -> str:
    chunks = []
    grouped: dict[str, list] = {t: [] for t in TYPE_ORDER}
    for person in data["contributors"]:
        for typ in person.get("contributions") or {}:
            items = person["contributions"][typ]
            if items and person.get("login") != AUTHOR_LOGIN:
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
            chunks.append(html_person_item(person, items))
        chunks.append("</ul>")
    if not any_group:
        chunks.append(
            "<p>No outside contributions have landed on the site yet. "
            "When a contribution is approved and merged, the author will appear here.</p>"
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
  <title>Contributors — Clark Huang</title>
  <meta name="description" content="People whose contributions have landed on Clark Huang's learning site and the OpenBook Silicon Valley C Players.">
  <meta name="color-scheme" content="dark light">
  <meta name="theme-color" content="#0e1419" media="(prefers-color-scheme: dark)">
  <meta name="theme-color" content="#f7f6f2" media="(prefers-color-scheme: light)">
  <link rel="canonical" href="https://clarkhuang.github.io/contributors/">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Clark Huang">
  <meta property="og:title" content="Contributors — Clark Huang">
  <meta property="og:description" content="People whose contributions have landed on Clark Huang's learning site and the OpenBook Silicon Valley C Players.">
  <meta property="og:url" content="https://clarkhuang.github.io/contributors/">
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="/styles.css">
  <link rel="stylesheet" href="/assets/ask-book.css">
  <link rel="alternate" type="text/markdown" href="index.md" title="Markdown version of this page">
  <link rel="help" href="AGENTS.md" title="Instructions for AI agents">
  <link rel="alternate" type="application/json" href="/contributors.json" title="contributors.json">
  <script type="application/ld+json">{{"@context": "https://schema.org", "@type": "WebPage", "name": "Contributors — Clark Huang", "description": "People whose contributions have landed on Clark Huang's learning site and the OpenBook Silicon Valley C Players.", "url": "https://clarkhuang.github.io/contributors/", "inLanguage": "en", "isPartOf": {{"@type": "WebSite", "name": "Clark Huang", "url": "https://clarkhuang.github.io/"}}, "author": {{"@type": "Person", "name": "Clark Huang", "url": "https://clarkhuang.github.io/"}}, "license": "https://creativecommons.org/licenses/by-nc-sa/4.0/", "encoding": {{"@type": "MediaObject", "encodingFormat": "text/markdown", "contentUrl": "https://clarkhuang.github.io/contributors/index.md"}}}}</script>
{ANALYTICS_HEAD}
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
          <p class="ai-use-links">Machine-readable: <a href="index.md">this page in Markdown</a> · <a href="AGENTS.md">AGENTS.md</a> · <a href="/contributors.json">contributors.json</a> · <a href="/llms.txt">llms.txt</a></p>
        </div>
      </details>
      <p class="crumbs"><a href="/">Home</a> / Contributors</p>
      <h1>Contributors</h1>
      <p class="lede">The people whose contributions have landed on this site and the free OpenBook <em>Silicon Valley C Players</em>. Credits use a public GitHub display name when the profile has one, otherwise the GitHub handle, or the name the person consented to publish on a guest story. A name is never invented. You can choose how, or whether, you are credited when you file an issue.</p>
      <p class="muted small">Last updated {generated}. Raw data: <a href="/contributors.json">contributors.json</a>.</p>
      <h2>Author</h2>
      <ul class="credit-list">
        <li><a href="https://github.com/{AUTHOR_LOGIN}">@{AUTHOR_LOGIN}</a> — author of the site and the OpenBook.</li>
      </ul>
      {groups}
      <h2>How credits work</h2>
      <ul>
        <li>Only work that actually landed on the site is listed. Filing an issue or opening a pull request does not, by itself, add a credit.</li>
        <li>You are listed by your public GitHub display name when your profile has one, otherwise by your GitHub handle, or by the name you consented to publish on a guest story. A name is never invented, and no other personal details are added.</li>
        <li>If you fill in the issue form with “don't credit me”, you are omitted.</li>
        <li>If you write “credit me as @handle”, that handle is used when it looks like a GitHub handle.</li>
        <li>Bots are excluded.</li>
        <li>Any outside contribution that lands is credited on this page in the same pull request (see <a href="https://github.com/{REPO}/blob/main/CONTRIBUTING.md">CONTRIBUTING.md</a> and <a href="/AGENTS.md">AGENTS.md</a>).</li>
        <li>Only Clark Huang approves work and merges it.</li>
      </ul>
      <p>The previous address of this page, <a href="/credits/">/credits/</a>, redirects here.</p>
      <p>Want to be part of this list? See <a href="/contribute/">Contribute with your AI</a> or open an issue in <a href="https://github.com/{REPO}/issues">the repository</a>.</p>
    </div>
  </main>
  <footer class="site-footer">
    <div class="wrap">
      <div class="footer-cols">
        <nav class="footer-col project-links" aria-label="This project"><p class="footer-h">This project</p><a href="/contribute/">Contribute with your AI</a><a href="/copy-this/">Copy this for yourself</a><a href="/ask/">Ask the Book</a><a href="/contributors/">Contributors</a><a href="/book/">Book preview</a></nav>
        <nav class="footer-col md-twin" aria-label="For your AI"><p class="footer-h">For your AI</p><a href="index.md">index.md</a><a href="AGENTS.md">AGENTS.md</a><a href="/contributors.json">contributors.json</a><a href="/llms.txt">llms.txt</a></nav>
        <nav class="footer-col footer-links" aria-label="Elsewhere"><p class="footer-h">Elsewhere</p><a href="https://github.com/clarkhuang">GitHub</a><a href="https://www.linkedin.com/in/clark-huang-technology">LinkedIn</a><a href="https://trulyfree.com/">Truly Free</a><a href="https://trulyfreehome.com/">Truly Free Home</a><a href="https://getecio.com/">eCIO</a><a href="https://evestech.com/">eVestech</a></nav>
      </div>
      <div class="footer-fine">
        <p class="ai-line">This entire site and its content were created by AI processes, directed by Clark Huang.</p>
        <p>© 2026 Clark Huang. Watched progress and a last-visit time are saved only in first-party cookies in your browser. The site uses Google Analytics 4 with privacy-friendly settings and no ads signals. <a href="/book/editorial-policy/#analytics">Privacy note</a>.</p>
        <p class="legal-line"><em>Silicon Valley C Players</em> is an embellished fictional dramatization; names, characters, companies, and places in the story are fictitious or used fictitiously. Lessons and tips are the author's opinions, not professional, legal, or financial advice. Content © Clark Huang, licensed <a href="https://creativecommons.org/licenses/by-nc-sa/4.0/">CC BY-NC-SA 4.0</a>. <a href="https://github.com/clarkhuang/clarkhuang.github.io/blob/main/TAKEDOWN.md">Corrections and takedowns</a> or <a href="mailto:clark75-7bw9ct@mail.grokbot.com">clark75-7bw9ct@mail.grokbot.com</a>.</p>
      </div>
    </div>
  </footer>
  <script src="/assets/site.js" defer></script>
</body>
</html>
"""


AGENTS_MD = """# AGENTS.md — Contributors

This folder is the public contributors list for Clark Huang's learning site and the OpenBook *Silicon Valley C Players*.

- HTML: https://clarkhuang.github.io/contributors/
- Markdown: https://clarkhuang.github.io/contributors/index.md
- JSON: https://clarkhuang.github.io/contributors.json
- Alias (redirect): https://clarkhuang.github.io/credits/
- Alias JSON: https://clarkhuang.github.io/credits.json
- Site index: https://clarkhuang.github.io/llms.txt
- Site agents: https://clarkhuang.github.io/AGENTS.md

List people as they appear in contributors.json. Use the public GitHub display name when the JSON has a `name` field, otherwise the handle. Do not invent contributors or names. Do not add other personal details. If someone is not on the list, their work has not landed on the site (or they asked not to be credited); say so.

Any outside contribution that lands must be credited on this page in the same pull request: add an entry to `sitegen/landed-contributions.json` and run `python3 scripts/build_credits.py`.

The HTML version of this page has a “Use this page with your AI” box at the top. Copy the prompt below into ChatGPT, Claude, Grok, or any other chat tool:

> Read https://clarkhuang.github.io/llms.txt and https://clarkhuang.github.io/contributors/index.md (plus https://clarkhuang.github.io/contributors/AGENTS.md). Summarize this page, then act as my guide to Clark Huang's site: list related lessons, answer my questions citing page URLs, and quiz me if I ask.
"""


CREDITS_REDIRECT_MD = """# Moved: Contributors

This address now redirects to the Contributors page.

- New page: https://clarkhuang.github.io/contributors/
- Markdown twin: https://clarkhuang.github.io/contributors/index.md
- Agents: https://clarkhuang.github.io/contributors/AGENTS.md
- JSON: https://clarkhuang.github.io/contributors.json
"""

CREDITS_REDIRECT_AGENTS = """# AGENTS.md — Credits (moved)

This address has moved. The public contributors list is now:

- HTML: https://clarkhuang.github.io/contributors/
- Markdown: https://clarkhuang.github.io/contributors/index.md
- Agents: https://clarkhuang.github.io/contributors/AGENTS.md
- JSON: https://clarkhuang.github.io/contributors.json

Do not invent contributors. Use the list on the new page.
"""

CREDITS_REDIRECT_HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Moved: Contributors — Clark Huang</title>
  <meta name="robots" content="noindex">
  <link rel="canonical" href="https://clarkhuang.github.io/contributors/">
  <meta http-equiv="refresh" content="0; url=/contributors/">
  <link rel="alternate" type="text/markdown" href="/contributors/index.md">
  <link rel="help" href="/contributors/AGENTS.md" title="Instructions for AI agents">
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
{ANALYTICS_HEAD}
</head>
<body>
  <main>
    <h1>This page moved</h1>
    <p>Contributor credits now live at <a href="/contributors/">/contributors/</a>.</p>
    <p>Machine-readable: <a href="/contributors/index.md">index.md</a> · <a href="/contributors/AGENTS.md">AGENTS.md</a> · <a href="/contributors.json">contributors.json</a>.</p>
  </main>
  <script>location.replace("/contributors/");</script>
</body>
</html>
"""


def render_contributors_md_repo(data: dict) -> str:
    lines = [
        "# Contributors",
        "",
        "Public list: https://clarkhuang.github.io/contributors/",
        "",
        "This file is the repository twin of the public Contributors page. "
        "Only outside contributions that have landed on the site are listed. "
        "Credits use a public GitHub display name when the profile has one, otherwise the GitHub handle, or the name the person consented to publish on a guest story.",
        "",
        f"Machine-readable: [contributors.json](https://clarkhuang.github.io/contributors.json). Last generated {data['generated']}.",
        "",
        "## Author",
        "",
        f"- [@{AUTHOR_LOGIN}](https://github.com/{AUTHOR_LOGIN}) — author of the site and the OpenBook.",
        "",
        "## Contributors",
        "",
    ]
    any_person = False
    for person in data["contributors"]:
        if person.get("login") == AUTHOR_LOGIN:
            continue
        items = []
        for typ in TYPE_ORDER:
            items.extend(person.get("contributions", {}).get(typ) or [])
        if not items:
            continue
        any_person = True
        lines.append(md_person_line(person, items))
    if not any_person:
        lines.append("No outside contributions have landed on the site yet.")
    lines += [
        "",
        "To credit a new landed contribution, add an entry to `sitegen/landed-contributions.json` in the same pull request and run `python3 scripts/build_credits.py`.",
        "",
    ]
    return "\n".join(lines)


def write(data: dict) -> None:
    contrib_dir = ROOT / "contributors"
    contrib_dir.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    (ROOT / "contributors.json").write_text(payload, encoding="utf-8")
    (ROOT / "credits.json").write_text(payload, encoding="utf-8")
    (contrib_dir / "index.md").write_text(render_md(data), encoding="utf-8")
    (contrib_dir / "index.html").write_text(render_html(data), encoding="utf-8")
    (contrib_dir / "AGENTS.md").write_text(AGENTS_MD, encoding="utf-8")
    (ROOT / "CONTRIBUTORS.md").write_text(render_contributors_md_repo(data), encoding="utf-8")

    credits_dir = ROOT / "credits"
    credits_dir.mkdir(parents=True, exist_ok=True)
    (credits_dir / "index.html").write_text(CREDITS_REDIRECT_HTML, encoding="utf-8")
    (credits_dir / "index.md").write_text(CREDITS_REDIRECT_MD, encoding="utf-8")
    (credits_dir / "AGENTS.md").write_text(CREDITS_REDIRECT_AGENTS, encoding="utf-8")

    outside = [p for p in data["contributors"] if p.get("login") != AUTHOR_LOGIN]
    print(f"Wrote contributors.json with {len(outside)} credited contributor(s)")


def main() -> None:
    try:
        people = collect()
    except FileNotFoundError:
        print("gh is not available; writing author-only seed plus curated landed file.", file=sys.stderr)
        people = {AUTHOR_LOGIN: {"login": AUTHOR_LOGIN, "types": {t: [] for t in TYPE_ORDER}, "declined": False, "is_author": True, "summaries": []}}
        # Still apply curated entries without live GitHub, using the file only.
        for entry in load_landed():
            login = (entry.get("login") or "").strip()
            if not login or is_bot(login) or login.lower() == AUTHOR_LOGIN:
                continue
            people[login.lower()] = {
                "login": login,
                "types": {t: [] for t in TYPE_ORDER},
                "declined": bool(entry.get("declined")),
                "summaries": [],
            }
            person = people[login.lower()]
            for contrib in entry.get("contributions") or []:
                typ = contrib.get("type") if contrib.get("type") in TYPE_ORDER else "feedback"
                rec = {
                    "number": contrib.get("issue"),
                    "title": contrib.get("summary") or "",
                    "url": contrib.get("issue_url") or (
                        f"https://github.com/{REPO}/issues/{contrib['issue']}" if contrib.get("issue") else None
                    ),
                    "role": "author",
                    "summary": contrib.get("summary"),
                }
                person["types"][typ].append(rec)
                if contrib.get("summary"):
                    person["summaries"].append(contrib["summary"])
    except subprocess.CalledProcessError:
        print("gh failed; writing author-only seed plus curated landed file.", file=sys.stderr)
        # Re-enter via the FileNotFoundError-style fallback by calling main's seed path is messy;
        # collect() already failed, so load curated only.
        people = {AUTHOR_LOGIN: {"login": AUTHOR_LOGIN, "types": {t: [] for t in TYPE_ORDER}, "declined": False, "is_author": True, "summaries": []}}
        for entry in load_landed():
            login = (entry.get("login") or "").strip()
            if not login or is_bot(login) or login.lower() == AUTHOR_LOGIN:
                continue
            people[login.lower()] = {
                "login": login,
                "types": {t: [] for t in TYPE_ORDER},
                "declined": bool(entry.get("declined")),
                "summaries": [],
            }
            person = people[login.lower()]
            for contrib in entry.get("contributions") or []:
                typ = contrib.get("type") if contrib.get("type") in TYPE_ORDER else "feedback"
                rec = {
                    "number": contrib.get("issue"),
                    "title": contrib.get("summary") or "",
                    "url": contrib.get("issue_url") or (
                        f"https://github.com/{REPO}/issues/{contrib['issue']}" if contrib.get("issue") else None
                    ),
                    "role": "author",
                    "summary": contrib.get("summary"),
                }
                person["types"][typ].append(rec)
                if contrib.get("summary"):
                    person["summaries"].append(contrib["summary"])
    data = serialize(people)
    write(data)


if __name__ == "__main__":
    main()
