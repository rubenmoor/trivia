// `--check-mod` (plan 120, decision 133): the loader's validators on one mod folder. Pure Node; mod files are read as data, never run.
import fs from "node:fs/promises";
import path from "node:path";
import { pathToFileURL } from "node:url";
import { BUNDLE_ICONS, bundleRows, readManifest } from "./mods.mjs";
import { contained } from "./resolve.mjs";

// LOCALES in app/client/src/lib/data.ts.
const LOCALES = ["es", "es-ES", "en", "de"];

const ERRORS = {
  not_a_folder: () => "not a folder",
  no_manifest: () => "no mod.json",
  bad_json: (e) => (e.reason === "too_big" ? "mod.json over 64 KB" : "mod.json is not a JSON object"),
  bad_field: (e) => `mod.json: field "${e.field}" missing or invalid`,
  entry_missing: () => "mod.json: entry file not found in the folder",
  bundle_json: () => "data/bundles.json: not a JSON object with a bundles list",
  bundle_row: (e) => `data/bundles.json: row ${e.id ? `"${e.id}"` : "without an id"} needs id, kind (slugs), languages, name, description; ids unique; country (ISO code in capitals, e.g. CO) on kind "region" only`,
  bad_categories: (e) => `${e.file}: missing, or not categories with slug and subcategories (unique)`,
  bad_pool: (e) => `${e.file}: ${e.message}`,
  no_pool: (e) => `bundle ${e.bundle}: no pool file for any of its languages`,
  no_bundles: () => "kind bundle but no bundles in data/bundles.json",
  media_missing: (e) => `${e.file}: question ${e.id}: ${e.what} file ${e.url} not found in the bundle folder`,
};
const WARNINGS = {
  unknown_language: (w) => `mod.json languages: "${w.tag}" isn't a game language`,
  unknown_key: (w) => `mod.json: unknown key "${w.key}"`,
  game_version: (w) => `made for ${w.game}, running ${w.running}`,
  bad_icon: (w) => `bundle ${w.id}: icon ignored (puzzle shown): not allowed on kind "region", else one of ${BUNDLE_ICONS.join(", ")}`,
  bundle_language: (w) => `bundle ${w.bundle}: language "${w.tag}" has no questions in the game (es, es-ES, en, de), ignored`,
  no_pool_file: (w) => `${w.file}: missing, bundle ${w.bundle} not offered in ${w.locale}`,
  bad_names: (w) => `${w.file}: ${w.key ? `${w.kind} "${w.key}" not in ${w.kind === "bundles" ? "data/bundles.json" : "categories.json"}` : "not a JSON object"}, ignored`,
};
// modPool's reasons (engine/pool.ts).
const REASONS = {
  bad_id: "id must be a-z, 0-9 and -, up to 64 characters",
  duplicate_id: "id used twice",
  no_text: "question or answer empty",
  wrong_answers: "needs exactly 3 wrong_answers",
  hints: "needs exactly 3 hints",
  difficulty: "difficulty must be a whole number 1-15",
  subcategory: "subcategory not in categories.json",
  status: 'status must be "approved" or left out',
  bad_media: "media file_url must be a relative path inside the bundle folder (no web URLs)",
};

const text = (table, x) => `${x.code}: ${table[x.code]?.(x) ?? x.code}`;
export const errorText = (e) => text(ERRORS, e);
const warningText = (w) => text(w.code in WARNINGS ? WARNINGS : ERRORS, w);

/** JSON of a file inside `dir`; undefined if missing, Error if unreadable. */
async function readJson(dir, rel) {
  const file = await contained(dir, rel);
  if (!file) return undefined;
  try {
    return JSON.parse(new TextDecoder("utf-8", { fatal: true }).decode(await fs.readFile(file)));
  } catch (err) {
    return err instanceof Error ? err : new Error(String(err));
  }
}

/** Raw relative path of a rewritten mod URL (`/data/bundles/<mod>:<bundle>/…`). */
const relOf = (url) => url.split("/").slice(4).map(decodeURIComponent).join("/");

/**
 * One mod folder → { id, errors, warnings } (counts). `dist`: our built client (its engine/pool.js, never the mod's);
 * `data`: our app/data (age groups, our categories). `out(line, isError)` gets every line as it comes.
 */
export async function checkMod(folder, { dist, data, gameVersion }, out = () => {}) {
  const pool = await import(pathToFileURL(path.join(dist, "engine", "pool.js")).href);
  let errors = 0;
  let warnings = 0;
  const error = (e, indent = "") => (errors++, out(`${indent}error: ${errorText(e)}`, true));
  const warning = (w) => (warnings++, out(`warning: ${warningText(w)}`, true));
  const done = (id) => {
    out(errors ? `${errors} error(s), ${warnings} warning(s): fix the errors above` : `${warnings} warning(s): loads as is`);
    return { id, errors, warnings };
  };

  const mod = await readManifest(folder, gameVersion);
  out(`mod ${mod.id ?? "?"}: ${mod.dir}`);
  mod.warnings.filter((w) => !w.code.startsWith("bundle_")).forEach(warning);
  if (mod.error) error(mod.error);
  // Without a parsed mod.json there is nothing more to read; a bad field: the rest is still checked.
  if (!mod.manifest) return done(mod.id);
  if (!mod.error) out(`kind: ${mod.kind.join(", ") || "none"}`);
  const id = mod.id ?? "mod";
  const rows = await bundleRows(mod.dir);
  rows.warnings.filter((w) => w.code !== "bad_icon").forEach((w) => error(w)); // bad_icon: a warning, shown above
  if (!rows.rows.length) {
    if (mod.kind.includes("bundle") && !rows.warnings.length) error({ code: "no_bundles" });
    return done(mod.id);
  }

  const groups = pool.parseAgeGroups(JSON.parse(await fs.readFile(path.join(data, "age-groups.json"), "utf8")));

  // Like the loader: question ids unique per locale across this mod's pools.
  const taken = Object.fromEntries(LOCALES.map((l) => [l, new Set()]));
  for (const row of rows.rows) {
    const bundle = `${id}:${row.id}`;
    const dir = path.join(mod.dir, "data", "bundles", row.id);
    const rel = (name) => `data/bundles/${row.id}/${name}`;
    out(`bundle ${row.id} (${row.kind}): ${row.name}`);
    for (const tag of row.languages.filter((l) => !LOCALES.includes(l))) warning({ code: "bundle_language", bundle: row.id, tag });
    const cats = await readJson(dir, "categories.json");
    const tax = cats instanceof Error ? null : pool.modSubcategories(cats);
    if (!tax) {
      error({ code: "bad_categories", file: rel("categories.json") });
      continue;
    }
    let pools = 0;
    for (const locale of row.languages.filter((l) => LOCALES.includes(l))) {
      const file = locale === "es" ? "pool.json" : `pool.${locale}.json`;
      const json = await readJson(dir, file);
      if (json === undefined) {
        warning({ code: "no_pool_file", file: rel(file), bundle: row.id, locale });
        continue;
      }
      pools++;
      let res;
      try {
        if (json instanceof Error) throw json;
        res = pool.modPool(json, bundle, tax.subs, taken[locale]);
      } catch (err) {
        error({ code: "bad_pool", file: rel(file), message: err.message });
        continue;
      }
      const missing = [];
      for (const q of res.questions)
        for (const [what, m] of [["media", q.media], ["background", q.background]])
          if (m?.file_url && !(await contained(dir, relOf(m.file_url)))) missing.push({ id: q.id.slice(id.length + 1), what, url: relOf(m.file_url) });
      const dropped = res.reasons.filter((r) => r.dropped).length;
      out(`  ${locale}: ${res.questions.length} ok, ${dropped} dropped`);
      const raw = new Map(json.questions.map((q) => [q?.id, q]));
      for (const r of res.reasons) {
        const q = raw.get(r.id);
        const web = r.reason === "bad_media" && [q?.media, q?.background].some((m) => /^[a-z][a-z0-9+.-]*:/i.test(m?.file_url ?? ""));
        const why = web ? "web URLs are dropped: put the file in the bundle folder" : REASONS[r.reason] ?? r.reason;
        errors++;
        out(`  error: ${r.reason}: ${rel(file)}: question ${r.id}${r.dropped ? " dropped" : ", its media dropped"}: ${why}`, true);
      }
      for (const m of missing) error({ code: "media_missing", file: rel(file), ...m }, "  ");
      for (const g of groups) {
        const [lo, hi] = g.window;
        const inWindow = res.questions.filter((q) => q.difficulty >= lo && q.difficulty <= hi);
        const none = [];
        for (let d = lo; d <= hi; d++) if (!inWindow.some((q) => q.difficulty === d)) none.push(d);
        out(`    ${g.id} (${lo}-${hi}): ${inWindow.length} questions${none.length ? `, none at ${none.join(", ")}` : ""}`);
      }
    }
    if (!pools) error({ code: "no_pool", bundle: row.id });
    // Every UI language's names file (namesFiles in engine/state.ts), unknown keys too.
    const known = { bundles: new Set(rows.rows.map((r) => r.id)), categories: new Set(tax.slugs), subcategories: new Set(tax.subs) };
    for (const locale of LOCALES) {
      const file = rel(`names.${locale}.json`);
      const names = await readJson(dir, `names.${locale}.json`);
      if (names === undefined) continue;
      if (names instanceof Error || names === null || typeof names !== "object" || Array.isArray(names)) {
        warning({ code: "bad_names", file });
        continue;
      }
      for (const [kind, keys] of Object.entries(known))
        for (const key of Object.keys(typeof names[kind] === "object" ? (names[kind] ?? {}) : {}))
          if (!keys.has(key.startsWith(`${id}:`) ? key.slice(id.length + 1) : key)) warning({ code: "bad_names", file, kind, key });
    }
  }
  return done(mod.id);
}
