// Mirrors the playable pool, app/data/pool.json (plans/02-question-pool.md, D-35). The authoring
// side (authoring/ui/src/lib/types.ts) extends these with the review and pipeline fields.

export type Status = "draft" | "approved" | "rejected" | "needs_work";

export interface Media {
  type: "image" | "audio" | "video";
  role: "decorative" | "illustrative" | "essential";
  source_url: string | null;
  /** Exact URL of the picked file; the server caches it (D-17). */
  file_url: string | null;
  credit: string | null;
}

/** Background image for audio questions (D-14). */
export interface Background {
  source_url: string | null;
  /** Exact URL of the picked file; the server caches it (D-17). */
  file_url: string | null;
  credit: string | null;
}

/** A broad category of one bundle's categories file (D-19, D-43). */
export interface Category {
  slug: string;
  name: string;
  bundle: string;
  subcategories: string[];
}

/** The supply check before a new game (GF-5, app/server/game.py). */
export interface Supply {
  ok: boolean;
  available: number;
  levels: { level: number; range: [number, number]; candidates: number; missing: number }[];
}

/** The age group and active bundles of a game (plan 27, D-38, D-39). */
export interface Choice {
  age_group: string;
  /** In bundles.json order, every always_on bundle included. */
  bundles: string[];
}

/** A known player (app/server/game.py `players`, D-28). */
export interface Player {
  name: string;
  games: number;
  won: number;
  last_played: string | null;
}

export type JokerName = "hint" | "skip" | "easier" | "category" | "snipe";

/** 13-game-modes.md "Implementation notes"; plan 36 builds `gamemaster` and `solo`. */
export type GameMode = "gamemaster" | "solo" | "rr-coop" | "rr-competitive" | "timed";

/** A count per joker; null = unlimited (13-game-modes.md, MD-1). */
export type JokerBudget = Record<JokerName, number | null>;

/** A server error code with its params (D-57); lib/errors.ts renders it. */
export interface ErrorInfo {
  code: string;
  params: Record<string, unknown>;
}

export interface JokerState {
  available: boolean;
  /** Why it can't be played right now; reasonText() renders it. */
  reason: ErrorInfo | null;
}

export interface Jokers {
  hint: JokerState;
  skip: JokerState & { purge: JokerState & { subcategory: string } };
  easier: JokerState;
  category: JokerState & {
    categories: { slug: string; name: string; available: boolean; subcategories: { name: string; available: boolean }[] }[];
  };
  snipe: JokerState;
}

/** What a played joker did (POST /api/game/joker → `event`), for the animation. */
export type JokerEvent =
  | { joker: "hint"; hint: number }
  | { joker: "skip"; purged: string | null }
  | { joker: "easier"; from: number; to: number }
  | { joker: "category"; subcategory: string }
  | { joker: "snipe"; outcome: "miss"; index: number }
  | { joker: "snipe"; outcome: "hit"; index: number; correct_index: number };

/** The game as the server shows it to the TV (app/server/game.py `view`): no correct answer before the final answer. */
export interface Game {
  id: number;
  /** null only for games from before players existed (D-28). */
  player: string | null;
  result: null | "won" | "lost" | "abandoned";
  level: number;
  phase: "select" | "question" | "won" | "lost";
  options: { description: string }[];
  history: { level: number; correct: boolean }[];
  can_undo: boolean;
  /** Subcategories purged with «Paso» in this game. */
  purged: string[];
  /** The level repeats after a «Francotirador» hit (until a card is picked). */
  repeat: boolean;
  /** Joker availability while a question is on screen, else null (09-jokers.md). */
  jokers: Jokers | null;
  /** Game settings (13-game-modes.md, MD-1): the joker budget per game, null = unlimited;
   * age group and bundles as stored (plan 27), missing = `DEFAULT_AGE_GROUP` / every bundle;
   * mode as stored, missing = `gamemaster`; `customized` outside gamemaster mode (plan 36). */
  settings: { jokers: JokerBudget; age_group?: string; bundles?: string[]; mode?: GameMode; customized?: boolean };
  /** Uses left in this game per joker, null = unlimited (MD-1). */
  jokers_left: JokerBudget;
  question: {
    id: string;
    question: string;
    answers: string[];
    media: Media;
    background: Background | null;
    /** The hints shown so far through «Soplo» (D-27). */
    hints: string[];
    /** Answer indexes struck out by «Francotirador» misses. */
    struck: number[];
    /** The subcategory chosen with «Cambiazo» for this question, or null. */
    swapped_to: string | null;
  } | null;
  last: {
    question_id: string;
    chosen: number;
    correct: boolean;
    correct_index: number;
    answer: string;
    fun_fact: string;
  } | null;
}
