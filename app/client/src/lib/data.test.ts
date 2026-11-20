// lib/data.ts's and lib/engine.ts's locale logic (pool.ts helpers) on app/data with a zh-Hans pool of chinese-base only (task 2422).
import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { join } from "node:path";
import { defaultChoice } from "../engine/choice.ts";
import { supply, newGame } from "../engine/game.ts";
import {
  baseListsLocale, bundleFile, bundlesFor, loadCategories, localeFor, packsFor, parseAgeGroups, parseBundles,
  parsePool, poolFile, poolLocales, readBasePool, withPacks,
} from "../engine/pool.ts";
import { seededRng } from "../engine/rng.ts";
import { emptySave, engineData, gameLocale } from "../engine/state.ts";

const DATA = join(import.meta.dirname, "../../../data");
const real = (f: string): unknown => JSON.parse(readFileSync(join(DATA, f), "utf8"));
const LOCALES = ["es", "es-ES", "en", "de", "zh-Hans", "zh-Hant"];

// /data/ files: real bundles.json and base's pools; chinese-base gets base's categories and its en questions as zh-Hans
const base = real("pool.en.json") as { questions: Record<string, unknown>[] };
const files = new Map<string, unknown>([
  ["bundles.json", real("bundles.json")],
  ["age-groups.json", real("age-groups.json")],
  ["categories.json", real("categories.json")],
  ...["pool.json", "pool.es-ES.json", "pool.en.json", "pool.de.json"].map((f) => [f, real(f)] as [string, unknown]),
  [bundleFile("chinese-base", "categories.json"), real("categories.json")],
  [poolFile("zh-Hans", "chinese-base"), { version: 1, questions: base.questions.map((q) => ({ ...q, bundle: "chinese-base" })) }],
]);
const bundles = parseBundles(files.get("bundles.json"));
const has = async (f: string): Promise<boolean> => files.has(f);
const read = async (f: string): Promise<unknown> => files.get(f) ?? null;

/** data.ts load()'s steps on `files`, without mods and names. */
async function load(locale: string, from = read) {
  const pool = await readBasePool(bundles, locale, from);
  const packs = Object.fromEntries(await Promise.all(packsFor(bundles, locale).map(async (b) => [b.id, await from(poolFile(locale, b.id))])));
  const out = withPacks(pool ? parsePool(pool) : [], bundles, locale, packs as Record<string, never>);
  const byBundle = Object.fromEntries(out.bundles.map((b) => [b.id, files.get(bundleFile(b.id, "categories.json"))]).filter(([, c]) => c));
  return engineData(out.pool, loadCategories(files.get("bundles.json"), byBundle), out.bundles, parseAgeGroups(files.get("age-groups.json")), locale);
}

test("available locales: zh-Hans by chinese-base's pool alone, zh-Hant (no pool) not", async () => {
  assert.equal(baseListsLocale(bundles, "zh-Hans"), false);
  assert.deepEqual(await poolLocales(LOCALES, bundles, has), ["es", "es-ES", "en", "de", "zh-Hans"]);
  assert.deepEqual(await poolLocales(LOCALES, [], has, (l) => `demo/${poolFile(l)}`), ["es"], "demo: base's own list only");
});

test("load: zh-Hans without base's pool loads chinese-base alone; bundlesFor gives only chinese-base", async () => {
  const data = await load("zh-Hans");
  assert.equal(data.locale, "zh-Hans");
  assert.equal(data.pool.length, base.questions.length);
  assert.deepEqual(bundlesFor(data).map((b) => b.id), ["chinese-base"]);
  const en = bundlesFor(await load("en")).map((b) => b.id);
  assert.equal(en[0], "base");
  assert.ok(!en.includes("chinese-base"), "no en pool for chinese-base in the fixture: not offered");
});

test("load: a missing base pool is still an error where base lists the locale, and in the demo", async () => {
  const noEn = async (f: string) => (f === "pool.en.json" ? null : read(f));
  const error = (p: Promise<unknown>) => p.then(() => "", (e: Error) => e.message);
  assert.ok(/pool\.en\.json: missing/.test(await error(load("en", noEn))));
  assert.ok(/missing/.test(await error(readBasePool(bundles, "zh-Hans", read, `demo/${poolFile("zh-Hans")}`, true))));
});

test("new game locale: zh-Hans when chinese-base's supply passes; zh-Hant and a failing supply fall back to es", async () => {
  const save = emptySave();
  const locales = await poolLocales(LOCALES, bundles, has);
  const ok = async (l: string) => supply(save, await load(l)).ok;
  assert.equal(await localeFor("zh-Hans", locales, ok), "zh-Hans");
  assert.equal(await localeFor("zh-Hant", locales, ok), "es");
  assert.equal(await localeFor("zh-Hans", locales, async () => false), "es");
  const data = await load("zh-Hans");
  const row = newGame(save, data, { rng: seededRng(1), now: "2026-11-20T12:00:00" }, "ana").save.games.at(-1)!;
  assert.equal(gameLocale(row), "zh-Hans");
  assert.deepEqual(defaultChoice(data).bundles, ["chinese-base"]);
});
