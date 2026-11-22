/* Ask the Book — instant local search + "Ask your AI" prefill buttons.
   No external libraries. Reads /search-index.json. */
(function () {
  "use strict";

  var INDEX_URL = "/search-index.json";
  var SITE = "https://clarkhuang.github.io";
  var LLMS = SITE + "/llms-full.txt";
  var LLMS_SHORT = SITE + "/llms.txt";
  var GITMCP = "https://gitmcp.io/clarkhuang/clarkhuang.github.io";

  var PROVIDERS = [
    { id: "chatgpt", label: "ChatGPT", url: "https://chatgpt.com/?q=" },
    { id: "claude", label: "Claude", url: "https://claude.ai/new?q=" },
    { id: "grok", label: "Grok", url: "https://grok.com/?q=" },
    { id: "perplexity", label: "Perplexity", url: "https://www.perplexity.ai/search?q=" }
  ];

  var index = null;
  var indexError = null;
  var loadPromise = null;

  function $(sel, ctx) { return (ctx || document).querySelector(sel); }
  function $$(sel, ctx) { return Array.prototype.slice.call((ctx || document).querySelectorAll(sel)); }

  function tokens(s) {
    return (s || "").toLowerCase().replace(/['’]/g, "").split(/[^a-z0-9]+/).filter(function (t) {
      return t.length > 1;
    });
  }

  function snippet(text, terms, width) {
    width = width || 180;
    var hay = text || "";
    var low = hay.toLowerCase();
    var at = -1;
    for (var i = 0; i < terms.length; i++) {
      at = low.indexOf(terms[i]);
      if (at !== -1) break;
    }
    if (at < 0) at = 0;
    var start = Math.max(0, at - 40);
    var end = Math.min(hay.length, start + width);
    var out = hay.slice(start, end).trim();
    if (start > 0) out = "…" + out;
    if (end < hay.length) out += "…";
    return out;
  }

  function scoreEntry(entry, terms) {
    if (!terms.length) return 0;
    var title = (entry.title || "").toLowerCase();
    var rule = (entry.rule || "").toLowerCase();
    var summary = (entry.summary || "").toLowerCase();
    var body = (entry.text || "").toLowerCase();
    var series = (entry.series || "").toLowerCase();
    var score = 0;
    var hits = 0;
    for (var i = 0; i < terms.length; i++) {
      var t = terms[i];
      var part = 0;
      if (title === t) part += 12;
      if (title.indexOf(t) !== -1) part += 8;
      if (rule.indexOf(t) !== -1) part += 5;
      if (series.indexOf(t) !== -1) part += 3;
      if (summary.indexOf(t) !== -1) part += 3;
      if (body.indexOf(t) !== -1) part += 1;
      if (part) { hits += 1; score += part; }
    }
    if (hits !== terms.length) score *= (hits / terms.length);
    if (entry.type === "lesson" || entry.type === "chapter") score += 0.4;
    return score;
  }

  function search(query, limit) {
    var terms = tokens(query);
    if (!index || !terms.length) return [];
    var scored = [];
    var entries = index.entries || [];
    for (var i = 0; i < entries.length; i++) {
      var s = scoreEntry(entries[i], terms);
      if (s > 0) scored.push({ entry: entries[i], score: s });
    }
    scored.sort(function (a, b) { return b.score - a.score; });
    var out = [];
    var seen = {};
    for (var j = 0; j < scored.length && out.length < (limit || 8); j++) {
      var url = scored[j].entry.url || scored[j].entry.markdown_url;
      if (!url || seen[url]) continue;
      // Prefer the lesson/chapter card over a duplicate transcript with the same URL.
      seen[url] = true;
      out.push(scored[j]);
    }
    return out;
  }

  function buildPrompt(question) {
    var q = (question || "").trim() || "(the reader will type their question here)";
    return [
      "You are helping a reader of Clark Huang's site (" + SITE + "/).",
      "",
      "Question: " + q,
      "",
      "Instructions:",
      "1. Read " + LLMS + " (or " + LLMS_SHORT + " if that is too long). If you can connect tools, use the read-only GitMCP endpoint at " + GITMCP + ".",
      "2. Answer only from this site. If the answer is not on the site, say so. Do not invent stories, quotes, numbers, or biography.",
      "3. Cite full " + SITE + "/… URLs (prefer the index.md twins).",
      "4. If the question is about the OpenBook Silicon Valley C Players or its narrator, answer in the tone of Charlie Hack, the book's fictional narrator. The story chapters are an embellished fictional dramatization; the how-to-work-with-AI half is nonfiction. Do not treat story events as facts about real people.",
      "5. For lesson questions, stay practical and cite the lesson rule."
    ].join("\n");
  }

  function loadIndex() {
    if (loadPromise) return loadPromise;
    loadPromise = fetch(INDEX_URL, { credentials: "same-origin" }).then(function (res) {
      if (!res.ok) throw new Error("HTTP " + res.status);
      return res.json();
    }).then(function (data) {
      index = data;
      return data;
    }).catch(function (err) {
      indexError = err;
      throw err;
    });
    return loadPromise;
  }

  function renderResults(box, query) {
    var list = $("[data-ask-results]", box);
    var status = $("[data-ask-status]", box);
    if (!list) return;
    list.innerHTML = "";
    var q = (query || "").trim();
    if (!q) {
      if (status) status.textContent = index
        ? "Type a few words. Results stay on this page and link back to the source."
        : (indexError ? "Could not load the search index. Use “Ask your AI” or copy the prompt instead." : "Loading the search index…");
      return;
    }
    if (!index) {
      if (status) status.textContent = indexError
        ? "Could not load the search index. Use “Ask your AI” or copy the prompt instead."
        : "Loading the search index…";
      return;
    }
    var hits = search(q, box.hasAttribute("data-ask-book-page") ? 12 : 5);
    if (status) {
      status.textContent = hits.length
        ? hits.length + (hits.length === 1 ? " result" : " results") + " on this site."
        : "No local matches. Ask your AI, or try different words.";
    }
    var terms = tokens(q);
    hits.forEach(function (hit) {
      var e = hit.entry;
      var li = document.createElement("li");
      var a = document.createElement("a");
      a.href = e.url || e.markdown_url || "#";
      var meta = document.createElement("span");
      meta.className = "ask-meta";
      meta.textContent = [e.type, e.series].filter(Boolean).join(" · ");
      var title = document.createElement("span");
      title.className = "ask-title";
      title.textContent = e.title || "Untitled";
      var snip = document.createElement("span");
      snip.className = "ask-snippet";
      snip.textContent = snippet(e.summary || e.rule || e.text || "", terms);
      a.appendChild(meta);
      a.appendChild(title);
      if (snip.textContent) a.appendChild(snip);
      li.appendChild(a);
      list.appendChild(li);
    });
  }

  function currentQuestion(box) {
    var field = $("[data-ask-q]", box);
    return field ? field.value : "";
  }

  function refreshPrompt(box) {
    var pre = $("[data-ask-prompt]", box);
    if (pre) pre.textContent = buildPrompt(currentQuestion(box));
    var q = currentQuestion(box).trim();
    $$("[data-ask-provider]", box).forEach(function (a) {
      var provider = PROVIDERS.filter(function (p) { return p.id === a.getAttribute("data-ask-provider"); })[0];
      if (!provider) return;
      if (!q) {
        a.setAttribute("aria-disabled", "true");
        a.setAttribute("tabindex", "-1");
        a.href = provider.url;
      } else {
        a.removeAttribute("aria-disabled");
        a.removeAttribute("tabindex");
        a.href = provider.url + encodeURIComponent(buildPrompt(q));
      }
    });
  }

  function enhance(box) {
    if (!box || box.getAttribute("data-ask-ready")) return;
    box.setAttribute("data-ask-ready", "true");

    var q = $("[data-ask-q]", box);
    if (q) {
      var t = null;
      q.addEventListener("input", function () {
        refreshPrompt(box);
        window.clearTimeout(t);
        t = window.setTimeout(function () { renderResults(box, q.value); }, 60);
      });
      q.addEventListener("search", function () { renderResults(box, q.value); });
    }

    $$("[data-copy]", box).forEach(function (b) {
      /* site.js also wires [data-copy]; this is a fallback if the box was injected later. */
      b.hidden = false;
    });

    var copyBtn = $("[data-ask-copy]", box);
    if (copyBtn && navigator.clipboard && navigator.clipboard.writeText && window.isSecureContext) {
      copyBtn.hidden = false;
      copyBtn.addEventListener("click", function () {
        var text = buildPrompt(currentQuestion(box));
        navigator.clipboard.writeText(text).then(function () {
          var status = $("[data-ask-copy-status]", box) || $("[data-status]", box);
          if (status) {
            status.textContent = "";
            setTimeout(function () { status.textContent = "Prompt copied."; }, 30);
          }
        }, function () {
          var status = $("[data-ask-copy-status]", box) || $("[data-status]", box);
          if (status) status.textContent = "Copy failed. Select the prompt and copy it instead.";
        });
      });
    }

    refreshPrompt(box);
    renderResults(box, q ? q.value : "");
    loadIndex().then(function () {
      renderResults(box, q ? q.value : "");
    }, function () {
      renderResults(box, q ? q.value : "");
    });
  }

  function widgetHTML(compact) {
    var buttons = PROVIDERS.map(function (p) {
      return '<a class="btn ghost" data-ask-provider="' + p.id + '" href="' + p.url + '" rel="noopener noreferrer">' + p.label + "</a>";
    }).join("");
    return (
      (compact
        ? '<h2>Ask the Book</h2><p class="ask-book-lede">Search this site instantly, or send your question to your own AI with a prompt that points at the public text and citations.</p>'
        : "") +
      '<form class="ask-book-form" action="/ask/" method="get" role="search">' +
        '<label for="ask-book-q">Your question</label>' +
        '<input type="search" id="ask-book-q" name="q" data-ask-q placeholder="For example: What is the rule in Paste First, Ask Second?" autocomplete="off" enterkeyhint="search">' +
      "</form>" +
      '<p class="ask-book-status" data-ask-status role="status">Loading the search index…</p>' +
      '<ul class="ask-book-results" data-ask-results></ul>' +
      '<p class="label">Ask your AI</p>' +
      '<div class="ask-ai-row">' + buttons + "</div>" +
      '<div class="ai-prompt" data-status-scope>' +
        '<pre class="ask-prompt-preview" data-ask-prompt tabindex="0"></pre>' +
        '<p class="tools"><button type="button" class="btn ghost" data-ask-copy hidden>Copy prompt</button> ' +
        '<span class="status" role="status" data-ask-copy-status></span></p>' +
      "</div>" +
      '<p class="ask-book-note">The buttons open ChatGPT, Claude, Grok, or Perplexity with the prompt already filled in. You review it before it runs (Grok and Claude wait; ChatGPT and Perplexity may send it). Nothing is sent from this page. <a href="/ask/">Full Ask the Book page</a>.</p>'
    );
  }

  function mountCompact() {
    if ($("[data-ask-book]") || $("#ask-book")) return;
    var footer = $("footer.site-footer");
    var mount = $("[data-ask-book-mount]");
    var box = document.createElement("section");
    box.className = "ask-book ask-book-compact";
    box.setAttribute("data-ask-book", "compact");
    box.setAttribute("aria-labelledby", "ask-book-heading-inject");
    box.innerHTML = widgetHTML(true).replace("<h2>Ask the Book</h2>", '<h2 id="ask-book-heading-inject">Ask the Book</h2>');
    if (mount) {
      mount.appendChild(box);
    } else if (footer && footer.parentNode) {
      /* Place just above the site footer, inside main if we can. */
      var main = $("main .wrap") || $("main");
      if (main) main.appendChild(box);
      else footer.parentNode.insertBefore(box, footer);
    } else {
      return;
    }
    enhance(box);
  }

  function init() {
    var pages = $$("[data-ask-book], #ask-book");
    if (pages.length) {
      pages.forEach(enhance);
      /* Prefill from ?q= on the full page. */
      var params = new URLSearchParams(location.search);
      var q = params.get("q");
      if (q) {
        pages.forEach(function (box) {
          var field = $("[data-ask-q]", box);
          if (field && !field.value) {
            field.value = q;
            refreshPrompt(box);
            loadIndex().then(function () { renderResults(box, q); }, function () { renderResults(box, q); });
          }
        });
      }
    } else {
      mountCompact();
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
