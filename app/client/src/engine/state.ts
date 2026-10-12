// The save document and transaction helpers of the TS referee (PORT-3, plan 20).
// SaveData = game.sqlite's tables as JSON; GameState = games.state (app/server/game.py docstring).
import type { Category, ErrorInfo, JokerBudget, JokerName, Supply } from "../lib/types.ts";
import type { PoolQuestion } from "./pool.ts";
import { broadOf, byId } from "./pool.ts";
import { pyRepr } from "./pycompat.ts";
import type { Rng } from "./rng.ts";

export const SAVE_VERSION = 1;

export interface SaveData {
  version: typeof SAVE_VERSION;
  players: PlayerRow[];
  games: GameRow[];
  burned: BurnRow[];
}

export interface PlayerRow {
  id: number;
  name: string;
  created_on: string;
}

export interface GameRow {
  id: number;
  started_on: string;
  finished_on: string | null;
  result: "won" | "lost" | "abandoned" | null;
  /** null only for games from before D-28. */
  player_id: number | null;
  state: GameState;
}

export interface BurnRow {
  question_id: string;
  /** null: burned for everyone (D-28). */
  player_id: number | null;
  game_id: number;
  burned_on: string;
}

export type Outcome = "skipped" | "easier" | "category" | "sniped" | "admin_skip" | "admin_burn";

/** An answered question has `correct`; a replaced or skipped one `outcome`. */
export interface HistoryEntry {
  level: number;
  question_id: string;
  correct?: boolean;
  outcome?: Outcome;
  /** Missing in games from before JK-2. */
  jokers?: JokerName[];
}

export interface LastAnswer {
  question_id: string;
  chosen: number;
  correct: boolean;
  correct_index: number;
}

export interface GameState {
  level: number;
  phase: "select" | "question" | "won" | "lost";
  options: string[];
  offered: string[];
  current: string | null;
  answers: string[];
  history: HistoryEntry[];
  last: LastAnswer | null;
  undo: GameState | null;
  purged: string[];
  hints_shown: number;
  struck: number[];
  jokers: JokerName[];
  swapped_to: string | null;
  repeat: boolean;
  settings: { jokers: JokerBudget };
}

export const UNLIMITED: JokerBudget = { hint: null, skip: null, easier: null, category: null, snipe: null };

export function emptySave(): SaveData {
  return { version: SAVE_VERSION, players: [], games: [], burned: [] };
}

/** Fill in the joker fields for games saved before JK-2 (game.with_defaults); mutates and returns. */
export function withDefaults(state: GameState): GameState {
  const s = state;
  s.purged ??= [];
  s.hints_shown ??= 0;
  s.struck ??= [];
  s.jokers ??= [];
  if (s.swapped_to === undefined) s.swapped_to = null;
  s.repeat ??= false;
  s.settings ??= {} as GameState["settings"];
  s.settings.jokers = { ...UNLIMITED, ...s.settings.jokers };
  return s;
}

/** INTEGER PRIMARY KEY without AUTOINCREMENT: max(id) + 1, 1 when empty. */
export function nextId(rows: { id: number }[]): number {
  return rows.reduce((m, r) => Math.max(m, r.id), 0) + 1;
}

// Error codes (D-57), as in game.py's ERRORS; English for logs.
type Params = Record<string, any>;
const ERRORS: Record<string, string | ((p: Params) => string)> = {
  name_missing: "player name missing",
  name_too_long: (p) => `name too long (at most ${p.max} letters)`,
  player_unknown: (p) => `no player ${pyRepr(String(p.name))}`,
  no_game: "no game is running",
  level_empty: (p) => `no questions left for level ${p.level} (difficulty ${p.lo}–${p.hi})`,
  supply_short: (p) =>
    "not enough questions: " +
    (p.levels as Params[]).map((l) => `level ${l.level} (difficulty ${l.lo}–${l.hi}): ${l.missing} missing`).join(", "),
  no_cards: "no cards on the table",
  card_invalid: (p) => `no card ${p.n}`,
  no_question: "no question to answer",
  answer_invalid: (p) => `no answer ${p.n}`,
  purge_short: "without this subcategory there are not enough questions",
  refill_empty: "no other question for this level",
  skip_not_question: "only a question on screen can be skipped",
  hints_used_up: "no hints left",
  easier_none: "no easier questions in this subcategory",
  category_unknown: "no such subcategory",
  category_same: "already in that subcategory",
  category_empty: "no questions of that subcategory for this level",
  category_none: "no questions of other subcategories for this level",
  snipe_last: "only one answer left",
  snipe_invalid: "can't aim at that answer",
  snipe_no_repeat: "if they hit the right one, there are no questions to repeat the level",
  budget_unknown_joker: "unknown joker in the budget",
  budget_invalid: "a budget is a count from 0 to 99, or null for unlimited",
  joker_unknown: (p) => `no joker ${pyRepr(String(p.joker))}`,
  joker_not_question: "jokers are only played on a question",
  joker_spent: (p) => `no ${p.joker} jokers left`,
  nothing_to_undo: "nothing to undo",
};

/** A request that doesn't fit the game's state: a code with params; `details` (a supply report) goes to the client. */
export class GameError extends Error {
  readonly code: string;
  readonly params: Params;
  readonly details: Supply | null;

  constructor(code: string, params: Params = {}, details: Supply | null = null) {
    const text = ERRORS[code];
    if (text === undefined) throw new Error(`unknown error code ${code}`);
    super(typeof text === "function" ? text(params) : text);
    this.code = code;
    this.params = params;
    this.details = details;
  }

  info(): ErrorInfo {
    return { code: this.code, params: this.params };
  }
}

/** Per action: the shuffles and the one timestamp all of the action's writes use. */
export interface Io {
  rng: Rng;
  now: string;
}

/** Per pool: built once by engineData. */
export interface EngineData {
  pool: PoolQuestion[];
  byId: Map<string, PoolQuestion>;
  categories: Category[];
  broad: Map<string, Category>;
}

export function engineData(pool: PoolQuestion[], categories: Category[]): EngineData {
  return { pool, byId: byId(pool), categories, broad: broadOf(categories) };
}

/** One transaction: fn mutates a copy; a throw (GameError → rollback) leaves `save` untouched. */
export function transact<T>(save: SaveData, fn: (work: SaveData) => T): { save: SaveData; result: T } {
  const work = structuredClone(save);
  const result = fn(work);
  return { save: work, result };
}

/** A savepoint: run fn on a copy of the working save, keep nothing; null if it works, else its error. */
export function trial(work: SaveData, fn: (copy: SaveData) => unknown): ErrorInfo | null {
  try {
    fn(structuredClone(work));
    return null;
  } catch (e) {
    if (e instanceof GameError) return e.info();
    throw e;
  }
}
