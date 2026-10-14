// Pool media → build/media for a packaged build (plan 56): encoded under shippedName (decision 185),
// hard links (or copies) from the encode cache work/ship-media/.
// build/pack-media.json: per pack, the media only it uses (its DLC depot carries them, decision 66).
// --check: no encoding; build/media against the pools and media-budget.json, exit 1 on ✗.
import { execFile, execFileSync } from "node:child_process";
import { createHash } from "node:crypto";
import { copyFileSync, linkSync, mkdirSync, readdirSync, readFileSync, renameSync, rmSync, statSync, writeFileSync } from "node:fs";
import { availableParallelism } from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { promisify } from "node:util";
import { cacheName, poolUrls, shippedName } from "./resolve.mjs";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const REPO = path.resolve(HERE, "..", "..");
const allowMissing = process.argv.includes("--allow-missing");
const check = process.argv.includes("--check");
const cache = process.env.TRIVIA_MEDIA || path.join(REPO, "media");
const out = path.join(HERE, "build", "media");
const encoded = path.join(process.env.TRIVIA_WORK || path.join(REPO, "work"), "ship-media");
const run = promisify(execFile);
const MB = 1e6;

const version = (cmd, arg) => {
  try {
    return execFileSync(cmd, [arg], { encoding: "utf8" }).split("\n")[0];
  } catch {
    console.error(`stage-media: ${cmd} not found; run \`trivia-desktop-build\` (it brings ffmpeg and cwebp)`);
    process.exit(1);
  }
};
const TOOLS = check ? "" : `${version("ffmpeg", "-version")} | cwebp ${version("cwebp", "-version")}`;

// Formats (decision 185); `args` and the version line make the settings hash.
const IMAGE = { box: [3840, 2160], q: [82, 76, 70, 64, 60], args: ["-m", "6", "-metadata", "icc"] };
const AUDIO = ["-vn", "-c:a", "libopus", "-b:a", "96k"];
const VIDEO = [
  ...["-map", "0:v:0", "-map", "0:a:0?"],
  ...["-vf", "scale=w=min(1920\\,iw):h=min(1080\\,ih):force_original_aspect_ratio=decrease:force_divisible_by=2"],
  ...["-c:v", "libvpx-vp9", "-crf", "33", "-b:v", "0", "-row-mt", "1", "-deadline", "good", "-cpu-used", "2"],
  ...["-c:a", "libopus", "-b:a", "96k"],
];
const KIND = { ".webp": "image", ".opus": "audio", ".webm": "video" };
const settings = { image: JSON.stringify(IMAGE), audio: JSON.stringify(AUDIO), video: JSON.stringify(VIDEO) };

const ffmpeg = (src, args, dst) => run("ffmpeg", ["-nostdin", "-v", "error", "-y", "-i", src, ...args, "-map_metadata", "-1", dst]);

async function image(src, dst) {
  const { stdout } = await run("ffprobe", ["-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "json", src]);
  const { width: w, height: h } = JSON.parse(stdout).streams[0];
  const s = Math.min(1, IMAGE.box[0] / w, IMAGE.box[1] / h);
  const resize = s < 1 ? ["-resize", String(Math.round(w * s)), String(Math.round(h * s))] : [];
  for (const q of IMAGE.q) {
    await run("cwebp", ["-quiet", "-q", String(q), ...IMAGE.args, ...resize, src, "-o", dst]);
    if (statSync(dst).size <= MB) break;
  }
  return s < 1;
}

// → the encoded file in work/ship-media/ (new or cached) and whether it was encoded now.
async function encode(src, name) {
  const ext = path.extname(name);
  const kind = KIND[ext];
  if (!kind) return { file: src, fresh: false };  // GIF, SVG: as is
  const { size, mtimeMs } = statSync(src);
  const hash = createHash("sha1").update(`${TOOLS}\n${settings[kind]}\n${size} ${mtimeMs}`).digest("hex").slice(0, 10);
  const file = path.join(encoded, `${name.slice(0, -ext.length)}-${hash}${ext}`);
  if (statSync(file, { throwIfNoEntry: false })) return { file, fresh: false };
  const tmp = `${file}.part${ext}`;
  let resized = false;
  if (kind === "image") resized = await image(src, tmp);
  else await ffmpeg(src, kind === "audio" ? AUDIO : VIDEO, tmp);
  // Same format, not shrunk or resized: the source is the better file.
  if (path.extname(src) === ext && !resized && statSync(tmp).size >= size) copyFileSync(src, tmp);
  renameSync(tmp, file);
  return { file, fresh: true };
}

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
  if (b) packMedia[b].push(shippedName(u));
}

// Budgets in MB (media-budget.json): per depot, per file (videos `video`).
if (check) {
  const budget = JSON.parse(readFileSync(path.join(HERE, "media-budget.json"), "utf8"));
  const shipped = JSON.parse(readFileSync(path.join(HERE, "build", "pack-media.json"), "utf8"));
  const size = new Map(readdirSync(out).map((f) => [f, statSync(path.join(out, f)).size]));
  const fails = [];
  const absent = [...urls].filter((u) => !size.has(shippedName(u))).sort();
  for (const u of absent) fails.push(`missing ${shippedName(u)}  ${u}`);
  const inPack = new Set(Object.values(shipped).flat());
  const depots = [["content", [...size.keys()].filter((f) => !inPack.has(f)), budget.content]];
  for (const [b, files] of Object.entries(shipped)) depots.push([`dlc ${b}`, files, budget.dlc[b] ?? budget.default_dlc]);
  for (const [name, files, max] of depots) {
    const mb = files.reduce((n, f) => n + (size.get(f) ?? 0), 0) / MB;
    const over = mb > max;
    console.log(`${over ? "✗" : "✓"} ${name}: ${files.length} files, ${mb.toFixed(0)} MB of ${max} MB`);
    if (over) fails.push(`${name} over budget: ${mb.toFixed(0)} > ${max} MB`);
  }
  const big = [...size].filter(([, n]) => n > MB).sort((a, b) => b[1] - a[1]);
  for (const [f, n] of big) {
    const max = KIND[path.extname(f)] === "video" ? budget.video : budget.file;
    if (n / MB > max) fails.push(`${f} ${(n / MB).toFixed(1)} MB > ${max} MB`);
  }
  console.log(`${big.length} files > 1 MB:`);
  for (const [f, n] of big) console.log(`  ${(n / MB).toFixed(1)} MB  ${f}`);
  for (const f of fails) console.error(`✗ ${f}`);
  console.log(`stage-media --check: ${fails.length ? `✗ ${fails.length} failure(s)` : "✓"} (${out})`);
  process.exit(fails.length ? 1 : 0);
}
rmSync(out, { recursive: true, force: true });
mkdirSync(out, { recursive: true });
mkdirSync(encoded, { recursive: true });
writeFileSync(path.join(HERE, "build", "pack-media.json"), JSON.stringify(packMedia, null, 2) + "\n");

const missing = [];
const jobs = [];
for (const url of [...urls].sort()) {
  const name = shippedName(url);
  const src = path.join(cache, cacheName(url));
  const st = statSync(src, { throwIfNoEntry: false });
  if (st) jobs.push({ name, src, before: st.size });
  else missing.push(`  ${name}  ${url}`);
}
jobs.sort((a, b) => b.before - a.before);  // videos first: the longest encodes

let fresh = 0;
let next = 0;
let done = 0;
const failed = [];
const kept = new Set();
async function worker() {
  for (let job = jobs[next++]; job; job = jobs[next++]) {
    try {
      const r = await encode(job.src, job.name);
      if (r.fresh) fresh++;
      kept.add(path.basename(r.file));
      try {
        linkSync(r.file, path.join(out, job.name));
      } catch {
        copyFileSync(r.file, path.join(out, job.name));
      }
      job.after = statSync(r.file).size;
      if (++done % 100 === 0) console.log(`stage-media: ${done}/${jobs.length}`);
    } catch (e) {
      failed.push(`  ${job.name}  ${job.src}: ${String(e.stderr || e.message).trim()}`);
    }
  }
}
await Promise.all(Array.from({ length: availableParallelism() }, worker));

for (const f of readdirSync(encoded)) if (!kept.has(f)) rmSync(path.join(encoded, f));  // stale encodes, .part files

const ok = jobs.filter((j) => j.after !== undefined);
const sum = (k) => (ok.reduce((n, j) => n + j[k], 0) / MB).toFixed(0);
const big = ok.filter((j) => j.after > MB).sort((a, b) => b.after - a.after);
console.log(
  `stage-media: ${ok.length} files (${fresh} encoded now), ${sum("before")} → ${sum("after")} MB, ${big.length} still > 1 MB; ${cache} → ${out}`,
);
for (const j of big) console.log(`  ${(j.after / MB).toFixed(1)} MB  ${j.name}`);
if (failed.length) {
  console.error(`stage-media: ${failed.length} failed to encode:\n${failed.join("\n")}`);
  process.exit(1);
}
if (missing.length) {
  console.error(`stage-media: ${missing.length} missing in ${cache}:\n${missing.join("\n")}`);
  if (!allowMissing) {
    console.error("run `trivia-media sync --status approved`, or stage with `npm run stage-media -- --allow-missing` and run electron-builder by hand");
    process.exit(1);
  }
}
