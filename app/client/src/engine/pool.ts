// Pool and category data (PORT-2): parsed JSON in, typed data out. Mirrors app/server/categories.py.
import type { Background, Category, Media, Status } from "../lib/types.ts";

/** One entry of app/data/pool.json, with the answer (the client is the referee). */
export interface PoolQuestion {
  id: string;
  status: Status;
  difficulty: number;
  subcategory: string | null;
  bundle: string;
  description: string;
  question: string;
  answer: string;
  wrong_answers: string[];
  hints: string[];
  fun_fact: string;
  media: Media;
  background: Background | null;
}

export function parsePool(json: unknown): PoolQuestion[] {
  const doc = json as { version?: unknown; questions?: unknown } | null;
  if (doc?.version !== 1) throw new Error(`pool.json: unsupported version ${String(doc?.version)}`);
  if (!Array.isArray(doc.questions)) throw new Error("pool.json: no questions");
  return doc.questions as PoolQuestion[];
}

/** app/data/bundles.json and each bundle's categories file → categories in display order, base first.
 * A bundle without a file has none. */
export function loadCategories(bundlesJson: unknown, files: Record<string, unknown>): Category[] {
  const ids = (bundlesJson as { bundles: { id: string }[] }).bundles.map((b) => b.id);
  return ids.flatMap((bundle) => {
    const file = files[bundle] as { categories: Omit<Category, "bundle">[] } | undefined;
    return file ? file.categories.map((c) => ({ ...c, bundle })) : [];
  });
}

/** Subcategory names in display order, of one bundle or of all. */
export function subcategories(cats: Category[], bundle?: string): string[] {
  return cats.filter((c) => bundle === undefined || c.bundle === bundle).flatMap((c) => c.subcategories);
}

/** subcategory → its broad category, across all bundles. */
export function broadOf(cats: Category[]): Map<string, Category> {
  return new Map(cats.flatMap((c) => c.subcategories.map((s) => [s, c] as const)));
}

/** The bundle whose list has this subcategory, or null. */
export function bundleOf(cats: Category[], sub: string): string | null {
  return broadOf(cats).get(sub)?.bundle ?? null;
}

/** question → broad category slug, or null (game.category_of). */
export function categoryOf(broad: Map<string, Category>): (q: { subcategory?: string | null }) => string | null {
  return (q) => (q.subcategory != null ? broad.get(q.subcategory)?.slug ?? null : null);
}

export function byId(pool: PoolQuestion[]): Map<string, PoolQuestion> {
  return new Map(pool.map((q) => [q.id, q]));
}
