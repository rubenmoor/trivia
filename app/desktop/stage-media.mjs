// Pool media → build/media for a packaged build (plan 56): hard links (or copies) from the cache.
import { copyFileSync, linkSync, mkdirSync, readFileSync, rmSync, statSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { cacheName, poolUrls } from "./resolve.mjs";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const REPO = path.resolve(HERE, "..", "..");
const allowMissing = process.argv.includes("--allow-missing");
const cache = process.env.TRIVIA_MEDIA || path.join(REPO, "media");
const out = path.join(HERE, "build", "media");

const urls = poolUrls(JSON.parse(readFileSync(path.join(REPO, "app", "data", "pool.json"), "utf8")));
rmSync(out, { recursive: true, force: true });
mkdirSync(out, { recursive: true });

let count = 0;
let bytes = 0;
const missing = [];
for (const url of [...urls].sort()) {
  const name = cacheName(url);
  const src = path.join(cache, name);
  let size;
  try {
    size = statSync(src).size;
  } catch {
    missing.push(`  ${name}  ${url}`);
    continue;
  }
  try {
    linkSync(src, path.join(out, name));
  } catch {
    copyFileSync(src, path.join(out, name));
  }
  count++;
  bytes += size;
}

console.log(`stage-media: ${count} files, ${(bytes / 1e6).toFixed(0)} MB from ${cache} → ${out}`);
if (missing.length) {
  console.error(`stage-media: ${missing.length} missing in ${cache}:\n${missing.join("\n")}`);
  if (!allowMissing) {
    console.error("run `trivia-media sync --status approved`, or stage with `npm run stage-media -- --allow-missing` and run electron-builder by hand");
    process.exit(1);
  }
}
