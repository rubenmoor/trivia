// Supply outlook at game start (plan 65, D-82): fresh games left, bottleneck, exhausted subcategories.
import type { Choice, GameMode } from "../lib/types.ts";
import { countOf, STANDARD_JOKERS } from "./game.ts";
import type { LevelRanges, PoolQuestion } from "./pool.ts";
import { subcategories } from "./pool.ts";
import { available, LEVELS, PER_LEVEL } from "./selection.ts";
import type { EngineData, SaveData } from "./state.ts";

const ALL_LEVELS = Array.from({ length: LEVELS }, (_, i) => i + 1);

/** Seen events per game from the standard set (D-74): every joker but Soplo replaces a question. */
const JOKER_SEEN = Object.entries(STANDARD_JOKERS).reduce((s, [j, n]) => (j === "hint" ? s : s + (n ?? 0)), 0);

/** Seen events per level per game (D-75, D-77): one game = 12 + the standard set's; rr-competitive
 * × N players; timed: one shared question per round, no jokers. Gamemaster as solo. */
export function seenPerLevel(mode: GameMode, players = 1): number {
  const game = (LEVELS + JOKER_SEEN) / LEVELS;
  if (mode === "rr-competitive") return game * players;
  if (mode === "timed") return 1;
  return game;
}

export interface OutlookChoice extends Choice {
  mode: GameMode;
  /** rr-competitive: players in the game. */
  players?: number;
}

export interface Outlook {
  /** Fresh games left: the largest k whose `4 + k·b` slots per level the count-0 questions fill (0 if none). */
  k: number;
  /** Difficulty ranges of the level(s) that fail first at k + 1, merged, ascending. */
  bottleneck: [number, number][];
  /** An inactive bundle whose activation raises k most, or null. */
  bundleHint: string | null;
  /** Exhausted subcategories not yet shown (`notified_exhausted`), in display order. */
  exhausted: string[];
}

const demandFor = (k: number, b: number) => (k < 0 ? 0 : PER_LEVEL + Math.ceil(k * b));

/** Count-0 questions per difficulty, with prefix sums. */
interface Fresh {
  lo: number;
  /** prefix[i] = questions with difficulty < lo + i. */
  prefix: number[];
}

function freshCounts(fresh: PoolQuestion[]): Fresh {
  if (!fresh.length) return { lo: 0, prefix: [0] };
  const ds = fresh.map((q) => q.difficulty);
  const lo = Math.min(...ds), hi = Math.max(...ds);
  const prefix = Array<number>(hi - lo + 2).fill(0);
  for (const d of ds) prefix[d - lo + 1]++;
  for (let i = 1; i < prefix.length; i++) prefix[i] += prefix[i - 1];
  return { lo, prefix };
}

const between = ({ lo, prefix }: Fresh, a: number, b: number): number => {
  const at = (d: number) => prefix[Math.min(Math.max(d - lo, 0), prefix.length - 1)];
  return at(b + 1) - at(a);
};

/** Difficulty intervals [a, b] where the levels inside need more than it holds (Hall's condition for
 * interval ranges: same-difficulty questions are interchangeable, so this is exact and fast). */
function violations(f: Fresh, ranges: LevelRanges, demand: (level: number) => number): [number, number][] {
  const ends = [...new Set(ranges.flat())].sort((x, y) => x - y);
  const out: [number, number][] = [];
  for (const a of ends) for (const b of ends) {
    if (b < a) continue;
    const need = ALL_LEVELS.reduce((s, l) => (a <= ranges[l - 1][0] && ranges[l - 1][1] <= b ? s + demand(l) : s), 0);
    if (need > between(f, a, b)) out.push([a, b]);
  }
  return out;
}

const fits = (f: Fresh, ranges: LevelRanges, demand: (l: number) => number) => violations(f, ranges, demand).length === 0;

/** Largest k ≥ 0 that fits; -1 if not even 4 per level. */
function freshGames(f: Fresh, ranges: LevelRanges, b: number): number {
  if (!fits(f, ranges, () => demandFor(0, b))) return -1;
  // Per level k ≤ (candidates − 4) / b: an upper bound.
  const cands = ranges.map(([lo, hi]) => between(f, lo, hi));
  let lo = 0, hi = Math.floor((Math.min(...cands) - PER_LEVEL) / b) + 1; // fits(lo), !fits(hi)
  while (hi - lo > 1) {
    const mid = (lo + hi) >> 1;
    if (fits(f, ranges, () => demandFor(mid, b))) lo = mid;
    else hi = mid;
  }
  return lo;
}

/** Levels that fail alone at k + 1 (the rest at k); if none does alone, those inside the smallest intervals short at k + 1. */
function bottleneckLevels(f: Fresh, ranges: LevelRanges, k: number, b: number): number[] {
  const alone = ALL_LEVELS.filter((l) => !fits(f, ranges, (x) => demandFor(x === l ? k + 1 : k, b)));
  if (alone.length) return alone;
  const short = violations(f, ranges, () => demandFor(k + 1, b));
  const inside = ([a, z]: readonly [number, number], [c, d]: readonly [number, number]) => c <= a && z <= d;
  const minimal = short.filter((v) => !short.some((w) => w !== v && inside(w, v)));
  return ALL_LEVELS.filter((l) => minimal.some((v) => inside(ranges[l - 1], v)));
}

/** Overlapping or touching ranges merged. */
function merge(ranges: [number, number][]): [number, number][] {
  const out: [number, number][] = [];
  for (const [lo, hi] of [...ranges].sort((a, b) => a[0] - b[0] || a[1] - b[1])) {
    const last = out.at(-1);
    if (last && lo <= last[1] + 1) last[1] = Math.max(last[1], hi);
    else out.push([lo, hi]);
  }
  return out;
}

/** Subcategories with approved, unblocked questions in the choice's bundles and window, all seen. */
function exhaustedSubs(save: SaveData, data: EngineData, choice: Choice): string[] {
  const [lo, hi] = data.groupById.get(choice.age_group)!.window;
  const count = countOf(save);
  const state = new Map<string, boolean>(); // subcategory → every question seen
  for (const q of available(data.pool, save.blocked, [], new Set(choice.bundles))) {
    if (q.subcategory === null || q.difficulty < lo || q.difficulty > hi) continue;
    state.set(q.subcategory, (state.get(q.subcategory) ?? true) && count(q) > 0);
  }
  return subcategories(data.categories).filter((s) => state.get(s));
}

/** The outlook for a new game with `choice`; reads the save, never writes it. */
export function outlook(save: SaveData, data: EngineData, choice: OutlookChoice): Outlook {
  const ranges = data.groupById.get(choice.age_group)!.levels;
  const b = seenPerLevel(choice.mode, choice.players);
  const count = countOf(save);
  const freshIn = (bundles: Iterable<string>) =>
    freshCounts(available(data.pool, save.blocked, [], new Set(bundles)).filter((q) => count(q) === 0));
  const fresh = freshIn(choice.bundles);
  const raw = freshGames(fresh, ranges, b);
  const k = Math.max(raw, 0);
  const bottleneck = merge(bottleneckLevels(fresh, ranges, raw, b).map((l) => [ranges[l - 1][0], ranges[l - 1][1]]));
  let bundleHint: string | null = null, best = raw;
  for (const { id } of data.bundles) {
    if (choice.bundles.includes(id)) continue;
    const kb = freshGames(freshIn([...choice.bundles, id]), ranges, b);
    if (kb > best) [bundleHint, best] = [id, kb];
  }
  const notified = new Set(save.notified_exhausted);
  const exhausted = exhaustedSubs(save, data, choice).filter((s) => !notified.has(s));
  return { k, bottleneck, bundleHint, exhausted };
}

/** Record `shown` in `notified_exhausted` (a new save); drops entries that aren't exhausted for `choice` any more.
 * Call it at every game start, `shown` empty or not, so the prune runs. */
export function noteExhausted(save: SaveData, data: EngineData, choice: Choice, shown: string[]): SaveData {
  const now = new Set(exhaustedSubs(save, data, choice));
  const kept = save.notified_exhausted.filter((s) => now.has(s));
  const added = shown.filter((s) => now.has(s) && !kept.includes(s));
  return { ...save, notified_exhausted: [...kept, ...added] };
}
