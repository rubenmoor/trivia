// The engine's data for a question locale, from app/data/ on disk (data.ts's load()): store screenshots, trivia-gallery,
// the packaged smoke (a build's resources/data/).
import { existsSync, readFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { bundleFile, loadCategories, baseListsLocale, packsFor, parseAgeGroups, parseBundles, parsePool, poolFile, withPacks } from "../../app/client/src/engine/pool.ts";
import { engineData, mergeNames, namesFiles } from "../../app/client/src/engine/state.ts";

const DATA = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..", "..", "app", "data");

/** The pool locale of a UI tag: zh keeps its script (pool.zh-Hans.json), es-ES reads es. */
export const poolLocale = (ui) => (ui.startsWith("zh") ? ui : ui.split("-")[0]);

/** Null if the locale has no pool (base's, or a pack's where base doesn't list it); `dir`: another data directory of app/data's layout; `demo`: the demo's pool (demo/),
 * base only, no packs (data.ts's load() in a demo build). */
export function loadData(locale, dir = DATA, demo = false) {
  const json = (file) => JSON.parse(readFileSync(path.join(dir, file), "utf8"));
  const file = (demo ? "demo/" : "") + poolFile(locale);
  const bundles = json("bundles.json");
  const optional = (f) => (existsSync(path.join(dir, f)) ? json(f) : null);
  const all = parseBundles(bundles).filter((b) => !demo || b.id === "base");
  const packs = Object.fromEntries(packsFor(all, locale).map((b) => [b.id, optional(poolFile(locale, b.id))]));
  // base's pool may be missing where base doesn't list the locale (zh: chinese-base's pack alone)
  const basePool = optional(file);
  if (!basePool && (baseListsLocale(all, locale) || !Object.values(packs).some(Boolean))) return null;
  const { pool, bundles: parsed } = withPacks(basePool ? parsePool(basePool) : [], all, locale, packs);
  const byBundle = {};
  for (const b of parsed) {
    const cats = optional(bundleFile(b.id, "categories.json"));
    if (cats) byBundle[b.id] = cats;
  }
  return engineData(
    pool, loadCategories(bundles, byBundle), parsed, parseAgeGroups(json("age-groups.json")), locale,
    mergeNames(parsed.flatMap((b) => namesFiles(locale).map((n) => [b.id, optional(bundleFile(b.id, n))]))),
    null, demo,
  );
}
