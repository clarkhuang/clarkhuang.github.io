#!/usr/bin/env python3
"""Static self-check for a generated site: HTML structure, duplicate ids, internal links, media and fragments,
and video versions (every data-video-version / data-video-versions must match the media file's hash; see stamp_versions.py).
Usage: python3 check_site.py SITE_DIR   (exit 1 on any error)"""
import os, sys, re
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote

VOID = {"area","base","br","col","embed","hr","img","input","link","meta","source","track","wbr","param"}
OPTIONAL_END = {"p","li","dt","dd","option","tr","td","th","thead","tbody","tfoot"}

class P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.errors, self.ids, self.refs = [], [], {}, []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            if a["id"] in self.ids: self.errors.append(f"duplicate id {a['id']!r}")
            self.ids[a["id"]] = 1
        for k in ("href", "src", "poster"):
            if a.get(k): self.refs.append((tag, k, a[k]))
        if tag not in VOID: self.stack.append((tag, self.getpos()))
    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID and self.stack and self.stack[-1][0] == tag: self.stack.pop()
    def handle_endtag(self, tag):
        if tag in VOID: return
        while self.stack and self.stack[-1][0] != tag and self.stack[-1][0] in OPTIONAL_END: self.stack.pop()
        if self.stack and self.stack[-1][0] == tag: self.stack.pop()
        else: self.errors.append(f"unexpected </{tag}> at line {self.getpos()[0]}")

def resolve(site, page_rel, url):
    u = urlsplit(url)
    if u.scheme or u.netloc: return None, None
    path = unquote(u.path)
    if not path: target = os.path.join(site, page_rel)
    elif path.startswith("/"): target = os.path.join(site, path.lstrip("/"))
    else: target = os.path.normpath(os.path.join(site, os.path.dirname(page_rel), path))
    if path.endswith("/") or os.path.isdir(target): target = os.path.join(target, "index.html")
    return target, u.fragment

def main(site):
    site = os.path.abspath(site); errors = 0; pages = {}
    for root, _, files in os.walk(site):
        for f in files:
            if f.endswith(".html"):
                rel = os.path.relpath(os.path.join(root, f), site)
                p = P(); p.feed(open(os.path.join(root, f), encoding="utf-8").read()); p.close()
                for t, pos in p.stack:
                    if t not in OPTIONAL_END | {"html", "body", "head"}: p.errors.append(f"unclosed <{t}> from line {pos[0]}")
                pages[rel] = p
    for rel, p in sorted(pages.items()):
        for e in p.errors: print(f"ERROR {rel}: {e}"); errors += 1
        for tag, attr, url in p.refs:
            if url.startswith(("mailto:", "javascript:", "data:")): continue
            target, frag = resolve(site, rel, url)
            if target is None: continue
            if not os.path.exists(target):
                print(f"ERROR {rel}: {attr}={url} -> missing {os.path.relpath(target, site)}"); errors += 1; continue
            if frag and not frag.startswith("t=") and target.endswith(".html"):
                tp = pages.get(os.path.relpath(target, site))
                if tp and frag not in tp.ids: print(f"ERROR {rel}: {url} -> no id #{frag}"); errors += 1
    # Production pages must carry the GA4 tag (skipped at runtime on /staging/) and must not still claim there is no analytics.
    ga_id = "G-F50XBTM25X"
    old_privacy = "No analytics, no third-party scripts"
    for rel in sorted(pages):
        html = open(os.path.join(site, rel), encoding="utf-8").read()
        if old_privacy in html:
            print(f"ERROR {rel}: footer still says there is no analytics"); errors += 1
        if ga_id not in html or 'pathname.indexOf("/staging/")' not in html:
            print(f"ERROR {rel}: missing production GA4 tag or /staging/ skip"); errors += 1
        if "allow_ad_personalization_signals: false" not in html or "allow_google_signals: false" not in html:
            print(f"ERROR {rel}: GA4 tag is missing no-ads / no-signals settings"); errors += 1
    # Watched / resume cookies are keyed "<id>@<version>": a re-rendered video without re-stamping must fail here.
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import stamp_versions
    for e in stamp_versions.verify(site): print(f"ERROR {e}"); errors += 1
    print(f"checked {len(pages)} HTML files, {sum(len(p.refs) for p in pages.values())} references: {errors} error(s)")
    return errors

if __name__ == "__main__":
    sys.exit(1 if main(sys.argv[1] if len(sys.argv) > 1 else ".") else 0)
