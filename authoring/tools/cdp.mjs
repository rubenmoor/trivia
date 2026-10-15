// Raw CDP for the shell (store screenshots, capsules, trailer, packaged smoke game): no puppeteer.
import { spawn } from "node:child_process";
import { mkdtemp, rm } from "node:fs/promises";
import { createServer } from "node:net";
import os from "node:os";
import path from "node:path";

export const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

export function freePort() {
  return new Promise((resolve) => {
    const srv = createServer().listen(0, "127.0.0.1", () => {
      const { port } = srv.address();
      srv.close(() => resolve(port));
    });
  });
}

/** Xvfb on a free display (`-displayfd`): `{ display: ":N", proc }` once it accepts clients. */
export function startXvfb(exe, width, height) {
  return new Promise((resolve, reject) => {
    const proc = spawn(exe, ["-displayfd", "3", "-screen", "0", `${width}x${height}x24`, "-nolisten", "tcp"], {
      stdio: ["ignore", "ignore", "ignore", "pipe"],
    });
    let out = "";
    proc.stdio[3].on("data", (d) => {
      out += d;
      if (out.includes("\n")) resolve({ display: `:${out.trim()}`, proc });
    });
    proc.on("error", reject);
    proc.on("exit", (code) => reject(new Error(`Xvfb exited (${code}) before it reported a display`)));
  });
}

/**
 * `trivia-desktop` on a debugging port, a temp save dir, no Steam; under Xvfb (width × height) unless `visible`.
 * `visible: undefined`: the script has no `--visible`. `stop()` closes the page, kills the processes, removes the dir.
 */
export async function launchShell({ name, width, height, visible, env = {}, args = [] }) {
  const saveDir = await mkdtemp(path.join(os.tmpdir(), `trivia-${name}-`));
  const procs = [];
  let page;
  const stop = async () => {
    page?.close();
    for (const p of procs.reverse()) p.exitCode === null && p.kill();
    await sleep(500);
    await rm(saveDir, { recursive: true, force: true });
  };
  try {
    let display = process.env.DISPLAY;
    if (!visible) {
      const x = await startXvfb("Xvfb", width, height).catch((e) => {
        throw e.code === "ENOENT" ? new Error(`Xvfb not found: run from the dev shell${visible === false ? ", or pass --visible" : ""}`) : e;
      });
      display = x.display;
      procs.push(x.proc);
    }
    const port = await freePort();
    const shellEnv = { ...process.env, DISPLAY: display, TRIVIA_SAVE_DIR: saveDir, TRIVIA_STEAM_SDK: path.join(saveDir, "no-steam"), ...env };
    const shellArgs = [`--remote-debugging-port=${port}`, "--remote-allow-origins=*", ...args];
    if (!visible) {
      // into Xvfb, not the desktop's Wayland
      delete shellEnv.WAYLAND_DISPLAY;
      delete shellEnv.NIXOS_OZONE_WL;
      shellArgs.push("--ozone-platform=x11");
    }
    const shell = spawn("trivia-desktop", shellArgs, { env: shellEnv, stdio: ["ignore", "ignore", "pipe"] });
    shell.stderr.on("data", (d) => process.env.DEBUG && process.stderr.write(d));
    procs.push(shell);
    page = await connectPort(port);
    await page.send("Page.enable");
    return { page, display, saveDir, stop };
  } catch (e) {
    await stop();
    throw e;
  }
}

/** `{ send, close }` over a message transport; `sessionId` routes to an attached target; `gone` fails every pending call. */
function rpc(write, close, sessionId) {
  let id = 0;
  const waiting = new Map();
  const onMessage = (msg) => {
    const w = msg.id && waiting.get(msg.id);
    if (!w) return;
    waiting.delete(msg.id);
    msg.error ? w.reject(new Error(msg.error.message)) : w.resolve(msg.result);
  };
  const gone = (why) => {
    for (const w of waiting.values()) w.reject(new Error(why));
    waiting.clear();
  };
  const send = (method, params = {}, session = sessionId) =>
    new Promise((resolve, reject) => {
      waiting.set(++id, { resolve, reject });
      write(JSON.stringify({ id, method, params, ...(session ? { sessionId: session } : {}) }));
    });
  return { send, close, onMessage, gone };
}

/** The app:// page on `--remote-debugging-port`. */
export async function connectPort(port) {
  for (let i = 0; i < 100; i++) {
    try {
      const list = await (await fetch(`http://127.0.0.1:${port}/json/list`)).json();
      const page = list.find((t) => t.type === "page" && t.url.startsWith("app://"));
      if (page) return openSocket(page.webSocketDebuggerUrl);
    } catch {}
    await sleep(200);
  }
  throw new Error("no page target on the debugging port");
}

function openSocket(url) {
  const ws = new WebSocket(url);
  const r = rpc((s) => ws.send(s), () => ws.close());
  ws.onmessage = (ev) => r.onMessage(JSON.parse(ev.data));
  ws.onclose = () => r.gone("page connection closed");
  return new Promise((resolve, reject) => {
    ws.onopen = () => resolve(r);
    ws.onerror = () => reject(new Error(`can't open ${url}`));
  });
}

/** The app:// page on `--remote-debugging-pipe`: the child's fds 3 (in) and 4 (out), NUL-separated. */
export async function connectPipe(child) {
  const [, , , input, output] = child.stdio;
  let buf = "";
  const browser = rpc((s) => input.write(s + "\0"), () => input.end());
  input.on("error", () => {});
  output.on("error", () => {});
  output.on("close", () => browser.gone("debugging pipe closed"));
  output.setEncoding("utf8");
  output.on("data", (d) => {
    buf += d;
    for (let i; (i = buf.indexOf("\0")) >= 0; buf = buf.slice(i + 1)) browser.onMessage(JSON.parse(buf.slice(0, i)));
  });
  const exited = new Promise((_, reject) => child.once("exit", (code) => reject(new Error(`shell exited (${code})`))));
  exited.catch(() => {});
  for (let i = 0; i < 100; i++) {
    const { targetInfos } = await Promise.race([browser.send("Target.getTargets"), exited]);
    const page = targetInfos.find((t) => t.type === "page" && t.url.startsWith("app://"));
    if (page) {
      const { sessionId } = await browser.send("Target.attachToTarget", { targetId: page.targetId, flatten: true });
      return { send: (method, params) => browser.send(method, params, sessionId), close: browser.close };
    }
    await sleep(200);
  }
  throw new Error("no page target on the debugging pipe");
}

const q = (sel) => JSON.stringify(sel);
export const visibleEl = (sel) =>
  `(() => { const e = document.querySelector(${q(sel)}); return !!e && !e.disabled && e.getClientRects().length > 0; })()`;

/** evaluate, waitFor, click on a connected page. */
export function pageHelpers(page) {
  async function evaluate(expr) {
    // A call made during a reload may never get an answer.
    let timer;
    const timeout = new Promise((_, reject) => { timer = setTimeout(() => reject(new Error(`no answer: ${expr.slice(0, 60)}`)), 10000); });
    const call = page.send("Runtime.evaluate", { expression: expr, awaitPromise: true, returnByValue: true });
    const { result, exceptionDetails } = await Promise.race([call, timeout]).finally(() => clearTimeout(timer));
    if (exceptionDetails) throw new Error(`${expr}: ${exceptionDetails.exception?.description ?? exceptionDetails.text}`);
    return result.value;
  }
  async function waitFor(expr, what, ms = 15000) {
    for (const end = Date.now() + ms; Date.now() < end; await sleep(100)) {
      if (await evaluate(expr).catch(() => false)) return;
    }
    throw new Error(`timeout: ${what}`);
  }
  async function click(sel) {
    await waitFor(visibleEl(sel), sel);
    await evaluate(`document.querySelector(${q(sel)}).click()`);
  }
  return { evaluate, waitFor, click };
}
