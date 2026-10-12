// Question selection per level (PORT-2): port of app/server/selection.py, same results.
import type { Supply } from "../lib/types.ts";
import type { PoolQuestion } from "./pool.ts";
import type { Rng } from "./rng.ts";

export const LEVELS = 12;
export const PER_LEVEL = 4;
export const LEVEL_RANGES: Readonly<Record<number, readonly [number, number]>> = {
  1: [1, 1], 2: [2, 3], 3: [3, 5], 4: [4, 6], 5: [4, 6], 6: [4, 6],
  7: [5, 7], 8: [6, 8], 9: [6, 9], 10: [7, 10], 11: [8, 10], 12: [9, 10],
};
const ALL_LEVELS = Array.from({ length: LEVELS }, (_, i) => i + 1);

type Q = Pick<PoolQuestion, "id" | "difficulty">;
export type CategoryKey = string | null;
export type SupplyLevel = Supply["levels"][number];

export function inRange(q: Pick<PoolQuestion, "difficulty">, level: number): boolean {
  const [lo, hi] = LEVEL_RANGES[level];
  return lo <= q.difficulty && q.difficulty <= hi;
}

/** Questions that can be offered: approved, not burned, not in `exclude`. */
export function available<T extends Pick<PoolQuestion, "id" | "status">>(
  pool: T[], burned: Iterable<string>, exclude: Iterable<string> = [],
): T[] {
  const skip = new Set([...burned, ...exclude]);
  return pool.filter((q) => q.status === "approved" && !skip.has(q.id));
}

/** PER_LEVEL distinct questions per level from its range (augmenting paths); `missing` empty = all filled. */
export function assign(
  questions: Q[], levels: Iterable<number>,
): { assignment: Map<number, string[]>; missing: Map<number, number> } {
  const width = (l: number) => LEVEL_RANGES[l][1] - LEVEL_RANGES[l][0];
  const sorted = [...levels].sort((a, b) => width(a) - width(b) || a - b);
  const slots = sorted.flatMap((l) => Array<number>(PER_LEVEL).fill(l));
  const cands = new Map(sorted.map((l) => [l, questions.filter((q) => inRange(q, l)).map((q) => q.id)]));
  const owner = new Map<string, number>(); // question id -> slot index

  const augment = (i: number, seen: Set<string>): boolean => {
    for (const qid of cands.get(slots[i])!) {
      if (seen.has(qid)) continue;
      seen.add(qid);
      const o = owner.get(qid);
      if (o === undefined || augment(o, seen)) {
        owner.set(qid, i);
        return true;
      }
    }
    return false;
  };

  const missing = new Map<number, number>();
  slots.forEach((level, i) => {
    if (!augment(i, new Set())) missing.set(level, (missing.get(level) ?? 0) + 1);
  });
  const assignment = new Map<number, string[]>(sorted.map((l) => [l, []]));
  for (const [qid, i] of owner) assignment.get(slots[i])!.push(qid);
  return { assignment, missing };
}

export interface DrawOptions<T> {
  n?: number;
  keep?: T[];
  avoidCategories?: Iterable<CategoryKey>;
  categoryOf?: (q: T) => CategoryKey;
  rng: Rng;
}

/** n questions for `level` from `questions` (already `available`), preferring fresh categories,
 * each only if later levels stay fillable; null if the level can't be filled. */
export function draw<T extends Q & { subcategory?: string | null }>(
  level: number, questions: T[], { n = PER_LEVEL, keep = [], avoidCategories = [], categoryOf, rng }: DrawOptions<T>,
): T[] | null {
  const cat = categoryOf ?? ((q: T) => q.subcategory ?? null);
  const avoid = new Set(avoidCategories);
  const later = Array.from({ length: LEVELS - level }, (_, i) => level + 1 + i);
  const taken = new Set(keep.map((q) => q.id));
  const cands = questions.filter((q) => inRange(q, level) && !taken.has(q.id));
  rng.shuffle(cands, "draw");
  const picked: T[] = [];
  for (let k = 0; k < n; k++) {
    const table = new Set([...keep, ...picked].map(cat));
    const key = (q: T) => (table.has(cat(q)) ? 2 : 0) + (avoid.has(cat(q)) ? 1 : 0);
    cands.sort((a, b) => key(a) - key(b));
    const pickedIds = new Set(picked.map((p) => p.id));
    const q = cands.find((q) => {
      if (pickedIds.has(q.id)) return false;
      const gone = new Set([...taken, ...pickedIds, q.id]);
      return assign(questions.filter((x) => !gone.has(x.id)), later).missing.size === 0;
    });
    if (!q) return null;
    picked.push(q);
  }
  return picked;
}

/** Per-level supply for the supply check (GF-5). */
export function supply(questions: Q[]): SupplyLevel[] {
  const { missing } = assign(questions, ALL_LEVELS);
  return ALL_LEVELS.map((level) => ({
    level,
    range: [LEVEL_RANGES[level][0], LEVEL_RANGES[level][1]],
    candidates: questions.filter((q) => inRange(q, level)).length,
    missing: missing.get(level) ?? 0,
  }));
}
