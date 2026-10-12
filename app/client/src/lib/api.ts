import * as engine from "../engine/api.ts";
import { flaggedIds, setFlag as saveFlag } from "../engine/save.ts";
import { read, run } from "./engine.ts";
import type { ErrorInfo, Game, JokerBudget, JokerEvent, JokerName, Player, Report, Supply } from "./types";

// The game's only door to the referee: the TS engine on an in-memory save, persisted via /api/save (plan 50, PORT-7).

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
  return read((save) => engine.getPlayers(save));
}

/** Delete a player's name and games (GF-7), not what the family saw; returns the remaining players. */
export async function deletePlayer(name: string): Promise<Player[]> {
  return run((save) => engine.deletePlayer(save, { name }));
}

/** IDs of the questions flagged for review (GM-5, D-47). */
export async function fetchFlags(): Promise<string[]> {
  return read((save) => ({ save, status: 200, body: flaggedIds(save) }));
}

/** Flag or unflag a question for review; returns every flagged ID. */
export async function setFlag(id: string, flagged: boolean, player: string | null): Promise<string[]> {
  return run((save, _data, io) => {
    try {
      const out = saveFlag(save, id, flagged, player, io.now);
      return { save: out, status: 200, body: flaggedIds(out) };
    } catch (e) {
      const message = e instanceof Error ? e.message : String(e);
      return { save, status: 400, body: { error: message, message } };
    }
  });
}

export async function fetchGame(): Promise<{ game: Game | null; supply: Supply }> {
  return read((save, data, io) => engine.getGame(save, data, io));
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
  return run((save, data, io) => engine.gameAction(save, data, io, "joker", { ...body })) as Promise<{
    game: Game;
    event: JokerEvent;
  }>;
}

/** Reported questions (MD-6), newest first; the running question's answer stays hidden. */
export async function fetchReports(): Promise<Report[]> {
  return read((save, data) => {
    const names = new Map(save.players.map((p) => [p.id, p.name]));
    const newest = save.games.reduce<(typeof save.games)[number] | null>((m, g) => (m && m.id > g.id ? m : g), null);
    const live = newest?.result === null && newest.state.phase === "question" ? newest : null;
    const body = save.reports
      .map((r) => {
        const q = data.byId.get(r.question_id);
        const hidden = live?.id === r.game_id && live.state.current === r.question_id;
        return {
          ...r,
          player: r.player_id === null ? null : (names.get(r.player_id) ?? null),
          question: q?.question ?? null,
          answer: hidden ? null : (q?.answer ?? null),
        };
      })
      .reverse();
    return { save, status: 200, body };
  });
}

/** A game action on the engine (engine/api.ts); returns the game afterwards. */
export async function gameAction(
  action: "new" | "pick" | "answer" | "skip" | "undo" | "abandon" | "jokers" | "report",
  body: GameActionBody = {},
): Promise<Game | null> {
  return (await run((save, data, io) => engine.gameAction(save, data, io, action, { ...body }))).game;
}
