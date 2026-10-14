// Pool media → build/media for a packaged build (plan 56): hard links (or copies) from the cache.
// build/pack-media.json: per pack, the media only it uses (its DLC depot carries them, decision 66).
import { copyFileSync, linkSync, mkdirSync, readdirSync, readFileSync, rmSync, statSync, writeFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { cacheName, poolUrls } from "./resolve.mjs";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const REPO = path.resolve(HERE, "..", "..");
const allowMissing = process.argv.includes("--allow-missing");
const cache = process.env.TRIVIA_MEDIA || path.join(REPO, "media");
const out = path.join(HERE, "build", "media");

// Raw files until encoded (task 1054): = shippedName only where the extension stays.
const staged = cacheName;

const DATA = path.join(REPO, "app", "data");
const read = (file) => poolUrls(JSON.parse(readFileSync(file, "utf8")));
const packs = readdirSync(path.join(DATA, "bundles"))
  .filter((b) => statSync(path.join(DATA, "bundles", b, "pool.json"), { throwIfNoEntry: false }))
  .map((b) => [b, read(path.join(DATA, "bundles", b, "pool.json"))]);
const urls = read(path.join(DATA, "pool.json"));
const owners = new Map();
for (const [b, own] of packs) for (const u of own) owners.set(u, urls.has(u) || owners.has(u) ? null : b);
const packMedia = Object.fromEntries(packs.map(([b]) => [b, []]));
for (const [u, b] of [...owners].sort()) {
  urls.add(u);
  if (b) packMedia[b].push(staged(u));
}
rmSync(out, { recursive: true, force: true });
mkdirSync(out, { recursive: true });
writeFileSync(path.join(HERE, "build", "pack-media.json"), JSON.stringify(packMedia, null, 2) + "\n");

let count = 0;
let bytes = 0;
const missing = [];
for (const url of [...urls].sort()) {
  const name = staged(url);
  const src = path.join(cache, cacheName(url));
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
