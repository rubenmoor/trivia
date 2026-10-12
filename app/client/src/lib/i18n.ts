// UI strings from a typed catalog (plans/15a-ui-translation.md, LUI-1, D-70). No library.
import es, { type Catalog, type Plural, type TextKey, type VariantsKey } from "../locales/es";

export type { Key, TextKey, VariantsKey } from "../locales/es";
export type Params = Record<string, string | number>;

const CATALOGS: Record<string, Catalog> = { es };

/** `es`; `?lang=` overrides it in dev only (no language menu, OQ-31). */
function pickLang(): string {
  if (import.meta.env?.DEV && typeof location !== "undefined") {
    const q = new URLSearchParams(location.search).get("lang");
    if (q && q in CATALOGS) return q;
  }
  return "es";
}

export const lang = pickLang();
const catalog = CATALOGS[lang];
const numbers = new Intl.NumberFormat(lang);
const plurals = new Intl.PluralRules(lang);

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
  return typeof v === "string" || (!!v && typeof v === "object" && !Array.isArray(v) && "other" in v);
}

/** The text of a key; plural maps pick by `params.n`. Missing → `⟦key⟧`. */
export function t(key: TextKey, params?: Params): string {
  const v = lookup(key);
  if (typeof v === "string") return fill(v, params);
  if (v && typeof v === "object" && !Array.isArray(v) && "other" in v) {
    const p = v as Plural;
    const n = params?.n;
    return fill((typeof n === "number" ? p[plurals.select(n)] : undefined) ?? p.other, params);
  }
  return `⟦${key}⟧`;
}

/** The lines of a variant entry. Missing → `[⟦key⟧]`. */
export function variants(key: VariantsKey): readonly string[] {
  const v = lookup(key);
  return Array.isArray(v) && v.length ? v : [`⟦${key}⟧`];
}

/** `<html lang>` and the tab title; `index.html` keeps «Trivia» as the pre-JS fallback. */
export function initDocument(): void {
  document.documentElement.lang = lang;
  document.title = t("app.title");
}
