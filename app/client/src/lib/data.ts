// The game data from /data/ (app/data/, read-only: app/server/main.py or the desktop protocol; plan 50, PORT-7).
import {
  type Bundle, bundleFile, loadCategories, modPool, modSubcategories, packsFor, parseAgeGroups, parseBundles, parsePool, poolFile, poolHash, withPacks,
} from "../engine/pool.ts";
import type { OldKeys } from "../engine/save.ts";
import { engineData, mergeNames, namesFiles, type EngineData, type Names } from "../engine/state.ts";
import { buildInfo } from "./build.ts";
import { call } from "./http.ts";
import { runDataHooks } from "./mods.ts";

/** A data file's JSON; null on 404 if `optional`, else a readable Error. */
async function get(file: string, optional = false): Promise<unknown> {
  const res = await call(`/data/${file}`);
  if (optional && res.status === 404) return null;
  if (!res.ok) throw new Error(`/data/${file}: HTTP ${res.status} — run \`qgen export\`?`);
  return res.json();
}

/** base's pool file of a locale: the demo's own list in a demo build (plan 174), no packs there. */
const basePoolFile = (locale: string): string => (buildInfo().demo ? `demo/${poolFile(locale)}` : poolFile(locale));

/** Question locales a pool may exist for (D-78); es always has one. */
export const LOCALES = ["es", "es-ES", "en", "de"] as const;

const cache = new Map<string, Promise<Loaded>>();
const withUi = new Map<string, Promise<EngineData>>();

/** Once per key; a failure is retried on the next call. */
function once<T>(map: Map<string, Promise<T>>, key: string, fn: () => Promise<T>): Promise<T> {
  let out = map.get(key);
  if (!out) {
    out = fn();
    out.catch(() => map.delete(key));
    map.set(key, out);
  }
  return out;
}

/** The engine data of `locale`, its age group and bundle names in `ui` (task 1024); once per pair. */
export function loadEngineData(locale = "es", ui = locale): Promise<EngineData> {
  const base = once(cache, locale, () => load(locale));
  if (ui === locale) return base.then((l) => l.data);
  return once(withUi, `${locale} ${ui}`, async () => {
    const { data, named } = await base;
    return { ...data, uiNames: await namesOf(named, ui) };
  });
}

/** Locales of LOCALES whose pool file exists; the body isn't read. */
export async function availableLocales(): Promise<string[]> {
  const found = await Promise.all(LOCALES.map(async (l) => {
    if (l === "es") return true;
    const res = await call(`/data/${basePoolFile(l)}`);
    await res.body?.cancel();
    return res.ok;
  }));
  return LOCALES.filter((_, i) => found[i]);
}

/** A problem with a mod bundle at load, for the mods screen (plan 115). */
export interface ModIssue {
  mod: string;
  bundle: string;
  /** bundles.json row name, else the id after `<mod>:`. */
  name: string;
  code: "bad_question" | "bad_media" | "bad_categories" | "no_pool" | "bundle_language";
  count: number;
}

const issues = new Map<string, ModIssue>();

/** The mod bundles' load issues so far, latest count per bundle and code. */
export function modIssues(): ModIssue[] {
  return [...issues.values()];
}

function issue(b: Bundle, code: ModIssue["code"], count = 1): void {
  if (count) issues.set(`${b.id} ${code}`, { mod: b.mod ?? "", bundle: b.id, name: b.name || b.id.slice(b.id.indexOf(":") + 1), code, count });
}

/** A mod bundle's file: its JSON, null if missing or unreadable. */
const modGet = (file: string): Promise<unknown> => get(file, true).catch(() => null);

/** `named`: the bundles that may have names files. */
interface Loaded {
  data: EngineData;
  named: Bundle[];
}

/** The locale's pool and its packs' (decision 66), bundles.json, age-groups.json, every bundle's categories file
 * and names files → engineData. A bundle without a categories file has none (categories.load()); a pack
 * without a pool file isn't offered (withPacks). Mod bundles (decision 128) are packs checked by modPool;
 * a broken one is left out like a pack without a file, its issues in modIssues(). Then the mods' data hooks (plan 117). */
async function load(locale: string): Promise<Loaded> {
  const [pool, bundles, ageGroups] = await Promise.all(
    [basePoolFile(locale), "bundles.json", "age-groups.json"].map((f) => get(f)),
  );
  const all = parseBundles(bundles).filter((b) => !buildInfo().demo || b.id === "base").map((b) => {
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
  const taken = new Set<string>();
  mods.forEach((b, i) => {
    const [json, catFile] = modFiles[i];
    packs[b.id] = null;
    const tax = modSubcategories(catFile);
    if (!tax) return issue(b, "bad_categories");
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
  });
  const packed = withPacks(parsePool(pool), all, locale, packs);
  const { questions, bundles: parsed, ageGroups: groups } = runDataHooks({
    locale, questions: packed.pool, bundles: packed.bundles, ageGroups: parseAgeGroups(ageGroups),
  });
  const named = parsed.filter((b) => b.source !== "mod" || byBundle[b.id]);
  const data = engineData(questions, loadCategories(bundles, byBundle), parsed, groups, locale, await namesOf(named, locale), poolHash(pool), buildInfo().demo);
  return { data, named };
}

/** The bundles' names files of `lang` merged (namesFiles: es-ES over es); missing files add nothing. */
async function namesOf(bundles: Bundle[], lang: string): Promise<Names> {
  const files = bundles.flatMap((b) => namesFiles(lang).map((n) => [b, bundleFile(b.id, n)] as const));
  return mergeNames(await Promise.all(files.map(async ([b, file]) =>
    [b.id, b.source === "mod" ? modNames(await modGet(file), b.mod ?? "") : await get(file, true)] as const)));
}

/** app/data/old-keys.json (decision 259); null before the slug migration. */
export async function loadOldKeys(): Promise<OldKeys | null> {
  return (await get("old-keys.json", true)) as OldKeys | null;
}

/** A mod's names file with raw `bundles` keys namespaced `<mod id>:<id>`; full ids kept. */
function modNames(file: unknown, mod: string): unknown {
  const f = file as Partial<Names> | null;
  if (!f?.bundles || typeof f.bundles !== "object") return f;
  const bundles = Object.fromEntries(Object.entries(f.bundles).map(([k, v]) => [k.includes(":") ? k : `${mod}:${k}`, v]));
  return { ...f, bundles };
}
