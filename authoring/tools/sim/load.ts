// app/data/ → EngineData for Node entry points (plan 62; plan 51's supply check may reuse it).
import { existsSync, readFileSync } from "node:fs";
import { join } from "node:path";
import { bundleFile, loadCategories, baseListsLocale, packsFor, parseAgeGroups, parseBundles, parsePool, poolFile, withPacks } from "../../../app/client/src/engine/pool.ts";
import { engineData, type EngineData } from "../../../app/client/src/engine/state.ts";

const DATA_DIR = join(import.meta.dirname, "../../../app/data");

export type Loaded = { ok: true; data: EngineData; pool: string } | { ok: false; error: "no_pool"; pool: string };

const read = (path: string): unknown => JSON.parse(readFileSync(path, "utf8"));

/** Pool of `locale` with its packs' (as lib/data.ts), categories of every bundle, bundles, age groups; a missing pool → no_pool. */
export function loadData(locale: string, dir = DATA_DIR): Loaded {
  const pool = join(dir, poolFile(locale));
  const bundlesJson = read(join(dir, "bundles.json"));
  const packFiles = packsFor(parseBundles(bundlesJson), locale).map((b) => {
    const f = join(dir, poolFile(locale, b.id));
    return [b.id, existsSync(f) ? read(f) : null];
  });
  // base's pool may be missing where base doesn't list the locale (zh: chinese-base's pack alone)
  const hasBase = existsSync(pool);
  if (!hasBase && (baseListsLocale(parseBundles(bundlesJson), locale) || !packFiles.some(([, f]) => f))) return { ok: false, error: "no_pool", pool };
  const { pool: questions, bundles } = withPacks(hasBase ? parsePool(read(pool)) : [], parseBundles(bundlesJson), locale, Object.fromEntries(packFiles));
  const files: Record<string, unknown> = {};
  for (const b of bundles) {
    const f = join(dir, bundleFile(b.id, "categories.json"));
    if (existsSync(f)) files[b.id] = read(f);
  }
  const data = engineData(questions, loadCategories(bundlesJson, files), bundles,
    parseAgeGroups(read(join(dir, "age-groups.json"))), locale);
  return { ok: true, data, pool };
}
