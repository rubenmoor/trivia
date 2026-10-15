#!/usr/bin/env node
// Store capsules, library art and the game icon (plan 88, decisions 77, 87): a typographic template, raw CDP against the shell.
// Usage (dev shell): node authoring/store/capsules.mjs [--only <path part>] [--visible]
// Needs app/client/dist (`npm run build`): the shell serves the game's fonts. Output: out/capsules/ (17a "Capsules and icon").
import { spawn } from "node:child_process";
import { existsSync, readFileSync } from "node:fs";
import { mkdir, mkdtemp, rm, writeFile } from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { connectPort, freePort, pageHelpers, sleep, startXvfb } from "../tools/cdp.mjs";

const REPO = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..", "..");
const OUT = path.join(REPO, "authoring", "store", "out", "capsules");

const args = process.argv.slice(2);
const only = args.includes("--only") ? args[args.indexOf("--only") + 1] : undefined;
const visible = args.includes("--visible");

// Store names (D-50, decision 78); `es` and `es-ES` share. Logotype: small line + big word.
const NAMES = {
  en: { above: "Living Room", main: "Trivia" },
  es: { main: "Trivia", below: "en Familia" },
  de: { above: "Wohnzimmer-", main: "Quiz" },
};

// Valve's asset list (17a "Capsules and icon"). text: logotype on it, per language; art: no words, once.
const STORE = [
  { name: "header", w: 920, h: 430, kind: "text" },
  { name: "small", w: 462, h: 174, kind: "text" },
  { name: "main", w: 1232, h: 706, kind: "text" },
  { name: "vertical", w: 748, h: 896, kind: "text" },
];
const LIBRARY = [
  { name: "library-capsule", w: 600, h: 900, kind: "text" },
  { name: "library-header", w: 920, h: 430, kind: "text" },
  { name: "library-logo", kind: "logo" },
];
const ART = [
  { name: "page-background", w: 1438, h: 810, kind: "art", dim: true },
  // Tower's top in the centred 860×380 safe area, right of centre: the logo goes bottom left.
  { name: "library-hero", w: 3840, h: 1240, kind: "art", towerX: 2250, towerTop: 440 },
];

/** Free DLC (decision 66): non-base bundles; name from `names.<lang>.json`, else `bundles.json`. */
function dlcs() {
  const { bundles } = JSON.parse(readFileSync(path.join(REPO, "app", "data", "bundles.json"), "utf8"));
  // Decision 110: colombia ships es + en.
  const langs = { colombia: ["es", "en"] };
  return bundles
    .filter((b) => b.kind !== "base")
    .map((b) => ({
      id: b.id,
      names: Object.fromEntries((langs[b.id] ?? b.languages).map((l) => {
        const file = path.join(REPO, "app", "data", `names.${l}.json`);
        const own = existsSync(file) ? JSON.parse(readFileSync(file, "utf8")).bundles?.[b.id]?.name : undefined;
        return [l, own ?? b.name];
      })),
    }));
}

// The template --------------------------------------------------------------------------------

// app/client/src/game/theme.css tokens (the page is replaced, so no var()).
const C = {
  night900: "#0b1120", night800: "#111a2e", night700: "#1a2540", slate600: "#2b3650",
  paper: "#eef1f6", amber: "#ffb81c", amberDeep: "#b97a00", sky: "#4cc9f0", mint: "#2fe39a", coral: "#ff5470",
  stone: "#5d6b86", brick: "#c8643b", marble: "#d9dce6", sapphire: "#3a6df0",
};
// The tower's materials by level (10-visual-design "Tower").
const BLOCKS = [C.stone, C.stone, C.stone, C.brick, C.brick, C.brick, C.marble, C.marble, C.marble, C.sapphire, C.sapphire, C.amber];

const CSS = `
@font-face { font-family: "Baloo 2"; src: url("/fonts/baloo-2.woff2") format("woff2"); font-weight: 400 800; }
* { box-sizing: border-box; margin: 0; }
html, body { width: 100%; height: 100%; background: transparent; overflow: hidden; }
.stage { position: relative; overflow: hidden; background: radial-gradient(ellipse at 50% 30%, ${C.night800}, ${C.night900} 75%); }
.spot { position: absolute; inset: 0; background: conic-gradient(from 160deg at var(--sx) -10%, transparent 0deg, rgba(255,184,28,0.16) 14deg, rgba(255,184,28,0.16) 26deg, transparent 40deg); filter: blur(calc(var(--u) * 2)); }
.glow { position: absolute; left: calc(var(--sx) - var(--u) * 30); bottom: 0; width: calc(var(--u) * 60); height: calc(var(--u) * 14); border-radius: 50%; background: radial-gradient(rgba(255,184,28,0.18), transparent 70%); }
.q { position: absolute; font-family: "Baloo 2"; font-weight: 800; color: ${C.paper}; opacity: 0.06; line-height: 1; }
.tower { position: absolute; display: flex; flex-direction: column-reverse; align-items: center; gap: calc(var(--b) * 0.12); }
.block { width: calc(var(--b) * 4.2); height: calc(var(--b) * 0.82); border-radius: calc(var(--b) * 0.18);
  background: linear-gradient(180deg, rgba(255,255,255,0.28), rgba(255,255,255,0) 45%, rgba(0,0,0,0.22)), var(--c);
  box-shadow: 0 calc(var(--b) * 0.08) 0 rgba(0,0,0,0.35); }
.block.top { background: linear-gradient(180deg, #ffe08a, ${C.amber} 50%, ${C.amberDeep}); box-shadow: 0 0 calc(var(--b) * 1.2) rgba(255,184,28,0.55), 0 calc(var(--b) * 0.08) 0 rgba(0,0,0,0.35); }
.base { width: calc(var(--b) * 5.4); height: calc(var(--b) * 0.5); border-radius: calc(var(--b) * 0.12); background: ${C.night700}; border-top: calc(var(--b) * 0.1) solid ${C.amber}; }
.crown { width: calc(var(--b) * 2.2); margin-bottom: calc(var(--b) * 0.1); filter: drop-shadow(0 0 calc(var(--b) * 0.5) rgba(255,184,28,0.6)); }
.logo { position: absolute; display: flex; flex-direction: column; align-items: center; font-family: "Baloo 2"; line-height: 0.82; white-space: nowrap; }
.logo .main { font-weight: 800; color: ${C.paper}; text-shadow: 0 0.04em 0 ${C.slate600}, 0 0.08em 0.25em rgba(0,0,0,0.5); }
.logo .side { font-weight: 700; color: ${C.amber}; font-size: 0.36em; line-height: 1; text-shadow: 0 0.06em 0.2em rgba(0,0,0,0.5); }
.logo .pack { font-weight: 800; color: ${C.paper}; font-size: 0.42em; line-height: 1.05; margin-top: 0.25em; padding: 0.08em 0.45em 0.02em;
  border-radius: 0.3em; background: ${C.night700}; border-bottom: 0.1em solid ${C.amber}; box-shadow: 0 0.08em 0.3em rgba(0,0,0,0.5); }
.stripe { position: absolute; left: 0; right: 0; bottom: 0; height: var(--st); display: flex; }
.stripe i { flex: 2; } .stripe i + i { flex: 1; }
`;

const crown = `<svg class="crown" viewBox="0 0 100 64"><path d="M6 58 L0 14 L28 34 L50 0 L72 34 L100 14 L94 58 Z" fill="${C.amber}" stroke="${C.amberDeep}" stroke-width="4" stroke-linejoin="round"/><circle cx="50" cy="40" r="7" fill="${C.coral}"/></svg>`;

const tower = () => `${BLOCKS.map((c, i) => `<div class="block${i === 11 ? " top" : ""}" style="--c:${c}"></div>`).join("")}${crown}`;

/** Seeded scatter of faint «?» glyphs; none on art-only assets (no words at all). */
function marks(w, h, u) {
  let s = 7;
  const r = () => ((s = (s * 16807) % 2147483647) / 2147483647);
  return Array.from({ length: 14 }, () => {
    const size = u * (6 + r() * 14);
    return `<span class="q" style="left:${r() * w - size / 3}px;top:${r() * h - size / 3}px;font-size:${size}px;transform:rotate(${(r() - 0.5) * 40}deg)">?</span>`;
  }).join("");
}

function logotype(name, pack) {
  const main = `<div class="main">${name.main}</div>`;
  return `<div class="logo">${name.above ? `<div class="side">${name.above}</div>` : ""}${main}${name.below ? `<div class="side">${name.below}</div>` : ""}${pack ? `<div class="pack">${pack}</div>` : ""}</div>`;
}

/** One asset as a page; layout by aspect: landscape tower right, portrait tower below, small capsule logo only. */
function page(a, name, pack) {
  const { w, h } = a;
  const u = Math.min(w, h) / 100;
  const land = w / h > 1.2;
  const small = a.name === "small";
  const text = a.kind === "text";
  // Tower block unit and position.
  const b = land ? h / 17 : h / 26;
  const towerX = a.towerX ?? (text && land ? w * 0.78 : w / 2);
  // Height above the base: 12 blocks, gaps, crown.
  const towerBottom = a.towerTop ? h - a.towerTop - b * 13.7 : land ? h * 0.06 : h * 0.04;
  const sx = `${towerX}px`;
  const showTower = !small;
  const stripe = pack ? `<div class="stripe" style="--st:${Math.max(4, u * 1.6)}px"><i style="background:${C.amber}"></i><i style="background:${C.sapphire}"></i><i style="background:${C.coral}"></i></div>` : "";
  const body = `
<div class="stage" style="width:${w}px;height:${h}px;--u:${u}px;--b:${b}px;--sx:${sx};${a.dim ? "filter:brightness(0.6) saturate(0.7);" : ""}">
  <div class="spot"></div><div class="glow"></div>
  ${text ? marks(w, h, u) : ""}
  ${showTower ? `<div class="tower" style="left:${towerX}px;bottom:${towerBottom}px;transform:translateX(-50%)"><div class="base"></div>${tower()}</div>` : ""}
  ${text ? logotype(name, pack) : ""}
  ${stripe}
</div>`;
  // Logo box: landscape left of the tower, portrait above it, small capsule nearly all of it.
  const box = small ? [w * 0.04, h * 0.06, w * 0.92, h * 0.82]
    : land ? [w * 0.05, h * 0.1, w * 0.58, h * 0.8]
    : [w * 0.07, h * 0.05, w * 0.86, h * 0.4];
  return { html: body, box };
}

/** In-page: grow the logotype until it fills `box` (x, y, w, h), centred. */
const FIT = `(box) => {
  const el = document.querySelector(".logo");
  if (!el) return;
  const [x, y, w, h] = box;
  let lo = 4, hi = 2000;
  while (hi - lo > 0.5) {
    const m = (lo + hi) / 2;
    el.style.fontSize = m + "px";
    const r = el.getBoundingClientRect();
    if (r.width <= w && r.height <= h) lo = m; else hi = m;
  }
  el.style.fontSize = lo + "px";
  const r = el.getBoundingClientRect();
  el.style.left = x + (w - r.width) / 2 + "px";
  el.style.top = y + (h - r.height) / 2 + "px";
}`;

/** Library logo: the logotype alone on transparent, 1280 wide or 720 tall (Valve). */
const LOGO_FIT = `() => {
  const el = document.querySelector(".logo");
  el.style.fontSize = "400px";
  el.style.padding = "0.06em 0.08em";
  let r = el.getBoundingClientRect();
  const s = Math.min(1280 / r.width, 720 / r.height);
  el.style.fontSize = 400 * s + "px";
  r = el.getBoundingClientRect();
  const w = r.width >= r.height * 1280 / 720 ? 1280 : Math.ceil(r.width);
  const h = w === 1280 ? Math.ceil(r.height) : 720;
  el.style.left = (w - r.width) / 2 + "px";
  el.style.top = (h - r.height) / 2 + "px";
  return [w, h];
}`;

/** The icon: an amber «?» over the night stage, readable at 16×16 (decision 87). */
function iconPage(size, rounded) {
  return `<div class="stage" style="width:${size}px;height:${size}px;${rounded ? `border-radius:${size * 0.2}px;` : ""}background:radial-gradient(circle at 50% 35%, ${C.night700}, ${C.night900} 80%);
    display:flex;align-items:center;justify-content:center;box-shadow:inset 0 0 0 ${size * 0.03}px ${C.amber}">
  <span style="font-family:'Baloo 2';font-weight:800;font-size:${size * 0.95}px;line-height:1;color:${C.amber};margin-top:${size * 0.16}px;
    text-shadow:0 ${size * 0.03}px 0 ${C.amberDeep}, 0 0 ${size * 0.12}px rgba(255,184,28,0.45)">?</span></div>`;
}

// Rendering -----------------------------------------------------------------------------------

let pg, evaluate;
const written = [];

async function render(file, w, h, html, { fit, logo, format = "png" } = {}) {
  if (only && !file.includes(only)) return;
  await evaluate(`(() => { document.head.innerHTML = ${JSON.stringify(`<style>${CSS}</style>`)}; document.body.innerHTML = ${JSON.stringify(html)}; })()`);
  await evaluate(`document.fonts.ready.then(() => document.fonts.load("800 40px 'Baloo 2'"))`);
  if (fit) await evaluate(`(${FIT})(${JSON.stringify(fit)})`);
  if (logo) {
    [w, h] = await evaluate(`(${LOGO_FIT})()`);
  }
  await evaluate(`new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(r)))`);
  const params = { format, ...(format === "jpeg" ? { quality: 95 } : {}), clip: { x: 0, y: 0, width: w, height: h, scale: 1 } };
  const { data } = await pg.send("Page.captureScreenshot", params);
  const out = path.join(OUT, file);
  await mkdir(path.dirname(out), { recursive: true });
  await writeFile(out, Buffer.from(data, "base64"));
  written.push(out);
  console.log(`  ${path.relative(REPO, out)}  ${w}×${h}`);
}

async function set(dir, assets, name, pack) {
  for (const a of assets) {
    if (a.kind === "logo") {
      await render(`${dir}/${a.name}.png`, 1600, 1000, logotype(name, pack).replace('class="logo"', 'class="logo" style="left:0;top:0"'), { logo: true });
      continue;
    }
    const { html, box } = page(a, name, pack);
    await render(`${dir}/${a.name}.png`, a.w, a.h, html, { fit: a.kind === "text" ? box : undefined });
  }
}

async function main() {
  if (!existsSync(path.join(REPO, "app", "client", "dist", "index.html"))) throw new Error("client not built: npm run build");
  const tmp = await mkdtemp(path.join(os.tmpdir(), "trivia-capsules-"));
  const procs = [];
  let display = process.env.DISPLAY;
  try {
    if (!visible) {
      const x = await startXvfb("Xvfb", 1920, 1080).catch((e) => {
        throw e.code === "ENOENT" ? new Error("Xvfb not found: run from the dev shell, or pass --visible") : e;
      });
      display = x.display;
      procs.push(x.proc);
    }
    const port = await freePort();
    const env = { ...process.env, DISPLAY: display, TRIVIA_SAVE_DIR: tmp, TRIVIA_STEAM_SDK: path.join(tmp, "no-steam"), TRIVIA_MUTE: "1" };
    const shellArgs = [`--remote-debugging-port=${port}`, "--remote-allow-origins=*", "--no-mods", "--disable-gpu"]; // GPU compositing under Xvfb stalls captures
    if (!visible) {
      // into Xvfb, not the desktop's Wayland
      delete env.WAYLAND_DISPLAY;
      delete env.NIXOS_OZONE_WL;
      shellArgs.push("--ozone-platform=x11");
    }
    const shell = spawn("trivia-desktop", shellArgs, {
      env,
      stdio: ["ignore", "ignore", "pipe"],
    });
    shell.stderr.on("data", (d) => process.env.DEBUG && process.stderr.write(d));
    procs.push(shell);
    pg = await connectPort(port);
    ({ evaluate } = pageHelpers(pg));
    await pg.send("Page.enable");
    // A viewport the hero fits in; transparent where the art leaves it.
    await pg.send("Emulation.setDeviceMetricsOverride", { width: 3840, height: 2160, deviceScaleFactor: 1, mobile: false });
    await pg.send("Emulation.setDefaultBackgroundColorOverride", { color: { r: 0, g: 0, b: 0, a: 0 } });
    await sleep(1500); // the game's own start settles before the page is replaced

    if (!only) await rm(OUT, { recursive: true, force: true });
    console.log("art");
    await set("art", ART);
    for (const [lang, name] of Object.entries(NAMES)) {
      console.log(lang);
      await set(lang, [...STORE, ...LIBRARY], name);
    }
    // DLC store pages: the store capsules only (no library entry of their own).
    for (const d of dlcs()) {
      for (const [lang, pack] of Object.entries(d.names)) {
        console.log(`dlc-${d.id} ${lang}`);
        await set(`dlc-${d.id}/${lang}`, STORE.filter((a) => a.kind === "text"), NAMES[lang] ?? NAMES.en, pack);
      }
    }
    console.log("icon");
    await render("icon-1024.png", 1024, 1024, iconPage(1024, true));
    await render("icon-256.png", 256, 256, iconPage(256, true));
    await render("app-icon-184.jpg", 184, 184, iconPage(184, false), { format: "jpeg" });
    await render("icon-16.png", 16, 16, iconPage(16, true));
    console.log(`${written.length} files in ${path.relative(REPO, OUT)}/`);
  } finally {
    pg?.close();
    for (const p of procs.reverse()) p.kill();
    await sleep(500);
    await rm(tmp, { recursive: true, force: true });
  }
}

main().catch((e) => {
  console.error(`capsules: ${e.message}`);
  process.exitCode = 1;
});
