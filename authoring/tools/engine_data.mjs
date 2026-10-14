// The engine's data for a question locale, from app/data/ on disk (data.ts's load()): store screenshots, trivia-gallery.
import { existsSync, readFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { bundleFile, loadCategories, packsFor, parseAgeGroups, parseBundles, parsePool, poolFile, withPacks } from "../../app/client/src/engine/pool.ts";
import { engineData, mergeNames } from "../../app/client/src/engine/state.ts";

const DATA = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..", "..", "app", "data");
const json = (file) => JSON.parse(readFileSync(path.join(DATA, file), "utf8"));

/** Null if the locale has no pool. */
export function loadData(locale) {
  const file = poolFile(locale);
  if (!existsSync(path.join(DATA, file))) return null;
  const bundles = json("bundles.json");
  const optional = (f) => (existsSync(path.join(DATA, f)) ? json(f) : null);
  const all = parseBundles(bundles);
  const packs = Object.fromEntries(packsFor(all, locale).map((b) => [b.id, optional(poolFile(locale, b.id))]));
  const { pool, bundles: parsed } = withPacks(parsePool(json(file)), all, locale, packs);
  const byBundle = {};
  for (const b of parsed) {
    const cats = optional(bundleFile(b.id, "categories.json"));
    if (cats) byBundle[b.id] = cats;
  }
  return engineData(
    pool, loadCategories(bundles, byBundle), parsed, parseAgeGroups(json("age-groups.json")), locale,
    locale === "es" ? undefined : mergeNames(parsed.map((b) => optional(bundleFile(b.id, `names.${locale}.json`)))),
  );
}
