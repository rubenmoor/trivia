// The authoring server's question API (authoring/server/main.py, port 8001).
import { call, json, post } from "$app/lib/api";
import type { AgeGroups, Bundle, Category, MediaStats, Overview, Question, Review, Slot, SpotCheckItem, SpotChecks, Status, Targets } from "./types";

/** Every bundle's broad categories with subcategories (D-19, D-43). */
export async function fetchCategories(): Promise<Category[]> {
  return json(await call("/api/categories"));
}

/** Filters of GET /api/questions; all optional (authoring/server/main.py). */
export interface QuestionFilter {
  /** A qgen.py run name, or "none" for questions without a batch. */
  batch?: string | null;
  /** A status, or `!` and a status for every other one (`!approved`, RV-22). */
  status?: Status | `!${Status}` | null;
  reviewer?: "human" | "llm" | "none" | null;
  bundle?: string | null;
  subcategory?: string | null;
  /** "missing": no picked media file. */
  media?: "missing" | null;
  /** A back-audit run (`backaudit-<k>`, plan 57): its questions. */
  run?: string | null;
  /** With batch or run: "1" = its spot-check sample in order (plan 16). */
  sample?: string | null;
  /** "flagged" = audited with a major finding (plan 16). */
  audit?: "flagged" | null;
}

export async function fetchQuestions(filter: QuestionFilter = {}): Promise<Question[]> {
  const params = new URLSearchParams();
  for (const [key, value] of Object.entries(filter)) if (value) params.set(key, value);
  const query = params.size ? `?${params}` : "";
  return json(await call(`/api/questions${query}`));
}

/** review: a new decision, or null to reset the question to draft. */
export async function saveReview(
  id: string,
  review: Pick<Review, "decision" | "feedback" | "problems"> | Review | null,
): Promise<Question> {
  return post(`/api/questions/${encodeURIComponent(id)}/review`, { review });
}

/** Download candidate `index` (0-based) into the slot. */
export async function pickMedia(id: string, index: number, slot: Slot = "media"): Promise<Question> {
  return post(`/api/questions/${encodeURIComponent(id)}/media`, { index, slot });
}

/** Save a new search term for the slot and fetch fresh candidates from Commons. */
export async function searchMedia(id: string, query: string, slot: Slot = "media"): Promise<Question> {
  return post(`/api/questions/${encodeURIComponent(id)}/media/search`, { query, slot });
}

/** The question bundles (app/data/bundles.json, D-39). */
export async function fetchBundles(): Promise<Bundle[]> {
  return json(await call("/api/bundles"));
}

/** Move a question to another bundle. */
export async function setBundle(id: string, bundle: string): Promise<Question> {
  return post(`/api/questions/${encodeURIComponent(id)}/bundle`, { bundle });
}

/** Set the difficulty (1–15, D-38); the server keeps the first original value. */
export async function setDifficulty(id: string, difficulty: number): Promise<Question> {
  return post(`/api/questions/${encodeURIComponent(id)}/difficulty`, { difficulty });
}

/** The difficulty scale and the age groups' windows (app/data/age-groups.json, D-38). */
export async function fetchAgeGroups(): Promise<AgeGroups> {
  return json(await call("/api/age-groups"));
}

/** Pool targets per bundle (authoring/data/targets.json, D-53). */
export async function fetchTargets(): Promise<Targets> {
  return json(await call("/api/targets"));
}

/** Everything the start page shows except the statistics (RV-12). */
export async function fetchOverview(): Promise<Overview> {
  return json(await call("/api/overview"));
}

/** Approved questions per media role and image resolution (RV-23). */
export async function fetchMediaStats(bundle: string | null): Promise<MediaStats> {
  return json(await call(`/api/stats/media${bundle ? `?${new URLSearchParams({ bundle })}` : ""}`));
}

/** Spot-check size, problem kinds and every recorded spot check (plan 16). */
export async function fetchSpotChecks(): Promise<SpotChecks> {
  return json(await call("/api/spot-checks"));
}

/** Record the spot check from the question's (just saved) human review. */
export async function recordSpotCheck(batch: string, id: string, mediaChanged: boolean): Promise<SpotCheckItem> {
  return post(`/api/spot-checks/${encodeURIComponent(batch)}/${encodeURIComponent(id)}`, { media_changed: mediaChanged });
}

/** Undo: remove the question's spot check. */
export async function removeSpotCheck(batch: string, id: string): Promise<null> {
  return post(`/api/spot-checks/${encodeURIComponent(batch)}/${encodeURIComponent(id)}`, { undo: true });
}
