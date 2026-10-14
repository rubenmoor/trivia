#!/usr/bin/env node
// Packaged smoke game (plan 89, release check step 6): the unpacked Linux build offline, clean env, temp HOME,
// TRIVIA_DEV_STEAM_USER=1 (decision 111: saves need a valid Steam user; the switch stands in for one).
// Usage (dev shell): node authoring/steam/smoke.mjs [app/desktop/release/linux-unpacked]; DEBUG=1 shows the shell's stderr
// New player → levels 1–3 with an image, audio and video question → quit → restart resumes; no «progress needs Steam»
// notice. Exit 1 names the step.
// With packs (DLC depots, decision 66): once as built (packs offered), once without their files (not offered).
import { spawn, spawnSync } from "node:child_process";
import { accessSync, constants, existsSync, readdirSync, readFileSync } from "node:fs";
import { mkdir, mkdtemp, readFile, rm, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { cacheName } from "../../app/desktop/resolve.mjs";
import { connectPipe, pageHelpers, sleep, startXvfb, visibleEl } from "../tools/cdp.mjs";

const REPO = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..", "..");
const BUILD = path.resolve(process.argv[2] ?? path.join(REPO, "app", "desktop", "release", "linux-unpacked"));
const BUNDLES = path.join("resources", "data", "bundles");
const TYPES = ["image", "audio", "video"]; // levels 1–3
const PLAYER = "Smoke";

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
  const pool = JSON.parse(readFileSync(path.join(DIR, "resources", "data", file), "utf8"));
  return TYPES.map((type) => {
    const q = pool.questions.find((x) => x.media?.type === type && x.media.file_url);
    if (!q) throw new Error(`no ${type} question in the pool`);
    const urls = [q.media.file_url, q.background?.file_url].filter(Boolean);
    return { type, q, files: urls.map((u) => path.join("resources", "media", cacheName(u))) };
  });
}

let DIR, page, h, home, display;
const procs = [];

const saveFile = () => path.join(home, ".config", "trivia", "save", "dev", "game.json") // decision 114;
const running = (save) => save.games.at(-1).state;

/** The save on disk once `test` holds (the shell writes after each action). */
async function saved(test, what) {
  for (const end = Date.now() + 10000; Date.now() < end; await sleep(100)) {
    try {
      const save = JSON.parse(await readFile(saveFile(), "utf8"));
      if (test(save)) return save;
    } catch {}
  }
  throw new Error(`save: ${what}`);
}

async function launch() {
  const steamRun = which("steam-run");
  // Muted: checks media load, not audio; sound is a manual row.
  const env = [`HOME=${home}`, `DISPLAY=${display}`, "TRIVIA_DEVTOOLS=1", "TRIVIA_MUTE=1", "TRIVIA_DEV_STEAM_USER=1"];
  // unshare -rn: no network; env -i + steam-run: no Nix shell env, an FHS runtime like a Steam Linux machine.
  const shell = spawn("unshare", ["-rn", "env", "-i", ...env, steamRun, path.join(DIR, "trivia"), "--lang=es", "--remote-debugging-pipe"], {
    stdio: ["ignore", "ignore", "pipe", "pipe", "pipe"],
  });
  shell.stderr.on("data", (d) => process.env.DEBUG && process.stderr.write(d));
  procs.push(shell);
  page = await connectPipe(shell);
  h = pageHelpers(page);
  return shell;
}

async function quit(shell) {
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
  if (!existsSync(path.join(BUILD, "trivia-bin"))) throw new Error(`${BUILD}: no unpacked Linux build (trivia-desktop-build --dir)`);
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
    console.log(built.length ? `with packs ${built.join(", ")}` : "no packs");
    await game(path.join(tmp, "home"));
    if (built.length) {
      at("without packs");
      DIR = withoutPacks(tmp);
      if (packs().length) throw new Error(`packs left: ${packs().join(", ")}`);
      await game(path.join(tmp, "home-nopacks"));
    }
    console.log("smoke: ok");
  } finally {
    page?.close();
    for (const p of procs.reverse()) if (p.exitCode === null) p.kill();
    await sleep(500);
    await rm(tmp, { recursive: true, force: true });
  }
}

/** The memory-only notice (no valid Steam user) fails. */
async function noNotice() {
  if (await h.evaluate(visibleEl(".start .notice"))) {
    throw new Error(`notice: "${(await h.evaluate(`document.querySelector(".start .notice").textContent`)).trim()}"`);
  }
}

/** One game in DIR with a fresh HOME: new player, levels 1–3, quit, restart resumes. */
async function game(dir) {
  home = dir;
  await mkdir(home);
  at("start");
  let shell = await launch();
  await h.waitFor(`${visibleEl(".language .option")} || ${visibleEl('[data-focus-id="main"]')} || ${visibleEl(".start .notice")}`, "first screen", 30000);
  if (await h.evaluate(visibleEl(".language .option"))) {
    at("language");
    await h.click(".language .option.current");
  }
  at("start screen");
  await h.waitFor(`${visibleEl('[data-focus-id="main"]')} || ${visibleEl(".start .notice")}`, "start screen");
  await noNotice();
  at("new player");
  await h.click('[data-focus-id="main"]');
  await h.waitFor(visibleEl("#new-player"), "player screen");
  await h.evaluate(`(() => {
    const i = document.querySelector("#new-player");
    i.value = ${JSON.stringify(PLAYER)};
    i.dispatchEvent(new Event("input", { bubbles: true }));
  })()`);
  await h.click('.new button[type="submit"]');
  at("mode");
  // Packs show in gamemaster mode's bundle selector.
  await h.click('[data-focus-id="mode-gamemaster"]');
  await h.waitFor(visibleEl(".bundles"), "bundle selector");
  const offered = await h.evaluate(`JSON.stringify([...document.querySelectorAll(".bundles [data-focus-id^='bundle-']")]
    .map((b) => b.dataset.focusId.slice(7)))`);
  await h.click('[data-focus-id="mode-solo"]');
  await h.click('[data-focus-id="group-young_teens"]');
  await h.click('[data-focus-id="start"]');
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

  at("quit");
  await saved((s) => running(s).level === 4 && running(s).phase === "select", "level 4");
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
  await h.waitFor(`${visibleEl(".level .hint")} || ${visibleEl(".cards .card")}`, "level 4");
  // Level screen's number, else the HUD's level chip (cards).
  const level = await h.evaluate(`document.querySelector(".level .title.big, .hud .level")?.textContent ?? ""`);
  if (!/4/.test(level)) throw new Error(`resumed at "${level.trim()}", not level 4`);
  await quit(shell);
  page.close();
  page = null;
}

main().catch((e) => {
  console.error(`smoke: ${step}: ${e.message}`);
  process.exitCode = 1;
});
