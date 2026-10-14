// Bridge for the page (plan 54, SW-2): window.triviaShell, nothing else (decision 130).
const { contextBridge, ipcRenderer } = require("electron");

contextBridge.exposeInMainWorld("triviaShell", {
  desktop: true,
  toggleFullscreen: () => ipcRenderer.invoke("trivia:toggle-fullscreen"),
  quit: () => ipcRenderer.invoke("trivia:quit"),
  loadSave: () => ipcRenderer.invoke("save:load"),
  writeSave: (text) => ipcRenderer.invoke("save:write", text),
  backupSave: (kind) => ipcRenderer.invoke("save:backup", kind),
  // Plan 114: mod list and mods.json writes.
  mods: {
    list: () => ipcRenderer.invoke("mods:list"),
    set: (order) => ipcRenderer.invoke("mods:set", order),
  },
  // Plan 106: consent and this run's session buffer.
  telemetry: {
    state: () => ipcRenderer.invoke("telemetry:state"),
    setConsent: (yes) => ipcRenderer.invoke("telemetry:consent", yes),
    load: () => ipcRenderer.invoke("telemetry:load"),
    record: (buffer) => ipcRenderer.invoke("telemetry:record", buffer),
  },
  // Plan 93: main holds the URL and the ticket; the page passes fields.
  report: {
    available: () => ipcRenderer.invoke("report:available"),
    send: (fields) => ipcRenderer.invoke("report:send", fields),
  },
  // Plan 85: the binding lives in main; the flag comes from main's additionalArguments.
  steam: {
    available: process.argv.includes("--trivia-steam"),
    user: process.argv.includes("--trivia-user"),
    dev: process.argv.includes("--trivia-dev"),
    steamId: () => ipcRenderer.invoke("steam:steam-id"),
    language: () => ipcRenderer.invoke("steam:language"),
    overlay: { enabled: () => ipcRenderer.invoke("steam:overlay-enabled") },
    showTextInput: (rect, current) => ipcRenderer.invoke("steam:show-text-input", rect, current),
    inputTypes: () => ipcRenderer.invoke("steam:input-types"),
    setPresence: (key, values) => ipcRenderer.invoke("steam:set-presence", key, values),
    unlock: (id) => ipcRenderer.invoke("steam:unlock", id),
  },
});
