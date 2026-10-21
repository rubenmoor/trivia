// Category and subcategory names in the question locale, bundle names in the UI language, of the last engine call (plan 68, D-81).
import { catKey, categoryOf, subName, subOf } from "../engine/pool.ts";
import type { BundleMark } from "../game/BundleMark.svelte";
import type { EngineData } from "../engine/state.ts";

let data = $state.raw<EngineData | null>(null);

/** engine.ts: the data an action ran on. */
export function useNames(d: EngineData): void {
  if (d !== data) data = d;
}

/** `lang` of question content (task 629): the game's question locale, not the UI's. */
export function questionLocale(): string {
  return data?.locale ?? "es";
}

/** The export hash of that pool (D-92). */
export function poolHash(): string | null {
  return data?.poolHash ?? null;
}

/** The locale's name (bundles: the UI language's), es's for es-ES; fallback categories.json's `name` / bundles.json name
 * / the key (a plain-string key is its name: old format, mods; decision 259). Keys: catKey, subKey, bundle id. */
export function displayName(kind: "category" | "subcategory" | "bundle", key: string): string {
  const d = data;
  if (!d) return key;
  if (kind === "subcategory") return d.names.subcategories[key] ?? subName(d.broad.get(key)?.bundle, key);
  if (kind === "category") return d.names.categories[key] ?? d.categories.find((c) => catKey(c) === key)?.name ?? key;
  return d.uiNames.bundles[key]?.name ?? d.bundles.find((b) => b.id === key)?.name ?? key;
}

/** The category and subcategory keys of a question of the pool, or null (a mod without them, no data); `bundle`: its
 * bundle's mark, null for a base question. */
export function topicOf(id: string): { category: string; subcategory: string | null; bundle: BundleMark | null } | null {
  const q = data?.byId.get(id);
  if (!q) return null;
  const category = categoryOf(data!.broad)(q);
  if (!category) return null;
  const b = data!.bundles.find((x) => x.id === q.bundle);
  const bundle = !b || b.kind === "base" ? null : { base: false, region: b.kind === "region", country: b.country, icon: b.icon, source: b.source };
  return { category, subcategory: subOf(q), bundle };
}
