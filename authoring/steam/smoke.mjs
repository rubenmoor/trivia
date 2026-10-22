#!/usr/bin/env node
// Packaged smoke game (plan 89, release check step 6): the unpacked Linux build offline, clean env, temp HOME,
// TRIVIA_DEV_STEAM_USER=1 (decision 111: saves need a valid Steam user; the switch stands in for one).
// Usage (dev shell): node authoring/steam/smoke.mjs [--demo] [--mods | --multiplayer | --matrix] [--trace <file>] [app/desktop/release/linux-unpacked];
// DEBUG=1 shows the shell's stderr
// New player → levels 1–3 with an image, audio and video question → quit → restart resumes; no «progress needs Steam»
// notice; then a Gamemaster-mode game, a few levels. Exit 1 names the step.
// --demo (plan 177): the demo build (release/demo/linux-unpacked): the solo and Gamemaster games, the multiplayer sessions
// of the built modes (BUILT_MODES) with --multiplayer; on the way the Start screen's demo line, one bundle tile and no pack,
// no PLACEHOLDER in the visible text, every question in app/data/demo/pool.json.
// --demo --matrix (plan 179, decision 347) instead: per single-player BUILT_MODES mode × age group (the build's age-groups.json) one
// game on screen from Choice to a win at the last level, first card each level, Soplo, Bájale, Paso, Cambiazo and
// Francotirador played on the way, then one to a loss (last card, a wrong answer); fresh HOME each; ✗ on a refused start
// (supply_short, no_questions), a game that doesn't reach its end or a question outside the demo list.
// --trace <file>: per scene the offered and shown question ids and the answer orders, as JSON (the release check compares two).
// With packs (DLC depots, decision 66): once as built (packs offered), once without their files (not offered).
// --mods (plan 104, task 942) instead: the shipped modding/ examples in <userData>/mods/: loaded, theme applied, player
// bundle offered and played, rules tweak's extra hint, no crash marker; then the conversion on top, then --no-mods.
// --multiplayer (plan 167, decision 299) instead: rr-coop, rr-competitive, timed × 3 pads, 3 keyboard seats, 4 pads +
// keyboard and mouse; each Mode → Join → Choice → Bundles → an end, fake pads (fake_pads.js) and trusted CDP keys and clicks.
// The middle of a session is played by the engine on the save (as the solo run swaps cards), the rest on screen; a
// seat that may not act changes nothing; the timed pads, keyboard-only rr-coop, keyboard-only timed (claim keys) and 4 pads + keyboard and mouse timed sessions
// quit and restart mid-session: pads rebind (decision 289), keyboard seats never ask for a pad (decision 321); after each: one games[]
// row with its seats (decision 277), the mode's win achievement derived for a win (decision 285).
import { spawn, spawnSync } from "node:child_process";
import { accessSync, constants, existsSync, readdirSync, readFileSync } from "node:fs";
import { cp, mkdir, mkdtemp, readFile, rm, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { earned } from "../../app/client/src/engine/achievements.ts";
import { BUILT_MODES, DEFAULT_AGE_GROUP, answer, claim, gameMode, jokersUsed, pick, show } from "../../app/client/src/engine/game.ts";
import { LEVELS } from "../../app/client/src/engine/selection.ts";
import { seededRng } from "../../app/client/src/engine/rng.ts";
import { cacheName, shippedName } from "../../app/desktop/resolve.mjs";
import { connectPipe, pageHelpers, sleep, startXvfb, visibleEl } from "../tools/cdp.mjs";
import { loadData } from "../tools/engine_data.mjs";

const REPO = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..", "..");
const ARGS = process.argv.slice(2);
const MODS = ARGS.includes("--mods");
const MULTI = ARGS.includes("--multiplayer");
const DEMO = ARGS.includes("--demo");
const MATRIX = ARGS.includes("--matrix");
if (MATRIX && !DEMO) throw new Error("--matrix needs --demo");
const TRACE = ARGS.includes("--trace") ? ARGS[ARGS.indexOf("--trace") + 1] : null;
if (ARGS.includes("--trace") && !TRACE) throw new Error("--trace needs a file");
const EXE = DEMO ? "living-room-trivia-demo" : "living-room-trivia";
const BUILD = path.resolve(
  ARGS.find((a, i) => !a.startsWith("--") && ARGS[i - 1] !== "--trace") ??
    path.join(REPO, "app", "desktop", "release", ...(DEMO ? ["demo"] : []), "linux-unpacked"),
);
const BUNDLES = path.join("resources", "data", "bundles");
const TYPES = ["image", "audio", "video"]; // levels 1–3
const PLAYER = "Smoke";

// The demo's question list (--demo): every question on screen is one of these.
const DEMO_IDS = DEMO
  ? new Set(JSON.parse(readFileSync(path.join(REPO, "app", "data", "demo", "pool.json"), "utf8")).questions.map((q) => q.id))
  : null;
// What --trace writes: per scene the questions offered and shown, with their answer orders.
const trace = [];
let scene;
const begin = (name) => trace.push((scene = { scene: name, questions: [] }));
/** A question on screen: `offered` the cards before the pick (none: a timed question), `st` the state with `current`. */
function seen(offered, st) {
  for (const id of [...offered, st.current]) if (DEMO_IDS && !DEMO_IDS.has(id)) throw new Error(`question ${id} is not in the demo list`);
  scene.questions.push({ level: st.level, offered, shown: st.current, answers: st.answers });
}
// Any visible PLACEHOLDER text, kept across reloads (sessionStorage) and read before a quit.
const WATCH = `(() => { if (window.__ph) return; window.__ph = setInterval(() => {
  const m = document.body?.innerText.match(/PLACEHOLDER\\S*/);
  if (m) sessionStorage.setItem("smoke.placeholder", m[0]);
}, 150); })()`;
async function noPlaceholder() {
  const hit = await h.evaluate(`sessionStorage.getItem("smoke.placeholder")`).catch(() => null);
  if (hit) throw new Error(`visible text ${hit}`);
}

let step = "prepare";
const at = (name) => console.log(`  ${(step = name)}`);

/** Absolute path of a command on PATH (env -i drops PATH). */
function which(cmd) {
  for (const dir of (process.env.PATH ?? "").split(":")) {
    const file = path.join(dir, cmd);
    try {
      accessSync(file, constants.X_OK);
      return file;
    } catch {}
  }
  throw new Error(`${cmd} not found: run from the dev shell`);
}

/** Packs whose pool file for `locale` is in the build (as data.ts poolFile). */
const packsFor = (locale) =>
  packs().filter((b) => existsSync(path.join(DIR, BUNDLES, b, locale === "es" ? "pool.json" : `pool.${locale}.json`)));
const packs = () => (existsSync(path.join(DIR, BUNDLES)) ? readdirSync(path.join(DIR, BUNDLES)) : []);

/** The first question per media type in the shipped pool of `locale` (as data.ts poolFile); their media files. */
function pickQuestions(locale) {
  const file = locale === "es" ? "pool.json" : `pool.${locale}.json`;
  const pool = JSON.parse(readFileSync(path.join(DIR, "resources", "data", DEMO ? "demo" : "", file), "utf8"));
  return TYPES.flatMap((type) => {
    const q = pool.questions.find((x) => x.media?.type === type && x.media.file_url);
    if (!q && DEMO) return []; // the demo list may lack a type (levels 1–n then)
    if (!q) throw new Error(`no ${type} question in the pool`);
    const urls = [q.media.file_url, q.background?.file_url].filter(Boolean);
    return [{ type, q, files: urls.map((u) => mediaFile(u)) }];
  });
}

/** A media file in the build: the raw cacheName, else shippedName (as resolve.mjs /media). */
function mediaFile(url) {
  const raw = path.join("resources", "media", cacheName(url));
  return existsSync(path.join(DIR, raw)) ? raw : path.join("resources", "media", shippedName(url));
}

let DIR, page, h, home, display;
const procs = [];

const saveFile = () => path.join(home, ".config", "trivia", "save", "dev", "game.json") // decision 114;
const running = (save) => save.games.at(-1).state;

/** The save on disk once `test` holds (the shell writes after each action). */
async function saved(test, what, ms = 10000) {
  for (const end = Date.now() + ms; Date.now() < end; await sleep(100)) {
    try {
      const save = JSON.parse(await readFile(saveFile(), "utf8"));
      if (test(save)) return save;
    } catch {}
  }
  throw new Error(`save: ${what}`);
}

async function launch(...args) {
  const steamRun = which("steam-run");
  // Muted: checks media load, not audio; sound is a manual row.
  const env = [`HOME=${home}`, `DISPLAY=${display}`, "TRIVIA_DEVTOOLS=1", "TRIVIA_MUTE=1", "TRIVIA_DEV_STEAM_USER=1"];
  // unshare -rn: no network; env -i + steam-run: no Nix shell env, an FHS runtime like a Steam Linux machine.
  const shell = spawn("unshare", ["-rn", "env", "-i", ...env, steamRun, path.join(DIR, EXE), "--lang=es", ...args, "--remote-debugging-pipe"], {
    stdio: ["ignore", "ignore", "pipe", "pipe", "pipe"],
  });
  shell.stderr.on("data", (d) => process.env.DEBUG && process.stderr.write(d));
  procs.push(shell);
  page = await connectPipe(shell);
  h = pageHelpers(page);
  if (DEMO) {
    await page.send("Page.enable");
    await page.send("Page.addScriptToEvaluateOnNewDocument", { source: WATCH });
    await h.evaluate(WATCH);
  }
  return shell;
}

async function quit(shell) {
  if (DEMO) await noPlaceholder();
  const exited = new Promise((r) => shell.once("exit", r));
  await h.evaluate("window.triviaShell.quit()").catch(() => {}); // the page goes away mid-call
  let timer;
  const timeout = new Promise((_, reject) => (timer = setTimeout(() => reject(new Error("shell didn't exit")), 10000)));
  await Promise.race([exited, timeout]).finally(() => clearTimeout(timer));
}

/** Wait for the question's media; a missing-media notice or a broken element fails. */
async function checkMedia(type) {
  const state = `(() => {
    if (document.querySelector(".media-missing")) return "missing";
    const imgs = [...document.querySelectorAll(".question-screen img")];
    const players = [...document.querySelectorAll(".question-screen video, .question-screen audio")];
    if (${type !== "image"} && !players.length) return "no player";
    if (players.some((m) => m.error)) return "missing";
    const ok = imgs.every((i) => i.complete && i.naturalWidth > 0) && players.every((m) => m.readyState >= 2);
    return ok ? "ok" : "loading";
  })()`;
  let last;
  for (const end = Date.now() + 30000; Date.now() < end; await sleep(200)) {
    last = await h.evaluate(state);
    if (last === "ok") return;
    if (last === "missing") throw new Error("missing-media notice on screen");
    if (last === "no player") break;
  }
  const info = await h.evaluate(`JSON.stringify([...document.querySelectorAll("video, audio")].map((m) => [m.tagName, m.readyState, m.networkState]))`);
  throw new Error(`media not ready (${last}) ${info}`);
}

/** Level `level`: swap the first card for `q`, reload, resume, pick it, check the media, answer right. */
async function playLevel(level, { type, q }) {
  at(`level ${level} (${type}, ${q.id})`);
  await h.waitFor(visibleEl(".cards .card"), "cards");
  const save = await saved((s) => running(s).phase === "select" && running(s).level === level, `level ${level} cards`);
  const offered = [...running(save).options];
  running(save).options[0] = q.id;
  await writeFile(saveFile(), JSON.stringify(save));
  await page.send("Page.reload", { ignoreCache: true });
  await sleep(500);
  await h.click('[data-focus-id="main"]');
  await h.waitFor(`${visibleEl(".level .hint")} || ${visibleEl(".cards .card")}`, "level or cards");
  if (await h.evaluate(visibleEl(".level .hint"))) await h.click(".level .hint");
  await h.click(".cards .card");
  await h.waitFor(visibleEl(".answers .answer"), "question screen");
  await checkMedia(type);
  const st = running(await saved((s) => running(s).current === q.id, "picked question"));
  seen(offered, st);
  await h.click(`.answers .answer:nth-child(${st.answers.indexOf(q.answer) + 1})`);
  await h.click(".final-button.ready");
  await h.waitFor(visibleEl(".result .title.good"), "correct screen", 30000);
  await h.click(".result .hint");
  await h.click(".level .hint");
}

/** `BUILD` without the packs' files (data and media, build/pack-media.json): hard links under `tmp`. */
function withoutPacks(tmp) {
  const media = JSON.parse(readFileSync(path.join(REPO, "app", "desktop", "build", "pack-media.json"), "utf8"));
  const dir = path.join(tmp, "linux-unpacked");
  const cp = spawnSync("cp", ["-al", BUILD, dir]);
  if (cp.status) throw new Error(`cp -al: ${cp.stderr}`);
  for (const b of Object.keys(media)) {
    spawnSync("rm", ["-rf", path.join(dir, BUNDLES, b)]);
    for (const f of media[b]) spawnSync("rm", ["-f", path.join(dir, "resources", "media", f)]);
  }
  return dir;
}

async function main() {
  if (!existsSync(path.join(BUILD, `${EXE}-bin`))) throw new Error(`${BUILD}: no unpacked Linux build (trivia-desktop-build${DEMO ? " --demo" : ""} --dir)`);
  DIR = BUILD;
  pickQuestions("es"); // fail early on a pool without media questions

  // Not /tmp: steam-run's sandbox has its own.
  await mkdir(path.join(REPO, "work"), { recursive: true });
  const tmp = await mkdtemp(path.join(REPO, "work", "smoke-"));
  try {
    at("Xvfb");
    const x = await startXvfb(which("Xvfb"), 1920, 1080);
    display = x.display;
    procs.push(x.proc);
    const built = packs();
    if (MATRIX) {
      await matrix(tmp);
      await finish("smoke --matrix: ok");
      return;
    }
    if (MULTI) {
      const runs = RUNS.filter((r) => !DEMO || BUILT_MODES.includes(r.mode));
      if (!runs.length) console.log("no built multiplayer mode");
      for (const [i, run] of runs.entries()) await multiplayer(path.join(tmp, `home-mp-${i}`), run);
      await finish("smoke --multiplayer: ok");
      return;
    }
    if (!MODS) console.log(built.length ? `with packs ${built.join(", ")}` : "no packs");
    if (MODS) await modsGame(path.join(tmp, "home-mods"));
    else {
      await game(path.join(tmp, "home"));
      await gamemasterGame(path.join(tmp, "home-gamemaster"));
    }
    if (!MODS && built.length) {
      at("without packs");
      DIR = withoutPacks(tmp);
      if (packs().length) throw new Error(`packs left: ${packs().join(", ")}`);
      await game(path.join(tmp, "home-nopacks"));
    }
    await finish(`smoke${MODS ? " --mods" : ""}: ok`);
  } finally {
    page?.close();
    for (const p of procs.reverse()) if (p.exitCode === null) p.kill();
    await sleep(500);
    await rm(tmp, { recursive: true, force: true });
  }
}

/** `--trace`'s file, then the verdict. */
async function finish(verdict) {
  if (TRACE) await writeFile(path.resolve(TRACE), JSON.stringify(trace, null, 1) + "\n");
  console.log(`${verdict}${DEMO ? " (demo)" : ""}`);
}

/** The memory-only notice (no valid Steam user) fails. */
async function noNotice() {
  if (await h.evaluate(visibleEl(".start .notice"))) {
    throw new Error(`notice: "${(await h.evaluate(`document.querySelector(".start .notice").textContent`)).trim()}"`);
  }
}

/** First start: language and consent screens, then the start screen, no memory-only notice. */
async function toStart() {
  const start = `${visibleEl('[data-focus-id="main"]')} || ${visibleEl(".start .notice")}`;
  await h.waitFor(`${visibleEl(".language .option")} || ${visibleEl(".consent .option")} || ${start}`, "first screen", 30000);
  if (await h.evaluate(visibleEl(".language .option"))) {
    at("language");
    await h.click(".language .option.current");
    await h.waitFor(`${visibleEl(".consent .option")} || ${start}`, "after language");
  }
  if (await h.evaluate(visibleEl(".consent .option"))) {
    at("consent");
    await h.click(".consent .option[data-focus-default]");
  }
  at("start screen");
  await h.waitFor(start, "start screen");
  await noNotice();
  if (DEMO) {
    const line = await h.evaluate(`document.querySelector(".start .demo")?.textContent.trim() ?? ""`);
    if (!line) throw new Error("no demo line on the Start screen");
  }
}

/** Start screen → a new player → the Mode screen. */
async function newPlayer() {
  at("new player");
  await h.click('[data-focus-id="main"]');
  await h.waitFor(visibleEl("#new-player"), "player screen");
  await h.evaluate(`(() => {
    const i = document.querySelector("#new-player");
    i.value = ${JSON.stringify(PLAYER)};
    i.dispatchEvent(new Event("input", { bubbles: true }));
  })()`);
  await h.click('.new button[type="submit"]');
}

/** Mode screens → age → the Bundles screen (packs show there; in the demo one tile, no pack) → Start: the bundles offered. */
async function chooseSingle(mode) {
  at(`mode ${mode}`);
  await h.click('[data-focus-id="kind-single"]');
  await h.click('[data-focus-id="next"]');
  await h.click(`[data-focus-id="mode-${mode}"]`);
  await h.click('[data-focus-id="next"]');
  if (mode === "solo") await h.click('[data-focus-id="group-young_teens"]'); // gamemaster: the settings screen, as defaulted
  await h.click('[data-focus-id="next"]');
  at("bundles");
  await h.waitFor(visibleEl('[data-focus-id="start"]'), "bundles screen");
  const offered = await h.evaluate(`JSON.stringify([...document.querySelectorAll(".bundles [data-focus-id^='bundle-']")]
    .map((b) => b.dataset.focusId.slice(7)))`);
  if (DEMO && offered !== '["base"]') throw new Error(`demo bundles offered: ${offered}, want base only`);
  await h.click('[data-focus-id="start"]');
  return offered;
}

/** One game in DIR with a fresh HOME: new player, levels 1–3, quit, restart resumes. */
async function game(dir) {
  home = dir;
  await mkdir(home);
  at("start");
  let shell = await launch();
  await toStart();
  await newPlayer();
  begin("solo");
  const offered = await chooseSingle("solo");
  await h.click(".level .hint");
  // The new game's question locale (plan 126: es unless the language has its own pool).
  const locale = (await saved((s) => s.games?.length, "new game")).games.at(-1).locale ?? "es";
  at("packs");
  const want = packsFor(locale).sort().join(", ") || "none";
  const { bundles } = JSON.parse(readFileSync(path.join(DIR, "resources", "data", "bundles.json"), "utf8"));
  const base = new Set(bundles.filter((b) => b.kind === "base").map((b) => b.id));
  const got = JSON.parse(offered).filter((b) => !base.has(b)).sort().join(", ") || "none";
  if (got !== want) throw new Error(`${locale} packs offered: ${got}; expected ${want}`);
  console.log(`  ${locale} packs offered: ${got}`);
  const picks = pickQuestions(locale);
  for (const p of picks) console.log(`  ${locale} ${p.type}: ${p.q.id} ${p.files.join(" ")}`);
  for (const [i, p] of picks.entries()) await playLevel(i + 1, p);
  const next = picks.length + 1;

  at("quit");
  await saved((s) => running(s).level === next && running(s).phase === "select", `level ${next}`);
  await quit(shell);
  if (!existsSync(saveFile())) throw new Error(`no save at ${saveFile()}`);

  at("restart");
  shell = await launch();
  await h.waitFor(`${visibleEl('[data-focus-id="main"]')} || ${visibleEl(".start .notice")}`, "start screen", 30000);
  await noNotice();
  const label = await h.evaluate(`document.querySelector('[data-focus-id="main"]').textContent`);
  if (!label.includes(PLAYER)) throw new Error(`no resume for ${PLAYER}: "${label.trim()}"`);
  at("resume");
  await h.click('[data-focus-id="main"]');
  await h.waitFor(`${visibleEl(".level .hint")} || ${visibleEl(".cards .card")}`, `level ${next}`);
  // Level screen's number, else the HUD's level chip (cards).
  const level = await h.evaluate(`document.querySelector(".level .title.big, .hud .level")?.textContent ?? ""`);
  if (!new RegExp(`\\b${next}\\b`).test(level)) throw new Error(`resumed at "${level.trim()}", not level ${next}`);
  await quit(shell);
  page.close();
  page = null;
}

/** The Gamemaster mode (every build): a fresh HOME, three levels on the first card, each answered right. */
async function gamemasterGame(dir) {
  home = dir;
  await mkdir(home);
  begin("gamemaster");
  at("gamemaster start");
  const shell = await launch();
  await toStart();
  await newPlayer();
  await chooseSingle("gamemaster");
  await h.click(".level .hint");
  const locale = (await saved((s) => s.games?.length, "new game")).games.at(-1).locale ?? "es";
  data = loadData(locale, path.join(DIR, "resources", "data"), DEMO);
  for (let level = 1; level <= 3; level++) {
    at(`gamemaster level ${level}`);
    await h.waitFor(visibleEl(".cards .card"), "cards");
    const offered = [...running(await saved((s) => running(s).phase === "select" && running(s).level === level, `level ${level} cards`)).options];
    await h.click(".cards .card");
    await h.waitFor(visibleEl(".answers .answer"), "question screen");
    if (await h.evaluate(visibleEl(".media-missing"))) throw new Error("missing-media notice on screen");
    const st = running(await saved((s) => running(s).phase === "question", "picked question"));
    seen(offered, st);
    await h.click(`.answers .answer:nth-child(${rightOf(st) + 1})`);
    await h.click(".final-button.ready");
    await h.waitFor(visibleEl(".result .title.good"), "correct screen", 30000);
    await h.click(".result .hint");
    await h.click(".level .hint");
  }
  await quit(shell);
  page.close();
  page = null;
}

const EXAMPLES = ["template-bundle", "examples/theme", "examples/rules-tweak"]; // load order, top first
const CONVERSION = "examples/conversion";
const userData = () => path.join(home, ".config", "trivia"); // main.mjs: appData/trivia when packaged
const modId = (rel) => JSON.parse(readFileSync(path.join(DIR, "modding", rel, "mod.json"), "utf8")).id;

/** <userData>/mods/<folder> from the build's modding/; mods.json as the shell writes it, notice accepted, `rels` on. */
async function installMods(rels) {
  for (const rel of rels) await cp(path.join(DIR, "modding", rel), path.join(userData(), "mods", path.basename(rel)), { recursive: true });
  const settings = { version: 1, mods: rels.map((rel) => ({ id: modId(rel), on: true })), notice: true, noticeAt: new Date().toISOString() };
  await writeFile(path.join(userData(), "mods.json"), JSON.stringify(settings, null, 2) + "\n");
}

/** `window.triviaShell.mods.list()` */
const modsList = () => h.evaluate("window.triviaShell.mods.list()");

/** Every id in `ids` loaded, no mod with an error. */
async function loaded(ids) {
  const { mods } = await modsList();
  const bad = mods.filter((m) => m.error || (ids.includes(m.id) && m.state !== "loaded"));
  const missing = ids.filter((id) => !mods.some((m) => m.id === id));
  if (bad.length || missing.length)
    throw new Error(`mods: ${[...bad.map((m) => `${m.id ?? m.dir} ${m.state}${m.error ? ` ${m.error.code}` : ""}`), ...missing.map((id) => `${id} not listed`)].join(", ")}`);
}

/** Shipped examples as a player's local mods: theme, player bundle, rules tweak; then the conversion; then --no-mods. */
async function modsGame(dir) {
  home = dir;
  await mkdir(home);
  for (const rel of [...EXAMPLES, CONVERSION])
    if (!existsSync(path.join(DIR, "modding", rel, "mod.json"))) throw new Error(`no modding/${rel} in the build`);
  at("install mods");
  await installMods(EXAMPLES);
  const ids = EXAMPLES.map(modId);
  const t0 = Date.now();
  at("start with mods");
  let shell = await launch();
  await toStart();
  at("mods loaded");
  await loaded(ids);
  at("theme");
  const css = readFileSync(path.join(DIR, "modding", "examples", "theme", "style.css"), "utf8");
  const [, name, value] = css.match(/(--[\w-]+):\s*([^;]+);/) ?? [];
  if (!name) throw new Error("no CSS variable in the theme's style.css");
  const got = await h.evaluate(`getComputedStyle(document.querySelector(".game")).getPropertyValue(${JSON.stringify(name)}).trim()`);
  if (got !== value.trim()) throw new Error(`${name} is "${got}", the theme sets "${value.trim()}"`);
  await newPlayer();
  at("player bundle");
  await h.click('[data-focus-id="kind-single"]');
  await h.click('[data-focus-id="next"]');
  await h.click('[data-focus-id="mode-solo"]');
  await h.click('[data-focus-id="next"]');
  await h.click('[data-focus-id="group-young_teens"]');
  await h.click('[data-focus-id="next"]');
  const tb = path.join(DIR, "modding", "template-bundle");
  const rows = JSON.parse(readFileSync(path.join(tb, "data", "bundles.json"), "utf8")).bundles;
  const bundle = `${modId("template-bundle")}:${rows[0].id}`;
  const tile = `[data-focus-id="bundle-${bundle}"]`;
  await h.waitFor(visibleEl(tile), `bundle ${bundle} offered`);
  if (!(await h.evaluate(visibleEl(`${tile} .made`)))) throw new Error(`bundle ${bundle} not marked player-made`);
  if ((await h.evaluate(`document.querySelector('${tile}').getAttribute("aria-checked")`)) !== "true") await h.click(tile);
  await h.click('[data-focus-id="start"]');
  const save = await saved((s) => s.games?.length, "new game");
  if (!running(save).settings?.bundles?.includes(bundle)) throw new Error(`game started without ${bundle}`);
  at("rules tweak");
  await h.waitFor(visibleEl('.side-tray [data-joker="hint"] .count'), "hint joker count");
  const hints = await h.evaluate(`document.querySelector('.side-tray [data-joker="hint"] .count').textContent.trim()`);
  if (hints !== "4") throw new Error(`hint jokers ${hints}, want 4 (3 + the rules tweak's one)`);
  await h.click(".level .hint");
  for (const [i, p] of pickQuestions(save.games.at(-1).locale ?? "es").entries()) await playLevel(i + 1, p);
  at("crash marker");
  await sleep(Math.max(0, t0 + 25000 - Date.now()));
  const marker = path.join(userData(), "mods-start.json");
  if (existsSync(marker)) throw new Error(`${marker} still there after 20 s`);
  await quit(shell);

  at("conversion");
  await installMods([CONVERSION, ...EXAMPLES]);
  shell = await launch();
  await h.waitFor(visibleEl("#guess"), "conversion's #guess", 30000);
  if (await h.evaluate(visibleEl('[data-focus-id="main"]'))) throw new Error("our start screen shows under the conversion");
  await loaded([CONVERSION, ...EXAMPLES].map(modId));
  await quit(shell);

  at("--no-mods");
  shell = await launch("--no-mods");
  await h.waitFor(visibleEl('[data-focus-id="main"]'), "our start screen", 30000);
  const list = await modsList();
  if (!list.noMods || list.safeStart?.reason !== "flag") throw new Error(`mods.list(): noMods ${list.noMods}, safeStart ${JSON.stringify(list.safeStart)}`);
  await quit(shell);
  page.close();
  page = null;
}

// Demo matrix (--demo --matrix) --------------------------------------------------------------------------------------

const SINGLE = ["solo", "gamemaster"];
/** The joker a winning matrix game plays per level, where its token is playable. */
const JOKER_AT = { 2: "hint", 4: "easier", 6: "skip", 8: "snipe", 10: "category" };

/** Every built mode × age group: a win, then a loss at level 3, 5, 7, … by the group's place. */
async function matrix(tmp) {
  const groups = JSON.parse(readFileSync(path.join(DIR, "resources", "data", "age-groups.json"), "utf8")).groups.map((g) => g.id);
  const multi = BUILT_MODES.filter((m) => !SINGLE.includes(m));
  if (multi.length) throw new Error(`no matrix games for multiplayer modes yet: ${multi.join(", ")}`);
  for (const mode of BUILT_MODES)
    for (const [i, group] of groups.entries()) {
      await matrixGame(path.join(tmp, `home-${mode}-${group}-win`), mode, group, groups, null);
      await matrixGame(path.join(tmp, `home-${mode}-${group}-loss`), mode, group, groups, 3 + 2 * i);
    }
}

/** The visible error lines (a refused start, a failed action). */
const errors = () => h.evaluate(`[...document.querySelectorAll(".error")].filter((e) => e.getClientRects().length).map((e) => e.textContent.trim()).join("; ")`);

/** One game in a fresh HOME: Choice (`group`) → Bundles → Start → every level on screen to a win (`wrongAt` null: first
 * card, jokers per JOKER_AT) or to the wrong answer at level `wrongAt` (last card). */
async function matrixGame(dir, mode, group, groups, wrongAt) {
  const label = `${mode} ${group} ${wrongAt ? "loss" : "win"}`;
  console.log(label);
  begin(label);
  home = dir;
  await mkdir(home);
  const shell = await launch();
  try {
    await toStart();
    await newPlayer();
    at(`${label}: choice`);
    await h.click('[data-focus-id="kind-single"]');
    await h.click('[data-focus-id="next"]');
    await h.click(`[data-focus-id="mode-${mode}"]`);
    await h.click('[data-focus-id="next"]');
    if (mode === "solo") await h.click(`[data-focus-id="group-${group}"]`);
    else {
      // The configure screen's difficulty line: the groups in order, a new player at the default one.
      const by = groups.indexOf(group) - groups.indexOf(DEFAULT_AGE_GROUP);
      for (let i = 0; i < Math.abs(by); i++)
        await h.click(`[data-focus-id="config-difficulty"] button.step:${by < 0 ? "first" : "last"}-of-type`);
    }
    await h.click('[data-focus-id="next"]');
    at(`${label}: bundles`);
    await h.waitFor(`${visibleEl('[data-focus-id="start"]')} || ${visibleEl(".bundles-screen .error")}`, "bundles screen");
    if (!(await h.evaluate(visibleEl('[data-focus-id="start"]')))) throw new Error(`start refused: ${await errors()}`);
    await h.click('[data-focus-id="start"]');
    const st0 = running(await saved((s) => s.games?.length, "new game"));
    if ((st0.settings.age_group ?? DEFAULT_AGE_GROUP) !== group || gameMode(st0) !== mode)
      throw new Error(`game started as ${gameMode(st0)} ${st0.settings.age_group}`);
    data = loadData(row(await saved(() => true, "save")).locale ?? "es", path.join(DIR, "resources", "data"), DEMO);
    const levels = st0.settings.levels ?? LEVELS;
    const which = wrongAt ? "last" : "first";
    for (let level = 1; ; level++) {
      at(`${label}: level ${level}`);
      await h.waitFor(`${visibleEl(".level .hint")} || ${visibleEl(".cards .card")}`, "level or cards", 30000);
      if (await h.evaluate(visibleEl(".level .hint"))) await h.click(".level .hint");
      let st = await openCard(level, which);
      if (!wrongAt && JOKER_AT[level]) st = await playJoker(JOKER_AT[level], st, level, which);
      const right = level !== wrongAt;
      const i = rightOf(st);
      await h.click(`.answers .answer:nth-child(${(right ? i : (i + 1) % st.answers.length) + 1})`);
      await h.click(".final-button.ready");
      if (!right || level === levels) break;
      await h.waitFor(visibleEl(".result .title.good"), "correct screen", 30000);
      await h.click(".result .hint");
    }
    at(`${label}: end`);
    await h.waitFor(visibleEl(wrongAt ? ".title.bad" : ".title.gold"), wrongAt ? "wrong screen" : "victory screen", 40000);
    const g = row(await saved((s) => row(s).result !== null && row(s).finished_on, "game over"));
    const want = wrongAt ? "lost" : "won";
    if (g.result !== want || g.state.level !== (wrongAt ?? levels)) throw new Error(`${g.result} at level ${g.state.level}, want ${want} at ${wrongAt ?? levels}`);
    console.log(`  ${label}: ${g.result} at level ${g.state.level}`);
    await quit(shell);
  } catch (e) {
    const shown = await errors().catch(() => "");
    throw new Error(`${e.message}${shown ? ` (on screen: ${shown})` : ""}`);
  } finally {
    if (shell.exitCode === null) shell.kill();
    page.close();
    page = null;
  }
}

/** The table at `level`: the `which` card picked, its question on screen (traced). */
async function openCard(level, which) {
  await h.waitFor(visibleEl(".cards .card"), "cards", 30000);
  const offered = [...running(await saved((s) => running(s).phase === "select" && running(s).level === level, `level ${level} cards`)).options];
  await sleep(500); // the table's arrival
  await h.evaluate(`[...document.querySelectorAll(".cards .card")].at(${which === "first" ? 0 : -1}).click()`);
  await h.waitFor(visibleEl(".answers .answer"), "question screen");
  if (await h.evaluate(visibleEl(".media-missing"))) throw new Error("missing-media notice on screen");
  const st = running(await saved((s) => running(s).phase === "question", "picked question"));
  seen(offered, st);
  return st;
}

/** `name` on the question on screen, if its token is playable (traced either way); the state after it (Paso: the next card's). */
async function playJoker(name, st, level, which) {
  const token = `.question-screen .token[data-joker="${name}"]`;
  await sleep(1000); // the screen's arrival
  if (!(await h.evaluate(visibleEl(token)))) {
    scene.questions.push({ level, joker: name, played: false });
    console.log(`  level ${level}: ${name} not playable`);
    return st;
  }
  at(`${scene.scene}: level ${level}: ${name}`);
  const used = jokersUsed(st)[name];
  await h.click(token);
  if (name === "hint" || name === "easier") await h.click(token); // armed, then played
  else if (name === "skip") await h.click(".dialog button.candy"); // «Paso», no purge
  else if (name === "category") {
    await h.click(".picker .grid .tile:not(:disabled)");
    await h.click(".picker .grid.subs .tile:not(:disabled)");
  } else {
    // Francotirador on a wrong answer; the crosshair starts on the first, a click on the target shoots.
    const wrong = st.answers.findIndex((_, i) => i !== rightOf(st));
    for (let n = wrong ? 2 : 1; n; n--) {
      await h.click(`.answers .answer:nth-child(${wrong + 1})`);
      await sleep(300);
    }
  }
  const after = running(await saved((s) => jokersUsed(running(s))[name] > used, `${name} played`));
  await sleep(3500); // the joker's animation; input waits for it
  if (name === "skip") {
    scene.questions.push({ level, joker: name });
    return openCard(level, which);
  }
  if (DEMO_IDS && !DEMO_IDS.has(after.current)) throw new Error(`question ${after.current} is not in the demo list`);
  scene.questions.push({ level, joker: name, shown: after.current, answers: after.answers, struck: after.struck });
  return after;
}

// Local multiplayer (--multiplayer) ----------------------------------------------------------------------------------

// A seat's device as the run drives it: a pad index, "kbm" (keyboard and mouse), "shared" (keyboard-only round-robin,
// decision 273) or a keyboard-only timed seat's claim key (decision 290).
const NAMES = [PLAYER, "Luna", "Mateo", "Sofía", "Max"];
const BTN = { A: 0, RB: 5, RT: 7, LEFT: 14 };
const PICK = [3, 1, 2, 0]; // answer i → Y, B, X, A (PAD_PICKS)
const WINS = { "rr-coop": "WIN_RR_COOP", "rr-competitive": "WIN_RR_COMPETITIVE", timed: "WIN_TIMED" };
const LOST = ".dialog[aria-labelledby='seat-lost-title']";
const PADS3 = [0, 1, 2];
const SHARED3 = ["shared", "shared", "shared"];
const FIVE = [0, 1, 2, 3, "kbm"];
const FAKE_PADS = readFileSync(path.join(REPO, "authoring", "tools", "fake_pads.js"), "utf8");

const row = (save) => save.games.at(-1);
/** A seat's own game (rr-competitive), else the session's. */
const stateOf = (g, seat) => g.seats[seat].state ?? g.state;
let data;
const rightOf = (st) => st.answers.indexOf(data.byId.get(st.current).answer);
let seed = 1;
const io = (ms) => ({ rng: seededRng(seed++), now: new Date().toISOString().slice(0, 19), ms });

/** A real (trusted) key press: the seat filter drops untrusted input only for clicks. */
async function key(k) {
  const named = { Enter: ["Enter", 13, "\r"], " ": ["Space", 32, " "] }[k];
  const [code, vk, text] = named ?? [/\d/.test(k) ? `Digit${k}` : `Key${k.toUpperCase()}`, k.toUpperCase().charCodeAt(0), k];
  await page.send("Input.dispatchKeyEvent", { type: "keyDown", key: k, code, windowsVirtualKeyCode: vk, text });
  await page.send("Input.dispatchKeyEvent", { type: "keyUp", key: k, code, windowsVirtualKeyCode: vk });
  await sleep(200);
}

/** A real mouse click on `sel`'s centre. */
async function mouse(sel) {
  await h.waitFor(visibleEl(sel), sel);
  const [x, y] = await h.evaluate(`(() => { const r = document.querySelector(${JSON.stringify(sel)}).getBoundingClientRect();
    return [r.x + r.width / 2, r.y + r.height / 2]; })()`);
  await page.send("Input.dispatchMouseEvent", { type: "mouseMoved", x, y });
  for (const type of ["mousePressed", "mouseReleased"]) await page.send("Input.dispatchMouseEvent", { type, x, y, button: "left", clickCount: 1 });
  await sleep(200);
}

const padPress = (button, i) => h.evaluate(`window.__press(${button}, ${i})`);

/** `seat` presses `what`: confirm, card (the first), answer `n`, submit, claim. Keyboard and mouse: cards and answers
 * by mouse, the rest by keys. */
async function press(r, seat, what, n = 0) {
  const b = r.seats[seat];
  if (typeof b === "number") {
    if (what === "card") await padPress(BTN.LEFT, b); // the ring on the first card; A presses only a ringed control
    return padPress({ confirm: BTN.A, card: BTN.A, answer: PICK[n], submit: BTN.RT, claim: BTN.RB }[what], b);
  }
  if (b === "kbm" && what === "card") return mouse(".cards .card");
  if (b === "kbm" && what === "answer") return mouse(`.answers .answer:nth-child(${n + 1})`);
  await key({ confirm: "Enter", card: "1", answer: String(n + 1), submit: "Enter", claim: b === "kbm" ? " " : b }[what]);
}

/** What is on screen, coarsely. */
const SCREEN = `[".level .hint", ".cards .card", ".answers .answer", ".final-button.ready", ".title.good", ".title.bad",
  ".title.gold", ${JSON.stringify(LOST)}].map((s) => ${visibleEl("__").replace('"__"', "s")}).join("")`;

/** A press from `seat`, which may not act now, changes neither the save nor the screen. */
async function refused(r, seat, what, n) {
  at(`${r.label}: seat ${seat}'s ${what} refused`);
  const save = await readFile(saveFile(), "utf8");
  const screen = await h.evaluate(SCREEN);
  await press(r, seat, what, n);
  await sleep(1000);
  if ((await readFile(saveFile(), "utf8")) !== save) throw new Error(`seat ${seat}'s ${what} changed the save`);
  if ((await h.evaluate(SCREEN)) !== screen) throw new Error(`seat ${seat}'s ${what} changed the screen`);
}

/** The lost-seat dialog for `seat` (decision 289), if up: its pad's A takes it. */
async function rebind(r, seat) {
  await sleep(300);
  if (!(await h.evaluate(visibleEl(LOST)))) return false;
  const name = await h.evaluate(`document.querySelector("#seat-lost-title").textContent`);
  if (!name.includes(NAMES[seat])) throw new Error(`lost-seat dialog "${name.trim()}", want seat ${seat} (${NAMES[seat]})`);
  at(`${r.label}: pad ${r.seats[seat]} takes seat ${seat}`);
  await padPress(BTN.A, r.seats[seat]);
  await h.waitFor(`!${visibleEl(LOST)} || !document.querySelector("#seat-lost-title").textContent.includes(${JSON.stringify(NAMES[seat])})`, "seat taken");
  return true;
}

/** A launch with `n` fake pads, at load and after every reload; the page counts as focused (the pad loop polls only then). */
async function launchPads(n) {
  const shell = await launch();
  const source = `(${FAKE_PADS})(${JSON.stringify(Array(n).fill(null))})`;
  await page.send("Page.enable");
  await page.send("Page.addScriptToEvaluateOnNewDocument", { source });
  await page.send("Emulation.setFocusEmulationEnabled", { enabled: true });
  await h.evaluate(`${source}; window.__pads(${n}); true`);
  return shell;
}

async function setText(sel, text) {
  await h.waitFor(visibleEl(sel), sel);
  await h.evaluate(`(() => {
    const i = document.querySelector(${JSON.stringify(sel)});
    i.value = ${JSON.stringify(text)};
    i.dispatchEvent(new Event("input", { bubbles: true }));
  })()`);
}

/** Mode → Join (every seat, its device, its name) → Choice (age) → Bundles → the session's first screen. */
async function setup(r) {
  at(`${r.label}: mode`);
  await h.click('[data-focus-id="kind-multi"]');
  await h.click('[data-focus-id="next"]');
  await h.click(`[data-focus-id="mode-${r.mode}"]`);
  await h.click('[data-focus-id="next"]');
  await ready(visibleEl(".join .seat.open"), "join screen"); // a pad press right on arrival is lost
  for (const [i, b] of r.seats.entries()) {
    at(`${r.label}: join seat ${i} (${b})`);
    if (typeof b === "number") await padPress(BTN.A, b);
    else {
      await h.click('[data-focus-id="join-keyboard"]');
      if (b.length === 1) await setText(".key-field", b);
    }
    await h.waitFor(visibleEl(`[data-focus-id="seat-name-${i}"]`), `seat ${i}`);
    if (!i) continue;
    await h.click(`[data-focus-id="seat-name-${i}"]`);
    await setText(".backdrop #new-player", NAMES[i]);
    await h.click('.backdrop .new button[type="submit"]');
    await h.waitFor(`document.querySelector('[data-focus-id="seat-name-${i}"]')?.textContent.includes(${JSON.stringify(NAMES[i])})`, `seat ${i} named`);
  }
  at(`${r.label}: age, bundles`);
  await h.click('[data-focus-id="next"]');
  await h.click('[data-focus-id="next"]');
  await h.click('[data-focus-id="start"]');
  const save = await saved((s) => s.games?.length && row(s).seats, "session started");
  data = loadData(row(save).locale ?? "es", path.join(DIR, "resources", "data"), DEMO);
  const want = r.seats.map((b) => (typeof b === "number" ? { pad: b } : b === "kbm" || b === "shared" ? b : { key: b }));
  const bound = await h.evaluate(`sessionStorage.getItem("trivia.seats.${row(save).id}")`);
  if (bound !== JSON.stringify(want)) throw new Error(`seats bound ${bound}, want ${JSON.stringify(want)}`);
}

/** `expr` holds, then a moment for the screen's transition (input waits while it runs). */
async function ready(expr, what, ms = 30000) {
  await h.waitFor(expr, what, ms);
  await sleep(1000);
}

/** One round-robin turn through the screens by the seat on turn: Level, the first card (`off` presses first, refused),
 * the answer, the result and its «Seguir». */
async function turn(r, right, off) {
  const before = await saved((s) => { const g = row(s); return g.result === null && stateOf(g, g.turn).phase === "select"; }, "a table");
  const seat = row(before).turn;
  const level = stateOf(row(before), seat).level;
  at(`${r.label}: seat ${seat}, level ${level}`);
  await ready(visibleEl(".level .hint"), "level screen");
  await rebind(r, seat);
  await press(r, seat, "confirm");
  await ready(visibleEl(".cards .card"), "cards");
  if (off !== undefined) await refused(r, off, "card");
  await press(r, seat, "card");
  const st = stateOf(row(await saved((s) => stateOf(row(s), seat).phase === "question", "card picked")), seat);
  seen(stateOf(row(before), seat).options, st);
  await ready(visibleEl(".answers .answer:not(:disabled)"), "question screen");
  const i = rightOf(st);
  await press(r, seat, "answer", right ? i : (i + 1) % st.answers.length);
  await h.waitFor(visibleEl(".final-button.ready"), "answer locked");
  await press(r, seat, "submit");
  const after = await saved((s) => stateOf(row(s), seat).history.length > st.history.length, "answered");
  const g = row(after);
  if (!right) {
    await ready(visibleEl(".title.bad"), "wrong screen");
    if (r.mode === "rr-competitive") {
      if (!g.seats[seat].out) throw new Error(`seat ${seat} not out after a wrong answer`);
      await press(r, seat, "confirm"); // «Seguir»: Wrong is every seat's
      if (g.result === null) await h.waitFor(visibleEl(".level .hint"), "next turn", 30000);
    } else if (g.result !== "lost") throw new Error(`team result ${g.result} after a wrong answer`);
  } else if (g.result === null) {
    await ready(visibleEl(".title.good"), "correct screen");
    await rebind(r, g.turn);
    await press(r, g.turn, "confirm");
  }
  if (g.result === "won") await h.waitFor(visibleEl(".title.gold"), "victory screen", 40000);
  return after;
}

/** The engine plays on the save (each turn its first card, right) until `until`; the page reloads and resumes. */
async function forward(r, until, what) {
  at(`${r.label}: engine to ${what}`);
  let save = await saved(() => true, "save");
  while (!until(save)) {
    const seat = row(save).turn;
    ({ save } = pick(save, data, io(), 0, seat));
    ({ save } = answer(save, data, io(), rightOf(stateOf(row(save), seat)), seat));
  }
  await writeFile(saveFile(), JSON.stringify(save));
  await page.send("Page.reload", { ignoreCache: true });
  await resume(r);
}

async function resume(r) {
  at(`${r.label}: resume`);
  await h.waitFor(visibleEl('[data-focus-id="main"]'), "start screen", 30000);
  await sleep(500);
  await h.click('[data-focus-id="main"]');
}

/** The question on screen with its clock running, the `n`th of the session. */
async function shown(n) {
  await saved((s) => row(s).result === null && row(s).state.history.length === n && row(s).state.timed.shown_at !== null, `question ${n + 1} shown`, 40000);
  await h.waitFor(visibleEl(".timed-screen .answers"), "timed question", 30000);
}

/** Timed: `seat` claims the question on screen (`off` presses claim and an answer, refused) and answers right, wrong,
 * or lets the 6 s run out. */
async function claims(r, seat, how, off) {
  const n = row(await saved(() => true, "save")).state.history.length;
  await shown(n);
  at(`${r.label}: seat ${seat} claims, ${how}`);
  await press(r, seat, "claim");
  const save = await saved((s) => row(s).state.timed.claim?.seat === seat, `seat ${seat}'s claim`);
  if (off !== undefined) {
    await refused(r, off, "claim");
    // a key seat's answer keys act for the claimer (decision 290)
    if (typeof r.seats[off] === "number" || r.seats[off] === "kbm") await refused(r, off, "answer", 0);
  }
  seen([], row(save).state);
  const i = rightOf(row(save).state);
  if (how !== "timeout") await press(r, seat, "answer", how === "right" ? i : (i + 1) % row(save).state.answers.length);
  const after = await saved((s) => row(s).state.history.length > n, "question ended", 15000);
  const h0 = row(after).state.history[n];
  if (h0.seat !== seat || h0.correct !== (how === "right") || !!h0.timeout !== (how === "timeout"))
    throw new Error(`question ${n + 1}: ${JSON.stringify(h0)}, want seat ${seat} ${how}`);
  if (how !== "right" && !row(after).seats[seat].out) throw new Error(`seat ${seat} not out`);
  return after;
}

/** Timed: the engine plays on the save, each question right by a seat still without one this round, until `until`. */
function timedForward(save, until) {
  let ms = Math.max(Date.now() - 10000, row(save).state.timed.shown_at ?? 0);
  const tick = () => io((ms += 50));
  while (!until(save)) {
    const g = row(save);
    const t = g.state.timed;
    if (t.shown_at === null) ({ save } = show(save, data, tick()));
    const left = g.seats.flatMap((s, i) => (s.out ? [] : [i]));
    const seat = left.find((i) => !t.round_correct.includes(i)) ?? left[0];
    ({ save } = claim(save, data, tick(), seat));
    ({ save } = answer(save, data, tick(), rightOf(row(save).state), seat));
  }
  return save;
}

/** The end: one games[] row with the seats in join order (decision 277), finished; the win achievement with a win
 * (decision 285); the end screen's confirm goes to Start, no resume. */
async function ended(r, end) {
  at(`${r.label}: ${end}`);
  const save = await saved((s) => row(s).result !== null && row(s).finished_on, "session over");
  if (save.games.length !== 1) throw new Error(`${save.games.length} games[] rows, want 1`);
  const g = row(save);
  const names = g.seats.map((s) => save.players.find((p) => p.id === s.player_id)?.name);
  if (names.join() !== NAMES.slice(0, r.seats.length).join()) throw new Error(`seats ${names.join(", ")}`);
  const win = earned(save, data).includes(WINS[r.mode]);
  if (win !== (g.result === "won")) throw new Error(`result ${g.result}, ${WINS[r.mode]} ${win ? "" : "not "}earned`);
  await ready(`${visibleEl(".title.gold")} || ${visibleEl(".title.bad")}`, "end screen", 40000);
  await press(r, 0, "confirm"); // the end screens are every seat's
  await h.waitFor(visibleEl('[data-focus-id="main"]'), "start screen", 20000);
  const label = await h.evaluate(`document.querySelector('[data-focus-id="main"]').textContent`);
  if (label.includes(PLAYER)) throw new Error(`a resume after the end: "${label.trim()}"`);
  console.log(`  ${r.label}: ${end}, ${g.result}${win ? `, ${WINS[r.mode]}` : ""}`);
}

/** Quit, start again, resume: pad seats wait for a pad and take it (decision 289), the others never ask
 * (decision 321). */
async function restarted(r) {
  at(`${r.label}: quit`);
  await quit(r.shell);
  at(`${r.label}: restart`);
  const pads = r.seats.flatMap((b, i) => (typeof b === "number" ? [i] : []));
  r.shell = await launchPads(pads.length);
  await resume(r);
  if (pads.length) {
    await h.waitFor(visibleEl(LOST), "lost-seat dialog", 20000);
    for (const seat of pads) if (!(await rebind(r, seat))) throw new Error(`no lost-seat dialog for seat ${seat}`);
  } else await sleep(2000);
  if (await h.evaluate(visibleEl(LOST))) throw new Error("lost-seat dialog after the restart");
}

const levelOf = (s, seat) => stateOf(row(s), seat).level;
const at12 = (seat) => (s) => row(s).turn === seat && levelOf(s, seat) === 12 && stateOf(row(s), seat).phase === "select";

const RUNS = [
  {
    mode: "rr-coop", seats: PADS3, async play(r) {
      await turn(r, true, 1);
      await turn(r, true, 0);
      await forward(r, (s) => levelOf(s, 0) === 12, "level 12");
      await turn(r, true, (row(await saved(() => true, "save")).turn + 1) % 3);
      await ended(r, "team win");
    },
  },
  {
    mode: "rr-coop", seats: SHARED3, async play(r) {
      await turn(r, true);
      await restarted(r);
      await turn(r, true);
      await turn(r, false);
      await ended(r, "team loss");
    },
  },
  {
    mode: "rr-coop", seats: FIVE, async play(r) {
      await turn(r, true, 4); // keyboard and mouse off turn: a click on a card
      for (let i = 1; i < 4; i++) await turn(r, true);
      await turn(r, true, 0); // a pad while keyboard and mouse are on turn
      await forward(r, (s) => levelOf(s, 0) === 12, "level 12");
      await turn(r, true);
      await ended(r, "team win");
    },
  },
  {
    mode: "rr-competitive", seats: PADS3, async play(r) {
      await turn(r, true, 2);
      await turn(r, false); // seat 1 out
      await turn(r, true, 1); // an out seat's pad
      await forward(r, at12(0), "seat 0 at level 12");
      await turn(r, true);
      await ended(r, "first to 12");
    },
  },
  {
    mode: "rr-competitive", seats: SHARED3, async play(r) {
      await turn(r, false);
      await turn(r, false);
      await ended(r, "last standing");
    },
  },
  {
    mode: "rr-competitive", seats: FIVE, async play(r) {
      await turn(r, true, 4);
      for (let i = 1; i < 4; i++) await turn(r, true);
      await turn(r, true, 3);
      await forward(r, at12(0), "seat 0 at level 12");
      await turn(r, true);
      await ended(r, "first to 12");
    },
  },
  {
    mode: "timed", seats: PADS3, async play(r) {
      await claims(r, 0, "right", 1);
      await claims(r, 1, "timeout", 2); // the 6 s run out: out
      const save = await claims(r, 0, "right");
      const lives = row(save).seats.map((s) => s.lives);
      if (lives[2] !== 2 || lives[0] !== 3) throw new Error(`lives after round 1: ${lives.join(", ")}`);
      console.log(`  ${r.label}: round 1 lives ${lives.join(", ")}`);
      await this.restart(r);
      await claims(r, 2, "right", 0);
      await ended(r, "sudden-death win");
    },
    /** Quit on round 2, the engine on to round 12 (sudden death), restart: resume, every pad takes its seat again. */
    async restart(r) {
      await h.waitFor(visibleEl("main .screen.round"), "round 2 screen", 30000);
      at(`${r.label}: quit`);
      await quit(r.shell);
      const save = timedForward(JSON.parse(await readFile(saveFile(), "utf8")),
        (s) => row(s).state.level === 12 && row(s).state.timed.round_done === 0);
      await writeFile(saveFile(), JSON.stringify(save));
      at(`${r.label}: restart`);
      r.shell = await launchPads(r.seats.length);
      await resume(r);
      await h.waitFor(visibleEl(LOST), "lost-seat dialog", 20000);
      for (const seat of [0, 2]) if (!(await rebind(r, seat))) throw new Error(`no lost-seat dialog for seat ${seat}`);
      if (await h.evaluate(visibleEl(LOST))) throw new Error("lost-seat dialog for a seat that is out");
    },
  },
  {
    mode: "timed", seats: ["j", "q", "x"], async play(r) {
      await claims(r, 0, "wrong", 1);
      await restarted(r);
      await claims(r, 1, "wrong", 2);
      await ended(r, "last standing");
    },
  },
  {
    mode: "timed", seats: FIVE, async play(r) {
      await claims(r, 4, "right", 0);
      await restarted(r); // pads rebind, keyboard and mouse needs no pad
      await claims(r, 4, "right");
      for (let i = 0; i < 4; i++) await claims(r, i, "wrong", i ? undefined : 4);
      await ended(r, "last standing");
    },
  },
];

/** One session in a fresh HOME. */
async function multiplayer(dir, r) {
  r.label = `${r.mode} ${r.seats.map((b) => (typeof b === "number" ? "pad" : b)).join("+")}`;
  console.log(r.label);
  begin(r.label);
  home = dir;
  await mkdir(home);
  seed = 1;
  r.shell = await launchPads(r.seats.filter((b) => typeof b === "number").length);
  await toStart();
  await newPlayer();
  await setup(r);
  await r.play(r);
  await quit(r.shell);
  page.close();
  page = null;
}

main().catch((e) => {
  console.error(`smoke: ${step}: ${e.message}`);
  process.exitCode = 1;
});
