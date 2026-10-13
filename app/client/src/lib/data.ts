// The game data from /data/ (app/data/, served read-only by app/server/main.py; plan 50, PORT-7).
import { loadCategories, parseAgeGroups, parseBundles, parsePool } from "../engine/pool.ts";
import { engineData, NO_NAMES, type EngineData, type Names } from "../engine/state.ts";
import { call } from "./api.ts";

/** A data file's JSON; null on 404 if `optional`, else a readable Error. */
async function get(base: string, file: string, optional = false): Promise<unknown> {
  const res = await call(`${base}/data/${file}`);
  if (optional && res.status === 404) return null;
  if (!res.ok) throw new Error(`/data/${file}: HTTP ${res.status} — run \`qgen export\`?`);
  return res.json();
}

/** Question locales a pool may exist for (D-78); es always has one. */
export const LOCALES = ["es", "en", "de"] as const;

/** The pool file of a locale (D-81): es is pool.json. */
const poolFile = (locale: string) => (locale === "es" ? "pool.json" : `pool.${locale}.json`);

const cache = new Map<string, Promise<EngineData>>();

/** The engine data of `locale`, once per locale; a failure is retried on the next call. */
export function loadEngineData(base = "", locale = "es"): Promise<EngineData> {
  const key = `${base}|${locale}`;
  let out = cache.get(key);
  if (!out) {
    out = load(base, locale);
    out.catch(() => cache.delete(key));
    cache.set(key, out);
  }
  return out;
}

/** Locales of LOCALES whose pool file exists; the body isn't read. */
export async function availableLocales(base = ""): Promise<string[]> {
  const found = await Promise.all(LOCALES.map(async (l) => {
    if (l === "es") return true;
    const res = await call(`${base}/data/${poolFile(l)}`);
    await res.body?.cancel();
    return res.ok;
  }));
  return LOCALES.filter((_, i) => found[i]);
}

/** Base's names file merged with every bundle's; none (es) → empty. */
function mergeNames(files: unknown[]): Names {
  const out: Names = { bundles: {}, categories: {}, subcategories: {}, age_groups: {} };
  for (const f of files as (Partial<Names> | null)[]) {
    if (!f) continue;
    Object.assign(out.bundles, f.bundles);
    Object.assign(out.categories, f.categories);
    Object.assign(out.subcategories, f.subcategories);
    Object.assign(out.age_groups, f.age_groups);
  }
  return out;
}

/** The locale's pool, bundles.json, age-groups.json, every bundle's categories file and names files → engineData.
 * A bundle without a categories file has none (categories.load()). */
async function load(base: string, locale: string): Promise<EngineData> {
  const [pool, bundles, ageGroups] = await Promise.all(
    [poolFile(locale), "bundles.json", "age-groups.json"].map((f) => get(base, f)),
  );
  const parsed = parseBundles(bundles);
  const files = await Promise.all(
    parsed.map((b) => get(base, b.id === "base" ? "categories.json" : `bundles/${b.id}/categories.json`, true)),
  );
  const names = locale === "es" ? NO_NAMES : mergeNames(await Promise.all(
    parsed.map((b) => get(base, b.id === "base" ? `names.${locale}.json` : `bundles/${b.id}/names.${locale}.json`, true)),
  ));
  const byBundle = Object.fromEntries(parsed.flatMap((b, i) => (files[i] ? [[b.id, files[i]]] : [])));
  return engineData(parsePool(pool), loadCategories(bundles, byBundle), parsed, parseAgeGroups(ageGroups), locale, names);
}
