import type { Category, ErrorInfo, Game, JokerBudget, JokerEvent, JokerName, Player, Supply } from "./types";

/** A refused request (D-57): `code` and `params` for errorText(), `message` in English; `supply` is set
 * when the pool can't fill a new game (GF-5). */
export class GameError extends Error implements ErrorInfo {
  readonly code: string;
  readonly params: ErrorInfo["params"];
  readonly supply: Supply | null;

  constructor(code: string, params: ErrorInfo["params"], message: string, supply: Supply | null) {
    super(message);
    this.code = code;
    this.params = params;
    this.supply = supply;
  }
}

/** The error of a failed response: GameError if the body has `error`, else a plain Error. */
function failure(res: Response, body: Record<string, any>): Error {
  if (typeof body.error !== "string") return new Error(`HTTP ${res.status} ${res.statusText}`);
  return new GameError(body.error, body.params ?? {}, body.message ?? body.error, body.supply ?? null);
}

export async function json<T>(res: Response): Promise<T> {
  if (!res.ok) throw failure(res, await res.json().catch(() => ({})));
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

/** IDs of the questions flagged for review (GM-5, D-47). */
export async function fetchFlags(): Promise<string[]> {
  return json(await call("/api/flags"));
}

/** Flag or unflag a question for review; returns every flagged ID. */
export async function setFlag(id: string, flagged: boolean, player: string | null): Promise<string[]> {
  return post("/api/flags", { id, flagged, player });
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
  if (!res.ok) throw failure(res, out);
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
  if (!res.ok) throw failure(res, out);
  return out.game;
}
