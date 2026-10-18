// Supply outlook at game start (plan 65, D-82): fresh games left, bottleneck, tight levels (decision 31), bundles running out.
import type { Choice, GameMode } from "../lib/types.ts";
import { availableFor, countOf, rangesFor, STANDARD_JOKERS } from "./game.ts";
import type { LevelRanges, PoolQuestion } from "./pool.ts";
import { bundlesFor } from "./pool.ts";
import { LEVELS, levelsOf } from "./selection.ts";
import type { EngineData, SaveData } from "./state.ts";

/** Seen events per game from the standard set (D-74): every joker but Soplo replaces a question. */
const JOKER_SEEN = Object.entries(STANDARD_JOKERS).reduce((s, [j, n]) => (j === "hint" ? s : s + (n ?? 0)), 0);

/** Seen events per level per game (D-75, D-77): one game = its levels + the standard set's; rr-competitive
 * × N players; timed: one question per player still in, no jokers, nobody dropping out (decision 276). Gamemaster,
 * rr-coop as solo. */
function seenPerLevel(mode: GameMode, players = 1, levels = LEVELS): number {
  if (mode === "timed") return players;
  const game = (levels + JOKER_SEEN) / levels;
  return mode === "rr-competitive" ? game * players : game;
}

interface OutlookChoice extends Choice {
  mode: GameMode;
  /** rr-competitive, timed: players in the game. */
  players?: number;
}

export interface Outlook {
  /** Fresh games left: the largest k whose `cards + k·b` slots per level the count-0 questions fill (0 if none). */
  k: number;
  /** Difficulty ranges of the level(s) that fail first at k + 1, merged, ascending. */
  bottleneck: [number, number][];
  /** Difficulty ranges of the levels with ≤ 1 count-0 question under one Hall assignment (decision 31), merged. */
  tight: [number, number][];
  /** Some level has no count-0 question left: this game may repeat. */
  none: boolean;
  /** An inactive non-base bundle of the locale whose activation shrinks the warning most (none, then tight levels), or null. */
  bundleHint: string | null;
  /** Chosen bundles running out (`runningOutBundles`) not yet shown (`notified_exhausted`), in choice order. */
  runningOut: string[];
}

/** Slots per level: `per` cards (at least 1) plus k games' seen events. */
const demandFor = (k: number, b: number, per: number) => (k < 0 ? 0 : per + Math.ceil(k * b));

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
    const need = levelsOf(ranges).reduce((s, l) => (a <= ranges[l - 1][0] && ranges[l - 1][1] <= b ? s + demand(l) : s), 0);
    if (need > between(f, a, b)) out.push([a, b]);
  }
  return out;
}

const fits = (f: Fresh, ranges: LevelRanges, demand: (l: number) => number) => violations(f, ranges, demand).length === 0;

/** Largest k ≥ 0 that fits; -1 if not even `per` per level. */
function freshGames(f: Fresh, ranges: LevelRanges, b: number, per: number): number {
  if (!fits(f, ranges, () => demandFor(0, b, per))) return -1;
  // Per level k ≤ (candidates − per) / b: an upper bound.
  const cands = ranges.map(([lo, hi]) => between(f, lo, hi));
  let lo = 0, hi = Math.floor((Math.min(...cands) - per) / b) + 1; // fits(lo), !fits(hi)
  while (hi - lo > 1) {
    const mid = (lo + hi) >> 1;
    if (fits(f, ranges, () => demandFor(mid, b, per))) lo = mid;
    else hi = mid;
  }
  return lo;
}

/** Levels that fail alone at `bump` (the rest at `base`); if none does alone, those inside the smallest intervals short at `bump`. */
function shortLevels(f: Fresh, ranges: LevelRanges, base: number, bump: number): number[] {
  const all = levelsOf(ranges);
  const alone = all.filter((l) => !fits(f, ranges, (x) => (x === l ? bump : base)));
  if (alone.length) return alone;
  const short = violations(f, ranges, () => bump);
  const inside = ([a, z]: readonly [number, number], [c, d]: readonly [number, number]) => c <= a && z <= d;
  const minimal = short.filter((v) => !short.some((w) => w !== v && inside(w, v)));
  return all.filter((l) => minimal.some((v) => inside(ranges[l - 1], v)));
}

/** Decision 31: levels that can't get 2 count-0 questions; `none`: some level can't get 1 (then only those). */
function tightness(f: Fresh, ranges: LevelRanges): { none: boolean; levels: number[] } {
  if (fits(f, ranges, () => 2)) return { none: false, levels: [] };
  const none = !fits(f, ranges, () => 1);
  return { none, levels: none ? shortLevels(f, ranges, 0, 1) : shortLevels(f, ranges, 1, 2) };
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

/** Chosen bundles running out (decision 31's super-tight rule per bundle): of their approved, unblocked, allowed
 * questions in the window (custom: start–end), some seen and at most 1 unseen. */
function runningOutBundles(save: SaveData, data: EngineData, choice: Choice): string[] {
  const [lo, hi] = choice.difficulty ? [choice.difficulty.start, choice.difficulty.end] : data.groupById.get(choice.age_group!)!.window;
  const count = countOf(save, data);
  return choice.bundles.filter((b) => {
    const qs = availableFor(save, data, choice, [b]).filter((q) => q.difficulty >= lo && q.difficulty <= hi);
    const fresh = qs.filter((q) => count(q) === 0).length;
    return fresh <= 1 && qs.length > fresh;
  });
}

/** The outlook for a new game with `choice`; reads the save, never writes it. */
export function outlook(save: SaveData, data: EngineData, choice: OutlookChoice): Outlook {
  const ranges = rangesFor(data, choice);
  const b = seenPerLevel(choice.mode, choice.players, choice.levels);
  // timed: no cards, N questions per level (the session's supply check)
  const per = choice.mode === "timed" ? choice.players ?? 1 : Math.max(choice.cards, 1);
  const count = countOf(save, data);
  const freshIn = (bundles: Iterable<string>) =>
    freshCounts(availableFor(save, data, choice, bundles).filter((q) => count(q) === 0));
  const fresh = freshIn(choice.bundles);
  const raw = freshGames(fresh, ranges, b, per);
  const k = Math.max(raw, 0);
  const at = (l: number): [number, number] => [ranges[l - 1][0], ranges[l - 1][1]];
  const bottleneck = merge(shortLevels(fresh, ranges, demandFor(raw, b, per), demandFor(raw + 1, b, per)).map(at));
  const tight = tightness(fresh, ranges);
  const score = ({ none, levels }: typeof tight) => (none ? ranges.length + 1 : 0) + levels.length;
  let bundleHint: string | null = null, best = score(tight);
  for (const { id, kind } of bundlesFor(data)) {
    if (!best || kind === "base" || choice.bundles.includes(id)) continue;
    const sb = score(tightness(freshIn([...choice.bundles, id]), ranges));
    if (sb < best) [bundleHint, best] = [id, sb];
  }
  const notified = new Set(save.notified_exhausted);
  const runningOut = runningOutBundles(save, data, choice).filter((b) => !notified.has(b));
  return { k, bottleneck, tight: merge(tight.levels.map(at)), none: tight.none, bundleHint, runningOut };
}

export interface SessionOutlook {
  /** The session's: the group with the lowest `k` (first on a tie). */
  outlook: Outlook;
  /** One per distinct age group, in seat order (rr-coop: the team's one). */
  groups: { age_group: string | null; players: number; outlook: Outlook }[];
}

/** Outlook of a multiplayer session (plan 158): rr-coop as solo; rr-competitive one per distinct age group,
 * `players` = its seats; timed one for all; `seatGroups` = each seat's age group, join order. `choice.age_group` is the shared one. */
export function sessionOutlook(save: SaveData, data: EngineData, choice: OutlookChoice, seatGroups: (string | null)[] = []): SessionOutlook {
  const counts = new Map<string | null, number>();
  if (choice.mode === "rr-competitive") for (const g of seatGroups) counts.set(g ?? choice.age_group, (counts.get(g ?? choice.age_group) ?? 0) + 1);
  if (!counts.size) counts.set(choice.age_group, choice.players ?? 1);
  const groups = [...counts].map(([age_group, players]) => ({
    age_group, players, outlook: outlook(save, data, { ...choice, age_group, players }),
  }));
  const worst = groups.reduce((a, g) => (g.outlook.k < a.outlook.k ? g : a));
  return { outlook: worst.outlook, groups };
}

/** Record `shown` in `notified_exhausted` (a new save); drops entries that aren't running out for `choice` any more
 * (also subcategory keys from before task 1104). Call it at every game start, `shown` empty or not, so the prune runs. */
export function noteRunningOut(save: SaveData, data: EngineData, choice: Choice, shown: string[]): SaveData {
  const now = new Set(runningOutBundles(save, data, choice));
  const kept = save.notified_exhausted.filter((s) => now.has(s));
  const added = shown.filter((s) => now.has(s) && !kept.includes(s));
  return { ...save, notified_exhausted: [...kept, ...added] };
}
