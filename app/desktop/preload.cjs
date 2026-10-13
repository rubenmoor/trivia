// Bridge for the page (plan 54, SW-2): window.trivia, nothing else.
const { contextBridge, ipcRenderer } = require("electron");

contextBridge.exposeInMainWorld("trivia", {
  desktop: true,
  toggleFullscreen: () => ipcRenderer.invoke("trivia:toggle-fullscreen"),
  quit: () => ipcRenderer.invoke("trivia:quit"),
  loadSave: () => ipcRenderer.invoke("save:load"),
  writeSave: (text) => ipcRenderer.invoke("save:write", text),
  backupSave: (kind) => ipcRenderer.invoke("save:backup", kind),
  localSave: () => ipcRenderer.invoke("save:local-offer"),
  adoptLocalSave: () => ipcRenderer.invoke("save:adopt-local"),
  // Plan 85: the binding lives in main; the flag comes from main's additionalArguments.
  steam: {
    available: process.argv.includes("--trivia-steam"),
    steamId: () => ipcRenderer.invoke("steam:steam-id"),
    language: () => ipcRenderer.invoke("steam:language"),
    overlay: { enabled: () => ipcRenderer.invoke("steam:overlay-enabled") },
    showTextInput: (rect, current) => ipcRenderer.invoke("steam:show-text-input", rect, current),
    inputTypes: () => ipcRenderer.invoke("steam:input-types"),
    setPresence: (key, values) => ipcRenderer.invoke("steam:set-presence", key, values),
    unlock: (id) => ipcRenderer.invoke("steam:unlock", id),
  },
});
