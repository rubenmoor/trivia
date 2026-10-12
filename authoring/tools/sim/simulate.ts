// Games per new player (plan 62, CT-2; plan 65): engine games on one v3 save until the first repeat (a seen card offered).
// stdin: a cell {locale, bundles?, age_group?, mode?, player?, players?, seeds?, seed?} or an array of cells; stdout: JSON.
import { readFileSync } from "node:fs";
import { GameError, STANDARD_JOKERS, answer, joker, newGame, pick, resolveChoice, view } from "../../../app/client/src/engine/game.ts";
import { outlook } from "../../../app/client/src/engine/outlook.ts";
import { categoryOf, type LevelRanges } from "../../../app/client/src/engine/pool.ts";
import { seededRng } from "../../../app/client/src/engine/rng.ts";
import * as selection from "../../../app/client/src/engine/selection.ts";
import { emptySave, type EngineData, type GameState, type Io, type SaveData } from "../../../app/client/src/engine/state.ts";
import type { GameMode, JokerName } from "../../../app/client/src/lib/types.ts";
import { loadData, type Loaded } from "./load.ts";

/** `typical`: p(correct) linear from level 1 to level 12. Only a model. */
export const TYPICAL_P = [0.95, 0.6] as const;
const NOW = "2026-01-01T00:00:00";
const NAME = "Sim";
const SIM_MODES = ["solo", "rr-coop", "rr-competitive", "timed"];
const MULTI = ["rr-competitive", "timed"];
/** Runs stop here if no repeat came yet (`capped`). */
export const MAX_GAMES = 500;

interface Cell {
  locale: string;
  bundles?: string[];
  age_group?: string;
  mode?: string;
  player?: "strong" | "typical";
  /** rr-competitive, timed: default 4. */
  players?: number;
  seeds?: number;
  seed?: number;
}

interface Bottleneck {
  level: number;
  lo: number;
  hi: number;
  /** Subcategories with questions at this range in the pool and none left. */
  dry: string[];
}

/** Model randomness (mulberry32), apart from the engine's Rng. */
function uniform(seed: number): () => number {
  let a = seed >>> 0;
  return () => {
    a = (a + 0x6d2b79f5) >>> 0;
    let t = Math.imul(a ^ (a >>> 15), a | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

const pCorrect = (level: number): number =>
  TYPICAL_P[0] + (TYPICAL_P[1] - TYPICAL_P[0]) * (level - 1) / (selection.LEVELS - 1);

/** First missing level of a supply_short (the whole pool, any count). */
function short(e: GameError, seen: Set<string>, data: EngineData, bundles: Set<string>): Bottleneck {
  const { level, lo, hi } = (e.params.levels as { level: number; lo: number; hi: number }[])[0];
  return dryAt(level, lo, hi, seen, data, bundles);
}

/** The level with the subcategories whose questions at its range were all seen. */
function dryAt(level: number, lo: number, hi: number, seen: Set<string>, data: EngineData, bundles: Set<string>): Bottleneck {
  const at = (qs: typeof data.pool) => new Set(qs.filter((q) => lo <= q.difficulty && q.difficulty <= hi).map((q) => q.subcategory));
  const all = selection.available(data.pool, [], [], bundles);
  const had = at(all);
  const still = at(all.filter((q) => !seen.has(q.id)));
  return { level, lo, hi, dry: [...had].filter((s) => s !== null && !still.has(s)) as string[] };
}

type Rand = { rand: () => number; randInt: (n: number) => number };
/** `games`: until the first repeat (Cambiazo's cards too); `draw`: until the first in a level draw, with its bottleneck. */
type Run = { games: number; cambiazo: boolean; draw: number; capped: boolean; bottleneck: Bottleneck };
const NONE: Bottleneck = { level: 0, lo: 0, hi: 0, dry: [] };

/** Ids with a seen row. */
const seenIds = (save: SaveData) => new Set(save.seen.map((s) => s.question_id));

/** One seed on one v3 save: games until the first that offers a seen card (count ≥ 1), and until the first
 * whose level draw does; at most MAX_GAMES. */
function run(data: EngineData, cell: Cell, seed: number): Run {
  const io: Io = { rng: seededRng(seed), now: NOW };
  const rand = uniform(seed ^ 0x9e3779b9);
  const r: Rand = { rand, randInt: (n) => Math.floor(rand() * n) };
  const args = { mode: "solo", age_group: cell.age_group, bundles: cell.bundles };
  const choice = resolveChoice(data, args);
  const bundles = new Set(choice.bundles);
  const ranges = data.groupById.get(choice.age_group)!.levels;
  if (cell.mode === "timed") return runTimed(data, cell, io, r, ranges, bundles);
  // rr-competitive until MD-8: one solo game per player on the one save (D-82); a game = a round.
  const names = cell.mode === "rr-competitive" ? Array.from({ length: cell.players! }, (_, i) => `${NAME} ${i + 1}`) : [NAME];
  let save = emptySave();
  let first: { games: number; cambiazo: boolean } | null = null;
  for (let games = 0; games < MAX_GAMES; games++) {
    for (const name of names) {
      const before = seenIds(save);
      let got: Repeats;
      try {
        ({ save, ...got } = playGame(save, data, io, r, name, args, cell, before));
      } catch (e) {
        if (e instanceof GameError && e.code === "supply_short") {
          return { ...(first ?? { games, cambiazo: false }), draw: games, capped: false, bottleneck: short(e, before, data, bundles) };
        }
        throw e;
      }
      if (!first && got.any !== null) first = { games, cambiazo: got.draw === null };
      if (got.draw !== null) {
        return { ...first!, draw: games, capped: false, bottleneck: dryAt(got.draw, ...ranges[got.draw - 1], before, data, bundles) };
      }
      // Finished games only slow every clone down; seen rows carry the counts.
      save.games = [];
    }
  }
  return { ...(first ?? { games: MAX_GAMES, cambiazo: false }), draw: MAX_GAMES, capped: true, bottleneck: NONE };
}

/** First level that offered a seen card: any card, a level-draw card (not Cambiazo's); null = none. */
type Repeats = { any: number | null; draw: number | null };

/** One engine game from newGame to won or lost, with its repeats of `seen`; newGame's GameError passes through. */
function playGame(
  save: SaveData, data: EngineData, io: Io, { rand, randInt }: Rand, name: string, args: object, cell: Cell, seen: Set<string>,
): { save: SaveData } & Repeats {
  let state: GameState;
  const reps: Repeats = { any: null, draw: null };
  let n = 0;
  const check = (cambiazo = false) => {
    if (state.offered.slice(n).some((id) => seen.has(id))) {
      reps.any ??= state.level;
      if (!cambiazo) reps.draw ??= state.level;
    }
    n = state.offered.length;
  };
  ({ save, state } = newGame(save, data, io, name, args));
  check();
  // Each joker of the standard set once, at a random level; a refused one is skipped.
  const pending = (Object.entries(STANDARD_JOKERS) as [JokerName, number | null][])
    .flatMap(([j, n]) => Array.from({ length: n ?? 0 }, () => ({ joker: j, level: 1 + randInt(selection.LEVELS) })));
  while (state.phase === "select" || state.phase === "question") {
    if (state.phase === "select") ({ save, state } = pick(save, data, io, randInt(state.options.length)));
    const due = pending.filter((p) => p.level === state.level);
    for (const p of due) {
      pending.splice(pending.indexOf(p), 1);
      const jargs = jokerArgs(p.joker, save, data, io, state, randInt);
      if (jargs === null) continue;
      try {
        ({ save, state } = joker(save, data, io, p.joker, jargs));
        check(p.joker === "category");
      } catch (e) {
        if (!(e instanceof GameError)) throw e;
      }
      if (state.phase !== "question") break;
    }
    if (state.phase !== "question") continue;
    const correct = state.answers.indexOf(data.byId.get(state.current!)!.answer);
    const right = cell.player === "strong" || rand() < pCorrect(state.level);
    const wrong = state.answers.map((_, i) => i).filter((i) => i !== correct && !state.struck.includes(i));
    ({ save, state } = answer(save, data, io, right ? correct : wrong[randInt(wrong.length)]));
    check();
  }
  return { save, ...reps };
}

/** timed until MD-9 (D-80): round = level, one question per player still in, seen for the save; no jokers.
 * A wrong answer drops the player (strong: nobody); one left wins. Games until a round draws a seen card (both counts). */
function runTimed(
  data: EngineData, cell: Cell, io: Io, { rand }: Rand, ranges: LevelRanges, bundles: Set<string>,
): Run {
  const cat = categoryOf(data.broad);
  const count = new Map<string, number>();
  const pool = selection.available(data.pool, [], [], bundles);
  const n = cell.players!, last = Math.min(n, 2) - 1;
  for (let games = 0; games < MAX_GAMES; games++) {
    const asked = new Set<string>(), cats = new Set<string | null>();
    const before = new Set(count.keys());
    let alive = n;
    for (let level = 1; level <= selection.LEVELS && alive > last; level++) {
      const drawn = selection.draw(level, pool.filter((q) => !asked.has(q.id)), {
        ranges, n: alive, avoidCategories: cats, categoryOf: cat, countOf: (q) => count.get(q.id) ?? 0, rng: io.rng,
      });
      if (drawn === null || drawn.some((q) => before.has(q.id))) {
        return { games, cambiazo: false, draw: games, capped: false, bottleneck: dryAt(level, ...ranges[level - 1], before, data, bundles) };
      }
      for (const q of drawn) {
        count.set(q.id, (count.get(q.id) ?? 0) + 1);
        asked.add(q.id);
        cats.add(cat(q));
      }
      if (cell.player !== "strong") alive -= Array.from({ length: alive }, () => rand() >= pCorrect(level)).filter(Boolean).length;
    }
  }
  return { games: MAX_GAMES, cambiazo: false, draw: MAX_GAMES, capped: true, bottleneck: NONE };
}

/** Arguments for a joker, or null to skip it: Cambiazo takes a random subcategory the engine allows. */
function jokerArgs(name: JokerName, save: SaveData, data: EngineData, io: Io, state: GameState, randInt: (n: number) => number) {
  if (name === "snipe") {
    const open = state.answers.map((_, i) => i).filter((i) => !state.struck.includes(i));
    return { index: open[randInt(open.length)] };
  }
  if (name !== "category") return {};
  const subs = view(save, data, io)?.jokers?.category.categories
    .flatMap((c) => c.subcategories.filter((s) => s.available).map((s) => s.name)) ?? [];
  return subs.length ? { subcategory: subs[randInt(subs.length)] } : null;
}

function quantile(sorted: number[], q: number): number {
  const i = (sorted.length - 1) * q, lo = Math.floor(i);
  return sorted[lo] + (sorted[Math.ceil(i)] - sorted[lo]) * (i - lo);
}

function simulate(cell: Cell, loaded: Loaded) {
  const mode = cell.mode ?? "solo", player = cell.player ?? "typical";
  const players = MULTI.includes(mode) ? cell.players ?? 4 : 1;
  const head = { locale: cell.locale, bundles: cell.bundles ?? null, age_group: cell.age_group ?? null, mode, player, players };
  if (!loaded.ok) return { ...head, result: "no_pool", pool: loaded.pool };
  // rr-coop sees like solo (D-77); the engine runs it as solo.
  if (!SIM_MODES.includes(mode)) throw new Error(`mode ${mode} not simulated (${SIM_MODES.join(", ")})`);
  const t0 = performance.now();
  const base = cell.seed ?? 1, n = cell.seeds ?? 50;
  const runs = Array.from({ length: n }, (_, i) => ({ seed: base + i, ...run(loaded.data, { ...cell, mode, player, players }, base + i) }));
  const games = runs.map((r) => r.games).sort((a, b) => a - b);
  const draws = runs.map((r) => r.draw).sort((a, b) => a - b);
  const done = runs.filter((r) => !r.capped);
  const levels = new Map<number, number>();
  for (const r of done) levels.set(r.bottleneck.level, (levels.get(r.bottleneck.level) ?? 0) + 1);
  const top = [...levels].sort((a, b) => b[1] - a[1] || a[0] - b[0])[0]?.[0];
  const atTop = done.filter((r) => r.bottleneck.level === top);
  const dry = new Map<string, number>();
  for (const r of atTop) for (const s of r.bottleneck.dry) dry.set(s, (dry.get(s) ?? 0) + 1);
  const choice = resolveChoice(loaded.data, { age_group: cell.age_group, bundles: cell.bundles });
  const fresh = outlook(emptySave(), loaded.data, { ...choice, mode: mode as GameMode, players });
  return {
    ...head, result: "ok", pool: loaded.pool, model: { typical_p: TYPICAL_P }, max_games: MAX_GAMES,
    games: { median: quantile(games, 0.5), p10: quantile(games, 0.1), min: games[0], max: games.at(-1),
      cambiazo: runs.filter((r) => r.cambiazo).length },
    draw: { median: quantile(draws, 0.5), p10: quantile(draws, 0.1), min: draws[0], max: draws.at(-1), capped: n - done.length },
    k: fresh.k,
    repeat: top === undefined ? null : {
      level: top, lo: atTop[0].bottleneck.lo, hi: atTop[0].bottleneck.hi, seeds: atTop.length,
      dry: [...dry].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0])).slice(0, 3).map(([s]) => s),
    },
    seeds: runs.map((r) => ({
      seed: r.seed, games: r.games, cambiazo: r.cambiazo, draw: r.draw, capped: r.capped, repeat_level: r.capped ? null : r.bottleneck.level,
    })),
    ms: Math.round(performance.now() - t0),
  };
}

const input = JSON.parse(readFileSync(0, "utf8")) as Cell | Cell[];
const cache = new Map<string, Loaded>();
const one = (c: Cell) => {
  if (!cache.has(c.locale)) cache.set(c.locale, loadData(c.locale));
  return simulate(c, cache.get(c.locale)!);
};
process.stdout.write(JSON.stringify(Array.isArray(input) ? input.map(one) : one(input)) + "\n");
