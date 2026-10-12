// The game data from /data/ (app/data/, served read-only by app/server/main.py; plan 50, PORT-7).
import { loadCategories, parseAgeGroups, parseBundles, parsePool } from "../engine/pool.ts";
import { engineData, type EngineData } from "../engine/state.ts";
import { call } from "./api.ts";

/** A data file's JSON; null on 404 if `optional`, else a readable Error. */
async function get(base: string, file: string, optional = false): Promise<unknown> {
  const res = await call(`${base}/data/${file}`);
  if (optional && res.status === 404) return null;
  if (!res.ok) throw new Error(`/data/${file}: HTTP ${res.status} — run \`qgen export\`?`);
  return res.json();
}

/** pool.json, bundles.json, age-groups.json and every bundle's categories file → engineData.
 * A bundle without a categories file has none (categories.load()). */
export async function loadEngineData(base = ""): Promise<EngineData> {
  const [pool, bundles, ageGroups] = await Promise.all(
    ["pool.json", "bundles.json", "age-groups.json"].map((f) => get(base, f)),
  );
  const parsed = parseBundles(bundles);
  const files = await Promise.all(
    parsed.map((b) => get(base, b.id === "base" ? "categories.json" : `bundles/${b.id}/categories.json`, true)),
  );
  const byBundle = Object.fromEntries(parsed.flatMap((b, i) => (files[i] ? [[b.id, files[i]]] : [])));
  return engineData(parsePool(pool), loadCategories(bundles, byBundle), parsed, parseAgeGroups(ageGroups));
}
