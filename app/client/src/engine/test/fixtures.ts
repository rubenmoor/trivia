import { existsSync, readFileSync } from "node:fs";
import { join } from "node:path";

const ENGINE = join(import.meta.dirname, "..");
const DATA = join(ENGINE, "../../../data");

/** A file under engine/fixtures/ (plan 18). */
export const fixture = (path: string): unknown => JSON.parse(readFileSync(join(ENGINE, "fixtures", path), "utf8"));

/** A file under app/data/, or undefined if absent. */
export function data(path: string): unknown {
  const p = join(DATA, path);
  return existsSync(p) ? JSON.parse(readFileSync(p, "utf8")) : undefined;
}
