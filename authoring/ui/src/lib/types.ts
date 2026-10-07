// Mirrors the question schema of authoring/data/questions.json (plans/02-question-pool.md).
// The play fields come from the game's types (app/client/src/lib/types.ts, D-35).
import type { Background as PlayBackground, Media as PlayMedia, Status } from "$app/lib/types";

export type { Category, Status } from "$app/lib/types";
export type Decision = Exclude<Status, "draft">;

/** The play fields plus the search spec used by `trivia-media fetch`. */
export interface Media extends PlayMedia {
  query: string;
  note: string | null;
}

/** A Wikimedia Commons file found by authoring/tools/media.py (work/media/<id>.json). */
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
export interface Background extends PlayBackground {
  query: string;
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
  /** Its broad category is the one in app/data/categories.json that lists it (D-19). */
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

