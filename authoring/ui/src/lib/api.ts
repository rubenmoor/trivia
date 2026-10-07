// The authoring server's question API (authoring/server/main.py, port 8001).
import { call, json, post } from "$app/lib/api";
import type { Question, Review, Slot, Status } from "./types";

export { fetchCategories } from "$app/lib/api";

/** batch: a qgen.py run name, "none" for questions without a batch, or null for all. */
export async function fetchQuestions(batch: string | null, status?: Status): Promise<Question[]> {
  const params = new URLSearchParams();
  if (batch) params.set("batch", batch);
  if (status) params.set("status", status);
  const query = params.size ? `?${params}` : "";
  return json(await call(`/api/questions${query}`));
}

/** review: a new decision, or null to reset the question to draft. */
export async function saveReview(
  id: string,
  review: Pick<Review, "decision" | "feedback"> | Review | null,
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

/** Set the difficulty (1–10); the server keeps the first original value. */
export async function setDifficulty(id: string, difficulty: number): Promise<Question> {
  return post(`/api/questions/${encodeURIComponent(id)}/difficulty`, { difficulty });
}

