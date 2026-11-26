import unittest
from urllib.parse import parse_qs, urlsplit
from unittest.mock import patch

import mongomock

from app import create_app
from catalog import load_catalog


class SignedInLearning(unittest.TestCase):
    def setUp(self):
        self.db = mongomock.MongoClient(tz_aware=True).reader_staging
        self.origin = "https://reader-staging.example"
        cfg = dict(READER_ENV="staging", READER_ORIGIN=self.origin,
                   SESSION_SECRET="only-for-tests", GITHUB_CLIENT_ID="test",
                   GITHUB_CLIENT_SECRET="test")
        self.app = create_app(cfg, self.db)
        self.catalog = load_catalog()
        self.key = next(key for key in self.catalog if key.startswith("se101/"))
        self.first = self.app.test_client()
        self.second = self.app.test_client()

    def sign_in_at(self, client, user):
        entry = client.get("/learn", query_string={"item": self.key})
        self.assertEqual(entry.location, "/login")
        state = parse_qs(urlsplit(client.get(entry.location).location).query)["state"][0]
        with patch("app.github_json", side_effect=[{"access_token": "test"}, {"id": user}]):
            destination = client.get("/callback", query_string={"code": "test", "state": state}).location
        self.assertEqual(parse_qs(urlsplit(destination).query)["item"], [self.key])
        return client.get(destination)

    def test_two_sessions_resume_one_account_on_staging_media(self):
        page = self.sign_in_at(self.first, 123)
        self.assertEqual(page.status_code, 200)
        self.assertIn(b"https://clarkhuang.github.io/staging/videos/", page.data)
        self.assertIn("media-src 'self' https://clarkhuang.github.io", page.headers["Content-Security-Policy"])
        data = dict(item=self.key, revision=0, position=12, completed=False)
        saved = self.first.put("/api/progress", json=data, headers={"Origin": self.origin})
        self.assertEqual(saved.status_code, 200)
        resumed = self.sign_in_at(self.second, 123)
        self.assertIn(b'data-position="12"', resumed.data)
        self.assertIn(b'data-revision="1"', resumed.data)
        other = self.sign_in_at(self.app.test_client(), 321)
        self.assertIn(b'data-position="0"', other.data)
        self.assertEqual(self.second.get("/learn", query_string={"item": "unknown"}).status_code, 404)
        self.assertIn(b"resume at 12 seconds", self.second.get("/learn").data)

    def test_catalog_groups_formats_and_keeps_progress_on_each_link(self):
        from html.parser import HTMLParser

        class Works(HTMLParser):
            def __init__(self):
                super().__init__()
                self.rows = []
                self.links = []
                self.inside = False

            def handle_starttag(self, tag, attrs):
                if tag == "li":
                    self.rows.append("")
                    self.inside = True
                if tag == "a" and self.inside:
                    self.links.append(dict(attrs)["href"])

            def handle_endtag(self, tag):
                if tag == "li":
                    self.inside = False

            def handle_data(self, text):
                if self.inside:
                    self.rows[-1] += text

        self.sign_in_at(self.first, 123)
        preview = {e["kind"]: k for k, e in self.catalog.items() if e["content_id"] == "preview"}
        for kind, key in preview.items():
            response = self.first.put("/api/progress", headers={"Origin": self.origin}, json={
                "item": key, "position": 33, "completed": kind == "audio", "revision": 0,
            })
            self.assertEqual(response.status_code, 200)
        html = self.first.get("/learn").text
        rows = Works()
        rows.feed(html)
        self.assertEqual(len(rows.rows), len({(e["series_id"], e["content_id"]) for e in self.catalog.values()}))
        keys = [parse_qs(urlsplit(link).query)["item"][0] for link in rows.links]
        self.assertCountEqual(keys, self.catalog.keys())
        for title in {e["series_title"] for e in self.catalog.values()}:
            self.assertIn("<h2>" + title + "</h2>", html)
        preview_rows = [" ".join(text.split()) for text in rows.rows if "— preview" in text]
        self.assertEqual(len(preview_rows), 1)
        self.assertIn("Watch — resume at 33 seconds", preview_rows[0])
        self.assertIn("Listen — completed", preview_rows[0])

    def test_same_title_does_not_combine_different_works(self):
        from learning import learning_sections
        record = {"title": "Introduction", "series_id": "books", "series_title": "Books", "kind": "video"}
        entries = {"a@001": dict(record, content_id="chapter-1"), "b@002": dict(record, content_id="chapter-2")}
        section, = learning_sections(entries)
        self.assertEqual(list(section["works"]), ["chapter-1", "chapter-2"])

    def test_return_links_target_exact_public_player_without_account_data(self):
        from catalog import SITE_ROOT
        self.sign_in_at(self.first, 123)
        for key, entry in self.catalog.items():
            with self.subTest(key=key):
                path = urlsplit(entry["page"]).path
                article = (SITE_ROOT / path.strip("/") / "index.html").read_text()
                self.assertIn('id="' + entry["anchor"] + '"', article)
                html = self.first.get("/learn", query_string={"item": key}).text
                href = f'href="https://clarkhuang.github.io/staging{path}#{entry["anchor"]}"'
                self.assertIn(href, html)
                self.assertLess(html.index(href), html.index('id="player"'))
