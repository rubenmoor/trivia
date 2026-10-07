// Mirrors the question schema in plans/02-question-pool.md.

export type Status = "draft" | "approved" | "rejected" | "needs_work";
export type Decision = Exclude<Status, "draft">;

export interface Media {
  type: "image" | "audio" | "video";
  role: "decorative" | "illustrative" | "essential";
  query: string;
  note: string | null;
  source_url: string | null;
  /** Exact URL of the picked file; the server caches it in media/ (D-17). */
  file_url: string | null;
  credit: string | null;
}

/** A Wikimedia Commons file found by tools/media.py (work/media/<id>.json). */
export interface MediaCandidate {
  type: Media["type"];
  title: string;
  page_url: string;
  preview_url: string | null;
  file_url: string;
  width: number | null;
  height: number | null;
  duration: number | null;
  mime: string;
  author: string | null;
  license: string | null;
  license_url: string | null;
}

/** Background image for audio questions (D-14). */
export interface Background {
  query: string;
  source_url: string | null;
  /** Exact URL of the picked file; the server caches it in media/ (D-17). */
  file_url: string | null;
  credit: string | null;
}

/** A broad category from data/categories.json (D-19). */
export interface Category {
  slug: string;
  name: string;
  subcategories: string[];
}

export type Slot = "media" | "background";

/** Set by `qgen.py apply` (plans/07-question-generation.md, QG-13). */
export interface Revision {
  action: "revise" | "drop";
  reason: string;
  /** Old values of the fields that changed. */
  previous: Record<string, unknown>;
  revised_on: string;
}

export interface Quality {
  correct: number;
  unambiguous: number;
  distractors: number;
  age_fit: number;
  fun: number;
  description: number;
  difficulty_estimate: number;
  notes: string;
}

/** Both make an approved question playable (D-33). */
export type Reviewer = "human" | "llm";

export interface Review {
  decision: Decision;
  feedback: string | null;
  reviewed_on: string;
  reviewer: Reviewer;
  /** The model behind an LLM review; null for a human. */
  model: string | null;
  /** The LLM review a human review replaced. */
  previous: Review | null;
}

export interface Question {
  id: string;
  status: Status;
  difficulty: number;
  description: string;
  question: string;
  answer: string;
  wrong_answers: string[];
  hints: string[];
  media: Media;
  fun_fact: string;
  /** Its broad category is the one in data/categories.json that lists it (D-19). */
  subcategory: string;
  style: string | null;
  quality: Quality | null;
  fact_checked: boolean | null;
  needs_media: boolean | null;
  batch: string | null;
  review: Review | null;
  background: Background | null;
  difficulty_original?: number | null;
  revision?: Revision | null;
  /** Added by the server: null when candidates were never fetched. */
  media_candidates: MediaCandidate[] | null;
  background_candidates: MediaCandidate[] | null;
}

/** The supply check before a new game (GF-5, server/game.py). */
export interface Supply {
  ok: boolean;
  available: number;
  levels: { level: number; range: [number, number]; candidates: number; missing: number }[];
}

/** A known player (server/game.py `players`, D-28). */
export interface Player {
  name: string;
  games: number;
  won: number;
  last_played: string | null;
}

export type JokerName = "hint" | "skip" | "easier" | "category" | "snipe";

export interface JokerState {
  available: boolean;
  /** Why it can't be played right now (Spanish, shown on the TV). */
  reason: string | null;
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

/** The game as the server shows it to the TV (server/game.py `view`): no correct answer before the final answer. */
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
