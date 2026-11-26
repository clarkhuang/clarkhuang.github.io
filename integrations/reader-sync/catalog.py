"""The versioned media served by this checkout's GitHub Pages release."""
import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit


SITE_ROOT = Path(__file__).resolve().parents[2]


class BookPlayers(HTMLParser):
    """Read the bookmark keys used by site.js, indexed by the player's media URL."""

    def __init__(self, page):
        super().__init__()
        self.page = page
        self.players = {}
        self.key = None
        self.anchor = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in {"video", "audio"}:
            self.key = None
            self.anchor = attrs.get("id")
            if attrs.get("data-chapter") and attrs.get("data-video-version"):
                self.key = attrs["data-chapter"] + "@" + attrs["data-video-version"]
        if self.key and tag in {"video", "audio", "source"} and attrs.get("src"):
            self.players[urljoin(self.page, attrs["src"])] = (self.key, self.anchor)

    def handle_endtag(self, tag):
        if tag in {"audio", "video"}:
            self.key = None


def load_catalog(root=SITE_ROOT):
    lessons = json.loads((root / "lessons.json").read_text())
    book = json.loads((root / "book.json").read_text())
    catalog = {}
    for series in lessons["series"]:
        for lesson in series["lessons"]:
            if not lesson.get("video_url"):
                continue
            url = lesson["video_url"]
            captions = lesson.get("captions_url")
            if not captions:
                candidate = url.rsplit(".", 1)[0] + ".vtt"
                if (root / urlsplit(candidate).path.lstrip("/")).is_file():
                    captions = candidate
            catalog[lesson["watched_key"]] = {
                "series_id": series["id"], "series_title": series["title"], "content_id": lesson["id"],
                "title": lesson["title"], "url": url, "page": lesson["page_url"],
                "duration": lesson["duration_seconds"], "captions": captions, "kind": "video",
                "anchor": "lesson-video",
            }

    def add_tracks(content_id, page, title, tracks):
        players = BookPlayers(page)
        players.feed((root / urlsplit(page).path.strip("/") / "index.html").read_text())
        for kind, track in tracks:
            if track and track.get("url"):
                key, anchor = players.players[track["url"]]
                catalog[key] = {"series_id": "book", "series_title": book["title"], "content_id": content_id,
                                "title": title, "url": track["url"], "page": page,
                                "duration": track["duration_seconds"], "kind": kind,
                                "captions": track.get("captions_url"), "anchor": anchor}

    preview_audio = next((t for t in book["audio"]["chapters"] if t["id"] == "preview"), {})
    add_tracks("preview", book["page_url"], book["title"] + " — preview", [
        ("video", book.get("video")),
        ("audio", {**preview_audio, "captions_url": book["audio"].get("captions_url")}),
    ])
    for chapter in book["chapters"]:
        add_tracks(chapter["id"], chapter["page_url"], chapter["title"],
                   [(kind, chapter.get(kind)) for kind in ("video", "audio")])
    return catalog
