// app:// URL → file (plan 54). Web Request/Response only, so plain `node` can test it.
import { createHash } from "node:crypto";
import { open, readdir, readFile, realpath, stat } from "node:fs/promises";
import path from "node:path";

const MIME = {
  ".html": "text/html; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".mjs": "text/javascript; charset=utf-8",
  ".map": "application/json; charset=utf-8",
  ".txt": "text/plain; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".woff2": "font/woff2",
  ".woff": "font/woff",
  ".ttf": "font/ttf",
  ".otf": "font/otf",
  ".ico": "image/x-icon",
  ".wasm": "application/wasm",
  ".m4a": "audio/mp4",
  ".mp3": "audio/mpeg",
  ".ogg": "audio/ogg",
  ".oga": "audio/ogg",
  ".opus": "audio/ogg",
  ".wav": "audio/wav",
  ".webm": "video/webm",
  ".mp4": "video/mp4",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".png": "image/png",
  ".gif": "image/gif",
  ".webp": "image/webp",
  ".svg": "image/svg+xml",
  ".avif": "image/avif",
};

const mimeOf = (file) => MIME[path.extname(file).toLowerCase()] ?? "application/octet-stream";

const json = (status, body) =>
  new Response(JSON.stringify(body), { status, headers: { "content-type": MIME[".json"] } });

// Root's realpath, once per root (a missing root: retried).
const roots = new Map();
async function realRoot(root) {
  if (!roots.has(root)) {
    const real = await realpath(root).catch(() => null);
    if (!real) return null;
    roots.set(root, real);
  }
  return roots.get(root);
}

// File under root, or null (no escape, symlinks included; files only).
export async function contained(root, rel) {
  const real = await realRoot(root);
  if (!real) return null;
  try {
    const file = await realpath(path.resolve(root, "." + path.posix.normalize("/" + rel)));
    if (!file.startsWith(real + path.sep)) return null;
    return (await stat(file)).isFile() ? file : null;
  } catch {
    return null;
  }
}

const sameFile = process.platform === "win32" ? (a, b) => a.toLowerCase() === b.toLowerCase() : (a, b) => a === b;

// Client files: no hashes in their names (decision 124), so never reused unchecked.
const CLIENT = { "cache-control": "no-cache" };

// A mod's own files, never overlaid (decision 148): mod.json, its entry, its root style.css.
const OWN = ["mod.json", "style.css"];
async function ownFiles(dir, entry) {
  const real = await realRoot(dir);
  const files = await Promise.all([...OWN, ...(entry ? [entry] : [])].map((rel) => contained(dir, rel)));
  return real ? [path.join(real, "mod.json"), ...files.filter(Boolean)] : [];
}

// First hit in the layers; hidden: a mod's own files (dir → Promise<paths>).
async function firstHit(roots, rel, hidden) {
  for (const root of roots) {
    const file = await contained(root, rel);
    if (file && !(hidden.has(root) && (await hidden.get(root)).some((f) => sameFile(file, f)))) return file;
  }
  return null;
}

// Single range only; null = whole file, false = unsatisfiable. As authoring/tools/http_base.py parse_range.
function parseRange(header, size) {
  const m = /^bytes=(\d*)-(\d*)$/.exec(header?.trim() ?? "");
  if (!m || (m[1] === "" && m[2] === "")) return null;
  let start, end;
  if (m[1] === "") {
    start = Math.max(0, size - Number(m[2]));
    end = size - 1;
  } else {
    start = Number(m[1]);
    end = m[2] === "" ? size - 1 : Math.min(Number(m[2]), size - 1);
  }
  return start > end || start >= size ? false : { start, end };
}

const CHUNK = 256 * 1024;

// Bytes start..end, read per pull. Not Readable.toWeb: a cancel mid-read (a dropped video) throws uncaught there (Node 22/24).
function body(file, start, end) {
  let fh = null;
  let pos = start;
  const close = () => fh?.close().catch(() => {});
  return new ReadableStream({
    async start() {
      fh = await open(file, "r");
    },
    async pull(c) {
      const want = Math.min(CHUNK, end - pos + 1);
      const { bytesRead, buffer } = want > 0 ? await fh.read(Buffer.allocUnsafe(want), 0, want, pos) : { bytesRead: 0 };
      if (!bytesRead) {
        await close();
        c.close();
        return;
      }
      pos += bytesRead;
      c.enqueue(new Uint8Array(buffer.buffer, buffer.byteOffset, bytesRead));
    },
    cancel: close,
  });
}

async function sendFile(file, request, extra = {}) {
  const { size } = await stat(file);
  const headers = { "content-type": mimeOf(file), "accept-ranges": "bytes", ...extra };
  const range = parseRange(request.headers.get("range"), size);
  if (range === false)
    return new Response(null, { status: 416, headers: { ...headers, "content-range": `bytes */${size}` } });
  if (range) {
    const { start, end } = range;
    return new Response(body(file, start, end), {
      status: 206,
      headers: { ...headers, "content-length": String(end - start + 1), "content-range": `bytes ${start}-${end}/${size}` },
    });
  }
  return new Response(size ? body(file, 0, size - 1) : null, { status: 200, headers: { ...headers, "content-length": String(size) } });
}

// Same name as authoring/tools/media_cache.py cache_path (D-17).
export function cacheName(url) {
  let ext = "";
  try {
    ext = path.posix.extname(new URL(url).pathname).toLowerCase();
  } catch {}
  if (!/^\.[a-z0-9]{1,5}$/.test(ext)) ext = ".bin";
  return createHash("sha1").update(url, "utf8").digest("hex").slice(0, 16) + ext;
}

// Packaged name (decision 185): cacheName's stem + the encoded format's extension.
const SHIPPED = {
  ...Object.fromEntries([".jpg", ".jpeg", ".png"].map((e) => [e, ".webp"])),
  ...Object.fromEntries([".mp3", ".ogg", ".oga", ".wav", ".flac", ".m4a"].map((e) => [e, ".opus"])),
  ...Object.fromEntries([".mp4", ".mov", ".ogv", ".mkv"].map((e) => [e, ".webm"])),
};
export function shippedName(url) {
  const name = cacheName(url);
  const ext = path.posix.extname(name);
  return name.slice(0, -ext.length) + (SHIPPED[ext] ?? ext);
}

// Every picked file_url in the pool, like authoring/tools/media_cache.py pool_urls; stage-media.mjs ships the same set.
export const poolUrls = ({ questions }) =>
  new Set(questions.flatMap((q) => [q.media?.file_url, q.background?.file_url]).filter(Boolean));

// es pool files in data/: base's, the demo's (demo/; the demo build has no full pool) and every installed pack's (decision 66).
async function poolFiles(data) {
  const packs = await readdir(path.join(data, "bundles")).catch(() => []);
  const has = (file) => stat(file).then(() => true, () => false);
  const base = path.join(data, "pool.json");
  const demo = path.join(data, "demo", "pool.json");
  const demoOnly = !(await has(base)) && (await has(demo));
  return [...(demoOnly ? [] : [base]), ...((await has(demo)) ? [demo] : []), ...packs.map((b) => path.join(data, "bundles", b, "pool.json"))];
}

// The pool's URLs, re-read when a pool file changes (qgen export in dev); a broken one: skipped, one stderr line.
function pooledUrls(data) {
  const seen = new Map(); // file → { key, urls }
  return async () => {
    const out = new Set();
    for (const file of await poolFiles(data)) {
      let hit = seen.get(file);
      try {
        const { mtimeMs, size } = await stat(file);
        if (hit?.key !== `${mtimeMs}:${size}`) {
          hit = { key: `${mtimeMs}:${size}`, urls: poolUrls(JSON.parse(await readFile(file, "utf8"))) };
          seen.set(file, hit);
        }
      } catch (err) {
        if (err.code === "ENOENT" && file !== path.join(data, "pool.json")) continue; // a pack folder without a pool
        if (hit?.key !== "bad") console.error(`trivia: ${file}: ${err.message}`);
        hit = { key: "bad", urls: new Set() };
        seen.set(file, hit);
      }
      for (const u of hit.urls) out.add(u);
    }
    return out;
  };
}

// Our bundles.json + loaded mods' rows, top first (decision 128); ids namespaced `<mod>:<id>`.
async function mergedBundles(data, mods) {
  const ours = JSON.parse(await readFile(path.join(data, "bundles.json"), "utf8"));
  const rows = mods.flatMap((m) =>
    m.bundles.map((row) => ({ ...row, id: `${m.id}:${row.id}`, source: "mod", mod: m.id, modName: m.name })),
  );
  return { ...ours, bundles: [...ours.bundles, ...rows] };
}

// layers: enabled mods' folders, top first (plan 112); ours last. mods: the loaded ones { id, name, dir, entry?, bundles }, same order.
// modsJs: `/mods.js` text (mods.mjs modsScript, decision 131).
export function makeResolver({ dist, data, media, layers = [], mods = [], modsJs = "export default [];\n" }) {
  dist = path.resolve(dist);
  data = path.resolve(data);
  media = path.resolve(media);
  const distRoots = [...layers.map((d) => path.resolve(d)), dist];
  const entries = new Map(mods.map((m) => [path.resolve(m.dir), m.entry]));
  const hidden = new Map(distRoots.slice(0, -1).map((d) => [d, ownFiles(d, entries.get(d))]));
  const byId = new Map(mods.map((m) => [m.id, m]));
  let merged = null; // built once per run: the layers are fixed
  const urls = pooledUrls(data);
  return async (request) => {
    const url = new URL(request.url);
    let rel;
    try {
      rel = decodeURIComponent(url.pathname);
    } catch {
      return json(404, { error: "not_found" });
    }
    if (rel === "/api" || rel.startsWith("/api/")) return json(404, { error: "not_found" });
    if (rel === "/mods.js")
      return new Response(modsJs, { status: 200, headers: { "content-type": MIME[".js"], ...CLIENT } });
    if (rel.startsWith("/mods/")) {
      const m = /^\/mods\/([^/]+)\/(.+)$/.exec(rel);
      const mod = m && byId.get(m[1]);
      const file = mod && (await contained(mod.dir, m[2]));
      if (!file || sameFile(file, path.join(await realRoot(mod.dir), "mod.json"))) return json(404, { error: "not_found" });
      return sendFile(file, request, CLIENT);
    }
    if (rel === "/data/bundles.json" && mods.length) {
      merged ??= mergedBundles(data, mods).catch((err) => {
        console.error(`trivia: bundles.json: ${err.message}`);
        return null;
      });
      const doc = await merged;
      return doc ? json(200, doc) : json(404, { error: "not_found" });
    }
    if (rel.startsWith("/data/")) {
      const m = /^\/data\/bundles\/([^/:]+):([^/:]+)\/(.+)$/.exec(rel);
      const mod = m && byId.get(m[1]);
      let file = null;
      if (mod?.bundles.some((b) => b.id === m[2])) file = await contained(path.join(mod.dir, "data", "bundles", m[2]), m[3]);
      else if (!rel.includes(":")) file = await contained(data, rel.slice("/data/".length));
      return file ? sendFile(file, request) : json(404, { error: "not_found" });
    }
    if (rel === "/media") {
      const fileUrl = url.searchParams.get("url") ?? "";
      if (!(await urls()).has(fileUrl)) return json(404, { error: "not_found" });
      const file = (await contained(media, cacheName(fileUrl))) ?? (await contained(media, shippedName(fileUrl)));
      return file ? sendFile(file, request) : json(404, { error: "media_missing" });
    }
    const file =
      (rel !== "/" && (await firstHit(distRoots, rel, hidden))) || (await firstHit(distRoots, "index.html", hidden));
    return sendFile(file || path.join(dist, "index.html"), request, CLIENT);
  };
}
