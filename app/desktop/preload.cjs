// Bridge for the page (plan 54, SW-2): window.triviaShell, nothing else (decision 130).
const { contextBridge, ipcRenderer } = require("electron");

contextBridge.exposeInMainWorld("triviaShell", {
  desktop: true,
  isFullscreen: () => ipcRenderer.invoke("trivia:fullscreen"),
  setFullscreen: (yes) => ipcRenderer.invoke("trivia:set-fullscreen", yes),
  onFullscreen: (cb) => {
    const on = (_e, yes) => cb(yes === true);
    ipcRenderer.on("trivia:fullscreen", on);
    return () => ipcRenderer.removeListener("trivia:fullscreen", on);
  },
  quit: () => ipcRenderer.invoke("trivia:quit"),
  loadSave: () => ipcRenderer.invoke("save:load"),
  writeSave: (text) => ipcRenderer.invoke("save:write", text),
  backupSave: (kind) => ipcRenderer.invoke("save:backup", kind),
  // Plan 151: the machine's locale country, "" for none.
  region: process.argv.find((a) => a.startsWith("--trivia-region="))?.slice("--trivia-region=".length) ?? "",
  // Plans 114, 118: mod list, mods.json writes, notice, restart, start confirmed.
  mods: {
    list: () => ipcRenderer.invoke("mods:list"),
    set: (order) => ipcRenderer.invoke("mods:set", order),
    notice: () => ipcRenderer.invoke("mods:notice"),
    restart: () => ipcRenderer.invoke("mods:restart"),
    ready: () => ipcRenderer.invoke("mods:ready"),
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
