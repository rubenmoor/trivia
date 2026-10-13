// UI strings from a typed catalog (plans/15a-ui-translation.md, LUI-1, D-70). No library.
import { de } from "../locales/de.ts";
import { en } from "../locales/en.ts";
import es, { type Catalog, type Override, type Plural, type TextKey, type VariantsKey } from "../locales/es.ts";
import { esES } from "../locales/es-ES.ts";

export type { Key } from "../locales/es.ts";
export type Params = Record<string, string | number>;

const isPlural = (v: unknown): v is Plural => !!v && typeof v === "object" && !Array.isArray(v) && "other" in v;
const isBranch = (v: unknown): v is Record<string, unknown> =>
  !!v && typeof v === "object" && !Array.isArray(v) && !isPlural(v);

/** `over` on `base`, branch by branch; leaves (plural maps and variant arrays too) replaced whole. */
function merge(base: Catalog, over: Override): Catalog {
  const go = (b: unknown, o: unknown): unknown =>
    isBranch(b) && isBranch(o) ? { ...b, ...Object.fromEntries(Object.entries(o).map(([k, v]) => [k, go(b[k], v)])) } : o;
  return go(base, over) as Catalog;
}

/** Shipping catalogs (LUI-5, D-78): `es` is neutral Latin American Spanish, `es-ES` overrides it. */
const CATALOGS: Record<string, Catalog> = { es, "es-ES": merge(es, esES), en, de };

/** UI languages a player can pick (plan 68); `xx` joins `CATALOGS` only later, in dev. */
export const UI_LANGS = Object.keys(CATALOGS);

/** A shipping catalog by tag, `es` if unknown; for pages that show one language without `initLang` (`/comodines`). */
export const catalogFor = (l: string): Catalog => CATALOGS[l] ?? es;

/** Dev-only catalogs, loaded on demand: `xx` (LUI-2). */
const DEV_LANGS = ["xx"];

/** The save's UI language; `?lang=` overrides it in dev only (also `DEV_LANGS`). Unknown → `es`. */
function pickLang(saved?: string): string {
  if (import.meta.env?.DEV && typeof location !== "undefined") {
    const q = new URLSearchParams(location.search).get("lang");
    if (q && (DEV_LANGS.includes(q) || q in CATALOGS)) return q;
  }
  return saved && saved in CATALOGS ? saved : "es";
}

/** Set once by `initLang` before the first render; a change reloads the app (plan 68). */
export let lang = pickLang();
/** `xx` has no language of its own: numbers, plurals and `<html lang>` stay `es`. */
const real = (l: string) => (import.meta.env?.DEV && l === "xx" ? "es" : l);
let catalog = CATALOGS[lang] ?? es;
let numbers = new Intl.NumberFormat(real(lang));
let plurals = new Intl.PluralRules(real(lang));

/** main.ts, before mounting: the save's UI language. */
export async function initLang(saved?: string): Promise<void> {
  lang = pickLang(saved);
  if (import.meta.env?.DEV && lang === "xx" && !CATALOGS.xx) CATALOGS.xx = (await import("../locales/xx.ts")).pseudo(es);
  catalog = CATALOGS[lang];
  numbers = new Intl.NumberFormat(real(lang));
  plurals = new Intl.PluralRules(real(lang));
}

/** Names of the languages in themselves (plan 68): data, not translated. Question `es` is neutral Spanish. */
const ENDONYMS: Record<string, string> = {
  es: "Español (Latinoamérica)",
  "es-ES": "Español (España)",
  en: "English",
  de: "Deutsch",
};

export function endonym(tag: string, kind: "ui" | "questions"): string {
  return kind === "questions" && tag === "es" ? "Español" : (ENDONYMS[tag] ?? tag);
}

const warned = new Set<string>();

/** `⟦key⟧`, with a dev warning once per key (LUI-2). */
function missing(key: string): string {
  if (import.meta.env?.DEV && !warned.has(key)) {
    warned.add(key);
    console.warn(`i18n: missing key ${key} (${lang})`);
  }
  return `⟦${key}⟧`;
}

function lookup(key: string): unknown {
  let node: unknown = catalog;
  for (const part of key.split(".")) {
    if (node === null || typeof node !== "object") return undefined;
    node = (node as Record<string, unknown>)[part];
  }
  return node;
}

/** Replaces `{name}` from params; numbers formatted for `lang`. */
export function fill(text: string, params?: Params): string {
  if (!params) return text;
  return text.replace(/\{(\w+)\}/g, (m, k: string) => {
    const v = params[k];
    return v === undefined ? m : typeof v === "number" ? numbers.format(v) : v;
  });
}

/** Whether `key` names a text in the catalog (for keys built at runtime). */
export function has(key: string): key is TextKey {
  const v = lookup(key);
  return typeof v === "string" || isPlural(v);
}

/** The text of a key; plural maps pick by `params.n`. Missing → `⟦key⟧`. */
export function t(key: TextKey, params?: Params): string {
  const v = lookup(key);
  if (typeof v === "string") return fill(v, params);
  if (isPlural(v)) {
    const n = params?.n;
    return fill((typeof n === "number" ? v[plurals.select(n)] : undefined) ?? v.other, params);
  }
  return missing(key);
}

/** The lines of a variant entry. Missing → `[⟦key⟧]`. */
export function variants(key: VariantsKey): readonly string[] {
  const v = lookup(key);
  return Array.isArray(v) && v.length ? v : [missing(key)];
}

/** `<html lang>` and the tab title; `index.html` keeps «Trivia» as the pre-JS fallback. */
export function initDocument(): void {
  document.documentElement.lang = real(lang);
  document.title = t("app.title");
}
