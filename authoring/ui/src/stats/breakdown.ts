// Approved questions per broad category and subcategory (D-19), shared by the stats pages
// and the start page.
import { catKey, subKey } from "$app/engine/pool.ts";
import type { Category, Names, Question } from "../lib/types.ts";

interface SubRow {
  /** Its key (decision 259). */
  name: string;
  bundle: string;
  /** The locale's name (names.<locale>.json), else the key. */
  label: string;
  count: number;
}

export interface CategoryRow {
  /** Its key, as catKey (unique across bundles). */
  name: string;
  label: string;
  count: number;
  /** In app/data/categories.json order. */
  subs: SubRow[];
}

/** One row per category in app/data/categories.json order, plus one for unknown subcategories;
 * labels from `names` (plan 67, decision 259), with the bundle when a label repeats across bundles (D-99).
 * With `scope` (bundle ids in view), other bundles' subcategories only when they have questions. */
export function breakdown(
  questions: Question[],
  categories: Category[],
  names: Names | null = null,
  scope: Set<string> | null = null,
): CategoryRow[] {
  const perSub = new Map<string, { bundle: string; name: string; count: number }>();
  for (const q of questions) {
    const k = subKey(q.bundle, q.subcategory);
    const row = perSub.get(k) ?? { bundle: q.bundle, name: q.subcategory, count: 0 };
    perSub.set(k, { ...row, count: row.count + 1 });
  }
  const known = new Set(categories.flatMap((c) => c.subcategories.map((s) => subKey(c.bundle, s))));
  const repeated = (all: string[]) => new Set(all.filter((x, i) => all.indexOf(x) !== i));
  const subLabel = (c: Category, s: string) => names?.subcategories[subKey(c.bundle, s)] ?? s;
  const catLabel = (c: Category) => names?.categories[catKey(c)] ?? c.name ?? c.slug;
  const subLabels = repeated(categories.flatMap((c) => c.subcategories.map((s) => subLabel(c, s))));
  const catLabels = repeated(categories.map(catLabel));
  const tag = (label: string, bundle: string, dup: Set<string>) => (dup.has(label) ? `${label} (${bundle})` : label);
  const out: CategoryRow[] = categories.flatMap((c) => {
    const all = c.subcategories.map((s) => {
      const k = subKey(c.bundle, s);
      return { name: s, bundle: c.bundle, label: tag(subLabel(c, s), c.bundle, subLabels), count: perSub.get(k)?.count ?? 0 };
    });
    const subs = !scope || scope.has(c.bundle) ? all : all.filter((s) => s.count);
    if (!subs.length) return [];
    return [{ name: catKey(c), label: tag(catLabel(c), c.bundle, catLabels), count: subs.reduce((n, s) => n + s.count, 0), subs }];
  });
  const unknown = [...perSub].filter(([k]) => !known.has(k))
    .map(([, { bundle, name, count }]) => ({ name, bundle, label: bundle === "base" ? name : `${name} (${bundle})`, count }));
  if (unknown.length) {
    const name = "(not in categories.json)";
    out.push({ name, label: name, count: unknown.reduce((n, s) => n + s.count, 0), subs: unknown });
  }
  return out;
}

/** Review queue of a bundle's subcategory's approved questions (RV-13 filters), in a locale's view if given. */
export function reviewLink(s: { name: string; bundle: string }, locale: string | null = null): string {
  return `/review?${new URLSearchParams({ bundle: s.bundle, subcategory: s.name, status: "approved", ...(locale ? { locale } : {}) })}`;
}

/** Fewer approved questions than a game asks (12): the category can't cover every level even once (RV-20). */
export const SPARSE_CATEGORY = 12;
/** Fewer than this: one player sees the whole subcategory in a game or two (RV-20). */
export const SPARSE_SUBCATEGORY = 3;
