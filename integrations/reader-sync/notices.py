"""Per-reader release notices. Only notice receipts can read and dismiss them."""
import json
import re
import threading
import time
from datetime import datetime, timedelta
from urllib.error import URLError
from urllib.request import Request, urlopen

from flask import abort, jsonify, make_response, request
from pymongo import ReturnDocument


def release_history(feed_url):
    """Cache public Pages history per worker. A failed refresh never advances a cursor."""
    lock = threading.Lock()
    cached_until, retry_after, cached = 0.0, 0.0, []

    def load():
        nonlocal cached_until, retry_after, cached
        with lock:
            if time.monotonic() < cached_until:
                return cached
            if time.monotonic() < retry_after:
                abort(503, "Release history is temporarily unavailable.")
            try:
                with urlopen(Request(feed_url, headers={"Accept": "application/json"}), timeout=2) as res:
                    raw = res.read(2_000_001)
                if len(raw) > 2_000_000:
                    raise ValueError("history too large")
                doc = json.loads(raw)
                if doc["schema_version"] != 1 or not isinstance(doc["releases"], list):
                    raise ValueError("unsupported history")
                normalized = []
                for row in doc["releases"]:
                    when = datetime.fromisoformat(row["published_at"].replace("Z", "+00:00"))
                    if (when.utcoffset() is None or type(row["sequence"]) is not int or row["sequence"] < 1
                            or not re.fullmatch(r"[0-9a-f]{40}", row["sha"])
                            or not isinstance(row["summary"], str) or not row["summary"].strip()):
                        raise ValueError("invalid release")
                    normalized.append({k: row[k] for k in ("sequence", "published_at", "sha", "summary")})
                normalized.sort(key=lambda row: row["sequence"], reverse=True)
                if len({row["sequence"] for row in normalized}) != len(normalized):
                    raise ValueError("duplicate release sequence")
            except (URLError, OSError, ValueError, KeyError, TypeError, AttributeError):
                retry_after = time.monotonic() + 15
                abort(503, "Release history is temporarily unavailable.")
            cached, cached_until = normalized, time.monotonic() + 60
            return cached
    return load


def register_notices(app, db, pages_origin, env, now, notice_reader):
    prefix = "/staging" if env == "staging" else ""
    app.config["LOAD_RELEASE_HISTORY"] = release_history(pages_origin + prefix + "/change-log/history.json")

    def cors(response):
        response.headers["Access-Control-Allow-Origin"] = pages_origin
        response.vary.add("Origin")
        return response

    @app.route("/api/pages/changes/visit", methods=["POST", "OPTIONS"])
    @app.route("/api/pages/changes/dismiss", methods=["POST", "OPTIONS"])
    def pages_changes():
        if request.headers.get("Origin") != pages_origin:
            abort(403)
        if request.method == "OPTIONS":
            response = make_response("", 204)
            response.headers.update({"Access-Control-Allow-Headers": "Authorization, Content-Type",
                                     "Access-Control-Allow-Methods": "POST"})
            return cors(response)
        reader = notice_reader()
        if not reader:
            return cors(make_response(jsonify({}), 401))
        owner, instant = reader["owner"], now()
        releases = app.config["LOAD_RELEASE_HISTORY"]()
        state = db.reader_notices.find_one({"_id": owner})
        if not state or "dismissed_through" not in state:
            first_login = (state or {}).get("first_login_at", instant)
            baseline = max((r["sequence"] for r in releases
                            if datetime.fromisoformat(r["published_at"].replace("Z", "+00:00")) <= first_login),
                           default=0)
            db.reader_notices.update_one({"_id": owner}, {"$setOnInsert": {"first_login_at": first_login}}, upsert=True)
            db.reader_notices.update_one({"_id": owner, "dismissed_through": {"$exists": False}},
                                         {"$set": {"dismissed_through": baseline}})
            state = db.reader_notices.find_one({"_id": owner})
        if request.path.endswith("/dismiss"):
            data = request.get_json(silent=True)
            through = data.get("through") if isinstance(data, dict) else None
            if type(through) is not int or not 1 <= through <= state.get("presented_through", 0):
                return cors(make_response(jsonify(error="Unknown notice batch"), 400))
            # Older pages and concurrent devices can acknowledge only the batch they saw.
            state = db.reader_notices.find_one_and_update(
                {"_id": owner}, {"$max": {"dismissed_through": through}}, return_document=ReturnDocument.AFTER)
        unread = [r for r in releases if r["sequence"] > state["dismissed_through"]
                  and datetime.fromisoformat(r["published_at"].replace("Z", "+00:00")) > state["first_login_at"]]
        latest = unread[0]["sequence"] if unread else None
        update = {}
        if latest and latest > state.get("presented_through", 0):
            update["presented_through"] = latest
        if not state.get("last_visit_at") or instant - state["last_visit_at"] >= timedelta(minutes=5):
            update["last_visit_at"] = instant
        if update:
            db.reader_notices.update_one({"_id": owner}, {"$max": update})
        return cors(jsonify(count=len(unread), through=latest, releases=unread[:4]))
