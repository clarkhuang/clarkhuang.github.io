"""Signed-in playback on the same origin as the account cookie and progress API."""
from urllib.parse import urlsplit

from flask import abort, redirect, render_template, request, session, url_for


def learning_sections(catalog):
    """Preserve the published series and reading order while grouping a work's formats."""
    sections = {}
    for media_key, entry in catalog.items():
        section = sections.setdefault(entry["series_id"], {"title": entry["series_title"], "works": {}})
        work = section["works"].setdefault(entry["content_id"], {"title": entry["title"], "formats": []})
        work["formats"].append((media_key, entry["kind"]))
    return sections.values()


def register_learning(app, db, catalog, env, pages_origin, valid_session):
    sections = learning_sections(catalog)

    def pages_url(page):
        path = urlsplit(page).path or "/"
        if path.startswith("/staging/"):
            path = path.removeprefix("/staging")
        prefix = "/staging" if env == "staging" else ""
        return pages_origin + prefix + path

    app.jinja_env.globals["pages_url"] = pages_url

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
            return render_template("learn.html", sections=sections, progress=progress)
        record = db.progress.find_one({"owner": owner, "item": key}) or {}
        entry = catalog[key]
        response = app.make_response(render_template(
            "learn.html", key=key, entry=entry, record=record,
            media_url=public_url(entry["url"]), page_url=pages_url(entry["page"]),
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
