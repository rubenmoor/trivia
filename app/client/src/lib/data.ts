// The game data from /data/ (app/data/, read-only: app/server/main.py or the desktop protocol; plan 50, PORT-7).
import { bundleFile, loadCategories, packsFor, parseAgeGroups, parseBundles, parsePool, poolFile, poolHash, withPacks } from "../engine/pool.ts";
import { engineData, mergeNames, NO_NAMES, type EngineData } from "../engine/state.ts";
import { call } from "./http.ts";

/** A data file's JSON; null on 404 if `optional`, else a readable Error. */
async function get(file: string, optional = false): Promise<unknown> {
  const res = await call(`/data/${file}`);
  if (optional && res.status === 404) return null;
  if (!res.ok) throw new Error(`/data/${file}: HTTP ${res.status} — run \`qgen export\`?`);
  return res.json();
}

/** Question locales a pool may exist for (D-78); es always has one. */
export const LOCALES = ["es", "en", "de"] as const;

const cache = new Map<string, Promise<EngineData>>();

/** The engine data of `locale`, once per locale; a failure is retried on the next call. */
export function loadEngineData(locale = "es"): Promise<EngineData> {
  let out = cache.get(locale);
  if (!out) {
    out = load(locale);
    out.catch(() => cache.delete(locale));
    cache.set(locale, out);
  }
  return out;
}

/** Locales of LOCALES whose pool file exists; the body isn't read. */
export async function availableLocales(): Promise<string[]> {
  const found = await Promise.all(LOCALES.map(async (l) => {
    if (l === "es") return true;
    const res = await call(`/data/${poolFile(l)}`);
    await res.body?.cancel();
    return res.ok;
  }));
  return LOCALES.filter((_, i) => found[i]);
}

/** The locale's pool and its packs' (decision 66), bundles.json, age-groups.json, every bundle's categories file
 * and names files → engineData. A bundle without a categories file has none (categories.load()); a pack
 * without a pool file isn't offered (withPacks). */
async function load(locale: string): Promise<EngineData> {
  const [pool, bundles, ageGroups] = await Promise.all(
    [poolFile(locale), "bundles.json", "age-groups.json"].map((f) => get(f)),
  );
  const all = parseBundles(bundles);
  const packFiles = await Promise.all(packsFor(all, locale).map(async (b) => [b.id, await get(poolFile(locale, b.id), true)]));
  const { pool: questions, bundles: parsed } = withPacks(parsePool(pool), all, locale, Object.fromEntries(packFiles));
  const files = await Promise.all(
    parsed.map((b) => get(bundleFile(b.id, "categories.json"), true)),
  );
  const names = locale === "es" ? NO_NAMES : mergeNames(await Promise.all(
    parsed.map((b) => get(bundleFile(b.id, `names.${locale}.json`), true)),
  ));
  const byBundle = Object.fromEntries(parsed.flatMap((b, i) => (files[i] ? [[b.id, files[i]]] : [])));
  return engineData(questions, loadCategories(bundles, byBundle), parsed, parseAgeGroups(ageGroups), locale, names, poolHash(pool));
}
