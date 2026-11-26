import unittest
from datetime import timedelta
from unittest.mock import patch
import mongomock
from app import create_app, digest, now

class ReaderTests(unittest.TestCase):
    def setUp(self):
        self.db=mongomock.MongoClient(tz_aware=True).reader_staging
        self.origin="https://test.example"
        app=create_app({"READER_ENV":"staging","READER_ORIGIN":self.origin,"SESSION_SECRET":"test-only","GITHUB_CLIENT_ID":"test","GITHUB_CLIENT_SECRET":"test"},self.db)
        self.a,self.b,self.agent=(app.test_client() for _ in range(3))
        self.headers={"Origin":self.origin}
        for client,owner in ((self.a,"1"),(self.b,"2")):
            self.db.sessions.insert_one({"_id":digest(owner),"owner":owner,"expires":now()+timedelta(hours=1)})
            with client.session_transaction() as sess: sess["sid"]=owner
    def test_profiles_and_origin(self):
        self.assertEqual(self.a.post("/profile",data={"goal":"finish 301"}).status_code,403)
        self.a.post("/profile",data={"goal":"finish 301"},headers=self.headers)
        self.assertEqual(self.a.get("/api/profile").json["goal"],"finish 301")
        self.assertEqual(self.b.get("/api/profile").json,{})
    def test_agent(self):
        pair=self.agent.post("/agent/pair",json={"name":"Coach","scopes":["progress:write"]}).json
        secret={"device_secret":pair["device_secret"]}
        self.assertEqual(self.agent.post("/agent/redeem",json=secret).status_code,403)
        self.a.get(pair["approval_url"].removeprefix(self.origin))
        self.a.post("/approve",headers=self.headers)
        token=self.agent.post("/agent/redeem",json=secret).json["access_token"]
        headers={"Authorization":"Bearer "+token}
        self.assertEqual(self.agent.post("/agent/redeem",json=secret).status_code,403)
        self.assertEqual(self.agent.get("/api/profile",headers=headers).status_code,403)
        body={"item":"se101/01@abc12345","revision":0,"position":20,"completed":False}
        self.assertEqual(self.agent.put("/api/progress",headers=headers,json=body).status_code,200)
        self.assertEqual(self.agent.put("/api/progress",headers=headers,json=body).status_code,409)
        self.assertEqual(self.a.get("/api/progress").json[0]["position"],20)
        self.assertEqual(self.b.get("/api/progress").json,[])
        self.a.post("/revoke/"+digest(token),headers=self.headers)
        self.assertEqual(self.agent.put("/api/progress",headers=headers,json=body).status_code,403)
    def test_login(self):
        with patch("app.github_json",side_effect=[{"access_token":"test"},{"id":789}]):
            self.agent.get("/login")
            with self.agent.session_transaction() as s: state=s["login"][0]
            self.assertEqual(self.agent.get("/callback",query_string={"state":state,"code":"test"}).status_code,302)
            self.assertEqual(self.agent.get("/api/profile").status_code,200)
            self.agent.post("/logout",headers=self.headers)
            self.assertEqual(self.agent.get("/api/profile").status_code,401)
