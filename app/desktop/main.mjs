// Electron shell (plan 54, D-63): plays app/client/dist over app://trivia/, no Python, no network.
import { app, BrowserWindow, dialog, ipcMain, Menu, protocol, session } from "electron";
import { existsSync } from "node:fs";
import { readFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { makeResolver } from "./resolve.mjs";
import { makeSaveFile, migrateToLocal } from "./save.mjs";

const ORIGIN = "app://trivia/";
const BACKGROUND = "#0b1120"; // --night-900

const REPO = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..", "..");
const STEAM_APP_ID = 480; // Spacewar until the real App ID (plan 85)

function roots() {
  if (app.isPackaged) {
    // Layout from electron-builder.yml (plan 56).
    const res = process.resourcesPath;
    return {
      dist: path.join(res, "client"),
      data: path.join(res, "data"),
      media: process.env.TRIVIA_MEDIA || path.join(res, "media"),
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

/** One folder per Steam user, `local/` without Steam (plan 87); `TRIVIA_SAVE_DIR` is the folder itself. */
async function userSaveDir() {
  const base = saveDir();
  if (process.env.TRIVIA_SAVE_DIR) return base;
  await migrateToLocal(base);
  const id = steam ? String(steam.getStatus().steamId) : "";
  return path.join(base, /^[1-9]\d*$/.test(id) ? id : "local");
}

/** Folder holding `redistributable_bin/` (Valve licence, not in git); dev falls back to the flake's. */
function steamSdkDir() {
  if (app.isPackaged) return path.join(process.resourcesPath, "steamworks_sdk");
  const local = path.join(REPO, "app", "desktop", "steamworks_sdk");
  return existsSync(path.join(local, "redistributable_bin")) ? local : process.env.TRIVIA_STEAM_SDK || local;
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
let steam = null; // the binding, only while Steam is up
let steamTimer = null;
let steamInput = false;
let overlay = false; // Windows only: the native window Steam's overlay draws into (D-92)
let saveFile = null; // set in start(), after Steam
let localFile = null; // `local/`'s save under Steam: offered once (plan 87)
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
  app.on("will-quit", stopSteam);
  app.whenReady().then(start);
}

/** Optional: any failure leaves `steam` null with one stderr line. No restart through Steam, no DRM. */
async function startSteam() {
  // A Steam launch sets SteamAppId; dev may override the constant.
  const appId = Number(process.env.SteamAppId || process.env.TRIVIA_STEAM_APPID || STEAM_APP_ID);
  const { log, warn, error } = console;
  let reason = null;
  try {
    const { SteamworksSDK } = await import("steamworks-ffi-node");
    const s = SteamworksSDK.getInstance();
    s.setSdkPath(steamSdkDir());
    // The binding logs several lines per failure; keep its first error only.
    console.log = console.warn = () => {};
    console.error = (...args) => {
      reason ??= args.join(" ").replace("[Steamworks] ", "").split("\n")[0];
    };
    if (!s.init({ appId })) throw new Error(reason ?? "init failed");
    steam = s;
  } catch (err) {
    Object.assign(console, { log, warn, error });
    console.error(`trivia: steam unavailable: ${err.message}`);
    return;
  }
  Object.assign(console, { log, warn, error });
  // Steam Input for the pads' real types only (glyphs); runCallbacks drives its frames.
  steamInput = steam.input.init(false);
  steamTimer = setInterval(() => steam.runCallbacks(), 100);
  console.error(
    `trivia: steam available, app ${appId}, user ${steam.getStatus().steamId}, language ${steam.apps.getCurrentGameLanguage()}`,
  );
}

function stopSteam() {
  if (!steam) return;
  clearInterval(steamTimer);
  if (steamInput) steam.input.shutdown();
  steamInput = false;
  steam.richPresence.clearRichPresence();
  steam.shutdown();
  steam = null;
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
  await startSteam();
  const dir = await userSaveDir();
  saveFile = makeSaveFile(dir);
  if (path.basename(dir) !== "local" && !process.env.TRIVIA_SAVE_DIR)
    localFile = makeSaveFile(path.join(path.dirname(dir), "local"));
  console.error(`trivia: save ${saveFile.file}`);
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
      additionalArguments: steam ? ["--trivia-steam"] : [],
    },
  });
  win.once("ready-to-show", () => win.show());
  // After the load: a frame subscription made before it gets no frames.
  if (steam && process.platform === "win32")
    win.webContents.once("did-finish-load", () => {
      overlay = steam.addElectronSteamOverlay(win, { title: "¡Trivia!" });
    });
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
  // First Steam start (plan 87): `local/`'s text while this user has no save; adopt copies it, `local/` stays.
  const localOffer = async () => (localFile && (await saveFile.read()) === null ? localFile.read() : null);
  handle("save:local-offer", () => queued(localOffer));
  handle("save:adopt-local", () =>
    queued(async () => {
      const text = await localOffer();
      if (text === null) throw new Error("no_local_save");
      await saveFile.write(text);
      return text;
    }),
  );
  // Steam (plan 85): pass-throughs; null/false without Steam. Stubs filled by later tasks.
  handle("steam:steam-id", () => steam?.getStatus().steamId ?? null);
  handle("steam:language", () => steam?.apps.getCurrentGameLanguage() ?? null);
  handle("steam:unlock", (id) =>
    steam && typeof id === "string" ? steam.achievements.unlockAchievement(id) : false,
  );
  handle("steam:overlay-enabled", () => overlay && steam?.utils.isOverlayEnabled() === true);
  // Floating keyboard types into the focused field; Steam shows it only in Big Picture or on the Deck.
  handle("steam:show-text-input", (rect) => {
    if (!steam || !(steam.utils.isSteamInBigPictureMode() || steam.utils.isSteamRunningOnSteamDeck())) return false;
    const px = (v) => Math.round(Number(v) || 0);
    // 0: EFloatingGamepadTextInputMode.SingleLine
    return steam.utils.showFloatingGamepadTextInput(0, px(rect?.x), px(rect?.y), px(rect?.width), px(rect?.height));
  });
  // SteamInputType: PS4 5, PS3 12, PS5 13; everything else gets Xbox glyphs.
  handle("steam:input-types", () =>
    steamInput
      ? steam.input
          .getConnectedControllers()
          .map((h) => ([5, 12, 13].includes(steam.input.getInputTypeForHandle(h)) ? "playstation" : "xbox"))
      : null,
  );
  // Rich presence: values first, then the steam_display token; "" clears. Tokens: steam-presence.vdf.
  handle("steam:set-presence", (key, values) => {
    if (!steam) return;
    if (!key || typeof key !== "string") return steam.richPresence.clearRichPresence();
    for (const [k, v] of Object.entries(values ?? {})) steam.richPresence.setRichPresence(k, String(v));
    steam.richPresence.setRichPresence("steam_display", key);
  });
}
