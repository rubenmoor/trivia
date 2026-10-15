#!/usr/bin/env node
// Store trailer (plan 88, PUB-8, decisions 79/80): a scripted game in the shell under Xvfb, its audio
// through a private PulseAudio null sink, ffmpeg grabs both; the takes are cut to ≈20 s per language.
// Usage (dev shell): trivia-trailer [--lang es,es-ES,en,de] [--keep-raw]
// Needs app/client/dist (`npm run build`) and the media cache (`trivia-media sync --status approved`).
import { spawn } from "node:child_process";
import { existsSync } from "node:fs";
import { copyFile, mkdir, mkdtemp, rm, writeFile } from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { cacheName } from "../../app/desktop/resolve.mjs";
import { launchShell, pageHelpers, sleep, visibleEl } from "../tools/cdp.mjs";
import { gameAt, latestState, resetSeed } from "../tools/demo_saves.mjs";
import { loadData } from "../tools/engine_data.mjs";

const REPO = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..", "..");
const OUT = path.join(REPO, "authoring", "store", "out", "trailer");
const MEDIA = process.env.TRIVIA_MEDIA || path.join(REPO, "media");
const W = 1920;
const H = 1080;
const FPS = 30;

// Per question pool: q1 answered right after Soplo, q2 Francotirador then a wrong answer. Short, an image each.
const Q = { es: { q1: "q-0030", q2: "q-0019" } };
const LEVEL = 4; // q1's level; q2 one up

// The cut (seconds around the marks the walk sets): ≈20 s.
const CUT = [
  ["q1", -0.7, "hint", 1.4],
  ["lock1", -0.2, "final1", 0.6],
  ["reveal1", -0.3, "reveal1", 1.6],
  ["level", 1.0, "level", 2.4],
  ["snipe", -0.2, "shot", 1.3],
  ["lock2", -0.2, "final2", 0.6],
  ["reveal2", -0.3, "wrong", 2.1],
];
const FADE = 0.08; // audio fade at every cut, no clicks

const args = process.argv.slice(2);
const opt = (name) => {
  const i = args.indexOf(name);
  return i >= 0 ? args[i + 1] : undefined;
};
const LANGS = (opt("--lang") ?? "es,es-ES,en,de").split(",");
const keepRaw = args.includes("--keep-raw");

// Processes ----------------------------------------------------------------------------------

function run(cmd, argv, opts = {}) {
  return new Promise((resolve, reject) => {
    const p = spawn(cmd, argv, { stdio: ["ignore", "ignore", "pipe"], ...opts });
    let err = "";
    p.stderr.on("data", (d) => (err += d));
    p.on("error", reject);
    p.on("exit", (code) => (code === 0 ? resolve() : reject(new Error(`${cmd} exited (${code}): ${err.trim().split("\n").slice(-3).join(" / ")}`))));
  });
}

/** A private PulseAudio with one null sink: the shell plays into it, ffmpeg records its monitor. */
async function startPulse(dir) {
  const socket = path.join(dir, "pa.sock"); // not "pulse": PulseAudio makes that folder itself
  const proc = spawn(
    "pulseaudio",
    ["-n", "--daemonize=no", "--exit-idle-time=-1", "--use-pid-file=no", "--system=false", "--disable-shm=yes",
      "--load=module-null-sink sink_name=trailer rate=48000 channels=2",
      `--load=module-native-protocol-unix socket=${socket} auth-anonymous=1`],
    // own runtime dir and no session bus: never the desktop's sound server
    { env: { ...process.env, HOME: dir, XDG_RUNTIME_DIR: dir, DBUS_SESSION_BUS_ADDRESS: "unix:path=/nonexistent", DISPLAY: "" }, stdio: "ignore" },
  );
  proc.on("error", () => {});
  for (let i = 0; i < 50 && !existsSync(socket); i++) await sleep(100);
  if (!existsSync(socket)) throw new Error("pulseaudio didn't start: run from the dev shell (trivia-trailer)");
  return { server: `unix:${socket}`, proc };
}

/** ffmpeg grabbing the display and the sink; `starts`: each input's first timestamp (wall clock, s). */
function startRecording(display, server, file) {
  const proc = spawn("ffmpeg", [
    "-hide_banner", "-loglevel", "info", "-nostats",
    "-thread_queue_size", "1024", "-f", "x11grab", "-draw_mouse", "0", "-framerate", String(FPS), "-video_size", `${W}x${H}`, "-i", display,
    "-thread_queue_size", "1024", "-f", "pulse", "-server", server, "-sample_rate", "48000", "-channels", "2", "-i", "trailer.monitor",
    "-c:v", "libx264", "-preset", "ultrafast", "-crf", "12", "-c:a", "pcm_s16le", "-y", file,
  ], { stdio: ["pipe", "ignore", "pipe"] });
  const starts = [];
  let err = "";
  const ready = new Promise((resolve, reject) => {
    proc.stderr.on("data", (d) => {
      err += d;
      for (const m of err.matchAll(/^Input #(\d), .*\n.*start: ([\d.]+)/gm)) starts[+m[1]] = +m[2];
      if (starts[0] && starts[1]) resolve();
    });
    proc.on("error", (e) => reject(e.code === "ENOENT" ? new Error("ffmpeg not found: run from the dev shell (trivia-trailer)") : e));
    proc.on("exit", (code) => reject(new Error(`ffmpeg exited (${code}): ${err.trim().split("\n").slice(-2).join(" / ")}`)));
  });
  const stop = () => new Promise((resolve) => {
    proc.removeAllListeners("exit");
    proc.on("exit", resolve);
    proc.stdin.write("q");
  });
  return { ready, starts, stop, proc };
}

/** The cut: each CUT span from the raw take, audio faded at the edges; Valve's format (17a, "Trailer"). */
async function cut(raw, starts, marks, file) {
  const [v0, a0] = starts;
  const parts = [];
  let filter = "";
  CUT.forEach(([from, fromOff, to, toOff], i) => {
    if (marks[from] === undefined || marks[to] === undefined) throw new Error(`no mark ${marks[from] === undefined ? from : to}`);
    const s = marks[from] + fromOff;
    const e = marks[to] + toOff;
    const d = (e - s).toFixed(3);
    filter += `[0:v]trim=${(s - v0).toFixed(3)}:${(e - v0).toFixed(3)},setpts=PTS-STARTPTS[v${i}];`;
    filter += `[0:a]atrim=${(s - a0).toFixed(3)}:${(e - a0).toFixed(3)},asetpts=PTS-STARTPTS,afade=t=in:d=${FADE},afade=t=out:st=${(d - FADE).toFixed(3)}:d=${FADE}[a${i}];`;
    parts.push(`[v${i}][a${i}]`);
  });
  filter += `${parts.join("")}concat=n=${CUT.length}:v=1:a=1[v][a]`;
  await run("ffmpeg", [
    "-hide_banner", "-loglevel", "error", "-i", raw, "-filter_complex", filter, "-map", "[v]", "-map", "[a]",
    "-c:v", "libx264", "-preset", "slow", "-profile:v", "high", "-pix_fmt", "yuv420p", "-r", String(FPS), "-b:v", "20M", "-maxrate", "25M", "-bufsize", "40M",
    "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", "-movflags", "+faststart", "-y", file,
  ]);
  return CUT.reduce((sum, [from, fromOff, to, toOff]) => sum + marks[to] + toOff - marks[from] - fromOff, 0);
}

// The walk -----------------------------------------------------------------------------------

let page, evaluate, waitFor, click;
const marks = {};
const mark = (name) => (marks[name] = Date.now() / 1000);

const mediaReady = `[...document.images].every((i) => i.complete)`;
const answerEl = (i) => `.answers .answer:nth-child(${i + 1})`;

async function load(saveDir, save) {
  await sleep(800); // the last save write lands first
  await writeFile(path.join(saveDir, "game.json"), JSON.stringify(save));
  await page.send("Page.reload", { ignoreCache: true });
  await sleep(500);
  await waitFor(visibleEl("button.candy"), "start screen");
  await sleep(1000);
}

async function question(saveDir, save, name) {
  await load(saveDir, save);
  await click("button.candy"); // resume
  await waitFor(visibleEl(".answers .answer"), `${name}: question`);
  await waitFor(mediaReady, `${name}: media`, 10000).catch(() => {});
  mark(name);
}

/** Lock answer `i`, wait for the padlock, «Respuesta final», the reveal. */
async function finalAnswer(i, n) {
  await click(answerEl(i));
  mark(`lock${n}`);
  await waitFor(visibleEl(".final-button.ready"), "final answer ready", 5000);
  await sleep(400);
  await click(".final-button.ready");
  mark(`final${n}`);
  await waitFor(`!!document.querySelector(".answers .answer.right")`, "reveal", 20000); // tiles are disabled by then
  mark(`reveal${n}`);
}

async function walk(saveDir, data, ui, q) {
  resetSeed(); // the same game for every language and run
  const s1 = gameAt(data, ui, LEVEL, q.q1);
  await question(saveDir, s1, "q1");
  await sleep(1500);
  await click('.token[data-joker="hint"]'); // arm
  await sleep(300);
  await click('.token[data-joker="hint"]'); // play
  mark("hint");
  await sleep(2500);
  await finalAnswer(latestState(s1).answers.indexOf(data.byId.get(q.q1).answer), 1);
  await waitFor(visibleEl("section.result .title.good"), "correct screen", 10000);
  await sleep(1200);
  await click("section.result button");
  await waitFor(visibleEl("section.level"), "level screen", 10000);
  mark("level");
  await sleep(3000);

  const s2 = gameAt(data, ui, LEVEL + 1, q.q2);
  await question(saveDir, s2, "q2");
  const right = latestState(s2).answers.indexOf(data.byId.get(q.q2).answer);
  const aim = [1, 2, 3].find((i) => i !== right); // not tile 0: the crosshair starts there, a click on it would shoot
  const wrong = [0, 1, 2, 3].find((i) => i !== right && i !== aim);
  await sleep(1200);
  await click('.token[data-joker="snipe"]');
  mark("snipe");
  await sleep(500);
  await click(answerEl(aim));
  await sleep(700);
  await click(answerEl(aim)); // shoot
  mark("shot");
  await waitFor(`!!document.querySelector(".answers .answer.struck")`, "shot", 8000); // the joker is done
  await sleep(1500);
  await finalAnswer(wrong, 2);
  await waitFor(visibleEl("section.result.wrong"), "wrong screen", 10000);
  mark("wrong");
  await sleep(3200);
}

// Main ---------------------------------------------------------------------------------------

async function main() {
  if (!existsSync(path.join(REPO, "app", "client", "dist", "index.html"))) throw new Error("client not built: npm run build");
  const plans = [];
  for (const ui of LANGS) {
    const locale = ui.split("-")[0];
    const data = loadData(locale);
    if (!data || !Q[locale]) {
      console.error(`${ui}: no pool.${locale}.json yet: its trailer waits for the question pool (decision 80)`);
      continue;
    }
    for (const id of Object.values(Q[locale])) {
      const url = data.byId.get(id)?.media?.file_url;
      if (!url) throw new Error(`${id}: not in the pool or no media; pick another in Q`);
      if (!existsSync(path.join(MEDIA, cacheName(url)))) throw new Error(`${id}: media not cached: trivia-media sync --status approved`);
    }
    plans.push({ ui, data, q: Q[locale] });
  }
  if (!plans.length) {
    process.exitCode = 1;
    return;
  }

  await mkdir(OUT, { recursive: true });
  const pulseDir = await mkdtemp(path.join(os.tmpdir(), "trivia-pulse-"));
  const procs = [];
  let shell;
  try {
    const pulse = await startPulse(pulseDir);
    procs.push(pulse.proc);
    // X11, not the desktop's Wayland: ffmpeg grabs the Xvfb display
    shell = await launchShell({
      name: "trailer", width: W, height: H, args: ["--no-mods"],
      // dev user: the demo save loads, no notice; sound on even under PM_WORKER
      env: { PULSE_SERVER: pulse.server, TRIVIA_SOUND: "1", TRIVIA_DEV_STEAM_USER: "1" },
    });
    const tmp = shell.saveDir;
    page = shell.page;
    ({ evaluate, waitFor, click } = pageHelpers(page));
    // No window manager in Xvfb: fullscreen never applies, so the window is sized by hand.
    await run("xdotool", ["search", "--sync", "--name", "Trivia", "windowmove", "%@", "0", "0", "windowsize", "%@", String(W), String(H)], { env: { ...process.env, DISPLAY: shell.display } });
    await waitFor(`innerWidth === ${W} && innerHeight === ${H}`, "window at full size", 5000);

    for (const { ui, data, q } of plans) {
      console.log(ui);
      const raw = path.join(tmp, `${ui}.raw.mkv`);
      const rec = startRecording(shell.display, pulse.server, raw);
      procs.push(rec.proc);
      await rec.ready;
      for (const k of Object.keys(marks)) delete marks[k];
      await walk(tmp, data, ui, q).catch(async (e) => {
        const shot = path.join(OUT, `${ui}-failed.png`); // where the walk stopped
        const { data: png } = await page.send("Page.captureScreenshot", { format: "png" });
        await writeFile(shot, Buffer.from(png, "base64"));
        throw new Error(`${e.message} (screen: ${path.relative(REPO, shot)})`);
      });
      await rec.stop();
      const file = path.join(OUT, `${ui}.mp4`);
      const secs = await cut(raw, rec.starts, marks, file);
      console.log(`  ${path.relative(REPO, file)} (${secs.toFixed(1)} s)`);
      if (keepRaw) await copyFile(raw, path.join(OUT, `${ui}.raw.mkv`));
      await rm(raw, { force: true });
    }
  } finally {
    for (const p of procs.reverse()) p.exitCode === null && p.kill();
    await shell?.stop();
    await rm(pulseDir, { recursive: true, force: true });
  }
}

main().catch((e) => {
  console.error(`trailer: ${e.message}`);
  process.exitCode = 1;
});
