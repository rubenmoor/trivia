// Approved questions per broad category and subcategory (D-19), shared by the stats pages
// and the start page.
import type { Category, Names, Question } from "../lib/types";

export interface SubRow {
  name: string;
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
 * labels from `names` (a translation locale, plan 67). */
export function breakdown(questions: Question[], categories: Category[], names: Names | null = null): CategoryRow[] {
  const perSub = new Map<string, number>();
  for (const q of questions) perSub.set(q.subcategory, (perSub.get(q.subcategory) ?? 0) + 1);
  const known = new Set(categories.flatMap((c) => c.subcategories));
  const out: CategoryRow[] = categories.map((c) => {
    const subs = c.subcategories.map((s) => ({ name: s, label: names?.subcategories[s] ?? s, count: perSub.get(s) ?? 0 }));
    return { name: c.name, label: names?.categories[c.slug] ?? c.name, count: subs.reduce((n, s) => n + s.count, 0), subs };
  });
  const unknown = [...perSub].filter(([s]) => !known.has(s)).map(([name, count]) => ({ name, label: name, count }));
  if (unknown.length) {
    const name = "(not in categories.json)";
    out.push({ name, label: name, count: unknown.reduce((n, s) => n + s.count, 0), subs: unknown });
  }
  return out;
}

/** Review queue of a subcategory's approved questions (RV-13 filters), in a locale's view if given. */
export function reviewLink(subcategory: string, locale: string | null = null): string {
  return `/review?${new URLSearchParams({ subcategory, status: "approved", ...(locale ? { locale } : {}) })}`;
}

/** Fewer approved questions than a game asks (12): the category can't cover every level even once (RV-20). */
export const SPARSE_CATEGORY = 12;
/** Fewer than this: one player sees the whole subcategory in a game or two (RV-20). */
export const SPARSE_SUBCATEGORY = 3;
