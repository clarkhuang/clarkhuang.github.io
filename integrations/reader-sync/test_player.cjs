// Run with node --test test_player.cjs.
const {test} = require("node:test");
const assert = require("node:assert/strict");
const {readFileSync} = require("node:fs");
const {join} = require("node:path");
const vm = require("node:vm");

const playerCode = readFileSync(join(__dirname, "static", "reader-player.js"), "utf8");

function fixture(send) {
  const media = new EventTarget();
  Object.assign(media, {readyState: 1, duration: 60, currentTime: 0, ended: false});
  const status = {dataset: {key: "test", revision: "1", position: "8", completed: "false", duration: "60"}};
  const button = new EventTarget();
  const document = new EventTarget();
  document.getElementById = id => ({player: media, checkpoint: status, save: button})[id];
  vm.runInNewContext(playerCode, {document, Date, fetch: (url, opts) => send(JSON.parse(opts.body))});
  return {media, status, button};
}

const flush = () => new Promise(resolve => setImmediate(resolve));
const success = revision => ({ok: true, status: 200, json: async () => ({revision})});

test("restore, serialize overlapping saves and keep the latest position", async () => {
  const writes = [];
  let finish;
  const {media} = fixture(body => {
    writes.push(body);
    if (writes.length === 1) return new Promise(resolve => { finish = resolve; });
    return Promise.resolve(success(3));
  });
  assert.equal(media.currentTime, 8);
  media.currentTime = 19;
  media.dispatchEvent(new Event("pause"));
  media.currentTime = 60;
  media.ended = true;
  media.dispatchEvent(new Event("ended"));
  assert.equal(writes.length, 1);
  finish(success(2));
  await flush();
  assert.deepEqual(writes.map(w => [w.revision, w.position, w.completed]), [[1, 19, false], [2, 60, true]]);
});

test("conflicting device updates stop autosave and leave a visible recovery action", async () => {
  let writes = 0;
  const {media, status, button} = fixture(async () => { writes++; return {status: 409}; });
  media.currentTime = 20;
  media.dispatchEvent(new Event("pause"));
  await flush();
  media.currentTime = 31;
  media.dispatchEvent(new Event("pause"));
  assert.equal(writes, 1);
  assert.equal(button.disabled, true);
  assert.match(status.textContent, /another device/);
});
