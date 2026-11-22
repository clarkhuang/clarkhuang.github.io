/* Clark Huang — learning site (opus variant).
   Progressive enhancement only: every video and audio track works without this file.
   State lives in first-party cookies (no localStorage, no analytics, no third parties):
     opus_watched  = "ai-tips/01,se101/02"            lessons played to ~90% or to the end
     opus_vpos     = "ai-tips/02:73.4,..."            video resume positions (seconds)
     opus_book_pos = "intro:31.2,math1a:12.0"         audiobook listening bookmarks (seconds) */
(function () {
  "use strict";
  var doc = document, root = doc.documentElement;
  root.classList.add("js");

  var YEAR = 31536000;
  var C_WATCHED = "opus_watched", C_VPOS = "opus_vpos", C_BOOK = "opus_book_pos";

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
      (maxAge == null ? YEAR : maxAge) + "; SameSite=Lax" +
      (location.protocol === "https:" ? "; Secure" : "");
  }
  function clearCookie(name) { setCookie(name, "", 0); }
  function readMap(name) {
    var map = {}, raw = getCookie(name);
    if (raw) raw.split(",").forEach(function (part) {
      var i = part.lastIndexOf(":"), v = parseFloat(part.slice(i + 1));
      if (i > 0 && isFinite(v)) map[part.slice(0, i)] = v;
    });
    return map;
  }
  function writeMap(name, map) {
    var parts = Object.keys(map).map(function (k) { return k + ":" + map[k].toFixed(1); });
    if (parts.length) setCookie(name, parts.join(",")); else clearCookie(name);
  }
  function fmt(s) {
    s = Math.max(0, Math.floor(s));
    return Math.floor(s / 60) + ":" + ("0" + (s % 60)).slice(-2);
  }
  function $$(sel, ctx) { return Array.prototype.slice.call((ctx || doc).querySelectorAll(sel)); }
  function play(media) { var p = media.play(); if (p && p.catch) p.catch(function () {}); }

  /* ---------- watched lessons */
  function watched() { return getCookie(C_WATCHED).split(",").filter(Boolean); }
  function isWatched(id) { return watched().indexOf(id) !== -1; }
  function markWatched(id) {
    var w = watched();
    if (w.indexOf(id) === -1) { w.push(id); setCookie(C_WATCHED, w.join(",")); }
    paint();
  }
  function paint() {
    var w = watched();
    $$("[data-watch-id]").forEach(function (el) {
      el.classList.toggle("is-watched", w.indexOf(el.getAttribute("data-watch-id")) !== -1);
    });
    $$("[data-progress]").forEach(function (el) {
      var ids = el.getAttribute("data-progress").split(",").filter(Boolean);
      var n = ids.filter(function (id) { return w.indexOf(id) !== -1; }).length;
      var bar = el.querySelector("progress"), count = el.querySelector(".count");
      if (bar) { bar.max = ids.length; bar.value = n; }
      if (count) count.textContent = n === ids.length && n > 0
        ? "All " + n + " watched ✓" : n + " of " + ids.length + " watched";
      el.classList.toggle("done", n > 0 && n === ids.length);
      el.hidden = false;
    });
    $$("[data-next]").forEach(function (el) {
      // "Up next": the first lesson in this list that has not been watched yet.
      var shown = false;
      $$("a[data-lesson-link]", el).forEach(function (a) {
        var show = !shown && w.indexOf(a.getAttribute("data-lesson-link")) === -1;
        a.hidden = !show;
        if (show) shown = true;
      });
      el.hidden = !shown;
    });
  }
  $$("[data-reset]").forEach(function (btn) {
    btn.hidden = false;
    btn.addEventListener("click", function () {
      if (!window.confirm("Reset your watched lessons and saved video positions on this site?")) return;
      clearCookie(C_WATCHED); clearCookie(C_VPOS); paint();
      $$("[data-resume]").forEach(function (b) { if (b.closest(".player-block")) b.hidden = true; });
      say(btn, "Progress reset.");
    });
  });
  function say(near, msg) {
    var s = (near.closest("[data-status-scope]") || doc).querySelector("[data-status]");
    if (s) { s.textContent = ""; setTimeout(function () { s.textContent = msg; }, 30); }
  }

  /* ---------- "Resume from m:ss" offer shared by video and audio */
  function offerResume(media, saved) {
    var box = doc.querySelector('[data-resume="' + media.id + '"]');
    if (!box || !(saved > 5)) return;
    var btn = box.querySelector("button[data-go]"), dismiss = box.querySelector("button[data-dismiss]");
    function hide() { box.hidden = true; }
    function show() {
      if (media.duration && saved > media.duration - 5) return hide();
      btn.textContent = "Resume from " + fmt(saved);
      box.hidden = false;
    }
    btn.addEventListener("click", function () {
      media.currentTime = saved; play(media); hide(); media.focus && media.focus();
    });
    if (dismiss) dismiss.addEventListener("click", hide);
    media.addEventListener("timeupdate", function () { if (media.currentTime >= saved - 1) hide(); });
    show();
    if (!media.duration) media.addEventListener("loadedmetadata", show, { once: true });
  }

  /* ---------- per-medium position memory (throttled writes, forced on pause / page hide) */
  function remember(media, cookieName, key, onEnded) {
    var last = 0;
    function save(force) {
      var now = Date.now();
      if (!force && now - last < 5000) return;
      last = now;
      var map = readMap(cookieName), t = media.currentTime;
      if (t > 5 && !(media.duration && t > media.duration - 5)) map[key] = t; else delete map[key];
      writeMap(cookieName, map);
    }
    media.addEventListener("timeupdate", function () { if (!media.paused) save(false); });
    media.addEventListener("pause", function () { save(true); });
    media.addEventListener("seeked", function () { if (media.paused) save(true); });
    media.addEventListener("ended", function () {
      var map = readMap(cookieName); delete map[key]; writeMap(cookieName, map);
      if (onEnded) onEnded();
    });
    window.addEventListener("pagehide", function () { if (!media.paused) save(true); });
    offerResume(media, readMap(cookieName)[key]);
  }

  /* ---------- lesson videos */
  $$("video[data-lesson]").forEach(function (v) {
    var id = v.getAttribute("data-lesson"), done = isWatched(id);
    v.addEventListener("timeupdate", function () {
      if (!done && v.duration && v.currentTime / v.duration >= 0.9) { done = true; markWatched(id); }
    });
    v.addEventListener("ended", function () { done = true; markWatched(id); });
    remember(v, C_VPOS, id);
  });

  /* ---------- audiobook tracks */
  $$("audio[data-track]").forEach(function (a) {
    var key = a.getAttribute("data-track");
    if (a.hasAttribute("data-no-bookmark")) return;
    remember(a, C_BOOK, key, function () {
      var s = doc.querySelector('[data-ended="' + a.id + '"]');
      if (s) s.hidden = false;
    });
  });
  $$("[data-forget-bookmarks]").forEach(function (btn) {
    btn.hidden = false;
    btn.addEventListener("click", function () {
      clearCookie(C_BOOK);
      $$("[data-resume]").forEach(function (b) { if (b.closest(".track")) b.hidden = true; });
      say(btn, "Listening bookmarks cleared.");
    });
  });

  /* ---------- chapter / scene / transcript links: seek in-page instead of opening the file */
  var lists = {};
  $$("a[data-seek][data-target]").forEach(function (a) {
    var id = a.getAttribute("data-target");
    (lists[id] = lists[id] || []).push(a);
    a.addEventListener("click", function (e) {
      var m = doc.getElementById(id);
      if (!m) return;
      e.preventDefault();
      m.currentTime = parseFloat(a.getAttribute("data-seek"));
      play(m);
    });
  });
  Object.keys(lists).forEach(function (id) {
    var m = doc.getElementById(id), links = lists[id], cur = null;
    if (!m) return;
    function mark() {
      var t = m.currentTime, best = null;
      links.forEach(function (a) { if (parseFloat(a.getAttribute("data-seek")) <= t + 0.05) best = a; });
      if (m.currentTime === 0 && m.paused) best = null;
      if (best === cur) return;
      if (cur) cur.removeAttribute("aria-current");
      if (best) best.setAttribute("aria-current", "true");
      cur = best;
    }
    m.addEventListener("timeupdate", mark);
    m.addEventListener("seeked", mark);
  });

  /* ---------- copy a lesson's rule (written to be pasted into an agent's instructions) */
  if (navigator.clipboard && window.isSecureContext) {
    $$("button[data-copy]").forEach(function (b) {
      b.hidden = false;
      b.addEventListener("click", function () {
        var src = doc.getElementById(b.getAttribute("data-copy"));
        navigator.clipboard.writeText(src.textContent.trim()).then(function () {
          say(b, "Rule copied to the clipboard.");
        }, function () { say(b, "Copy failed. Select the text and copy it manually."); });
      });
    });
  }

  /* ---------- videobook teaser: stick figures + captions driven by the audio clock */
  var tz = doc.getElementById("teaser");
  if (tz) {
    var audio = tz.querySelector("audio"), capEl = tz.querySelector(".tz-caption");
    var cues = $$("[data-cue]").map(function (a) {
      return { t: parseFloat(a.getAttribute("data-seek")), text: a.lastElementChild.textContent, scene: a.getAttribute("data-scene") };
    });
    var scenes = $$(".scene", tz), steps = $$("[data-from],[data-until]", tz), cur = -2, raf = 0;
    var idle = capEl.textContent;
    function render() {
      var t = audio.currentTime, idx = -1;
      for (var i = 0; i < cues.length; i++) if (cues[i].t <= t + 0.05) idx = i;
      if (t === 0 && audio.paused) idx = -1;
      if (idx === cur) return;
      cur = idx;
      var scene = idx < 0 ? cues[0].scene : cues[idx].scene, step = Math.max(idx, 0);
      capEl.textContent = idx < 0 ? idle : cues[idx].text;
      scenes.forEach(function (s) { s.classList.toggle("on", s.getAttribute("data-scene") === scene); });
      steps.forEach(function (el) {
        if (el.hasAttribute("data-from")) el.classList.toggle("in", +el.getAttribute("data-from") <= step);
        if (el.hasAttribute("data-until")) el.classList.toggle("out", +el.getAttribute("data-until") < step);
      });
    }
    function tick() { render(); raf = audio.paused ? 0 : requestAnimationFrame(tick); }
    audio.addEventListener("play", function () { tz.classList.add("playing"); if (!raf) tick(); });
    audio.addEventListener("pause", function () { tz.classList.remove("playing"); render(); });
    audio.addEventListener("ended", function () { tz.classList.remove("playing"); });
    audio.addEventListener("seeked", render);
    audio.addEventListener("timeupdate", render);
    render();
  }

  paint();
})();
