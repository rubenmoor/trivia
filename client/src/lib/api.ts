import type { Category, Game, Player, Question, Review, Slot, Supply } from "./types";

async function json<T>(res: Response): Promise<T> {
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.error ?? `HTTP ${res.status} ${res.statusText}`);
  }
  return res.json();
}

/** fetch() that turns "server not running" into a readable error. */
async function call(url: string, init?: RequestInit): Promise<Response> {
  try {
    return await fetch(url, init);
  } catch {
    throw new Error("server not reachable — is `python3 server/main.py` running?");
  }
}

/** batch: a qgen.py run name, "none" for questions without a batch, or null for all. */
export async function fetchQuestions(batch: string | null): Promise<Question[]> {
  const query = batch ? `?batch=${encodeURIComponent(batch)}` : "";
  return json(await call(`/api/questions${query}`));
}

export async function fetchCategories(): Promise<Category[]> {
  return json(await call("/api/categories"));
}

async function post<T>(url: string, body: unknown): Promise<T> {
  return json(
    await call(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }),
  );
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

/** A refused game action; `supply` is set when the pool can't fill a new game (GF-5). */
export class GameError extends Error {
  constructor(message: string, readonly supply: Supply | null) {
    super(message);
  }
}

/** Known players, the most recent first (D-28). */
export async function fetchPlayers(): Promise<Player[]> {
  return json(await call("/api/players"));
}

/** Delete a player with all their games and burns (GF-7); returns the remaining players. */
export async function deletePlayer(name: string): Promise<Player[]> {
  return json(
    await call("/api/players/delete", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name }),
    }),
  );
}

export async function fetchGame(): Promise<{ game: Game | null; supply: Supply }> {
  return json(await call("/api/game"));
}

/** The body of a game action: `index` for pick/answer, `player` for new, `everyone` for skip (D-28). */
export interface GameActionBody {
  index?: number;
  player?: string;
  everyone?: boolean;
}

/** POST /api/game/<action> (server/game.py); returns the game afterwards. */
export async function gameAction(
  action: "new" | "pick" | "answer" | "skip" | "undo" | "abandon",
  body: GameActionBody = {},
): Promise<Game | null> {
  const res = await call(`/api/game/${action}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  const out = await res.json().catch(() => ({}));
  if (!res.ok) throw new GameError(out.error ?? `HTTP ${res.status}`, out.supply ?? null);
  return out.game;
}
