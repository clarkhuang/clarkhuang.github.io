import unittest
from unittest.mock import patch
from urllib.parse import parse_qs, urlsplit

import mongomock
from app import create_app


class OAuthTests(unittest.TestCase):
    def setUp(self):
        settings = dict(READER_ENV="staging", READER_ORIGIN="https://reader.example",
                        GITHUB_CLIENT_ID="test", GITHUB_CLIENT_SECRET="test", SESSION_SECRET="test")
        self.client = create_app(settings, mongomock.MongoClient(tz_aware=True).reader).test_client()
        url = self.client.get("/login").location
        self.query = parse_qs(urlsplit(url).query, keep_blank_values=True)

    def callback(self, responses):
        with patch("app.github_json", side_effect=responses):
            return self.client.get("/callback", query_string={"code": "test", "state": self.query["state"][0]})

    def test_malformed_state_is_rejected(self):
        response = self.client.get("/callback", query_string={"state": "無", "code": "test"})
        self.assertEqual(response.status_code, 400)

    def test_refuses_extra_scopes(self):
        self.assertEqual(self.query["scope"], [""])
        self.assertEqual(self.callback([{"scope": "repo", "access_token": "test"}]).status_code, 403)
        self.assertEqual(self.client.get("/api/profile").status_code, 401)

    def test_malformed_identity_fails_without_creating_session(self):
        self.assertEqual(self.callback([{"scope": "", "access_token": "test"}, {}]).status_code, 502)
        self.assertEqual(self.client.get("/api/profile").status_code, 401)
