import type { Category, Game, JokerBudget, JokerEvent, JokerName, Player, Supply } from "./types";

export async function json<T>(res: Response): Promise<T> {
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.error ?? `HTTP ${res.status} ${res.statusText}`);
  }
  return res.json();
}

/** fetch() that turns "server not running" into a readable error. */
export async function call(url: string, init?: RequestInit): Promise<Response> {
  try {
    return await fetch(url, init);
  } catch {
    throw new Error("server not reachable — is the game server (`trivia`) running?");
  }
}

export async function fetchCategories(): Promise<Category[]> {
  return json(await call("/api/categories"));
}

export async function post<T>(url: string, body: unknown): Promise<T> {
  return json(
    await call(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }),
  );
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

/** The body of a game action: `index` for pick/answer, `player` for new, `everyone` for skip (D-28),
 * `jokers` for the joker budget (MD-4). */
export interface GameActionBody {
  index?: number;
  player?: string;
  everyone?: boolean;
  jokers?: Partial<JokerBudget>;
}

/** Play a joker (09-jokers.md): the game afterwards plus what happened, for the animation. */
export async function playJoker(body: {
  joker: JokerName;
  purge?: boolean;
  subcategory?: string;
  index?: number;
}): Promise<{ game: Game; event: JokerEvent }> {
  const res = await call("/api/game/joker", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  const out = await res.json().catch(() => ({}));
  if (!res.ok) throw new GameError(out.error ?? `HTTP ${res.status}`, null);
  return out;
}

/** POST /api/game/<action> (app/server/game.py); returns the game afterwards. */
export async function gameAction(
  action: "new" | "pick" | "answer" | "skip" | "undo" | "abandon" | "jokers",
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
