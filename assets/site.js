/* Clark Huang — learning site. Progressive enhancement only: every video and audio works without it.
   Guest progress lives in first-party cookies. Optional account sign-in stores separate display-only and release-notice receipts. Guest cookies:
     watched  = "ai-tips/01@1a2b3c4d,se101/02@9f8e7d6c"         lessons played to ~90% or to the end, or marked by hand
     vpos     = "ai-tips/02@1a2b3c4d:73.4,se101/01@0a1b2c3d:12.0" video resume positions in seconds (newest last, max 20)
     book_pos = "preview@4226615c:31.2"                           audiobook/videobook bookmarks in seconds
     last_visit = "<unix seconds>"                               start of the most recent visit (persistent)
     visit_ref  = "<unix seconds>|first"                         session cookie: frozen cutoff for New tags
   Every key is "<id>@<version>". The version is the first 8 hex chars of the SHA-256 of the media file, stamped
   into the HTML as data-video-version (data-video-versions on a data-progress meter, same order as its ids) by
   sitegen/stamp_versions.py. A re-rendered video gets a new version, so it shows as unwatched and does not offer
   a stale resume position. Keys with no "@version" (older cookies) are always stale; keys whose version differs
   from one this page knows for that id are stale too. Stale keys are pruned on page load and on every write.
   Keys for ids this page does not show are kept until a page that knows them loads.
   A first visit (no last_visit) shows no New tags. visit_ref keeps the previous visit's cutoff for the whole browsing session so tags do not vanish on the next page. Cookie names "watched", "vpos" and "book_pos" are unchanged from earlier versions of the site. */
(function () {
  "use strict";
  var doc = document;
  doc.documentElement.classList.add("js");

  var YEAR = 31536000, C_WATCHED = "watched", C_VPOS = "vpos", C_BOOK = "book_pos", C_LAST = "last_visit", C_REF = "visit_ref", VPOS_MAX = 20;

  // Read the public service origins beside this script. Keep playing locally unless
  // the learner follows a sign-in link to the configured service in a top-level tab.
  var script = doc.currentScript;
  if (script && script.src && window.fetch) {
    var nav = doc.querySelector('nav[aria-label="Primary"]');
    if (nav) {
      [["About", "about/"]].forEach(function (entry) {
        var url = new URL("../" + entry[1], script.src);
        if (Array.from(nav.links || nav.querySelectorAll("a")).some(function (a) { return a.href === url.href; })) return;
        var link = doc.createElement("a");
        link.href = url.href;
        link.textContent = entry[0];
        if (location.pathname === url.pathname) link.setAttribute("aria-current", "page");
        nav.appendChild(link);
      });
    }
    var endpoints = new URL("reader-endpoints.json", script.src);
    fetch(endpoints, {credentials: "omit"}).then(function (response) {
      if (!response.ok) throw new Error("Reader configuration unavailable");
      return response.json();
    }).then(function (config) {
      var staging = location.pathname.indexOf("/staging/") === 0;
      var address = config[staging ? "staging" : "production"];
      if (!address || config.staging === config.production) return;
      var service = new URL(address);
      if (service.protocol !== "https:" || service.origin !== address) return;
      scheduleReaderWarmup(service, config.pagesHost, staging);
      function addLink(parent, item, label) {
        var target = new URL("/learn", service);
        if (item) target.searchParams.set("item", item);
        var link = doc.createElement("a");
        link.href = target.href;
        link.textContent = label;
        parent.appendChild(link);
        return link;
      }
      if (nav) {
        var account = addLink(nav, "", "Sign in with GitHub");
        account.className = "reader-sign-in";
        setupReaderAccount(account, service);
      }
      doc.querySelectorAll("video[data-lesson-id],video[data-chapter],audio[data-chapter]").forEach(function (media) {
        var key = vkey(media.dataset.lessonId || media.dataset.chapter, ver(media));
        if (!key) return;
        var paragraph = doc.createElement("p");
        var container = media.closest(".player") || media;
        container.parentNode.insertBefore(paragraph, container.nextSibling);
        addLink(paragraph, key, media.tagName === "AUDIO" ? "Listen with account sync" : "Watch with account sync");
      });
    }).catch(function () { /* Guest playback works independently of account sync. */ });
  }

  function scheduleReaderWarmup(service, pagesHost, staging) {
    // Copies and previews must opt in using their own published host and service origins.
    var canonical = doc.querySelector('link[rel="canonical"]');
    var scriptURL = new URL(script.src);
    if (location.protocol !== "https:" || location.host !== pagesHost ||
        scriptURL.origin !== location.origin || scriptURL.pathname !== (staging ? "/staging" : "") + "/assets/site.js" ||
        !canonical || canonical.href !== location.origin + location.pathname.replace(/index\.html$/, "")) return;

    function warm() {
      if (doc.visibilityState !== "visible" || navigator.onLine === false ||
          navigator.globalPrivacyControl === true || navigator.doNotTrack === "1" ||
          (navigator.connection && navigator.connection.saveData)) return;
      var key = "reader.warm." + service.origin;
      var identity = "reader.identity." + service.origin;
      try {
        // Returning or signing-in readers already contact the service to check their session.
        if (window.localStorage.getItem(identity) || window.sessionStorage.getItem(identity) ||
            window.sessionStorage.getItem(identity + ".pending")) return;
        var last = Number(window.localStorage.getItem(key));
        var now = Date.now();
        if (last > 0 && now >= last && now - last < 15 * 60 * 1000) return;
        window.localStorage.setItem(key, String(now));
      } catch (_) { return; }
      fetch(new URL("/healthz", service), {mode: "no-cors", credentials: "omit",
        referrerPolicy: "no-referrer", cache: "no-store", redirect: "error"}).catch(function () {});
    }
    if (doc.readyState === "complete") warm();
    else window.addEventListener("load", warm, {once: true});
  }

  function setupReaderAccount(link, service) {
    // A receipt can only ask for the GitHub handle attached to a live reader session.
    // The reader session cookie and GitHub credentials stay on the top-level reader origin.
    var key = "reader.identity." + service.origin;
    var pending;
    var confirmed;
    try {
      pending = window.sessionStorage;
      pending.getItem(key);
      // Shared across ordinary tabs, falling back to this tab when storage is restricted.
      try {
        confirmed = window.localStorage;
        confirmed.setItem(key + ".probe", "1");
        confirmed.removeItem(key + ".probe");
      } catch (_) { confirmed = pending; }
      if (!window.crypto || !window.crypto.subtle || !window.TextEncoder) return;
    } catch (_) { return; }
    // Restore search/filter and chapter-anchor state locally. The reader receives just the path.
    var savedView = pending.getItem(key + ".view");
    if (savedView) {
      pending.removeItem(key + ".view");
      try {
        var original = new URL(savedView, location.origin);
        if (original.origin === location.origin && original.pathname === location.pathname &&
            (original.search || original.hash) && !location.search && !location.hash) {
          location.replace(original.href);
          return;
        }
      } catch (_) { /* An invalid saved view still leaves the learner on the requested page. */ }
    }
    var signedIn = false;
    var busy = false;
    var generation = 0;
    function hex(bytes) {
      return Array.from(bytes, function (n) { return n.toString(16).padStart(2, "0"); }).join("");
    }
    var noticeBox = null;
    var activeNoticeToken = null;
    var noticeRevision = 0;
    var upgrade = null;
    function clearNotices() {
      ++noticeRevision;
      activeNoticeToken = null;
      if (noticeBox) { noticeBox.remove(); noticeBox = null; }
    }
    function drawNotices(result, token) {
      if (noticeBox) { noticeBox.remove(); noticeBox = null; }
      if (!result.count || !result.releases || !result.releases.length) return;
      var main = doc.querySelector("main");
      if (!main) return;
      var base = location.pathname.indexOf("/staging/") === 0 ? "/staging" : "";
      noticeBox = doc.createElement("aside");
      noticeBox.className = "reader-changes";
      noticeBox.setAttribute("aria-labelledby", "reader-changes-heading");
      var heading = doc.createElement("h2");
      heading.id = "reader-changes-heading";
      heading.textContent = "What’s changed since your last login";
      var list = doc.createElement("ul");
      result.releases.forEach(function (entry) {
        if (!/^[a-f0-9]{40}$/.test(entry.sha)) return;
        var li = doc.createElement("li");
        var anchor = doc.createElement("a");
        anchor.href = base + "/change-log/archive/#release-" + entry.sha;
        anchor.textContent = entry.summary;
        li.appendChild(anchor);
        list.appendChild(li);
      });
      var archive = doc.createElement("a");
      archive.href = base + "/change-log/";
      archive.textContent = "View full change log";
      var button = doc.createElement("button");
      button.type = "button";
      button.textContent = "Dismiss " + (result.count === 1 ? "this update" : "these " + result.count + " updates");
      var status = doc.createElement("p");
      status.setAttribute("role", "status");
      button.addEventListener("click", function () {
        if (token !== activeNoticeToken) return;
        button.disabled = true;
        var thisVisit = ++noticeRevision;
        fetch(new URL("/api/pages/changes/dismiss", service), {
          method: "POST", credentials: "omit", cache: "no-store", referrerPolicy: "no-referrer",
          headers: {Authorization: "Bearer " + token, "Content-Type": "application/json"},
          body: JSON.stringify({through: result.through})
        }).then(function (res) {
          if (!res.ok) throw new Error();
          return res.json();
        }).then(function (next) {
          if (thisVisit !== noticeRevision) return;
          drawNotices(next, token);
          confirmed.setItem(key + ".dismissed", String(Date.now()));
        }).catch(function () {
          if (thisVisit !== noticeRevision) return;
          button.disabled = false;
          status.textContent = "Couldn’t save the dismissal. Please try again.";
        });
      });
      noticeBox.append(heading, list, archive, button, status);
      var container = main.querySelector(".wrap") || main;
      container.prepend(noticeBox);
    }
    function loadNotices(token) {
      if (token !== activeNoticeToken) clearNotices();
      activeNoticeToken = token;
      var current = ++noticeRevision;
      fetch(new URL("/api/pages/changes/visit", service), {
        method: "POST", credentials: "omit", cache: "no-store", referrerPolicy: "no-referrer",
        headers: {Authorization: "Bearer " + token}
      }).then(function (res) {
        if (!res.ok) throw new Error();
        return res.json();
      }).then(function (data) {
        if (current === noticeRevision) drawNotices(data, token);
      }).catch(function () { /* An unavailable feed leaves ordinary course navigation usable. */ });
    }
    function show(login, verifier) {
      signedIn = Boolean(login);
      link.textContent = signedIn ? "@" + login : "Sign in with GitHub";
      link.href = new URL(signedIn ? "/" : "/learn", service).href;
      if (signedIn) {
        var prefix = doc.createElement("span");
        prefix.className = "reader-signed-prefix";
        prefix.textContent = "Signed in as ";
        link.prepend(prefix);
        link.setAttribute("aria-label", "Signed in as @" + login + ". Open learning profile");
      } else link.removeAttribute("aria-label");
      if (upgrade) { upgrade.remove(); upgrade = null; }
      var notice;
      try { notice = JSON.parse(confirmed.getItem(key + ".notices")); } catch (_) {}
      if (login && notice && notice.identity === verifier) {
        loadNotices(notice.proof);
      } else {
        clearNotices();
        if (login) {
          // A previously issued display-only credential remains display-only.
          upgrade = doc.createElement("a");
          upgrade.href = link.href;
          upgrade.textContent = "Enable update notices";
          upgrade.addEventListener("click", startLogin);
          link.parentNode.appendChild(upgrade);
        }
      }
    }
    function refresh() {
      var revision = ++generation;
      var candidate = pending.getItem(key + ".pending");
      var verifier = candidate || confirmed.getItem(key);
      if (!verifier) { show(null); return; }
      fetch(new URL("/api/pages/identity", service), {
        headers: {Authorization: "Bearer " + verifier},
        credentials: "omit", cache: "no-store", referrerPolicy: "no-referrer"
      }).then(function (response) {
        if (revision !== generation) return;
        if (response.status === 401 || response.status === 403) {
          if (candidate) {
            if (pending.getItem(key + ".pending") === candidate) {
              pending.removeItem(key + ".pending");
              pending.removeItem(key + ".notice-pending");
            }
            refresh();
          } else {
            if (confirmed.getItem(key) === verifier) {
              confirmed.removeItem(key);
              confirmed.removeItem(key + ".notices");
            }
            show(null);
          }
        } else if (response.ok) {
          return response.json().then(function (data) {
            if (revision !== generation) return;
            if (candidate && typeof data.login === "string" && data.login) {
              var noticeProof = pending.getItem(key + ".notice-pending");
              if (noticeProof) {
                confirmed.setItem(key + ".notices", JSON.stringify({identity: verifier, proof: noticeProof}));
                pending.removeItem(key + ".notice-pending");
              }
              confirmed.setItem(key, verifier);
              pending.removeItem(key + ".pending");
            }
            show(typeof data.login === "string" && data.login, verifier);
          });
        } else show(null);
      }).catch(function () { if (revision === generation) show(null); });
    }
    function startLogin(event) {
      if ((signedIn && event.currentTarget === link) || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
      event.preventDefault();
      if (busy) return;
      busy = true;
      ++generation;
      var verifier = hex(window.crypto.getRandomValues(new Uint8Array(32)));
      var noticeProof = hex(window.crypto.getRandomValues(new Uint8Array(32)));
      Promise.all([verifier, noticeProof].map(function (proof) {
        return window.crypto.subtle.digest("SHA-256", new TextEncoder().encode(proof));
      })).then(function (hashes) {
        pending.setItem(key + ".notice-pending", noticeProof);
        pending.setItem(key + ".pending", verifier);
        pending.setItem(key + ".view", location.pathname + location.search + location.hash);
        var form = doc.createElement("form");
        form.method = "post";
        form.action = new URL("/pages/login", service).href;
        var fields = {page: location.pathname, challenge: hex(new Uint8Array(hashes[0])),
                      notice_challenge: hex(new Uint8Array(hashes[1]))};
        Object.keys(fields).forEach(function (name) {
          var input = doc.createElement("input");
          input.type = "hidden";
          input.name = name;
          input.value = fields[name];
          form.appendChild(input);
        });
        doc.body.appendChild(form);
        form.submit();
      }).catch(function () { location.assign(link.href); });
    }
    link.addEventListener("click", startLogin);
    refresh();
    window.addEventListener("pageshow", function (event) {
      busy = false;
      if (event.persisted) refresh();
    });
    window.addEventListener("storage", function (event) {
      if (event.key === key || event.key === key + ".dismissed" || event.key === null) refresh();
    });
    doc.addEventListener("visibilitychange", function () {
      if (doc.visibilityState === "visible") refresh();
    });
  }

  /* ---------- cookies */
  function getCookie(name) {
    var parts = doc.cookie ? doc.cookie.split("; ") : [];
    for (var i = 0; i < parts.length; i++) {
      var eq = parts[i].indexOf("=");
      if (parts[i].slice(0, eq) === name) {
        try { return decodeURIComponent(parts[i].slice(eq + 1)); } catch (e) { return ""; }
      }
    }
    return "";
  }
  function setCookie(name, value, maxAge) {
    var parts = name + "=" + encodeURIComponent(value) + "; path=/; SameSite=Lax";
    if (maxAge !== false) parts += "; max-age=" + (maxAge == null ? YEAR : maxAge);
    if (location.protocol === "https:") parts += "; Secure";
    doc.cookie = parts;
  }
  function clearCookie(name) { setCookie(name, "", 0); }
  function $$(sel, ctx) { return Array.prototype.slice.call((ctx || doc).querySelectorAll(sel)); }

  /* ---------- media versions: every cookie key is "<id>@<version>" */
  var KNOWN = {};                            // id -> { version: 1 } for media this page shows
  function ver(el) { return el.getAttribute("data-video-version") || ""; }
  function vkey(id, v) { return id && v ? id + "@" + v : ""; }
  function known(id, v) { if (id && v) (KNOWN[id] = KNOWN[id] || {})[v] = 1; }
  $$("[data-video-version]").forEach(function (el) {
    ["data-lesson-id", "data-chapter", "data-watch-id", "data-toggle-watched", "data-lesson-link"].forEach(function (a) {
      if (el.hasAttribute(a)) known(el.getAttribute(a), ver(el));
    });
  });
  $$("[data-progress][data-video-versions]").forEach(function (el) {
    var vs = el.getAttribute("data-video-versions").split(",");
    el.getAttribute("data-progress").split(",").forEach(function (id, i) { known(id, vs[i]); });
  });
  // Unversioned keys are stale; so is a version that differs from every version this page knows for that id.
  function fresh(key) {
    var at = key.lastIndexOf("@");
    if (at < 1 || at === key.length - 1) return false;
    var k = KNOWN[key.slice(0, at)];
    return !k || !!k[key.slice(at + 1)];
  }
  function idOf(key) { return key.slice(0, key.lastIndexOf("@")); }

  // "key:seconds" pairs; keys keep their order so the oldest can be dropped first. Stale keys are skipped.
  function readMap(name) {
    var map = {}, raw = getCookie(name);
    if (raw) raw.split(",").forEach(function (part) {
      var i = part.lastIndexOf(":"), v = parseFloat(part.slice(i + 1)), k = part.slice(0, i);
      if (i > 0 && isFinite(v) && fresh(k)) map[k] = v;
    });
    return map;
  }
  function writeMap(name, map, max) {
    var keys = Object.keys(map).filter(function (k) { return map[k] > 0; });
    if (max && keys.length > max) keys = keys.slice(keys.length - max);
    if (keys.length) setCookie(name, keys.map(function (k) { return k + ":" + map[k].toFixed(1); }).join(","));
    else clearCookie(name);
  }

  function fmt(s) { s = Math.max(0, Math.floor(s)); return Math.floor(s / 60) + ":" + ("0" + (s % 60)).slice(-2); }
  function play(m) { var p = m.play(); if (p && p.catch) p.catch(function () {}); }
  function say(near, msg) {
    var scope = near.closest("[data-status-scope]") || doc, s = scope.querySelector("[data-status]");
    if (s) { s.textContent = ""; setTimeout(function () { s.textContent = msg; }, 30); }
  }

  /* ---------- watched lessons (keys are "<id>@<version>") */
  function watched() { return getCookie(C_WATCHED).split(",").filter(Boolean).filter(fresh); }
  function writeWatched(w) { if (w.length) setCookie(C_WATCHED, w.join(",")); else clearCookie(C_WATCHED); }
  function isWatched(key) { return !!key && watched().indexOf(key) !== -1; }
  function setWatched(key, on) {
    if (!key) return;
    var id = idOf(key), w = watched().filter(function (k) { return idOf(k) !== id; });   // one version per id
    if (on) w.push(key);
    writeWatched(w);
    paint();
  }
  // Prune stale keys (unversioned, or an old version of media this page shows) as soon as the page loads.
  (function prune() {
    var raw = getCookie(C_WATCHED).split(",").filter(Boolean), w = watched();
    if (w.length !== raw.length) writeWatched(w);
    [[C_VPOS, VPOS_MAX], [C_BOOK, 0]].forEach(function (c) {
      var map = readMap(c[0]), rawMap = getCookie(c[0]).split(",").filter(Boolean);
      if (Object.keys(map).length !== rawMap.length) writeMap(c[0], map, c[1]);
    });
  })();
  function visitCutoff() {
    var ref = getCookie(C_REF);
    if (!ref) {
      var prev = getCookie(C_LAST);
      ref = prev || "first";
      setCookie(C_REF, ref, false);          // session cookie: stays for this browsing session only
      setCookie(C_LAST, String(Math.floor(Date.now() / 1000)));
    }
    if (ref === "first") return null;
    var n = parseInt(ref, 10);
    return isFinite(n) ? n * 1000 : null;
  }
  function paintNew() {
    var cut = visitCutoff();
    $$("[data-new]").forEach(function (el) {
      var host = el.closest("[data-new-at]") || el;
      var at = Date.parse(host.getAttribute("data-new-at") || "");
      el.hidden = !(cut != null && isFinite(at) && at > cut);
    });
  }
  function paint() {
    var w = watched();

    function has(id, v) { var k = vkey(id, v); return !!k && w.indexOf(k) !== -1; }
    $$("[data-watch-id]").forEach(function (el) { el.classList.toggle("is-watched", has(el.getAttribute("data-watch-id"), ver(el))); });
    $$("[data-toggle-watched]").forEach(function (b) {
      var on = has(b.getAttribute("data-toggle-watched"), ver(b));
      b.textContent = on ? "Mark as not watched" : "Mark as watched";
      b.setAttribute("aria-pressed", on ? "true" : "false");
      b.hidden = false;
    });
    $$("[data-progress]").forEach(function (el) {
      var ids = el.getAttribute("data-progress").split(",").filter(Boolean);
      var vs = (el.getAttribute("data-video-versions") || "").split(",");
      var n = ids.filter(function (id, i) { return has(id, vs[i]); }).length, bar = el.querySelector("progress"), count = el.querySelector(".count");
      if (bar) { bar.max = ids.length || 1; bar.value = n; bar.textContent = n + " of " + ids.length; }
      if (count) count.textContent = (n && n === ids.length) ? "All " + n + " watched ✓" : n + " of " + ids.length + " watched";
      el.classList.toggle("done", n > 0 && n === ids.length);
      el.hidden = false;
    });
    // "Up next": reveal the first lesson link in the list that has not been watched yet.
    $$("[data-next]").forEach(function (el) {
      var shown = false;
      $$("a[data-lesson-link]", el).forEach(function (a) {
        var show = !shown && !has(a.getAttribute("data-lesson-link"), ver(a));
        a.hidden = !show;
        if (show) shown = true;
      });
      el.hidden = !shown;
    });
    paintNew();
  }
  doc.addEventListener("click", function (e) {
    var b = e.target.closest ? e.target.closest("[data-toggle-watched]") : null;
    if (!b) return;
    e.preventDefault();
    var key = vkey(b.getAttribute("data-toggle-watched"), ver(b)), on = !isWatched(key);
    if (!key) return;
    setWatched(key, on);
    say(b, on ? "Marked as watched." : "Marked as not watched.");
  });
  $$("[data-reset-progress]").forEach(function (btn) {
    btn.hidden = false;
    btn.addEventListener("click", function () {
      if (!window.confirm("Reset your watched lessons and saved video positions on this site?")) return;
      clearCookie(C_WATCHED); clearCookie(C_VPOS); paint();
      $$("video[id]").forEach(function (v) { var r = doc.querySelector('[data-resume="' + v.id + '"]'); if (r) r.hidden = true; });
      say(btn, "Progress reset.");
    });
  });

  /* ---------- "Resume from m:ss": offered, never a silent jump */
  function offerResume(media, saved, onHide) {
    var box = doc.querySelector('[data-resume="' + media.id + '"]');
    if (!box || !(saved > 5)) return;
    var go = box.querySelector("[data-go]"), dismiss = box.querySelector("[data-dismiss]");
    function hide() { box.hidden = true; if (onHide) onHide(); }
    function show() {
      if (media.duration && saved > media.duration - 5) { box.hidden = true; return; }
      go.textContent = "Resume from " + fmt(saved);
      box.hidden = false;
    }
    go.addEventListener("click", function () {
      function seek() { media.currentTime = saved; play(media); }
      if (media.readyState >= 1) seek(); else { media.addEventListener("loadedmetadata", seek, { once: true }); media.load(); }
      hide();
    });
    if (dismiss) dismiss.addEventListener("click", hide);
    media.addEventListener("timeupdate", function () { if (!box.hidden && media.currentTime > 1) box.hidden = true; });
    show();
    if (!media.duration) media.addEventListener("loadedmetadata", show, { once: true });
  }

  /* ---------- position memory: throttled writes, forced on pause / seek / page hide, cleared at end */
  function remember(media, cookie, key, max, onEnded) {
    var last = 0;
    function save(force) {
      var now = Date.now();
      if (!force && now - last < 5000) return;
      last = now;
      var map = readMap(cookie), t = media.currentTime;
      delete map[key];                       // re-insert so the newest entry is last
      if (t > 5 && !(media.duration && t > media.duration - 5)) map[key] = t;
      writeMap(cookie, map, max);
    }
    media.addEventListener("timeupdate", function () { if (!media.paused) save(false); });
    media.addEventListener("pause", function () { if (!media.ended) save(true); });
    media.addEventListener("seeked", function () { if (media.paused) save(true); });
    media.addEventListener("ended", function () {
      var map = readMap(cookie); delete map[key]; writeMap(cookie, map, max);
      if (onEnded) onEnded();
    });
    window.addEventListener("pagehide", function () { if (!media.paused) save(true); });
    return readMap(cookie)[key];
  }

  /* ---------- lesson videos */
  $$("video[data-lesson-id]").forEach(function (v) {
    var id = vkey(v.getAttribute("data-lesson-id"), ver(v)), done = isWatched(id);
    if (!id) return;                         // unstamped page: nothing to key watched state or position on
    function mark() { if (!done) { done = true; setWatched(id, true); } }
    v.addEventListener("timeupdate", function () { if (v.duration && v.currentTime / v.duration >= 0.9) mark(); });
    v.addEventListener("ended", mark);
    offerResume(v, remember(v, C_VPOS, id, VPOS_MAX));
  });

  /* ---------- audiobook / videobook tracks (book_pos, keyed "<chapter>@<version>" per media file) */
  $$("audio[data-chapter], video[data-chapter]").forEach(function (a) {
    var ch = a.getAttribute("data-chapter"), key = vkey(ch, ver(a));
    if (!key) return;
    var msg = doc.getElementById("book-resume-" + ch)
      || (a.id === "book-video" ? doc.getElementById("book-resume-preview-video") : null)
      || (ch === "intro" ? doc.getElementById("book-resume") : null);
    var saved = remember(a, C_BOOK, key, 0, function () {
      if (msg) msg.textContent = "Finished. The full book is coming in 2027.";
    });
    if (saved > 5 && msg) msg.textContent = "Bookmark saved at " + fmt(saved) + ".";
    offerResume(a, saved, function () { if (msg) msg.textContent = ""; });
  });

  /* ---------- chapter links: real "file#t=" links, upgraded to in-page seeking; current one highlighted */
  var lists = {};
  $$("a[data-seek][data-target]").forEach(function (a) {
    var id = a.getAttribute("data-target");
    (lists[id] = lists[id] || []).push(a);
    a.addEventListener("click", function (e) {
      var m = doc.getElementById(id);
      if (!m) return;
      e.preventDefault();
      var t = parseFloat(a.getAttribute("data-seek"));
      function seek() { m.currentTime = t; play(m); }
      if (m.readyState >= 1) seek(); else { m.addEventListener("loadedmetadata", seek, { once: true }); m.load(); }
      var r = doc.querySelector('[data-resume="' + id + '"]'); if (r) r.hidden = true;
    });
  });
  Object.keys(lists).forEach(function (id) {
    var m = doc.getElementById(id), links = lists[id], cur = null;
    if (!m) return;
    function mark() {
      var t = m.currentTime, best = null;
      links.forEach(function (a) { if (parseFloat(a.getAttribute("data-seek")) <= t + 0.25) best = a; });
      if (t === 0 && m.paused) best = null;
      if (best === cur) return;
      if (cur) cur.removeAttribute("aria-current");
      if (best) best.setAttribute("aria-current", "true");
      cur = best;
    }
    m.addEventListener("timeupdate", mark);
    m.addEventListener("seeked", mark);
  });

  /* ---------- copy a lesson's rule (rules are written to be pasted into an agent's instructions) */
  if (navigator.clipboard && navigator.clipboard.writeText && window.isSecureContext) {
    $$("button[data-copy]").forEach(function (b) {
      b.hidden = false;
      b.addEventListener("click", function () {
        var src = doc.getElementById(b.getAttribute("data-copy"));
        navigator.clipboard.writeText(src.textContent.trim()).then(function () {
          say(b, "Copied.");
        }, function () { say(b, "Copy failed. Select the text and copy it instead."); });
      });
    });
  }


  /* Ask the Book compact widget on lesson pages (book page includes the script itself). */
  (function loadAskBook() {
    var path = location.pathname || "";
    var lesson = /\/(ai-tips|software-engineering-101|software-engineering-201)\/[0-9]/.test(path);
    if (!lesson) return;
    if (doc.querySelector("script[src$='ask-book.js']")) return;
    var link = doc.createElement("link");
    link.rel = "stylesheet";
    link.href = "/assets/ask-book.css";
    doc.head.appendChild(link);
    var s = doc.createElement("script");
    s.src = "/assets/ask-book.js";
    s.defer = true;
    (doc.body || doc.documentElement).appendChild(s);
  })();

  paint();
})();

  /* Open the book chapter list on desktop; keep it collapsed on phones. */
  if (window.matchMedia) {
    var wide = window.matchMedia("(min-width: 821px)");
    function syncChapters(d) {
      document.querySelectorAll("details.chapters-wrap").forEach(function (el) {
        el.open = d.matches;
      });
    }
    syncChapters(wide);
    if (wide.addEventListener) wide.addEventListener("change", function () { syncChapters(wide); });
  }
