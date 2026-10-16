// Games per new player (plan 62, CT-2; plan 65): engine sessions on one save until the first repeat (a seen card offered).
// stdin: a cell {locale, bundles?, age_group?, mode?, player?, players?, seeds?, seed?} or an array of cells; stdout: JSON.
import { readFileSync } from "node:fs";
import { rangesFor } from "../../../app/client/src/engine/choice.ts";
import {
  GameError, MODES, STANDARD_JOKERS, answer, claim, joker, newGame, newSession, pick, resolveChoice, show, view, type ChoiceArgs,
} from "../../../app/client/src/engine/game.ts";
import { outlook } from "../../../app/client/src/engine/outlook.ts";
import { subOf } from "../../../app/client/src/engine/pool.ts";
import { seededRng } from "../../../app/client/src/engine/rng.ts";
import * as selection from "../../../app/client/src/engine/selection.ts";
import { emptySave, newest, rowStates, type EngineData, type GameRow, type GameState, type Io, type SaveData } from "../../../app/client/src/engine/state.ts";
import type { GameMode, JokerName } from "../../../app/client/src/lib/types.ts";
import { loadData, type Loaded } from "./load.ts";

/** `typical`: p(correct) linear from level 1 to level 12. Only a model. */
const TYPICAL_P = [0.95, 0.6] as const;
const NOW = "2026-01-01T00:00:00";
const NAME = "Sim";
/** Time between two engine actions: inside every timed deadline. */
const STEP_MS = 1000;
const SIM_MODES: readonly string[] = MODES.filter((m) => m !== "gamemaster"); // = qgen.SIM_MODES
const MULTI = ["rr-coop", "rr-competitive", "timed"]; // = qgen.SIM_MULTI
/** Runs stop here if no repeat came yet (`capped`). */
const MAX_GAMES = 500;

interface Cell {
  locale: string;
  bundles?: string[];
  age_group?: string;
  mode?: string;
  player?: "strong" | "typical";
  /** Sessions: default 4. */
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

/** The level with the subcategories (keys) whose questions at its range were all seen. */
function dryAt(level: number, lo: number, hi: number, seen: Set<string>, data: EngineData, bundles: Set<string>): Bottleneck {
  const at = (qs: typeof data.pool) => new Set(qs.filter((q) => lo <= q.difficulty && q.difficulty <= hi).map(subOf));
  const all = selection.available(data.pool, [], [], bundles);
  const had = at(all);
  const still = at(all.filter((q) => !seen.has(q.id)));
  return { level, lo, hi, dry: [...had].filter((s): s is string => s !== null && !still.has(s)) };
}

type Rand = { rand: () => number; randInt: (n: number) => number };
/** `games`: until the first repeat (Cambiazo's cards too); `draw`: until the first in a level draw, with its bottleneck. */
type Run = { games: number; cambiazo: boolean; draw: number; capped: boolean; bottleneck: Bottleneck };
const NONE: Bottleneck = { level: 0, lo: 0, hi: 0, dry: [] };

/** Ids with a seen row. */
const seenIds = (save: SaveData) => new Set(save.seen.map((s) => s.question_id));

/** One seed on one save: sessions until the first that offers a seen card (count ≥ 1), and until the first
 * whose level draw does; at most MAX_GAMES. */
function run(data: EngineData, cell: Cell, seed: number): Run {
  const io: Io = { rng: seededRng(seed), now: NOW, ms: Date.parse(NOW) };
  const rand = uniform(seed ^ 0x9e3779b9);
  const r: Rand = { rand, randInt: (n) => Math.floor(rand() * n) };
  const args = { mode: cell.mode as GameMode, age_group: cell.age_group, bundles: cell.bundles };
  const choice = resolveChoice(data, args);
  const bundles = new Set(choice.bundles);
  const ranges = rangesFor(data, choice);
  const names = cell.mode === "solo" ? [NAME] : Array.from({ length: cell.players! }, (_, i) => `${NAME} ${i + 1}`);
  let save: SaveData = { ...emptySave(), language: data.locale };
  let first: { games: number; cambiazo: boolean } | null = null;
  for (let games = 0; games < MAX_GAMES; games++) {
    const before = seenIds(save);
    let got: Repeats;
    try {
      ({ save, ...got } = playSession(save, data, io, r, names, args, cell, before));
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
    // Finished sessions only slow every clone down; seen rows carry the counts.
    save.games = [];
  }
  return { ...(first ?? { games: MAX_GAMES, cambiazo: false }), draw: MAX_GAMES, capped: true, bottleneck: NONE };
}

/** First level that offered a seen card: any card, a level-draw card (not Cambiazo's); null = none. */
type Repeats = { any: number | null; draw: number | null };

/** One session's working set; `save` moves on with every action. */
interface Sim {
  save: SaveData;
  data: EngineData;
  io: Io;
  r: Rand;
  cell: Cell;
  check: (cambiazo?: boolean) => void;
}

const rowOf = (s: Sim): GameRow => newest(s.save.games)!;

/** One engine action, `STEP_MS` after the previous one. */
function act(s: Sim, fn: (save: SaveData) => { save: SaveData }): void {
  s.io.ms! += STEP_MS;
  s.save = fn(s.save).save;
}

/** One engine session from `new` to its end (solo: one game), with its repeats of `seen`; `new`'s GameError passes
 * through. */
function playSession(
  save: SaveData, data: EngineData, io: Io, r: Rand, names: string[], args: ChoiceArgs, cell: Cell, seen: Set<string>,
): { save: SaveData } & Repeats {
  const reps: Repeats = { any: null, draw: null };
  const done: number[] = [];
  const s: Sim = { save, data, io, r, cell, check: () => {} };
  s.check = (cambiazo = false) => rowStates(rowOf(s)).forEach((st, i) => {
    if (st.offered.slice(done[i] ?? 0).some((id) => seen.has(id))) {
      reps.any ??= st.level;
      if (!cambiazo) reps.draw ??= st.level;
    }
    done[i] = st.offered.length;
  });
  act(s, (sv) => (cell.mode === "solo" ? newGame(sv, data, io, names[0], args) : newSession(sv, data, io, names, args)));
  s.check();
  if (cell.mode === "timed") playTimed(s);
  else playTurns(s);
  return { save: s.save, ...reps };
}

/** The question's correct index, or a random wrong one not struck. */
function chosen(data: EngineData, state: GameState, right: boolean, randInt: (n: number) => number): number {
  const correct = state.answers.indexOf(data.byId.get(state.current!)!.answer);
  const wrong = state.answers.map((_, i) => i).filter((i) => i !== correct && !state.struck.includes(i));
  return right ? correct : wrong[randInt(wrong.length)];
}

/** solo, rr-coop, rr-competitive: the seat on turn picks, plays its due jokers, answers. Each joker of a game's
 * standard set once, at a random level (rr-coop: the team's one set); a refused one is skipped. */
function playTurns(s: Sim): void {
  const { data, io, r: { rand, randInt } } = s;
  const plan = () => (Object.entries(STANDARD_JOKERS) as [JokerName, number | null][])
    .flatMap(([j, n]) => Array.from({ length: n ?? 0 }, () => ({ joker: j, level: 1 + randInt(selection.LEVELS) })));
  const perSeat = rowOf(s).state.settings.mode === "rr-competitive";
  const pending = perSeat ? rowOf(s).seats!.map(plan) : [plan()];
  const turn = () => {
    const row = rowOf(s), seat = row.seats ? row.turn! : undefined;
    return { seat, state: row.seats?.[seat!].state ?? row.state };
  };
  while (rowOf(s).result === null) {
    const { seat, state: before } = turn();
    if (before.phase === "select") act(s, (sv) => pick(sv, data, io, randInt(before.options.length), seat));
    let { state } = turn();
    const own = pending[perSeat ? seat! : 0];
    for (const p of own.filter((p) => p.level === state.level)) {
      own.splice(own.indexOf(p), 1);
      const jargs = jokerArgs(p.joker, s.save, data, io, state, randInt);
      if (jargs === null) continue;
      try {
        act(s, (sv) => joker(sv, data, io, p.joker, jargs, seat));
        s.check(p.joker === "category");
      } catch (e) {
        if (!(e instanceof GameError)) throw e;
      }
      ({ state } = turn());
      if (state.phase !== "question") break;
    }
    if (state.phase !== "question") continue;
    const right = s.cell.player === "strong" || rand() < pCorrect(state.level);
    act(s, (sv) => answer(sv, data, io, chosen(data, state, right, randInt), seat));
    s.check();
  }
}

/** timed: each question shown, claimed by a random seat still in, answered right with pCorrect (strong: always, so
 * round 12 ends it); the clock never runs out. */
function playTimed(s: Sim): void {
  const { data, io, r: { rand, randInt } } = s;
  while (rowOf(s).result === null) {
    const row = rowOf(s);
    if (row.state.timed!.shown_at === null) {
      act(s, (sv) => show(sv, data, io));
      continue;
    }
    const seats = row.seats!.flatMap((x, i) => (x.out ? [] : [i]));
    const seat = seats[randInt(seats.length)];
    act(s, (sv) => claim(sv, data, io, seat));
    const state = rowOf(s).state;
    const right = s.cell.player === "strong" || rand() < pCorrect(state.level);
    act(s, (sv) => answer(sv, data, io, chosen(data, state, right, randInt), seat));
    s.check();
  }
}

/** Arguments for a joker, or null to skip it: Cambiazo takes a random subcategory the engine allows. */
function jokerArgs(name: JokerName, save: SaveData, data: EngineData, io: Io, state: GameState, randInt: (n: number) => number) {
  if (name === "snipe") {
    const open = state.answers.map((_, i) => i).filter((i) => !state.struck.includes(i));
    return { index: open[randInt(open.length)] };
  }
  if (name !== "category") return {};
  const subs = view(save, data, io)?.jokers?.category.categories
    .flatMap((c) => c.subcategories.filter((s) => s.available).map((s) => s.key)) ?? [];
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
