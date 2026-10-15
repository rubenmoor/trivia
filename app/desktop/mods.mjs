// Mods (plan 112): mod.json validator, discovery, per-machine settings, load order. Bytes only: no mod file is run here.
import fs from "node:fs/promises";
import path from "node:path";

const MAX_BYTES = 64 * 1024;
const MAX_WALK = 10000;
export const ID = /^[a-z0-9][a-z0-9-]{1,63}$/;
const SEMVER = /^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$/;
const WORKSHOP_ID = /^[1-9]\d{0,19}$/;
// UI_LANGS in app/client/src/lib/i18n.ts.
const LANGS = new Set(["es", "es-ES", "en", "de"]);
const KINDS = ["bundle", "theme", "code", "conversion"];
const KEYS = new Set(["id", "name", "description", "version", "game", "languages", "entry", "kind", "workshopId"]);

const chars = (s) => [...s].length;
const isObject = (v) => v !== null && typeof v === "object" && !Array.isArray(v);
const isString = (v, min, max) => typeof v === "string" && chars(v) >= min && chars(v) <= max;
const sameVersion = (a, b) => {
  const pa = SEMVER.exec(a);
  const pb = SEMVER.exec(b ?? "");
  return !!pb && [1, 2, 3].every((i) => Number(pa[i]) === Number(pb[i]));
};

const exists = (p, test) =>
  fs.stat(p).then(
    (s) => test(s),
    () => false,
  );

/** File `rel` inside `dir` after symlinks, or null. */
async function inside(dir, rel) {
  try {
    const root = await fs.realpath(dir);
    const file = await fs.realpath(path.resolve(root, rel));
    return file.startsWith(root + path.sep) && (await fs.stat(file)).isFile() ? file : null;
  } catch {
    return null;
  }
}

/** Any .css below dir (symlinks not followed, capped). */
async function hasCss(dir) {
  const queue = [dir];
  for (let seen = 0; queue.length && seen < MAX_WALK; ) {
    const entries = await fs.readdir(queue.shift(), { withFileTypes: true }).catch(() => []);
    for (const e of entries) {
      seen++;
      if (e.isFile() && e.name.toLowerCase().endsWith(".css")) return true;
      if (e.isDirectory()) queue.push(path.join(e.parentPath ?? e.path, e.name));
    }
  }
  return false;
}

async function deriveKind(dir, entry) {
  const kind = [];
  if (await exists(path.join(dir, "data", "bundles"), (s) => s.isDirectory())) kind.push("bundle");
  else if (await exists(path.join(dir, "data", "bundles.json"), (s) => s.isFile())) kind.push("bundle");
  if (await hasCss(dir)) kind.push("theme");
  if (entry) kind.push("code");
  if (await exists(path.join(dir, "index.html"), (s) => s.isFile())) kind.push("conversion");
  return kind;
}

/** First field error of a parsed manifest, or null; pushes warnings. */
function checkFields(m, gameVersion, warnings) {
  const bad = (field) => ({ code: "bad_field", field });
  if (typeof m.id !== "string" || !ID.test(m.id)) return bad("id");
  if (!isString(m.name, 1, 80) || !m.name.trim()) return bad("name");
  if (!isString(m.description, 0, 2000)) return bad("description");
  if (!isString(m.version, 1, 32)) return bad("version");
  if (typeof m.game !== "string" || !SEMVER.test(m.game)) return bad("game");
  if (m.languages !== undefined) {
    if (!Array.isArray(m.languages) || !m.languages.every((l) => typeof l === "string")) return bad("languages");
    for (const tag of m.languages) if (!LANGS.has(tag)) warnings.push({ code: "unknown_language", tag });
  }
  if (m.entry !== undefined && (typeof m.entry !== "string" || !/\.m?js$/.test(m.entry))) return bad("entry");
  if (m.kind !== undefined) {
    const ok = Array.isArray(m.kind) && m.kind.every((k) => KINDS.includes(k)) && new Set(m.kind).size === m.kind.length;
    if (!ok) return bad("kind");
  }
  if (m.workshopId !== undefined && (typeof m.workshopId !== "string" || !WORKSHOP_ID.test(m.workshopId)))
    return bad("workshopId");
  for (const key of Object.keys(m)) if (!KEYS.has(key)) warnings.push({ code: "unknown_key", key });
  if (!sameVersion(m.game, gameVersion)) warnings.push({ code: "game_version", game: m.game, running: gameVersion });
  return null;
}

/** One mod folder → { id, dir, manifest, kind, warnings, error }; id null when unknown. */
export async function readManifest(dir, gameVersion) {
  dir = path.resolve(dir);
  const out = { id: null, dir, manifest: null, kind: [], bundles: [], style: false, warnings: [], error: null };
  const fail = (error) => ({ ...out, error });
  if (!(await exists(dir, (s) => s.isDirectory()))) return fail({ code: "not_a_folder" });
  const file = path.join(dir, "mod.json");
  let bytes;
  try {
    if ((await fs.stat(file)).size > MAX_BYTES) return fail({ code: "bad_json", reason: "too_big" });
    bytes = await fs.readFile(file);
  } catch {
    return fail({ code: "no_manifest" });
  }
  let m;
  try {
    m = JSON.parse(new TextDecoder("utf-8", { fatal: true }).decode(bytes));
  } catch {
    return fail({ code: "bad_json" });
  }
  if (!isObject(m)) return fail({ code: "bad_json" });
  out.manifest = m;
  if (typeof m.id === "string" && ID.test(m.id)) out.id = m.id;
  const error = checkFields(m, gameVersion, out.warnings);
  if (error) return fail(error);
  if (m.entry !== undefined && !(await inside(dir, m.entry))) return fail({ code: "entry_missing" });
  out.kind = m.kind ?? (await deriveKind(dir, m.entry));
  out.style = !!(await inside(dir, "style.css"));
  const bundles = await bundleRows(dir);
  out.bundles = bundles.rows;
  out.warnings.push(...bundles.warnings);
  return out;
}

const BUNDLE_BYTES = 256 * 1024;
const SLUG = /^[a-z0-9][a-z0-9-]{0,63}$/;

/** `<dir>/data/bundles.json` rows (plan 115), structure and slugs only; ids as in the file. */
export async function bundleRows(dir) {
  const file = path.join(dir, "data", "bundles.json");
  const bad = { rows: [], warnings: [{ code: "bundle_json" }] };
  let doc;
  try {
    if ((await fs.stat(file)).size > BUNDLE_BYTES) return bad;
    doc = JSON.parse(new TextDecoder("utf-8", { fatal: true }).decode(await fs.readFile(file)));
  } catch (err) {
    return err.code === "ENOENT" ? { rows: [], warnings: [] } : bad;
  }
  if (!isObject(doc) || !Array.isArray(doc.bundles)) return bad;
  const rows = [];
  const warnings = [];
  const ids = new Set();
  for (const row of doc.bundles) {
    const ok =
      isObject(row) &&
      typeof row.id === "string" &&
      SLUG.test(row.id) &&
      !ids.has(row.id) &&
      typeof row.kind === "string" &&
      SLUG.test(row.kind) &&
      Array.isArray(row.languages) &&
      row.languages.every((l) => typeof l === "string") &&
      typeof row.name === "string" &&
      typeof row.description === "string";
    if (!ok) {
      warnings.push({ code: "bundle_row", id: typeof row?.id === "string" ? row.id : null });
      continue;
    }
    ids.add(row.id);
    rows.push(row);
  }
  return { rows, warnings };
}

/** Local mods folder, then Workshop items (lowest published file id first); later duplicates invalid. */
export async function discover({ local, workshop = [] }, gameVersion) {
  const mods = [];
  if (local) {
    const entries = await fs.readdir(local, { withFileTypes: true }).catch(() => []);
    for (const name of entries.map((e) => e.name).sort()) {
      const dir = path.resolve(local, name);
      if (!(await exists(dir, (s) => s.isDirectory()))) continue;
      if (!(await exists(path.join(dir, "mod.json"), () => true))) {
        console.error(`trivia: mods: ${dir}: no mod.json, ignored`);
        continue;
      }
      mods.push({ ...(await readManifest(dir, gameVersion)), source: "local", publishedFileId: null });
    }
  }
  const items = [...workshop].sort((a, b) => {
    const [x, y] = [BigInt(a.publishedFileId), BigInt(b.publishedFileId)];
    return x < y ? -1 : x > y ? 1 : 0;
  });
  for (const { dir, publishedFileId, state, warnings = [] } of items) {
    const source = { source: "workshop", publishedFileId: String(publishedFileId) };
    // Not on disk this run (downloading, disabled): listed, not loaded.
    if (!dir) {
      mods.push({ id: null, dir: null, manifest: null, kind: [], warnings, error: null, ...source, state });
      continue;
    }
    const mod = { ...(await readManifest(dir, gameVersion)), ...source };
    mod.warnings.unshift(...warnings);
    const named = mod.manifest?.workshopId;
    if (!mod.error && named !== undefined && named !== source.publishedFileId)
      mod.warnings.push({ code: "workshop_id_mismatch", workshopId: named });
    mods.push(mod);
  }
  const owner = new Map();
  for (const mod of mods) {
    if (mod.error || !mod.id) continue;
    const other = owner.get(mod.id);
    if (other) mod.error = { code: "duplicate_id", other: other.dir, publishedFileId: other.publishedFileId };
    else owner.set(mod.id, mod);
  }
  return mods;
}

const EMPTY = () => ({ version: 1, mods: [] });

/** mods.json; missing → empty; unreadable → empty, one stderr line, file left alone. */
export async function readSettings(file) {
  let doc;
  try {
    doc = JSON.parse(await fs.readFile(file, "utf8"));
  } catch (err) {
    if (err.code !== "ENOENT") console.error(`trivia: mods: ${file}: ${err.message}, using none`);
    return EMPTY();
  }
  const ok =
    isObject(doc) &&
    doc.version === 1 &&
    Array.isArray(doc.mods) &&
    doc.mods.every((e) => isObject(e) && typeof e.id === "string" && typeof e.on === "boolean");
  if (!ok) {
    console.error(`trivia: mods: ${file}: not a version 1 settings file, using none`);
    return EMPTY();
  }
  const seen = new Set();
  return { ...doc, mods: doc.mods.filter((e) => !seen.has(e.id) && seen.add(e.id)) };
}

/** One-time notice accepted on this machine (plan 118). */
export const noticed = (settings) => settings.notice === true;

/** Settings with the notice accepted now; rows untouched. */
export const withNotice = (settings) => ({ ...settings, notice: true, noticeAt: new Date().toISOString() });

/** Atomic: temp + rename. */
export function writeSettings(file, settings) {
  return writeJson(file, settings);
}

async function writeJson(file, value) {
  const tmp = file + ".tmp";
  await fs.mkdir(path.dirname(file), { recursive: true });
  try {
    const fd = await fs.open(tmp, "w");
    try {
      await fd.writeFile(JSON.stringify(value, null, 2) + "\n", "utf8");
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

/** Crash marker `mods-start.json` (plan 118): `{ at, mods }`; any file there counts, unreadable → `mods: []`; none → null. */
export async function readMarker(file) {
  let text;
  try {
    text = await fs.readFile(file, "utf8");
  } catch (err) {
    if (err.code === "ENOENT") return null;
    return { at: null, mods: [] };
  }
  try {
    const doc = JSON.parse(text);
    const mods = Array.isArray(doc?.mods) ? doc.mods.filter((id) => typeof id === "string" && ID.test(id)) : [];
    return { at: typeof doc?.at === "string" ? doc.at : null, mods };
  } catch {
    return { at: null, mods: [] };
  }
}

/** Atomic like the settings. */
export function writeMarker(file, ids) {
  return writeJson(file, { at: new Date().toISOString(), mods: ids });
}

export function clearMarker(file) {
  return fs.rm(file, { force: true });
}

/**
 * Discovered mods + settings → { list, layers, settings, changed }.
 * New ids appended `on`, `off` until the notice is accepted; unknown ids kept (`missing`); layers: loaded dirs, index 0 = top = wins.
 */
export function arrange(mods, settings, { validUser }) {
  const known = new Set(settings.mods.map((e) => e.id));
  const on = noticed(settings);
  const added = mods.filter((m) => m.id && !known.has(m.id) && known.add(m.id)).map((m) => ({ id: m.id, on }));
  const next = added.length ? { ...settings, mods: [...settings.mods, ...added] } : settings;
  const primary = new Map(mods.filter((m) => m.id && m.error?.code !== "duplicate_id").map((m) => [m.id, m]));
  const list = next.mods.map(({ id, on }, position) => {
    const mod = primary.get(id);
    if (!mod) return { id, on, position, state: "missing" };
    const state = mod.error ? "invalid" : !on ? "off" : !validUser ? "no_user" : "loaded";
    return { ...mod, on, position, state };
  });
  for (const mod of mods)
    if (!mod.dir) list.push({ ...mod, on: false, position: null });
    else if (!mod.id || mod.error?.code === "duplicate_id")
      list.push({ ...mod, on: false, position: null, state: "invalid" });
  const layers = list.filter((e) => e.state === "loaded").map((e) => e.dir);
  return { list, layers, settings: next, changed: next !== settings };
}

const modUrl = (id, rel) =>
  `/mods/${id}/` + path.posix.normalize("/" + rel.replaceAll("\\", "/")).slice(1).split("/").map(encodeURIComponent).join("/");

/** `/mods.js` text (decision 131): loaded mods in run order, bottom of the load order first. */
export function modsScript(list) {
  const rows = list
    .filter((m) => m.state === "loaded")
    .reverse()
    .map(({ id, manifest: m, style }) => ({
      id,
      name: m.name,
      version: m.version,
      entry: m.entry === undefined ? null : modUrl(id, m.entry),
      style: style ? modUrl(id, "style.css") : null,
    }));
  return rows.length ? `export default [\n${rows.map((r) => "  " + JSON.stringify(r)).join(",\n")}\n];\n` : "export default [];\n";
}
