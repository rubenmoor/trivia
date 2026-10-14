// The game data from /data/ (app/data/, read-only: app/server/main.py or the desktop protocol; plan 50, PORT-7).
import {
  type Bundle, bundleFile, loadCategories, modPool, packsFor, parseAgeGroups, parseBundles, parsePool, poolFile, poolHash, withPacks,
} from "../engine/pool.ts";
import { engineData, mergeNames, NO_NAMES, type EngineData } from "../engine/state.ts";
import { call } from "./http.ts";
import { runDataHooks } from "./mods.ts";

/** A data file's JSON; null on 404 if `optional`, else a readable Error. */
async function get(file: string, optional = false): Promise<unknown> {
  const res = await call(`/data/${file}`);
  if (optional && res.status === 404) return null;
  if (!res.ok) throw new Error(`/data/${file}: HTTP ${res.status} — run \`qgen export\`?`);
  return res.json();
}

/** Question locales a pool may exist for (D-78); es always has one. */
export const LOCALES = ["es", "en", "de"] as const;

const cache = new Map<string, Promise<EngineData>>();

/** The engine data of `locale`, once per locale; a failure is retried on the next call. */
export function loadEngineData(locale = "es"): Promise<EngineData> {
  let out = cache.get(locale);
  if (!out) {
    out = load(locale);
    out.catch(() => cache.delete(locale));
    cache.set(locale, out);
  }
  return out;
}

/** Locales of LOCALES whose pool file exists; the body isn't read. */
export async function availableLocales(): Promise<string[]> {
  const found = await Promise.all(LOCALES.map(async (l) => {
    if (l === "es") return true;
    const res = await call(`/data/${poolFile(l)}`);
    await res.body?.cancel();
    return res.ok;
  }));
  return LOCALES.filter((_, i) => found[i]);
}

/** A problem with a mod bundle at load, for the mods screen (plan 115). */
export interface ModIssue {
  mod: string;
  bundle: string;
  code: "bad_question" | "bad_media" | "bad_categories" | "no_pool" | "bundle_language" | "taxonomy_clash";
  count: number;
}

const issues = new Map<string, ModIssue>();

/** The mod bundles' load issues so far, latest count per bundle and code. */
export function modIssues(): ModIssue[] {
  return [...issues.values()];
}

function issue(b: Bundle, code: ModIssue["code"], count = 1): void {
  if (count) issues.set(`${b.id} ${code}`, { mod: b.mod ?? "", bundle: b.id, code, count });
}

/** A mod bundle's file: its JSON, null if missing or unreadable. */
const modGet = (file: string): Promise<unknown> => get(file, true).catch(() => null);

/** A categories file's subcategories if well-formed (slugs, names, unique within it), else null. */
function modSubcategories(file: unknown): { slugs: string[]; subs: string[] } | null {
  const cats = (file as { categories?: unknown } | null)?.categories;
  if (!Array.isArray(cats) || !cats.length) return null;
  const ok = cats.every((c) => typeof c?.slug === "string" && c.slug && typeof c.name === "string" && Array.isArray(c.subcategories)
    && c.subcategories.length && c.subcategories.every((s: unknown) => typeof s === "string" && s));
  if (!ok) return null;
  const slugs = cats.map((c) => c.slug as string);
  const subs = cats.flatMap((c) => c.subcategories as string[]);
  return new Set(slugs).size === slugs.length && new Set(subs).size === subs.length ? { slugs, subs } : null;
}

/** The locale's pool and its packs' (decision 66), bundles.json, age-groups.json, every bundle's categories file
 * and names files → engineData. A bundle without a categories file has none (categories.load()); a pack
 * without a pool file isn't offered (withPacks). Mod bundles (decision 128) are packs checked by modPool;
 * a broken one is left out like a pack without a file, its issues in modIssues(). Then the mods' data hooks (plan 117). */
async function load(locale: string): Promise<EngineData> {
  const [pool, bundles, ageGroups] = await Promise.all(
    [poolFile(locale), "bundles.json", "age-groups.json"].map((f) => get(f)),
  );
  const all = parseBundles(bundles).map((b) => {
    if (b.source !== "mod") return b;
    const languages = b.languages.filter((l) => (LOCALES as readonly string[]).includes(l));
    issue(b, "bundle_language", b.languages.length - languages.length);
    return { ...b, languages };
  });
  const ours = all.filter((b) => b.source !== "mod");
  const mods = packsFor(all, locale).filter((b) => b.source === "mod");
  const [packFiles, files, modFiles] = await Promise.all([
    Promise.all(packsFor(ours, locale).map(async (b) => [b.id, await get(poolFile(locale, b.id), true)] as const)),
    Promise.all(ours.map((b) => get(bundleFile(b.id, "categories.json"), true))),
    Promise.all(mods.map((b) => Promise.all([modGet(poolFile(locale, b.id)), modGet(bundleFile(b.id, "categories.json"))]))),
  ]);
  const packs: Record<string, unknown> = Object.fromEntries(packFiles);
  const byBundle: Record<string, unknown> = Object.fromEntries(ours.flatMap((b, i) => (files[i] ? [[b.id, files[i]]] : [])));
  const cats = loadCategories(bundles, byBundle);
  const slugs = new Set(cats.map((c) => c.slug));
  const subs = new Set(cats.flatMap((c) => c.subcategories));
  const taken = new Set<string>();
  mods.forEach((b, i) => {
    const [json, catFile] = modFiles[i];
    packs[b.id] = null;
    const tax = modSubcategories(catFile);
    if (!tax) return issue(b, "bad_categories");
    // Until task 826 (bundle-scoped taxonomy): names must not repeat across bundles.
    if (tax.slugs.some((s) => slugs.has(s)) || tax.subs.some((s) => subs.has(s))) return issue(b, "taxonomy_clash");
    if (!json) return issue(b, "no_pool");
    let out;
    try {
      out = modPool(json, b.id, tax.subs, taken);
    } catch {
      return issue(b, "no_pool");
    }
    issue(b, "bad_question", out.badQuestions);
    issue(b, "bad_media", out.badMedia);
    if (!out.questions.length) return issue(b, "no_pool");
    packs[b.id] = { version: 1, questions: out.questions };
    byBundle[b.id] = catFile;
    tax.slugs.forEach((s) => slugs.add(s));
    tax.subs.forEach((s) => subs.add(s));
  });
  const packed = withPacks(parsePool(pool), all, locale, packs);
  const { questions, bundles: parsed, ageGroups: groups } = runDataHooks({
    locale, questions: packed.pool, bundles: packed.bundles, ageGroups: parseAgeGroups(ageGroups),
  });
  const names = locale === "es" ? NO_NAMES : mergeNames(await Promise.all(
    parsed.filter((b) => b.source !== "mod" || byBundle[b.id]).map((b) => {
      const file = bundleFile(b.id, `names.${locale}.json`);
      return b.source === "mod" ? modGet(file) : get(file, true);
    }),
  ));
  return engineData(questions, loadCategories(bundles, byBundle), parsed, groups, locale, names, poolHash(pool));
}
