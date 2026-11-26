import hashlib
import secrets
import unittest
from datetime import timedelta
from unittest.mock import Mock, patch

import mongomock
from app import create_app, digest, now


class ReleaseNoticeTests(unittest.TestCase):
    pages = "https://pages.example"
    reader = "https://reader.example"

    def setUp(self):
        self.db = mongomock.MongoClient(tz_aware=True).reader
        self.app = create_app(dict(READER_ENV="staging", READER_ORIGIN=self.reader, PAGES_ORIGIN=self.pages,
                                   GITHUB_CLIENT_ID="test", GITHUB_CLIENT_SECRET="test", SESSION_SECRET="test"), self.db)
        self.client = self.app.test_client()
        self.releases = [self.entry(1, now() - timedelta(days=7))]
        self.feed = Mock(side_effect=lambda: sorted(self.releases, key=lambda r: -r["sequence"]))
        self.app.config["LOAD_RELEASE_HISTORY"] = self.feed

    @staticmethod
    def entry(number, instant):
        return {"sequence": number, "published_at": instant.isoformat(), "sha": f"{number:040x}",
                "summary": "Release " + str(number)}

    def login(self, client, owner="123"):
        proof, notice = secrets.token_hex(32), secrets.token_hex(32)
        challenge = hashlib.sha256(proof.encode()).hexdigest()
        start = client.post("/pages/login", base_url=self.reader, headers={"Origin": self.pages}, data={
            "page": "/staging/", "challenge": challenge, "notice_challenge": digest(notice)})
        self.assertEqual(start.status_code, 303)
        client.get(start.location, base_url=self.reader)
        with patch("app.github_json", side_effect=[{"access_token": "test"}, {"id": int(owner), "login": "learner"}]):
            result = client.get("/callback", base_url=self.reader, query_string={"state": "pages." + challenge, "code": "test"})
        self.assertEqual(result.status_code, 303)
        return proof, notice

    def call(self, proof, method="visit", data=None, origin=pages):
        return self.client.post("/api/pages/changes/" + method, base_url=self.reader,
                                headers={"Authorization": "Bearer " + proof, "Origin": origin}, json=data)

    def test_new_reader_and_independent_receipts(self):
        identity, notice = self.login(self.client)
        self.assertEqual(self.call(identity).status_code, 401)
        self.assertEqual(self.call(notice, origin="https://other.example").status_code, 403)
        self.assertEqual(self.client.get("/api/pages/identity", base_url=self.reader,
            headers={"Origin": self.pages, "Authorization": "Bearer " + notice}).status_code, 401)
        self.assertEqual(self.client.get("/api/profile", headers={"Authorization": "Bearer " + notice}).status_code, 403)
        self.feed.assert_not_called()
        self.assertEqual(self.call(notice).json["count"], 0)
        state = self.db.reader_notices.find_one({"_id": "123"})
        self.assertIn("last_visit_at", state)
        self.assertIn("last_login_at", state)
        self.client.post("/logout", base_url=self.reader, headers={"Origin": self.reader})
        self.assertEqual(self.call(notice).status_code, 401)

    def test_old_dismissal_preserves_newer_releases_across_visits_and_devices(self):
        _, notice = self.login(self.client)
        self.assertEqual(self.call(notice).json["count"], 0)
        self.releases.append(self.entry(2, now() + timedelta(seconds=1)))
        batch = self.call(notice).json
        self.assertEqual(batch["through"], 2)
        _, device2 = self.login(self.app.test_client())
        self.assertEqual(self.call(device2).json, batch)
        self.assertEqual(self.call(notice, "dismiss", {"through": 1000000}).status_code, 400)
        self.releases.append(self.entry(3, now() + timedelta(seconds=2)))
        self.assertEqual(self.call(device2, "dismiss", {"through": 2}).json["through"], 3)
        latest = self.call(notice).json
        self.assertEqual([r["sequence"] for r in latest["releases"]], [3])
        self.assertEqual(self.call(device2, "dismiss", {"through": 3}).json["count"], 0)
        self.assertEqual(self.call(notice, "dismiss", {"through": 2}).json["count"], 0)

    def test_changes_between_login_and_first_view(self):
        _, notice = self.login(self.client)
        self.releases.append(self.entry(2, now() + timedelta(seconds=1)))
        self.assertEqual(self.call(notice).json["count"], 1)
        # A second reader joining after these releases starts with their own baseline.
        _, other = self.login(self.app.test_client(), owner="456")
        # Move this second reader's baseline forward to model a later real-world login.
        self.db.reader_notices.update_one({"_id": "456"}, {"$set": {"first_login_at": now() + timedelta(seconds=5)}})
        self.assertEqual(self.call(other).json["count"], 0)
        self.assertEqual(self.call(notice).json["through"], 2)
