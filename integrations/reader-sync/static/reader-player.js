"use strict";
(() => {
  const player = document.getElementById("player");
  const status = document.getElementById("checkpoint");
  const saveButton = document.getElementById("save");
  const key = status.dataset.key;
  const duration = Number(status.dataset.duration);
  let revision = Number(status.dataset.revision);
  let completed = status.dataset.completed === "true";
  let savedPosition = Number(status.dataset.position);
  let busy = false;
  let queued = false;
  let blocked = false;
  let lastAttempt = 0;
  let ready = false;

  function restore() {
    if (ready) return;
    if (!completed && savedPosition > 0) player.currentTime = Math.min(savedPosition, player.duration);
    ready = true;
    status.textContent = completed ? "Completed" : savedPosition ? "Resumed from your saved position." : "";
  }
  if (player.readyState >= 1) restore();
  else player.addEventListener("loadedmetadata", restore, {once: true});

  async function save() {
    if (!ready || blocked) return;
    if (busy) { queued = true; return; }
    const position = Math.min(duration, Math.round(player.currentTime * 10) / 10);
    const done = completed || player.ended;
    if (position === savedPosition && done === completed) return;
    busy = true;
    lastAttempt = Date.now();
    try {
      const response = await fetch("/api/progress", {
        method: "PUT", headers: {"Content-Type": "application/json"}, keepalive: true,
        body: JSON.stringify({item: key, revision, position, completed: done})
      });
      if (response.status === 409 || response.status === 401) {
        blocked = true;
        saveButton.disabled = true;
        status.textContent = response.status === 409
          ? "Progress changed on another device. Reload to use its saved position."
          : "Your session expired. Reload to sign in and resume.";
        return;
      }
      if (!response.ok) throw new Error("Save failed");
      revision = (await response.json()).revision;
      savedPosition = position;
      completed = done;
      status.textContent = done ? "Completed and saved." : "Position saved.";
    } catch {
      status.textContent = "Could not confirm the save. Select Save position to retry.";
    } finally {
      busy = false;
      if (queued) { queued = false; void save(); }
    }
  }
  saveButton.addEventListener("click", save);
  ["pause", "ended", "seeked"].forEach(name => player.addEventListener(name, save));
  player.addEventListener("timeupdate", () => {
    if (Date.now() - lastAttempt >= 10000) void save();
  });
  document.addEventListener("visibilitychange", () => {
    if (document.visibilityState === "hidden") void save();
  });
})();
