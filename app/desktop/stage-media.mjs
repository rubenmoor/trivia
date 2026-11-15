// Pool media → build/media for a packaged build (plan 56): encoded under shippedName (decision 185),
// hard links (or copies) from the encode cache work/ship-media/.
// build/pack-media.json: per shipped bundle folder, the media only it uses (its DLC depot carries them, decision 66; [] without a pool).
// build/data/: app/data/ without topic bundle pools until all five topics have 2000 approved per locale (decision 520).
// Audio and video sound is levelled to -18 LUFS after the cut (loudness.mjs).
// Excerpt questions (decision 644): the build's pools point at `<url>#t=start,end`, one cut file per window; the media is cut to it.
// --check: no encoding; build/media against the pools and media-budget.json, exit 1 on ✗.
// --demo (or TRIVIA_DEMO=1, as the dist:*:demo scripts set it; decision 342): only app/data/demo/ pools (all locales) → build/media-demo/,
// no packs, no pack-media.json; budget `demo.content`. Also build/data-demo/: app/data/ without bundles/ and the full pools, with demo/.
import { execFile, execFileSync } from "node:child_process";
import { createHash } from "node:crypto";
import { copyFileSync, cpSync, existsSync, linkSync, mkdirSync, readdirSync, readFileSync, renameSync, rmSync, statSync, writeFileSync } from "node:fs";
import { availableParallelism } from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { promisify } from "node:util";
import { filter, measure, TARGET_LUFS, TRUE_PEAK } from "./loudness.mjs";
import { VIDEO } from "./media-formats.mjs";
import { cacheName, excerptOf, poolUrls, shipPool, shippedName, sourceUrl } from "./resolve.mjs";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const REPO = path.resolve(HERE, "..", "..");
const allowMissing = process.argv.includes("--allow-missing");
const check = process.argv.includes("--check");
const demo = process.argv.includes("--demo") || process.env.TRIVIA_DEMO === "1";
const cache = process.env.TRIVIA_MEDIA || path.join(REPO, "media");
const out = path.join(HERE, "build", demo ? "media-demo" : "media");
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
const GIF = { widths: [1280, 960, 640], q: [60, 40, 25], max: 4 * MB };
const AUDIO = ["-vn", "-c:a", "libopus", "-b:a", "96k"];
const KIND = { ".webp": "image", ".opus": "audio", ".webm": "video" };
const LEVEL = `loudnorm ${TARGET_LUFS} ${TRUE_PEAK}`; // in the hash: a new target re-encodes
const settings = { image: JSON.stringify(IMAGE) + JSON.stringify(GIF), audio: JSON.stringify(AUDIO) + LEVEL, video: JSON.stringify(VIDEO) + LEVEL };

const ffmpeg = (src, args, dst) => run("ffmpeg", ["-nostdin", "-v", "error", "-y", "-i", src, ...args, "-map_metadata", "-1", dst]);

async function image(src, dst) {
  const { stdout } = await run("ffprobe", ["-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "json", src]);
  const { width: w, height: h } = JSON.parse(stdout).streams[0];
  const s = Math.min(1, IMAGE.box[0] / w, IMAGE.box[1] / h);
  const resize = s < 1 ? ["-resize", String(Math.round(w * s)), String(Math.round(h * s))] : [];
  let input = src;
  try {
    for (const q of IMAGE.q) {
      try {
        await run("cwebp", ["-quiet", "-q", String(q), ...IMAGE.args, ...resize, input, "-o", dst]);
      } catch (e) {
        if (input !== src) throw e;
        // CMYK or truncated JPEG: cwebp can't read it, ffmpeg decodes it (RGB, ICC dropped).
        input = `${dst}.png`;
        await ffmpeg(src, ["-frames:v", "1", "-vf", "sidedata=mode=delete:type=ICC_PROFILE", "-pix_fmt", "rgb24"], input);
        await run("cwebp", ["-quiet", "-q", String(q), ...IMAGE.args, ...resize, input, "-o", dst]);
      }
      if (statSync(dst).size <= MB) break;
    }
  } finally {
    if (input !== src) rmSync(input, { force: true });
  }
  return s < 1;
}

// Animated GIF → animated WebP (ffmpeg): width and quality step down until it fits GIF.max.
async function gif(src, dst) {
  for (const w of GIF.widths)
    for (const q of GIF.q) {
      await ffmpeg(src, ["-vf", `scale=min(${w}\\,iw):-2`, "-c:v", "libwebp_anim", "-lossless", "0", "-q:v", String(q), "-loop", "0", "-an"], dst);
      if (statSync(dst).size <= GIF.max) return true;
    }
  return true;
}

// → the encoded file in work/ship-media/ (new or cached) and whether it was encoded now.
async function encode(src, name, excerpt) {
  const ext = path.extname(name);
  const kind = KIND[ext];
  if (!kind) return { file: src, fresh: false };  // GIF, SVG: as is
  const { size, mtimeMs } = statSync(src);
  const hash = createHash("sha1").update(`${TOOLS}\n${settings[kind]}\n${size} ${mtimeMs}${excerpt ? ` ${excerpt.start}-${excerpt.end}` : ""}`).digest("hex").slice(0, 10);
  const file = path.join(encoded, `${name.slice(0, -ext.length)}-${hash}${ext}`);
  if (statSync(file, { throwIfNoEntry: false })) return { file, fresh: false };
  const tmp = `${file}.part${ext}`;
  let resized = false;
  let levelled = false;
  if (kind === "image") resized = path.extname(src).toLowerCase() === ".gif" ? await gif(src, tmp) : await image(src, tmp);
  else {
    const cut = excerpt ? ["-ss", String(excerpt.start), "-to", String(excerpt.end)] : [];
    const m = await measure(src, cut); // levelled after the cut; null: silent, left as is
    levelled = !!m;
    await ffmpeg(src, [...cut, ...(m ? ["-af", filter(m)] : []), ...(kind === "audio" ? AUDIO : VIDEO)], tmp);
  }
  // Same format, not shrunk or resized (nor cut or levelled): the source is the better file.
  if (!excerpt && !levelled && path.extname(src) === ext && !resized && statSync(tmp).size >= size) copyFileSync(src, tmp);
  renameSync(tmp, file);
  return { file, fresh: true };
}

const DATA = path.join(REPO, "app", "data");
// Topic bundles ship only when all five have TOPIC_BAR questions per locale (decision 520); pool.json = es.
const TOPIC_BAR = 2000;
const poolLocale = (f) => /^pool(?:\.([\w-]+))?\.json$/.exec(f)?.[1] ?? (f === "pool.json" ? "es" : null);
const topics = JSON.parse(readFileSync(path.join(DATA, "bundles.json"), "utf8")).bundles.filter((b) => b.kind === "theme").map((b) => b.id);
const topicCount = (b, f) => JSON.parse(readFileSync(path.join(DATA, "bundles", b, f), "utf8")).questions.filter((q) => q.status === "approved").length;
const atBar = (f) => topics.every((b) => existsSync(path.join(DATA, "bundles", b, f)) && topicCount(b, f) >= TOPIC_BAR);
const shipsPool = (b, f) => !topics.includes(b) || atBar(f);
const read = (file) => poolUrls(shipPool(JSON.parse(readFileSync(file, "utf8"))));
const urls = new Set();
const packMedia = {};
if (demo) {
  const dir = path.join(DATA, "demo");
  for (const f of readdirSync(dir).filter((f) => /^pool(\.[\w-]+)?\.json$/.test(f))) for (const u of read(path.join(dir, f))) urls.add(u);
} else {
  const packs = readdirSync(path.join(DATA, "bundles"))
    .filter((b) => statSync(path.join(DATA, "bundles", b), { throwIfNoEntry: false })?.isDirectory())
    .map((b) => [b, existsSync(path.join(DATA, "bundles", b, "pool.json")) && shipsPool(b, "pool.json") ? read(path.join(DATA, "bundles", b, "pool.json")) : new Set()]); // no pool yet: a pack without media
  for (const u of read(path.join(DATA, "pool.json"))) urls.add(u);
  const owners = new Map();
  for (const [b, own] of packs) for (const u of own) owners.set(u, urls.has(u) || owners.has(u) ? null : b);
  for (const [b] of packs) packMedia[b] = [];
  for (const [u, b] of [...owners].sort()) {
    urls.add(u);
    if (b) packMedia[b].push(shippedName(u));
  }
}

// Budgets in MB (media-budget.json): per depot, per file (videos `video`).
if (check) {
  const budget = JSON.parse(readFileSync(path.join(HERE, "media-budget.json"), "utf8"));
  const shipped = demo ? {} : JSON.parse(readFileSync(path.join(HERE, "build", "pack-media.json"), "utf8"));
  const size = new Map(readdirSync(out).map((f) => [f, statSync(path.join(out, f)).size]));
  const fails = [];
  const absent = [...urls].filter((u) => !size.has(shippedName(u))).sort();
  for (const u of absent) fails.push(`missing ${shippedName(u)}  ${u}`);
  const inPack = new Set(Object.values(shipped).flat());
  // No size line for the base content or the packs (decision 653); only the demo has one.
  const depots = [["content", [...size.keys()].filter((f) => !inPack.has(f)), demo ? budget.demo.content : null]];
  for (const [b, files] of Object.entries(shipped)) depots.push([`dlc ${b}`, files, null]);
  for (const [name, files, max] of depots) {
    const mb = files.reduce((n, f) => n + (size.get(f) ?? 0), 0) / MB;
    const over = max !== null && mb > max;
    console.log(`${over ? "✗" : "✓"} ${name}: ${files.length} files, ${mb.toFixed(0)} MB${max === null ? "" : ` of ${max} MB`}`);
    if (over) fails.push(`${name} over budget: ${mb.toFixed(0)} > ${max} MB`);
  }
  const horizonDir = path.join(REPO, "app", "client", "public", "horizon");
  const horizon = readdirSync(horizonDir).filter((f) => f.endsWith(".webp")).map((f) => [f, statSync(path.join(horizonDir, f)).size]);
  const horizonMb = horizon.reduce((n, [, b]) => n + b, 0) / MB;
  console.log(`${horizonMb > budget.horizon ? "✗" : "✓"} horizon: ${horizon.length} files, ${horizonMb.toFixed(1)} MB of ${budget.horizon} MB`);
  if (horizonMb > budget.horizon) fails.push(`horizon over budget: ${horizonMb.toFixed(1)} > ${budget.horizon} MB`);
  for (const [f, n] of horizon) if (n / MB > budget.file) fails.push(`horizon/${f} ${(n / MB).toFixed(1)} MB > ${budget.file} MB`);
  const audioDir = path.join(REPO, "app", "client", "public", "audio");
  const audio = readdirSync(audioDir).filter((f) => f.endsWith(".m4a"));
  const audioMb = audio.reduce((n, f) => n + statSync(path.join(audioDir, f)).size, 0) / MB;
  console.log(`${audioMb > budget.audio ? "✗" : "✓"} audio: ${audio.length} files, ${audioMb.toFixed(1)} MB of ${budget.audio} MB`);
  if (audioMb > budget.audio) fails.push(`audio over budget: ${audioMb.toFixed(1)} > ${budget.audio} MB`);
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
if (demo) {
  const data = path.join(HERE, "build", "data-demo");
  rmSync(data, { recursive: true, force: true });
  mkdirSync(path.join(data, "demo"), { recursive: true });
  for (const f of readdirSync(DATA, { withFileTypes: true }))
    if (f.isFile() && !/^pool(\.[\w-]+)?\.json$/.test(f.name)) copyFileSync(path.join(DATA, f.name), path.join(data, f.name));
  for (const f of readdirSync(path.join(DATA, "demo"))) copyFileSync(path.join(DATA, "demo", f), path.join(data, "demo", f));
}
if (!demo) {
  // build/data/: app/data/ without the topic pools below the bar (the build's data dir)
  const data = path.join(HERE, "build", "data");
  rmSync(data, { recursive: true, force: true });
  cpSync(DATA, data, {
    recursive: true,
    filter: (src) => {
      const rel = path.relative(DATA, src).split(path.sep);
      return !(rel[0] === "bundles" && rel.length === 3 && poolLocale(rel[2]) && !shipsPool(rel[1], rel[2]));
    },
  });
}
// The built pools: excerpts folded into file_url (shipPool).
const shipPools = (dir) => {
  for (const f of readdirSync(dir, { recursive: true }).filter((f) => /(^|[\\/])pool(\.[\w-]+)?\.json$/.test(f))) {
    const file = path.join(dir, f);
    const text = readFileSync(file, "utf8");
    if (text.includes('"excerpt"')) writeFileSync(file, JSON.stringify(shipPool(JSON.parse(text))) + "\n");
  }
};
shipPools(path.join(HERE, "build", demo ? "data-demo" : "data"));
mkdirSync(encoded, { recursive: true });
if (!demo) writeFileSync(path.join(HERE, "build", "pack-media.json"), JSON.stringify(packMedia, null, 2) + "\n");

const missing = [];
const jobs = [];
for (const url of [...urls].sort()) {
  const name = shippedName(url);
  const src = path.join(cache, cacheName(sourceUrl(url)));
  const st = statSync(src, { throwIfNoEntry: false });
  if (st) jobs.push({ name, src, before: st.size, excerpt: excerptOf(url) });
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
      const r = await encode(job.src, job.name, job.excerpt);
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

// Stale encodes, .part files; not in the demo, whose files are a subset of the full build's cache.
if (!demo) for (const f of readdirSync(encoded)) if (!kept.has(f)) rmSync(path.join(encoded, f));

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
