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

/** A file found by authoring/tools/media.py (work/media/<id>.json) at one of the providers (D-45). */
export interface MediaCandidate {
  type: Media["type"];
  /** commons, openverse, nasa, freesound; missing on candidates from before MP-2 (= commons). */
  provider?: string;
  /** The original site behind an aggregator (Openverse): Flickr, The Met, … */
  source?: string;
  license_kind?: string;
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
  /** Kinds of problems (qgen.py PROBLEMS, plan 15). */
  problems?: string[];
}

/** work/<batch>/audit/<id>.json: the independent LLM audit (plan 16). */
export interface Audit {
  verdict: "ok" | "problem";
  problems: string[];
  severity: "minor" | "major";
  difficulty_estimate: number;
  notes: string;
  model: string;
  on: string;
}

/** One question's spot check in authoring/data/spot-checks.json (plan 16). */
export interface SpotCheckItem {
  llm: Decision;
  /** "problem": the audit has a major finding; null: not audited. */
  audit: "ok" | "problem" | null;
  human: Decision;
  problems: string[];
  /** [before the human, after]. */
  difficulty: [number, number];
  media_changed: boolean;
  on: string;
}

/** GET /api/spot-checks. */
export interface SpotChecks {
  size: number;
  problems: string[];
  checks: Record<string, { size: number; seed: string; items: Record<string, SpotCheckItem> }>;
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
  /** Its broad category is the one in a bundle's categories file that lists it (D-19, D-43). */
  subcategory: string;
  style: string | null;
  /** D-39: the one bundle the question is in. */
  bundle: string;
  /** D-37: the concept from the subcategory's list, and the question axes. */
  concept?: string | null;
  axes?: Record<string, string> | null;
  quality: Quality | null;
  fact_checked: boolean | null;
  needs_media: boolean | null;
  batch: string | null;
  review: Review | null;
  background: Background | null;
  difficulty_original?: number | null;
  revision?: Revision | null;
  /** Added by the server: null when not audited. */
  audit: Audit | null;
  /** Added by the server: null when candidates were never fetched. */
  media_candidates: MediaCandidate[] | null;
  background_candidates: MediaCandidate[] | null;
}

/** A question bundle (app/data/bundles.json, D-39). */
export type Bundle = {
  id: string;
  kind: "base" | "region" | "theme";
  always_on: boolean;
  name: string;
  description: string;
  rule: string;
};

/** app/data/age-groups.json (D-38): one shared difficulty scale, a window of it per age group. */
export type AgeGroups = {
  scale: [number, number];
  focus: string | null;
  groups: { id: string; name: string; ages: [number, number | null]; window: [number, number] }[];
};

/** GET /api/overview (authoring/server/overview.py, RV-12): what the start page shows. */
export interface Overview {
  queues: {
    needs_work: number;
    drafts: number;
    approved_without_media: number;
    not_cached: number;
    bundles: { id: string; name: string; questions: number; unreviewed: number }[];
  };
  llm_approved: number;
  unfinished_runs: string[];
  batches: {
    name: string;
    date: string | null;
    merged: number;
    approved: number;
    needs_work: number;
    rejected: number;
    draft: number;
    human: number;
    llm_approved: number;
    report: string | null;
  }[];
  supply: {
    /** null: a new player (global burns only). */
    player: string | null;
    burned: number;
    levels: { level: number; range: [number, number]; candidates: number; missing: number }[];
  }[];
  per_level: number;
  next_batch_subcategories: string[];
  counts: { status: Record<string, number>; bundle: Record<string, number> };
}

/** GET /api/stats/media (authoring/server/media_stats.py, RV-23). */
export interface MediaStats {
  questions: number;
  /** Most questions first; counts per media type and without a picked file. */
  roles: ({ role: Media["role"]; questions: number; no_file: number } & Partial<Record<Media["type"], number>>)[];
  /** Picked images by long edge in px, small to large, then SVG / not cached / unreadable. */
  bands: { band: string; questions: number }[];
  /** The most common exact sizes. */
  sizes: { size: string; questions: number }[];
}
