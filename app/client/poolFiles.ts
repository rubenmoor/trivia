// Pool files whose media a full build ships and credits: es pools of base and the DLC packs (decision 66), and every
// pool of a `kind: base` pack (decision 753: content depot, no es pool needed). Same rule as app/desktop/stage-urls.mjs.
import { existsSync, readdirSync, readFileSync } from "node:fs";

export function poolFiles(dataDir: string): string[] {
  const { bundles } = JSON.parse(readFileSync(`${dataDir}bundles.json`, "utf8")) as { bundles: { id: string; kind: string }[] };
  const basePacks = new Set(bundles.filter((b) => b.kind === "base" && b.id !== "base").map((b) => b.id));
  const files = [`${dataDir}pool.json`];
  for (const b of readdirSync(`${dataDir}bundles`)) {
    const dir = `${dataDir}bundles/${b}/`;
    if (!existsSync(dir)) continue;
    if (basePacks.has(b)) files.push(...readdirSync(dir).filter((f) => /^pool(\.[\w-]+)?\.json$/.test(f)).sort().map((f) => dir + f));
    else if (existsSync(`${dir}pool.json`)) files.push(`${dir}pool.json`);
  }
  return files;
}
