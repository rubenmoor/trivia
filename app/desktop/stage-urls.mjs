// Which media URLs a build ships (stage-media.mjs): `urls` in the content depot, `packMedia` per DLC pack (only its own),
// `baseMedia` per `kind: base` pack (content depot too, decision 753).
import { existsSync, readdirSync, readFileSync, statSync } from "node:fs";
import path from "node:path";
import { poolUrls, shipPool, shippedName } from "./resolve.mjs";

// Topic bundles ship only when all five have TOPIC_BAR questions per locale (decision 520); pool.json = es.
const TOPIC_BAR = 2000;
export const poolLocale = (f) => /^pool(?:\.([\w-]+))?\.json$/.exec(f)?.[1] ?? (f === "pool.json" ? "es" : null);

export function stageUrls(DATA, demo = false) {
  const kinds = JSON.parse(readFileSync(path.join(DATA, "bundles.json"), "utf8")).bundles;
  const topics = kinds.filter((b) => b.kind === "theme").map((b) => b.id);
  const basePacks = new Set(kinds.filter((b) => b.kind === "base" && b.id !== "base").map((b) => b.id));
  const topicCount = (b, f) => JSON.parse(readFileSync(path.join(DATA, "bundles", b, f), "utf8")).questions.filter((q) => q.status === "approved").length;
  const atBar = (f) => topics.every((b) => existsSync(path.join(DATA, "bundles", b, f)) && topicCount(b, f) >= TOPIC_BAR);
  const shipsPool = (b, f) => !topics.includes(b) || atBar(f);
  const read = (file) => poolUrls(shipPool(JSON.parse(readFileSync(file, "utf8"))));
  const urls = new Set();
  const packMedia = {};
  const baseMedia = new Map(); // base pack id → its shipped names
  if (demo) {
    const dir = path.join(DATA, "demo");
    for (const f of readdirSync(dir).filter((f) => /^pool(\.[\w-]+)?\.json$/.test(f))) for (const u of read(path.join(dir, f))) urls.add(u);
    return { urls, packMedia, baseMedia, shipsPool };
  }
  const dirs = readdirSync(path.join(DATA, "bundles")).filter((b) => statSync(path.join(DATA, "bundles", b), { throwIfNoEntry: false })?.isDirectory());
  for (const b of dirs.filter((b) => basePacks.has(b))) {
    const own = new Set();
    for (const f of readdirSync(path.join(DATA, "bundles", b)).filter(poolLocale)) for (const u of read(path.join(DATA, "bundles", b, f))) own.add(u);
    for (const u of own) urls.add(u);
    baseMedia.set(b, [...own].map(shippedName));
  }
  const packs = dirs
    .filter((b) => !basePacks.has(b))
    .map((b) => [b, existsSync(path.join(DATA, "bundles", b, "pool.json")) && shipsPool(b, "pool.json") ? read(path.join(DATA, "bundles", b, "pool.json")) : new Set()]); // no pool yet: a pack without media
  for (const u of read(path.join(DATA, "pool.json"))) urls.add(u);
  const owners = new Map();
  for (const [b, own] of packs) for (const u of own) owners.set(u, urls.has(u) || owners.has(u) ? null : b);
  for (const [b] of packs) packMedia[b] = [];
  for (const [u, b] of [...owners].sort()) {
    urls.add(u);
    if (b) packMedia[b].push(shippedName(u));
  }
  return { urls, packMedia, baseMedia, shipsPool };
}
