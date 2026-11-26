const {test} = require("node:test");
const assert = require("node:assert/strict");
const {webcrypto} = require("node:crypto");
const {readFileSync} = require("node:fs");
const {join} = require("node:path");
const vm = require("node:vm");

const script = readFileSync(join(__dirname, "../../assets/site.js"), "utf8");
const tick = () => new Promise(resolve => setImmediate(resolve));
const json = (status, value) => new Response(JSON.stringify(value), {
  status, headers: {"Content-Type": "application/json"},
});

async function page(reply) {
  const location = new URL("https://pages.example/staging/book/");
  const ids = new Map(), requests = [], forms = [];
  function element(tag) {
    const el = Object.assign(new EventTarget(), {
      tag, children: [], querySelector: () => null, querySelectorAll: () => [],
      appendChild(child) { this.children.push(child); child.parentNode = this; },
      prepend(child) { this.children.unshift(child); if (child.id) ids.set(child.id, child); },
      setAttribute() {}, removeAttribute() {}, remove() { ids.delete(this.id); },
      submit() { forms.push(this); },
    });
    return el;
  }
  const nav = element("nav"), main = element("main");
  const document = Object.assign(new EventTarget(), {
    currentScript: {src: location.origin + "/staging/assets/site.js"},
    documentElement: {classList: {add() {}}}, body: element("body"), createElement: element,
    getElementById: id => ids.get(id), querySelectorAll: () => [],
    querySelector: selector => selector === 'nav[aria-label="Primary"]' ? nav : selector === "main" ? main : null,
    cookie: "", readyState: "complete", visibilityState: "visible",
  });
  const fetch = async (url, init) => {
    if (url.pathname.endsWith("reader-endpoints.json")) return json(200, {
      staging: "https://reader.example", production: "https://prod.example", pagesHost: "pages.example",
    });
    requests.push(url.pathname);
    assert.equal(init.credentials, "omit");
    assert.equal(init.mode, "cors");
    assert.equal(init.redirect, "error");
    assert.equal(init.headers, undefined);
    return reply(url.pathname, init);
  };
  function storage() {
    const map = new Map();
    return {getItem: k => map.get(k), setItem: (k, v) => map.set(k, v), removeItem: k => map.delete(k)};
  }
  const window = Object.assign(new EventTarget(), {TextEncoder, crypto: webcrypto, sessionStorage: storage(),
    localStorage: storage(), fetch});
  vm.runInNewContext(script, {document, window, location, navigator: {}, URL, fetch, TextEncoder, Uint8Array,
    AbortController, setTimeout: setImmediate, clearTimeout: clearImmediate});
  await tick();
  const link = nav.children.find(child => child.className === "reader-sign-in");
  return {forms, requests, window, ids, click() {
    link.dispatchEvent(Object.assign(new Event("click", {cancelable: true}), {button: 0}));
  }};
}

async function until(check) {
  for (let i = 0; i < 1000; i++) {
    if (check()) return;
    await tick();
  }
  assert.fail("Expected sign-in transition did not complete");
}

test("cold HTML and network failures keep the user on Pages until the chosen Reader confirms readiness", async () => {
  let ready = false;
  const p = await page((path) => {
    if (path.endsWith("/identity")) throw new Error("CORS/network");
    return ready ? json(200, {ready:true, environment:"staging"}) : new Response("<html>Starting</html>");
  });
  p.click(); p.click();
  p.window.dispatchEvent(new Event("pageshow"));
  p.click();
  assert.equal(p.forms.length, 0);
  assert.match(p.ids.get("reader-sign-in-status").textContent, /Starting/);
  ready = true;
  await until(() => p.forms.length > 0);
  assert.equal(p.forms.length, 1);
  assert.equal(p.forms[0].action, "https://reader.example/pages/login");
  assert.equal(p.forms[0].method, "post");
  assert.equal(p.forms[0].children.find(e => e.name === "page").value, "/staging/book/");
});

test("wrong environment times out without downgrading, then a deliberate retry can succeed", async () => {
  let env = "production";
  const p = await page(() => json(200, {ready: true, environment: env}));
  p.click();
  await until(() => /retry/.test(p.ids.get("reader-sign-in-status").textContent));
  assert.equal(p.forms.length, 0);
  assert.equal(p.requests.length, 12);
  assert.ok(p.requests.every(path => path === "/api/pages/ready"));
  env = "staging";
  p.click();
  await until(() => p.forms.length === 1);
});

test("only an exact signed-out JSON reply identifies a warm legacy deployment", async () => {
  let legacy = {unexpected: true};
  const p = await page(path => path.endsWith("/identity") ? json(401, legacy) : new Response("Missing", {status:404}));
  p.click();
  await until(() => /retry/.test(p.ids.get("reader-sign-in-status").textContent));
  assert.equal(p.forms.length, 0);
  legacy = {};
  p.click();
  await until(() => p.forms.length === 1);
});
