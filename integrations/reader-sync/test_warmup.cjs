const {test} = require("node:test");
const assert = require("node:assert/strict");
const {readFileSync} = require("node:fs");
const {join} = require("node:path");
const vm = require("node:vm");

const root = join(__dirname, "../..");
const code = readFileSync(join(root, "assets/site.js"), "utf8");
const config = JSON.parse(readFileSync(join(root, "assets/reader-endpoints.json"), "utf8"));
const origin = "https://" + config.pagesHost;

function storage() {
  const entries = new Map();
  return {getItem: key => entries.get(key) ?? null, setItem: (key, value) => entries.set(key, value)};
}

async function visit(options = {}) {
  const location = new URL(options.page || "/book/", options.origin || origin);
  const canonical = options.canonical || location.origin + location.pathname.replace(/index\.html$/, "");
  const script = (location.pathname.startsWith("/staging/") ? "/staging" : "") + "/assets/site.js";
  const document = Object.assign(new EventTarget(), {
    currentScript: {src: new URL(options.script || script, location).href},
    documentElement: {classList: {add() {}}},
    getElementById: () => null, querySelectorAll: () => [],
    querySelector: selector => selector === 'link[rel="canonical"]' ? {href: canonical} : null,
    cookie: "", visibilityState: options.visibility || "visible", readyState: options.readyState || "loading",
  });
  const visits = [];
  const fetch = async (url, init) => {
    if (url.pathname.endsWith("reader-endpoints.json")) return {ok: true, json: async () => config};
    visits.push({url: url.href, ...init});
  };
  const window = Object.assign(new EventTarget(), {localStorage: options.local || storage(), sessionStorage: storage(), fetch});
  vm.runInNewContext(code, {document, location, window, navigator: options.navigator || {}, URL, fetch});
  await new Promise(resolve => setImmediate(resolve));
  return {visits, loaded() { window.dispatchEvent(new Event("load")); }};
}

test("waits for load, makes a single anonymous GET, and isolates staging from production", async () => {
  const local = storage();
  const prod = await visit({local});
  assert.deepEqual(prod.visits, []);
  prod.loaded();
  prod.loaded();
  assert.deepEqual(prod.visits, [{url: config.production + "/healthz", mode: "no-cors", credentials: "omit",
    referrerPolicy: "no-referrer", cache: "no-store", redirect: "error"}]);
  const next = await visit({local, readyState: "complete"});
  assert.equal(next.visits.length, 0);
  const stage = await visit({local, page: "/staging/about/index.html", readyState: "complete"});
  assert.equal(stage.visits[0].url, config.staging + "/healthz");
  local.setItem("reader.warm." + config.production, Date.now() - 16 * 60 * 1000);
  const later = await visit({local, readyState: "complete"});
  assert.equal(later.visits.length, 1);
});

test("skips copies, previews, hidden pages, privacy or data-saving signals and signed-in visits", async () => {
  const local = storage();
  local.setItem("reader.identity." + config.production, "receipt");
  for (const options of [{origin: "http://localhost:8000"}, {origin: "https://preview.example"},
      {canonical: origin + "/original-path/"}, {page: "/staging/about/", script: "/assets/site.js"},
      {visibility: "hidden"}, {navigator: {onLine: false}}, {navigator: {connection: {saveData: true}}},
      {navigator: {globalPrivacyControl: true}}, {navigator: {doNotTrack: "1"}}, {local},
      {local: {getItem() { throw new Error("storage disabled"); }}}]) {
    const result = await visit(options);
    result.loaded();
    assert.deepEqual(result.visits, []);
  }
});
