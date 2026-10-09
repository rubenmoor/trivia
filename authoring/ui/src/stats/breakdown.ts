// Approved questions per broad category and subcategory (D-19), shared by the stats pages
// and the start page.
import type { Category, Question } from "../lib/types";

export interface SubRow {
  name: string;
  count: number;
}

export interface CategoryRow {
  name: string;
  count: number;
  /** In app/data/categories.json order. */
  subs: SubRow[];
}

/** One row per category in app/data/categories.json order, plus one for unknown subcategories. */
export function breakdown(questions: Question[], categories: Category[]): CategoryRow[] {
  const perSub = new Map<string, number>();
  for (const q of questions) perSub.set(q.subcategory, (perSub.get(q.subcategory) ?? 0) + 1);
  const known = new Set(categories.flatMap((c) => c.subcategories));
  const out: CategoryRow[] = categories.map((c) => {
    const subs = c.subcategories.map((s) => ({ name: s, count: perSub.get(s) ?? 0 }));
    return { name: c.name, count: subs.reduce((n, s) => n + s.count, 0), subs };
  });
  const unknown = [...perSub].filter(([s]) => !known.has(s)).map(([name, count]) => ({ name, count }));
  if (unknown.length) {
    out.push({ name: "(not in categories.json)", count: unknown.reduce((n, s) => n + s.count, 0), subs: unknown });
  }
  return out;
}

/** Review queue of a subcategory's approved questions (RV-13 filters). */
export function reviewLink(subcategory: string): string {
  return `/review?${new URLSearchParams({ subcategory, status: "approved" })}`;
}
