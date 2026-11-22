#!/usr/bin/env python3
"""Rewrite a built site so it can live under /staging/.

- Prefix root-relative URLs and production absolute URLs with /staging
- Inject noindex and a visible staging banner on every HTML page
- Leave /staging/ out of the staging copy of sitemap.xml (delete it)
- Keep staging self-contained (callers should copy assets into staging/)

Usage: python3 stage_site.py /path/to/staging/root
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

PREFIX = "/staging"
PROD = "https://clarkhuang.github.io"
BANNER_STYLE = (
    "position:sticky;top:0;z-index:9999;background:#3b1d08;color:#fff7e8;"
    "text-align:center;padding:10px 16px;font:600 14px/1.4 IBM Plex Sans,system-ui,sans-serif;"
    "border-bottom:2px solid #d6944e"
)
BANNER = (
    f'<div class="staging-banner" role="status" style="{BANNER_STYLE}">'
    "Staging preview — not the live site. "
    f'<a href="{PROD}/" style="color:#fff;text-decoration:underline">Go to the live site</a>.'
    "</div>"
)
NOINDEX = '<meta name="robots" content="noindex, nofollow">'

# href="/foo", src='/foo', poster="/foo", action="/foo", content="/foo" (but not //)
ATTR_RE = re.compile(
    r'''\b((?:href|src|poster|action|cite|data-[a-z0-9_-]+)\s*=\s*["'])(/(?!/|staging(?:/|"|'))[^"']*)(["'])''',
    re.I,
)
# url(/foo) in CSS — skip protocol-relative and already-prefixed paths
CSS_URL_RE = re.compile(r"url\(\s*(['\"]?)(/[^)\"]+?)\1\s*\)")

ABS_RE = re.compile(r"""https://clarkhuang\.github\.io(?!/staging)(/[^"'\\s<>]*)?""")


def rewrite_text(text: str, is_css: bool = False) -> str:
    def attr(m):
        return m.group(1) + PREFIX + m.group(2) + m.group(3)

    text = ATTR_RE.sub(attr, text)

    def css(m):
        quote, path = m.group(1), m.group(2)
        if path.startswith("//") or path.startswith(PREFIX + "/") or path == PREFIX:
            return m.group(0)
        return f"url({quote}{PREFIX}{path}{quote})"

    if is_css:
        text = CSS_URL_RE.sub(css, text)
    else:
        # inline style url() in HTML
        text = CSS_URL_RE.sub(css, text)

    def absurl(m):
        path = m.group(1) or "/"
        if path.startswith("/staging"):
            return PROD + path
        return PROD + PREFIX + path

    text = ABS_RE.sub(absurl, text)
    return text


def inject_html(html: str) -> str:
    if "staging-banner" not in html:
        if re.search(r"<body[^>]*>", html, re.I):
            html = re.sub(r"(<body[^>]*>)", r"\1\n" + BANNER, html, count=1, flags=re.I)
        else:
            html = BANNER + html
    if 'name="robots"' not in html.lower() or "noindex" not in html.lower():
        if re.search(r"<head[^>]*>", html, re.I):
            html = re.sub(r"(<head[^>]*>)", r"\1\n    " + NOINDEX, html, count=1, flags=re.I)
        else:
            html = NOINDEX + html
    return html


def process(root: Path) -> None:
    root = root.resolve()
    # Drop sitemap so staging URLs are not advertised as a second site map at /staging/sitemap.xml
    for name in ("sitemap.xml",):
        p = root / name
        if p.exists():
            p.unlink()
    # Staging robots: ask crawlers not to index this tree
    (root / "robots.txt").write_text("User-agent: *\nDisallow: /\n")
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if ".git" in path.parts or path.suffix.lower() in {
            ".mp4", ".mp3", ".jpg", ".jpeg", ".png", ".webp", ".gif",
            ".woff", ".woff2", ".ttf", ".otf", ".ico", ".pdf", ".zip",
        }:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        orig = text
        suffix = path.suffix.lower()
        if suffix in {".html", ".htm"}:
            text = rewrite_text(text)
            text = inject_html(text)
        elif suffix in {".css", ".js", ".md", ".txt", ".json", ".xml", ".vtt", ".svg"}:
            text = rewrite_text(text, is_css=(suffix == ".css"))
        if text != orig:
            path.write_text(text, encoding="utf-8")


def main():
    if len(sys.argv) != 2:
        sys.exit("usage: stage_site.py /path/to/staging/root")
    root = Path(sys.argv[1])
    if not root.is_dir():
        sys.exit(f"not a directory: {root}")
    process(root)
    print(f"staged {root}")


if __name__ == "__main__":
    main()
