"""Serve the signed-in reader on its own HTTPS origin alongside static Pages."""
import base64
import hashlib
import hmac
import json
import os
import secrets
from datetime import datetime, timedelta, timezone
from urllib.parse import urlencode, urlsplit
from urllib.request import Request, urlopen

from flask import Flask, abort, jsonify, redirect, render_template_string, request, session
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

SCOPES = {"profile:read", "progress:read", "progress:write"}
PROFILE_FIELDS = {"goal", "hardware", "format"}
def now():
    return datetime.now(timezone.utc)

def digest(value):
    return hashlib.sha256(value.encode()).hexdigest()

def github_json(url, *, fields=None, token=None):
    headers = {"Accept": "application/json", "User-Agent": "OpenBook-reader"}
    if token:
        headers["Authorization"] = "Bearer " + token
    with urlopen(Request(url, data=urlencode(fields).encode() if fields else None,
                         headers=headers), timeout=10) as response:
        return json.load(response)

def create_app(config=None, database=None):
    conf = os.environ if config is None else config
    env = conf["READER_ENV"]
    if env not in {"staging", "production"}:
        raise ValueError("READER_ENV must be staging or production")
    origin = conf["READER_ORIGIN"].rstrip("/")
    if urlsplit(origin).scheme != "https" or urlsplit(origin).path:
        raise ValueError("READER_ORIGIN must be an HTTPS origin")
    app = Flask(__name__)
    app.config.update(SECRET_KEY=conf["SESSION_SECRET"], SESSION_COOKIE_NAME="__Host-reader",
                      SESSION_COOKIE_SECURE=True, SESSION_COOKIE_HTTPONLY=True,
                      SESSION_COOKIE_SAMESITE="Lax", MAX_CONTENT_LENGTH=8192)
    db = database if database is not None else MongoClient(
        conf["MONGODB_URI"], serverSelectionTimeoutMS=6000, tz_aware=True)["reader_" + env]
    for collection in (db.sessions, db.grants, db.pairs, db.limits):
        collection.create_index("expires", expireAfterSeconds=0)
    db.progress.create_index([("owner", 1), ("item", 1)], unique=True)
    db.pairs.create_index("secret", unique=True)
    def valid(collection, key):
        return collection.find_one({"_id": digest(key), "expires": {"$gt": now()}})
    def reader():
        row = valid(db.sessions, session.get("sid", ""))
        if not row:
            abort(401)
        return row["owner"]
    def principal(scope):
        auth = request.headers.get("Authorization", "")
        if auth:
            token = auth.removeprefix("Bearer ")
            grant = valid(db.grants, token) if auth.startswith("Bearer ") else None
            if not grant or scope not in grant["scopes"]:
                abort(403)
            return grant["owner"], grant["_id"]
        return reader(), "reader"
    @app.before_request
    def protect():
        if request.endpoint in {"pair", "redeem", "login"}:
            minute = int(now().timestamp()) // 60
            bucket = digest(f"{request.endpoint}:{request.remote_addr}:{minute}")
            hits = db.limits.find_one_and_update({"_id":bucket},
                {"$inc":{"count":1},"$setOnInsert":{"expires":now()+timedelta(minutes=2)}},
                upsert=True,return_document=True)
            if hits["count"] > 30:
                abort(429)
        if request.method in {"POST", "PUT", "DELETE"}:
            if request.endpoint in {"pair", "redeem"}:
                return
            if request.endpoint == "save_progress" and request.headers.get("Authorization"):
                return  # save_progress requires a scoped grant whenever this header is set.
            if request.headers.get("Origin") != origin:
                abort(403)
    @app.after_request
    def private(response):
        response.headers.update({"Cache-Control": "no-store", "Referrer-Policy": "no-referrer",
                                 "X-Content-Type-Options": "nosniff",
                                 "Content-Security-Policy": "default-src 'self'; frame-ancestors 'none'; form-action 'self'; base-uri 'none'"})
        return response
    @app.get("/login")
    def login():
        state, verifier = secrets.token_urlsafe(32), secrets.token_urlsafe(48)
        session["login"] = [state, verifier, int(now().timestamp())]
        challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).decode().rstrip("=")
        return redirect("https://github.com/login/oauth/authorize?" + urlencode({
            "client_id": conf["GITHUB_CLIENT_ID"], "redirect_uri": origin+"/callback",
            "state": state, "code_challenge": challenge, "code_challenge_method": "S256"}))
    @app.get("/callback")
    def callback():
        pending = session.pop("login", None)
        if not pending or not hmac.compare_digest(request.args.get("state",""), pending[0]) or now().timestamp()-pending[2]>600:
            abort(400)
        token = github_json("https://github.com/login/oauth/access_token", fields={
            "client_id": conf["GITHUB_CLIENT_ID"], "client_secret": conf["GITHUB_CLIENT_SECRET"],
            "redirect_uri": origin+"/callback", "code": request.args.get("code",""), "code_verifier": pending[1]}).get("access_token")
        if not token:
            abort(401)
        identity = github_json("https://api.github.com/user", token=token)
        owner = str(int(identity["id"]))
        next_pair = session.get("pair")
        session.clear()
        if next_pair:
            session["pair"] = next_pair
        sid = secrets.token_urlsafe(32)
        db.sessions.insert_one({"_id":digest(sid),"owner":owner,"expires":now()+timedelta(days=7)})
        session["sid"] = sid
        return redirect("/")
    @app.get("/")
    def home():
        if not valid(db.sessions, session.get("sid","")):
            return '<a href="/login">Sign in with GitHub to save your learning profile</a>'
        owner = reader()
        p = db.profiles.find_one({"_id":owner}) or {}
        pairing = valid(db.pairs, session.get("pair",""))
        return render_template_string("""<!doctype html><meta name="viewport" content="width=device-width, initial-scale=1"><h1>Your learning profile</h1>
        <form method="post" action="/profile">{% for key in fields %}<p><label>{{key|capitalize}} <input name="{{key}}" maxlength="240" value="{{p.get(key,'')}}"></label></p>{% endfor %}<button>Save profile</button></form>
        {% if pairing %}<h2>Connect an agent</h2><p>Approve only if you started this connection. Agent: {{pairing.name}}. Access: {{pairing.scopes|join(', ')}}.</p><form method="post" action="/approve"><button>Approve agent</button></form>{% endif %}
        <h2>Connected agents</h2>{% for g in grants %}<form method="post" action="/revoke/{{g._id}}">{{g.name}} · {{g.scopes|join(', ')}} <button>Revoke</button></form>{% endfor %}
        <p><a href="/api/progress">View saved progress</a></p><form method="post" action="/logout"><button>Sign out</button></form>""",
        fields=sorted(PROFILE_FIELDS),p=p,pairing=pairing,grants=db.grants.find({"owner":owner,"expires":{"$gt":now()}}))
    @app.post("/profile")
    def profile():
        owner = reader()
        if set(request.form)-PROFILE_FIELDS or any(len(v)>240 for v in request.form.values()):
            abort(400)
        db.profiles.update_one({"_id":owner},{"$set":{k:request.form.get(k,"") for k in PROFILE_FIELDS}},upsert=True)
        return redirect("/")
    @app.get("/api/profile")
    def get_profile():
        owner,_ = principal("profile:read")
        return jsonify(db.profiles.find_one({"_id":owner},{"_id":0}) or {})
    @app.get("/api/progress")
    def progress():
        owner,_ = principal("progress:read")
        return jsonify(list(db.progress.find({"owner":owner},{"owner":0,"actor":0,"_id":0})))
    @app.put("/api/progress")
    def save_progress():
        import re
        owner,actor = principal("progress:write")
        data = request.get_json()
        if not isinstance(data,dict) or set(data)!={"item","revision","position","completed"}:
            abort(400)
        item,rev,pos,done = (data[k] for k in ("item","revision","position","completed"))
        if not isinstance(item,str) or not re.fullmatch(r"[a-z0-9-]{1,40}/[a-z0-9-]{1,60}@[0-9a-f]{8}",item):
            abort(400)
        if type(rev)!=int or not 0<=rev<2**31 or type(pos) not in (float,int) or not 0<=pos<=86400 or type(done)!=bool:
            abort(400)
        try:
            result = db.progress.update_one({"owner":owner,"item":item,"revision":rev},
                {"$set":{"position":pos,"completed":done,"actor":actor},"$inc":{"revision":1}},upsert=rev==0)
        except DuplicateKeyError:
            abort(409)
        if not result.matched_count and result.upserted_id is None:
            abort(409)
        return jsonify(revision=rev+1)
    @app.post("/agent/pair")
    def pair():
        data = request.get_json()
        if not isinstance(data,dict):
            abort(400)
        scopes,name = data.get("scopes"),data.get("name")
        if not isinstance(name,str) or not 1<=len(name)<=60 or not isinstance(scopes,list) or not scopes or not all(isinstance(s,str) and s in SCOPES for s in scopes):
            abort(400)
        userkey,secret = secrets.token_urlsafe(24),secrets.token_urlsafe(32)
        db.pairs.insert_one({"_id":digest(userkey),"secret":digest(secret),"scopes":sorted(set(scopes)),
                             "name":name,"expires":now()+timedelta(minutes=5)})
        return jsonify(approval_url=origin+"/connect/"+userkey,device_secret=secret,expires_in=300)
    @app.get("/connect/<key>")
    def connect(key):
        if not valid(db.pairs,key): abort(404)
        session["pair"]=key
        return redirect("/")
    @app.post("/approve")
    def approve():
        owner=reader()
        key=session.pop("pair","")
        if not db.pairs.update_one({"_id":digest(key),"owner":{"$exists":False},"expires":{"$gt":now()}},{"$set":{"owner":owner}}).matched_count:
            abort(409)
        return redirect("/")
    @app.post("/agent/redeem")
    def redeem():
        data=request.get_json()
        secret=data.get("device_secret") if isinstance(data,dict) else None
        if not isinstance(secret,str) or len(secret)>100: abort(400)
        row=db.pairs.find_one_and_delete({"secret":digest(secret),"owner":{"$exists":True},"expires":{"$gt":now()}})
        if not row: abort(403)
        token=secrets.token_urlsafe(32)
        db.grants.insert_one({"_id":digest(token),"owner":row["owner"],"name":row["name"],"scopes":row["scopes"],"expires":now()+timedelta(days=7)})
        return jsonify(access_token=token,expires_in=604800)
    @app.post("/revoke/<key>")
    def revoke(key):
        db.grants.delete_one({"_id":key,"owner":reader()})
        return redirect("/")
    @app.post("/logout")
    def logout():
        db.sessions.delete_one({"_id":digest(session.get("sid",""))})
        session.clear()
        return redirect("/")
    return app
