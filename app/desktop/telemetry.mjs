// Opt-in telemetry store (plan 106, decisions 119, 121): consent + install id, one session file per run; no network.
import { randomUUID } from "node:crypto";
import fs from "node:fs/promises";
import path from "node:path";

const UUID = /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/;
// Plan 105's contract caps; bytes below its 64 KiB.
const MAX_GAMES = 30;
const MAX_ANSWERS = 500;
const MAX_GAME_ANSWERS = 100;
const MAX_BYTES = 60 * 1024;
const MAX_FILES = 5;
const MAX_LENGTH_S = 86400;

async function atomicWrite(file, text) {
  const tmp = `${file}.tmp`;
  try {
    const fd = await fs.open(tmp, "w");
    try {
      await fd.writeFile(text, "utf8");
      await fd.sync();
    } finally {
      await fd.close();
    }
    await fs.rename(tmp, file);
  } catch (err) {
    await fs.rm(tmp, { force: true });
    throw err;
  }
}

/** Store in `dir`; nothing is created until a yes. `version`: the game's (`app.getVersion()`). */
export function makeTelemetry(dir, { version, uptime = () => process.uptime() }) {
  const installFile = path.join(dir, "install.json");
  const sessions = path.join(dir, "sessions");
  let consent = null; // null: never asked
  let install = null;
  let current = null; // { session, games, index }
  let sealed = new Set(); // game keys in files closed by a rollover this run
  let writing = Promise.resolve();

  /** One file operation at a time, in order. */
  function queued(fn) {
    const p = writing.then(fn);
    writing = p.catch(() => {});
    return p;
  }

  const lengthS = () => Math.min(MAX_LENGTH_S, Math.max(0, Math.round(uptime())));
  const body = (s) => ({ session: s.session, install, version, length_s: lengthS(), games: s.games });
  const size = (games) => Buffer.byteLength(JSON.stringify(body({ session: current?.session ?? "", games })), "utf8");

  async function writeCurrent() {
    await fs.mkdir(sessions, { recursive: true });
    await atomicWrite(path.join(sessions, `${current.session}.json`), JSON.stringify({ ...body(current), index: current.index }));
  }

  /** Files on disk, oldest first; `*.json` only (incl. plan 107's `.retry.json`). */
  async function files() {
    let names;
    try {
      names = await fs.readdir(sessions);
    } catch (err) {
      if (err.code === "ENOENT") return [];
      throw err;
    }
    const list = [];
    for (const name of names.filter((n) => n.endsWith(".json"))) {
      const file = path.join(sessions, name);
      const stat = await fs.stat(file).catch(() => null);
      if (stat?.isFile()) list.push({ file, mtime: stat.mtimeMs });
    }
    return list.sort((a, b) => a.mtime - b.mtime);
  }

  async function begin() {
    const old = await files();
    for (const { file } of old.slice(0, Math.max(0, old.length - (MAX_FILES - 1)))) await fs.rm(file, { force: true });
    current = { session: randomUUID(), games: [], index: [] };
    await writeCurrent();
  }

  async function writeInstall() {
    await fs.mkdir(dir, { recursive: true });
    await atomicWrite(installFile, JSON.stringify(consent ? { consent: true, install } : { consent: false }));
  }

  /** Reads `install.json`; with a stored yes the run's session starts. */
  function start() {
    return queued(async () => {
      let doc = null;
      try {
        doc = JSON.parse(await fs.readFile(installFile, "utf8"));
      } catch {}
      consent = typeof doc?.consent === "boolean" ? doc.consent : null;
      if (!consent) return;
      if (UUID.test(doc.install)) install = doc.install;
      else {
        install = randomUUID();
        await writeInstall();
      }
      for (const f of await fs.readdir(sessions).catch(() => []))
        if (f.endsWith(".tmp")) await fs.rm(path.join(sessions, f), { force: true });
      await begin();
    });
  }

  const state = () => ({ available: true, consent });

  /** Yes: id if missing, session starts. No: `{consent: false}`, every session file and the id gone. */
  function setConsent(yes) {
    return queued(async () => {
      if (yes) {
        consent = true;
        install ??= randomUUID();
        await writeInstall();
        if (!current) await begin();
      } else {
        consent = false;
        install = null;
        current = null;
        sealed = new Set();
        await writeInstall();
        await fs.rm(sessions, { recursive: true, force: true });
      }
      return state();
    });
  }

  const load = () => (current ? { games: current.games, index: current.index } : null);

  /** This run's games (index parallel); games already sealed by a rollover are dropped. */
  function record({ games, index }) {
    return queued(async () => {
      if (!consent || !current) return;
      const keep = index.map((e) => !sealed.has(e.key));
      let todo = games
        .filter((_, i) => keep[i])
        .map((g) => (Array.isArray(g.answers) ? { ...g, answers: g.answers.slice(0, MAX_GAME_ANSWERS) } : g));
      let todoIndex = index.filter((_, i) => keep[i]);
      for (;;) {
        let n = 0;
        let answers = 0;
        while (n < todo.length) {
          const next = answers + (todo[n].answers?.length ?? 0);
          if (n + 1 > MAX_GAMES || next > MAX_ANSWERS || size(todo.slice(0, n + 1)) > MAX_BYTES) break;
          answers = next;
          n++;
        }
        n = Math.max(n, Math.min(1, todo.length)); // one game always fits (≤ 100 answers)
        current.games = todo.slice(0, n);
        current.index = todoIndex.slice(0, n);
        await writeCurrent();
        if (n === todo.length) return;
        for (const e of current.index) sealed.add(e.key);
        todo = todo.slice(n);
        todoIndex = todoIndex.slice(n);
        await begin();
      }
    });
  }

  /** Last `length_s` stamp, for `before-quit`; waits for pending writes. */
  const finish = () => queued(async () => current && writeCurrent());

  /** Leftover files from earlier runs (plan 107): `{ file, body }`, body null when unreadable. */
  async function pending() {
    const out = [];
    for (const { file } of await files()) {
      if (current && path.basename(file) === `${current.session}.json`) continue;
      let doc = null;
      try {
        doc = JSON.parse(await fs.readFile(file, "utf8"));
      } catch {}
      out.push({ file, body: doc });
    }
    return out;
  }

  return { dir, start, state, setConsent, load, record, finish, pending };
}
