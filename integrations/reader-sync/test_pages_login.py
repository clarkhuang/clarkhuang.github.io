import hashlib
import secrets
import unittest
from urllib.parse import parse_qs, urlsplit
from unittest.mock import patch

import mongomock
from app import create_app
from pymongo.errors import ConnectionFailure


class PagesIdentityTests(unittest.TestCase):
    pages = "https://pages.example"
    reader = "https://reader.example"
    page = "/staging/software-engineering-101/"

    def setUp(self):
        self.db = mongomock.MongoClient(tz_aware=True).reader
        self.app = create_app(dict(READER_ENV="staging", READER_ORIGIN=self.reader,
                                   PAGES_ORIGIN=self.pages, GITHUB_CLIENT_ID="test",
                                   GITHUB_CLIENT_SECRET="test", SESSION_SECRET="test"), self.db)
        self.client = self.app.test_client()

    def test_ready_is_exact_origin_and_fails_closed_on_database_error(self):
        path = "/api/pages/ready"
        self.assertEqual(self.client.get(path).status_code, 403)
        self.assertNotIn("Access-Control-Allow-Origin",
                         self.client.get(path, headers={"Origin": self.reader}).headers)
        with patch.object(self.db, "command", return_value={"ok": 1}) as ping:
            response = self.client.get(path, headers={"Origin": self.pages})
            ping.assert_called_once_with("ping")
        self.assertEqual(response.json, {"ready": True, "environment": "staging"})
        self.assertEqual(response.headers["Access-Control-Allow-Origin"], self.pages)
        with patch.object(self.db, "command", side_effect=ConnectionFailure("test")):
            response = self.client.get(path, headers={"Origin": self.pages})
        self.assertEqual(response.status_code, 503)
        self.assertFalse(response.json["ready"])

    def test_cold_start_recovery_get_has_no_login_side_effect(self):
        before = self.db.list_collection_names()
        response = self.client.get("/pages/login?challenge=discarded&return=https://elsewhere.example/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.pages + "/staging/my-learning/", response.text)
        self.assertNotIn("elsewhere.example", response.text)
        self.assertNotIn("Set-Cookie", response.headers)
        self.assertEqual(self.db.list_collection_names(), before)
        self.assertEqual(self.db.pages_logins.count_documents({}), 0)
        self.assertEqual(self.db.sessions.count_documents({}), 0)

    def start(self, page=None):
        proof = secrets.token_hex(32)
        challenge = hashlib.sha256(proof.encode()).hexdigest()
        response = self.client.post("/pages/login", data={"page": page or self.page,
                                                          "challenge": challenge},
                                    headers={"Origin": self.pages}, base_url=self.reader)
        self.assertEqual(response.status_code, 303)
        return proof, response.location

    def authorize(self, continuation):
        response = self.client.get(continuation, base_url=self.reader)
        self.assertEqual(response.status_code, 302)
        return parse_qs(urlsplit(response.location).query)["state"][0]

    def identity(self, proof):
        # Browser omits all reader cookies from the cross-origin identity request.
        return self.app.test_client(use_cookies=False).get(
            "/api/pages/identity", base_url=self.reader,
            headers={"Origin": self.pages, "Authorization": "Bearer " + proof})

    def callback(self, state):
        with patch("app.github_json", side_effect=[{"access_token": "provider"},
                                                   {"id": 123, "login": "learner"}]):
            return self.client.get("/callback", base_url=self.reader,
                                   query_string={"state": state, "code": "provider-code"})

    def test_return_source_and_verify_display_without_reader_cookie(self):
        proof, continuation = self.start()
        self.assertNotIn(proof, continuation)
        state = self.authorize(continuation)
        self.assertEqual(self.identity(proof).status_code, 401)
        self.assertEqual(self.callback(state).location, self.pages + self.page)
        display = self.identity(proof)
        self.assertEqual(display.json, {"login": "learner"})
        self.assertEqual(display.headers["Access-Control-Allow-Origin"], self.pages)
        self.assertEqual(display.headers["Cache-Control"], "no-store")
        self.assertNotIn("Access-Control-Allow-Credentials", display.headers)
        self.assertEqual(self.client.get("/api/profile", headers={
            "Authorization": "Bearer " + proof}, base_url=self.reader).status_code, 403)
        self.assertEqual(self.callback(state).status_code, 400)
        proof2, continuation2 = self.start("/staging/book/")
        self.assertEqual(self.client.get(continuation2, base_url=self.reader).location,
                         self.pages + "/staging/book/")
        self.assertEqual(self.identity(proof2).json, {"login": "learner"})
        self.client.post("/logout", headers={"Origin": self.reader}, base_url=self.reader)
        self.assertEqual(self.identity(proof).status_code, 401)
        self.assertEqual(self.identity(proof2).status_code, 401)

    def test_redirects_preflight_and_cookie_binding(self):
        data = {"challenge": "0" * 64, "page": self.page}
        self.assertEqual(self.client.post("/pages/login", data=data, headers={
            "Origin": "https://elsewhere.example"}).status_code, 403)
        for page in ["/book/", "//evil.example/", "/staging/../book/", "/staging/hey?token=x",
                     "/staging/%2e/", "/staging/\\x/"]:
            with self.subTest(page=page):
                self.assertEqual(self.client.post("/pages/login", data={**data, "page": page},
                    headers={"Origin": self.pages}, base_url=self.reader).status_code, 400)
        preflight = self.client.options("/api/pages/identity", headers={
            "Origin": self.pages, "Access-Control-Request-Headers": "authorization"})
        self.assertEqual(preflight.status_code, 204)
        self.assertEqual(preflight.headers["Access-Control-Allow-Headers"], "Authorization")
        wrong = self.client.options("/api/pages/identity", headers={"Origin": self.reader})
        self.assertNotIn("Access-Control-Allow-Origin", wrong.headers)
        _, continuation = self.start()
        self.assertEqual(self.app.test_client().get(continuation, base_url=self.reader).status_code, 400)

    def test_parallel_tabs_cancellation_leaves_other_flow_intact(self):
        first, path1 = self.start()
        second, path2 = self.start("/staging/about/")
        state1, state2 = self.authorize(path1), self.authorize(path2)
        with patch("app.github_json") as exchange:
            cancel = self.client.get("/callback", query_string={
                "state": state2, "error": "access_denied"}, base_url=self.reader)
            exchange.assert_not_called()
        self.assertEqual(cancel.location, self.pages + "/staging/about/")
        self.assertEqual(self.identity(second).status_code, 401)
        self.assertEqual(self.callback(state1).location, self.pages + self.page)
        self.assertEqual(self.identity(first).json, {"login": "learner"})
