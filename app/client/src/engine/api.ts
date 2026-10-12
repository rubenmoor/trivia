// The game routes of app/server/main.py on the engine (PORT-3, plan 20): same {status, body} as recorded.
import type { Choice, Game, GameMode, JokerEvent, Player, Supply } from "../lib/types.ts";
import * as game from "./game.ts";
import { noteExhausted as noteExhaustedIn, outlook as outlookOf, type Outlook } from "./outlook.ts";
import { pyInt, pyStr, pyTruthy } from "./pycompat.ts";
import type { EngineData, Io, SaveData } from "./state.ts";
import { GameError } from "./state.ts";

/** A refused request on the wire (D-57). */
export interface ErrorBody {
  error: string;
  params?: Record<string, unknown>;
  message: string;
  supply?: Supply | null;
}

export type Reply<T> = { save: SaveData; status: number; body: T | ErrorBody };

const NOT_FOUND: ErrorBody = { error: "not_found", message: "not found" };

function errorBody(e: GameError): ErrorBody {
  return { error: e.code, params: e.params, message: e.message, supply: e.details };
}

/** Run fn; a GameError becomes `status` with the save unchanged. Other errors throw (Python: 500). */
function guard<T>(save: SaveData, status: number, fn: () => Reply<T>): Reply<T> {
  try {
    return fn();
  } catch (e) {
    if (e instanceof GameError) return { save, status, body: errorBody(e) };
    throw e;
  }
}

/** GET /api/game[?player=]: view first, then supply. */
export function getGame(save: SaveData, data: EngineData, io: Io, player?: string | null):
  Reply<{ game: Game | null; supply: Supply }> {
  return guard(save, 400, () => {
    const view = game.view(save, data, io);
    if (player) game.cleanName(player);
    return { save, status: 200, body: { game: view, supply: game.supply(save, data) } };
  });
}

/** GET /api/players */
export function getPlayers(save: SaveData): Reply<Player[]> {
  return { save, status: 200, body: game.players(save) };
}

/** POST /api/players/delete {name} */
export function deletePlayer(save: SaveData, body: Record<string, unknown>): Reply<Player[]> {
  return guard(save, 409, () => {
    const out = game.deletePlayer(save, body.name).save;
    return { save: out, status: 200, body: game.players(out) };
  });
}

/** The keys of `body` that are present. */
function pick<K extends string>(body: Record<string, unknown>, keys: readonly K[]): Partial<Record<K, unknown>> {
  return Object.fromEntries(keys.filter((k) => k in body).map((k) => [k, body[k]])) as Partial<Record<K, unknown>>;
}

/** The start screen's preset and supply per choice (plan 27): a missing field comes from the
 * player's newest game, else the defaults. */
export function choice(save: SaveData, data: EngineData, body: Record<string, unknown>):
  Reply<{ choice: Choice; supply: Supply }> {
  return guard(save, 409, () => {
    const out = game.resolveChoice(data, pick(body, ["age_group", "bundles"]), game.playerChoice(save, data, body.player));
    return { save, status: 200, body: { choice: out, supply: game.supply(save, data, out) } };
  });
}

type Action = (save: SaveData) => { save: SaveData; event?: JokerEvent };

/** POST /api/game/<action> */
export function gameAction(save: SaveData, data: EngineData, io: Io, action: string, body: Record<string, unknown>):
  Reply<{ game: Game | null; event?: JokerEvent }> {
  const index = () => pyInt("index" in body ? body.index : -1);
  const actions: Record<string, Action> = {
    new: (s) => game.newGame(s, data, io, body.player, pick(body, ["age_group", "bundles", "mode", "jokers"])),
    pick: (s) => game.pick(s, data, io, index()),
    answer: (s) => game.answer(s, data, io, index()),
    skip: (s) => game.skip(s, data, io, pyTruthy(body.everyone)),
    undo: (s) => game.undo(s, io),
    abandon: (s) => game.abandon(s, io),
    jokers: (s) => game.setJokers(s, io, body.jokers ?? null),
    report: (s) => game.report(s, io, body.note),
    joker: (s) => game.joker(s, data, io, pyStr(body.joker), pick(body, ["purge", "subcategory", "index"])),
  };
  if (!Object.hasOwn(actions, action)) return { save, status: 404, body: NOT_FOUND };
  return guard(save, 409, () => {
    const { save: out, event } = actions[action](save);
    const res: { game: Game | null; event?: JokerEvent } = { game: game.view(out, data, io) };
    if (action === "joker") res.event = event;
    return { save: out, status: 200, body: res };
  });
}

/** Supply outlook for the start screen (plan 65): body = choice + mode (+ players). */
export function outlook(save: SaveData, data: EngineData, body: Record<string, unknown>): Reply<Outlook> {
  return guard(save, 409, () => {
    const choice = game.resolveChoice(data, pick(body, ["age_group", "bundles"]));
    const mode = body.mode ?? "gamemaster";
    if (!(game.MODES as unknown[]).includes(mode)) throw new GameError("mode_unknown", { mode: String(mode) });
    const players = Number.isInteger(body.players) && (body.players as number) > 0 ? body.players as number : 1;
    return { save, status: 200, body: outlookOf(save, data, { ...choice, mode: mode as GameMode, players }) };
  });
}

/** Exhausted subcategories shown (plan 65): body = choice + `subcategories`. */
export function noteExhausted(save: SaveData, data: EngineData, body: Record<string, unknown>): Reply<{ ok: true }> {
  return guard(save, 409, () => {
    const choice = game.resolveChoice(data, pick(body, ["age_group", "bundles"]));
    const shown = Array.isArray(body.subcategories) ? body.subcategories.filter((s) => typeof s === "string") : [];
    return { save: noteExhaustedIn(save, data, choice, shown), status: 200, body: { ok: true } };
  });
}
