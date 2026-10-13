// Mirrors the playable pool, app/data/pool.json (plans/02-question-pool.md, D-35). The authoring
// side (authoring/ui/src/lib/types.ts) extends these with the review and pipeline fields.

export type Status = "draft" | "approved" | "rejected" | "needs_work";

export interface Media {
  type: "image" | "audio" | "video";
  role: "decorative" | "illustrative" | "essential";
  source_url: string | null;
  /** Exact URL of the picked file; served from the media cache (D-17). */
  file_url: string | null;
  credit: string | null;
}

/** Background image for audio questions (D-14). */
export interface Background {
  source_url: string | null;
  /** Exact URL of the picked file; served from the media cache (D-17). */
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

/** The supply check before a new game (GF-5, engine/selection.ts). */
export interface Supply {
  ok: boolean;
  available: number;
  levels: { level: number; range: [number, number]; candidates: number; missing: number }[];
}

/** A custom difficulty ramp (D-88): integers 1–15, end ≥ start. */
export interface Difficulty {
  start: number;
  end: number;
}

/** A game's configuration (plan 27, D-38, D-39, D-88): what the configure screen shows. */
export interface Choice {
  /** null with a custom `difficulty`. */
  age_group: string | null;
  difficulty: Difficulty | null;
  /** In bundles.json order, exactly one base bundle (plan 71). */
  bundles: string[];
  /** 1–20. */
  levels: number;
  /** Cards per level, 0–4; 0: the question opens at once. */
  cards: number;
  video: boolean;
  audio: boolean;
  jokers: JokerBudget;
}

/** UI and question language of a save (plan 68); a game keeps the question locale it started in. */
export interface Language {
  ui: string;
  questions: string;
}

/** A known player (engine/game.ts `players`, D-28). */
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

/** An engine error code with its params (D-57); lib/errors.ts renders it. */
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

/** What a played joker did (`playJoker` → `event`), for the animation. */
export type JokerEvent =
  | { joker: "hint"; hint: number }
  | { joker: "skip"; purged: string | null }
  | { joker: "easier"; from: number; to: number }
  | { joker: "category"; subcategory: string }
  | { joker: "snipe"; outcome: "miss"; index: number }
  | { joker: "snipe"; outcome: "hit"; index: number; correct_index: number };

/** A flagged question as «Preguntas marcadas» shows it (decision 60); `answer` null while it's on screen. */
export interface Flagged {
  question_id: string;
  flagged_on: string;
  player: string | null;
  level?: number;
  note?: string;
  question: string | null;
  answer: string | null;
}

/** The game as the engine shows it to the TV (engine/game.ts `view`): no correct answer before the final answer. */
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
   * mode as stored, missing = `gamemaster`; `customized` outside gamemaster mode (plan 36);
   * difficulty, levels, cards, video, audio (D-88): missing = age group, 12, 4, allowed. */
  settings: {
    jokers: JokerBudget; age_group?: string; bundles?: string[]; mode?: GameMode; customized?: boolean;
    difficulty?: Difficulty; levels?: number; cards?: number; video?: false; audio?: false;
  };
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

/** credits.json, made by app/client/credits.ts at build time (PUB-5, plan 47). */
export type CreditKind = "image" | "audio" | "video" | "background";

export interface MediaCredit {
  kind: CreditKind;
  title: string;
  /** null: unknown author (the screen shows its own text). */
  author: string | null;
  author_url: string | null;
  license: string;
  license_url: string | null;
  source_url: string;
  provider: string | null;
}

export interface SoundCredit {
  file: string;
  used_for: string;
  source: string;
  source_url: string | null;
  author: string;
  license: string;
}

export interface Credits {
  version: 1;
  /** Licence files at the repo root (plan 40), with their first line. */
  game: { file: string; title: string }[];
  media: MediaCredit[];
  sounds: { entries: SoundCredit[]; note: string };
  fonts: { name: string; license: string; license_file: string }[];
  /** Controller glyphs drawn for the game (Glyph.svelte). */
  glyphs: boolean;
  libraries: { name: string; version: string; license: string; url: string }[];
}
