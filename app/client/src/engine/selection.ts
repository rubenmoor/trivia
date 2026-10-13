// Question selection per level (PORT-2): port of the former app/server/selection.py (deleted in PORT-8), same results.
import type { Supply } from "../lib/types.ts";
import type { LevelRanges, PoolQuestion } from "./pool.ts";
import type { Rng } from "./rng.ts";

/** Defaults; a game's own: `settings.levels` (= its ranges' length) and `settings.cards` (D-88). */
export const LEVELS = 12;
export const PER_LEVEL = 4;

/** Levels 1..n of `ranges`. */
export const levelsOf = (ranges: LevelRanges): number[] => Array.from({ length: ranges.length }, (_, i) => i + 1);

type Q = Pick<PoolQuestion, "id" | "difficulty">;
type CategoryKey = string | null;
type SupplyLevel = Supply["levels"][number];

export function inRange(q: Pick<PoolQuestion, "difficulty">, level: number, ranges: LevelRanges): boolean {
  const [lo, hi] = ranges[level - 1];
  return lo <= q.difficulty && q.difficulty <= hi;
}

/** Questions that can be offered: approved, not blocked, not in `exclude`, in an active bundle (seen ones too, plan 65). */
export function available<T extends Pick<PoolQuestion, "id" | "status"> & { bundle?: string }>(
  pool: T[], blocked: Iterable<string>, exclude: Iterable<string>, bundles: ReadonlySet<string>,
): T[] {
  const skip = new Set([...blocked, ...exclude]);
  return pool.filter((q) => q.status === "approved" && !skip.has(q.id) && bundles.has(q.bundle ?? "base"));
}

/** `perLevel` distinct questions per level from its range (augmenting paths); `missing` empty = all filled. */
export function assign(
  questions: Q[], levels: Iterable<number>, ranges: LevelRanges, perLevel = PER_LEVEL,
): { assignment: Map<number, string[]>; missing: Map<number, number> } {
  const width = (l: number) => ranges[l - 1][1] - ranges[l - 1][0];
  const sorted = [...levels].sort((a, b) => width(a) - width(b) || a - b);
  const slots = sorted.flatMap((l) => Array<number>(perLevel).fill(l));
  const cands = new Map(sorted.map((l) => [l, questions.filter((q) => inRange(q, l, ranges)).map((q) => q.id)]));
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
  ranges: LevelRanges;
  n?: number;
  /** Cards each later level must keep fillable. */
  perLevel?: number;
  keep?: T[];
  avoidCategories?: Iterable<CategoryKey>;
  categoryOf?: (q: T) => CategoryKey;
  /** Seen count per question (plan 65), default 0. */
  countOf?: (q: T) => number;
  rng: Rng;
}

/** n questions for `level` from `questions` (already `available`): the lowest seen count first, then
 * fresh categories, each only if later levels stay fillable; null if the level can't be filled. */
export function draw<T extends Q & { subcategory?: string | null }>(
  level: number, questions: T[], { ranges, n = PER_LEVEL, perLevel = PER_LEVEL, keep = [], avoidCategories = [], categoryOf, countOf, rng }: DrawOptions<T>,
): T[] | null {
  const cat = categoryOf ?? ((q: T) => q.subcategory ?? null);
  const avoid = new Set(avoidCategories);
  const later = Array.from({ length: ranges.length - level }, (_, i) => level + 1 + i);
  const taken = new Set(keep.map((q) => q.id));
  const cands = questions.filter((q) => inRange(q, level, ranges) && !taken.has(q.id));
  rng.shuffle(cands, "draw");
  const count = new Map(cands.map((q) => [q.id, countOf?.(q) ?? 0]));
  const picked: T[] = [];
  for (let k = 0; k < n; k++) {
    const table = new Set([...keep, ...picked].map(cat));
    const key = (q: T) => (table.has(cat(q)) ? 2 : 0) + (avoid.has(cat(q)) ? 1 : 0);
    cands.sort((a, b) => count.get(a.id)! - count.get(b.id)! || key(a) - key(b));
    const pickedIds = new Set(picked.map((p) => p.id));
    const q = cands.find((q) => {
      if (pickedIds.has(q.id)) return false;
      const gone = new Set([...taken, ...pickedIds, q.id]);
      return assign(questions.filter((x) => !gone.has(x.id)), later, ranges, perLevel).missing.size === 0;
    });
    if (!q) return null;
    picked.push(q);
  }
  return picked;
}

/** Per-level supply for the supply check (GF-5). */
export function supply(questions: Q[], ranges: LevelRanges, perLevel = PER_LEVEL): SupplyLevel[] {
  const all = levelsOf(ranges);
  const { missing } = assign(questions, all, ranges, perLevel);
  return all.map((level) => ({
    level,
    range: [ranges[level - 1][0], ranges[level - 1][1]],
    candidates: questions.filter((q) => inRange(q, level, ranges)).length,
    missing: missing.get(level) ?? 0,
  }));
}
