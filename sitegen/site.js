/* Clark Huang — learning site. Progressive enhancement only: every video and audio works without it.
   State lives in first-party cookies only (no localStorage, no analytics, no third parties):
     watched  = "ai-tips/01,se101/02"        lessons played to ~90% or to the end, or marked by hand
     vpos     = "ai-tips/02:73.4,se101/01:12.0"  video resume positions in seconds (newest last, max 20)
     book_pos = "preview:31.2"               audiobook/videobook bookmarks in seconds (older intro,math1a keys may still be in a cookie)
   Cookie names "watched" and "book_pos" are unchanged from earlier versions of the site. */
(function () {
  "use strict";
  var doc = document;
  doc.documentElement.classList.add("js");

  var YEAR = 31536000, C_WATCHED = "watched", C_VPOS = "vpos", C_BOOK = "book_pos", VPOS_MAX = 20;

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
    doc.cookie = name + "=" + encodeURIComponent(value) + "; path=/; max-age=" +
      (maxAge == null ? YEAR : maxAge) + "; SameSite=Lax" + (location.protocol === "https:" ? "; Secure" : "");
  }
  function clearCookie(name) { setCookie(name, "", 0); }
  // "key:seconds" pairs; keys keep their order so the oldest can be dropped first.
  function readMap(name) {
    var map = {}, raw = getCookie(name);
    if (raw) raw.split(",").forEach(function (part) {
      var i = part.lastIndexOf(":"), v = parseFloat(part.slice(i + 1));
      if (i > 0 && isFinite(v)) map[part.slice(0, i)] = v;
    });
    return map;
  }
  function writeMap(name, map, max) {
    var keys = Object.keys(map).filter(function (k) { return map[k] > 0; });
    if (max && keys.length > max) keys = keys.slice(keys.length - max);
    if (keys.length) setCookie(name, keys.map(function (k) { return k + ":" + map[k].toFixed(1); }).join(","));
    else clearCookie(name);
  }

  function $$(sel, ctx) { return Array.prototype.slice.call((ctx || doc).querySelectorAll(sel)); }
  function fmt(s) { s = Math.max(0, Math.floor(s)); return Math.floor(s / 60) + ":" + ("0" + (s % 60)).slice(-2); }
  function play(m) { var p = m.play(); if (p && p.catch) p.catch(function () {}); }
  function say(near, msg) {
    var scope = near.closest("[data-status-scope]") || doc, s = scope.querySelector("[data-status]");
    if (s) { s.textContent = ""; setTimeout(function () { s.textContent = msg; }, 30); }
  }

  /* ---------- watched lessons */
  function watched() { return getCookie(C_WATCHED).split(",").filter(Boolean); }
  function isWatched(id) { return watched().indexOf(id) !== -1; }
  function setWatched(id, on) {
    var w = watched(), i = w.indexOf(id);
    if (on && i === -1) w.push(id);
    if (!on && i !== -1) w.splice(i, 1);
    if (w.length) setCookie(C_WATCHED, w.join(",")); else clearCookie(C_WATCHED);
    paint();
  }
  function paint() {
    var w = watched();
    function has(id) { return w.indexOf(id) !== -1; }
    $$("[data-watch-id]").forEach(function (el) { el.classList.toggle("is-watched", has(el.getAttribute("data-watch-id"))); });
    $$("[data-toggle-watched]").forEach(function (b) {
      var on = has(b.getAttribute("data-toggle-watched"));
      b.textContent = on ? "Mark as not watched" : "Mark as watched";
      b.setAttribute("aria-pressed", on ? "true" : "false");
      b.hidden = false;
    });
    $$("[data-progress]").forEach(function (el) {
      var ids = el.getAttribute("data-progress").split(",").filter(Boolean);
      var n = ids.filter(has).length, bar = el.querySelector("progress"), count = el.querySelector(".count");
      if (bar) { bar.max = ids.length || 1; bar.value = n; bar.textContent = n + " of " + ids.length; }
      if (count) count.textContent = (n && n === ids.length) ? "All " + n + " watched ✓" : n + " of " + ids.length + " watched";
      el.classList.toggle("done", n > 0 && n === ids.length);
      el.hidden = false;
    });
    // "Up next": reveal the first lesson link in the list that has not been watched yet.
    $$("[data-next]").forEach(function (el) {
      var shown = false;
      $$("a[data-lesson-link]", el).forEach(function (a) {
        var show = !shown && !has(a.getAttribute("data-lesson-link"));
        a.hidden = !show;
        if (show) shown = true;
      });
      el.hidden = !shown;
    });
  }
  doc.addEventListener("click", function (e) {
    var b = e.target.closest ? e.target.closest("[data-toggle-watched]") : null;
    if (!b) return;
    e.preventDefault();
    var id = b.getAttribute("data-toggle-watched"), on = !isWatched(id);
    setWatched(id, on);
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
    var id = v.getAttribute("data-lesson-id"), done = isWatched(id);
    function mark() { if (!done) { done = true; setWatched(id, true); } }
    v.addEventListener("timeupdate", function () { if (v.duration && v.currentTime / v.duration >= 0.9) mark(); });
    v.addEventListener("ended", mark);
    offerResume(v, remember(v, C_VPOS, id, VPOS_MAX));
  });

  /* ---------- audiobook tracks (cookie format unchanged: book_pos) */
  $$("audio[data-chapter], video[data-chapter]").forEach(function (a) {
    var ch = a.getAttribute("data-chapter");
    var msg = doc.getElementById("book-resume-" + ch)
      || (a.id === "book-video" ? doc.getElementById("book-resume-preview-video") : null)
      || (ch === "intro" ? doc.getElementById("book-resume") : null);
    var saved = remember(a, C_BOOK, ch, 0, function () {
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
