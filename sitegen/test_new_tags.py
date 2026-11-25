#!/usr/bin/env python3
"""Headless-browser test: publish dates are visible, and New tags follow last-visit cookies.

Copies the site to a temp dir (media hard-linked, HTML copied, so the repo is never written), serves it with
`python3 -m http.server`, and drives it with Playwright (Google Chrome if present; else Chromium).

  python3 sitegen/test_new_tags.py [--out RESULTS.md]

A first visit shows no New tags. Returning visits show New on videos published or updated since the previous
visit, and those tags stay for the whole browsing session (visit_ref session cookie). Exit 1 if any check fails.
"""
import os, shutil, socket, subprocess, sys, tempfile, time, urllib.parse
from contextlib import closing
from datetime import datetime
from zoneinfo import ZoneInfo

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
from playwright.sync_api import sync_playwright  # noqa: E402

MEDIA_EXT = (".mp4", ".mp3", ".jpg", ".png", ".webp", ".woff2", ".m4a")
BOOK = "/book/"
HOME = "/"
SE201_IDX = "/software-engineering-201/"
AI_TIPS_03 = "/ai-tips/03-define-the-number-before-you-ask-for-it/"
ET = ZoneInfo("America/New_York")
# After every Nov 23 video, before the Nov 24 book-preview update.
CUTOFF = int(datetime(2026, 11, 23, 23, 59, 59, tzinfo=ET).timestamp())
results = []


def check(name, ok, detail=""):
    results.append((name, bool(ok), detail))
    print(("PASS " if ok else "FAIL ") + name + (f"  [{detail}]" if detail else ""))


def copy_site(dst):
    def cp(src, d):
        if src.endswith(MEDIA_EXT):
            try:
                os.link(src, d)
                return d
            except OSError:
                pass
        return shutil.copy2(src, d)
    shutil.copytree(REPO, dst, copy_function=cp, ignore=shutil.ignore_patterns(".git", "node_modules"))


def free_port():
    with closing(socket.socket()) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def cookie(ctx, name):
    for c in ctx.cookies():
        if c["name"] == name:
            return urllib.parse.unquote(c["value"])
    return None


def set_cookies(ctx, base, **kv):
    ctx.add_cookies([{"name": k, "value": urllib.parse.quote(v, safe=""), "url": base} for k, v in kv.items()])


def visible_new(page):
    return page.locator("[data-new]:visible").all_text_contents()


def main():
    out = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else None
    tmp = tempfile.mkdtemp(prefix="new-tags-")
    site = os.path.join(tmp, "site")
    copy_site(site)
    port = free_port()
    base = f"http://127.0.0.1:{port}"
    srv = subprocess.Popen([sys.executable, "-m", "http.server", str(port), "--bind", "127.0.0.1"], cwd=site,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(0.8)
    browser_used = ""
    try:
        with sync_playwright() as p:
            try:
                browser = p.chromium.launch(channel="chrome")
                browser_used = "Google Chrome (headless)"
            except Exception:
                browser = p.chromium.launch()
                browser_used = "Playwright Chromium (headless)"

            # --- dates are in the HTML even without JS ---
            ctx0 = browser.new_context(java_script_enabled=False)
            pg = ctx0.new_page()
            pg.goto(base + BOOK, wait_until="domcontentloaded")
            body = pg.inner_text("body")
            check("book page shows Published Nov 22, 2026 without JS", "Published Nov 22, 2026" in body, body[body.find("Published"):body.find("Published")+80] if "Published" in body else "missing")
            check("book page shows Updated Nov 24, 2026 without JS", "Updated Nov 24, 2026" in body)
            html = pg.content()
            check("book page JSON-LD has VideoObject uploadDate 2026-11-22",
                  '"@type": "VideoObject"' in html and '"uploadDate": "2026-11-22"' in html)
            check("book page JSON-LD has dateModified 2026-11-24", '"dateModified": "2026-11-24"' in html)
            pg.goto(base + AI_TIPS_03, wait_until="domcontentloaded")
            body = pg.inner_text("body")
            check("unchanged lesson shows Published Nov 21, 2026 and no Updated",
                  "Published Nov 21, 2026" in body and "Updated " not in pg.locator(".lesson-meta").inner_text())
            ctx0.close()

            # --- first visit: no New tags; cookies are set ---
            ctx = browser.new_context()
            pg = ctx.new_page()
            pg.goto(base + HOME, wait_until="domcontentloaded")
            tags = visible_new(pg)
            check("first visit on home: no New tags", tags == [], f"visible={tags}")
            check("first visit sets visit_ref=first", cookie(ctx, "visit_ref") == "first", f"visit_ref={cookie(ctx, 'visit_ref')}")
            last = cookie(ctx, "last_visit")
            check("first visit sets last_visit to a unix timestamp",
                  last is not None and last.isdigit() and int(last) > 1_700_000_000, f"last_visit={last}")
            stored_last = last
            pg.goto(base + BOOK, wait_until="domcontentloaded")
            tags = visible_new(pg)
            check("same session, book page: still no New tags", tags == [], f"visible={tags}")
            check("same session does not change visit_ref or last_visit",
                  cookie(ctx, "visit_ref") == "first" and cookie(ctx, "last_visit") == stored_last,
                  f"visit_ref={cookie(ctx, 'visit_ref')} last_visit={cookie(ctx, 'last_visit')}")
            ctx.close()

            # --- returning visit after Nov 23: book preview is New, Nov 21 lesson is not ---
            ctx = browser.new_context()
            set_cookies(ctx, base, last_visit=str(CUTOFF), visit_ref=str(CUTOFF))
            pg = ctx.new_page()
            pg.goto(base + BOOK, wait_until="domcontentloaded")
            tags = visible_new(pg)
            check("returning visit: book preview shows a New tag",
                  any(t.strip().lower() == "new" for t in tags), f"visible={tags}")
            check("New tag text is the word New (accessible, not icon-only)",
                  any(t.strip() in ("New", "NEW") or "new" in t.strip().lower() for t in tags), f"visible={tags}")
            # home: book card New, AI Tips (lesson 17, Nov 25) New, SE201 (lesson 9, Nov 24 evening) New
            pg.goto(base + HOME, wait_until="domcontentloaded")
            book_card = pg.locator(".card", has=pg.locator("h3", has_text="Silicon Valley C Players"))
            tips_card = pg.locator(".card", has=pg.locator("h3", has_text="AI Tips"))
            se201_card = pg.locator(".card", has=pg.locator("h3", has_text="Software Engineering 201"))
            check("home book card shows New", book_card.locator("[data-new]:visible").count() == 1)
            check("home AI Tips card shows New (lesson 17 landed after the cutoff)", tips_card.locator("[data-new]:visible").count() == 1)
            check("home SE201 card shows New (lesson 9 landed after the cutoff)", se201_card.locator("[data-new]:visible").count() == 1)
            check("session cookies stay at the seeded cutoff after a second page",
                  cookie(ctx, "visit_ref") == str(CUTOFF) and cookie(ctx, "last_visit") == str(CUTOFF),
                  f"visit_ref={cookie(ctx, 'visit_ref')} last_visit={cookie(ctx, 'last_visit')}")

            # series index: se201-10 (Nov 23) not New; se201-09 (Nov 24, after the cutoff) is the only New
            pg.goto(base + SE201_IDX, wait_until="domcontentloaded")
            check("SE201 series index shows New only on lesson 9 for this cutoff",
                  pg.locator("[data-new]:visible").count() == 1
                  and pg.locator('[data-watch-id="se201/09"] [data-new]:visible').count() == 1,
                  f"count={pg.locator('[data-new]:visible').count()}")
            pg.goto(base + AI_TIPS_03, wait_until="domcontentloaded")
            check("Nov 21 lesson is not tagged New",
                  pg.locator(".lesson-meta [data-new]:visible").count() == 0)
            ctx.close()

            # --- new session after viewing: visit_ref missing, last_visit = now (after book update) → no New ---
            ctx = browser.new_context()
            now = str(int(time.time()) + 60)
            set_cookies(ctx, base, last_visit=now)  # no visit_ref: new session uses last_visit as cutoff
            pg = ctx.new_page()
            pg.goto(base + BOOK, wait_until="domcontentloaded")
            check("later session whose last_visit is now: no New tags",
                  visible_new(pg) == [], f"visible={visible_new(pg)} visit_ref={cookie(ctx, 'visit_ref')}")
            check("new session freezes previous last_visit as visit_ref",
                  cookie(ctx, "visit_ref") == now, f"visit_ref={cookie(ctx, 'visit_ref')}")
            ctx.close()
            browser.close()
    finally:
        srv.terminate()
        srv.wait()
        shutil.rmtree(tmp, ignore_errors=True)

    fails = [r for r in results if not r[1]]
    if out:
        lines = ["# New-tag and publish-date: headless browser test", "",
                 f"- Date: {time.strftime('%Y-%m-%d %H:%M %Z')}",
                 f"- Script: `sitegen/test_new_tags.py` (repo copy in a temp dir, served by `python3 -m http.server`)",
                 f"- Browser: {browser_used}",
                 f"- Cutoff used for the returning-visit checks: {datetime.fromtimestamp(CUTOFF, ET).isoformat()}",
                 f"- Result: **{len(results) - len(fails)} passed, {len(fails)} failed**", "",
                 "| Result | Check | Detail |", "|---|---|---|"]
        lines += [f"| {'PASS' if ok else 'FAIL'} | {n} | {d.replace('|', '/')} |" for n, ok, d in results]
        os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
        open(out, "w").write("\n".join(lines) + "\n")
    print(f"{len(results) - len(fails)} passed, {len(fails)} failed")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
