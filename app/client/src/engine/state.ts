// The save document and transaction helpers of the TS referee (PORT-3, plan 20).
// SaveData = game.sqlite's tables as JSON plus flags (plan 49); GameState = games.state (app/server/game.py docstring).
import type { Category, Difficulty, ErrorInfo, GameMode, JokerBudget, JokerName, Language, Supply } from "../lib/types.ts";
import type { AgeGroup, Bundle, PoolQuestion } from "./pool.ts";
import { broadOf, byId } from "./pool.ts";
import { pyRepr } from "./pycompat.ts";
import type { Rng } from "./rng.ts";

export const SAVE_VERSION = 3;

export type { Language };

export interface SaveData {
  version: typeof SAVE_VERSION;
  players: PlayerRow[];
  games: GameRow[];
  /** One row per seen event (plan 65); count(q) = rows for q, for the whole save. Since version 3. */
  seen: SeenRow[];
  /** «Bloquear pregunta»: never offered again. Since version 3. */
  blocked: string[];
  /** Exhausted subcategories already shown at game start. Since version 3. */
  notified_exhausted: string[];
  /** Questions flagged for review (GM-5, D-47); keyed by question ID. */
  flags: Record<string, FlagEntry>;
  /** «Reportar pregunta» (MD-6): log only; since version 2. */
  reports: ReportRow[];
  /** UI and question language (plan 68); parseSave fills {es, es}, a fresh save gets defaultLanguage(). */
  language?: Language;
}

/** The family's language: what a save from before plan 68 plays in. */
export const SPANISH: Language = { ui: "es", questions: "es" };

export interface ReportRow {
  question_id: string;
  game_id: number;
  player_id: number | null;
  level: number;
  reported_on: string;
  note?: string;
}

export interface FlagEntry {
  flagged_on: string;
  player: string | null;
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
  /** The question locale the game plays in (plan 68); missing = es. */
  locale?: string;
  state: GameState;
}

export const gameLocale = (row: GameRow): string => row.locale ?? "es";

export interface SeenRow {
  question_id: string;
  /** 0: the game was deleted (GF-7); game IDs get reused. */
  game_id: number;
  seen_on: string;
}

/** `admin_burn`: «Saltar y quemar para todos» in games from before plan 65. */
export type Outcome = "skipped" | "easier" | "category" | "sniped" | "admin_skip" | "admin_block" | "admin_burn";

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
  /** age_group / bundles / mode: only when the new game's request carried them (plan 27, plan 36);
   * missing mode = gamemaster. `customized`: outside gamemaster mode only. D-88: `difficulty` (then no
   * age_group), `levels` (missing 12), `cards` (missing 4), `video` / `audio` (only false; missing = allowed). */
  settings: {
    jokers: JokerBudget; age_group?: string; bundles?: string[]; mode?: GameMode; customized?: boolean;
    difficulty?: Difficulty; levels?: number; cards?: number; video?: false; audio?: false;
  };
}

export const UNLIMITED: JokerBudget = { hint: null, skip: null, easier: null, category: null, snipe: null };

export function emptySave(): SaveData {
  return { version: SAVE_VERSION, players: [], games: [], seen: [], blocked: [], notified_exhausted: [], flags: {}, reports: [] };
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
  age_group_unknown: (p) => `unknown age group ${pyRepr(String(p.group))}`,
  bundle_unknown: (p) => `unknown bundle ${pyRepr(String(p.bundle))}`,
  bundles_not_list: "bundles must be a list",
  bundle_not_offered: (p) => `bundle ${pyRepr(String(p.bundle))} isn't offered in ${p.locale}`,
  base_bundle_count: "pick exactly one base bundle",
  difficulty_invalid: "a custom difficulty is {start, end}, whole numbers 1–15, end ≥ start, without an age group",
  levels_invalid: (p) => `levels: a whole number ${p.min}–${p.max}`,
  cards_invalid: (p) => `cards per level: a whole number ${p.min}–${p.max}`,
  switch_invalid: (p) => `${p.field} is true or false`,
  mode_unknown: (p) => `unknown mode ${pyRepr(String(p.mode))}`,
  mode_not_built: (p) => `mode ${pyRepr(String(p.mode))} isn't playable yet`,
  gamemaster_only: (p) => `${p.action} only in gamemaster mode`,
  note_invalid: "a note is text of at most 500 letters",
  language_unknown: (p) => `no ${p.kind} language ${pyRepr(String(p.lang))}`,
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

/** Display names of one locale (D-81): base's names file merged with every bundle's. */
export interface Names {
  bundles: Record<string, { name: string; description?: string }>;
  categories: Record<string, string>;
  subcategories: Record<string, string>;
}

/** Per pool: built once by engineData. */
export interface EngineData {
  /** The question locale of `pool` (plan 68). */
  locale: string;
  /** Empty for es: the keys are the Spanish names. */
  names: Names;
  pool: PoolQuestion[];
  byId: Map<string, PoolQuestion>;
  categories: Category[];
  broad: Map<string, Category>;
  bundles: Bundle[];
  ageGroups: AgeGroup[];
  groupById: Map<string, AgeGroup>;
}

export const NO_NAMES: Names = { bundles: {}, categories: {}, subcategories: {} };

export function engineData(
  pool: PoolQuestion[], categories: Category[], bundles: Bundle[], ageGroups: AgeGroup[],
  locale = "es", names: Names = NO_NAMES,
): EngineData {
  return {
    locale, names, pool, byId: byId(pool), categories, broad: broadOf(categories),
    bundles, ageGroups, groupById: new Map(ageGroups.map((g) => [g.id, g])),
  };
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
