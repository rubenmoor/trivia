// The save as one file (plan 55, SW-3): a dumb store, the client validates (parseSave).
import fs from "node:fs/promises";
import path from "node:path";

const MAX_BYTES = 10 * 1024 * 1024;
const RETRIES = 10;
const RETRY_MS = 100;
const LOCKED = new Set(["EPERM", "EBUSY", "EACCES"]);
const KINDS = new Set(["corrupt", "newer"]);

/** Error whose message is the code, so it survives IPC. */
export function saveError(code) {
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

  async function write(text) {
    if (!envelope(text)) throw saveError("bad_save");
    await fs.mkdir(dir, { recursive: true });
    const fd = await fs.open(tmp, "w");
    try {
      await fd.writeFile(text, "utf8");
      await fd.sync();
    } finally {
      await fd.close();
    }
    for (let attempt = 0; ; attempt++) {
      try {
        await rename(tmp, file);
        return;
      } catch (err) {
        if (!LOCKED.has(err.code) || attempt >= RETRIES) {
          await fs.rm(tmp, { force: true });
          throw LOCKED.has(err.code) ? saveError("save_locked") : err;
        }
        await new Promise((r) => setTimeout(r, RETRY_MS));
      }
    }
  }

  async function backup(kind) {
    if (!KINDS.has(kind)) throw new Error(`bad backup kind: ${kind}`);
    await fs.mkdir(backups, { recursive: true });
    const base = path.join(backups, `game-${kind}-${stamp()}`);
    for (let n = 1; ; n++) {
      const target = n === 1 ? `${base}.json` : `${base}-${n}.json`;
      try {
        await fs.access(target);
        continue;
      } catch {}
      await rename(file, target);
      return target;
    }
  }

  async function dropStaleTemp() {
    await fs.rm(tmp, { force: true });
  }

  return { file, read, write, backup, dropStaleTemp };
}
