#!/usr/bin/env node
// Pre-session menus check (task 2114; plans/14-input.md "Before the session"): the built client on the Node dev server
// (`npm run serve -w app/client`, a temp save dir, never state/) in headless Chromium over raw CDP, trusted key presses
// and fake pads (fake_pads.js). Usage (dev shell, after `npm run build -w app/client`): node authoring/tools/menu_check.mjs
// [--visible] [--chromium <exe>]; exit 1 names the failed step. Steps:
//   enter     fresh save: only Enter from Start to the first question → a standard-mode game, a suggested team name, default settings
//   pad-a     the same with only pad A (a fresh save)
//   last      that player plays a gamemaster game; next time only Enter → gamemaster mode (the save's last) preselected and played
//   space     Space on the ring's Mode tile only picks it; Enter with the ring on a tile goes on; Space on a bundle tile
//             toggles it once (no native double click); Enter with the ring on a bundle starts the game
//   letter    a bundle's letter toggles it and moves the ring onto it; a mode's letter likewise
//   pad-x     X on the ring's bundle toggles it, A with the ring on a bundle starts
import { spawn } from "node:child_process";
import { readFileSync } from "node:fs";
import { mkdtemp, readFile, rm } from "node:fs/promises";
import { createServer } from "node:net";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { connectPipe, pageHelpers, sleep, visibleEl } from "./cdp.mjs";

const REPO = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..", "..");
const ARGS = process.argv.slice(2);
const VISIBLE = ARGS.includes("--visible");
const CHROMIUM = ARGS.includes("--chromium") ? ARGS[ARGS.indexOf("--chromium") + 1] : process.env.CHROMIUM ?? "chromium";
const FAKE_PADS = readFileSync(path.join(REPO, "authoring", "tools", "fake_pads.js"), "utf8").replace(/^\/\/.*\n/gm, "");
const BTN = { A: 0, X: 2, UP: 12, DOWN: 13, LEFT: 14 };
const ES = "Español (Latinoamérica)";
const TEAM_NAMES = new Set(
  (await import(path.join(REPO, "app", "client", "src", "locales", "es.ts"))).default?.screen?.player?.teamNames ?? [],
);

let step = "prepare";
const at = (s) => (step = s);
let page;
let h;
let saveDir;

const freePort = () =>
  new Promise((resolve) => {
    const srv = createServer().listen(0, "127.0.0.1", () => {
      const { port } = srv.address();
      srv.close(() => resolve(port));
    });
  });

/** `vite preview` with the dev server's plugin on `saveDir`; killed by its process group (npm → sh → vite). */
async function startServer(port) {
  const proc = spawn("npm", ["run", "serve", "-w", "app/client", "--", "--port", String(port)], {
    cwd: REPO, env: { ...process.env, TRIVIA_SAVE_DIR: saveDir, TRIVIA_MUTE: "1" }, stdio: ["ignore", "pipe", "pipe"], detached: true,
  });
  let log = "";
  proc.stdout.on("data", (d) => (log += d));
  proc.stderr.on("data", (d) => (log += d));
  for (let i = 0; i < 150; i++) {
    if (proc.exitCode !== null) break;
    try {
      await fetch(`http://localhost:${port}/`);
      return proc;
    } catch {}
    await sleep(200);
  }
  throw new Error(`dev server didn't start:\n${log}`);
}

/** Headless Chromium (Spanish UI, so the letters below are es) on the debugging pipe; the page is the game. */
async function launchBrowser(url) {
  const profile = await mkdtemp(path.join(os.tmpdir(), "trivia-menu-check-profile-"));
  const args = [
    ...(VISIBLE ? [] : ["--headless=new"]), "--remote-debugging-pipe", `--user-data-dir=${profile}`, "--no-first-run", "--no-default-browser-check",
    "--disable-gpu", "--window-size=1920,1080", "--lang=es", "--accept-lang=es", "--autoplay-policy=no-user-gesture-required", "--mute-audio", url,
  ];
  const env = { ...process.env };
  delete env.LD_LIBRARY_PATH; // the dev shell's (alsa for Electron) breaks the system Chromium
  const child = spawn(CHROMIUM, args, { env, stdio: ["ignore", "ignore", process.env.DEBUG ? "inherit" : "ignore", "pipe", "pipe"] });
  const page = await connectPipe(child, (t) => t.url.startsWith("http"));
  return { child, page, profile };
}

const saveFile = () => path.join(saveDir, "game.json");
const readSave = async () => JSON.parse(await readFile(saveFile(), "utf8"));
/** The save once `test` holds on it. */
async function saved(test, what, ms = 10000) {
  for (const end = Date.now() + ms; Date.now() < end; await sleep(100)) {
    const s = await readSave().catch(() => null);
    if (s && test(s)) return s;
  }
  throw new Error(`timeout: ${what}`);
}

/** A trusted key press (CDP Input domain), like smoke.mjs's. */
async function key(k) {
  const named = { Enter: ["Enter", 13, "\r"], " ": ["Space", 32, " "], ArrowLeft: ["ArrowLeft", 37], ArrowRight: ["ArrowRight", 39], ArrowDown: ["ArrowDown", 40], ArrowUp: ["ArrowUp", 38] }[k];
  const [code, vk, text] = named ?? [/\d/.test(k) ? `Digit${k}` : `Key${k.toUpperCase()}`, k.toUpperCase().charCodeAt(0), k];
  await page.send("Input.dispatchKeyEvent", { type: text ? "keyDown" : "rawKeyDown", key: k, code, windowsVirtualKeyCode: vk, ...(text ? { text } : {}) });
  await page.send("Input.dispatchKeyEvent", { type: "keyUp", key: k, code, windowsVirtualKeyCode: vk });
  await sleep(250);
}
const padPress = async (button, i = 0) => {
  await h.evaluate(`window.__press(${button}, ${i})`);
  await sleep(150);
};

const ringId = () => h.evaluate(`document.querySelector("[data-nav]")?.dataset.focusId ?? null`);
const onScreen = (sel) => h.evaluate(visibleEl(sel));
const pressed = (sel) => h.evaluate(`document.querySelector(${JSON.stringify(sel)})?.getAttribute("aria-checked")`);

/** The page from scratch (a reload keeps the save), on Start. */
async function toStart() {
  await h.evaluate("location.reload()").catch(() => {});
  await sleep(1500);
  await h.evaluate(`${FAKE_PADS}; true`).catch(() => {}); // the init script installs it; a reload too, this is the belt
  const start = visibleEl('[data-focus-id="main"]');
  await h.waitFor(`${visibleEl(".language .option")} || ${visibleEl(".consent .option")} || ${start}`, "first screen", 30000);
  if (await onScreen(".language .option")) {
    // the first start asks the language (a list screen: Enter picks the ring's, the guess); the letters below are es: pick it
    const es = await h.evaluate(`[...document.querySelectorAll(".language .option")].findIndex((b) => b.textContent.trim() === ${JSON.stringify(ES)})`);
    if (es < 0) throw new Error("no Spanish option on the Language screen");
    await key(String(es + 1));
    await h.waitFor(`${visibleEl(".consent .option")} || ${start}`, "after language", 30000);
    await h.evaluate(`${FAKE_PADS}; true`).catch(() => {});
  }
  if (await onScreen(".consent .option")) await h.click(".consent .option[data-focus-default]");
  await h.waitFor(start, "start screen");
  await sleep(600); // the arrive animation; input is live, the ring is not
}

async function waitScreen(sel, what) {
  await h.waitFor(visibleEl(sel), what, 15000);
  await sleep(700); // transitions ignore input while they run
}

/** Start → Mode → Player → Choice → Bundles → the first question, one `go` per screen. */
async function onlyConfirm(go, label) {
  at(`${label}: start`);
  await go();
  await waitScreen(".mode-screen", "mode screen");
  at(`${label}: mode`);
  for (let i = 0; i < 2 && (await onScreen(".mode-screen")); i++) {
    await go();
    await sleep(900);
  }
  await waitScreen("#new-player", "player screen");
  at(`${label}: player`);
  const name = await h.evaluate(`document.querySelector("#new-player").value`);
  await go();
  await waitScreen(".choice", "choice screen");
  at(`${label}: choice`);
  await go();
  await waitScreen('[data-focus-id="start"]', "bundles screen");
  at(`${label}: bundles`);
  await h.waitFor(`!document.querySelector('[data-focus-id="start"]').disabled`, "start enabled");
  await go();
  const save = await saved((s) => s.games?.length > 0, "a game started");
  await h.waitFor(`${visibleEl(".level .hint")} || ${visibleEl(".cards .card")}`, "level screen", 30000);
  return { name, game: save.games.at(-1), save };
}

const modeOf = (g) => g.state.settings.mode ?? "gamemaster";

async function checkEnterOnly(label, go) {
  const { name, game, save } = await onlyConfirm(go, label);
  const player = save.players.find((p) => p.id === game.player_id)?.name;
  if (!TEAM_NAMES.has(name) || player !== name) throw new Error(`team name: field "${name}", player "${player}" (want a suggested team name)`);
  if (modeOf(game) !== "solo") throw new Error(`mode ${modeOf(game)}, want solo`);
  const s = game.state.settings;
  if (s.age_group !== "young_teens" || s.customized || s.video === false || s.audio === false) throw new Error(`settings ${JSON.stringify(s)}, want the defaults`);
  if (JSON.stringify(s.bundles) !== '["base"]') throw new Error(`bundles ${JSON.stringify(s.bundles)}, want the first base bundle only`);
  return name;
}

/** A gamemaster game for `name` through the menus, then the next walk with only Enter preselects it (the save's last mode). */
async function checkLastChoice(name) {
  at("last: gamemaster game");
  await toStart();
  await key("n"); // es: «Nueva partida»'s key (a game is running: Enter would be «Continuar», the Start list's default)
  await waitScreen(".mode-screen", "mode screen");
  if (await onScreen('[data-focus-id="kind-single"]')) {
    await key("Enter");
    await sleep(900);
  }
  await key("a"); // es: «Modo anfitrión»'s letter picks it and takes the ring
  if ((await ringId()) !== "mode-gamemaster") throw new Error(`ring on ${await ringId()} after the letter, want mode-gamemaster`);
  if ((await pressed('[data-focus-id="mode-gamemaster"]')) !== "true") throw new Error("the letter didn't pick gamemaster mode");
  await key("Enter"); // «Seguir», whatever has the ring
  await waitScreen("#new-player", "player screen");
  await key("Enter"); // the most recent name
  await waitScreen(".choice", "choice screen");
  await key("Enter");
  await waitScreen('[data-focus-id="start"]', "bundles screen");
  await h.waitFor(`!document.querySelector('[data-focus-id="start"]').disabled`, "start enabled");
  await key("Enter");
  const save = await saved((s) => s.games?.length === 2, "the second game");
  if (modeOf(save.games.at(-1)) !== "gamemaster") throw new Error(`second game's mode ${modeOf(save.games.at(-1))}, want gamemaster`);
  await h.waitFor(`${visibleEl(".level .hint")} || ${visibleEl(".cards .card")}`, "level screen", 30000);
  at("last: next time, only Enter");
  await toStart();
  await key("n");
  await waitScreen(".mode-screen", "mode screen");
  if (await onScreen('[data-focus-id="kind-single"]')) {
    if ((await pressed('[data-focus-id="kind-single"]')) !== "true") throw new Error("the kind step doesn't preselect «Solo o en grupo»");
    await key("Enter");
    await sleep(900);
  }
  await h.waitFor(`document.querySelector('[data-focus-id="mode-gamemaster"]')?.getAttribute("aria-checked") === "true"`, "gamemaster preselected", 5000);
  await key("Enter");
  await waitScreen("#new-player", "player screen");
  await key("Enter");
  await waitScreen(".choice", "choice screen");
  if (!(await onScreen('[data-focus-id="config-levels"]'))) throw new Error("not the configure screen: gamemaster mode wasn't carried");
  await key("Enter");
  await waitScreen('[data-focus-id="start"]', "bundles screen");
  await h.waitFor(`!document.querySelector('[data-focus-id="start"]').disabled`, "start enabled");
  await key("Enter");
  const again = await saved((s) => s.games?.length === 3, "the third game");
  if (modeOf(again.games.at(-1)) !== "gamemaster") throw new Error(`third game's mode ${modeOf(again.games.at(-1))}, want gamemaster`);
  if (again.games.at(-1).player_id !== again.players.find((p) => p.name === name)?.id) throw new Error("the third game isn't the same player's");
}

/** Space picks / toggles the ring's tile only; Enter goes on from any tile; a letter moves the ring. */
async function checkSpaceAndLetters() {
  at("space: to the mode screen");
  await toStart();
  await key("n");
  await waitScreen(".mode-screen", "mode screen");
  if (await onScreen('[data-focus-id="kind-single"]')) {
    await key("Enter");
    await sleep(900);
  }
  // the ring onto the standard tile: the first arrow shows the ring on the default («Seguir»), then up, then left to the first tile
  await key("ArrowUp");
  await key("ArrowUp");
  await key("ArrowLeft");
  await key("ArrowLeft");
  if ((await ringId()) !== "mode-solo") throw new Error(`ring on ${await ringId()}, want mode-solo`);
  at("space: Space picks the tile, nothing more");
  await key(" ");
  await sleep(500);
  if (!(await onScreen(".mode-screen"))) throw new Error("Space on a mode tile left the screen");
  if ((await pressed('[data-focus-id="mode-solo"]')) !== "true") throw new Error("Space didn't pick the ring's tile");
  if ((await pressed('[data-focus-id="mode-gamemaster"]')) === "true") throw new Error("Space didn't un-pick the other tile");
  at("letter: a mode's letter picks it and moves the ring");
  await key("a");
  if ((await ringId()) !== "mode-gamemaster" || (await pressed('[data-focus-id="mode-gamemaster"]')) !== "true") throw new Error(`after the letter: ring ${await ringId()}, picked ${await pressed('[data-focus-id="mode-gamemaster"]')}`);
  await key("g");
  if ((await ringId()) !== "mode-solo" || (await pressed('[data-focus-id="mode-solo"]')) !== "true") throw new Error("the standard mode's letter didn't pick it with the ring");
  at("space: Enter with the ring on a tile goes on");
  await key("Enter");
  await waitScreen("#new-player", "player screen");
  await key("Enter");
  await waitScreen(".choice", "choice screen");
  await key("Enter");
  await waitScreen('[data-focus-id="start"]', "bundles screen");
  at("space: a bundle's letter toggles it and takes the ring");
  const tiles = await h.evaluate(`JSON.stringify([...document.querySelectorAll(".bundles [data-focus-id^='bundle-']")].map((b) => [b.dataset.focusId, b.getAttribute("aria-checked"), b.querySelector("kbd")?.textContent ?? ""]))`);
  const [first] = JSON.parse(tiles);
  if (!first) throw new Error("no bundle tile");
  const [id, on, letter] = first;
  if (!letter) throw new Error(`bundle ${id} has no letter`);
  await key(letter.toLowerCase());
  if ((await ringId()) !== id) throw new Error(`ring on ${await ringId()} after the bundle letter, want ${id}`);
  if ((await pressed(`[data-focus-id="${id}"]`)) === on) throw new Error("the bundle letter didn't toggle the bundle");
  at("space: Space toggles the ring's bundle exactly once");
  await key(" ");
  await sleep(600);
  if ((await pressed(`[data-focus-id="${id}"]`)) !== on) throw new Error("Space didn't toggle the ring's bundle back (or toggled twice)");
  if (!(await onScreen('[data-focus-id="start"]'))) throw new Error("Space on a bundle left the Bundles screen");
  at("space: Enter with the ring on a bundle starts the game");
  await h.waitFor(`!document.querySelector('[data-focus-id="start"]').disabled`, "start enabled");
  const n = (await readSave()).games.length;
  await key("Enter");
  await saved((s) => s.games.length === n + 1, "the game started from a ringed bundle");
  await h.waitFor(`${visibleEl(".level .hint")} || ${visibleEl(".cards .card")}`, "level screen", 30000);
}

/** The pad: X toggles the ring's bundle, A with the ring on a bundle starts. */
async function checkPadX() {
  at("pad-x: to the bundles screen");
  await toStart();
  await h.evaluate("window.__pads(1); true");
  await key("n");
  await waitScreen(".mode-screen", "mode screen");
  for (let i = 0; i < 2 && (await onScreen(".mode-screen")); i++) {
    await padPress(BTN.A);
    await sleep(900);
  }
  await waitScreen("#new-player", "player screen");
  await padPress(BTN.A);
  await waitScreen(".choice", "choice screen");
  await padPress(BTN.A);
  await waitScreen('[data-focus-id="start"]', "bundles screen");
  const id = await h.evaluate(`document.querySelector(".bundles [data-focus-id^='bundle-']")?.dataset.focusId`);
  const on = await pressed(`[data-focus-id="${id}"]`);
  await sleep(1000); // the arrive animations move the controls: spatial focus reads their rects
  const path = [];
  await padPress(BTN.DOWN); // the ring shows on the default («¡A jugar!»)
  path.push(await ringId());
  // up to the tiles' top row (the optional ones flow in rows), then left over the ruler to the base column
  for (const button of [BTN.UP, BTN.UP, BTN.UP, BTN.LEFT, BTN.LEFT, BTN.LEFT, BTN.LEFT, BTN.LEFT, BTN.LEFT]) {
    if ((await ringId()) === id) break;
    await padPress(button);
    path.push(await ringId());
  }
  if ((await ringId()) !== id) throw new Error(`ring on ${await ringId()} (${path.join(" → ")}), want ${id}`);
  at("pad-x: X toggles the ring's bundle");
  await padPress(BTN.X);
  await sleep(500);
  if ((await pressed(`[data-focus-id="${id}"]`)) === on) throw new Error("X didn't toggle the ring's bundle");
  await padPress(BTN.X);
  await sleep(500);
  if ((await pressed(`[data-focus-id="${id}"]`)) !== on) throw new Error("X didn't toggle it back");
  if (!(await onScreen('[data-focus-id="start"]'))) throw new Error("X on a bundle left the Bundles screen");
  at("pad-x: A with the ring on a bundle starts");
  await h.waitFor(`!document.querySelector('[data-focus-id="start"]').disabled`, "start enabled");
  const n = (await readSave()).games.length;
  await padPress(BTN.A);
  await saved((s) => s.games.length === n + 1, "the game started by A from a ringed bundle");
}

async function main() {
  saveDir = await mkdtemp(path.join(os.tmpdir(), "trivia-menu-check-"));
  const port = await freePort();
  const url = `http://localhost:${port}/`;
  let server;
  let browser;
  try {
    at("dev server");
    server = await startServer(port);
    at("browser");
    browser = await launchBrowser(url);
    page = browser.page;
    h = pageHelpers(page);
    await page.send("Page.enable");
    await page.send("Page.addScriptToEvaluateOnNewDocument", { source: `(${FAKE_PADS})(null)` });
    await page.send("Emulation.setFocusEmulationEnabled", { enabled: true });

    await toStart();
    const name = await checkEnterOnly("enter", () => key("Enter"));
    console.log(`enter: ok (team «${name}», standard mode, defaults)`);

    at("pad-a: fresh save");
    await rm(saveFile(), { force: true });
    await toStart();
    await h.evaluate("window.__pads(1); true");
    const padName = await checkEnterOnly("pad-a", () => padPress(BTN.A));
    console.log(`pad-a: ok (team «${padName}»)`);

    await checkLastChoice(padName);
    console.log("last: ok (gamemaster mode preselected and played)");

    await checkSpaceAndLetters();
    console.log("space, letter: ok");

    await checkPadX();
    console.log("pad-x: ok");
    console.log("menu check: ok");
  } catch (e) {
    console.error(`menu check ✗ at step «${step}»: ${e.message}`);
    process.exitCode = 1;
  } finally {
    if (browser?.child && browser.child.exitCode === null) browser.child.kill();
    if (server && server.exitCode === null) process.kill(-server.pid, "SIGTERM");
    await sleep(500);
    if (browser?.profile) await rm(browser.profile, { recursive: true, force: true });
    await rm(saveDir, { recursive: true, force: true });
  }
}

await main();
