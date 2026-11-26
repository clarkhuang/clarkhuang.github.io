const test = require("node:test");
const assert = require("node:assert/strict");
const {parseDraft} = require("./static/profile.js");
const fields = ["goal", "hardware", "format"];

test("plain and fenced JSON accept only known nonempty text", () => {
  assert.deepEqual(parseDraft('{"goal":"  build a site  ","hardware":null,"format":"  ","other":"private"}', fields),
                   {goal: "build a site"});
  assert.deepEqual(parseDraft('```json\n{"hardware":"Linux laptop"}\n```', fields), {hardware: "Linux laptop"});
  assert.deepEqual(parseDraft('{"__proto__":{"secret":"ignored"},"format":"transcript"}', fields), {format:"transcript"});
});

test("invalid drafts reject the whole object without echoing its contents", () => {
  for (const text of ["", "[]", "false", "null", "{}", '{"hardware":""}', '{"x":42}',
                       '{"hardware":"ok","goal":{"secret":"teststring"}}',
                       JSON.stringify({goal: "teststring".repeat(35)}),
                       JSON.stringify({format: "teststring\nnext line"}),
                       "teststring".repeat(1000)]) {
    assert.throws(() => parseDraft(text, fields), e => !e.message.includes("teststring"));
  }
});
