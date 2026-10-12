// Electron shell (plan 54, D-63): plays app/client/dist over app://trivia/, no Python, no network.
import { app, BrowserWindow, dialog, Menu, protocol, session } from "electron";
import { existsSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { makeResolver } from "./resolve.mjs";

const ORIGIN = "app://trivia/";
const BACKGROUND = "#0b1120"; // --night-900

function roots() {
  if (app.isPackaged) {
    const res = process.resourcesPath;
    return {
      dist: path.join(res, "client", "dist"),
      data: path.join(res, "data"),
      media: process.env.TRIVIA_MEDIA || path.join(app.getPath("userData"), "media"),
    };
  }
  const repo = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..", "..");
  return {
    dist: path.join(repo, "app", "client", "dist"),
    data: path.join(repo, "app", "data"),
    media: process.env.TRIVIA_MEDIA || path.join(repo, "media"),
  };
}

protocol.registerSchemesAsPrivileged([
  { scheme: "app", privileges: { standard: true, secure: true, supportFetchAPI: true, stream: true } },
]);
app.commandLine.appendSwitch("autoplay-policy", "no-user-gesture-required");
Menu.setApplicationMenu(null);

let win = null;

if (!app.requestSingleInstanceLock()) {
  app.quit();
} else {
  app.on("second-instance", () => {
    if (!win) return;
    if (win.isMinimized()) win.restore();
    win.focus();
  });
  app.on("window-all-closed", () => app.quit());
  app.whenReady().then(start);
}

function start() {
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

  win.loadURL(ORIGIN);
}
