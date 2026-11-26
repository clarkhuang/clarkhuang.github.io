/* Draft locally; the reader chooses when to send the edited form. */
(function () {
  "use strict";

  function parseDraft(text, allowed) {
    if (!text.trim()) throw new Error("Paste your assistant’s JSON reply first.");
    if (text.length > 8192) throw new Error("Paste only the profile JSON (up to 8,192 characters).");
    let source = text.trim();
    const fenced = source.match(/^```(?:json)?\s*\n([\s\S]*?)\n\s*```$/i);
    if (fenced) source = fenced[1];
    let parsed;
    try { parsed = JSON.parse(source); }
    catch (_) { throw new Error("Use one JSON object. You can ask your assistant to resend just the JSON."); }
    if (!parsed || Array.isArray(parsed) || typeof parsed !== "object") {
      throw new Error("Paste a JSON object with goal, hardware or format.");
    }

    const draft = {};
    for (const key of allowed) {
      if (!Object.prototype.hasOwnProperty.call(parsed, key) || parsed[key] === null) continue;
      const value = parsed[key];
      if (typeof value !== "string") throw new Error("Use plain text for " + key + ".");
      const trimmed = value.trim();
      if (!trimmed) continue;
      if (trimmed.length > 240 || /[\x00-\x1f\x7f]/.test(trimmed)) {
        throw new Error("Keep " + key + " to one line of 240 characters or fewer.");
      }
      draft[key] = trimmed;
    }
    if (Object.keys(draft).length === 0) {
      throw new Error("The reply needs at least one nonempty goal, hardware or format entry.");
    }
    return draft;
  }

  if (typeof module !== "undefined" && module.exports) {
    module.exports = {parseDraft};
    return;
  }

  const form = document.getElementById("learning-profile");
  if (!form) return;
  const fields = Array.from(form.querySelectorAll("input[name]"));
  const keys = fields.map(input => input.name);
  const prompt = document.getElementById("profile-prompt");
  const copy = document.getElementById("profile-copy");
  const copyStatus = document.getElementById("profile-copy-status");
  const paste = document.getElementById("profile-json");
  const status = document.getElementById("profile-import-status");
  copy.hidden = false;
  document.getElementById("profile-import-controls").hidden = false;

  copy.addEventListener("click", async function () {
    try {
      await navigator.clipboard.writeText(prompt.value);
      copyStatus.textContent = "Prompt copied.";
    } catch (_) {
      prompt.focus();
      prompt.select();
      copyStatus.textContent = "Prompt selected. Use your device’s Copy command.";
    }
  });

  document.getElementById("profile-import").addEventListener("click", function () {
    let draft;
    try { draft = parseDraft(paste.value, keys); }
    catch (error) {
      paste.setAttribute("aria-invalid", "true");
      status.textContent = error.message;
      paste.focus();
      return;
    }
    paste.removeAttribute("aria-invalid");
    for (const input of fields) {
      if (Object.prototype.hasOwnProperty.call(draft, input.name)) input.value = draft[input.name];
    }
    status.textContent = "Draft applied. Review the fields below and select Save profile to keep your changes.";
    const first = fields.find(input => Object.prototype.hasOwnProperty.call(draft, input.name));
    first.focus();
  });
}());
