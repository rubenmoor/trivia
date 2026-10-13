// Pool and category data (PORT-2): parsed JSON in, typed data out. Mirrors authoring/tools/categories.py.
import type { Background, Category, Media, Status } from "../lib/types.ts";

/** One entry of app/data/pool.json, with the answer (the client is the referee). */
export interface PoolQuestion {
  id: string;
  status: Status;
  difficulty: number;
  /** Always one of the categories' subcategories (qgen validate). */
  subcategory: string;
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

/** The pool's export hash (D-92); absent in old pools → null. */
export function poolHash(json: unknown): string | null {
  const hash = (json as { hash?: unknown } | null)?.hash;
  return typeof hash === "string" ? hash : null;
}

/** An entry of app/data/bundles.json (D-39); `kind: "base"` marks a base bundle (plan 71). */
export interface Bundle {
  id: string;
  kind: string;
  /** Question locales it's offered in. */
  languages: string[];
  name: string;
  description: string;
}

export function parseBundles(json: unknown): Bundle[] {
  const bundles = (json as { bundles?: unknown } | null)?.bundles;
  if (!Array.isArray(bundles) || bundles.length === 0) throw new Error("bundles.json: no bundles");
  return bundles.map(({ id, kind, languages, name, description }) => {
    if (typeof kind !== "string" || !kind) throw new Error(`bundles.json: ${id}: no kind`);
    if (!Array.isArray(languages) || languages.length === 0) throw new Error(`bundles.json: ${id}: no languages`);
    return { id, kind, languages, name, description };
  });
}

/** The bundles offered in `locale`, bundles.json order (plan 71). */
export function bundlesFor(data: { bundles: Bundle[]; locale: string }, locale = data.locale): Bundle[] {
  return data.bundles.filter((b) => b.languages.includes(locale));
}

/** [lo, hi] per level, index 0 = level 1. */
export type LevelRanges = readonly (readonly [number, number])[];

/** An age group of app/data/age-groups.json (D-38). */
export interface AgeGroup {
  id: string;
  name: string;
  ages: readonly [number, number | null];
  window: readonly [number, number];
  levels: LevelRanges;
  /** Difficulty → weight, derived from `levels` (D-76). */
  level_weights: Readonly<Record<string, number>>;
}

/** Weight per difficulty of the window: round(12 × Σ 1/(hi − lo + 1)) over the levels containing it (D-31, D-76). */
function levelWeights(window: readonly [number, number], levels: LevelRanges): Record<string, number> {
  const out: Record<string, number> = {};
  for (let d = window[0]; d <= window[1]; d++)
    out[d] = Math.round(12 * levels.reduce((s, [lo, hi]) => (lo <= d && d <= hi ? s + 1 / (hi - lo + 1) : s), 0));
  return out;
}

/** Throws unless every group has 12 levels inside its window and `level_weights` as they derive,
 * ids are unique and young_teens exists. */
export function parseAgeGroups(json: unknown): AgeGroup[] {
  const groups = (json as { groups?: unknown } | null)?.groups;
  if (!Array.isArray(groups)) throw new Error("age-groups.json: no groups");
  const out = groups.map(({ id, name, ages, window, levels, level_weights }): AgeGroup => {
    const [wlo, whi] = window ?? [];
    if (!Array.isArray(levels) || levels.length !== 12) throw new Error(`age-groups.json: ${id}: needs 12 levels`);
    levels.forEach((r: unknown, i: number) => {
      const ok = Array.isArray(r) && r.length === 2 && r.every(Number.isInteger) && wlo <= r[0] && r[0] <= r[1] && r[1] <= whi;
      if (!ok)
        throw new Error(`age-groups.json: ${id}: level ${i + 1} ${JSON.stringify(r)} not inside window ${wlo}–${whi}`);
    });
    const want = levelWeights(window, levels);
    if (JSON.stringify(level_weights) !== JSON.stringify(want))
      throw new Error(`age-groups.json: ${id}: level_weights must be ${JSON.stringify(want)}`);
    return { id, name, ages, window, levels, level_weights };
  });
  const ids = out.map((g) => g.id);
  if (new Set(ids).size !== ids.length) throw new Error("age-groups.json: duplicate group id");
  if (!ids.includes("young_teens")) throw new Error("age-groups.json: no young_teens");
  return out;
}

/** A bundle's own file in app/data/ (D-43): base's at the top, another's in bundles/<id>/. */
export const bundleFile = (bundle: string, name: string): string => (bundle === "base" ? name : `bundles/${bundle}/${name}`);

/** A bundle's pool file of a locale in app/data/ (D-81, decision 66): es is pool.json; a pack's in bundles/<id>/. */
export const poolFile = (locale: string, bundle = "base"): string =>
  bundleFile(bundle, locale === "es" ? "pool.json" : `pool.${locale}.json`);

/** Packs: the bundles besides base offered in `locale`, each with its own pool file (decision 66). */
export const packsFor = (bundles: Bundle[], locale: string): Bundle[] =>
  bundles.filter((b) => b.id !== "base" && b.languages.includes(locale));

/** base's pool plus the packs' pools of `locale` (packsFor order); a pack without a file (null) isn't
 * offered there: `locale` leaves its languages, so a stored choice naming it reads as the defaults. */
export function withPacks(
  pool: PoolQuestion[], bundles: Bundle[], locale: string, packs: Record<string, unknown>,
): { pool: PoolQuestion[]; bundles: Bundle[] } {
  return {
    pool: [...pool, ...packsFor(bundles, locale).flatMap((b) => (packs[b.id] ? parsePool(packs[b.id]) : []))],
    bundles: bundles.map((b) =>
      packsFor([b], locale).length && !packs[b.id] ? { ...b, languages: b.languages.filter((l) => l !== locale) } : b),
  };
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

/** question → broad category slug, or null. */
export function categoryOf(broad: Map<string, Category>): (q: { subcategory?: string | null }) => string | null {
  return (q) => (q.subcategory != null ? broad.get(q.subcategory)?.slug ?? null : null);
}

export function byId(pool: PoolQuestion[]): Map<string, PoolQuestion> {
  return new Map(pool.map((q) => [q.id, q]));
}
