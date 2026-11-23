#!/usr/bin/env python3
"""Headless-browser test: watched / resume cookies are keyed per video version ("<id>@<sha256[:8]>").

Copies the site to a temp dir (media hard-linked, HTML copied, so the repo is never written), serves it with
`python3 -m http.server`, and drives it with Playwright (Google Chrome if present, for H.264; else Chromium).

  python3 sitegen/test_watched_versions.py [--out RESULTS.md]

Checks: marking watched writes "id@version"; lesson, series index, and home page show it; a re-rendered video
(changed bytes + re-stamp) shows unwatched and its stale key is pruned; check_site's verify() catches a re-render
that was not re-stamped; legacy unversioned cookies count as unwatched and are dropped; vpos and book_pos are
version-keyed too. Exit 1 if any check fails.
"""
import os, shutil, socket, subprocess, sys, tempfile, time, urllib.parse
from contextlib import closing

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
import stamp_versions  # noqa: E402
from playwright.sync_api import sync_playwright  # noqa: E402

MEDIA_EXT = (".mp4", ".mp3", ".jpg", ".png", ".webp", ".woff2", ".m4a")
SE201_01 = "/software-engineering-201/01-four-eras-of-building-systems/"
SE101_02 = "/software-engineering-101/02-rigor-follows-risk/"
SE201_IDX = "/software-engineering-201/"
results = []


def check(name, ok, detail=""):
    results.append((name, bool(ok), detail))
    print(("PASS " if ok else "FAIL ") + name + (f"  [{detail}]" if detail else ""))


def copy_site(dst):
    def cp(src, d):
        if src.endswith(MEDIA_EXT):
            try: os.link(src, d); return d
            except OSError: pass
        return shutil.copy2(src, d)
    shutil.copytree(REPO, dst, copy_function=cp, ignore=shutil.ignore_patterns(".git", "node_modules"))


def free_port():
    with closing(socket.socket()) as s:
        s.bind(("127.0.0.1", 0)); return s.getsockname()[1]


def cookie(ctx, name):
    for c in ctx.cookies():
        if c["name"] == name: return urllib.parse.unquote(c["value"])
    return None


def set_cookies(ctx, base, **kv):
    ctx.add_cookies([{"name": k, "value": urllib.parse.quote(v, safe=""), "url": base} for k, v in kv.items()])


def main():
    out = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else None
    tmp = tempfile.mkdtemp(prefix="watched-versions-")
    site = os.path.join(tmp, "site")
    copy_site(site)
    port = free_port(); base = f"http://127.0.0.1:{port}"
    srv = subprocess.Popen([sys.executable, "-m", "http.server", str(port), "--bind", "127.0.0.1"], cwd=site,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(0.8)
    v01 = stamp_versions.media_version(os.path.join(site, "videos/se201-01-four-eras-of-building-systems.mp4"))
    v0102 = stamp_versions.media_version(os.path.join(site, "videos/se101-02-rigor-follows-risk.mp4"))
    vbook = stamp_versions.media_version(os.path.join(site, "videos/book-preview.mp4"))
    vaudio = stamp_versions.media_version(os.path.join(site, "audio/book-preview.mp3"))
    browser_used = ""
    try:
        with sync_playwright() as p:
            try: browser = p.chromium.launch(channel="chrome"); browser_used = "Google Chrome (headless)"
            except Exception: browser = p.chromium.launch(); browser_used = "Playwright Chromium (headless)"

            # 1. Mark watched with the button on an SE201 lesson page.
            ctx = browser.new_context(); pg = ctx.new_page()
            pg.goto(base + SE201_01)
            attr = pg.get_attribute("video#lesson-video", "data-video-version")
            check("lesson video carries data-video-version = sha256(mp4)[:8]", attr == v01, f"{attr} vs {v01}")
            pg.click(".lesson-meta [data-toggle-watched]")
            w = cookie(ctx, "watched")
            check("button writes versioned key", w == f"se201/01@{v01}", f"watched={w}")
            check("lesson page shows watched", "is-watched" in (pg.get_attribute(".lesson-meta", "class") or ""))
            check("toggle reads 'Mark as not watched'", pg.inner_text(".lesson-meta [data-toggle-watched]") == "Mark as not watched")
            pg.goto(base + SE201_IDX)
            check("series index: lesson 1 row ticked",
                  "is-watched" in (pg.get_attribute('li[data-watch-id="se201/01"]', "class") or ""))
            cnt = pg.inner_text('[data-progress] .count')
            check("series index: meter counts it", cnt.startswith("1 of "), cnt)
            nxt = pg.eval_on_selector_all("[data-next] a[data-lesson-link]", "as => as.filter(a => !a.hidden).map(a => a.dataset.lessonLink)")
            check("series index: Up next skips it", nxt == ["se201/02"], str(nxt))
            pg.goto(base + "/")
            cnt = pg.eval_on_selector('[data-progress^="se201/"] .count', "e => e.textContent")
            check("home page: SE201 meter counts it", cnt.startswith("1 of "), cnt)

            # 2. 'ended' marks watched with a versioned key (SE101), keeping the SE201 entry.
            pg.goto(base + SE101_02)
            pg.eval_on_selector("video#lesson-video", "v => v.dispatchEvent(new Event('ended'))")
            w = cookie(ctx, "watched")
            check("'ended' event writes versioned key, other ids kept",
                  set((w or "").split(",")) == {f"se201/01@{v01}", f"se101/02@{v0102}"}, f"watched={w}")
            saved_watched = w

            # 3. vpos: real playback, then pause (needs a browser that decodes H.264). Plays rather than seeks
            #    because `python3 -m http.server` has no Range support, so seeking does not land.
            pg.goto(base + SE201_01)
            t = pg.evaluate("""() => new Promise(res => {
                const v = document.getElementById('lesson-video'); v.muted = true;
                v.addEventListener('timeupdate', function tick() {
                  if (v.currentTime > 6.5) { v.removeEventListener('timeupdate', tick); v.pause(); res(v.currentTime); } });
                const p = v.play(); if (p && p.catch) p.catch(() => res(null));
                setTimeout(() => res(null), 20000); })""")
            pg.wait_for_timeout(300)
            vp = cookie(ctx, "vpos")
            if t:
                key, _, secs = (vp or "").rpartition(":")
                check("vpos written on pause with versioned key", key == f"se201/01@{v01}" and abs(float(secs or 0) - t) < 0.5,
                      f"vpos={vp}, paused at {t:.1f}s")
            else:
                check("vpos written on pause (media did not play in this browser; skipped)", True, "skipped")
            ctx.close()

            # 4. Seeded vpos: current version offered; stale version + unversioned keys pruned.
            ctx = browser.new_context(); pg = ctx.new_page()
            set_cookies(ctx, base, vpos=f"se101/03:12.0,se201/01@deadbeef:10.0,se201/01@{v01}:42.0")
            pg.goto(base + SE201_01)
            vp = cookie(ctx, "vpos")
            check("vpos: stale + unversioned keys pruned on load", vp == f"se201/01@{v01}:42.0", f"vpos={vp}")
            pg.wait_for_timeout(300)
            go = pg.eval_on_selector('[data-resume="lesson-video"]', "b => b.hidden ? '' : b.querySelector('[data-go]').textContent")
            check("vpos: resume offered at the current version's position", go == "Resume from 0:42", repr(go))
            ctx.close()

            # 5. Legacy unversioned cookie counts as unwatched and is dropped.
            ctx = browser.new_context(); pg = ctx.new_page()
            set_cookies(ctx, base, watched="se101/02")
            pg.goto(base + SE101_02)
            check("legacy 'watched=se101/02': lesson shows unwatched",
                  "is-watched" not in (pg.get_attribute(".lesson-meta", "class") or ""))
            check("legacy 'watched=se101/02': entry dropped", cookie(ctx, "watched") is None, f"watched={cookie(ctx, 'watched')}")
            set_cookies(ctx, base, watched="se101/02,ai-tips/01")
            pg.goto(base + "/")
            cnt = pg.eval_on_selector('[data-progress^="se101/"] .count', "e => e.textContent")
            check("legacy cookie: home SE101 meter shows 0", cnt.startswith("0 of "), cnt)
            check("legacy cookie: dropped on home page too", cookie(ctx, "watched") is None)
            ctx.close()

            # 6. Keys for ids a page does not show are kept (it cannot judge them).
            ctx = browser.new_context(); pg = ctx.new_page()
            set_cookies(ctx, base, watched="se201/01@0badc0de")
            pg.goto(base + "/ask/")
            check("unknown-on-this-page key kept on /ask/", cookie(ctx, "watched") == "se201/01@0badc0de")
            ctx.close()

            # 7. Book: book_pos keyed per media file; legacy key dropped.
            ctx = browser.new_context(); pg = ctx.new_page()
            set_cookies(ctx, base, book_pos=f"preview:31.2,intro:5.0,preview@{vbook}:61.0")
            pg.goto(base + "/book/")
            bp = cookie(ctx, "book_pos")
            check("book_pos: legacy keys pruned, versioned kept", bp == f"preview@{vbook}:61.0", f"book_pos={bp}")
            pg.wait_for_timeout(300)
            vid = pg.eval_on_selector('[data-resume="book-video"]', "b => b.hidden ? '' : b.querySelector('[data-go]').textContent")
            aud = pg.eval_on_selector_all('[data-resume="book-audio"]', "bs => bs.map(b => b.hidden ? '' : 'shown')")
            check("book: videobook resume offered at 1:01", vid == "Resume from 1:01", repr(vid))
            check("book: audiobook (different file/version) not offered the video's position", aud in ([], [""]),
                  f"audio version {vaudio} != video {vbook}; {aud}")
            ctx.close()

            # 8. Re-render SE201 lesson 1: new bytes. check_site must fail until re-stamped.
            mp4 = os.path.join(site, "videos/se201-01-four-eras-of-building-systems.mp4")
            data = open(mp4, "rb").read(); os.unlink(mp4)          # break the hard link before writing
            with open(mp4, "wb") as f: f.write(data + b"\0re-render\0")
            stale = stamp_versions.verify(site)
            check("check_site verify() fails after a re-render without re-stamping", len(stale) > 0, f"{len(stale)} error(s)")
            changed, errs = stamp_versions.stamp_site(site)
            v01b = stamp_versions.media_version(mp4)
            check("stamp_versions re-stamps pages that show lesson 1", v01b != v01 and not errs and len(changed) >= 3,
                  f"{v01} -> {v01b}; {len(changed)} files: {', '.join(changed)}")
            check("check_site verify() passes after re-stamp", stamp_versions.verify(site) == [])

            ctx = browser.new_context(); pg = ctx.new_page()
            set_cookies(ctx, base, watched=saved_watched, vpos=f"se201/01@{v01}:42.0")
            pg.goto(base + SE201_IDX)
            check("after re-render: series index shows lesson 1 unwatched",
                  "is-watched" not in (pg.get_attribute('li[data-watch-id="se201/01"]', "class") or ""))
            cnt = pg.inner_text('[data-progress] .count')
            check("after re-render: meter back to 0", cnt.startswith("0 of "), cnt)
            w = cookie(ctx, "watched")
            check("after re-render: stale se201/01 key pruned, se101/02 kept", w == f"se101/02@{v0102}", f"watched={w}")
            pg.goto(base + SE201_01)
            check("after re-render: lesson page shows unwatched",
                  "is-watched" not in (pg.get_attribute(".lesson-meta", "class") or "")
                  and pg.inner_text(".lesson-meta [data-toggle-watched]") == "Mark as watched")
            check("after re-render: stale vpos dropped, no resume offer",
                  cookie(ctx, "vpos") is None and pg.eval_on_selector('[data-resume="lesson-video"]', "b => b.hidden"))
            pg.click(".lesson-meta [data-toggle-watched]")
            w = cookie(ctx, "watched")
            check("after re-render: marking again stores the new version", set(w.split(",")) == {f"se101/02@{v0102}", f"se201/01@{v01b}"}, f"watched={w}")
            ctx.close()
            browser.close()
    finally:
        srv.terminate(); srv.wait()
        shutil.rmtree(tmp, ignore_errors=True)

    fails = [r for r in results if not r[1]]
    if out:
        lines = ["# Watched-state versioning: headless browser test", "",
                 f"- Date: {time.strftime('%Y-%m-%d %H:%M %Z')}",
                 f"- Script: `sitegen/test_watched_versions.py` (repo copy in a temp dir, served by `python3 -m http.server`)",
                 f"- Browser: {browser_used}",
                 f"- Versions: se201/01 = `{v01}`, se101/02 = `{v0102}`, book video = `{vbook}`, book audio = `{vaudio}`",
                 f"- Result: **{len(results) - len(fails)} passed, {len(fails)} failed**", "",
                 "| Result | Check | Detail |", "|---|---|---|"]
        lines += [f"| {'PASS' if ok else 'FAIL'} | {n} | {d.replace('|', '/')} |" for n, ok, d in results]
        os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
        open(out, "w").write("\n".join(lines) + "\n")
    print(f"{len(results) - len(fails)} passed, {len(fails)} failed")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
