#!/usr/bin/env python3
"""Generate the clarkhuang.github.io static site. Run after the videos are encoded.
Do not run pages/gen_extra.py against the public site; those behind-the-scenes pages stay on the box.

Environment:
  SITE     output directory (default /workspace/legacy/site). Must already hold index.html (the bio is
           read from it byte-for-byte), videos/, videos/posters/, audio/ and book/cover.jpg.
  CONTENT  series/lesson data (default: content.json next to this file).

Lesson fields in content.json: n, slug, id, title, video (file name in videos/ or null for an outline page),
summary, rule, log + script (render log and scene script, used for chapters), and optionally
"chapters": [[seconds, "Title"], ...] (used when log/script are missing or unreadable),
"duration": seconds (used when ffprobe cannot read the video) and "poster" (file name in videos/posters/).
"""
import json, os, re, html, subprocess, shutil, sys
import ai_friendly as AF

HERE = os.path.dirname(os.path.abspath(__file__))
_PARENT = os.path.abspath(os.path.join(HERE, ".."))
_DEFAULT_SITE = _PARENT if os.path.exists(os.path.join(_PARENT, "book", "cover.jpg")) else "/workspace/legacy/site"
SITE = os.path.abspath(os.environ.get("SITE", _DEFAULT_SITE))
CONTENT = os.environ.get("CONTENT", os.path.join(HERE, "content.json"))
BASE = "https://clarkhuang.github.io"

COVER_ALT = (
    "Book cover for Silicon Valley C Players, a free OpenBook by Clark Huang: "
    "a navy field, a mint brush-stroke letter C over circuit-board mountains, "
    "the kicker A Free OpenBook, and the line An embellished fictional dramatization."
)
COVER_DESCRIPTION = (
    "A portrait book cover (864 times 1152 pixels, 3:4) on a deep navy background. "
    "Across the top, small copper-orange lettering reads A FREE OPENBOOK. "
    "In the center, a large mint-green brush-stroke letter C sits over faint circuit-board "
    "traces shaped like rolling mountains. Below, large white sans-serif type reads "
    "SILICON VALLEY and C PLAYERS on two lines. A smaller, muted line reads "
    "AN EMBELLISHED FICTIONAL DRAMATIZATION. At the bottom, the author name CLARK HUANG "
    "appears in white. There are no photographs and no real company logos. "
    "Charlie Hack is the fictional narrator inside the book; Clark Huang is the author."
)
E = html.escape

BIO = None  # read from existing index.html, kept byte-for-byte
WARN = []

def warn(msg):
    WARN.append(msg); print("warning:", msg, file=sys.stderr)

def probe(p):
    try:
        return float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",p],
                                    capture_output=True,text=True,check=True).stdout)
    except (OSError, subprocess.CalledProcessError, ValueError):
        return None

def mmss(t):
    t = int(t); return f"{t//60}:{t%60:02d}"

def iso_dur(t):
    t = int(round(t)); return f"PT{t//60}M{t%60}S"

def chapters_from_log(log, script):
    starts = {m.group(1): float(m.group(2)) for m in re.finditer(r"^\s+(\d\d\w*?_\w+)\s+([\d.]+)s", open(log).read(), re.M)}
    spec = json.load(open(script)); seen=[]; out=[]
    for sc in spec["scenes"]:
        c = sc.get("chapter","")
        if c and c not in seen:
            seen.append(c); out.append([starts[sc["id"]], AF.chapter_case(c)])
    if out: out[0][0] = 0.0
    return out

def chapters(l):
    """Render log + scene script as before; the lesson's own "chapters" list is the fallback."""
    log, script = l.get("log"), l.get("script")
    if log and script and os.path.exists(log) and os.path.exists(script):
        try:
            return chapters_from_log(log, script)
        except (KeyError, ValueError, json.JSONDecodeError) as e:
            warn(f"{l['id']}: could not read chapters from {log} / {script} ({e!r}); using fallback")
    return [[float(t), str(c)] for t, c in (l.get("chapters") or [])]

def first_sentence(s):
    m = re.match(r"(.+?[.?!])(\s|$)", s)
    return m.group(1) if m else s

NUM = "zero one two three four five six seven eight nine ten eleven twelve".split()
def count_word(n, cap=True):
    w = NUM[n] if n < len(NUM) else str(n)
    return w.capitalize() if cap else w

def plural(n, word):
    return f"{n} {word}" + ("" if n == 1 else "s")

# ------------------------------------------------------------------ content
def load_content(path):
    data = json.load(open(path))
    series = {k: v for k, v in data.items() if not k.startswith("_")}
    for skey, s in series.items():
        for f in ("title", "short", "key", "blurb", "intro", "lessons"):
            if f not in s: sys.exit(f"content: series {skey} is missing '{f}'")
        s.setdefault("soon", [])
        seen = set()
        for l in s["lessons"]:
            for f in ("n", "slug", "id", "title", "summary"):
                if f not in l: sys.exit(f"content: a lesson in {skey} is missing '{f}'")
            if l["id"] in seen: sys.exit(f"content: duplicate lesson id {l['id']}")
            seen.add(l["id"])
            l.setdefault("video", None); l.setdefault("rule", None)
    return series

FOOT_LINKS = [("GitHub","https://github.com/clarkhuang"),("LinkedIn","https://www.linkedin.com/in/clark-huang-technology"),
              ("Truly Free","https://trulyfree.com/"),("Truly Free Home","https://trulyfreehome.com/"),
              ("eCIO","https://getecio.com/"),("eVestech","https://evestech.com/")]

# Public nav only. Behind-the-scenes pages (compare, playbook, research, interview plan) are not published.
NAV = [("Home","/",""),("AI Tips","/ai-tips/","ai-tips"),("SE 101","/software-engineering-101/","software-engineering-101"),
       ("SE 201","/software-engineering-201/","software-engineering-201"),("Book","/book/","book"),("Ask","/ask/","ask")]
NAV_EXTRA = []

def nav_items():
    return NAV + [x for x in NAV_EXTRA if os.path.exists(os.path.join(SITE, x[1].strip("/"), "index.html"))]

def page_url(path):
    rel = path.replace("\\", "/")
    if rel in ("index.html", "/index.html", "", "/"):
        return BASE + "/"
    if rel.endswith("/index.html"):
        return BASE + "/" + rel[:-len("index.html")]
    return BASE + "/" + rel

def font_links():
    return """  <link rel="preload" href="/assets/fonts/ibm-plex-sans-400.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="/assets/fonts/newsreader-600.woff2" as="font" type="font/woff2" crossorigin>
"""

HERO_ART = """<svg class="hero-art" viewBox="0 0 400 320" role="presentation" aria-hidden="true">
  <rect width="400" height="320" fill="none"/>
  <g class="trace-dim trace" fill="none">
    <path d="M20 260 H140 V180 H240"/>
    <path d="M40 40 H160 V120 H300"/>
    <path d="M300 120 V220 H380"/>
    <path d="M140 260 V300"/>
    <rect x="128" y="168" width="24" height="24" rx="2"/>
    <rect x="228" y="108" width="24" height="24" rx="2"/>
    <circle cx="140" cy="260" r="5"/>
    <circle cx="40" cy="40" r="5"/>
    <circle cx="380" cy="220" r="5"/>
  </g>
  <g class="trace glow-line">
    <path d="M30 200 C80 200 90 80 160 80 S260 160 310 90 S360 40 390 70"/>
    <path d="M60 280 C120 240 180 250 220 200 S300 150 360 180"/>
  </g>
  <g class="node">
    <rect x="148" y="68" width="24" height="24" rx="3"/>
    <rect x="208" y="188" width="24" height="24" rx="3"/>
    <circle cx="310" cy="90" r="6"/>
    <circle cx="220" cy="200" r="6"/>
  </g>
</svg>"""

PRIVATE_PATHS = ("compare", "playbook", "interview-plan", "ai-tips/research")

def remove_private_pages():
    for rel in PRIVATE_PATHS:
        pth = os.path.join(SITE, rel)
        if os.path.exists(pth):
            shutil.rmtree(pth)
            print("removed", rel)

def copy_fonts():
    src = os.path.join(HERE, "fonts")
    dst = os.path.join(SITE, "assets", "fonts")
    os.makedirs(dst, exist_ok=True)
    if os.path.isdir(src):
        for name in os.listdir(src):
            if name.endswith(".woff2"):
                shutil.copy2(os.path.join(src, name), os.path.join(dst, name))

def write_share_image():
    """1200×630 typographic share card in the site palette. First-party, no third-party assets."""
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        warn("Pillow is not installed; skipping share.jpg")
        return
    w, h = 1200, 630
    img = Image.new("RGB", (w, h), "#0c1217")
    d = ImageDraw.Draw(img)
    # faint diagonal traces
    for i, y in enumerate(range(40, 630, 46)):
        d.line([(0, y), (w, y - 90)], fill="#1a2a24", width=2)
    d.rectangle((0, 0, 16, h), fill="#4ade80")
    # fonts
    def font(size, bold=False):
        candidates = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        ]
        for c in candidates:
            if os.path.exists(c):
                return ImageFont.truetype(c, size)
        return ImageFont.load_default()
    serif = font(86, True)
    sans = font(28, False)
    small = font(22, False)
    d.text((88, 168), "Clark Huang", font=serif, fill="#f3f7f9")
    d.text((88, 280), "AI-native software learning", font=sans, fill="#4ade80")
    d.text((88, 430), "AI Tips  ·  Software Engineering 101 and 201", font=small, fill="#c2ccd4")
    d.text((88, 470), "Silicon Valley C Players  ·  preview, coming in 2027", font=small, fill="#c2ccd4")
    d.text((88, 560), "clarkhuang.github.io", font=small, fill="#8a9aa8")
    dest = os.path.join(SITE, "assets", "share.jpg")
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    img.save(dest, "JPEG", quality=90, optimize=True)

def write_robots_and_sitemap(series):
    open(os.path.join(SITE, "robots.txt"), "w").write(
        "User-agent: *\nAllow: /\nDisallow: /staging/\n\nSitemap: " + BASE + "/sitemap.xml\n"
    )
    urls = [BASE + "/", BASE + "/book/", BASE + "/contribute/", BASE + "/copy-this/", BASE + "/ask/", BASE + "/credits/", BASE + "/llms.txt", BASE + "/llms-full.txt", BASE + "/search-index.json", BASE + "/credits.json"]
    for skey, s in series.items():
        urls.append(f"{BASE}/{skey}/")
        for l in s["lessons"]:
            urls.append(f"{BASE}/{skey}/{l['slug']}/")
    parts = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        parts.append(f"  <url><loc>{E(u)}</loc></url>")
    parts.append("</urlset>\n")
    open(os.path.join(SITE, "sitemap.xml"), "w").write("\n".join(parts))

def write_404():
    body = """      <h1>Page not found</h1>
      <p class="lede">That address is not on this site. Start from the <a href="/">home page</a>, or browse <a href="/ai-tips/">AI Tips</a>, <a href="/software-engineering-101/">Software Engineering 101</a>, <a href="/software-engineering-201/">Software Engineering 201</a>, or the <a href="/book/">book preview</a>. You can also <a href="/contribute/">contribute with your AI</a> or <a href="/copy-this/">copy this site for yourself</a>.</p>"""
    page("404.html", "Page not found — Clark Huang", "Page not found.", body, "404")

def page_jsonld(title, desc, canon):
    """Schema.org WebPage metadata for the page head; points at the Markdown twin."""
    d = {"@context": "https://schema.org", "@type": "WebPage", "name": title, "description": desc, "url": canon, "inLanguage": "en",
         "isPartOf": {"@type": "WebSite", "name": "Clark Huang", "url": BASE + "/"},
         "author": {"@type": "Person", "name": "Clark Huang", "url": BASE + "/"},
         "license": "https://creativecommons.org/licenses/by-nc-sa/4.0/",
         "encoding": {"@type": "MediaObject", "encodingFormat": "text/markdown", "contentUrl": canon.rsplit("/", 1)[0] + "/index.md"}}
    return '  <script type="application/ld+json">' + json.dumps(d, ensure_ascii=False).replace("</", "<\\/") + '</script>\n'

def page(path, title, desc, body, current="", main_class=""):
    navh = "".join(f'<a href="{h}"{" aria-current=\"page\"" if k==current else ""}>{n}</a>' for n,h,k in nav_items())
    links = "".join(f'<a href="{h}">{n}</a>' for n,h in FOOT_LINKS)
    panel = AF.panel_html(path)
    canon = page_url(path)
    main_attr = f' class="{main_class}"' if main_class else ""
    share = BASE + "/assets/share.jpg"
    extra_head = extra_js = ""
    if current in {"book", "ask", "credits", "contribute"} or main_class == "lesson":
        extra_head = '  <link rel="stylesheet" href="/assets/ask-book.css">\n'
    if current in {"book", "ask"}:
        extra_js = '  <script src="/assets/ask-book.js" defer></script>\n'
    doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{E(title)}</title>
  <meta name="description" content="{E(desc)}">
  <meta name="color-scheme" content="dark light">
  <meta name="theme-color" content="#0c1217" media="(prefers-color-scheme: dark)">
  <meta name="theme-color" content="#f4f1ea" media="(prefers-color-scheme: light)">
  <link rel="canonical" href="{canon}">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Clark Huang">
  <meta property="og:title" content="{E(title)}">
  <meta property="og:description" content="{E(desc)}">
  <meta property="og:url" content="{canon}">
  <meta property="og:image" content="{share}">
  <meta property="og:image:alt" content="Clark Huang — AI-native software learning">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{E(title)}">
  <meta name="twitter:description" content="{E(desc)}">
  <meta name="twitter:image" content="{share}">
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
{font_links()}  <link rel="stylesheet" href="/styles.css">
{extra_head}{AF.head_links()}{page_jsonld(title, desc, canon) if current != "404" else ""}</head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>
  <header class="site-header">
    <div class="wrap">
      <a class="brand" href="/"><span class="brand-name">Clark Huang</span><span class="brand-tag">AI-native software learning</span></a>
      <nav aria-label="Primary">{navh}</nav>
    </div>
  </header>
  <main id="main"{main_attr}>
    <div class="wrap">
{panel}{body}
    </div>
  </main>
  <footer class="site-footer">
    <div class="wrap">
      <div class="footer-cols">
        <nav class="footer-col project-links" aria-label="This project"><p class="footer-h">This project</p><a href="/contribute/">Contribute with your AI</a><a href="/copy-this/">Copy this for yourself</a><a href="/ask/">Ask the Book</a><a href="/credits/">Credits</a><a href="/book/">Book preview</a></nav>
{AF.footer_twins()}        <nav class="footer-col footer-links" aria-label="Elsewhere"><p class="footer-h">Elsewhere</p>{links}</nav>
      </div>
      <div class="footer-fine">
        <p class="ai-line">This entire site and its content were created by AI processes, directed by Clark Huang.</p>
        <p>© 2026 Clark Huang. Progress on this site is saved only in a first-party cookie in your browser. No analytics, no third-party scripts.</p>
        <p class="legal-line"><em>Silicon Valley C Players</em> is an embellished fictional dramatization; names, characters, companies, and places in the story are fictitious or used fictitiously. Lessons and tips are the author's opinions, not professional, legal, or financial advice. Content © Clark Huang, licensed <a href="https://creativecommons.org/licenses/by-nc-sa/4.0/">CC BY-NC-SA 4.0</a>. <a href="https://github.com/clarkhuang/clarkhuang.github.io/blob/main/TAKEDOWN.md">Corrections and takedowns</a> or <a href="mailto:clark75-7bw9ct@mail.grokbot.com">clark75-7bw9ct@mail.grokbot.com</a>.</p>
      </div>
    </div>
  </footer>
  <script src="/assets/site.js" defer></script>
{extra_js}</body>
</html>
"""
    full = os.path.join(SITE, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w").write(doc)

def watch_state(lid, toggle=True):
    """Watched badge (+ manual toggle). Hidden until site.js has read the cookie, so no false 'Not watched'."""
    t = f'<button type="button" class="linkish" data-toggle-watched="{lid}" aria-pressed="false" hidden>Mark as watched</button>' if toggle else ""
    return ('<span class="watch-state"><span class="badge dim unwatched-badge">Not watched</span>'
            '<span class="badge watched-badge"><span class="check" aria-hidden="true">✓</span>Watched</span>' + t + '</span>')

def meter(ids, label):
    n = len(ids)
    return (f'<div class="meter" data-progress="{",".join(ids)}" hidden><progress max="{n}" value="0" aria-label="{E(label)}">0 of {n}</progress>'
            f'<span class="count">0 of {n} watched</span></div>')

def upnext(lessons, href, cls="upnext"):
    """Links to every available lesson, all hidden; site.js reveals the first unwatched one."""
    links = "".join(f'<a href="{href(l)}" data-lesson-link="{l["id"]}" hidden>Lesson {l["n"]}: {E(l["title"])}</a>' for l in lessons)
    return f'<p class="{cls}" data-next hidden>Up next: {links}</p>'

def old_lessons_json():
    try:
        d = json.load(open(os.path.join(SITE, "lessons.json")))
        return {l["id"]: l for s in d.get("series", []) for l in s.get("lessons", [])}
    except (OSError, ValueError):
        return {}

def media_info(l, old):
    """Duration, chapters and poster for a video lesson. Missing media are reported, not fatal."""
    vpath = f"/videos/{l['video']}"
    poster = f"/videos/posters/{l.get('poster') or re.sub(r'\.mp4$', '', l['video']) + '.jpg'}"
    if not os.path.exists(SITE + vpath): warn(f"{l['id']}: video {vpath} not found in SITE")
    if not os.path.exists(SITE + poster): warn(f"{l['id']}: poster {poster} not found in SITE")
    dur = probe(SITE + vpath) if os.path.exists(SITE + vpath) else None
    if dur is None: dur = l.get("duration")
    if dur is None: dur = (old.get(l["id"]) or {}).get("duration_seconds")
    if dur is None: warn(f"{l['id']}: no duration (ffprobe failed and no 'duration' given)")
    return vpath, poster, (float(dur) if dur is not None else None), chapters(l)

def build():
    global BIO
    SERIES = load_content(CONTENT)
    src = open(f"{SITE}/index.html").read()
    BIO = re.search(r'<p class="bio">.*?</p>', src, re.S).group(0)
    old = old_lessons_json()
    lessons_json = {"site": BASE, "generated_by": "AI processes, directed by Clark Huang", "series": []}

    for skey, s in SERIES.items():
        for l in s["lessons"]:
            if l["video"]:
                l["_vpath"], l["_poster"], l["_dur"], l["_ch"] = media_info(l, old)
        avail = [l for l in s["lessons"] if l["video"]]
        sj = {"id": s["key"], "title": s["title"], **({"subtitle": s["subtitle"]} if s.get("subtitle") else {}), "page": f"{BASE}/{skey}/", "markdown_url": f"{BASE}/{skey}/index.md",
              "agents_url": f"{BASE}/{skey}/AGENTS.md",
              "status": "in progress" if avail else "coming soon",
              "summary": s["intro"], "lessons": []}
        # lesson pages
        for i, l in enumerate(s["lessons"]):
            url = f"/{skey}/{l['slug']}/"
            prev = s["lessons"][i-1] if i > 0 else None
            nxt = s["lessons"][i+1] if i+1 < len(s["lessons"]) else None
            pager = '<nav class="pager" aria-label="Lesson navigation">'
            pager += (f'<a class="prev" href="/{skey}/{prev["slug"]}/"><small>Previous</small>Lesson {prev["n"]}: {E(prev["title"])}</a>' if prev
                      else f'<a class="prev" href="/{skey}/"><small>Back</small>All {E(s["title"])} lessons</a>')
            pager += (f'<a class="next" href="/{skey}/{nxt["slug"]}/"><small>Next</small>Lesson {nxt["n"]}: {E(nxt["title"])}</a>' if nxt
                      else (f'<span class="next"><small>Next</small>Lesson {l["n"]+1}: {E(s["soon"][0])}, coming soon</span>' if s["soon"]
                            else f'<a class="next" href="/{skey}/"><small>Series</small>Back to {E(s["title"])}</a>'))
            pager += "</nav>"
            if l["video"]:
                vpath, poster, dur, ch = l["_vpath"], l["_poster"], l["_dur"], l["_ch"]
                dur_txt = mmss(dur) if dur else ""
                if ch:
                    chh = ('<h2 class="label">Chapters</h2><ol class="chapters">' + "".join(
                        f'<li><a href="{vpath}#t={t:.1f}" data-seek="{t:.1f}" data-target="lesson-video"><span class="ts">{mmss(t)}</span><span>{E(c)}</span></a></li>'
                        for t, c in ch) + '</ol><p class="chapter-hint">Select a chapter to jump there in the video.</p>')
                else:
                    chh = '<h2 class="label">Length</h2><p class="muted">' + (f'One short beat, about {dur_txt}. No chapters needed.' if dur else 'One short beat. No chapters needed.') + '</p>'
                if nxt:
                    after = f'<p class="upnext-after">Up next: <a href="/{skey}/{nxt["slug"]}/">Lesson {nxt["n"]}: {E(nxt["title"])}</a>{"" if nxt["video"] else " (outline)"}</p>'
                elif s["soon"]:
                    after = f'<p class="upnext-after">Next in {E(s["short"])}: Lesson {l["n"]+1}, {E(s["soon"][0])}, is coming soon. <a href="/{skey}/">All {E(s["title"])} lessons</a></p>'
                else:
                    after = f'<p class="upnext-after">That is the last lesson so far. <a href="/{skey}/">Back to {E(s["title"])}</a></p>'
                rule = ""
                if l.get("rule"):
                    rid = "rule-" + re.sub(r"[^a-z0-9]+", "-", l["id"].lower())
                    rule = (f'<div class="rulecard" data-status-scope><p class="label">The rule · for your agents</p><p id="{rid}">{E(l["rule"])}</p>'
                            f'<p class="tools"><button type="button" class="btn ghost" data-copy="{rid}" hidden>Copy rule</button><span class="status" role="status" data-status></span></p></div>')
                cap_track = (f'\n        <track kind="captions" srclang="en" label="English" src="/videos/{l["captions"]}" default>' if l.get("captions") else "")
                cap_meta = (f'<span aria-hidden="true">·</span><a href="/videos/{l["captions"]}">Captions (VTT)</a>' if l.get("captions") else "")
                cap_meta += (f'<span aria-hidden="true">·</span><a href="{E(l["source_url"])}">How it was built</a>' if l.get("source_url") else "")
                dur_meta = f'<span><time datetime="{iso_dur(dur)}">{dur_txt}</time></span><span aria-hidden="true">·</span>' if dur else ""
                body = f"""      <p class="crumbs"><a href="/">Home</a> / <a href="/{skey}/">{E(s['title'])}</a> / Lesson {l['n']}</p>
      <h1>{E(l['title'])}</h1>
      <div class="player"><video id="lesson-video" controls preload="metadata" playsinline width="1280" height="720" poster="{poster}" data-lesson-id="{l['id']}" aria-label="Lesson video: {E(l['title'])}">
        <source src="{vpath}" type="video/mp4">{cap_track}
        Your browser can't play this video. <a href="{vpath}">Download the MP4</a>.
      </video></div>
      <div class="lesson-meta" data-watch-id="{l['id']}" data-status-scope>{dur_meta}<span>Narrated in Clark's AI voice</span><span aria-hidden="true">·</span><a href="{vpath}" download>Download MP4</a>{cap_meta}{watch_state(l['id'])}<span class="status" role="status" data-status></span></div>
      <p class="resume" data-resume="lesson-video" hidden><button type="button" class="btn" data-go>Resume</button><button type="button" class="linkish" data-dismiss>Start from the beginning</button></p>
      {after}
      <div class="grid2">
        <section>
          <h2 class="label">The lesson</h2>
          <p>{E(l['summary'])}</p>
          {rule}{('<p class="muted credit">' + l['credit_html'] + '</p>') if l.get('credit_html') else ''}
        </section>
        <aside>{chh}</aside>
      </div>
      {pager}"""
                sj["lessons"].append({"id": l["id"], "number": l["n"], "title": l["title"], "status": "available",
                    "summary": l["summary"], "rule": l["rule"], "page_url": BASE + url, "video_url": BASE + vpath,
                    "poster_url": BASE + poster, "markdown_url": BASE + url + "index.md", "agents_url": BASE + url + "AGENTS.md",
                    "duration_seconds": round(dur, 1) if dur else None,
                    "chapters": [{"start_seconds": round(t, 1), "title": c} for t, c in ch],
                    **({"captions_url": f"{BASE}/videos/{l['captions']}"} if l.get("captions") else {}),
                    **({"source_url": l["source_url"]} if l.get("source_url") else {})})
            else:
                premise = s.get("premise_label") or f"The premise of {s['short']}"
                body = f"""      <p class="crumbs"><a href="/">Home</a> / <a href="/{skey}/">{E(s['title'])}</a> / Lesson {l['n']}</p>
      <h1>{E(l['title'])} <span class="badge soon">Coming soon</span></h1>
      <div class="placeholder"><div><strong>Video coming soon</strong>This lesson is in planning. The video will appear here when it's ready.</div></div>
      <div class="grid2" style="margin-top:34px">
        <section>
          <h2 class="label">The idea</h2>
          <p>{E(l['summary'])}</p>
        </section>
        <aside>
          <h2 class="label">{E(premise)}</h2>
          <p class="muted">{E(s['intro'])}</p>
        </aside>
      </div>
      {pager}"""
                sj["lessons"].append({"id": l["id"], "number": l["n"], "title": l["title"], "status": "coming soon",
                    "summary": l["summary"], "rule": None, "page_url": BASE + url, "video_url": None,
                    "markdown_url": BASE + url + "index.md", "agents_url": BASE + url + "AGENTS.md"})
            page(f"{skey}/{l['slug']}/index.html", f"{l['title']} — {s['title']} — Clark Huang", l["summary"][:155], body, skey, main_class="lesson")
            AF.write_lesson_twins(SITE, skey, s, l)

        for k, t in enumerate(s["soon"], start=len(s["lessons"]) + 1):
            sj["lessons"].append({"id": f"{s['key']}/{k:02d}", "number": k, "title": t, "status": "coming soon", "page_url": None, "video_url": None})
        lessons_json["series"].append(sj)

        # series page
        rows = ""
        for l in s["lessons"]:
            if l["video"]:
                bits = ([mmss(l["_dur"])] if l["_dur"] else []) + ["video"] + ([plural(len(l["_ch"]), "chapter")] if l["_ch"] else [])
                rows += (f'<li class="vid" data-watch-id="{l["id"]}" data-status-scope>'
                         f'<div class="thumb"><img src="{l["_poster"]}" alt="" width="1280" height="720" loading="lazy" decoding="async">'
                         f'<span class="check tick" aria-hidden="true">✓</span></div>'
                         f'<div><h3><a href="/{skey}/{l["slug"]}/"><span class="n">{l["n"]:02d}</span>{E(l["title"])}</a></h3>'
                         f'<p class="sum">{E(first_sentence(l["summary"]))}</p>'
                         f'<p class="meta"><span>{" · ".join(bits)}</span>{watch_state(l["id"])}<span class="status" role="status" data-status></span></p></div></li>')
            else:
                rows += (f'<li><a href="/{skey}/{l["slug"]}/"><span class="n">{l["n"]:02d}</span>'
                         f'<span class="t">{E(l["title"])}<span class="s">Coming soon</span></span><span class="badge soon">Coming soon</span></a></li>')
        for k, t in enumerate(s["soon"], start=len(s["lessons"]) + 1):
            rows += f'<li><div class="row"><span class="n">{k:02d}</span><span class="t">{E(t)}</span><span class="badge dim">Coming soon</span></div></li>'
        prog = ""
        if avail:
            nexts = upnext(avail, lambda l, skey=skey: f"/{skey}/{l['slug']}/")
            prog = (f'<div class="panel" data-status-scope>{meter([l["id"] for l in avail], s["title"] + " lessons watched")}'
                    f'{nexts}'
                    f'<p class="upnext"><button type="button" class="reset" data-reset-progress hidden>Reset progress</button><span class="status" role="status" data-status></span></p>'
                    f'<noscript><p class="small muted" style="margin:6px 0 0">Turn on JavaScript to keep track of which lessons you have watched.</p></noscript></div>')
        outlines = [l for l in s["lessons"] if not l["video"]]
        complete = bool(avail) and not outlines and not s["soon"]
        if complete:
            status = '<span class="badge">Available</span>'
        elif avail:
            status = '<span class="badge">In progress</span>'
        else:
            status = '<span class="badge soon">Coming soon</span>'
        total = len(s["lessons"]) + len(s["soon"])
        body = f"""      <p class="crumbs"><a href="/">Home</a> / {E(s['title'])}</p>
      <h1>{E(s['title'])} {status}</h1>
      {('<p class="label">' + E(s['subtitle']) + '</p>') if s.get('subtitle') else ''}
      <p class="lede">{E(s['intro'])}</p>
      <div class="rule-line"></div>
      <div class="section-head"><h2>Lessons</h2><p class="section-note">{len(avail)} of {total} available</p></div>
      {prog}
      <ol class="lessons">{rows}</ol>"""
        page(f"{skey}/index.html", f"{s['title']}" + (f": {s['subtitle']}" if s.get("subtitle") else "") + " — Clark Huang", s["intro"][:155], body, skey)
        AF.write_series_twins(SITE, skey, s)

    # index
    cards = ""
    for skey, s in SERIES.items():
        avail = [l for l in s["lessons"] if l["video"]]
        outlines = [l for l in s["lessons"] if not l["video"]]
        total = len(s["lessons"]) + len(s["soon"])
        complete = bool(avail) and not outlines and not s["soon"]
        thumb = ""
        if avail and avail[0].get("_poster"):
            thumb = (f'<div class="card-thumb"><img src="{avail[0]["_poster"]}" alt="" width="1280" height="720" loading="lazy" decoding="async"></div>')
        if avail:
            badge = '<span class="badge">Available</span>' if complete else '<span class="badge">In progress</span>'
            meta = f'<span class="card-num">{len(avail)} of {total} lessons</span>{badge}'
            prog = f'<p class="progress">{plural(len(avail), "video lesson")}' + (f', {f"{len(outlines)} coming soon"}' if outlines else "") + '</p>'
            prog += meter([l["id"] for l in avail], s["title"] + " lessons watched")
            links = upnext(avail, lambda l, skey=skey: f"/{skey}/{l['slug']}/", "upnext card-upnext")
        else:
            meta = '<span class="card-num">Next series</span><span class="badge soon">Coming soon</span>'
            prog = f'<p class="progress">{count_word(len(outlines))} lesson{"" if len(outlines)==1 else "s"} coming soon</p>' if outlines else '<p class="progress">In planning</p>'
            links = ""
        cards += (f'<div class="card">{thumb}<a class="card-body-link" href="/{skey}/"><div class="card-meta">{meta}</div><h3>{E(s["title"])}</h3>'
                  f'<p>{E(s["blurb"])}</p>{prog}<span class="card-cta">{"Start watching" if avail else "See the plan"}</span></a>{links}</div>')
    cards += ('<div class="card"><div class="card-thumb cover-thumb"><img src="/book/cover.jpg" alt="' + E(COVER_ALT) + '" width="864" height="1152" loading="lazy" decoding="async"></div>'
              + '<a class="card-body-link" href="/book/"><div class="card-meta"><span class="card-num">OpenBook · Preview</span><span class="badge soon">Coming 2027</span></div>'
              + '<h3>Silicon Valley C Players</h3><p>A free OpenBook that begins by dreaming in green and ends by dreaming about AI. Written and interviewed by AI.</p>'
              + '<p class="progress">Videobook and audio preview</p><span class="card-cta">Watch the preview</span></a></div>')
    body = f"""      <section class="hero" aria-labelledby="about-heading">
        <div class="hero-copy">
          <h1 id="about-heading">Clark Huang</h1>
          {BIO}
          <p class="hero-cta"><a class="btn" href="/ai-tips/">Start with AI Tips</a><a class="btn ghost" href="/book/">Book preview</a></p>
        </div>
        {HERO_ART}
      </section>
      <section aria-labelledby="series-heading" data-status-scope>
        <div class="section-head"><h2 id="series-heading">Learn</h2><p class="section-note">Short video lessons on AI-native software work. Your progress is remembered on this device. <button type="button" class="reset" data-reset-progress hidden>Reset progress</button><span class="status" role="status" data-status></span></p></div>
        <div class="cards">{cards}</div>
        <p class="section-note">This site is also an open project. <a href="/contribute/">Contribute with your AI</a>, or <a href="/copy-this/">copy this for yourself</a>.</p>
      </section>
      <section aria-labelledby="ask-connect-heading">
        <div class="section-head"><h2 id="ask-connect-heading">Ask, connect, contribute</h2><p class="section-note">Search the lessons and the book preview, or hook your own AI to this site.</p></div>
        <div class="cards">
          <a class="card" href="/ask/"><div class="card-meta"><span class="card-num">Ask</span></div><h3>Ask the Book</h3><p>Search lessons, chapters, and transcripts in your browser, or send a cited prompt to ChatGPT, Claude, Grok, or Perplexity.</p><span class="card-cta">Ask a question</span></a>
          <a class="card" href="/contribute/#mcp"><div class="card-meta"><span class="card-num">MCP</span></div><h3>Connect your AI</h3><p>A public, read-only GitMCP endpoint at <span class="url">gitmcp.io/<wbr>clarkhuang/<wbr><span class="nobr">clarkhuang.github.io.</span></span> Contributions still go through GitHub issues.</p><span class="card-cta">Get the config</span></a>
          <a class="card" href="/credits/"><div class="card-meta"><span class="card-num">OpenBook</span></div><h3>Contributor credits</h3><p>People who have helped, listed by GitHub handle. You can choose how, or whether, you are credited.</p><span class="card-cta">See the list</span></a>
        </div>
      </section>"""
    page("index.html", "Clark Huang — AI-native software learning",
         "Public learning pages by Clark Huang on AI-native software workflows: AI Tips, Software Engineering 101 and 201, and Silicon Valley C Players, a free OpenBook (an embellished fictional dramatization).", body, "")
    AF.write_home_twin(SITE, SERIES, BIO)
    AF.write_root_agents(SITE)
    AF.write_llms_txt(SITE, SERIES, extras=[
        ("contribute/index.md", "Contribute with your AI", "A copy-paste prompt, GitHub issue forms, and a Connect your AI (MCP) section."),
        ("copy-this/index.md", "Copy this for yourself", "How to fork or use this site as a template for your own OpenBook or learning series."),
        ("ask/index.md", "Ask the Book", "In-browser search of lessons, chapters, scenes, and transcripts, plus a prompt you can send to your own AI."),
        ("credits/index.md", "Contributor credits", "People who have contributed, listed by GitHub handle."),
        ("search-index.json", "search-index.json", "Local search index used by Ask the Book."),
    ])

    lessons_json["book"] = f"{BASE}/book.json"
    lessons_json["agent_rules_note"] = "Each available lesson's 'rule' is written to be loaded by AI agents as a standing instruction. Markdown twins and AGENTS.md live next to every HTML page; the site index for language models is /llms.txt."
    lessons_json["ai_readable"] = {"llms_txt": f"{BASE}/llms.txt", "llms_full_txt": f"{BASE}/llms-full.txt",
                                   "agents_md": f"{BASE}/AGENTS.md", "home_md": f"{BASE}/index.md",
                                   "rebuild_md": f"{BASE}/REBUILD.md",
                                   "note": "Every HTML page has a Markdown twin at the same path with index.md, plus AGENTS.md in the same folder. Staging lives at /staging/ and is not listed here."}
    lessons_json["cookies"] = {"watched": "watched=<lesson id>,<lesson id>...",
                               "video_position": "vpos=<lesson id>:<seconds>[,...] (resume offer, cleared when the video ends)"}
    json.dump(lessons_json, open(f"{SITE}/lessons.json", "w"), indent=2, ensure_ascii=False)
    build_book()
    AF.write_llms_full(SITE, SERIES, INTRO, BACK)
    build_involve_pages()
    shutil.copy(os.path.join(HERE, "site.css"), f"{SITE}/styles.css")
    os.makedirs(f"{SITE}/assets", exist_ok=True)
    shutil.copy(os.path.join(HERE, "site.js"), f"{SITE}/assets/site.js")
    copy_fonts()
    write_share_image()
    write_404()
    write_robots_and_sitemap(SERIES)
    remove_private_pages()
    idx = os.path.join(HERE, "..", "scripts", "build_ai_index.py")
    if os.path.isfile(idx):
        subprocess.check_call([sys.executable, idx, "--search-only"], cwd=SITE)
    print(f"ok: {sum(len(s['lessons']) for s in SERIES.values())} lesson pages in {SITE}" + (f", {len(WARN)} warning(s)" if WARN else ""))

INTRO = [
 "Fair warning. This is an embellished fictional dramatization that may or may not be based on true stories. The narrator is a guy named Charlie Hack. Any resemblance to me is mostly coincidental. Names, characters, companies and events are fictitious, or used fictitiously.",
 "This preview jumps into the middle of the book. Part Three. C Things That Looked Like A Things.",
 "Silicon Valley is very good at telling a story about A players. The people who look like they were always going to win. The companies that look like they were always going to work. The myth is a straight line: a garage, a genius, a ticker symbol. Most of the real work looks nothing like that. It looks like another ordinary Tuesday, doing the next right thing.",
 "From the outside, a C thing can look like an A thing. Applause is loud. The real work is quieter. The book is about that gap: what people saw, and what was really going on.",
 "A C player is not a failure. A C player is the person who was never the smartest in the room, and kept going anyway. There's always someone smarter, richer, wiser. Stay humble. Stay curious.",
 "The Valley falls in love with products. Specific wins. Specific years. I got more out of building a platform: a foundation you can stand on, and build the next thing on, and the thing after that. You don't invent a career in one move. You stack building blocks. Habits. Fundamentals. The unglamorous layer nobody puts on a slide. That layer is what you actually stand on later.",
 "It's all relative, how good you look from the outside. I just kept going. And I kept doing my best.",
 "Then the work itself changed. I'm usually the most excited person in the room about AI. Which is funny, because I should be the saddest. AI came after the code writers first. In my view, AI now writes essentially all of the code. So gear your software engineering practices around that. That's what Software Engineering 101 and 201 are about, and the second half of this book: how to work now, and how companies should use AI.",
 "The book begins with a green-screen dream. It ends by dreaming about AI. This part, in the middle, is the turn. It's free. It's open. And when version one is ready, if you were around for any of it, you get to tell your side. The story is still being written.",
]
BACK = [
 "An embellished fictional dramatization about C players, the gap between applause and the work, and platforms you can actually stand on. A free OpenBook, like open-source software.",
 "This preview is from the middle of the book: Part Three, C Things That Looked Like A Things, and the turn that follows. The Valley tells a story about A players. The real work looks like another Tuesday.",
 "The second half is about how to work now that AI, in Clark's view, writes essentially all of the code, and how companies should use it.",
 "Silicon Valley C Players. Written and interviewed by AI, from Clark Huang's own words. Coming in 2027.",
]


def book_preview_chapters():
    path = f"{SITE}/videos/book-preview-chapters.json"
    if not os.path.exists(path):
        return ""
    try:
        chs = json.load(open(path))
    except (OSError, ValueError):
        return ""
    if not chs:
        return ""
    items = "".join(
        f'<li><a href="/videos/book-preview.mp4#t={c["start_seconds"]:.1f}" data-seek="{c["start_seconds"]:.1f}" data-target="book-video">'
        f'<span class="ts">{mmss(c["start_seconds"])}</span><span>{E(c["title"])}</span></a></li>'
        for c in chs
    )
    return (f'          <details class="chapters-wrap"><summary>Chapters ({len(chs)})</summary>'
            f'<ol class="chapters">{items}</ol></details>\n')


def build_book():
    try:
        prev = json.load(open(f"{SITE}/book.json"))
        prev_ch = {c["id"]: c.get("duration_seconds") for c in prev.get("audio", {}).get("chapters", [])}
        prev_vid = (prev.get("video") or {}).get("duration_seconds")
    except (OSError, ValueError, KeyError, TypeError):
        prev_ch, prev_vid = {}, None
    audio_path = f"{SITE}/audio/book-preview.mp3"
    video_path = f"{SITE}/videos/book-preview.mp4"
    poster_path = f"{SITE}/videos/posters/book-preview.jpg"
    dur = probe(audio_path) or prev_ch.get("preview") or 0
    vdur = probe(video_path) if os.path.exists(video_path) else (prev_vid or 0)
    has_video = os.path.exists(video_path)
    has_poster = os.path.exists(poster_path)
    intro_h = "".join(f"<p>{E(p)}</p>" for p in INTRO)
    back_h = f"<blockquote>{E(BACK[0])}</blockquote>" + "".join(f"<p>{E(p)}</p>" for p in BACK[1:])
    poster_attr = ' poster="/videos/posters/book-preview.jpg"' if has_poster else ""
    if has_video:
        video_block = (
            '          <div class="player"><video id="book-video" controls preload="metadata" playsinline width="1280" height="720"'
            + poster_attr
            + ' data-chapter="preview" aria-label="Videobook preview: Silicon Valley C Players">\n'
            '            <source src="/videos/book-preview.mp4" type="video/mp4">\n'
            + ('            <track kind="captions" src="/videos/book-preview.vtt" srclang="en" label="English">\n'
               if os.path.exists(f"{SITE}/videos/book-preview.vtt") else "")
            + '            Your browser cannot play this video. <a href="/videos/book-preview.mp4">Download the MP4</a>.\n'
            '          </video></div>\n'
            f'          <div class="lesson-meta"><span><time datetime="{iso_dur(vdur)}">{mmss(vdur)}</time></span>'
            '<span aria-hidden="true">·</span><span>Narrated in Clark\'s AI voice</span>'
            '<span aria-hidden="true">·</span><a href="/videos/book-preview.mp4" download>Download MP4</a></div>\n'
            '          <p class="resume" data-resume="book-video" hidden><button type="button" class="btn" data-go>Resume</button>'
            '<button type="button" class="linkish" data-dismiss>Start from the beginning</button></p>\n'
            '          <p class="resume-msg" id="book-resume-preview-video" aria-live="polite"></p>\n'
            + book_preview_chapters()
        )
        video_fmt = (
            '              <a class="fmt" href="#preview-h">\n'
            '                <div class="card-meta"><span class="card-num">Videobook</span><span class="badge">Preview available</span></div>\n'
            '                <h3>Videobook</h3>\n'
            '                <p>The same narration, with playful stick-figure pictures. The player remembers where you stopped.</p>\n'
            '              </a>'
        )
    else:
        video_block = (
            '          <div class="placeholder"><div><strong>Videobook preview</strong>'
            'The matching stick-figure preview is being finished and will appear here.</div></div>\n'
        )
        video_fmt = (
            '              <div class="fmt">\n'
            '                <div class="card-meta"><span class="card-num">Videobook</span><span class="badge soon">Preview coming shortly</span></div>\n'
            '                <h3>Videobook</h3>\n'
            '                <p>The same narration, brought to life with playful, simple stick-figure animations and graphics.</p>\n'
            '              </div>'
        )
    video_dl = (
        f'<a class="dl" href="/videos/book-preview.mp4" download>Preview MP4<small>Videobook · {mmss(vdur)}</small></a>'
        if has_video else ""
    )
    body = f"""      <p class="crumbs"><a href="/">Home</a> / Book</p>
      <div class="book">
        <div>
          <img class="cover" src="/book/cover.jpg" alt="{E(COVER_ALT)}" width="864" height="1152">
          <p class="muted" style="font-size:13px;margin-top:12px">Self-published · A free OpenBook · Audiobook, videobook and ebook · Coming in 2027</p>
        </div>
        <div>
          <h1>Silicon Valley C Players</h1>
          <p class="h1-status"><span class="badge soon">Coming 2027</span></p>
          <p class="lede">A free OpenBook that begins by dreaming in green and ends by dreaming about AI. Written and interviewed by AI, from Clark Huang's own words.</p>
          <p class="disclaimer"><strong>Fair warning.</strong> This is an embellished fictional dramatization that may or may not be based on true stories. The narrator is a fictional C player named Charlie Hack; every name, company, and place in the story has been changed, mixed up, or made up, and any resemblance is coincidental. The how-to-work-with-AI half is real advice, with real sources. Think you recognize someone? You don't — but if something bothers you, <a href="https://github.com/clarkhuang/clarkhuang.github.io/issues/new?template=takedown-request.yml">tell us</a> or <a href="mailto:clark75-7bw9ct@mail.grokbot.com">clark75-7bw9ct@mail.grokbot.com</a> and we will fix it.</p>

          <section class="audiobox preview-lead" id="preview" aria-labelledby="preview-h">
            <h2 id="preview-h">Preview</h2>
            <p class="muted" style="font-size:14px;margin:0 0 12px">A mid-book preview, in Clark's voice, about {mmss(dur)}. From Part Three and the turn that follows.</p>
{video_block}            <p class="muted ai-media-links">Read along: <a href="/book-source/preview/transcript.md">full transcript</a> · <a href="/videos/book-preview.vtt">captions (VTT)</a> · <a href="/videos/book-preview-chapters.json">chapters</a> · <a href="/book-source/preview/script.md">scene script</a> · <a href="/book-source/preview/REBUILD.md">how to rebuild this preview</a> · <a href="/book-source/cover/PROMPT.md">cover brief</a></p>
          </section>

          <section class="openbook" aria-labelledby="openbook-h">
            <h2 id="openbook-h">How the OpenBook works</h2>
            <p>The name is a metaphor: Clark wants to be an open book about this, the way open-source software is open. Silicon Valley C Players will be free.</p>
            <ol class="openbook-steps">
              <li><strong>Anyone can take part from day one.</strong> Share a story, a correction, or an improvement. <a href="/contribute/">Contribute with your AI</a> — one prompt, then a GitHub issue. Clark is the only gate: nothing is built or published until he approves it.</li>
              <li><strong>Version one still comes first,</strong> in 2027: Clark's account, then a wider invitation to anyone who recognizes a story, or is related to him, to add their side, and stories he may have forgotten.</li>
              <li><strong>Versions work like software.</strong> Later editions are numbered. Previous audiobook and videobook editions stay up as tagged releases, and the next edition is only rebuilt when Clark approves it.</li>
            </ol>
            <p class="muted">Want the same idea for your own learning site or OpenBook? <a href="/copy-this/">Copy this for yourself</a>.</p>
          </section>


          <section class="audiobox" aria-labelledby="listen-h">
            <h2 class="label" id="listen-h">Listen without the pictures</h2>
            <p class="muted" style="font-size:14px;margin:0">The same narration as an audio track · {mmss(dur)} · your place is bookmarked automatically on this device</p>
            <audio id="book-audio" controls preload="metadata" data-chapter="preview">
              <source src="/audio/book-preview.mp3" type="audio/mpeg">
              <track kind="captions" src="/audio/book-preview.vtt" srclang="en" label="English">
              Your browser cannot play this audio. <a href="/audio/book-preview.mp3">Download the preview MP3</a>.
            </audio>
            <p class="resume" data-resume="book-audio" hidden><button type="button" class="btn" data-go>Resume</button><button type="button" class="linkish" data-dismiss>Start from the beginning</button></p>
            <p class="resume-msg" id="book-resume-preview" aria-live="polite"></p>
            <h3 class="label" style="margin-top:20px">Downloads</h3>
            <div class="downloads">
              <a class="dl" href="/audio/book-preview.mp3" download>Preview MP3<small>Audio · {mmss(dur)}</small></a>
              {video_dl}
              <span class="dl is-later">Audiobook MP3<small>Available in 2027</small></span>
              <span class="dl is-later">Audiobook M4B<small>Available in 2027</small></span>
              <span class="dl is-later">Ebook EPUB<small>Available in 2027</small></span>
            </div>
          </section>

          <details class="transcript-wrap" aria-labelledby="intro-h">
            <summary id="intro-h">Read the transcript</summary>
            <div class="transcript-body">{intro_h}</div>
          </details>
          <section class="backcover" aria-labelledby="back-h">
            <h2 class="label" id="back-h">From the back cover</h2>
            {back_h}
            <p class="muted" style="font-size:14px;margin:0 0 10px">A free OpenBook. Self-published. Written and interviewed by AI. Coming in 2027.</p>
          </section>
        </div>
      </div>
      <section aria-labelledby="ask-connect-book-h" style="margin-top:36px">
        <h2 id="ask-connect-book-h">Ask, connect, contribute</h2>
        <p>Search this preview, or send a question to your own AI, from <a href="/ask/">Ask the Book</a>. For book questions, you can ask the tool to answer in the tone of Charlie Hack, the book's fictional narrator. Story chapters are an embellished fictional dramatization; they are not facts about real people.</p>
        <p>Connect an AI assistant with the public, read-only GitMCP endpoint <code>https://gitmcp.io/clarkhuang/clarkhuang.github.io</code>. Config snippets for Claude Code, Claude Desktop, Cursor, and ChatGPT are on the <a href="/contribute/#mcp">Contribute</a> and <a href="/ask/#mcp">Ask the Book</a> pages. GitMCP is a free third-party service and cannot change the book; contributions go through GitHub issues. <a href="/credits/">Contributor credits</a> are listed by GitHub handle.</p>
        <div data-ask-book-mount></div>
      </section>"""
    page("book/index.html", "Silicon Valley C Players — a free OpenBook by Clark Huang (preview)",
         "Silicon Valley C Players, a free OpenBook by Clark Huang: an embellished fictional dramatization, with an audiobook and videobook preview. Written and interviewed by AI. Coming in 2027.", body, "book")
    video_meta = None
    formats = [{"format": "audiobook", "status": "preview available"}]
    if has_video:
        video_meta = {"title": "Videobook preview", "url": f"{BASE}/videos/book-preview.mp4",
                      "duration_seconds": round(vdur, 1) if vdur else None,
                      "poster_url": f"{BASE}/videos/posters/book-preview.jpg" if has_poster else None,
                      "captions_url": f"{BASE}/videos/book-preview.vtt",
                      "chapters_url": f"{BASE}/videos/book-preview-chapters.json",
                      "transcript_url": f"{BASE}/book-source/preview/transcript.md",
                      "script_url": f"{BASE}/book-source/preview/script.md",
                      "script_json_url": f"{BASE}/book-source/preview/script.json",
                      "scenes_url": f"{BASE}/book-source/preview/scenes/",
                      "rebuild_url": f"{BASE}/book-source/preview/REBUILD.md"}
        formats.insert(0, {"format": "videobook", "status": "preview available",
                           "description": "The same narration with playful, simple stick-figure animations and graphics."})
    else:
        formats.append({"format": "videobook", "status": "preview coming shortly",
                        "description": "The same narration with playful, simple stick-figure animations and graphics."})
    json.dump({"title": "Silicon Valley C Players", "subtitle": "A free OpenBook", "author": "Clark Huang", "status": "preview",
               "release": "2027", "publishing": "self-published",
               "concept": "A free OpenBook, like open-source software. Version one comes first; then people who recognize a story, or are related to Clark, can add their side, and stories he may have forgotten. A contribution path is already open; a broader invitation comes with v1.",
               "formats": formats, "method": "written and interviewed by AI",
               "disclaimer": "An embellished fictional dramatization that may or may not be based on true stories. The narrator is a fictional C player named Charlie Hack; every name, company, and place in the story has been changed, mixed up, or made up, and any resemblance is coincidental. The how-to-work-with-AI half is real advice, with real sources.",
               "page_url": f"{BASE}/book/", "cover_url": f"{BASE}/book/cover.jpg",
               "cover": {"url": f"{BASE}/book/cover.jpg", "width": 864, "height": 1152,
                         "alt": COVER_ALT, "description": COVER_DESCRIPTION,
                         "prompt_url": f"{BASE}/book-source/cover/PROMPT.md",
                         "rebuild_url": f"{BASE}/book-source/cover/render_cover.py",
                         "base_art_url": f"{BASE}/book-source/cover/base-art.png"},
               "introduction": INTRO, "back_cover": BACK,
               "video": video_meta,
               "preview": {"transcript_url": f"{BASE}/book-source/preview/transcript.md",
                           "script_url": f"{BASE}/book-source/preview/script.md",
                           "script_json_url": f"{BASE}/book-source/preview/script.json",
                           "scenes_url": f"{BASE}/book-source/preview/scenes/",
                           "captions_url": f"{BASE}/videos/book-preview.vtt",
                           "audio_captions_url": f"{BASE}/audio/book-preview.vtt",
                           "chapters_url": f"{BASE}/videos/book-preview-chapters.json",
                           "audio_chapters_url": f"{BASE}/audio/book-preview-chapters.json",
                           "rebuild_url": f"{BASE}/book-source/preview/REBUILD.md",
                           "how_to_cite": "Quote the transcript or a scene file and give a chapter title or timestamp. For the web, use https://clarkhuang.github.io/book/ plus a media timestamp (#t=58.9). Charlie Hack is the fictional narrator; Clark Huang is the author. Do not identify real people or companies behind the fictional names."},
               "ai_readable": {"llms_txt": f"{BASE}/llms.txt", "llms_full_txt": f"{BASE}/llms-full.txt",
                               "book_md": f"{BASE}/book/index.md", "agents_md": f"{BASE}/book/AGENTS.md",
                               "rebuild_md": f"{BASE}/REBUILD.md"},
               "audio": {"bookmark_cookie": "book_pos=<chapter>:<seconds>[,<chapter>:<seconds>...]", "resume": "offered as a 'Resume from m:ss' button; cleared when the track ends",
                         "captions_url": f"{BASE}/audio/book-preview.vtt",
                         "chapters_url": f"{BASE}/audio/book-preview-chapters.json",
                         "transcript_url": f"{BASE}/book-source/preview/transcript.md",
                         "chapters": [{"id": "preview", "title": "Book preview", "status": "available",
                                       "url": f"{BASE}/audio/book-preview.mp3", "duration_seconds": round(dur, 1)},
                                      {"id": "full", "title": "Full audiobook", "status": "coming in 2027", "url": None}]},
               "downloads": [{"format": "MP3", "status": "preview available", "url": f"{BASE}/audio/book-preview.mp3"},
                             *([{"format": "MP4", "title": "Videobook preview", "status": "preview available", "url": f"{BASE}/videos/book-preview.mp4"}] if has_video else []),
                             {"format": "MP3 (full)", "status": "available in 2027", "url": None},
                             {"format": "M4B", "status": "available in 2027", "url": None},
                             {"format": "EPUB", "status": "available in 2027", "url": None}]},
              open(f"{SITE}/book.json", "w"), indent=2, ensure_ascii=False)
    AF.write_book_twin(SITE, INTRO, BACK, [
        {"title": "Book preview (audio)", "url": f"{BASE}/audio/book-preview.mp3", "duration_seconds": round(dur, 1)},
        {"title": "Full audiobook", "url": None},
    ], video_meta=video_meta)



CONTRIBUTE_PROMPT = """Please help me contribute to Clark Huang's free OpenBook and learning site at https://clarkhuang.github.io/

1. Read https://clarkhuang.github.io/llms.txt and https://clarkhuang.github.io/AGENTS.md (and the AGENTS.md next to any page I share with you).
2. Look at open issues: https://github.com/clarkhuang/clarkhuang.github.io/issues
3. Either pick an open issue labeled "good first issue", or help me propose one of these:
   - a correction (an edit to the book, or my side of a story already in it)
   - a new story or chapter idea
   - a refactor (cleanup or an improvement that does not change the facts)
4. Draft a GitHub issue I can paste, using the matching template:
   - Correction: https://github.com/clarkhuang/clarkhuang.github.io/issues/new?template=correction.yml
   - New story: https://github.com/clarkhuang/clarkhuang.github.io/issues/new?template=new-story.yml
   - Refactor: https://github.com/clarkhuang/clarkhuang.github.io/issues/new?template=refactor.yml
5. Do not invent stories or details. Do not use real names of private people, or real company names, in story submissions. Describe people by role and companies in general terms. Stick to what I actually tell you.
"""

MCP_HTML = '\n      <section class="mcp-block" id="mcp" aria-labelledby="mcp-h">\n        <h2 id="mcp-h">Connect your AI (MCP)</h2>\n        <p>This project has a public, read-only <a href="https://gitmcp.io">GitMCP</a> endpoint:</p>\n        <p><code>https://gitmcp.io/clarkhuang/clarkhuang.github.io</code></p>\n        <p>GitMCP is a free third-party service. It is not affiliated with this site. It only reads public documentation (it prefers <a href="/llms.txt">llms.txt</a>) and public code. It cannot open issues, merge pull requests, or change the book. Contributions still go through GitHub issues, as described above.</p>\n        <p>The tools it exposes for this repository are <code>fetch_clarkhuang_docs</code>, <code>search_clarkhuang_docs</code>, <code>search_clarkhuang_code</code>, and <code>fetch_generic_url_content</code>.</p>\n        <h3>Claude Code</h3>\n        <pre class="config" id="mcp-claude-code" tabindex="0">claude mcp add --transport http clarkhuang https://gitmcp.io/clarkhuang/clarkhuang.github.io</pre>\n        <p class="tools" data-status-scope><button type="button" class="btn ghost" data-copy="mcp-claude-code" hidden>Copy command</button><span class="status" role="status" data-status></span></p>\n        <h3>Claude Desktop</h3>\n        <p>If your Claude Desktop build supports a remote HTTP MCP server, add the URL above. Otherwise use the <code>mcp-remote</code> bridge in <code>claude_desktop_config.json</code>:</p>\n        <pre class="config" id="mcp-claude-desktop" tabindex="0">{\n  "mcpServers": {\n    "clarkhuang": {\n      "command": "npx",\n      "args": ["mcp-remote", "https://gitmcp.io/clarkhuang/clarkhuang.github.io"]\n    }\n  }\n}</pre>\n        <p class="tools" data-status-scope><button type="button" class="btn ghost" data-copy="mcp-claude-desktop" hidden>Copy config</button><span class="status" role="status" data-status></span></p>\n        <h3>Cursor</h3>\n        <p>Add this to <code>~/.cursor/mcp.json</code> (or the project <code>.cursor/mcp.json</code>):</p>\n        <pre class="config" id="mcp-cursor" tabindex="0">{\n  "mcpServers": {\n    "clarkhuang": {\n      "url": "https://gitmcp.io/clarkhuang/clarkhuang.github.io"\n    }\n  }\n}</pre>\n        <p class="tools" data-status-scope><button type="button" class="btn ghost" data-copy="mcp-cursor" hidden>Copy config</button><span class="status" role="status" data-status></span></p>\n        <h3>ChatGPT and other connectors</h3>\n        <p>Paste this as the connector / MCP server URL (Streamable HTTP):</p>\n        <pre class="config" id="mcp-url" tabindex="0">https://gitmcp.io/clarkhuang/clarkhuang.github.io</pre>\n        <p class="tools" data-status-scope><button type="button" class="btn ghost" data-copy="mcp-url" hidden>Copy URL</button><span class="status" role="status" data-status></span></p>\n        <h3>Example prompts</h3>\n        <ul>\n          <li>“Using the clarkhuang GitMCP tools, what is <em>Silicon Valley C Players</em>, and how can I contribute a story without using real names?”</li>\n          <li>“Search the docs for the standing rule in AI Tips lesson 1 and quote it, with a link to the Markdown twin.”</li>\n          <li>“Fetch the documentation, then list the Software Engineering 101 lessons and their rules.”</li>\n        </ul>\n        <p class="muted">The same section lives at <a href="mcp-section.md">mcp-section.md</a> and on <a href="/ask/#mcp">Ask the Book</a>.</p>\n      </section>\n'

def build_involve_pages():
    prompt = E(CONTRIBUTE_PROMPT.strip())
    body = f"""      <p class="crumbs"><a href="/">Home</a> / Contribute</p>
      <h1>Contribute with your AI</h1>
      <p class="lede">You do not have to be a programmer. Point any AI chat tool at this site, tell it what you know, and let it draft a GitHub issue. Clark reviews every issue and is the only person who can approve work or publish it.</p>
      <h2>The prompt</h2>
      <p>Copy this, paste it into ChatGPT, Claude, Grok, or any other chat tool, then add your story or idea in your own words.</p>
      <div class="prompt-box" data-status-scope>
        <pre id="contribute-prompt-text" tabindex="0">{prompt}</pre>
        <p class="tools"><button type="button" class="btn ghost" data-copy="contribute-prompt-text" hidden>Copy prompt</button><span class="status" role="status" data-status></span></p>
      </div>
      <h2>If you would rather skip GitHub</h2>
      <p>You still use a short GitHub form — that is how proposals are tracked, like in an open-source project. You do not need to write code. Open the <a href="https://github.com/clarkhuang/clarkhuang.github.io/issues/new?template=new-story.yml">share-a-story form</a> (or the <a href="https://github.com/clarkhuang/clarkhuang.github.io/issues/new?template=correction.yml">correction</a> or <a href="https://github.com/clarkhuang/clarkhuang.github.io/issues/new?template=refactor.yml">refactor</a> form), and ask your AI to help you fill it in. You can paste the prompt above first, then the form fields.</p>
      <p>Please do not include real names of private people, or real company names, in a story. Describe people by role (“my lab partner,” “a team lead”) and companies in general terms (“a startup in San Francisco,” “a firm from Berlin”).</p>
      <h2>What happens next</h2>
      <ol class="steps-plain">
        <li>Your issue is labeled for Clark to review.</li>
        <li>If he wants it built, he adds an approved label. Only his label or comment starts an agent.</li>
        <li>An agent drafts the change as a pull request. Nothing goes live until Clark merges it.</li>
      </ol>
      <p class="involve-links"><a class="btn" href="https://github.com/clarkhuang/clarkhuang.github.io/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22">See starter issues</a><a class="btn ghost" href="/copy-this/">Copy this site for yourself</a></p>
      <p class="muted">If something in the book or on this site affects you, please use a <a href="https://github.com/clarkhuang/clarkhuang.github.io/issues/new?template=takedown-request.yml">takedown request</a> instead. Full policy: the takedown note in the repository.</p>
"""
    body += MCP_HTML
    page("contribute/index.html", "Contribute with your AI — Clark Huang",
         "A plain-language way to contribute to Clark Huang's OpenBook and learning site: one copy-paste prompt, then a GitHub issue. Clark approves every change.",
         body, "contribute")
    AF.write_prose_twins(SITE, "contribute/index.html", "Contribute with your AI",
        "You can contribute to this OpenBook and the learning series by pointing any AI chat tool at the site. Copy the prompt on this page, add what you know, and have the tool draft a GitHub issue for a correction, a new story, or a refactor. If you would rather skip around GitHub, open the share-a-story form and ask your AI to help you fill it in. Do not invent details or use real names of private people or real company names in story submissions. Only Clark Huang approves work and publishes it.",
        "A plain-language contribution page with one copy-paste prompt and links to GitHub issue forms. No email address is published.")

    body = """      <p class="crumbs"><a href="/">Home</a> / Copy this</p>
      <h1>Copy this for yourself</h1>
      <p class="lede">This site is a demonstration of how an OpenBook and a short video learning series can be built in the open, with AI, the way a software project is run. You are welcome to copy the idea and the repository for your own work.</p>
      <h2>Use it as a template</h2>
      <p>The repository is a GitHub template. On <a href="https://github.com/clarkhuang/clarkhuang.github.io">clarkhuang/clarkhuang.github.io</a>, choose <strong>Use this template</strong>, then <strong>Create a new repository</strong>. Or fork the repository if you would rather keep a link to the original.</p>
      <ol class="steps-plain">
        <li>Create your copy of the repository.</li>
        <li>In the repository settings, turn on GitHub Pages from the <code>main</code> branch, at the root.</li>
        <li>Replace the home-page bio, the lesson text, and the book preview with your own material. Keep the <code>llms.txt</code>, <code>AGENTS.md</code>, and “Use this page with your AI” prompt, so other people (and their AIs) can read your site the same way.</li>
        <li>If you keep the OpenBook workflow, leave the issue templates, the <code>approved</code> label gate, and the <code>next-revision</code> branch in place, then add your own review rules.</li>
      </ol>
      <p>The live site is static: plain HTML, CSS, and a small script, plus video and audio files. There is no build step on GitHub Pages. The generator that produces the pages lives alongside the published files in this project, so you can change the source and regenerate, or edit the HTML directly.</p>
      <h2>What you can and cannot copy</h2>
      <p>The <em>idea</em> — an OpenBook, AI-friendly lesson pages, issue-driven revisions — is yours to reuse. Book text in this repository is licensed <a href="https://creativecommons.org/licenses/by-nc-sa/4.0/">CC BY-NC-SA 4.0</a>: you may share and adapt it with credit, not for commercial use, and under the same license. Do not present Clark's stories as your own life. Lessons and tips are his opinions, not professional advice.</p>
      <p class="involve-links"><a class="btn" href="https://github.com/clarkhuang/clarkhuang.github.io">Open the repository</a><a class="btn ghost" href="/contribute/">Contribute to this one</a></p>
"""
    page("copy-this/index.html", "Copy this for yourself — Clark Huang",
         "How to fork or use Clark Huang's site as a template for your own OpenBook or AI-friendly learning series.",
         body, "copy-this")
    AF.write_prose_twins(SITE, "copy-this/index.html", "Copy this for yourself",
        "This repository is a GitHub template. Use it to create your own OpenBook or short video learning series: enable GitHub Pages from the main branch, replace the bio, lessons and book preview, and keep the AI-friendly files (llms.txt, AGENTS.md, and the copy-paste prompt). Book text is licensed CC BY-NC-SA 4.0. Do not present Clark's stories as your own.",
        "A plain-language page explaining how to copy this site idea with GitHub's template or fork flow.")


if __name__ == "__main__":
    build()
