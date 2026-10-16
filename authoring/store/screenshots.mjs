#!/usr/bin/env node
// Store screenshots (plan 88, PUB-8, decision 79): 7 per language at 1920×1080 (5 without its question pool),
// the shell under Xvfb, raw CDP, a demo save per shot.
// Usage (dev shell): node authoring/store/screenshots.mjs [--lang en,es,es-ES,de] [--visible]
// Needs app/client/dist (`npm run build`) and the media cache (`trivia-media sync --status approved`).
import { existsSync } from "node:fs";
import { mkdir, rm, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { cacheName } from "../../app/desktop/resolve.mjs";
import { launchShell, pageHelpers, sleep, visibleEl } from "../tools/cdp.mjs";
import { baseSave, gameAt, latestState } from "../tools/demo_saves.mjs";
import { loadData } from "../tools/engine_data.mjs";

const REPO = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..", "..");
const OUT = path.join(REPO, "authoring", "store", "out", "screenshots");
const MEDIA = process.env.TRIVIA_MEDIA || path.join(REPO, "media"); // as the shell's roots()
const W = 1920;
const H = 1080;

// Gameplay shots' questions (es pool): approved, short, an image each.
const Q = { locked: "q-0030", joker: "q-0019" };

const args = process.argv.slice(2);
const opt = (name) => {
  const i = args.indexOf(name);
  return i >= 0 ? args[i + 1] : undefined;
};
const LANGS = (opt("--lang") ?? "en,es,es-ES,de").split(",");
const visible = args.includes("--visible");

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

/** Resume a seeded game from Start. */
async function resume(saveDir, save) {
  await load(saveDir, save);
  await click("button.candy");
}

async function onQuestion(saveDir, save) {
  await resume(saveDir, save);
  await waitFor(visibleEl(".answers .answer"), "question screen");
}

const answerEl = (i) => `.answers .answer:nth-child(${i + 1})`;

/** Gameplay (decision 79): a locked-in answer, Francotirador aiming. Needs the UI language's own questions. */
async function gameplay(lang, saveDir, data, ui) {
  const lockSave = gameAt(data, ui, 5, Q.locked);
  await onQuestion(saveDir, lockSave);
  await sleep(2500);
  await click(answerEl(latestState(lockSave).answers.indexOf(data.byId.get(Q.locked).answer)));
  await waitFor(visibleEl(".final-button.ready"), "locked answer", 10000);
  await sleep(800);
  await shoot(lang, "question-locked");

  const jokerSave = gameAt(data, ui, 6, Q.joker);
  await onQuestion(saveDir, jokerSave);
  await sleep(1500);
  // Not tile 0: the crosshair starts there, a click on it would shoot.
  const wrong = latestState(jokerSave).answers.findIndex((a, i) => i > 0 && a !== data.byId.get(Q.joker).answer);
  await click('.token[data-joker="snipe"]');
  await sleep(300);
  await click(answerEl(wrong));
  await sleep(1200);
  await shoot(lang, "joker-snipe");
}

/** Start → player → the Choice screen in `mode`. */
async function toChoice(saveDir, data, ui, mode) {
  await load(saveDir, baseSave(ui, data.locale));
  await click("button.candy");
  await waitFor(visibleEl(".name-button"), "player screen");
  await sleep(800);
  await click(".name-button");
  await waitFor(visibleEl(`[data-focus-id="mode-${mode}"]`), "choice screen");
  await click(`[data-focus-id="mode-${mode}"]`);
}

const focus = (sel) => evaluate(`document.querySelector(${JSON.stringify(sel)}).focus()`);

/** The 5 informative shots (decision 79): modes, Customize game, configure screen, joker presets, bundles (the last screen before the game). */
async function menus(lang, saveDir, data, ui) {
  await toChoice(saveDir, data, ui, "solo");
  await click('[data-focus-id="group-young_teens"]');
  await sleep(3000);
  await shoot(lang, "modes");

  await click('[data-focus-id="customize"]');
  await waitFor(visibleEl(".dialog"), "customize");
  await sleep(1200);
  await shoot(lang, "customize");

  await toChoice(saveDir, data, ui, "gamemaster");
  await waitFor(visibleEl('[data-focus-id="config-preset"]'), "configure screen");
  await sleep(2500);
  await shoot(lang, "configure");

  await click('[data-focus-id="config-preset"] button.step:last-of-type'); // Estándar → Sin límite
  await focus('[data-focus-id="config-preset"]');
  await sleep(1000);
  await shoot(lang, "joker-presets");

  await click('[data-focus-id="next"]');
  await waitFor(visibleEl('[data-focus-id="start"]'), "bundles screen");
  const pack = '[data-focus-id="bundle-colombia"]';
  if (await evaluate(`!!document.querySelector(${JSON.stringify(pack)})`)) {
    await click(pack);
    await focus(pack);
  }
  await sleep(1200);
  await shoot(lang, "bundles");
}
