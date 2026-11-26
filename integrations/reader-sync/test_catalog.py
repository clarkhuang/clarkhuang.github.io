import json
import unittest
from datetime import timedelta

import mongomock
from app import create_app, digest, now
from catalog import SITE_ROOT, load_catalog


class CatalogProgressTests(unittest.TestCase):
    def setUp(self):
        self.catalog = load_catalog()
        db = mongomock.MongoClient(tz_aware=True).reader_staging
        origin = "https://test.example"
        app = create_app({"READER_ENV": "staging", "READER_ORIGIN": origin,
                          "SESSION_SECRET": "test-only", "GITHUB_CLIENT_ID": "test",
                          "GITHUB_CLIENT_SECRET": "test"}, db)
        self.client = app.test_client()
        self.headers = {"Origin": origin}
        db.sessions.insert_one({"_id": digest("session"), "owner": "1",
                                "expires": now() + timedelta(hours=1)})
        with self.client.session_transaction() as session:
            session["sid"] = "session"

    def write(self, key, position):
        return self.client.put("/api/progress", headers=self.headers,
                               json={"item": key, "position": position,
                                     "completed": False, "revision": 0}).status_code

    def test_real_lesson_bounds_and_version(self):
        lesson = json.loads((SITE_ROOT / "lessons.json").read_text())["series"][0]["lessons"][0]
        key = lesson["watched_key"]
        self.assertEqual(self.write(key, lesson["duration_seconds"] + 1), 400)
        self.assertEqual(self.write(lesson["id"] + "@unknown", 0), 400)
        self.assertEqual(self.write("fabricated/01@12345678", 0), 400)
        self.assertEqual(self.write(key, lesson["duration_seconds"]), 200)

    def test_book_audio_video_keep_independent_versioned_bookmarks(self):
        keys = [key for key in self.catalog if key.startswith("preview@")]
        self.assertEqual({self.catalog[key]["kind"] for key in keys}, {"audio", "video"})
        for key in keys:
            self.assertEqual(self.write(key, 13), 200)
        self.assertEqual({r["item"] for r in self.client.get("/api/progress").json}, set(keys))
