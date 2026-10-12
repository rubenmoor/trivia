// app:// URL → file (plan 54). Web Request/Response only, so plain `node` can test it.
import { readFile, stat } from "node:fs/promises";
import path from "node:path";

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

export const mimeOf = (file) => MIME[path.extname(file).toLowerCase()] ?? "application/octet-stream";

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

async function sendFile(file) {
  return new Response(await readFile(file), { status: 200, headers: { "content-type": mimeOf(file) } });
}

export function makeResolver({ dist }) {
  dist = path.resolve(dist);
  return async (request) => {
    const url = new URL(request.url);
    let rel;
    try {
      rel = decodeURIComponent(url.pathname);
    } catch {
      return json(404, { error: "not_found" });
    }
    if (rel === "/api" || rel.startsWith("/api/")) return json(404, { error: "not_found" });
    const file = rel !== "/" && (await contained(dist, rel));
    return sendFile(file || path.join(dist, "index.html"));
  };
}
