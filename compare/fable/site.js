/* Clark Huang — learning site (fable variant).
   Progressive enhancement only: every page reads and plays without this file.
   State lives in three small first-party cookies (no localStorage, no network):
     fable_watched   = "ai-tips/01,se101/02"          lessons watched
     fable_video_pos = "ai-tips/02:45,se101/01:120"   video resume points, seconds
     fable_book_pos  = "intro:31,math1a:12"           audiobook bookmarks, seconds */
(function () {
  "use strict";

  var YEAR = 60 * 60 * 24 * 365;
  var WATCHED = "fable_watched", VIDEO_POS = "fable_video_pos", BOOK_POS = "fable_book_pos";
  var reduceMotion = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;

  function $all(sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); }
  function fmt(s) { s = Math.max(0, Math.floor(s)); return Math.floor(s / 60) + ":" + ("0" + (s % 60)).slice(-2); }

  /* ---------- cookies ---------- */
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
  function setCookie(name, value) {
    document.cookie = name + "=" + encodeURIComponent(value) + "; path=/; max-age=" + (value ? YEAR : 0) +
      "; SameSite=Lax" + (location.protocol === "https:" ? "; Secure" : "");
  }
  // "key:value,key:value" <-> object
  function readMap(name) {
    var map = {};
    getCookie(name).split(",").forEach(function (part) {
      var i = part.lastIndexOf(":");
      if (i > 0) map[part.slice(0, i)] = part.slice(i + 1);
    });
    return map;
  }
  function writeMap(name, map) {
    setCookie(name, Object.keys(map).map(function (k) { return k + ":" + map[k]; }).join(","));
  }

  /* ---------- watched lessons ---------- */
  function watched() { return getCookie(WATCHED).split(",").filter(Boolean); }
  function setWatched(id, on) {
    var list = watched().filter(function (x) { return x !== id; });
    if (on) list.push(id);
    setCookie(WATCHED, list.join(","));
    paint();
  }
  function paint() {
    var list = watched();
    function has(id) { return list.indexOf(id) !== -1; }

    $all("[data-state]").forEach(function (el) {          // "Watched" / "Not watched" badges
      var on = has(el.getAttribute("data-state"));
      el.textContent = on ? "✓ Watched" : "Not watched";
      el.classList.toggle("done", on);
      el.hidden = false;
    });
    $all("[data-watch-row]").forEach(function (el) {
      el.classList.toggle("is-watched", has(el.getAttribute("data-watch-row")));
    });
    $all("[data-toggle-watched]").forEach(function (b) {
      var on = has(b.getAttribute("data-toggle-watched"));
      b.textContent = on ? "Mark as not watched" : "Mark as watched";
      b.setAttribute("aria-pressed", on ? "true" : "false");
      b.hidden = false;
    });
    $all("[data-progress]").forEach(function (el) {       // per-series meters
      var ids = el.getAttribute("data-progress").split(",").filter(Boolean);
      var n = ids.filter(has).length;
      var bar = el.querySelector("progress"), text = el.querySelector("span");
      if (bar) { bar.max = ids.length; bar.value = n; }
      if (text) text.textContent = n + " of " + ids.length + " watched" + (n === ids.length ? " · series complete" : "");
      el.hidden = false;
    });
    $all("[data-reset]").forEach(function (b) { b.hidden = list.length === 0 && !getCookie(VIDEO_POS); });
  }
  document.addEventListener("click", function (e) {
    var t = e.target.closest ? e.target.closest("[data-toggle-watched],[data-reset]") : null;
    if (!t) return;
    if (t.hasAttribute("data-reset")) {
      if (confirm("Reset your watched progress and video resume points on this site?")) {
        setCookie(WATCHED, ""); setCookie(VIDEO_POS, ""); paint();
        $all("[data-resume-for]").forEach(function (el) { if (el.getAttribute("data-kind") === "video") el.hidden = true; });
      }
    } else {
      var id = t.getAttribute("data-toggle-watched");
      setWatched(id, watched().indexOf(id) === -1);
    }
  });

  /* ---------- seek helper (works before metadata has loaded) ---------- */
  function seek(media, t, thenPlay) {
    function go() {
      media.currentTime = t;
      if (thenPlay) { var p = media.play(); if (p && p.catch) p.catch(function () {}); }
    }
    if (media.readyState >= 1) go();
    else { media.addEventListener("loadedmetadata", go, { once: true }); media.load(); }
  }

  /* ---------- remember a position and offer "Resume from m:ss" ---------- */
  function remember(media, cookie, key, kind) {
    var slot = document.querySelector('[data-resume-for="' + key + '"]');
    var last = 0;
    function save(force) {
      var now = Date.now();
      if (!force && now - last < 5000) return;
      last = now;
      var map = readMap(cookie), t = media.currentTime, d = media.duration || 0;
      if (t < 3 || (d && t > d - 3)) delete map[key]; else map[key] = Math.round(t);
      writeMap(cookie, map);
    }
    media.addEventListener("timeupdate", function () { save(false); });
    media.addEventListener("pause", function () { save(true); });
    media.addEventListener("ended", function () { save(true); });
    window.addEventListener("pagehide", function () { if (media.currentTime > 0) save(true); });

    var saved = parseFloat(readMap(cookie)[key]);
    if (!slot || !(saved >= 3)) return;
    slot.setAttribute("data-kind", kind);
    var btn = document.createElement("button");
    btn.type = "button"; btn.className = "btn quiet";
    btn.textContent = "Resume from " + fmt(saved);
    btn.addEventListener("click", function () { seek(media, saved, true); slot.hidden = true; media.focus(); });
    slot.textContent = (kind === "video" ? "You stopped partway through. " : "Bookmark saved. ");
    slot.appendChild(btn);
    slot.hidden = false;
    media.addEventListener("play", function () { slot.hidden = true; }, { once: true });
  }

  /* ---------- lesson videos ---------- */
  $all("video[data-lesson]").forEach(function (v) {
    var id = v.getAttribute("data-lesson"), done = false;
    function mark() { if (!done) { done = true; setWatched(id, true); } }
    v.addEventListener("timeupdate", function () { if (v.duration && v.currentTime / v.duration >= 0.9) mark(); });
    v.addEventListener("ended", mark);
    remember(v, VIDEO_POS, id, "video");
  });
  $all("audio[data-track]").forEach(function (a) { remember(a, BOOK_POS, a.getAttribute("data-track"), "audio"); });

  /* ---------- chapter / scene lists: <ol data-for="media-id"> with <a data-t="seconds"> ---------- */
  $all("ol[data-for]").forEach(function (list) {
    var media = document.getElementById(list.getAttribute("data-for"));
    var links = $all("a[data-t]", list);
    if (!media || !links.length) return;
    var starts = links.map(function (a) { return parseFloat(a.getAttribute("data-t")); });
    list.addEventListener("click", function (e) {
      var a = e.target.closest("a[data-t]");
      if (!a) return;
      e.preventDefault();                                   // without JS the link opens the file at #t=
      seek(media, parseFloat(a.getAttribute("data-t")), true);
    });
    function highlight() {
      var t = media.currentTime + 0.05, cur = -1;
      for (var i = 0; i < starts.length; i++) if (t >= starts[i]) cur = i;
      links.forEach(function (a, i) {
        if (i === cur) a.setAttribute("aria-current", "true"); else a.removeAttribute("aria-current");
      });
    }
    media.addEventListener("timeupdate", highlight);
    media.addEventListener("seeked", highlight);
  });

  /* ---------- copy a lesson's rule (it is written to be pasted into an agent) ---------- */
  $all("[data-copy]").forEach(function (b) {
    var src = document.getElementById(b.getAttribute("data-copy"));
    if (!src || !navigator.clipboard) return;
    b.hidden = false;
    b.addEventListener("click", function () {
      navigator.clipboard.writeText(src.textContent.trim()).then(function () {
        var old = b.textContent; b.textContent = "Copied";
        setTimeout(function () { b.textContent = old; }, 1600);
      });
    });
  });

  /* ---------- videobook stage: stick-figure scenes driven by the narration clock ----------
     Cues are the transcript links (<a data-t>) inside .cues; drawing parts carry
     data-from / data-to cue indexes. Nothing here runs on a timer of its own unless
     the audio file cannot be loaded, in which case a silent clock stands in. */
  var stage = document.querySelector("[data-stage]");
  if (stage) (function () {
    var audio = document.getElementById(stage.getAttribute("data-stage"));
    var caption = stage.querySelector(".caption");
    var cueLinks = $all(".cues a[data-t]");
    var starts = cueLinks.map(function (a) { return parseFloat(a.getAttribute("data-t")); });
    var scenes = cueLinks.map(function (a) { return a.closest("li[data-scene]"); });
    var parts = $all("[data-from]", stage).map(function (el) {
      var to = el.getAttribute("data-to");
      return { el: el, from: +el.getAttribute("data-from"), to: to === null ? Infinity : +to };
    });
    var total = parseFloat(stage.getAttribute("data-duration")) || 77;
    var current = -1, raf = 0;
    var silent = null;                                     // {t, at, running} when audio is unavailable

    function now() {
      if (!silent) return audio.currentTime;
      return Math.min(total, silent.t + (silent.running ? (performance.now() - silent.at) / 1000 : 0));
    }
    function playing() { return silent ? silent.running : !audio.paused && !audio.ended; }

    function render() {
      var t = now() + 0.05, i = 0;
      for (var k = 0; k < starts.length; k++) if (t >= starts[k]) i = k;
      if (i !== current) {
        current = i;
        parts.forEach(function (p) { p.el.classList.toggle("on", i >= p.from && i < p.to); });
        caption.innerHTML = cueLinks[i].innerHTML;
      }
      // progress through the current scene, 0..1, used by the walking figure
      var first = i, lastCue = i;
      while (first > 0 && scenes[first - 1] === scenes[i]) first--;
      while (lastCue < scenes.length - 1 && scenes[lastCue + 1] === scenes[i]) lastCue++;
      var s0 = starts[first], s1 = lastCue + 1 < starts.length ? starts[lastCue + 1] : total;
      var at = reduceMotion ? starts[i] : t;               // reduced motion: step once per caption
      stage.style.setProperty("--p", Math.max(0, Math.min(1, (at - s0) / (s1 - s0))).toFixed(3));
    }
    function loop() {
      render();
      if (silent && now() >= total) { silent.running = false; silent.t = total; sync(); return; }
      if (playing()) raf = requestAnimationFrame(loop);
    }
    function sync() {
      var on = playing();
      stage.classList.toggle("is-playing", on);
      start.hidden = on || (!silent && now() > 0.3);
      cancelAnimationFrame(raf);
      if (on) loop(); else render();
    }
    function toggle() {
      if (silent) {
        if (silent.running) { silent.t = now(); silent.running = false; }
        else { if (silent.t >= total) silent.t = 0; silent.at = performance.now(); silent.running = true; }
        sync();
      } else if (audio.paused) { var p = audio.play(); if (p && p.catch) p.catch(function () {}); }
      else audio.pause();
    }

    var start = document.createElement("button");
    start.type = "button"; start.className = "btn stage-start";
    start.textContent = "▶ Play the teaser · " + fmt(total);
    start.addEventListener("click", toggle);
    stage.insertBefore(start, stage.firstChild);
    stage.querySelector("svg").addEventListener("click", toggle);

    ["play", "pause", "ended", "seeked", "timeupdate"].forEach(function (ev) {
      audio.addEventListener(ev, ev === "timeupdate" ? render : sync);
    });
    var src = audio.querySelector("source");
    function goSilent() {
      if (silent) return;
      silent = { t: 0, at: 0, running: false };
      var note = document.getElementById("stage-note");
      if (note) { note.textContent = "The narration could not be loaded, so the teaser will play silently with captions."; note.hidden = false; }
      start.textContent = "▶ Play without sound · " + fmt(total);
      sync();
    }
    if (src) src.addEventListener("error", goSilent);
    audio.addEventListener("error", goSilent);

    // transcript lines seek the stage too (the generic handler above already seeks the audio)
    document.querySelector(".cues").addEventListener("click", function (e) {
      var a = e.target.closest("a[data-t]");
      if (a && silent) { e.preventDefault(); silent.t = parseFloat(a.getAttribute("data-t")); silent.at = performance.now(); silent.running = true; sync(); }
    });
    render();
  })();

  paint();
})();
