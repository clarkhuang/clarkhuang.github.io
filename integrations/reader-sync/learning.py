"""Signed-in playback on the same origin as the account cookie and progress API."""
from urllib.parse import urlsplit

from flask import abort, redirect, render_template, request, session, url_for


def register_learning(app, db, catalog, env, valid_session):
    def public_url(url):
        if not url:
            return None
        parts = urlsplit(url)
        if parts.scheme != "https" or not parts.hostname or parts.username or parts.password:
            raise ValueError("Expected a public HTTPS catalog URL")
        if env == "staging" and not parts.path.startswith("/staging/"):
            return parts._replace(path="/staging" + parts.path).geturl()
        return url

    @app.get("/learn")
    def learn():
        key = request.args.get("item")
        if key is not None and key not in catalog:
            abort(404)
        account = valid_session()
        if not account:
            session["learn_item"] = key or ""
            return redirect(url_for("login"))
        owner = account["owner"]
        if key is None:
            progress = {r["item"]: r for r in db.progress.find({"owner": owner})}
            return render_template("learn.html", catalog=catalog, progress=progress)
        record = db.progress.find_one({"owner": owner, "item": key}) or {}
        entry = catalog[key]
        response = app.make_response(render_template(
            "learn.html", key=key, entry=entry, record=record,
            media_url=public_url(entry["url"]), page_url=public_url(entry["page"]),
            captions_url=public_url(entry.get("captions")),
        ))
        origins = sorted({
            "https://" + urlsplit(public_url(url)).netloc
            for url in (entry["url"], entry.get("captions")) if url
        })
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; frame-ancestors 'none'; form-action 'self'; base-uri 'none'; "
            "media-src 'self' " + " ".join(origins)
        )
        return response
