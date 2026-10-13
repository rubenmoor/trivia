#!/usr/bin/env node
// Store screenshots (plan 88, PUB-8): the shell at 1920×1080 under Xvfb, raw CDP, a demo save per shot.
// Usage (dev shell): node authoring/store/screenshots.mjs [--lang en,es,es-ES,de] [--visible]
// Needs app/client/dist (`npm run build`) and the media cache (`trivia-media sync --status approved`).
import { spawn } from "node:child_process";
import { existsSync, readFileSync } from "node:fs";
import { mkdir, mkdtemp, rm, writeFile } from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { cacheName } from "../../app/desktop/resolve.mjs";
import { connectPort, freePort, pageHelpers, sleep, startXvfb, visibleEl } from "../tools/cdp.mjs";
import { answer, newGame, pick } from "../../app/client/src/engine/game.ts";
import { bundleFile, loadCategories, packsFor, parseAgeGroups, parseBundles, parsePool, poolFile, withPacks } from "../../app/client/src/engine/pool.ts";
import { seededRng } from "../../app/client/src/engine/rng.ts";
import { emptySave, engineData, mergeNames, SAVE_VERSION } from "../../app/client/src/engine/state.ts";

const REPO = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..", "..");
const DATA = path.join(REPO, "app", "data");
const OUT = path.join(REPO, "authoring", "store", "out", "screenshots");
const MEDIA = process.env.TRIVIA_MEDIA || path.join(REPO, "media"); // as the shell's roots()
const W = 1920;
const H = 1080;

// Made-up players, no family data; the first one plays.
const PLAYERS = ["Luna", "Mateo", "Sofía", "Max", "Emma"];
// Shots' questions (es pool): picture, video, joker, the last level.
const Q = { image: "q-0030", video: "q-0055", joker: "q-0019", final: "q-0053" };

const args = process.argv.slice(2);
const opt = (name) => {
  const i = args.indexOf(name);
  return i >= 0 ? args[i + 1] : undefined;
};
const LANGS = (opt("--lang") ?? "en,es,es-ES,de").split(",");
const visible = args.includes("--visible");

const json = (file) => JSON.parse(readFileSync(path.join(DATA, file), "utf8"));

/** data.ts's load(), from disk; null if the locale has no pool. */
function loadData(locale) {
  const file = poolFile(locale);
  if (!existsSync(path.join(DATA, file))) return null;
  const bundles = json("bundles.json");
  const optional = (f) => (existsSync(path.join(DATA, f)) ? json(f) : null);
  const all = parseBundles(bundles);
  const packs = Object.fromEntries(packsFor(all, locale).map((b) => [b.id, optional(poolFile(locale, b.id))]));
  const { pool, bundles: parsed } = withPacks(parsePool(json(file)), all, locale, packs);
  const byBundle = {};
  for (const b of parsed) {
    const cats = optional(bundleFile(b.id, "categories.json"));
    if (cats) byBundle[b.id] = cats;
  }
  return engineData(
    pool, loadCategories(bundles, byBundle), parsed, parseAgeGroups(json("age-groups.json")), locale,
    locale === "es" ? undefined : mergeNames(parsed.map((b) => optional(bundleFile(b.id, `names.${locale}.json`)))),
  );
}

// Save documents -----------------------------------------------------------------------------

let seed = 1;
const io = () => ({ rng: seededRng(seed++), now: "2026-10-13T20:00:00" });

function baseSave(ui, questions) {
  const save = { ...emptySave(), language: { ui, questions } };
  save.players = PLAYERS.map((name, i) => ({ id: i + 1, name, created_on: `2026-10-0${9 - i}T18:00:00` })); // newest first: PLAYERS[0] tops the list
  return save;
}

const latestState = (save) => save.games.at(-1).state;

/** A solo game of PLAYERS[0] at `level`: the levels below won; `qid` on screen, else the table. */
function gameAt(data, ui, level, qid) {
  let { save } = newGame(baseSave(ui, data.locale), data, io(), PLAYERS[0], { mode: "solo" });
  for (let l = 1; l < level; l++) {
    ({ save } = pick(save, data, io(), 0));
    const s = latestState(save);
    const right = data.byId.get(s.current).answer;
    ({ save } = answer(save, data, io(), s.answers.indexOf(right)));
  }
  if (qid) {
    latestState(save).options[0] = qid;
    ({ save } = pick(save, data, io(), 0));
  }
  if (save.version !== SAVE_VERSION) throw new Error("save version");
  return save;
}

// Page helpers -------------------------------------------------------------------------------

let page, evaluate, waitFor, click;

/** Images decoded, media able to play. */
const mediaReady = `[...document.images].every((i) => i.complete) && [...document.querySelectorAll("video, audio")].every((m) => m.readyState >= 2)`;

async function load(saveDir, save) {
  await sleep(800); // the last shot's save write lands first
  await writeFile(path.join(saveDir, "game.json"), JSON.stringify(save));
  await page.send("Page.reload", { ignoreCache: true });
  await sleep(500);
  await waitFor(visibleEl("main button.candy, button.candy"), "start screen");
}

const shots = [];
async function shoot(lang, name) {
  await waitFor(mediaReady, `${name}: media`, 20000).catch(() => console.error(`  ${name}: media not ready, shot anyway`));
  const { data } = await page.send("Page.captureScreenshot", { format: "png", clip: { x: 0, y: 0, width: W, height: H, scale: 1 } });
  const n = String(shots.filter((s) => s.lang === lang).length + 1).padStart(2, "0");
  const file = path.join(OUT, lang, `${n}-${name}.png`);
  await writeFile(file, Buffer.from(data, "base64"));
  shots.push({ lang, file });
  console.log(`  ${path.relative(REPO, file)}`);
}

// The walk -----------------------------------------------------------------------------------

/** Start, player, mode choice, customize (each language). */
async function menus(lang, saveDir, data, ui) {
  await load(saveDir, baseSave(ui, data.locale));
  await sleep(1500);
  await shoot(lang, "start");
  await click("button.candy");
  await waitFor(visibleEl(".name-button"), "player screen");
  await sleep(3000);
  await shoot(lang, "player");
  await click(".name-button");
  await click('[data-focus-id="mode-solo"]');
  await waitFor(visibleEl('[data-focus-id="group-young_teens"]'), "age groups");
  await click('[data-focus-id="group-young_teens"]');
  await sleep(3000);
  await shoot(lang, "modes");
  await click('[data-focus-id="customize"]');
  await sleep(1500);
  await shoot(lang, "customize");
}

/** Resume a seeded game from Start. */
async function resume(saveDir, save) {
  await load(saveDir, save);
  await click("button.candy");
}

async function tower(lang, saveDir, data, ui, cards) {
  await resume(saveDir, gameAt(data, ui, 11));
  await waitFor(visibleEl(".level .hint"), "level screen");
  await sleep(2500);
  await shoot(lang, "tower");
  if (!cards) return;
  await click(".level .hint");
  await waitFor(visibleEl(".cards .card"), "cards");
  await sleep(2000);
  await shoot(lang, "cards");
}

async function onQuestion(saveDir, save) {
  await resume(saveDir, save);
  await waitFor(visibleEl(".answers .answer"), "question screen");
}

/** Question screens need the UI language's own questions. */
async function questions(lang, saveDir, data, ui) {
  await onQuestion(saveDir, gameAt(data, ui, 4, Q.image));
  await sleep(2500);
  await shoot(lang, "image-question");

  await onQuestion(saveDir, gameAt(data, ui, 7, Q.video));
  await waitFor(`(() => { const v = document.querySelector("video"); return !!v && v.currentTime > 3; })()`, "video playing", 20000)
    .catch(() => console.error("  video didn't play, shot anyway"));
  await shoot(lang, "video-question");

  // Francotirador aiming at a wrong answer.
  const jokerSave = gameAt(data, ui, 6, Q.joker);
  await onQuestion(saveDir, jokerSave);
  await sleep(1500);
  const s = latestState(jokerSave);
  // Not tile 0: the crosshair starts there, a click on it would shoot.
  const wrong = s.answers.findIndex((a, i) => i > 0 && a !== data.byId.get(Q.joker).answer);
  await click('.token[data-joker="snipe"]');
  await sleep(300);
  await click(`.answers .answer:nth-child(${wrong + 1})`);
  await sleep(1200);
  await shoot(lang, "joker");

  const finalSave = gameAt(data, ui, 12, Q.final);
  await onQuestion(saveDir, finalSave);
  await sleep(1000);
  const f = latestState(finalSave);
  await click(`.answers .answer:nth-child(${f.answers.indexOf(data.byId.get(Q.final).answer) + 1})`);
  await click(".final-button.ready");
  await waitFor(visibleEl(".result.victory"), "victory", 30000);
  await sleep(3500);
  await shoot(lang, "victory");
}

// Main ---------------------------------------------------------------------------------------

async function main() {
  if (!existsSync(path.join(REPO, "app", "client", "dist", "index.html"))) throw new Error("client not built: npm run build");
  const es = loadData("es");
  for (const id of Object.values(Q)) {
    const url = es.byId.get(id)?.media?.file_url;
    if (!url) throw new Error(`${id}: not in the pool or no media; pick another in Q`);
    if (!existsSync(path.join(MEDIA, cacheName(url)))) throw new Error(`${id}: media not cached: trivia-media sync --status approved`);
  }

  const tmp = await mkdtemp(path.join(os.tmpdir(), "trivia-shots-"));
  const procs = [];
  let display = process.env.DISPLAY;
  try {
    if (!visible) {
      const x = await startXvfb("Xvfb", W, H).catch((e) => {
        throw e.code === "ENOENT" ? new Error("Xvfb not found: run from the dev shell, or pass --visible") : e;
      });
      display = x.display;
      procs.push(x.proc);
    }
    const port = await freePort();
    const shell = spawn("trivia-desktop", [`--remote-debugging-port=${port}`, "--remote-allow-origins=*"], {
      env: { ...process.env, DISPLAY: display, TRIVIA_SAVE_DIR: tmp, TRIVIA_STEAM_SDK: path.join(tmp, "no-steam") },
      stdio: ["ignore", "ignore", "pipe"],
    });
    shell.stderr.on("data", (d) => process.env.DEBUG && process.stderr.write(d));
    procs.push(shell);
    page = await connectPort(port);
    ({ evaluate, waitFor, click } = pageHelpers(page));
    await page.send("Page.enable");
    await page.send("Emulation.setDeviceMetricsOverride", { width: W, height: H, deviceScaleFactor: 1, mobile: false });

    const followUp = [];
    for (const ui of LANGS) {
      console.log(ui);
      await rm(path.join(OUT, ui), { recursive: true, force: true });
      await mkdir(path.join(OUT, ui), { recursive: true });
      const own = loadData(ui.split("-")[0]);
      const data = own ?? es; // UI-only shots on the es pool show no question text
      await menus(ui, tmp, data, ui);
      await tower(ui, tmp, data, ui, !!own);
      if (own) await questions(ui, tmp, data, ui);
      else followUp.push(ui);
    }
    console.log(`${shots.length} screenshots in ${path.relative(REPO, OUT)}/`);
    if (followUp.length) console.log(`no question pool for ${followUp.join(", ")}: menus and tower only; re-run once it lands`);
  } finally {
    page?.close();
    for (const p of procs.reverse()) p.kill();
    await sleep(500);
    await rm(tmp, { recursive: true, force: true });
  }
}

main().catch((e) => {
  console.error(`screenshots: ${e.message}`);
  process.exitCode = 1;
});
