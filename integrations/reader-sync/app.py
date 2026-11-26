"""Serve the signed-in reader on its own HTTPS origin alongside static Pages."""
import base64
import hashlib
import hmac
import json
import os
import secrets
from datetime import datetime, timedelta, timezone
from urllib.parse import urlencode, urlsplit
from urllib.error import URLError
from urllib.request import Request, urlopen

from catalog import load_catalog
from flask import Flask, abort, jsonify, redirect, render_template, request, session, url_for
from learning import register_learning
from pages_login import register_pages_login
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
    try:
        with urlopen(Request(url, data=urlencode(fields).encode() if fields else None,
                             headers=headers), timeout=10) as response:
            payload = json.load(response)
    except (URLError, TimeoutError, ValueError):
        abort(502, "GitHub sign-in is temporarily unavailable.")
    if not isinstance(payload, dict):
        abort(502)
    return payload

def create_app(config=None, database=None):
    conf = os.environ if config is None else config
    env = conf["READER_ENV"]
    if env not in {"staging", "production"}:
        raise ValueError("READER_ENV must be staging or production")
    origin = conf["READER_ORIGIN"].rstrip("/")
    if urlsplit(origin).scheme != "https" or urlsplit(origin).path:
        raise ValueError("READER_ORIGIN must be an HTTPS origin")
    catalog = load_catalog()
    app = Flask(__name__)
    app.config.update(SECRET_KEY=conf["SESSION_SECRET"], SESSION_COOKIE_NAME="__Host-reader",
                      SESSION_COOKIE_SECURE=True, SESSION_COOKIE_HTTPONLY=True,
                      SESSION_COOKIE_SAMESITE="Lax", MAX_CONTENT_LENGTH=8192)
    db = database if database is not None else MongoClient(
        conf["MONGODB_URI"], serverSelectionTimeoutMS=6000, tz_aware=True)["reader_" + env]
    for collection in (db.sessions, db.grants, db.limits):
        collection.create_index("expires", expireAfterSeconds=0)
    db.progress.create_index([("owner", 1), ("item", 1)], unique=True)
    db.grants.create_index("pair_id", unique=True, sparse=True)
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
            if not grant or grant.get("status", "issued") != "issued" or scope not in grant["scopes"]:
                abort(403)
            return grant["owner"], grant["_id"]
        return reader(), "reader"
    @app.before_request
    def protect():
        if request.endpoint in {"pair", "redeem", "login", "pages_login"}:
            minute = int(now().timestamp()) // 60
            bucket = digest(f"{request.endpoint}:{request.remote_addr}:{minute}")
            hits = db.limits.find_one_and_update({"_id":bucket},
                {"$inc":{"count":1},"$setOnInsert":{"expires":now()+timedelta(minutes=2)}},
                upsert=True,return_document=True)
            if hits["count"] > 30:
                abort(429)
        if request.method in {"POST", "PUT", "DELETE"}:
            if request.endpoint in {"pair", "redeem", "pages_login"}:
                return
            if request.endpoint == "save_progress" and request.headers.get("Authorization"):
                return  # save_progress requires a scoped grant whenever this header is set.
            if request.headers.get("Origin") != origin:
                abort(403)
    @app.after_request
    def private(response):
        response.headers.setdefault("Content-Security-Policy", "default-src 'self'; frame-ancestors 'none'; form-action 'self'; base-uri 'none'")
        response.headers.update({"Cache-Control": "no-store", "Referrer-Policy": "no-referrer",
                                 "X-Content-Type-Options": "nosniff"})
        return response
    @app.get("/.well-known/reader-sync.json")
    def discovery():
        return jsonify(version=1, environment=env, catalog="/api/catalog",
                       pair={"method": "POST", "path": "/agent/pair", "fields": ["name", "scopes"]},
                       redeem={"method": "POST", "path": "/agent/redeem", "fields": ["device_secret"]},
                       scopes=sorted(SCOPES), profile="/api/profile", progress="/api/progress",
                       instructions="Show the approval URL and comparison code to the reader. "
                                    "Keep the device secret private. Use the issued bearer for the approved scopes.")

    @app.get("/api/catalog")
    def media_keys():
        return jsonify({key: {"title": item["title"], "duration": item["duration"], "kind": item["kind"]}
                        for key, item in catalog.items()})

    @app.get("/healthz")
    def health():
        db.command("ping")
        return "", 204

    def github_authorize(state, verifier):
        challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).decode().rstrip("=")
        return redirect("https://github.com/login/oauth/authorize?" + urlencode({
            "client_id": conf["GITHUB_CLIENT_ID"], "redirect_uri": origin+"/callback",
            "scope": "", "state": state, "code_challenge": challenge, "code_challenge_method": "S256"}))
    def github_identity(verifier):
        credentials = github_json("https://github.com/login/oauth/access_token", fields={
            "client_id": conf["GITHUB_CLIENT_ID"], "client_secret": conf["GITHUB_CLIENT_SECRET"],
            "redirect_uri": origin+"/callback", "code": request.args.get("code",""), "code_verifier": verifier})
        if credentials.get("scope", ""):
            abort(403, "This reader only accepts public identity access.")
        token = credentials.get("access_token")
        if not token:
            abort(401)
        identity = github_json("https://api.github.com/user", token=token)
        if type(identity.get("id")) is not int or identity["id"] <= 0:
            abort(502)
        return identity

    def establish_session(identity):
        # Rotate the browser session. Existing Pages receipts must follow logout/account changes.
        if session.get("sid"):
            db.sessions.delete_one({"_id": digest(session["sid"])})
        session.clear()
        sid = secrets.token_urlsafe(32)
        row = {"_id": digest(sid), "owner": str(identity["id"]), "login": identity.get("login"),
               "expires": now() + timedelta(days=7)}
        db.sessions.insert_one(row)
        session["sid"] = sid
        return row

    pages_callback = register_pages_login(
        app, db, conf.get("PAGES_ORIGIN", "https://clarkhuang.github.io"), env, now,
        lambda: valid(db.sessions, session.get("sid", "")), github_authorize,
        github_identity, establish_session)

    @app.get("/login")
    def login():
        state, verifier = secrets.token_urlsafe(32), secrets.token_urlsafe(48)
        session["login"] = [state, verifier, int(now().timestamp())]
        return github_authorize(state, verifier)
    @app.get("/callback")
    def callback():
        state = request.args.get("state", "")
        if state.startswith("pages."):
            return pages_callback(state)
        pending = session.pop("login", None)
        if not pending or not hmac.compare_digest(request.args.get("state", "").encode(), pending[0].encode()) or now().timestamp()-pending[2]>600:
            abort(400)
        identity = github_identity(pending[1])
        next_item = session.get("learn_item")
        next_pair = session.get("pair")
        establish_session(identity)
        if next_pair:
            session["pair"] = next_pair
        if next_item is not None and not next_pair:
            return redirect(url_for("learn", item=next_item or None))
        return redirect("/")
    @app.get("/")
    def home():
        if not valid(db.sessions, session.get("sid","")):
            return render_template("profile.html", signed_in=False)
        owner = reader()
        p = db.profiles.find_one({"_id":owner}) or {}
        pair_key = session.get("pair", "")
        pairing = db.grants.find_one({"pair_id": digest(pair_key), "status": "pending", "expires": {"$gt": now()}})
        return render_template("profile.html", signed_in=True,
        fields=sorted(PROFILE_FIELDS),p=p,pairing=pairing,pair_key=pair_key,grants=db.grants.find({"owner":owner,"expires":{"$gt":now()}}))
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
        owner,actor = principal("progress:write")
        data = request.get_json()
        if not isinstance(data,dict) or set(data)!={"item","revision","position","completed"}:
            abort(400)
        item,rev,pos,done = (data[k] for k in ("item","revision","position","completed"))
        media = catalog.get(item) if isinstance(item, str) else None
        if media is None:
            abort(400)
        if type(rev) != int or not 0 <= rev < 2**31 or type(done) != bool:
            abort(400)
        if type(pos) not in (float, int) or not 0 <= pos <= media["duration"]:
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
        pair_key = secrets.token_urlsafe(24)
        device_secret = secrets.token_urlsafe(32)
        user_code = secrets.token_hex(4).upper()
        user_code = user_code[:4] + "-" + user_code[4:]
        expires = now() + timedelta(minutes=5)
        db.grants.insert_one({
            "_id": digest(agent_token(device_secret)), "pair_id": digest(pair_key),
            "scopes": sorted(set(scopes)), "name": name, "user_code": user_code,
            "status": "pending", "expires": expires, "pair_until": expires,
        })
        return jsonify(approval_url=origin + "/connect/" + pair_key, user_code=user_code,
                       device_secret=device_secret, expires_in=300)

    def agent_token(device_secret):
        # Reproduce the same credential for a retry without storing it in the database.
        return hmac.new(app.secret_key.encode(), b"reader-agent-v1:" + device_secret.encode(),
                        hashlib.sha256).hexdigest()

    @app.get("/connect/<key>")
    def connect(key):
        if not db.grants.find_one({"pair_id": digest(key), "status": "pending", "expires": {"$gt": now()}}):
            abort(404)
        session["pair"] = key
        return redirect("/")

    @app.post("/approve")
    def approve():
        owner = reader()
        key = request.form.get("pair_key", "")
        # A stale tab must never authorize a different agent or a different request.
        if not key or key != session.get("pair"):
            abort(409)
        result = db.grants.update_one(
            {"pair_id": digest(key), "status": "pending", "expires": {"$gt": now()}},
            {"$set": {"owner": owner, "status": "approved"}},
        )
        if not result.matched_count:
            abort(409)
        session.pop("pair", None)
        return redirect("/")

    @app.post("/agent/redeem")
    def redeem():
        data = request.get_json()
        secret = data.get("device_secret") if isinstance(data, dict) else None
        if not isinstance(secret, str) or not 1 <= len(secret) <= 100:
            abort(400)
        token = agent_token(secret)
        instant = now()
        grant_id = digest(token)
        db.grants.update_one(
            {"_id": grant_id, "status": "approved", "pair_until": {"$gt": instant}},
            {"$set": {"status": "issued", "expires": instant + timedelta(days=7)}},
        )
        # Repeated calls during the original pairing window return the issued grant.
        # Revocation deletes this same document, so a retry cannot resurrect a grant.
        row = db.grants.find_one({"_id": grant_id, "status": "issued",
                                  "pair_until": {"$gt": instant}, "expires": {"$gt": instant}})
        if not row:
            abort(403)
        return jsonify(access_token=token, expires_in=int((row["expires"] - instant).total_seconds()))
    @app.post("/revoke/<key>")
    def revoke(key):
        db.grants.delete_one({"_id":key,"owner":reader()})
        return redirect("/")
    @app.post("/logout")
    def logout():
        db.sessions.delete_one({"_id":digest(session.get("sid",""))})
        session.clear()
        return redirect("/")
    register_learning(app, db, catalog, env, lambda: valid(db.sessions, session.get("sid", "")))
    return app
