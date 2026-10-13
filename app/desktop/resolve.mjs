// app:// URL → file (plan 54). Web Request/Response only, so plain `node` can test it.
import { createHash } from "node:crypto";
import { createReadStream } from "node:fs";
import { readdir, readFile, stat } from "node:fs/promises";
import path from "node:path";
import { Readable } from "node:stream";

const MIME = {
  ".html": "text/html; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".woff2": "font/woff2",
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

// File under root, or null (no escape, files only).
async function contained(root, rel) {
  const file = path.resolve(root, "." + path.posix.normalize("/" + rel));
  if (file !== root && !file.startsWith(root + path.sep)) return null;
  try {
    return (await stat(file)).isFile() ? file : null;
  } catch {
    return null;
  }
}

// Single range only; null = whole file, false = unsatisfiable.
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

const body = (file, opts) => Readable.toWeb(createReadStream(file, opts));

async function sendFile(file, request) {
  const { size } = await stat(file);
  const headers = { "content-type": mimeOf(file), "accept-ranges": "bytes" };
  const range = parseRange(request.headers.get("range"), size);
  if (range === false)
    return new Response(null, { status: 416, headers: { ...headers, "content-range": `bytes */${size}` } });
  if (range) {
    const { start, end } = range;
    return new Response(body(file, { start, end }), {
      status: 206,
      headers: { ...headers, "content-length": String(end - start + 1), "content-range": `bytes ${start}-${end}/${size}` },
    });
  }
  return new Response(size ? body(file) : null, { status: 200, headers: { ...headers, "content-length": String(size) } });
}

// Same name as app/server/media_cache.py cache_path (D-17).
export function cacheName(url) {
  let ext = "";
  try {
    ext = path.posix.extname(new URL(url).pathname).toLowerCase();
  } catch {}
  if (!/^\.[a-z0-9]{1,5}$/.test(ext)) ext = ".bin";
  return createHash("sha1").update(url, "utf8").digest("hex").slice(0, 16) + ext;
}

// Every picked file_url in the pool, like media_cache.pool_urls; stage-media.mjs ships the same set.
export const poolUrls = ({ questions }) =>
  new Set(questions.flatMap((q) => [q.media?.file_url, q.background?.file_url]).filter(Boolean));

// es pool files in data/: base's and every installed pack's (decision 66).
export async function poolFiles(data) {
  const packs = await readdir(path.join(data, "bundles")).catch(() => []);
  return [path.join(data, "pool.json"), ...packs.map((b) => path.join(data, "bundles", b, "pool.json"))];
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

export function makeResolver({ dist, data, media }) {
  dist = path.resolve(dist);
  data = path.resolve(data);
  media = path.resolve(media);
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
    if (rel.startsWith("/data/")) {
      const file = await contained(data, rel.slice("/data/".length));
      return file ? sendFile(file, request) : json(404, { error: "not_found" });
    }
    if (rel === "/media") {
      const fileUrl = url.searchParams.get("url") ?? "";
      if (!(await urls()).has(fileUrl)) return json(404, { error: "not_found" });
      const file = await contained(media, cacheName(fileUrl));
      return file ? sendFile(file, request) : json(404, { error: "media_missing" });
    }
    const file = rel !== "/" && (await contained(dist, rel));
    return sendFile(file || path.join(dist, "index.html"), request);
  };
}
