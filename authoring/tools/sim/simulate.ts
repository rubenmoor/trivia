// Games per new player (plan 62, CT-2): plays engine games for one player until newGame's supply check fails.
// stdin: a cell {locale, bundles?, age_group?, mode?, player?, seeds?, seed?} or an array of cells; stdout: JSON.
import { readFileSync } from "node:fs";
import { GameError, STANDARD_JOKERS, answer, joker, newGame, pick, resolveChoice, view } from "../../../app/client/src/engine/game.ts";
import { seededRng } from "../../../app/client/src/engine/rng.ts";
import * as selection from "../../../app/client/src/engine/selection.ts";
import { emptySave, type EngineData, type GameState, type Io, type SaveData } from "../../../app/client/src/engine/state.ts";
import type { JokerName } from "../../../app/client/src/lib/types.ts";
import { loadData, type Loaded } from "./load.ts";

/** `typical`: p(correct) linear from level 1 to level 12. Only a model. */
export const TYPICAL_P = [0.95, 0.6] as const;
const NOW = "2026-01-01T00:00:00";
const NAME = "Sim";
const SIM_MODES = ["solo", "rr-coop"];

interface Cell {
  locale: string;
  bundles?: string[];
  age_group?: string;
  mode?: string;
  player?: "strong" | "typical";
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

/** First missing level of a supply_short, with the subcategories that ran dry at its range. */
function bottleneck(e: GameError, save: SaveData, data: EngineData, bundles: Set<string>): Bottleneck {
  const { level, lo, hi } = (e.params.levels as { level: number; lo: number; hi: number }[])[0];
  const left = selection.available(data.pool, save.burned.map((b) => b.question_id), [], bundles);
  const at = (qs: typeof data.pool) => new Set(qs.filter((q) => lo <= q.difficulty && q.difficulty <= hi).map((q) => q.subcategory));
  const had = at(selection.available(data.pool, [], [], bundles));
  const still = at(left);
  return { level, lo, hi, dry: [...had].filter((s) => s !== null && !still.has(s)) as string[] };
}

/** One seed: games until the supply check fails. */
function run(data: EngineData, cell: Cell, seed: number): { games: number; bottleneck: Bottleneck } {
  const io: Io = { rng: seededRng(seed), now: NOW };
  const rand = uniform(seed ^ 0x9e3779b9);
  const randInt = (n: number) => Math.floor(rand() * n);
  const args = { mode: "solo", age_group: cell.age_group, bundles: cell.bundles };
  const bundles = new Set(resolveChoice(data, args).bundles);
  let save = emptySave();
  for (let games = 0; ; games++) {
    let state: GameState;
    try {
      ({ save, state } = newGame(save, data, io, NAME, args));
    } catch (e) {
      if (e instanceof GameError && e.code === "supply_short") return { games, bottleneck: bottleneck(e, save, data, bundles) };
      throw e;
    }
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
    }
    // Finished games only slow every clone down; later games read the burns.
    save.games = [];
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
    .flatMap((c) => c.subcategories.filter((s) => s.available).map((s) => s.name)) ?? [];
  return subs.length ? { subcategory: subs[randInt(subs.length)] } : null;
}

function quantile(sorted: number[], q: number): number {
  const i = (sorted.length - 1) * q, lo = Math.floor(i);
  return sorted[lo] + (sorted[Math.ceil(i)] - sorted[lo]) * (i - lo);
}

function simulate(cell: Cell, loaded: Loaded) {
  const mode = cell.mode ?? "solo", player = cell.player ?? "typical";
  const head = { locale: cell.locale, bundles: cell.bundles ?? null, age_group: cell.age_group ?? null, mode, player };
  if (!loaded.ok) return { ...head, result: "no_pool", pool: loaded.pool };
  // rr-coop burns like solo (D-77); the engine runs it as solo.
  if (!SIM_MODES.includes(mode)) throw new Error(`mode ${mode} not simulated (${SIM_MODES.join(", ")})`);
  const t0 = performance.now();
  const base = cell.seed ?? 1, n = cell.seeds ?? 50;
  const runs = Array.from({ length: n }, (_, i) => ({ seed: base + i, ...run(loaded.data, { ...cell, player }, base + i) }));
  const games = runs.map((r) => r.games).sort((a, b) => a - b);
  const levels = new Map<number, number>();
  for (const r of runs) levels.set(r.bottleneck.level, (levels.get(r.bottleneck.level) ?? 0) + 1);
  const top = [...levels].sort((a, b) => b[1] - a[1] || a[0] - b[0])[0][0];
  const atTop = runs.filter((r) => r.bottleneck.level === top);
  const dry = new Map<string, number>();
  for (const r of atTop) for (const s of r.bottleneck.dry) dry.set(s, (dry.get(s) ?? 0) + 1);
  return {
    ...head, result: "ok", pool: loaded.pool, model: { typical_p: TYPICAL_P },
    games: { median: quantile(games, 0.5), p10: quantile(games, 0.1), min: games[0], max: games.at(-1) },
    bottleneck: {
      level: top, lo: atTop[0].bottleneck.lo, hi: atTop[0].bottleneck.hi, seeds: atTop.length,
      dry: [...dry].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0])).slice(0, 3).map(([s]) => s),
    },
    seeds: runs.map((r) => ({ seed: r.seed, games: r.games, bottleneck_level: r.bottleneck.level })),
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
