// Electron shell (plan 54, D-63): plays app/client/dist over app://trivia/, no Python, no network.
import { app, BrowserWindow, dialog, ipcMain, Menu, protocol, session } from "electron";
import { existsSync } from "node:fs";
import { readFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { makeResolver } from "./resolve.mjs";
import { makeSaveFile } from "./save.mjs";

const ORIGIN = "app://trivia/";
const BACKGROUND = "#0b1120"; // --night-900

const REPO = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..", "..");

function roots() {
  if (app.isPackaged) {
    const res = process.resourcesPath;
    return {
      dist: path.join(res, "client", "dist"),
      data: path.join(res, "data"),
      media: process.env.TRIVIA_MEDIA || path.join(app.getPath("userData"), "media"),
    };
  }
  return {
    dist: path.join(REPO, "app", "client", "dist"),
    data: path.join(REPO, "app", "data"),
    media: process.env.TRIVIA_MEDIA || path.join(REPO, "media"),
  };
}

function saveDir() {
  if (process.env.TRIVIA_SAVE_DIR) return process.env.TRIVIA_SAVE_DIR;
  return app.isPackaged ? path.join(app.getPath("userData"), "save") : path.join(REPO, "state", "desktop");
}

/** `--import-save <file>` from argv, or null. */
function importArg() {
  const i = process.argv.indexOf("--import-save");
  return i >= 0 ? process.argv[i + 1] ?? null : null;
}

protocol.registerSchemesAsPrivileged([
  { scheme: "app", privileges: { standard: true, secure: true, supportFetchAPI: true, stream: true } },
]);
app.commandLine.appendSwitch("autoplay-policy", "no-user-gesture-required");
Menu.setApplicationMenu(null);
// Fixed folder, independent of the product name (plan 55); before ready and the instance lock.
if (app.isPackaged) app.setPath("userData", path.join(app.getPath("appData"), "trivia"));

let win = null;
const saveFile = makeSaveFile(saveDir());
let writing = Promise.resolve();
let pending = 0;

/** One save operation at a time, in order. */
function queued(fn) {
  pending++;
  const p = writing.then(fn).finally(() => pending--);
  writing = p.catch(() => {});
  return p;
}

if (!app.requestSingleInstanceLock()) {
  app.quit();
} else {
  app.on("second-instance", () => {
    if (!win) return;
    if (win.isMinimized()) win.restore();
    win.focus();
  });
  app.on("window-all-closed", () => app.quit());
  app.on("before-quit", (event) => {
    if (!pending) return;
    event.preventDefault();
    writing.then(() => app.quit());
  });
  app.whenReady().then(start);
}

async function importSave(file) {
  if ((await saveFile.read()) !== null) {
    console.error(`trivia: --import-save: ${saveFile.file} exists, not overwritten`);
    return;
  }
  try {
    await saveFile.write(await readFile(file, "utf8"));
    console.error(`trivia: imported ${file} → ${saveFile.file}`);
  } catch (err) {
    console.error(`trivia: --import-save ${file}: ${err.message}`);
  }
}

async function start() {
  await saveFile.dropStaleTemp();
  const importFrom = importArg();
  if (importFrom) await importSave(importFrom);

  const dirs = roots();
  if (!existsSync(path.join(dirs.dist, "index.html"))) {
    dialog.showErrorBox("¡Trivia!", "client not built: run `npm run build -w app/client`");
    app.quit();
    return;
  }

  const ses = session.defaultSession;
  ses.protocol.handle("app", makeResolver(dirs));
  ses.webRequest.onBeforeRequest(
    { urls: ["http://*/*", "https://*/*", "ws://*/*", "wss://*/*"] },
    (_details, callback) => callback({ cancel: true }),
  );
  ses.setPermissionRequestHandler((_wc, permission, callback) => callback(permission === "fullscreen"));
  ses.setPermissionCheckHandler((_wc, permission) => permission === "fullscreen");

  win = new BrowserWindow({
    fullscreen: true,
    show: false,
    backgroundColor: BACKGROUND,
    title: "¡Trivia!",
    webPreferences: {
      contextIsolation: true,
      sandbox: true,
      nodeIntegration: false,
      preload: path.join(path.dirname(fileURLToPath(import.meta.url)), "preload.cjs"),
      devTools: process.env.TRIVIA_DEVTOOLS === "1",
    },
  });
  win.once("ready-to-show", () => win.show());
  win.on("closed", () => (win = null));

  const wc = win.webContents;
  wc.on("will-navigate", (event, url) => {
    if (!url.startsWith(ORIGIN)) event.preventDefault();
  });
  wc.setWindowOpenHandler(() => ({ action: "deny" }));
  wc.on("before-input-event", (event, input) => {
    if (input.type === "keyDown" && input.key === "F11") {
      event.preventDefault();
      win.setFullScreen(!win.isFullScreen());
    }
  });

  bridge();
  win.loadURL(ORIGIN);
}

/** IPC for preload.cjs; only our own page may call. */
function bridge() {
  const handle = (channel, fn) =>
    ipcMain.handle(channel, (event, ...args) => {
      if (!event.senderFrame?.url.startsWith(ORIGIN)) throw new Error("forbidden");
      return fn(...args);
    });
  handle("trivia:toggle-fullscreen", () => win?.setFullScreen(!win.isFullScreen()));
  handle("trivia:quit", () => app.quit());
  // Rejections carry the code as the message: bad_save, save_locked.
  handle("save:load", () => queued(() => saveFile.read()));
  handle("save:write", (text) => queued(() => saveFile.write(text)));
  handle("save:backup", (kind) => queued(() => saveFile.backup(kind)));
}
