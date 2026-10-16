// Approved questions per broad category and subcategory (D-19), shared by the stats pages
// and the start page.
import { catKey, subKey } from "$app/engine/pool.ts";
import type { Category, Names, Question } from "../lib/types.ts";

interface SubRow {
  name: string;
  bundle: string;
  /** The locale's name (names.<locale>.json), else the Spanish name. */
  label: string;
  count: number;
}

export interface CategoryRow {
  name: string;
  label: string;
  count: number;
  /** In app/data/categories.json order. */
  subs: SubRow[];
}

/** One row per category in app/data/categories.json order, plus one for unknown subcategories;
 * labels from `names` (a translation locale, plan 67), with the bundle when a name repeats (D-99).
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
  const subNames = repeated(categories.flatMap((c) => c.subcategories));
  const catNames = repeated(categories.map((c) => c.name ?? c.slug));
  const tag = (label: string, name: string, bundle: string, dup: Set<string>) => (dup.has(name) ? `${label} (${bundle})` : label);
  const out: CategoryRow[] = categories.flatMap((c) => {
    const all = c.subcategories.map((s) => {
      const k = subKey(c.bundle, s);
      return { name: s, bundle: c.bundle, label: tag(names?.subcategories[k] ?? s, s, c.bundle, subNames), count: perSub.get(k)?.count ?? 0 };
    });
    const subs = !scope || scope.has(c.bundle) ? all : all.filter((s) => s.count);
    if (!subs.length) return [];
    const name = c.name ?? c.slug;
    const label = tag(names?.categories[catKey(c)] ?? name, name, c.bundle, catNames);
    return [{ name, label, count: subs.reduce((n, s) => n + s.count, 0), subs }];
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
