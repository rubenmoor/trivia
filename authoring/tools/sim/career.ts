// Career supply figures (milestone 20, plan 193): solo games of 1–N players taking turns on one save, the correct
// answers per category row × difficulty band. stdin: a cell {locale, age_group, player, players, seeds, games?, subjects?} or an array; stdout: JSON.
import { readFileSync } from "node:fs";
import { rangesFor } from "../../../app/client/src/engine/choice.ts";
import { GameError, resolveChoice } from "../../../app/client/src/engine/game.ts";
import { broadOf, categoryOf } from "../../../app/client/src/engine/pool.ts";
import { seededRng } from "../../../app/client/src/engine/rng.ts";
import { emptySave, newest, type EngineData, type GameState, type Io, type SaveData } from "../../../app/client/src/engine/state.ts";
import type { GameMode } from "../../../app/client/src/lib/types.ts";
import { loadData, type Loaded } from "./load.ts";
import { playSession, seenIds, uniform, type Cell, type Rand } from "./simulate.ts";

/** Difficulty bands of the career figures (inclusive): one place to change them. */
const BANDS: readonly (readonly [number, number])[] = [[1, 4], [5, 8], [9, 12], [13, 15]];
/** Correct-answer milestones. */
const MILESTONES = [25, 50, 100, 200] as const;
/** Sessions per seed. */
const MAX_GAMES = 100;
const ALL = "(all)";
const NOW = "2026-01-01T00:00:00";

interface CareerCell extends Cell {
  /** Category slug → subject; missing slugs are their own row. */
  subjects?: Record<string, string>;
  /** Sessions per seed. */
  games?: number;
}

const bandOf = (d: number): number => BANDS.findIndex(([lo, hi]) => lo <= d && d <= hi);
const median = (v: number[]): number => {
  const s = [...v].sort((a, b) => a - b), i = (s.length - 1) / 2;
  return (s[Math.floor(i)] + s[Math.ceil(i)]) / 2;
};
const finite = (x: number): number | null => (Number.isFinite(x) ? x : null);

/** key = `row|band|exact` or `row|band|harder` (this band or harder). */
const keysOf = (row: string, band: number): string[] =>
  [row, ALL].flatMap((r) => [`${r}|${band}|exact`, ...Array.from({ length: band + 1 }, (_, b) => `${r}|${b}|harder`)]);

/** One seat's history of a finished session: its correct answers. */
const correctOf = (state: GameState): string[] =>
  state.history.filter((h) => h.correct && h.outcome === undefined).map((h) => h.question_id);

interface Track {
  /** Correct answers per game, cumulative. */
  every: Map<string, number>;
  distinct: Map<string, Set<string>>;
  /** First game (1-based) reaching a milestone: `every.N` / `distinct.N`. */
  first: Map<string, number>;
  /** Distinct before the first repeat (set at that point). */
  atRepeat: Map<string, number> | null;
}

interface Seat {
  tracks: Track;
  games: number;
}

/** One seed on one save: per round each seat plays one solo game in turn (shared seen list); stops at the cap or
 * when the engine runs short. */
function runSeed(data: EngineData, cell: CareerCell, seed: number, rowOf: (id: string) => { row: string; band: number } | null) {
  const io: Io = { rng: seededRng(seed), now: NOW, ms: Date.parse(NOW) };
  const rand = uniform(seed ^ 0x9e3779b9);
  const r: Rand = { rand, randInt: (n) => Math.floor(rand() * n) };
  const players = cell.players ?? 1;
  const args = { mode: "solo" as GameMode, age_group: cell.age_group, bundles: cell.bundles };
  const solo = { ...cell, mode: "solo", players: 1 } as Cell;
  const seats: Seat[] = Array.from({ length: players }, () => ({ games: 0, tracks: { every: new Map(), distinct: new Map(), first: new Map(), atRepeat: null } }));
  let save: SaveData = { ...emptySave(), language: data.locale };
  let repeat: number | null = null;
  const max = cell.games ?? MAX_GAMES;
  rounds: for (let g = 1; g <= max; g++) {
    for (const [i, seat] of seats.entries()) {
      let got;
      try {
        ({ save, ...got } = playSession(save, data, io, r, [`Sim ${i + 1}`], args, solo, seenIds(save)));
      } catch (e) {
        if (e instanceof GameError && e.code === "supply_short") break rounds;
        throw e;
      }
      if (repeat === null && got.any !== null) {
        repeat = g;
        for (const s of seats) s.tracks.atRepeat = new Map([...s.tracks.distinct].map(([k, v]) => [k, v.size]));
      }
      const t = seat.tracks;
      seat.games = g;
      for (const id of correctOf(newest(save.games)!.state)) {
        const rb = rowOf(id);
        if (!rb) continue;
        for (const k of keysOf(rb.row, rb.band)) {
          t.every.set(k, (t.every.get(k) ?? 0) + 1);
          (t.distinct.get(k) ?? t.distinct.set(k, new Set()).get(k)!).add(id);
        }
      }
      for (const [k, n] of t.every) for (const m of MILESTONES) if (n >= m) t.first.has(`every.${m}|${k}`) || t.first.set(`every.${m}|${k}`, g);
      for (const [k, v] of t.distinct) for (const m of MILESTONES) if (v.size >= m) t.first.has(`distinct.${m}|${k}`) || t.first.set(`distinct.${m}|${k}`, g);
      save.games = []; // seen rows carry the counts
    }
  }
  return { seats, repeat };
}

function career(cell: CareerCell, loaded: Loaded) {
  const players = cell.players ?? 1;
  const head = { locale: cell.locale, age_group: cell.age_group ?? null, player: cell.player ?? "typical", players };
  if (!loaded.ok) return { ...head, result: "no_pool", pool: loaded.pool };
  const data = loaded.data;
  cell = { ...cell, bundles: cell.bundles ?? ["base"] };
  const choice = resolveChoice(data, { age_group: cell.age_group, bundles: cell.bundles });
  const bundles = new Set(choice.bundles);
  const cat = categoryOf(broadOf(data.categories));
  const rowFor = (q: { bundle?: string; subcategory?: string | null; difficulty: number }) => {
    const key = cat(q), b = bandOf(q.difficulty);
    if (key === null || b < 0) return null;
    const slug = key.includes("/") ? key.slice(key.indexOf("/") + 1) : key;
    return { row: cell.subjects?.[slug] ?? slug, band: b };
  };
  const inGame = data.pool.filter((q) => bundles.has(q.bundle ?? "base"));
  const rowById = new Map(inGame.map((q) => [q.id, rowFor(q)] as const));
  const lookup = (id: string) => rowById.get(id) ?? null;
  const runs = Array.from({ length: cell.seeds ?? 3 }, (_, i) => runSeed(data, { ...cell, player: head.player as "strong" | "typical" }, (cell.seed ?? 1) + i, lookup));
  const keys = new Set<string>();
  for (const q of inGame) { const x = rowFor(q); if (x) keysOf(x.row, x.band).forEach((k) => keys.add(k)); }
  const staticCount = new Map<string, number>();
  for (const q of inGame) { const x = rowFor(q); if (x) for (const k of keysOf(x.row, x.band)) staticCount.set(k, (staticCount.get(k) ?? 0) + 1); }
  const seats = runs.flatMap((r) => r.seats.filter((s) => s.games > 0));
  const figures = [...keys].sort().map((k) => {
    const [row, band, incl] = k.split("|");
    const reach = (kind: "every" | "distinct", m: number) =>
      finite(median(seats.map((s) => s.tracks.first.get(`${kind}.${m}|${k}`) ?? Infinity)));
    return {
      row, band: Number(band), incl, static: staticCount.get(k) ?? 0,
      per_game: seats.reduce((a, s) => a + (s.tracks.every.get(k) ?? 0) / s.games, 0) / seats.length,
      distinct_before_repeat: median(seats.map((s) => (s.tracks.atRepeat ? s.tracks.atRepeat.get(k) : s.tracks.distinct.get(k)?.size) ?? 0)),
      games_to: Object.fromEntries(MILESTONES.map((m) => [m, { every: reach("every", m), distinct: reach("distinct", m) }])),
    };
  });
  return {
    ...head, result: "ok", pool: loaded.pool, bundles: choice.bundles, bands: BANDS, milestones: MILESTONES, max_games: cell.games ?? MAX_GAMES,
    ranges: rangesFor(data, choice), repeat_game: finite(median(runs.map((r) => r.repeat ?? Infinity))), figures,
  };
}

if (import.meta.filename === process.argv[1]) {
  const input = JSON.parse(readFileSync(0, "utf8")) as CareerCell | CareerCell[];
  const cache = new Map<string, Loaded>();
  const one = (c: CareerCell) => {
    if (!cache.has(c.locale)) cache.set(c.locale, loadData(c.locale));
    return career(c, cache.get(c.locale)!);
  };
  process.stdout.write(JSON.stringify(Array.isArray(input) ? input.map(one) : one(input)) + "\n");
}
