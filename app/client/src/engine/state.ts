// The save document and transaction helpers of the TS referee (PORT-3, plan 20).
// SaveData = game.sqlite's tables as JSON plus flags (plan 49); GameState = games.state of the former Python referee.
import type { Category, Difficulty, ErrorInfo, GameMode, JokerBudget, JokerName, Language, SeatDevice, Supply } from "../lib/types.ts";
import type { AgeGroup, Bundle, PoolQuestion } from "./pool.ts";
import { broadOf, byId, subKey } from "./pool.ts";
import { pyRepr } from "./pycompat.ts";
import type { Rng } from "./rng.ts";

export const SAVE_VERSION = 5; // bump authoring/tools/save_file.py's upgrades too (and app/server/save.py VERSION/LISTS until task 765)

export type { Language };

export interface SaveData {
  version: typeof SAVE_VERSION;
  players: PlayerRow[];
  games: GameRow[];
  /** One row per seen event (plan 65); count(q) = rows for q, for the whole save. Since version 3. */
  seen: SeenRow[];
  /** «Bloquear pregunta»: never offered again. Since version 3. */
  blocked: string[];
  /** Bundles already shown as running out at game start (task 1104; subcategory keys before, pruned). Since version 3. */
  notified_exhausted: string[];
  /** Questions flagged for review (GM-5, D-47); keyed by question ID. Version 4 merged `reports` in (decision 60). */
  flags: Record<string, FlagEntry>;
  /** UI and question language (plan 126); parseSave fills es, a fresh save gets defaultLanguage(). */
  language?: Language;
}

/** The family's language: what a save from before plan 68 plays in. */
export const SPANISH: Language = "es";

export interface FlagEntry {
  flagged_on: string;
  player: string | null;
  /** Missing in flags from before version 4. */
  level?: number;
  note?: string;
  /** The game's question locale (decision 102); missing = es. */
  locale?: string;
  /** The question as the player saw it, in `locale` (decision 102); missing in older flags. */
  shown?: FlagText;
  /** Last successful report send (plan 93); additive, no version bump. */
  reported_on?: string;
}

export interface FlagText {
  question: string;
  answer: string;
  wrong_answers: string[];
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
  /** `completed`: the last level reached by reveals (D-105), neither won nor lost. */
  result: "won" | "lost" | "completed" | "abandoned" | null;
  /** null: games before D-28 or a multiplayer session. */
  player_id: number | null;
  /** A multiplayer session (milestone 16), join order; missing = a one-player game (`player_id`). Since version 5. */
  seats?: Seat[];
  /** Seat index on turn (round-robin modes); missing outside them. */
  turn?: number;
  /** The question locale the game plays in (plan 68); missing = es. */
  locale?: string;
  state: GameState;
}

/** One player of a session. `state`: rr-competitive's own game; `lives` / `out`: timed (`out` also rr-competitive's wrong answer). */
export interface Seat {
  /** null after the player was deleted. */
  player_id: number | null;
  state?: GameState;
  lives?: number;
  out?: true;
  result?: "won" | "lost";
  /** The seat's controls (plan 172); missing on older rows. */
  device?: SeatDevice;
}

export const isSeatDevice = (v: unknown): v is SeatDevice =>
  v === "pad" || v === "kbm" || v === "shared"
  || (typeof v === "object" && v !== null && !Array.isArray(v) && Object.keys(v).length === 1 && typeof (v as { key?: unknown }).key === "string" && (v as { key: string }).key !== "");

/** The players of a row, in seat order (a one-player game: its player). */
export const rowPlayers = (row: GameRow): (number | null)[] => row.seats?.map((s) => s.player_id) ?? [row.player_id];

/** Every game state of a row: rr-competitive's seats' own, else the row's. */
export const rowStates = (row: GameRow): GameState[] =>
  row.state.settings.mode === "rr-competitive" && row.seats ? row.seats.flatMap((s) => (s.state ? [s.state] : [])) : [row.state];

/** A seat's outcome: its own, else the row's (rr-coop). */
export const seatResult = (row: GameRow, i: number): GameRow["result"] => row.seats?.[i]?.result ?? row.result;

export const gameLocale = (row: GameRow): string => row.locale ?? "es";

/** The game with the highest id, or null. */
export const newest = (games: readonly GameRow[]): GameRow | null =>
  games.reduce<GameRow | null>((m, g) => (m === null || g.id > m.id ? g : m), null);

interface SeenRow {
  question_id: string;
  /** 0: the game was deleted (GF-7); game IDs get reused. */
  game_id: number;
  seen_on: string;
}

/** `admin_burn`: «Saltar y quemar para todos» in games from before plan 65. */
export type Outcome = "skipped" | "easier" | "category" | "sniped" | "admin_skip" | "admin_block" | "admin_burn" | "admin_replace";

/** An answered question has `correct`; a revealed one `revealed` (D-105); a replaced or skipped one `outcome`. */
interface HistoryEntry {
  level: number;
  question_id: string;
  correct?: boolean;
  revealed?: true;
  outcome?: Outcome;
  /** Missing in games from before JK-2. */
  jokers?: JokerName[];
  /** Who answered (sessions); missing = the row's one player. */
  seat?: number;
  /** timed (plan 159): the answer picked (null: none), hints shown by then; a claim run out or nobody claimed. */
  chosen?: number | null;
  hints?: number;
  timeout?: true;
  unclaimed?: true;
}

/** A reveal (D-105): `chosen` null, `correct` false, `revealed`. */
interface LastAnswer {
  question_id: string;
  chosen: number | null;
  correct: boolean;
  revealed?: true;
  correct_index: number;
  /** In a session: who answered. */
  seat?: number;
  /** timed: the claim ran out, or nobody claimed (`chosen` null, `correct` false). */
  timeout?: true;
  unclaimed?: true;
}

/** Competitive timed's shared question flow (plan 159); times in epoch ms. */
export interface TimedState {
  /** Seats in at the round's start (decision 276). */
  round_size: number;
  round_done: number;
  /** Seats with a correct answer this round. */
  round_correct: number[];
  /** null: drawn, not on screen yet (decision 296). */
  shown_at: number | null;
  claim: { seat: number; at: number } | null;
  paused_at: number | null;
  /** Extra sudden-death rounds at the last level (decision 281). */
  repeat: number;
}

export interface GameState {
  level: number;
  phase: "select" | "question" | "won" | "lost" | "completed";
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
  /** timed only. */
  timed?: TimedState;
  /** age_group / bundles / mode: only when the new game's request carried them (plan 27, plan 36);
   * missing mode = gamemaster. `customized`: outside gamemaster mode only. D-88: `difficulty` (then no
   * age_group), `levels` (missing 12), `cards` (missing 4), `video` / `audio` (only false; missing = allowed); D-105: `answers` (only false; missing = on). */
  settings: {
    jokers: JokerBudget; age_group?: string; bundles?: string[]; mode?: GameMode; customized?: boolean;
    difficulty?: Difficulty; levels?: number; cards?: number; video?: false; audio?: false; answers?: false;
  };
}

export const UNLIMITED: JokerBudget = { hint: null, skip: null, easier: null, category: null, snipe: null };

export function emptySave(): SaveData {
  return { version: SAVE_VERSION, players: [], games: [], seen: [], blocked: [], notified_exhausted: [], flags: {} };
}

/** Fill in the joker fields for games saved before JK-2 (game.with_defaults); mutates and returns. */
export function withDefaults(s: GameState): GameState {
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

// Error codes (D-57), as in the former game.py's ERRORS; English for logs.
type Params = Record<string, unknown>;
const ERRORS: Record<string, string | ((p: Params) => string)> = {
  name_missing: "player name missing",
  name_too_long: (p) => `name too long (at most ${p.max} letters)`,
  player_unknown: (p) => `no player ${pyRepr(String(p.name))}`,
  no_game: "no game is running",
  level_empty: (p) => `no questions left for level ${p.level} (difficulty ${p.lo}–${p.hi})`,
  supply_short: (p) =>
    "not enough questions: " +
    (p.levels as Params[]).map((l) => `${l.seat === undefined ? "" : `seat ${l.seat} `}level ${l.level} (difficulty ${l.lo}–${l.hi}): ${l.missing} missing`).join(", "),
  no_questions: "no question for this choice",
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
  difficulty_invalid: "a custom difficulty is {start, end}, whole numbers 1–15, end ≥ start, without an age group",
  levels_invalid: (p) => `levels: a whole number ${p.min}–${p.max}`,
  cards_invalid: (p) => `cards per level: a whole number ${p.min}–${p.max}`,
  switch_invalid: (p) => `${p.field} is true or false`,
  mode_unknown: (p) => `unknown mode ${pyRepr(String(p.mode))}`,
  mode_not_built: (p) => `mode ${pyRepr(String(p.mode))} isn't playable yet`,
  mode_single: (p) => `mode ${pyRepr(String(p.mode))} is for one player`,
  seat_missing: "the action names no seat",
  seat_unknown: "no such seat",
  seat_out: "that seat is out of the game",
  not_your_turn: "it's not that seat's turn",
  player_twice: (p) => `${pyRepr(String(p.name))} is seated twice`,
  players_too_few: (p) => `a session needs at least ${p.min} players`,
  gamemaster_only: (p) => `${p.action} only in gamemaster mode`,
  replace_empty: "no other question for this level",
  question_unknown: (p) => `no question ${pyRepr(String(p.id))} in the loaded pool`,
  level_invalid: (p) => `level: a whole number ${p.min}–${p.max}`,
  answers_on: "the answer is only revealed with answers off",
  answers_off: "answers are off: reveal the answer",
  snipe_answers_off: "answers are off",
  claim_taken: "another seat has claimed the question",
  claim_first: "claim the question first",
  not_your_claim: "another seat claimed the question",
  not_shown: "the question is not on screen yet",
  paused: "the clock is paused",
  already_paused: "the clock is already paused",
  not_paused: "the clock is not paused",
  not_expired: (p) => `the clock still runs (${p.ms} ms left)`,
  timed_no_jokers: "no jokers in timed mode",
  timed_only: (p) => `${p.action} only in timed mode`,
  cheat_not_select: (p) => `${p.action} only with the cards on the table`,
  language_unknown: (p) => `no language ${pyRepr(String(p.lang))}`,
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
  /** Epoch ms of the action (timed's clock, plan 159); missing = `now`. */
  ms?: number;
}

/** Display names of one locale (D-81): base's names file merged with every bundle's. */
export interface Names {
  bundles: Record<string, { name: string; description?: string }>;
  /** By catKey / subKey (decision 259): each file keys its own bundle's keys. */
  categories: Record<string, string>;
  subcategories: Record<string, string>;
  /** Age-group id → name (decision 48). */
  age_groups: Record<string, string>;
}

/** Per pool: built once by engineData. */
export interface EngineData {
  /** The question locale of `pool` (plan 68). */
  locale: string;
  /** Empty where no names files exist (plain-format mods: the keys are the names). */
  names: Names;
  /** Of the UI language (task 1024): age group and bundle names; `names` when it's the question locale. */
  uiNames: Names;
  pool: PoolQuestion[];
  /** pool.json's export hash (D-92), null if absent. */
  poolHash: string | null;
  byId: Map<string, PoolQuestion>;
  categories: Category[];
  broad: Map<string, Category>;
  bundles: Bundle[];
  ageGroups: AgeGroup[];
  groupById: Map<string, AgeGroup>;
  /** Demo build (decision 338): the only place engine code learns it. */
  demo: boolean;
}

const NO_NAMES: Names = { bundles: {}, categories: {}, subcategories: {}, age_groups: {} };

/** A locale's names files, the overriding one last (decision 259): es-ES reads es's, then its own. */
export const namesFiles = (lang: string): string[] =>
  (lang === "es-ES" ? ["names.es.json", "names.es-ES.json"] : [`names.${lang}.json`]);

/** Base's names file merged with every bundle's ([bundle id, file]), later ones winning; null files (none) are skipped. */
export function mergeNames(files: (readonly [string, unknown])[]): Names {
  const out: Names = { bundles: {}, categories: {}, subcategories: {}, age_groups: {} };
  const keyed = (bundle: string, m: Record<string, string> | undefined) =>
    Object.fromEntries(Object.entries(m ?? {}).map(([k, v]) => [subKey(bundle, k), v]));
  for (const [bundle, f] of files as [string, Partial<Names> | null][]) {
    if (!f) continue;
    Object.assign(out.bundles, f.bundles);
    Object.assign(out.categories, keyed(bundle, f.categories));
    Object.assign(out.subcategories, keyed(bundle, f.subcategories));
    Object.assign(out.age_groups, f.age_groups);
  }
  return out;
}

export function engineData(
  pool: PoolQuestion[], categories: Category[], bundles: Bundle[], ageGroups: AgeGroup[],
  locale = "es", names: Names = NO_NAMES, poolHash: string | null = null, demo = false,
): EngineData {
  return {
    locale, names, uiNames: names, pool, poolHash, byId: byId(pool), categories, broad: broadOf(categories),
    bundles, ageGroups, groupById: new Map(ageGroups.map((g) => [g.id, g])), demo,
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
