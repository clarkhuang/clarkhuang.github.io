import os
import unittest
from uuid import uuid4
from pymongo import MongoClient
from datetime import timedelta
from unittest.mock import patch
import mongomock
from app import create_app, digest, now
from catalog import load_catalog

class ReaderTests(unittest.TestCase):
    def setUp(self):
        test_uri = os.environ.get("READER_TEST_MONGO")
        client = MongoClient(test_uri, tz_aware=True) if test_uri else mongomock.MongoClient(tz_aware=True)
        self.db = client["reader_test_" + uuid4().hex]
        self.addCleanup(client.close)
        self.addCleanup(client.drop_database, self.db.name)
        self.origin="https://test.example"
        app=create_app({"READER_ENV":"staging","READER_ORIGIN":self.origin,"SESSION_SECRET":"test-only","GITHUB_CLIENT_ID":"test","GITHUB_CLIENT_SECRET":"test"},self.db)
        self.a,self.b,self.agent=(app.test_client() for _ in range(3))
        self.headers={"Origin":self.origin}
        for client,owner in ((self.a,"1"),(self.b,"2")):
            self.db.sessions.insert_one({"_id":digest(owner),"owner":owner,"expires":now()+timedelta(hours=1)})
            with client.session_transaction() as sess: sess["sid"]=owner
    def test_form_page_allows_same_origin_submission_only(self):
        self.assertEqual(self.a.get("/").headers["Referrer-Policy"], "same-origin")
        self.assertEqual(self.a.get("/api/profile").headers["Referrer-Policy"], "no-referrer")
        self.assertEqual(self.a.post("/logout", headers={"Origin": "null"}).status_code, 403)
        self.assertEqual(self.a.post("/logout", headers=self.headers).status_code, 302)

    def test_profiles_and_origin(self):
        self.assertEqual(self.a.post("/profile",data={"goal":"finish 301"}).status_code,403)
        self.a.post("/profile",data={"goal":"finish 301"},headers=self.headers)
        self.assertEqual(self.a.get("/api/profile").json["goal"],"finish 301")
        self.assertEqual(self.b.get("/api/profile").json,{})
    def test_profile_form_partial_updates_validation_and_manual_clear(self):
        self.a.post("/profile", data={"goal": "build a site", "format": "transcript"}, headers=self.headers)
        self.a.post("/profile", data={"hardware": "MacBook Air"}, headers=self.headers)
        self.assertEqual(self.a.get("/api/profile").json, {
            "goal": "build a site", "format": "transcript", "hardware": "MacBook Air"})
        for bad in ({"format": "A" * 241}, {"goal": "two\nlines"}, {"invalid-key": "x"}, {}):
            with self.subTest(bad=bad):
                self.assertEqual(self.a.post("/profile", data=bad, headers=self.headers).status_code, 400)
        response = self.a.post("/profile", data={"format": ""}, headers=self.headers, follow_redirects=True)
        self.assertIn("Profile saved.", response.text)
        self.assertIn("volunteer scheduling app", response.text)
        self.assertEqual(self.a.get("/api/profile").json["format"], "")
        self.assertEqual(self.b.get("/api/profile").json, {})

    def test_hub_save_returns_to_the_environment_matched_pages_hub(self):
        editor = self.a.get("/?source=hub")
        self.assertIn('action="/profile?source=hub"', editor.text)
        response = self.a.post("/profile?source=hub", data={"goal": "private example"},
                               headers=self.headers, follow_redirects=True)
        self.assertIn("https://clarkhuang.github.io/staging/my-learning/", response.text)
        self.assertNotIn("private example", response.text)
        self.assertEqual(self.b.get("/api/profile").json, {})
        anonymous = self.agent.get("/?source=hub")
        self.assertIn('href="/login?source=hub"', anonymous.text)

    def test_profile_requires_origin_even_with_authorization_header(self):
        response = self.a.post("/profile", data={"goal": "unexpected"},
                               headers={"Authorization": "Bearer invalid"})
        self.assertEqual(response.status_code, 403)
        self.assertEqual(self.a.get("/api/profile").json, {})

    def test_agent(self):
        pair=self.agent.post("/agent/pair",json={"name":"Coach","scopes":["progress:write"]}).json
        secret={"device_secret":pair["device_secret"]}
        self.assertEqual(self.agent.post("/agent/redeem",json=secret).status_code,403)
        path = pair["approval_url"].removeprefix(self.origin)
        self.assertIn(pair["user_code"], self.a.get(path, follow_redirects=True).text)
        self.a.post("/approve", data={"pair_key": path.rsplit("/", 1)[1]}, headers=self.headers)
        token=self.agent.post("/agent/redeem",json=secret).json["access_token"]
        headers={"Authorization":"Bearer "+token}
        self.assertEqual(self.agent.post("/agent/redeem",json=secret).json["access_token"],token)
        self.assertEqual(self.agent.get("/api/profile",headers=headers).status_code,403)
        body={"item":next(iter(load_catalog())),"revision":0,"position":20,"completed":False}
        self.assertEqual(self.agent.put("/api/progress",headers=headers,json=body).status_code,200)
        self.assertEqual(self.agent.put("/api/progress",headers=headers,json=body).status_code,409)
        self.assertEqual(self.a.get("/api/progress").json[0]["position"],20)
        self.assertEqual(self.b.get("/api/progress").json,[])
        self.a.post("/revoke/"+digest(token),headers=self.headers)
        self.assertEqual(self.agent.post("/agent/redeem",json=secret).status_code,403)
        self.assertEqual(self.agent.put("/api/progress",headers=headers,json=body).status_code,403)
    def test_pairing_in_two_tabs(self):
        requests = [self.agent.post("/agent/pair", json={"name": name, "scopes": ["progress:read"]}).json
                    for name in ("Study coach", "Lesson guide")]
        keys = []
        for request in requests:
            path = request["approval_url"].removeprefix(self.origin)
            self.assertIn(request["user_code"], self.a.get(path, follow_redirects=True).text)
            keys.append(path.rsplit("/", 1)[1])
        self.assertEqual(self.a.post("/approve", data={"pair_key": keys[0]}, headers=self.headers).status_code, 409)
        for request in requests:
            self.assertEqual(self.agent.post("/agent/redeem", json={"device_secret": request["device_secret"]}).status_code, 403)
        self.assertEqual(self.a.post("/approve", data={"pair_key": keys[1]}, headers=self.headers).status_code, 302)
        self.assertEqual(self.agent.post("/agent/redeem", json={"device_secret": requests[1]["device_secret"]}).status_code, 200)

    def test_retry_window_ends_without_shortening_issued_grant(self):
        pair = self.agent.post("/agent/pair", json={"name": "Coach", "scopes": ["profile:read"]}).json
        path = pair["approval_url"].removeprefix(self.origin)
        self.a.get(path)
        self.a.post("/approve", data={"pair_key": path.rsplit("/", 1)[1]}, headers=self.headers)
        body = {"device_secret": pair["device_secret"]}
        token = self.agent.post("/agent/redeem", json=body).json["access_token"]
        self.db.grants.update_one({"_id": digest(token)}, {"$set": {"pair_until": now() - timedelta(seconds=1)}})
        self.assertEqual(self.agent.post("/agent/redeem", json=body).status_code, 403)
        self.assertEqual(self.agent.get("/api/profile", headers={"Authorization": "Bearer " + token}).status_code, 200)

    def test_login(self):
        with patch("app.github_json",side_effect=[{"access_token":"test"},{"id":789}]):
            self.agent.get("/login")
            with self.agent.session_transaction() as s: state=s["login"][0]
            self.assertEqual(self.agent.get("/callback",query_string={"state":state,"code":"test"}).status_code,302)
            self.assertEqual(self.agent.get("/api/profile").status_code,200)
            self.agent.post("/logout",headers=self.headers)
            self.assertEqual(self.agent.get("/api/profile").status_code,401)
