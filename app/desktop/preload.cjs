// Bridge for the page (plan 54, SW-2): window.trivia, nothing else.
const { contextBridge, ipcRenderer } = require("electron");

contextBridge.exposeInMainWorld("trivia", {
  desktop: true,
  toggleFullscreen: () => ipcRenderer.invoke("trivia:toggle-fullscreen"),
  quit: () => ipcRenderer.invoke("trivia:quit"),
  loadSave: () => ipcRenderer.invoke("save:load"),
  writeSave: (text) => ipcRenderer.invoke("save:write", text),
  backupSave: (kind) => ipcRenderer.invoke("save:backup", kind),
});
