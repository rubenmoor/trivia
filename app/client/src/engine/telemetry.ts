// Opt-in telemetry (plan 106, decision 119): this run's games from the save → plan 105's contract games.
import type { Difficulty, JokerName } from "../lib/types.ts";
import { gameChoice, JOKERS } from "./choice.ts";
import { isOurs } from "./pool.ts";
import { gameLocale, type EngineData, type GameRow, type SaveData } from "./state.ts";

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
  result: "won" | "lost" | "abandoned" | "open";
  customized: boolean;
  mods: boolean;
  jokers: Record<JokerName, number>;
  answers: TelemetryAnswer[];
}

/** `key` = `<game id>@<started_on>`; `from`: first history entry of this session. */
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

export const gameKey = (row: GameRow): string => `${row.id}@${row.started_on}`;

/** Snapshot at session start: every game known then; running ones keep their history length. */
export function telemetryStart(save: SaveData): TelemetryStart {
  return new Map(save.games.map((r) => [gameKey(r), r.result === null ? r.state.history.length : -1]));
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
export function telemetryGame(row: GameRow, from: number, data: EngineData, mods: boolean): TelemetryGame {
  const { state } = row;
  const choice = gameChoice(state, data);
  const levels = state.settings.levels ?? 12;
  const slice = state.history.slice(from);
  const jokers = Object.fromEntries(JOKERS.map((j) => [j, 0])) as Record<JokerName, number>;
  for (const j of [...slice.flatMap((h) => h.jokers ?? []), ...(state.jokers ?? [])]) jokers[j] = (jokers[j] ?? 0) + 1;
  const answers = slice
    .filter((h) => h.correct !== undefined && h.level >= 1 && h.level <= levels && ourQuestion(h.question_id, data))
    .slice(0, MAX_GAME_ANSWERS)
    .map((h) => ({ question: h.question_id, level: h.level, correct: h.correct!, jokers: counts(h.jokers) }));
  return {
    mode: state.settings.mode ?? "gamemaster",
    locale: gameLocale(row),
    pool: data.poolHash,
    age_group: choice.age_group,
    difficulty: choice.difficulty,
    levels,
    reached: row.result === "won" ? levels : state.level,
    result: row.result ?? "open",
    customized: state.settings.customized ?? false,
    mods,
    jokers,
    answers,
  };
}

/** The session's rows: those already recorded (row null when gone), then rows new since `start` (from 0)
 * and those running at `start` (from its length). */
export function sessionRows(save: SaveData, prev: Telemetry, start: TelemetryStart): { key: string; from: number; row: GameRow | null }[] {
  const rows = new Map(save.games.map((r) => [gameKey(r), r]));
  const out = prev.index.map(({ key, from }) => ({ key, from, row: rows.get(key) ?? null }));
  const known = new Set(prev.index.map((e) => e.key));
  for (const [key, row] of rows) {
    const from = start.get(key) ?? 0;
    if (!known.has(key) && from >= 0) out.push({ key, from, row });
  }
  return out;
}

/** Rebuilds every session row; a recorded game whose row is gone stays as it was. `data`: per game locale. */
export function buildTelemetry(save: SaveData, prev: Telemetry, start: TelemetryStart, data: ReadonlyMap<string, EngineData>, mods: boolean): Telemetry {
  const out: Telemetry = { games: [], index: [] };
  sessionRows(save, prev, start).forEach(({ key, from, row }, i) => {
    out.games.push(row ? telemetryGame(row, from, data.get(gameLocale(row))!, mods) : prev.games[i]!);
    out.index.push({ key, from });
  });
  return out;
}
