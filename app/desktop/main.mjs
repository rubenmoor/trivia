// Electron shell (plan 54, D-63): plays app/client/dist over app://trivia/, no Python, no network.
import { app, BrowserWindow, dialog, ipcMain, Menu, protocol, screen, session } from "electron";
import { appendFileSync, existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { readFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import {
  arrange,
  clearMarker,
  discover,
  ID as MOD_ID,
  modsScript,
  noticed,
  readMarker,
  readSettings,
  withNotice,
  writeMarker,
  writeSettings,
} from "./mods.mjs";
import { checkMod } from "./check-mod.mjs";
import { muteReason } from "./mute.mjs";
import { describe, itemUrl, preparePublish, publish, VISIBILITY } from "./publish.mjs";
import {
  devTicket,
  IDENTITY,
  MAX_TELEMETRY_BODY,
  postJson,
  postReport,
  reportFields,
  reportTarget,
  TELEMETRY_IDENTITY,
} from "./report.mjs";
import { makeResolver } from "./resolve.mjs";
import { makeSaveFile } from "./save.mjs";
import { loadWindowState, MIN_SIZE, startBounds, trackWindow } from "./window-state.mjs";
import { makeTelemetry } from "./telemetry.mjs";
import { fakeUgc, workshopItems } from "./workshop.mjs";

const ORIGIN = "app://trivia/";
const BACKGROUND = "#0b1120"; // --night-900

const REPO = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..", "..");
const STEAM_APP_ID = 480; // Spacewar until the real App ID (plan 85)
const STEAM_DEMO_APP_ID = 480; // Spacewar until the demo app exists (plan 178)

/** Demo build (decision 338): packaged `"demo": true` in package.json, unpackaged `TRIVIA_DEMO=1`; read once. */
let demo;
function isDemo() {
  if (demo !== undefined) return demo;
  demo = process.env.TRIVIA_DEMO === "1";
  if (app.isPackaged) {
    try {
      demo = JSON.parse(readFileSync(path.join(app.getAppPath(), "package.json"), "utf8")).demo === true;
    } catch (err) {
      console.error(`trivia: demo: package.json: ${err.message}`);
      demo = false;
    }
  }
  return demo;
}

const windowTitle = () => (isDemo() ? "¡Trivia! Demo" : "¡Trivia!");

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
    dist: path.join(REPO, "app", "client", isDemo() ? "dist-demo" : "dist"),
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

/** Crash marker (plan 118), beside mods.json. */
function modsMarkerFile() {
  return path.join(path.dirname(modsSettingsFile()), "mods-start.json");
}

/** Telemetry (plan 106): per install, outside Auto-Cloud's `save/`. */
function telemetryDir() {
  if (process.env.TRIVIA_TELEMETRY_DIR) return process.env.TRIVIA_TELEMETRY_DIR;
  return app.isPackaged ? path.join(app.getPath("userData"), "telemetry") : path.join(REPO, "state", "telemetry");
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

const USAGE =
  "known flags: --import-save <file> [--force], --no-mods, --check-mod <folder>, --publish-mod <folder> [--changenote <text>] [--visibility public|friends|unlisted|private] [--content-only] [--dry-run], --rp-probe, --lag-probe";
// Our flags' namespace; anything else (Electron/Chromium switches, the dev app path, Steam's) passes.
const OWN = /^--(import|export|save|trivia|no-mods|force|check|publish|changenote|visibility|content-only|dry-run|rp-probe|lag-probe)/;
const VALUE = { "--import-save": "a file", "--check-mod": "a folder", "--publish-mod": "a folder", "--changenote": "a text", "--visibility": "a value" };
const SWITCH = new Set(["--no-mods", "--force", "--content-only", "--dry-run", "--rp-probe", "--lag-probe"]);

/** Our flags from argv: `{ importSave, force, noMods, checkMod, publish }`, or `{ error }` for an unknown own-looking flag or a missing value. */
function parseArgs(argv) {
  const v = {};
  for (let i = 1; i < argv.length; i++) {
    const [flag, inline] = argv[i].split(/=(.*)/s);
    if (!OWN.test(flag)) continue;
    if (SWITCH.has(flag) && inline === undefined) {
      v[flag] = true;
      continue;
    }
    if (!VALUE[flag]) return { error: `unknown flag ${flag}; ${USAGE}` };
    const value = inline ?? argv[++i];
    if (!value || value.startsWith("--")) return { error: `${flag} needs ${VALUE[flag]}; ${USAGE}` };
    v[flag] = value;
  }
  const extra = ["--changenote", "--visibility", "--content-only", "--dry-run"].filter((f) => v[f]);
  if (!v["--publish-mod"] && extra.length) return { error: `${extra[0]} needs --publish-mod; ${USAGE}` };
  if (v["--force"] && !v["--import-save"]) return { error: `--force needs --import-save; ${USAGE}` };
  if (v["--publish-mod"] && (v["--import-save"] || v["--no-mods"]))
    return { error: `--publish-mod runs alone; ${USAGE}` };
  if (v["--check-mod"] && Object.keys(v).length > 1) return { error: `--check-mod runs alone; ${USAGE}` };
  if (v["--visibility"] && !(v["--visibility"] in VISIBILITY))
    return { error: `--visibility: public, friends, unlisted or private; ${USAGE}` };
  const publish = v["--publish-mod"] && {
    folder: path.resolve(v["--publish-mod"]),
    changenote: v["--changenote"] ?? null,
    visibility: v["--visibility"] ?? null,
    contentOnly: !!v["--content-only"],
    dryRun: !!v["--dry-run"],
  };
  const checkMod = v["--check-mod"] ? path.resolve(v["--check-mod"]) : null;
  return { importSave: v["--import-save"] ?? null, force: !!v["--force"], noMods: !!v["--no-mods"], rpProbe: !!v["--rp-probe"], lagProbe: !!v["--lag-probe"], checkMod, publish: publish || null };
}

/** argv for a relaunch: our own flags dropped (with their values), Electron's and Steam's kept. */
function relaunchArgs(argv) {
  const out = [];
  for (let i = 1; i < argv.length; i++) {
    const [flag, inline] = argv[i].split(/=(.*)/s);
    if (!OWN.test(flag)) out.push(argv[i]);
    else if (VALUE[flag] && inline === undefined) i++;
  }
  return out;
}

const args = parseArgs(process.argv);

protocol.registerSchemesAsPrivileged([
  { scheme: "app", privileges: { standard: true, secure: true, supportFetchAPI: true, stream: true } },
]);
app.commandLine.appendSwitch("autoplay-policy", "no-user-gesture-required");
Menu.setApplicationMenu(null);
// Fixed folder, independent of the product name (plan 55); before ready and the instance lock. Demo and full game share it (decision 336): one save, one instance.
if (app.isPackaged) app.setPath("userData", path.join(app.getPath("appData"), "trivia"));

let win = null;
let steam = null; // the binding, only while Steam is up
let steamTimer = null;
let steamInput = false;
let validUser = false; // decision 111: Steam user with a SteamID, or the dev switch; fixed for the session
let overlay = false; // Windows only: the native window Steam's overlay draws into (D-92)
let activeDirs = new Set(); // this run's overlay layers (plan 112): fixed until restart
let safeStart = null; // plan 118: { reason: "crashed", mods } | { reason: "flag" } | null
let marker = false; // this run wrote mods-start.json and the start isn't confirmed yet
let markerTimer = null;
let leaving = false; // quitting or relaunching: no more marker reactions
let saveFile = null; // set in start(), after Steam; stays null without a valid user
let telemetry = null; // likewise (decision 111)
let flushing = null; // the quit's save + telemetry flush (plan 107)
let flushed = false;
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
} else if ((args.checkMod || args.publish) && isDemo()) {
  // Demo: no mods or Workshop (decision 337).
  console.error(`trivia: ${args.checkMod ? "--check-mod" : "--publish-mod"} is not available in the demo`);
  app.exit(2);
} else if (args.checkMod) {
  headless("--check-mod", () => checkModCmd(args.checkMod));
} else if (args.publish) {
  headless("--publish-mod", () => publishMod(args.publish));
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
    leaving = true;
    if (flushed || (!pending && !telemetry)) return;
    event.preventDefault();
    flushing ??= flush()
      .catch(telemetryError)
      .finally(() => {
        flushed = true;
        app.quit();
      });
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
async function startSteam({ input = true } = {}) {
  const appId = steamAppId();
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
  steamInput = input && steam.input.init(false);
  steamTimer = setInterval(() => {
    steam.runCallbacks();
    rpTick?.();
  }, 100);
  console.error(
    `trivia: steam available, app ${appId}, user ${steam.getStatus().steamId} ${hasSteamId() ? "valid" : "none"}, language ${steam.apps.getCurrentGameLanguage()}`,
  );
}

/** A Steam launch sets SteamAppId; dev may override the constant. */
function steamAppId() {
  return Number(process.env.SteamAppId || process.env.TRIVIA_STEAM_APPID || (isDemo() ? STEAM_DEMO_APP_ID : STEAM_APP_ID));
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
  clearInterval(rpSecond);
  rpTick = null;
  if (steamInput) steam.input.shutdown();
  steamInput = false;
  steam.richPresence.clearRichPresence();
  steam.shutdown();
  steam = null;
}

// PLACEHOLDER(1479): Remote Play probe (plan 168, decision 302), `--rp-probe`; task 1479 removes this block and its calls.
let rpTick = null;
let rpLog = () => {};
let rpApi = null; // { f: flat calls, host: own steam id }
let rpDirect = false;
let rpFlashAt = 0; // F11: ms of the white frame, 0 = not armed
let rpPadsDown = "";
const rpLines = [];
const RP_BOX = "document.getElementById('rp-probe-box')";

/** koffi load of the binding's Steam library, v003 flat calls (decision 301). */
async function rpProbeStart() {
  const file = path.join(
    steamSdkDir(),
    "redistributable_bin",
    ...(process.platform === "win32" ? ["win64", "steam_api64.dll"] : ["linux64", "libsteam_api.so"]),
  );
  const logFile = path.join(app.getPath("userData"), "rp-probe.log");
  mkdirSync(path.dirname(logFile), { recursive: true });
  rpLog = (text) => {
    const line = `${new Date().toISOString().slice(11, 23)} ${text}`;
    rpLines.push(line);
    if (rpLines.length > 8) rpLines.shift();
    appendFileSync(logFile, `${line}\n`);
    console.error(`rp-probe: ${line}`);
  };
  console.error(`rp-probe: log ${logFile}`);
  if (!steam) return rpLog("no Steam: nothing to probe");
  try {
    const koffi = (await import("koffi")).default;
    const lib = koffi.load(file);
    let self = null;
    let version = 0;
    for (let n = 6; n >= 3 && !self; n--) {
      try {
        self = lib.func(`void *SteamAPI_SteamRemotePlay_v00${n}()`)();
        version = n;
      } catch {}
    }
    if (!self) throw new Error("no SteamAPI_SteamRemotePlay_v00N accessor");
    const P = "SteamAPI_ISteamRemotePlay_";
    const fn = (sig) => lib.func(sig.replace(/(\w+)\(/, `${P}$1(`));
    const f = {
      count: fn("uint32 GetSessionCount(void *s)"),
      id: fn("uint32 GetSessionID(void *s, int i)"),
      steamId: fn("uint64 GetSessionSteamID(void *s, uint32 id)"),
      name: fn("const char *GetSessionClientName(void *s, uint32 id)"),
      form: fn("int GetSessionClientFormFactor(void *s, uint32 id)"),
      enable: fn("bool BEnableRemotePlayTogetherDirectInput(void *s)"),
      disable: fn("void DisableRemotePlayTogetherDirectInput(void *s)"),
      input: fn("uint32 GetInput(void *s, void *buf, uint32 max)"),
      visible: fn("void SetMouseVisibility(void *s, uint32 id, bool v)"),
      cursor: fn("uint32 CreateMouseCursor(void *s, int w, int h, int hx, int hy, const void *bgra, int pitch)"),
      setCursor: fn("void SetMouseCursor(void *s, uint32 id, uint32 cursor)"),
    };
    rpApi = { f, self, host: String(steam.getStatus().steamId) };
    rpLog(`start: remote play v00${version}, host ${rpApi.host}, direct input off`);
    const sessions = new Map();
    const buf = Buffer.alloc(64 * 32);
    const FORM = ["unknown", "phone", "tablet", "computer", "tv", "vr"];
    rpTick = () => {
      const now = new Set();
      for (let i = 0, n = f.count(self); i < n; i++) now.add(f.id(self, i));
      for (const id of now)
        if (!sessions.has(id)) {
          const sid = String(f.steamId(self, id));
          const info = { sid, name: f.name(self, id), form: FORM[f.form(self, id)] ?? f.form(self, id) };
          sessions.set(id, info);
          rpLog(`session + id ${id} steam ${sid} ${sid === rpApi.host ? "HOST'S OWN" : "GUEST"} name "${info.name}" form ${info.form}`);
        }
      for (const [id, info] of sessions)
        if (!now.has(id)) {
          sessions.delete(id);
          rpLog(`session - id ${id} steam ${info.sid} name "${info.name}"`);
        }
      for (let n = f.input(self, buf, 32); n > 0; n = n === 32 ? f.input(self, buf, 32) : 0)
        for (let i = 0; i < n; i++) rpEvent(buf.subarray(i * 64, i * 64 + 64));
      rpPads(true);
    };
    rpSecond = setInterval(() => rpSecondly(sessions), 1000);
  } catch (err) {
    rpLog(`koffi/Steam: ${err.message}`);
  }
}

function rpEvent(b) {
  const sid = b.readUInt32LE(0);
  const type = b.readInt32LE(4);
  const head = `session ${sid}`;
  if (type === 1)
    rpLog(`rp mouse ${head} motion ${b[8] ? `abs ${b.readFloatLE(12).toFixed(3)},${b.readFloatLE(16).toFixed(3)}` : `delta ${b.readInt32LE(20)},${b.readInt32LE(24)}`}`);
  else if (type === 2 || type === 3) rpLog(`rp mouse ${head} button ${type === 2 ? "down" : "up"} 0x${b.readInt32LE(8).toString(16)}`);
  else if (type === 4) rpLog(`rp mouse ${head} wheel dir ${b.readInt32LE(8)} amount ${b.readFloatLE(12)}`);
  else if (type === 5 || type === 6) {
    const ch = b.readUInt32LE(16);
    rpLog(`rp key ${head} ${type === 5 ? "down" : "up"} scancode ${b.readInt32LE(8)} mods 0x${b.readUInt32LE(12).toString(16)} char ${ch ? JSON.stringify(String.fromCodePoint(ch)) : "-"}`);
  } else rpLog(`rp unknown ${head} type ${type}`);
}

let rpSecond = null;
let rpBusy = false;

/** Every second: Steam Input handles and the page's pads. */
function rpSecondly(sessions) {
  try {
    const hs = steam.input.getConnectedControllers();
    rpLog(
      `steam-input ${hs.length} handles${hs
        .map((h) => ` [${h} type ${steam.input.getInputTypeForHandle(h)} session ${steam.input.getRemotePlaySessionID(h)} pad ${steam.input.getGamepadIndexForController(h)}]`)
        .join("")} sessions ${sessions.size}`,
    );
  } catch (err) {
    rpLog(`steam-input: ${err.message}`);
  }
  rpPads(false);
}

const RP_PADS = `JSON.stringify([...navigator.getGamepads()].filter(Boolean).map((g) => ({ i: g.index, id: g.id, p: g.buttons.flatMap((b, n) => (b.pressed ? [n] : [])) })))`;

/** `pads` line (log) or, when armed by F11, the first press afterwards (quiet = from the 100 ms tick). */
function rpPads(quiet) {
  if (!win || win.isDestroyed() || (quiet && !rpFlashAt) || rpBusy) return;
  rpBusy = true;
  win.webContents
    .executeJavaScript(RP_PADS)
    .then((json) => {
      const pads = JSON.parse(json);
      const down = JSON.stringify(pads.map((p) => [p.i, p.p]).filter(([, p]) => p.length));
      if (!quiet) rpLog(`pads ${pads.length}${pads.map((p) => ` [${p.i} "${p.id}" pressed ${p.p.join(",") || "-"}]`).join("")}`);
      if (rpFlashAt && down !== "[]" && down !== rpPadsDown) {
        rpLog(`flash → pad press after ${Date.now() - rpFlashAt} ms: ${down}`);
        rpFlashAt = 0;
      }
      rpPadsDown = down;
    })
    .catch(() => {})
    .finally(() => (rpBusy = false));
}

const RP_PAGE = `(() => {
  const box = document.createElement("pre");
  box.id = "rp-probe-box";
  box.style.cssText = "position:fixed;right:0;bottom:0;z-index:2147483647;margin:0;padding:6px;max-width:60vw;background:#000c;color:#0f0;font:12px monospace;white-space:pre-wrap;pointer-events:none";
  document.body.append(box);
  let last = 0;
  const say = (kind, e) => {
    const now = performance.now();
    if (kind === "dom mouse move" && now - last < 100) return;
    last = now;
    console.log("rp-probe " + kind + " " + Math.round(e.clientX) + "," + Math.round(e.clientY) + " trusted " + e.isTrusted + " pointer " + e.pointerType + " button " + e.button);
  };
  addEventListener("pointermove", (e) => say("dom mouse move", e), true);
  addEventListener("pointerdown", (e) => say("dom mouse down", e), true);
})()`;

function rpProbeWindow(wc) {
  wc.on("did-finish-load", () => {
    wc.executeJavaScript(RP_PAGE).catch(() => {});
    rpLog("window loaded");
  });
  wc.on("console-message", (event) => {
    if (event.message.startsWith("rp-probe ")) rpLog(event.message.slice(9));
  });
  setInterval(() => {
    if (!win || win.isDestroyed()) return;
    const text = `${path.join(app.getPath("userData"), "rp-probe.log")}\n${rpLines.join("\n")}\nF9 direct input · F10 cursor · F11 flash`;
    wc.executeJavaScript(`{ const b = ${RP_BOX}; if (b) b.textContent = ${JSON.stringify(text)}; }`).catch(() => {});
  }, 500);
  wc.on("before-input-event", (event, input) => {
    if (input.type !== "keyDown" || input.isAutoRepeat) return;
    rpLog(`dom key ${input.key} code ${input.code}`);
    if (!["F9", "F10", "F11"].includes(input.key)) return;
    event.preventDefault();
    if (!rpApi) return rpLog(`${input.key}: no Remote Play API`);
    const { f, self } = rpApi;
    if (input.key === "F9") {
      rpDirect = !rpDirect;
      if (rpDirect) rpLog(`direct input on → ${f.enable(self)}`);
      else {
        f.disable(self);
        rpLog("direct input off");
      }
    } else if (input.key === "F10") {
      const px = Buffer.alloc(32 * 32 * 4);
      for (let i = 0; i < 32 * 32; i++) {
        const edge = i % 32 < 3 || i % 32 > 28 || i < 96 || i > 32 * 29;
        px.set(edge ? [255, 255, 255, 255] : [0, 0, 255, 255], i * 4); // BGRA: red fill
      }
      const cursor = f.cursor(self, 32, 32, 0, 0, px, 128);
      const ids = [];
      for (let i = 0, n = f.count(self); i < n; i++) ids.push(f.id(self, i));
      for (const id of ids) {
        f.visible(self, id, true);
        f.setCursor(self, id, cursor);
      }
      rpLog(`custom cursor ${cursor} for sessions [${ids.join(",")}]`);
    } else {
      rpFlashAt = Date.now();
      wc.executeJavaScript(
        `{ const d = document.createElement("div"); d.style.cssText = "position:fixed;inset:0;background:#fff;z-index:2147483646"; document.body.append(d); setTimeout(() => d.remove(), 300); }`,
      ).catch(() => {});
      rpLog("flash: press a pad on the guest");
    }
  });
}

// EResult codes the binding reports for createItem/submitItemUpdate.
const ERESULT = {
  2: "generic failure",
  8: "invalid parameter",
  9: "file not found",
  15: "access denied: not the item's owner, or the Workshop isn't enabled for this app",
  16: "timeout",
  25: "limit exceeded: Workshop storage quota",
};

/** A headless command (plans 119, 120): no window, no instance lock; exit with its code. */
function headless(flag, run) {
  run().then(
    (code) => app.exit(code),
    (err) => {
      console.error(`trivia: ${flag}: ${err.stack ?? err}`);
      app.exit(1);
    },
  );
}

/** Headless output: stdout/stderr; packaged Windows has no console, so also a log file (once `logTo` names it) and a message box. */
function headlessOutput() {
  const winOut = app.isPackaged && process.platform === "win32";
  const early = [];
  let logFile = null;
  const toLog = (line) => {
    try {
      appendFileSync(logFile, `${line}\n`);
    } catch {}
  };
  const out = (line, isError = false) => {
    (isError ? process.stderr : process.stdout).write(`${line}\n`);
    if (!winOut) return;
    if (logFile) toLog(line);
    else early.push(line);
  };
  const logTo = (file) => {
    if (!winOut) return;
    logFile = file;
    try {
      writeFileSync(logFile, "");
    } catch {}
    early.forEach(toLog);
  };
  /** `{ code, text }` → the message box (Windows packaged), → code. */
  const finish = async ({ code, text }) => {
    if (winOut) {
      await app.whenReady();
      await dialog.showMessageBox({
        type: code ? "error" : "info",
        title: "¡Trivia!",
        message: code ? `${text}\n\nlog: ${logFile}` : text,
      });
    }
    return code;
  };
  return { out, logTo, finish };
}

/** `--check-mod` (plan 120): the loader's checks on one folder, read only. → exit code 0 ok, 1 errors. */
async function checkModCmd(folder) {
  const { out, logTo, finish } = headlessOutput();
  logTo(path.join(path.dirname(folder), `${path.basename(folder)}-check.log`));
  const r = await checkMod(folder, { ...roots(), gameVersion: app.getVersion() }, out);
  const text = r.errors ? `${r.errors} error(s) in ${folder}: fix them` : `${path.basename(folder)}: loads as is`;
  return finish({ code: r.errors ? 1 : 0, text });
}

/** `--publish-mod` (plan 119): the folder is only read and copied. → exit code. */
async function publishMod(opts) {
  const { out, logTo, finish } = headlessOutput();
  const p = await preparePublish(opts.folder, app.getVersion(), roots());
  logTo(path.join(path.dirname(opts.folder), `${p.manifest?.id ?? path.basename(opts.folder)}-publish.log`));
  for (const w of p.warnings) out(`warning: ${w}`, true);
  let result;
  if (p.error) {
    out(`error: ${p.error}`, true);
    result = { code: 1, text: p.error };
  } else {
    try {
      result = await upload(p, opts, out);
    } finally {
      await p.dispose();
      stopSteam();
    }
  }
  return finish(result);
}

/** Dry-run summary, or Steam + publish; the binding's warn/error lines pass through. → { code, text }. */
async function upload(p, opts, out) {
  for (const line of describe(p, opts)) out(line);
  if (opts.dryRun) return { code: 0, text: `dry run ok: ${p.manifest.id}` };
  await startSteam({ input: false });
  // Real user only (decision 111): the dev switch doesn't publish.
  if (!hasSteamId()) {
    const text = "publishing needs the Steam client running and logged in";
    out(`error: ${text}`, true);
    return { code: 1, text };
  }
  const { log, warn, error } = console;
  let reason = null;
  const pass = (...args) => {
    let line = args.join(" ").replace("[Steamworks] ", "").split("\n")[0];
    const code = /result: (\d+)$/.exec(line)?.[1];
    if (ERESULT[code]) line += ` (${ERESULT[code]})`;
    reason = line;
    out(`steam: ${line}`, true);
  };
  console.log = () => {};
  console.warn = console.error = pass;
  try {
    const r = await publish(steam.workshop, steamAppId(), p, opts, out);
    if (r.ok) return { code: 0, text: `published ${itemUrl(r.workshopId)}` };
    return { code: 1, text: `publishing failed${reason ? `: ${reason}` : ""}` };
  } finally {
    Object.assign(console, { log, warn, error });
  }
}

/** Source file → this user's save; the source stays untouched. → ok. */
async function importSave(file, force) {
  const source = path.resolve(file);
  try {
    const kept = await saveFile.importText(await readFile(source, "utf8"), { force });
    console.error(`trivia: imported ${source} → ${saveFile.file}`);
    if (kept) console.error(`trivia: old save kept in ${kept}`);
    return true;
  } catch (err) {
    console.error(`trivia: --import-save ${source}: ${err.message}`);
    return false;
  }
}

// PLACEHOLDER(1486): lag probe (plan 170), `--lag-probe`; task 1486 removes this block, the page and the flag.
function lagProbe() {
  const logFile = path.join(app.getPath("userData"), "lag-probe.log");
  mkdirSync(path.dirname(logFile), { recursive: true });
  win = new BrowserWindow({
    fullscreen: true,
    show: false,
    backgroundColor: "#000000",
    title: "lag probe",
    webPreferences: { contextIsolation: true, sandbox: true, nodeIntegration: false },
  });
  win.once("ready-to-show", () => win.show());
  if (isDemo()) win.on("page-title-updated", (e) => e.preventDefault()); // index.html's <title> would win
  win.on("closed", () => (win = null));
  const wc = win.webContents;
  wc.setAudioMuted(true);
  wc.on("console-message", (event) => {
    if (!event.message.startsWith("lag-probe ")) return;
    const line = `${new Date().toISOString().slice(11, 23)} ${event.message.slice(10)}`;
    appendFileSync(logFile, `${line}\n`);
    console.error(`lag-probe: ${line}`);
  });
  console.error(`lag-probe: log ${logFile}`);
  win.loadFile(path.join(path.dirname(fileURLToPath(import.meta.url)), "lag-probe.html"), { query: { log: logFile } });
}

async function start() {
  await startSteam();
  if (args.lagProbe) return lagProbe();
  if (args.rpProbe) await rpProbeStart();
  validUser = checkUser();
  if (validUser) {
    saveFile = makeSaveFile(userSaveDir());
    console.error(`trivia: save ${saveFile.file}`);
    await saveFile.dropStaleTemp();
    if (!isDemo()) { // decision 337: no telemetry in the demo
      telemetry = makeTelemetry(telemetryDir(), { version: app.getVersion() });
      await telemetry.start().catch(telemetryError);
    }
  } else console.error("trivia: no Steam user, progress not saved");
  if (!telemetryOn()) console.error("trivia: telemetry off");
  if (args.importSave) {
    if (!saveFile) {
      console.error("trivia: --import-save needs a Steam user (or TRIVIA_DEV_STEAM_USER=1)");
      app.exit(1);
      return;
    }
    if (!(await importSave(args.importSave, args.force))) {
      app.exit(1);
      return;
    }
  }

  const dirs = roots();
  if (!existsSync(path.join(dirs.dist, "index.html"))) {
    dialog.showErrorBox(
      windowTitle(),
      isDemo() && !app.isPackaged
        ? "demo client not built: run `TRIVIA_DEMO=1 npm run build -w app/client`"
        : "client not built: run `npm run build -w app/client`",
    );
    app.quit();
    return;
  }

  const { layers, mods, modsJs } = await loadMods();

  const ses = session.defaultSession;
  ses.protocol.handle("app", makeResolver({ ...dirs, layers, mods, modsJs }));
  ses.webRequest.onBeforeRequest(
    { urls: ["http://*/*", "https://*/*", "ws://*/*", "wss://*/*"] },
    (_details, callback) => callback({ cancel: true }),
  );
  ses.setPermissionRequestHandler((_wc, permission, callback) => callback(permission === "fullscreen"));
  ses.setPermissionCheckHandler((_wc, permission) => permission === "fullscreen");
  // No dictionary download (task 1003).
  ses.setSpellCheckerLanguages([]);

  const winFile = path.join(app.getPath("userData"), "window.json");
  const winState = loadWindowState(winFile);
  win = new BrowserWindow({
    ...startBounds(winState, screen),
    minWidth: MIN_SIZE.width,
    minHeight: MIN_SIZE.height,
    fullscreen: args.rpProbe || winState.fullscreen, // the probe forces fullscreen and keeps no state
    show: false,
    backgroundColor: BACKGROUND,
    title: windowTitle(),
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
        `--trivia-region=${localeCountry()}`,
      ],
    },
  });
  win.once("ready-to-show", () => win.show());
  if (telemetry) win.webContents.once("did-finish-load", () => setTimeout(sendLeftovers, LEFTOVERS_MS));
  // After the load: a frame subscription made before it gets no frames.
  if (steam && process.platform === "win32")
    win.webContents.once("did-finish-load", () => {
      overlay = steam.addElectronSteamOverlay(win, { title: windowTitle() });
    });
  win.on("closed", () => (win = null));
  if (!args.rpProbe) {
    const tracker = trackWindow(win, winState, winFile);
    app.on("before-quit", () => tracker.flush());
  }
  for (const e of ["enter-full-screen", "leave-full-screen"])
    win.on(e, () => win.webContents.send("trivia:fullscreen", win.isFullScreen()));

  const wc = win.webContents;
  const muted = muteReason(process.env);
  if (muted) {
    wc.setAudioMuted(true);
    console.error(`trivia: muted (${muted})`);
  }
  wc.on("will-navigate", (event, url) => {
    if (!url.startsWith(ORIGIN)) event.preventDefault();
  });
  wc.setWindowOpenHandler(() => ({ action: "deny" }));

  if (args.rpProbe) rpProbeWindow(wc);
  bridge();
  if (layers.length) await watchStart(wc, mods.map((m) => m.id));
  win.loadURL(ORIGIN);
}

const CONFIRM_MS = 20000;
const PING_MS = 3000;

/** Plan 118: marker before the load; confirmed by `mods:ready` or a page alive 20 s after the load; a crash or hang relaunches. */
async function watchStart(wc, ids) {
  try {
    await writeMarker(modsMarkerFile(), ids);
    marker = true;
  } catch (err) {
    console.error(`trivia: mods: ${modsMarkerFile()}: ${err.message}`);
    return;
  }
  wc.once("did-finish-load", () => {
    markerTimer = setTimeout(async () => {
      const alive = await Promise.race([
        wc.executeJavaScript("0").then(() => true, () => false),
        new Promise((resolve) => setTimeout(() => resolve(false), PING_MS)),
      ]);
      if (alive) confirmStart("alive");
      else startFailed("not responding");
    }, CONFIRM_MS);
  });
  wc.on("render-process-gone", (_e, { reason }) => reason !== "clean-exit" && startFailed(`page ${reason}`));
  wc.on("did-fail-load", (_e, code, desc, _url, mainFrame) => {
    if (mainFrame && code !== -3) startFailed(`load failed: ${desc}`);
  });
}

async function confirmStart(how) {
  if (!marker) return;
  marker = false;
  clearTimeout(markerTimer);
  await clearMarker(modsMarkerFile()).then(
    () => console.error(`trivia: mods: start confirmed (${how})`),
    (err) => console.error(`trivia: mods: ${modsMarkerFile()}: ${err.message}`),
  );
}

/** Marker stays: the next start is safe. */
function startFailed(why) {
  if (!marker || leaving) return;
  marker = false;
  clearTimeout(markerTimer);
  console.error(`trivia: mods: start failed (${why}), relaunching without mods`);
  relaunch();
}

/** Save queue and telemetry flushed, then a fresh process without our own flags. */
async function relaunch() {
  if (leaving) return;
  leaving = true;
  app.relaunch({ args: relaunchArgs(process.argv) });
  flushing ??= flush().catch(telemetryError);
  await flushing;
  app.exit(0);
}

/** Discovery, mods.json, load order → overlay layers, loaded mods' bundles and `/mods.js`, fixed for the run; none with --no-mods. */
async function loadMods() {
  if (isDemo()) return { layers: [], mods: [], modsJs: modsScript([]) }; // decision 337: no mods in the demo
  const file = modsSettingsFile();
  const arranged = await arrangeMods(true);
  if (arranged.changed)
    await writeSettings(file, arranged.settings).catch((err) => console.error(`trivia: mods: ${file}: ${err.message}`));
  const mods = arranged.list;
  for (const mod of mods)
    if (mod.source === "workshop")
      console.error(`trivia: mod ${mod.id ?? "?"} workshop ${mod.publishedFileId} ${mod.dir ? "installed" : mod.state}`);
  const crashed = await readMarker(modsMarkerFile());
  if (crashed) {
    await clearMarker(modsMarkerFile()).catch((err) => console.error(`trivia: mods: ${modsMarkerFile()}: ${err.message}`));
    safeStart = { reason: "crashed", mods: crashed.mods };
    console.error(`trivia: mods: last start with mods didn't finish (${crashed.mods.join(", ") || "?"}): no mods this run`);
  } else if (args.noMods) {
    safeStart = { reason: "flag" };
    console.error("trivia: --no-mods: no mods this run");
  }
  if (safeStart) return { layers: [], mods: [], modsJs: modsScript([]) };
  const count = {};
  for (const mod of mods) {
    count[mod.state] = (count[mod.state] ?? 0) + 1;
    const notes = [...(mod.error ? [mod.error.code] : []), ...(mod.warnings ?? []).map((w) => w.code)];
    console.error(`trivia: mod ${mod.id ?? mod.dir ?? mod.publishedFileId} ${mod.state}${notes.length ? ` [${notes.join(", ")}]` : ""}`);
  }
  if (mods.length)
    console.error(`trivia: mods: ${Object.entries(count).map(([state, n]) => `${n} ${state}`).join(", ")}`);
  activeDirs = new Set(arranged.layers);
  const loaded = mods.filter((m) => m.state === "loaded");
  return {
    layers: arranged.layers,
    mods: loaded.map((m) => ({ id: m.id, name: m.manifest.name, dir: m.dir, entry: m.manifest.entry, bundles: m.bundles })),
    modsJs: modsScript(mods),
  };
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
  const text = (v) => (typeof v === "string" ? v : null); // an invalid mod.json may have anything
  return {
    id: mod.id,
    name: text(m.name),
    version: text(m.version),
    game: text(m.game),
    description: text(m.description),
    source: mod.source,
    publishedFileId: mod.publishedFileId,
    kind: mod.kind,
    languages: Array.isArray(m.languages) ? m.languages.filter((l) => typeof l === "string") : [],
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
  if (isDemo()) return { mods: [], notice: true, noMods: true, safeStart: null, validUser }; // decision 337
  const { list, settings } = await arrangeMods();
  return {
    mods: list.filter((e) => e.state !== "missing").map(modEntry),
    notice: noticed(settings),
    noMods: safeStart !== null,
    safeStart,
    validUser,
  };
}

/** One-time notice accepted (plan 118): new mods come on from now; existing rows kept. */
async function acceptNotice() {
  if (isDemo()) return listMods(); // mods.json is the full game's (decision 336)
  const { settings } = await arrangeMods();
  await writeSettings(modsSettingsFile(), withNotice(settings));
  return listMods();
}

/** Plan 118: «Restart to apply». */
async function restart() {
  console.error("trivia: mods: restart");
  await confirmStart("restart");
  await relaunch();
}

/** `[{ id, on }]` in load order; ids left out keep their order after them. Next run's overlay only. */
async function setMods(order) {
  if (isDemo()) return listMods();
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

/** Code only: paths and bodies carry ids. */
function telemetryError(err) {
  console.error(`trivia: telemetry: ${err?.code ?? "error"}`);
}

const plain = (v) => v !== null && typeof v === "object" && Object.getPrototypeOf(v) === Object.prototype;

/** `{ games, index }` from the page: plain objects, parallel arrays, ≤ 1 MiB. */
function telemetryArg(arg) {
  const ok =
    plain(arg) &&
    Array.isArray(arg.games) &&
    Array.isArray(arg.index) &&
    arg.games.length === arg.index.length &&
    arg.games.length <= 200 &&
    arg.games.every((g) => plain(g) && (g.answers === undefined || Array.isArray(g.answers))) &&
    arg.index.every((e) => plain(e) && typeof e.key === "string" && e.key.length <= 200 && Number.isInteger(e.from) && e.from >= 0) &&
    Buffer.byteLength(JSON.stringify(arg), "utf8") <= 1024 * 1024;
  if (!ok) throw new Error("bad_telemetry");
  return { games: arg.games, index: arg.index };
}

/** Plans 93, 107: the server's base URL, `reportUrl` beside `version` in package.json; read once. */
let configuredUrl;
function serverBase() {
  if (configuredUrl !== undefined) return configuredUrl;
  configuredUrl = "";
  try {
    configuredUrl = JSON.parse(readFileSync(path.join(app.getAppPath(), "package.json"), "utf8")).reportUrl ?? "";
  } catch (err) {
    console.error(`trivia: report: package.json: ${err.message}`);
  }
  return configuredUrl;
}

/** `<base>/reports`, or the dev override; null = copy only. */
function reportConfig() {
  const configured = serverBase();
  const target = reportTarget(configured, process.env);
  if (configured && !target) console.error("trivia: report: reportUrl is not an http(s) URL");
  if (target?.dev) console.error(`trivia: report: dev URL ${target.url.href} (TRIVIA_REPORT_URL)`);
  return target;
}

let reportTargetCache;
function reportAvailable() {
  if (!validUser || isDemo()) return false; // decision 337: no question reports in the demo
  reportTargetCache ??= reportConfig();
  return reportTargetCache !== null;
}

/** One POST per call, fresh ticket, cancelled after the response; ticket and fields never logged. */
async function sendReport(arg) {
  let fields;
  try {
    fields = reportFields(arg);
  } catch (err) {
    console.error(`trivia: report: bad field ${err.field ?? "?"}`);
    throw err;
  }
  if (!reportAvailable()) return { ok: false, status: 0, error: "unavailable" };
  const { url, dev } = reportTargetCache;
  const r = await withTicket(IDENTITY, dev, (ticket) => postReport(url, fields, ticket));
  if (!r) {
    console.error("trivia: report: no Steam ticket");
    return { ok: false, status: 0, error: "no_ticket" };
  }
  console.error(`trivia: report: ${r.ok ? "sent" : `failed ${r.status} ${r.error}`}`);
  return r;
}

const TICKET_MS = 2000;

/** `fn(ticketHex)` with a fresh ticket for `identity` (dev: `dev-<random>`), cancelled after; null without a ticket in 2 s. */
async function withTicket(identity, dev, fn) {
  let ticket = null;
  if (dev || !hasSteamId()) ticket = { ticketHex: devTicket(), authTicket: null };
  else {
    const t = await steamTicket(identity);
    if (t?.success && t.ticketHex) ticket = t;
    else if (t?.authTicket) steam?.user.cancelAuthTicket(t.authTicket);
  }
  if (!ticket) return null;
  try {
    return await fn(ticket.ticketHex);
  } finally {
    if (ticket.authTicket) steam?.user.cancelAuthTicket(ticket.authTicket);
  }
}

/** The binding's callback, or null after `TICKET_MS`; a late ticket is cancelled. */
function steamTicket(identity) {
  const p = steam.user.getAuthTicketForWebApi({ genericString: identity }).catch(() => null);
  return new Promise((resolve) => {
    const timer = setTimeout(() => {
      resolve(null);
      p.then((t) => t?.authTicket && steam?.user.cancelAuthTicket(t.authTicket));
    }, TICKET_MS);
    p.then((t) => {
      clearTimeout(timer);
      resolve(t);
    });
  });
}

// Plan 107, decision 120: one send at quit, one later try at the next start.
const QUIT_BUDGET_MS = 4000;
const LEFTOVERS_MS = 30000;

let telemetryTargetCache;
/** Gate: valid user, a stored yes, a server URL. */
function telemetryOn() {
  if (!validUser || !telemetry?.consented()) return false;
  telemetryTargetCache ??= reportTarget(serverBase(), process.env, "telemetry");
  return telemetryTargetCache !== null;
}

/** Save queue, the last stamp, then this run's session: one try within `QUIT_BUDGET_MS`, window hidden. */
async function flush() {
  if (!telemetry) return void (await writing);
  const on = telemetryOn();
  if (on) win?.hide();
  const [, file] = await Promise.all([writing, on ? telemetry.close() : telemetry.finish()]);
  if (file) await sendSession(file, false, Date.now() + QUIT_BUDGET_MS);
}

/** Once per run: files left by earlier runs, oldest first, each deleted after this try. */
async function sendLeftovers() {
  try {
    for (const { file } of await telemetry.pending()) {
      if (flushing || !telemetryOn()) return;
      await sendSession(file, true);
    }
  } catch (err) {
    telemetryError(err);
  }
}

/** One POST of a session file; silent but one dev line, never ids, ticket or body. */
async function sendSession(file, final, deadline) {
  const body = await telemetry.outgoing(file);
  if (!body) {
    await telemetry.settle(file, 0, true);
    console.error("trivia: telemetry: unreadable session dropped");
    return;
  }
  const { url, dev } = telemetryTargetCache;
  const r = await withTicket(TELEMETRY_IDENTITY, dev, (ticket) => {
    const left = deadline && Math.max(1, deadline - Date.now());
    const timeouts = left ? { connectMs: Math.min(left, 5000), totalMs: left } : {};
    return postJson(url, { ...body, ticket }, { maxBody: MAX_TELEMETRY_BODY, ...timeouts });
  });
  const tooLarge = r?.error === "too_large";
  const status = r?.res?.statusCode ?? 0;
  const kept = await telemetry.settle(file, status, final || tooLarge);
  console.error(`trivia: telemetry → ${tooLarge ? "too_large" : status} ${kept ? "kept" : "dropped"}`);
}

/** The machine's locale country (plan 151), "" for none; getLocaleCountryCode() is "" on Linux, so the system locale's region. */
function localeCountry() {
  try {
    return app.getLocaleCountryCode() || (new Intl.Locale(app.getSystemLocale()).region ?? "");
  } catch {
    return "";
  }
}

/** IPC for preload.cjs; only our own page may call. */
function bridge() {
  const handle = (channel, fn) =>
    ipcMain.handle(channel, (event, ...args) => {
      if (!event.senderFrame?.url.startsWith(ORIGIN)) throw new Error("forbidden");
      return fn(...args);
    });
  handle("trivia:fullscreen", () => win?.isFullScreen() ?? false);
  handle("trivia:set-fullscreen", (yes) => win?.setFullScreen(yes === true));
  handle("trivia:quit", () => app.quit());
  // Rejections carry the code as the message: bad_save, save_locked, no_user (decision 111: memory-only).
  const refused = () => Promise.reject(new Error("no_user"));
  handle("save:load", () => (saveFile ? queued(() => saveFile.read()) : null));
  handle("save:write", (text) => (saveFile ? queued(() => saveFile.write(text)) : refused()));
  handle("save:backup", (kind) => (saveFile ? queued(() => saveFile.backup(kind)) : refused()));
  // Telemetry (plan 106): no-ops without a valid user; record rejects bad_telemetry.
  handle("telemetry:state", () => telemetry?.state() ?? { available: false, consent: null });
  handle("telemetry:consent", (yes) => {
    if (!telemetry) return { available: false, consent: null };
    if (typeof yes !== "boolean") throw new Error("bad_telemetry");
    return telemetry.setConsent(yes);
  });
  handle("telemetry:load", () => telemetry?.load() ?? null);
  handle("telemetry:record", async (arg) => {
    if (telemetry) await telemetry.record(telemetryArg(arg));
  });
  // Mods (plan 114): fresh list per call; set rejects bad_mods, writes mods.json, applies next start.
  handle("mods:list", listMods);
  handle("mods:set", setMods);
  // Plan 118: notice, restart, the page's ready (clears the crash marker).
  handle("mods:notice", acceptNotice);
  handle("mods:restart", restart);
  handle("mods:ready", () => confirmStart("ready"));
  // Reports (plan 93): main posts, the page passes fields only; send rejects bad_report.
  handle("report:available", reportAvailable);
  handle("report:send", sendReport);
  // Steam (plan 85): pass-throughs; null/false without Steam.
  handle("steam:steam-id", () => steam?.getStatus().steamId ?? null);
  handle("steam:language", () => steam?.apps.getCurrentGameLanguage() ?? null);
  handle("steam:unlock", async (id) => {
    if (!steam || typeof id !== "string" || isDemo()) return false; // decision 346: no achievements in the demo
    const ok = await steam.achievements.unlockAchievement(id);
    if (!ok) console.error(`trivia: steam: unlock ${id} refused`);
    return ok;
  });
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
