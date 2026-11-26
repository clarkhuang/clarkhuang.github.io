"""Top-level Pages sign-in and its read-only, per-tab identity receipt."""
import hashlib
import re
import secrets
from datetime import timedelta
from urllib.parse import urlsplit

from flask import abort, jsonify, make_response, redirect, request, url_for
from pymongo.errors import DuplicateKeyError


def register_pages_login(app, db, pages_origin, env, now, current_session, authorize,
                         github_identity, establish_session):
    origin = urlsplit(pages_origin)
    if (origin.scheme != "https" or not origin.hostname or origin.username or origin.password
            or origin.path or origin.query or origin.fragment or pages_origin != origin.geturl()):
        raise ValueError("PAGES_ORIGIN must be an HTTPS origin without a path")

    receipts = db.pages_logins
    receipts.create_index("expires", expireAfterSeconds=0)

    def sha(value):
        return hashlib.sha256(value.encode("ascii")).hexdigest()

    def cookie_name(challenge):
        return "__Host-pages-" + challenge

    def validate_path(page):
        # Only canonical Pages paths are accepted. Queries and fragments stay in the tab.
        if (not page or len(page) > 512 or not re.fullmatch(r"/[A-Za-z0-9_./-]*", page)
                or "//" in page or any(s in {".", ".."} for s in page.split("/"))
                or not (page.endswith("/") or page.endswith(".html"))):
            abort(400)
        if (env == "staging") != page.startswith("/staging/"):
            abort(400)
        return page

    @app.post("/pages/login")
    def pages_login():
        if request.headers.get("Origin") != pages_origin:
            abort(403)
        page = validate_path(request.form.get("page", ""))
        challenge = request.form.get("challenge", "")
        if not re.fullmatch(r"[0-9a-f]{64}", challenge):
            abort(400)
        binding = secrets.token_urlsafe(32)
        try:
            receipts.insert_one({"_id": challenge, "binding": sha(binding), "page": page,
                                 "expires": now() + timedelta(minutes=10), "status": "pending",
                                 "pkce": secrets.token_urlsafe(48)})
        except DuplicateKeyError:
            abort(409)
        response = redirect(url_for("continue_pages", challenge=challenge), code=303)
        response.set_cookie(cookie_name(challenge), binding, max_age=600, secure=True,
                            httponly=True, samesite="Lax", path="/")
        return response

    def pending(challenge):
        if not re.fullmatch(r"[0-9a-f]{64}", challenge):
            abort(400)
        binding = request.cookies.get(cookie_name(challenge), "")
        if not re.fullmatch(r"[A-Za-z0-9_-]{43}", binding):
            abort(400)
        row = receipts.find_one({"_id": challenge, "binding": sha(binding), "status": "pending",
                                 "expires": {"$gt": now()}})
        if not row:
            abort(400)
        return row

    def return_to_page(row):
        response = redirect(pages_origin + row["page"], code=303)
        response.delete_cookie(cookie_name(row["_id"]), secure=True, httponly=True, samesite="Lax")
        return response

    def finish(row, reader):
        result = receipts.update_one(
            {"_id": row["_id"], "status": "pending", "binding": row["binding"], "expires": {"$gt": now()}},
            {"$set": {"status": "issued", "session_id": reader["_id"], "expires": reader["expires"]},
             "$unset": {"pkce": "", "binding": "", "page": ""}})
        if not result.matched_count:
            abort(400)
        return return_to_page(row)

    @app.get("/pages/continue/<challenge>")
    def continue_pages(challenge):
        row = pending(challenge)
        reader = current_session()
        if reader and reader.get("login"):
            return finish(row, reader)
        return authorize("pages." + challenge, row["pkce"])

    def handle_callback(state):
        row = pending(state.removeprefix("pages."))
        if request.args.get("error") == "access_denied":
            receipts.delete_one({"_id": row["_id"], "status": "pending", "binding": row["binding"]})
            return return_to_page(row)
        identity = github_identity(row["pkce"])
        if not identity.get("login") or not isinstance(identity["login"], str):
            abort(502)
        return finish(row, establish_session(identity))

    @app.route("/api/pages/identity", methods=["GET", "OPTIONS"])
    def pages_identity():
        if request.headers.get("Origin") != pages_origin:
            abort(403)
        if request.method == "OPTIONS":
            response = make_response("", 204)
            response.headers.update({"Access-Control-Allow-Headers": "Authorization",
                                     "Access-Control-Allow-Methods": "GET"})
        else:
            match = re.fullmatch(r"Bearer ([a-f0-9]{64})", request.headers.get("Authorization", ""))
            receipt = receipts.find_one({"_id": sha(match[1]), "status": "issued",
                                         "expires": {"$gt": now()}}) if match else None
            reader = db.sessions.find_one({"_id": receipt["session_id"],
                                           "expires": {"$gt": now()}}) if receipt else None
            response = jsonify({"login": reader["login"]} if reader else {})
            response.status_code = 200 if reader else 401
        response.headers["Access-Control-Allow-Origin"] = pages_origin
        response.vary.add("Origin")
        return response

    return handle_callback
