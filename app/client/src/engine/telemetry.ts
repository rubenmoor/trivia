// Opt-in telemetry (plan 106, decision 119): this run's games from the save → plan 105's contract games.
import type { Difficulty, JokerName } from "../lib/types.ts";
import { gameChoice, JOKERS } from "./choice.ts";
import { gameMode } from "./game.ts";
import { isOurs } from "./pool.ts";
import { LEVELS } from "./selection.ts";
import { gameLocale, rowPlayers, seatResult, type EngineData, type GameRow, type GameState, type SaveData } from "./state.ts";

export interface TelemetryAnswer {
  question: string;
  level: number;
  correct: boolean;
  jokers: Partial<Record<JokerName, number>>;
}

export interface TelemetryGame {
  mode: string;
  locale: string;
  pool: string | null;
  age_group: string | null;
  difficulty: Difficulty | null;
  levels: number;
  reached: number;
  result: "won" | "lost" | "completed" | "abandoned" | "open";
  customized: boolean;
  mods: boolean;
  /** Seats in the session; 1 for solo and gamemaster (decision 286). */
  players: number;
  jokers: Record<JokerName, number>;
  answers: TelemetryAnswer[];
}

/** `key` = `<game id>@<started_on>`, rr-competitive `…#<seat>`; `from`: first history entry of this session. */
export interface TelemetryIndex {
  key: string;
  from: number;
}

export interface Telemetry {
  games: TelemetryGame[];
  index: TelemetryIndex[];
}

/** History length per game key when the session began; running games only count. */
export type TelemetryStart = Map<string, number>;

const MAX_GAME_ANSWERS = 100;

const gameKey = (row: GameRow): string => `${row.id}@${row.started_on}`;

/** A telemetry game's source: a row, or one seat of an rr-competitive session (decision 286). */
interface Unit {
  key: string;
  row: GameRow;
  seat?: number;
}

const units = (row: GameRow): Unit[] =>
  row.state.settings.mode === "rr-competitive" && row.seats
    ? row.seats.flatMap((s, seat) => (s.state ? [{ key: `${gameKey(row)}#${seat}`, row, seat }] : []))
    : [{ key: gameKey(row), row }];

const unitState = ({ row, seat }: Unit): GameState => (seat === undefined ? row.state : row.seats![seat]!.state!);

/** Snapshot at session start: every game known then; running ones keep their history length. */
export function telemetryStart(save: SaveData): TelemetryStart {
  return new Map(save.games.flatMap(units).map((u) => [u.key, u.row.result === null ? unitState(u).history.length : -1]));
}

function counts(jokers: readonly JokerName[] | undefined): Partial<Record<JokerName, number>> {
  const out: Partial<Record<JokerName, number>> = {};
  for (const j of jokers ?? []) out[j] = (out[j] ?? 0) + 1;
  return out;
}

/** Ours and shipped; mod questions never (decision 128). */
function ourQuestion(id: string, data: EngineData): boolean {
  const bundle = isOurs(id) ? data.byId.get(id)?.bundle : undefined;
  return bundle !== undefined && data.bundles.some((b) => b.id === bundle);
}

/** `mods`: this run's overlay isn't empty (decision 146). */
function telemetryGame(u: Unit, from: number, data: EngineData, mods: boolean): TelemetryGame {
  const { row } = u;
  const state = unitState(u);
  const mode = row.state.settings.mode ?? gameMode(row.state);
  const result = u.seat === undefined ? row.result : seatResult(row, u.seat);
  const timed = mode === "timed";
  const choice = gameChoice(state, data);
  const levels = state.settings.levels ?? LEVELS;
  const slice = state.history.slice(from);
  const jokers = Object.fromEntries(JOKERS.map((j) => [j, 0])) as Record<JokerName, number>;
  if (!timed) for (const j of [...slice.flatMap((h) => h.jokers ?? []), ...(state.jokers ?? [])]) jokers[j]++;
  const answers = slice
    .filter((h) => h.correct !== undefined && h.level >= 1 && h.level <= levels && ourQuestion(h.question_id, data))
    .slice(0, MAX_GAME_ANSWERS)
    .map((h) => ({ question: h.question_id, level: h.level, correct: h.correct!, jokers: counts(h.jokers) }));
  return {
    mode,
    locale: gameLocale(row),
    pool: data.poolHash,
    age_group: choice.age_group,
    difficulty: choice.difficulty,
    levels,
    reached: result === "won" || result === "completed" ? levels : state.level,
    result: result ?? "open",
    customized: state.settings.customized ?? false,
    mods,
    players: rowPlayers(row).length,
    jokers,
    answers,
  };
}

/** The session's games: those already recorded (row null when gone), then new since `start` (from 0)
 * and those running at `start` (from its length). */
export function sessionRows(save: SaveData, prev: Telemetry, start: TelemetryStart): { key: string; from: number; unit: Unit | null }[] {
  const all = new Map(save.games.flatMap(units).map((u) => [u.key, u]));
  const out = prev.index.map(({ key, from }) => ({ key, from, unit: all.get(key) ?? null }));
  const known = new Set(prev.index.map((e) => e.key));
  for (const [key, unit] of all) {
    const from = start.get(key) ?? 0;
    if (!known.has(key) && from >= 0) out.push({ key, from, unit });
  }
  return out;
}

/** Rebuilds every session game; a recorded game whose row is gone stays as it was. `data`: per game locale. */
export function buildTelemetry(save: SaveData, prev: Telemetry, start: TelemetryStart, data: ReadonlyMap<string, EngineData>, mods: boolean): Telemetry {
  const out: Telemetry = { games: [], index: [] };
  sessionRows(save, prev, start).forEach(({ key, from, unit }, i) => {
    out.games.push(unit ? telemetryGame(unit, from, data.get(gameLocale(unit.row))!, mods) : prev.games[i]!);
    out.index.push({ key, from });
  });
  return out;
}
