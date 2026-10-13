import { readFileSync } from "node:fs";
import { join } from "node:path";
import type { Category } from "../../lib/types.ts";
import { type AgeGroup, type Bundle, loadCategories, parseAgeGroups, parseBundles } from "../pool.ts";

const ENGINE = join(import.meta.dirname, "..");
const DATA = join(ENGINE, "../../../data");

/** A file under engine/fixtures/ (plan 18). */
export const fixture = (path: string): unknown => JSON.parse(readFileSync(join(ENGINE, "fixtures", path), "utf8"));

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
