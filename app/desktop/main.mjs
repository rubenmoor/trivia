// Electron shell (plan 54, D-63): plays app/client/dist over app://trivia/, no Python, no network.
import { app, BrowserWindow, dialog, ipcMain, Menu, protocol, session } from "electron";
import { existsSync, mkdirSync } from "node:fs";
import { readFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { arrange, discover, ID as MOD_ID, readSettings, writeSettings } from "./mods.mjs";
import { makeResolver } from "./resolve.mjs";
import { makeSaveFile } from "./save.mjs";
import { fakeUgc, workshopItems } from "./workshop.mjs";

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

/** Local mods (plan 112): `TRIVIA_MODS_DIR`, packaged `<userData>/mods/` (created), dev `REPO/mods/`. */
function modsDir() {
  if (process.env.TRIVIA_MODS_DIR) return process.env.TRIVIA_MODS_DIR;
  if (!app.isPackaged) return path.join(REPO, "mods");
  const dir = path.join(app.getPath("userData"), "mods");
  mkdirSync(dir, { recursive: true });
  return dir;
}

/** Per machine, not in the save (decision 136). */
function modsSettingsFile() {
  return app.isPackaged ? path.join(app.getPath("userData"), "mods.json") : path.join(REPO, "state", "desktop", "mods.json");
}

/** Valid user's folder (plan 87, decision 114): `<steamid64>/`, `dev/` under the dev switch; `TRIVIA_SAVE_DIR` as is. */
function userSaveDir() {
  if (process.env.TRIVIA_SAVE_DIR) return process.env.TRIVIA_SAVE_DIR;
  return path.join(saveDir(), hasSteamId() ? String(steam.getStatus().steamId) : "dev");
}

/** Folder holding `redistributable_bin/` (Valve licence, not in git); dev falls back to the flake's. */
function steamSdkDir() {
  if (app.isPackaged) return path.join(process.resourcesPath, "steamworks_sdk");
  const local = path.join(REPO, "app", "desktop", "steamworks_sdk");
  return existsSync(path.join(local, "redistributable_bin")) ? local : process.env.TRIVIA_STEAM_SDK || local;
}

const USAGE = "known flags: --import-save <file>, --no-mods";
// Our flags' namespace; anything else (Electron/Chromium switches, the dev app path, Steam's) passes.
const OWN = /^--(import|export|save|trivia|no-mods)/;

/** Our flags from argv: `{ importSave, noMods }`, or `{ error }` for an unknown own-looking flag or a missing value. */
function parseArgs(argv) {
  let importSave = null;
  let noMods = false;
  for (let i = 1; i < argv.length; i++) {
    const [flag, inline] = argv[i].split(/=(.*)/s);
    if (!OWN.test(flag)) continue;
    if (flag === "--no-mods" && inline === undefined) {
      noMods = true;
      continue;
    }
    if (flag !== "--import-save") return { error: `unknown flag ${flag}; ${USAGE}` };
    const value = inline ?? argv[++i];
    if (!value || value.startsWith("--")) return { error: `--import-save needs a file; ${USAGE}` };
    importSave = value;
  }
  return { importSave, noMods };
}

const args = parseArgs(process.argv);

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
let validUser = false; // decision 111: Steam user with a SteamID, or the dev switch; fixed for the session
let overlay = false; // Windows only: the native window Steam's overlay draws into (D-92)
let activeDirs = new Set(); // this run's overlay layers (plan 112): fixed until restart
let saveFile = null; // set in start(), after Steam; stays null without a valid user
let writing = Promise.resolve();
let pending = 0;

/** One save operation at a time, in order. */
function queued(fn) {
  pending++;
  const p = writing.then(fn).finally(() => pending--);
  writing = p.catch(() => {});
  return p;
}

if (args.error) {
  console.error(`trivia: ${args.error}`);
  // No console on Windows: a dialog too when packaged.
  if (app.isPackaged)
    app.whenReady().then(() => {
      dialog.showErrorBox("¡Trivia!", args.error);
      app.exit(2);
    });
  else app.exit(2);
} else if (!app.requestSingleInstanceLock()) {
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
  app.whenReady()
    .then(start)
    .catch((err) => {
      dialog.showErrorBox("¡Trivia!", err.stack ?? String(err));
      app.quit();
    });
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
    `trivia: steam available, app ${appId}, user ${steam.getStatus().steamId} ${hasSteamId() ? "valid" : "none"}, language ${steam.apps.getCurrentGameLanguage()}`,
  );
}

function hasSteamId() {
  return steam !== null && /^[1-9]\d*$/.test(String(steam.getStatus().steamId));
}

/** Soft check, no DRM (decision 111); `TRIVIA_DEV_STEAM_USER=1` stands in for a user, packaged too. */
function checkUser() {
  if (hasSteamId()) return true;
  if (process.env.TRIVIA_DEV_STEAM_USER !== "1") return false;
  console.error("trivia: dev Steam user (TRIVIA_DEV_STEAM_USER)");
  return true;
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
  validUser = checkUser();
  if (validUser) {
    saveFile = makeSaveFile(userSaveDir());
    console.error(`trivia: save ${saveFile.file}`);
    await saveFile.dropStaleTemp();
  } else console.error("trivia: no Steam user, progress not saved");
  if (args.importSave) {
    if (!saveFile) {
      console.error("trivia: --import-save needs a Steam user (or TRIVIA_DEV_STEAM_USER=1)");
      app.exit(1);
      return;
    }
    await importSave(args.importSave);
  }

  const dirs = roots();
  if (!existsSync(path.join(dirs.dist, "index.html"))) {
    dialog.showErrorBox("¡Trivia!", "client not built: run `npm run build -w app/client`");
    app.quit();
    return;
  }

  const layers = await loadMods();

  const ses = session.defaultSession;
  ses.protocol.handle("app", makeResolver({ ...dirs, layers }));
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
      additionalArguments: [
        ...(steam ? ["--trivia-steam"] : []),
        ...(validUser ? ["--trivia-user"] : []),
        ...(validUser && !hasSteamId() ? ["--trivia-dev"] : []),
      ],
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
    if (input.type === "keyDown" && input.key === "F11" && !input.isAutoRepeat) {
      event.preventDefault();
      win.setFullScreen(!win.isFullScreen());
    }
  });

  bridge();
  win.loadURL(ORIGIN);
}

/** Discovery, mods.json, load order → overlay layers, fixed for the run; none with --no-mods. */
async function loadMods() {
  const file = modsSettingsFile();
  const arranged = await arrangeMods(true);
  if (arranged.changed)
    await writeSettings(file, arranged.settings).catch((err) => console.error(`trivia: mods: ${file}: ${err.message}`));
  const mods = arranged.list;
  for (const mod of mods)
    if (mod.source === "workshop")
      console.error(`trivia: mod ${mod.id ?? "?"} workshop ${mod.publishedFileId} ${mod.dir ? "installed" : mod.state}`);
  if (args.noMods) {
    console.error("trivia: --no-mods: no mods this run");
    return [];
  }
  const count = {};
  for (const mod of mods) {
    count[mod.state] = (count[mod.state] ?? 0) + 1;
    const notes = [...(mod.error ? [mod.error.code] : []), ...(mod.warnings ?? []).map((w) => w.code)];
    console.error(`trivia: mod ${mod.id ?? mod.dir ?? mod.publishedFileId} ${mod.state}${notes.length ? ` [${notes.join(", ")}]` : ""}`);
  }
  if (mods.length)
    console.error(`trivia: mods: ${Object.entries(count).map(([state, n]) => `${n} ${state}`).join(", ")}`);
  activeDirs = new Set(arranged.layers);
  return arranged.layers;
}

/** Fresh discovery (local + Workshop re-query) arranged against mods.json; at start and per `mods:list`. */
async function arrangeMods(log = false) {
  const found = await discover({ local: modsDir(), workshop: workshopSource(log) }, app.getVersion());
  return arrange(found, await readSettings(modsSettingsFile()), { validUser });
}

/** Subscribed items (plan 114): real user only (decision 111); dev switch + `TRIVIA_DEV_WORKSHOP_DIR`: a fake folder. */
function workshopSource(log) {
  try {
    if (hasSteamId()) return workshopItems(steam.workshop);
    const dir = process.env.TRIVIA_DEV_WORKSHOP_DIR;
    if (!dir || process.env.TRIVIA_DEV_STEAM_USER !== "1") return [];
    if (log) console.error(`trivia: dev Workshop folder ${dir} (TRIVIA_DEV_WORKSHOP_DIR)`);
    return workshopItems(fakeUgc(dir));
  } catch (err) {
    console.error(`trivia: workshop unavailable: ${err.message}`);
    return [];
  }
}

/** Page's view of one list entry: plain JSON, no disk paths but the folder's basename. */
function modEntry(mod) {
  const m = mod.manifest ?? {};
  return {
    id: mod.id,
    name: m.name ?? null,
    version: m.version ?? null,
    description: m.description ?? null,
    source: mod.source,
    publishedFileId: mod.publishedFileId,
    kind: mod.kind,
    languages: Array.isArray(m.languages) ? m.languages : [],
    on: mod.on,
    active: !!mod.dir && activeDirs.has(mod.dir),
    position: mod.position,
    state: mod.state,
    warnings: mod.warnings.map((w) => w.code),
    error: mod.error ? { code: mod.error.code, ...(mod.error.field ? { field: mod.error.field } : {}) } : null,
    dir: mod.dir ? path.basename(mod.dir) : null,
  };
}

async function listMods() {
  const { list } = await arrangeMods();
  return { mods: list.filter((e) => e.state !== "missing").map(modEntry), noMods: args.noMods, validUser };
}


/** `[{ id, on }]` in load order; ids left out keep their order after them. Next run's overlay only. */
async function setMods(order) {
  const ok =
    Array.isArray(order) &&
    order.length <= 500 &&
    order.every((e) => e !== null && typeof e === "object" && typeof e.id === "string" && MOD_ID.test(e.id) && typeof e.on === "boolean") &&
    new Set(order.map((e) => e.id)).size === order.length;
  if (!ok) throw new Error("bad_mods");
  const { settings } = await arrangeMods();
  const given = new Set(order.map((e) => e.id));
  const mods = [...order.map(({ id, on }) => ({ id, on })), ...settings.mods.filter((e) => !given.has(e.id))];
  await writeSettings(modsSettingsFile(), { ...settings, mods });
  return listMods();
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
  // Rejections carry the code as the message: bad_save, save_locked, no_user (decision 111: memory-only).
  const refused = () => Promise.reject(new Error("no_user"));
  handle("save:load", () => (saveFile ? queued(() => saveFile.read()) : null));
  handle("save:write", (text) => (saveFile ? queued(() => saveFile.write(text)) : refused()));
  handle("save:backup", (kind) => (saveFile ? queued(() => saveFile.backup(kind)) : refused()));
  // Mods (plan 114): fresh list per call; set rejects bad_mods, writes mods.json, applies next start.
  handle("mods:list", listMods);
  handle("mods:set", setMods);
  // Steam (plan 85): pass-throughs; null/false without Steam.
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
