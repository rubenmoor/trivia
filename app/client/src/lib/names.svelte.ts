// Category and subcategory names in the question locale, bundle names in the UI language, of the last engine call (plan 68, D-81).
import { catKey, subName } from "../engine/pool.ts";
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

/** The locale's name (bundles: the UI language's); fallback the Spanish name / categories.json / bundles.json name.
 * Keys: category and subcategory keys (catKey, subKey: bundle + slug or Spanish name, D-99), bundle id. */
export function displayName(kind: "category" | "subcategory" | "bundle", key: string): string {
  const d = data;
  if (!d) return key;
  if (kind === "subcategory") return d.names.subcategories[key] ?? subName(d.broad.get(key)?.bundle, key);
  if (kind === "category") return d.names.categories[key] ?? d.categories.find((c) => catKey(c) === key)?.name ?? key;
  return d.uiNames.bundles[key]?.name ?? d.bundles.find((b) => b.id === key)?.name ?? key;
}
