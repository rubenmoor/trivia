// Mirrors the question schema of authoring/data/questions.json (plans/02-question-pool.md).
// The play fields come from the game's types (app/client/src/lib/types.ts, D-35).
import type { Background as PlayBackground, Media as PlayMedia, Status } from "$app/lib/types";

export type { Category, Status } from "$app/lib/types";
export type Decision = Exclude<Status, "draft">;

/** A picked file's licence record (plan 26); missing on slots picked before it. */
export interface LicenceRecord {
  provider?: string;
  license?: string | null;
  license_url?: string | null;
  author?: string | null;
  author_url?: string | null;
  /** Commons restriction flags: information only, never a reason to replace (D-61). */
  restrictions?: string[];
  /** PD templates of a public-domain file (D-62). */
  pd_reasons?: string[];
}

/** providers.licence_verdict of a picked slot (plan 53); reasons are "code: text". */
export interface LicenceVerdict {
  verdict: "ok" | "replace";
  reasons: string[];
}

/** The play fields plus the search spec used by `trivia-media fetch`. */
interface Media extends PlayMedia, LicenceRecord {
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
interface Background extends PlayBackground, LicenceRecord {
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

/** The rater's scores (qgen.py RUBRIC); no_giveaway, no_overlap missing on older batches. */
interface Quality {
  correct: number;
  unambiguous: number;
  no_giveaway?: number;
  no_overlap?: number;
  distractors: number;
  age_fit: number;
  fun: number;
  description: number;
  difficulty_estimate: number;
  notes: string;
}

/** Both make an approved question playable (D-33). */
type Reviewer = "human" | "llm";

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
interface Audit {
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
  /** Added by the server: per picked slot; unpicked slots left out. */
  licence: Partial<Record<Slot, LicenceVerdict>>;
  /** D-81: false = doesn't travel (absent = true). */
  translatable?: boolean;
  /** Locale view (plan 67): the translation's locale, its Spanish source and whether that changed since. */
  locale?: string;
  source?: SourceText;
  stale?: boolean;
}

/** The Spanish side of a translation item (plan 67). */
export type SourceText = Pick<
  Question,
  "question" | "answer" | "wrong_answers" | "hints" | "description" | "fun_fact" | "difficulty" | "status"
>;

/** GET /api/names?locale=: display names keyed by bundle id, category slug, Spanish subcategory (D-81). */
export interface Names {
  bundles: Record<string, { name: string; description: string }>;
  categories: Record<string, string>;
  subcategories: Record<string, string>;
  age_groups: Record<string, string>;
}

/** A question bundle (app/data/bundles.json, D-39). */
export type Bundle = {
  id: string;
  kind: "base" | "region" | "theme";
  languages: string[];
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

/** A bundle's targets in authoring/data/targets.json (D-53): approved questions in total and per difficulty. */
export interface BundleTargets {
  total: number;
  difficulty: Record<string, number>;
}

/** GET /api/targets: the whole file; non-bundle keys ("about", "batch_health", "quality") left untyped. */
export type Targets = Record<string, unknown>;

/** GET /api/overview (authoring/server/overview.py, RV-12): what the start page shows. */
export interface Overview {
  queues: {
    needs_work: number;
    drafts: number;
    approved_without_media: number;
    not_cached: number;
    /** Questions on the licence replacement list (plan 53). */
    licence_replace: number;
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
    /** A translation run (tr-*): its locale (plan 67); null for Spanish batches. */
    locale: string | null;
  }[];
  /** Per locale with a translation file (plan 67); untranslated, not_translatable: approved sources. */
  locales: {
    locale: string;
    approved: number;
    needs_work: number;
    draft: number;
    rejected: number;
    stale: number;
    not_translatable: number;
    untranslated: number;
  }[];
  /** The profile (= the save, plan 65), pool minus blocked. */
  supply: {
    blocked: number;
    unseen: number;
    seen_once: number;
    seen_twice: number;
    /** "any": every count; "unseen": count 0 only. */
    rows: { label: string; levels: { level: number; range: [number, number]; candidates: number; missing: number }[] }[];
  };
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
