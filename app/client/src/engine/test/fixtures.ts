import { existsSync, readFileSync } from "node:fs";
import { join } from "node:path";
import type { Category } from "../../lib/types.ts";
import {
  type AgeGroup, type Bundle, loadCategories, packsFor, parseAgeGroups, parseBundles, parsePool, poolFile, type PoolQuestion, subKey, withPacks,
} from "../pool.ts";
import type { OldKeys } from "../save.ts";

const ENGINE = join(import.meta.dirname, "..");
const DATA = join(ENGINE, "../../../data");

/** A file under engine/fixtures/ (plan 18). */
export const fixture = (path: string): unknown => JSON.parse(readFileSync(join(ENGINE, "fixtures", path), "utf8"));

const slug = (name: string): string =>
  name.normalize("NFD").replace(/\p{M}/gu, "").toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");

/** The frozen fixtures on slug keys (decision 259): subcategory names → slugs, categories without names.
 * `oldKeys`: recorded names (bare, also colombia's: pre-D-99) → new keys, like app/data/old-keys.json;
 * `back`: new key → recorded name; `catName`: category slug → recorded name. */
export function slugFixtures() {
  const raw = fixture("categories.json") as Category[];
  const oldKeys: OldKeys = { categories: {}, subcategories: {} };
  const back = new Map<string, string>();
  const catName = new Map(raw.map((c) => [c.slug, c.name ?? c.slug]));
  const categories: Category[] = raw.map(({ name: _, ...c }) => ({
    ...c,
    subcategories: c.subcategories.map((s) => {
      const key = subKey(c.bundle, slug(s));
      oldKeys.subcategories[s] = oldKeys.subcategories[subKey(c.bundle, s)] = key;
      back.set(key, s);
      return slug(s);
    }),
  }));
  const pool = (name: string): PoolQuestion[] =>
    (fixture(`pools/${name}.json`) as { questions: PoolQuestion[] }).questions.map((q) => ({ ...q, subcategory: slug(q.subcategory) }));
  return { categories, oldKeys, back, catName, pool };
}

/** A file under app/data/. */
export const data = (path: string): unknown => JSON.parse(readFileSync(join(DATA, path), "utf8"));

/** Categories of the real app/data/ bundles. */
export function realCategories(): Category[] {
  const bundles = data("bundles.json") as { bundles: { id: string }[] };
  const files = Object.fromEntries(
    bundles.bundles.map((b) => [b.id, data(b.id === "base" ? "categories.json" : `bundles/${b.id}/categories.json`)]),
  );
  return loadCategories(bundles, files);
}

/** The real app/data/ bundles and age groups. */
export const realBundles = (): Bundle[] => parseBundles(data("bundles.json"));
export const realAgeGroups = (): AgeGroup[] => parseAgeGroups(data("age-groups.json"));

/** The real es pool: base's and the packs' (decision 66); a pack without a pool file is not offered (decision 112). */
export function realPool(): PoolQuestion[] {
  const packs = Object.fromEntries(packsFor(realBundles(), "es").filter((b) => existsSync(join(DATA, poolFile("es", b.id)))).map((b) => [b.id, data(poolFile("es", b.id))]));
  return withPacks(parsePool(data("pool.json")), realBundles(), "es", packs).pool;
}
