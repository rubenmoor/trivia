// The save as one file (plan 55, SW-3): a dumb store, the client validates (parseSave).
import fs from "node:fs/promises";
import path from "node:path";

const MAX_BYTES = 10 * 1024 * 1024;
const RETRIES = 10;
const RETRY_MS = 100;
const LOCKED = new Set(["EPERM", "EBUSY", "EACCES"]);
const KINDS = new Set(["corrupt", "newer"]);

/** Error whose message is the code, so it survives IPC. */
function saveError(code) {
  const err = new Error(code);
  err.code = code;
  return err;
}

function envelope(text) {
  if (typeof text !== "string" || Buffer.byteLength(text, "utf8") > MAX_BYTES) return false;
  let doc;
  try {
    doc = JSON.parse(text);
  } catch {
    return false;
  }
  return doc !== null && typeof doc === "object" && !Array.isArray(doc) && typeof doc.version === "number";
}

const pad = (n) => String(n).padStart(2, "0");
function stamp(d = new Date()) {
  return `${d.getFullYear()}${pad(d.getMonth() + 1)}${pad(d.getDate())}-${pad(d.getHours())}${pad(d.getMinutes())}${pad(d.getSeconds())}`;
}

const exists = (p) =>
  fs.access(p).then(
    () => true,
    () => false,
  );

export function makeSaveFile(dir, { rename = fs.rename } = {}) {
  const file = path.join(dir, "game.json");
  const tmp = file + ".tmp";
  const backups = path.join(dir, "backup");

  async function read() {
    try {
      return await fs.readFile(file, "utf8");
    } catch (err) {
      if (err.code === "ENOENT") return null;
      throw err;
    }
  }

  /** Rename, retried while Windows holds `to` (or `from`) open → save_locked. */
  async function move(from, to) {
    for (let attempt = 0; ; attempt++) {
      try {
        return await rename(from, to);
      } catch (err) {
        if (!LOCKED.has(err.code)) throw err;
        if (attempt >= RETRIES) throw saveError("save_locked");
        await new Promise((r) => setTimeout(r, RETRY_MS));
      }
    }
  }

  async function write(text) {
    if (!envelope(text)) throw saveError("bad_save");
    await fs.mkdir(dir, { recursive: true });
    try {
      const fd = await fs.open(tmp, "w");
      try {
        await fd.writeFile(text, "utf8");
        await fd.sync();
      } finally {
        await fd.close();
      }
      await move(tmp, file);
    } catch (err) {
      await fs.rm(tmp, { force: true });
      throw err;
    }
  }

  /** game.json → backup/game-<kind>-<stamp>.json, moved or copied. */
  async function stash(kind, op) {
    await fs.mkdir(backups, { recursive: true });
    const base = path.join(backups, `game-${kind}-${stamp()}`);
    for (let n = 1; ; n++) {
      const target = n === 1 ? `${base}.json` : `${base}-${n}.json`;
      if (await exists(target)) continue;
      await op(file, target);
      return target;
    }
  }

  async function backup(kind) {
    if (!KINDS.has(kind)) throw new Error(`bad backup kind: ${kind}`);
    return stash(kind, move);
  }

  /** `text` as the save; a present save needs `force` and is copied to backup/ first. → backup path | null. */
  async function importText(text, { force = false } = {}) {
    if (!envelope(text)) throw saveError("not a save (JSON object with a numeric version, at most 10 MB)");
    if ((await read()) !== null) {
      if (!force) throw saveError(`${file} exists, not overwritten (--force: replace it, old one to backup/)`);
      const kept = await stash("import", (from, to) => fs.copyFile(from, to));
      await write(text);
      return kept;
    }
    await write(text);
    return null;
  }

  async function dropStaleTemp() {
    await fs.rm(tmp, { force: true });
  }

  return { file, read, write, backup, importText, dropStaleTemp };
}
