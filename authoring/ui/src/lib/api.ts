// The authoring server's question API (authoring/server/main.py, port 8001).
import { call, json, post } from "$app/lib/http.ts";
import type { AgeGroups, Bundle, Category, MediaStats, Names, Overview, Question, Review, Slot, SpotCheckItem, SpotChecks, Status, Targets } from "./types.ts";

const SERVER = "the authoring server (`trivia-authoring`)";

const get = async <T>(url: string): Promise<T> => json(await call(url, undefined, SERVER));
const send = <T>(url: string, body: unknown): Promise<T> => post(url, body, SERVER);

/** Every bundle's broad categories with subcategories (D-19, D-43). */
export async function fetchCategories(): Promise<Category[]> {
  return get("/api/categories");
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
  /** "replace": not rejected, a picked file on the licence replacement list (plan 53). */
  licence?: "replace" | null;
  /** A translation locale (en, de): its translations with the Spanish source (plan 67); absent = Spanish. */
  locale?: string | null;
  /** With locale: "1" = only stale translations. */
  stale?: string | null;
  /** With locale: "1" = only playing translations (translations.plays). */
  plays?: string | null;
}

export async function fetchQuestions(filter: QuestionFilter = {}): Promise<Question[]> {
  const params = new URLSearchParams();
  for (const [key, value] of Object.entries(filter)) if (value) params.set(key, value);
  const query = params.size ? `?${params}` : "";
  return get(`/api/questions${query}`);
}

/** review: a new decision, or null to reset the question to draft. */
export async function saveReview(
  id: string,
  review: Pick<Review, "decision" | "feedback" | "problems"> | Review | null,
  locale: string | null = null,
): Promise<Question> {
  return send(`/api/questions/${encodeURIComponent(id)}/review`, { review, locale });
}

/** Download candidate `index` (0-based) into the slot. */
export async function pickMedia(id: string, index: number, slot: Slot = "media"): Promise<Question> {
  return send(`/api/questions/${encodeURIComponent(id)}/media`, { index, slot });
}

/** Save a new search term for the slot and fetch fresh candidates; `all`: ask every provider (plan 53). */
export async function searchMedia(id: string, query: string, slot: Slot = "media", all = false): Promise<Question> {
  return send(`/api/questions/${encodeURIComponent(id)}/media/search`, { query, slot, all });
}

/** The question bundles (app/data/bundles.json, D-39). */
export async function fetchBundles(): Promise<Bundle[]> {
  return get("/api/bundles");
}

/** Move a question to another bundle. */
export async function setBundle(id: string, bundle: string): Promise<Question> {
  return send(`/api/questions/${encodeURIComponent(id)}/bundle`, { bundle });
}

/** Set the difficulty (1–15, D-38); the server keeps the first original value. */
export async function setDifficulty(id: string, difficulty: number, locale: string | null = null): Promise<Question> {
  return send(`/api/questions/${encodeURIComponent(id)}/difficulty`, { difficulty, locale });
}

/** The source's translatable flag; false rejects its translations ("no viaja", plan 67). */
export async function setTranslatable(id: string, translatable: boolean, locale: string | null = null): Promise<Question> {
  return send(`/api/questions/${encodeURIComponent(id)}/translatable`, { translatable, locale });
}

/** Display names in a translation locale (names.<locale>.json, D-81); null for Spanish. */
export async function fetchNames(locale: string): Promise<Names | null> {
  return get(`/api/names?${new URLSearchParams({ locale })}`);
}

/** The difficulty scale and the age groups' windows (app/data/age-groups.json, D-38). */
export async function fetchAgeGroups(): Promise<AgeGroups> {
  return get("/api/age-groups");
}

/** Pool targets per bundle (authoring/data/targets.json, D-53). */
export async function fetchTargets(): Promise<Targets> {
  return get("/api/targets");
}

/** Everything the start page shows except the statistics (RV-12). */
export async function fetchOverview(): Promise<Overview> {
  return get("/api/overview");
}

/** Approved questions per media role and image resolution (RV-23); with locale its playing translations' sources. */
export async function fetchMediaStats(bundle: string | null, locale: string | null = null): Promise<MediaStats> {
  const params = new URLSearchParams();
  if (bundle) params.set("bundle", bundle);
  if (locale) params.set("locale", locale);
  return get(`/api/stats/media${params.size ? `?${params}` : ""}`);
}

/** Spot-check size, problem kinds and every recorded spot check (plan 16). */
export async function fetchSpotChecks(): Promise<SpotChecks> {
  return get("/api/spot-checks");
}

/** Record the spot check from the question's (just saved) human review. */
export async function recordSpotCheck(batch: string, id: string, mediaChanged: boolean): Promise<SpotCheckItem> {
  return send(`/api/spot-checks/${encodeURIComponent(batch)}/${encodeURIComponent(id)}`, { media_changed: mediaChanged });
}

/** Undo: remove the question's spot check. */
export async function removeSpotCheck(batch: string, id: string): Promise<null> {
  return send(`/api/spot-checks/${encodeURIComponent(batch)}/${encodeURIComponent(id)}`, { undo: true });
}
