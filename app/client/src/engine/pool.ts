// Pool and category data (PORT-2): parsed JSON in, typed data out. Mirrors authoring/tools/categories.py.
import type { Background, Category, Media, Status } from "../lib/types.ts";

/** One entry of app/data/pool.json, with the answer (the client is the referee). */
export interface PoolQuestion {
  id: string;
  status: Status;
  difficulty: number;
  /** Always one of its bundle's subcategories (qgen validate); keyed with the bundle (subKey). */
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
  /** `kind: "region"` only, required there: ISO 3166-1 alpha-2 (plan 151); its flag is the bundle's icon. */
  country?: string;
  /** Question locales it's offered in. */
  languages: string[];
  name: string;
  description: string;
  /** A mod's row, merged in by the shell (decision 128); id `<mod>:<bundle>`. */
  source?: "mod";
  mod?: string;
  modName?: string;
}

/** Mod ids are `<mod>:<id>`; ':' is never in ours (decision 128). The one "not ours" test. */
export const isModId = (id: string): boolean => id.includes(":");
export const isOurs = (id: string): boolean => !isModId(id);

/** A regional bundle's `country` (plan 151); COUNTRY in authoring/tools/qgen.py, countryOk in app/desktop/mods.mjs. */
export const COUNTRY = /^[A-Z]{2}$/;

/** `country` present and well-formed exactly on a regional bundle. */
const countryOk = (kind: unknown, country: unknown): boolean =>
  kind === "region" ? typeof country === "string" && COUNTRY.test(country) : country === undefined;

/** Our rows throw when bad; a mod row with a bad `country` is skipped. */
export function parseBundles(json: unknown): Bundle[] {
  const bundles = (json as { bundles?: unknown } | null)?.bundles;
  if (!Array.isArray(bundles) || bundles.length === 0) throw new Error("bundles.json: no bundles");
  return bundles.flatMap(({ id, kind, country, languages, name, description, source, mod, modName }) => {
    if (typeof kind !== "string" || !kind) throw new Error(`bundles.json: ${id}: no kind`);
    if (!Array.isArray(languages) || (languages.length === 0 && source !== "mod")) throw new Error(`bundles.json: ${id}: no languages`);
    if (!countryOk(kind, country)) {
      if (source === "mod") return [];
      throw new Error(`bundles.json: ${id}: country`);
    }
    const c = country === undefined ? {} : { country };
    return [source === "mod" ? { id, kind, ...c, languages, name, description, source, mod, modName } : { id, kind, ...c, languages, name, description }];
  });
}

/** Why modPool drops a question; `bad_media` may drop only its media or background (decision 133). */
export type ModReason =
  | "bad_id" | "duplicate_id" | "no_text" | "wrong_answers" | "hints" | "difficulty" | "subcategory" | "status" | "bad_media";

/** A mod question's issue; `dropped`: the question is left out, else only its bad media. */
export interface ModIssue {
  id: string;
  reason: ModReason;
  dropped: boolean;
}

/** No media (a text-only mod question). */
const NO_MEDIA: Media = { type: "image", role: "decorative", source_url: null, file_url: null, credit: null };
const MOD_ID = /^[a-z0-9][a-z0-9-]{0,63}$/;
const str = (v: unknown): v is string => typeof v === "string" && v.trim() !== "";
const opt = (v: unknown): string | null => (typeof v === "string" ? v : null);
const three = (v: unknown): v is string[] => Array.isArray(v) && v.length === 3 && v.every(str);

/** A mod file_url → its URL under the bundle folder; null if not a plain relative path inside it. */
function modUrl(bundle: string, rel: unknown): string | null {
  if (!str(rel) || /^[a-z][a-z0-9+.-]*:|^[/\\]/i.test(rel) || rel.includes("\\")) return null;
  const parts = rel.split("/");
  if (parts.some((p) => p === "" || p === "." || p === "..")) return null;
  return `/data/bundles/${bundle}/${parts.map(encodeURIComponent).join("/")}`;
}

/** A mod bundle's pool (decision 128): ids → `<mod>:<id>`, `bundle` = the runtime id, media paths → its
 * folder, no media → NO_MEDIA; invalid questions dropped, bad media dropped (the question too if essential).
 * Issues per question for the mods screen and `--check-mod` (decision 133). `taken`: runtime ids already
 * used, gains this pool's. Throws on a bad pool file. Pure: also imported by the shell's check (Node). */
export function modPool(json: unknown, bundle: string, subcategories: Iterable<string>, taken = new Set<string>()): {
  questions: PoolQuestion[]; reasons: ModIssue[]; badQuestions: number; badMedia: number;
} {
  const mod = bundle.slice(0, bundle.indexOf(":"));
  const subs = new Set(subcategories);
  const questions: PoolQuestion[] = [];
  const reasons: ModIssue[] = [];
  const raw = parsePool(json);
  raw.forEach((one, i) => {
    const q = (one ?? {}) as unknown as Record<string, unknown>;
    const id = str(q.id) ? q.id : `#${i + 1}`;
    const bad = (reason: ModReason, dropped = true) => void reasons.push({ id, reason, dropped });
    const reason: ModReason | null =
      !str(q.id) || !MOD_ID.test(q.id) ? "bad_id"
      : taken.has(`${mod}:${id}`) ? "duplicate_id"
      : !str(q.question) || !str(q.answer) ? "no_text"
      : !three(q.wrong_answers) ? "wrong_answers"
      : !three(q.hints) ? "hints"
      : !Number.isInteger(q.difficulty) || (q.difficulty as number) < 1 || (q.difficulty as number) > 15 ? "difficulty"
      : !str(q.subcategory) || !subs.has(q.subcategory) ? "subcategory"
      : q.status !== undefined && q.status !== "approved" ? "status"
      : null;
    if (reason) return bad(reason);
    let media = NO_MEDIA;
    const m = q.media as Record<string, unknown> | null | undefined;
    if (m) {
      const url = modUrl(bundle, m.file_url);
      if (!url || !["image", "audio", "video"].includes(m.type as string)) {
        if (m.role === "essential") return bad("bad_media");
        bad("bad_media", false);
      } else {
        const role = ["decorative", "illustrative", "essential"].includes(m.role as string) ? m.role : "illustrative";
        media = { type: m.type, role, source_url: opt(m.source_url), file_url: url, credit: opt(m.credit) } as Media;
      }
    }
    let background: Background | null = null;
    const b = q.background as Record<string, unknown> | null | undefined;
    if (b) {
      const url = modUrl(bundle, b.file_url);
      if (url) background = { source_url: opt(b.source_url), file_url: url, credit: opt(b.credit) };
      else bad("bad_media", false);
    }
    taken.add(`${mod}:${id}`);
    questions.push({
      id: `${mod}:${id}`, status: "approved", difficulty: q.difficulty as number, subcategory: q.subcategory as string,
      bundle, description: opt(q.description) ?? "", question: q.question as string, answer: q.answer as string,
      wrong_answers: q.wrong_answers as string[], hints: q.hints as string[], fun_fact: opt(q.fun_fact) ?? "", media, background,
    });
  });
  const badMedia = reasons.filter((r) => r.reason === "bad_media").length;
  return { questions, reasons, badQuestions: raw.length - questions.length, badMedia };
}

/** A categories file's subcategories if well-formed (slugs, keys unique within it; `name` optional, decision 259), else null. */
export function modSubcategories(file: unknown): { slugs: string[]; subs: string[] } | null {
  const cats = (file as { categories?: unknown } | null)?.categories;
  if (!Array.isArray(cats) || !cats.length) return null;
  const ok = cats.every((c) => typeof c?.slug === "string" && c.slug && (c.name === undefined || typeof c.name === "string") && Array.isArray(c.subcategories)
    && c.subcategories.length && c.subcategories.every((s: unknown) => typeof s === "string" && s));
  if (!ok) return null;
  const slugs = cats.map((c) => c.slug as string);
  const subs = cats.flatMap((c) => c.subcategories as string[]);
  return new Set(slugs).size === slugs.length && new Set(subs).size === subs.length ? { slugs, subs } : null;
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

/** Key of a bundle's subcategory or category (decision 259: bundle + slug); base's is the bare slug. */
export const subKey = (bundle: string, key: string): string => (bundle === "base" ? key : `${bundle}/${key}`);
/** A question's subcategory key, or null. */
export const subOf = (q: { bundle?: string; subcategory?: string | null }): string | null =>
  (q.subcategory != null ? subKey(q.bundle ?? "base", q.subcategory) : null);
export const catKey = (c: Pick<Category, "bundle" | "slug">): string => subKey(c.bundle, c.slug);
/** The bundle's own key in a subKey (unknown bundle: the key); a plain-string key is its name (old format, mods). */
export const subName = (bundle: string | undefined, key: string): string =>
  (bundle && bundle !== "base" ? key.slice(bundle.length + 1) : key);

/** subcategory key → its broad category, across all bundles. */
export function broadOf(cats: Category[]): Map<string, Category> {
  return new Map(cats.flatMap((c) => c.subcategories.map((s) => [subKey(c.bundle, s), c] as const)));
}

/** question → broad category key, or null. */
export function categoryOf(broad: Map<string, Category>): (q: { bundle?: string; subcategory?: string | null }) => string | null {
  return (q) => {
    const c = broad.get(subOf(q) ?? "");
    return c ? catKey(c) : null;
  };
}

export function byId(pool: PoolQuestion[]): Map<string, PoolQuestion> {
  return new Map(pool.map((q) => [q.id, q]));
}
