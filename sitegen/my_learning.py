"""Render a public Pages learning directory from this checkout's published catalogs."""
import json
import sys
from html import escape
from pathlib import Path
from urllib.parse import urlsplit

import ai_friendly
import gen

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "integrations/reader-sync"))
from catalog import load_catalog  # Same versioned player keys used by the reader.


def catalog(name):
    return json.loads((ROOT / name).read_text())


def path(url):
    parsed = urlsplit(url)
    if parsed.scheme != "https" or parsed.netloc != "clarkhuang.github.io":
        raise ValueError(f"Unexpected public catalog URL: {url}")
    return parsed.path


def render():
    desc = "Read and watch on the learning site, resume on this device, or open your private reader account."
    html = ['<h1>My learning</h1>',
            '<p class="lede">Choose a lesson or chapter. Each opens here with its transcript and media.</p>',
            '<section data-learning-local hidden><h2>Continue on this device</h2><ul></ul></section>',
            '<section><h2>Your reader account</h2>',
            '<p data-learning-identity>Use GitHub sign-in to access your private profile and account bookmarks.</p>',
            '<p data-learning-account-links hidden></p>',
            '<p>Playback on these public pages saves your place in this browser. '
            'Use the account player to save a position across devices.</p></section>',
            '<h2>Browse courses and book chapters</h2>']
    md = [desc, '## Your reader account',
          'Public lesson playback saves progress on this device. Use the account player for cross-device positions. '
          'Open the private profile to manage preferences and agent permissions.',
          '## Browse courses and book chapters']
    def group(title, entries):
        html.append(f'<details><summary>{escape(title)} ({len(entries)})</summary><ul>')
        md.append("### " + title)
        for label, url, key in entries:
            href = path(url)
            attr = f' data-local-key="{escape(key, quote=True)}"' if key else ""
            html.append(f'<li><a href="{escape(href, quote=True)}"{attr}>{escape(label)}</a></li>')
            md.append(f'- [{label}]({href})')
        html.append('</ul></details>')
    for series in catalog("lessons.json")["series"]:
        group(series["title"], [(f'{l["number"]}. {l["title"]}', l["page_url"], l["watched_key"])
                               for l in series["lessons"] if l["status"] == "available"])
    book = catalog("book.json")
    group(book["title"], [(c["title"], c["page_url"], None) for c in book["chapters"]])
    # Book video and audio have independent positions. Keep the public directory
    # grouped by work while mapping saved playback to the matching player.
    for key, track in load_catalog(ROOT).items():
        if path(track["page"]).startswith("/book/"):
            title = f'{track["title"]} ({track["kind"]})'
            html.append(f'<span hidden data-local-key="{escape(key)}" data-local-path="{escape(path(track["page"]))}"'
                        f' data-local-label="{escape(title, quote=True)}"></span>')
    html.append('<p><a href="/book/">Book preview and audiobook</a> · '
                '<a href="/software-engineering-301/">SE 301 local-compute playbook</a> · '
                '<a href="/software-engineering-401/">SE 401 outline</a></p>')
    md.append('[Book preview and audiobook](/book/) · [SE 301 playbook](/software-engineering-301/) · '
              '[SE 401 outline](/software-engineering-401/)')
    gen.page("my-learning/index.html", "My learning — Clark Huang", desc, "\n".join(html), current="my-learning")
    ai_friendly.write_prose_twins(str(ROOT), "my-learning/index.html", "My learning", "\n\n".join(md), desc)


if __name__ == "__main__":
    render()
