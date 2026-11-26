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
