#!/usr/bin/env node
// Packaged smoke game (plan 89, release check step 6): the unpacked Linux build offline, clean env, temp HOME.
// Usage (dev shell): node authoring/steam/smoke.mjs [app/desktop/release/linux-unpacked]; DEBUG=1 shows the shell's stderr
// New player → levels 1–3 with an image, audio and video question → quit → restart resumes. Exit 1 names the step.
import { spawn } from "node:child_process";
import { accessSync, constants, existsSync, readFileSync } from "node:fs";
import { mkdir, mkdtemp, readFile, rm, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { cacheName } from "../../app/desktop/resolve.mjs";
import { connectPipe, pageHelpers, sleep, visibleEl } from "../tools/cdp.mjs";

const REPO = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..", "..");
const DIR = path.resolve(process.argv[2] ?? path.join(REPO, "app", "desktop", "release", "linux-unpacked"));
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

/** The first question per media type in the shipped pool; their media files. */
function pickQuestions() {
  const pool = JSON.parse(readFileSync(path.join(DIR, "resources", "data", "pool.json"), "utf8"));
  return TYPES.map((type) => {
    const q = pool.questions.find((x) => x.media?.type === type && x.media.file_url);
    if (!q) throw new Error(`no ${type} question in the pool`);
    const urls = [q.media.file_url, q.background?.file_url].filter(Boolean);
    return { type, q, files: urls.map((u) => path.join("resources", "media", cacheName(u))) };
  });
}

let page, h, home, display;
const procs = [];

const saveFile = () => path.join(home, ".config", "trivia", "save", "local", "game.json");
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
  const env = [`HOME=${home}`, `DISPLAY=${display}`, "TRIVIA_DEVTOOLS=1"];
  // unshare -rn: no network; env -i + steam-run: no Nix shell env, an FHS runtime like a Steam Linux machine.
  const shell = spawn("unshare", ["-rn", "env", "-i", ...env, steamRun, path.join(DIR, "trivia"), "--remote-debugging-pipe"], {
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
  await h.evaluate("window.trivia.quit()").catch(() => {}); // the page goes away mid-call
  await Promise.race([exited, sleep(10000).then(() => Promise.reject(new Error("shell didn't exit")))]);
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

async function main() {
  if (!existsSync(path.join(DIR, "trivia-bin"))) throw new Error(`${DIR}: no unpacked Linux build (trivia-desktop-build --dir)`);
  const picks = pickQuestions();
  for (const p of picks) console.log(`  ${p.type}: ${p.q.id} ${p.files.join(" ")}`);

  // Not /tmp: steam-run's sandbox has its own.
  await mkdir(path.join(REPO, "work"), { recursive: true });
  home = await mkdtemp(path.join(REPO, "work", "smoke-"));
  display = `:${90 + Math.floor(Math.random() * 400)}`;
  try {
    at("Xvfb");
    const x = spawn(which("Xvfb"), [display, "-screen", "0", "1920x1080x24", "-nolisten", "tcp"], { stdio: "ignore" });
    procs.push(x);
    await sleep(1000);

    at("start");
    let shell = await launch();
    await h.waitFor(`${visibleEl(".language .option")} || ${visibleEl('[data-focus-id="main"]')}`, "first screen", 30000);
    if (await h.evaluate(visibleEl(".language .option"))) {
      at("language");
      await h.click(".language .option.current");
    }
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
    await h.click('[data-focus-id="mode-solo"]');
    await h.click('[data-focus-id="group-young_teens"]');
    await h.click('[data-focus-id="start"]');
    await h.click(".level .hint");
    for (const [i, p] of picks.entries()) await playLevel(i + 1, p);

    at("quit");
    await saved((s) => running(s).level === 4 && running(s).phase === "select", "level 4");
    await quit(shell);

    at("restart");
    shell = await launch();
    await h.waitFor(visibleEl('[data-focus-id="main"]'), "start screen", 30000);
    const label = await h.evaluate(`document.querySelector('[data-focus-id="main"]').textContent`);
    if (!label.includes(PLAYER)) throw new Error(`no resume for ${PLAYER}: "${label.trim()}"`);
    at("resume");
    await h.click('[data-focus-id="main"]');
    await h.waitFor(`${visibleEl(".level .hint")} || ${visibleEl(".cards .card")}`, "level 4");
    const level = await h.evaluate(`document.querySelector(".level .title, .hud")?.textContent ?? ""`);
    if (!/4/.test(level)) throw new Error(`resumed at "${level.trim()}", not level 4`);
    await quit(shell);
    console.log("smoke: ok");
  } finally {
    page?.close();
    for (const p of procs.reverse()) if (p.exitCode === null) p.kill();
    await sleep(500);
    await rm(home, { recursive: true, force: true });
  }
}

main().catch((e) => {
  console.error(`smoke: ${step}: ${e.message}`);
  process.exitCode = 1;
});
