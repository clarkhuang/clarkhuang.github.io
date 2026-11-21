/* Watched-progress and audiobook bookmarks. First-party cookies only; no third-party scripts, no analytics. */
(function () {
  "use strict";
  var YEAR = 60 * 60 * 24 * 365;

  function getCookie(name) {
    var parts = document.cookie ? document.cookie.split("; ") : [];
    for (var i = 0; i < parts.length; i++) {
      var eq = parts[i].indexOf("=");
      if (parts[i].slice(0, eq) === name) {
        try { return decodeURIComponent(parts[i].slice(eq + 1)); } catch (e) { return ""; }
      }
    }
    return "";
  }
  function setCookie(name, value, maxAge) {
    document.cookie = name + "=" + encodeURIComponent(value) + "; path=/; max-age=" +
      (maxAge == null ? YEAR : maxAge) + "; SameSite=Lax" + (location.protocol === "https:" ? "; Secure" : "");
  }

  // ---------- watched lessons: cookie "watched" = "ai-tips/01,se101/02"
  function watched() {
    var v = getCookie("watched");
    return v ? v.split(",").filter(Boolean) : [];
  }
  function markWatched(id) {
    var w = watched();
    if (w.indexOf(id) === -1) { w.push(id); setCookie("watched", w.join(",")); }
    paint();
  }
  function paint() {
    var w = watched();
    document.querySelectorAll("[data-watch-id]").forEach(function (el) {
      el.classList.toggle("is-watched", w.indexOf(el.getAttribute("data-watch-id")) !== -1);
    });
    document.querySelectorAll("[data-progress]").forEach(function (el) {
      var ids = el.getAttribute("data-progress").split(",").filter(Boolean);
      var n = ids.filter(function (id) { return w.indexOf(id) !== -1; }).length;
      var txt = el.querySelector(".progress");
      if (txt) {
        txt.textContent = n + " of " + ids.length + " watched";
        txt.classList.toggle("done", ids.length > 0 && n === ids.length);
      }
      var bar = el.querySelector(".bar i");
      if (bar) bar.style.width = (ids.length ? Math.round(100 * n / ids.length) : 0) + "%";
    });
  }
  document.querySelectorAll("[data-reset-progress]").forEach(function (b) {
    b.addEventListener("click", function () {
      if (confirm("Reset your watched progress on this site?")) { setCookie("watched", "", 0); paint(); }
    });
  });

  document.querySelectorAll("video[data-lesson-id]").forEach(function (v) {
    var id = v.getAttribute("data-lesson-id"), done = false;
    function check() {
      if (!done && v.duration && v.currentTime / v.duration >= 0.9) { done = true; markWatched(id); }
    }
    v.addEventListener("timeupdate", check);
    v.addEventListener("ended", function () { done = true; markWatched(id); });
  });

  function fmt(s) { s = Math.max(0, Math.floor(s)); return Math.floor(s / 60) + ":" + ("0" + (s % 60)).slice(-2); }

  // chapter buttons seek the media element named in data-target
  document.querySelectorAll("[data-seek]").forEach(function (b) {
    b.addEventListener("click", function () {
      var m = document.getElementById(b.getAttribute("data-target"));
      if (!m) return;
      m.currentTime = parseFloat(b.getAttribute("data-seek"));
      var p = m.play(); if (p && p.catch) p.catch(function () {});
    });
  });

  // ---------- audiobook: cookie "book_pos" = "<chapter>:<seconds>[,<chapter>:<seconds>...]"
  function parseBookPos() {
    var map = {};
    var raw = getCookie("book_pos");
    if (!raw) return map;
    raw.split(",").forEach(function (part) {
      var i = part.indexOf(":");
      if (i > 0) map[part.slice(0, i)] = part.slice(i + 1);
    });
    return map;
  }
  function writeBookPos(map) {
    var parts = [];
    Object.keys(map).forEach(function (k) { parts.push(k + ":" + map[k]); });
    setCookie("book_pos", parts.join(","));
  }
  document.querySelectorAll("audio[data-chapter]").forEach(function (audio) {
    var chapter = audio.getAttribute("data-chapter");
    var resumeEl = document.getElementById("book-resume-" + chapter) ||
                   (chapter === "intro" ? document.getElementById("book-resume") : null);
    var saved = parseBookPos();
    var lastSave = 0;
    function save(force) {
      var now = Date.now();
      if (!force && now - lastSave < 3000) return;
      lastSave = now;
      var map = parseBookPos();
      map[chapter] = audio.currentTime.toFixed(1);
      writeBookPos(map);
    }
    audio.addEventListener("loadedmetadata", function () {
      var t = parseFloat(saved[chapter]);
      if (t > 2 && t < audio.duration - 2) {
        audio.currentTime = t;
        if (resumeEl) resumeEl.textContent = "Bookmark restored: resuming at " + fmt(t) + ".";
      }
    });
    audio.addEventListener("timeupdate", function () { save(false); });
    audio.addEventListener("pause", function () { save(true); });
    audio.addEventListener("ended", function () {
      var map = parseBookPos();
      map[chapter] = "0";
      writeBookPos(map);
      if (resumeEl) resumeEl.textContent = "Finished. The full audiobook is coming in 2027.";
    });
    window.addEventListener("pagehide", function () { if (!audio.paused) save(true); });
    if (parseFloat(saved[chapter]) > 2 && resumeEl) {
      resumeEl.textContent = "Bookmark found at " + fmt(parseFloat(saved[chapter])) + ". Press play to resume.";
    }
  });

  paint();
})();
