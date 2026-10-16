// The former game routes of app/server/main.py (gone since PORT-8) on the engine (PORT-3, plan 20): same {status, body} as recorded.
import type { Choice, Game, GameMode, JokerEvent, Player, Supply } from "../lib/types.ts";
import * as game from "./game.ts";
import { noteRunningOut as noteRunningOutIn, outlook as outlookOf, sessionOutlook, type Outlook } from "./outlook.ts";
import { pyInt, pyStr, pyTruthy } from "./pycompat.ts";
import type { EngineData, Io, Language, SaveData } from "./state.ts";
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

/** GET /api/game[?player=]: the view; `player` only checked. */
export function getGame(save: SaveData, data: EngineData, io: Io, player?: string | null):
  Reply<{ game: Game | null }> {
  return guard(save, 400, () => {
    const view = game.view(save, data, io);
    if (player) game.cleanName(player);
    return { save, status: 200, body: { game: view } };
  });
}

/** GET /api/players */
export function getPlayers(save: SaveData): Reply<Player[]> {
  return { save, status: 200, body: game.players(save) };
}

/** POST /api/players/delete {name} */
export function deletePlayer(save: SaveData, body: Record<string, unknown>, io: Io): Reply<Player[]> {
  return guard(save, 409, () => {
    const out = game.deletePlayer(save, body.name, io).save;
    return { save: out, status: 200, body: game.players(out) };
  });
}

/** The keys of `body` that are present. */
function pick<K extends string>(body: Record<string, unknown>, keys: readonly K[]): Partial<Record<K, unknown>> {
  return Object.fromEntries(keys.filter((k) => k in body).map((k) => [k, body[k]])) as Partial<Record<K, unknown>>;
}

/** The start / configure screen's preset and supply per choice (plan 27, D-88): a missing field comes
 * from the player's newest game, else the defaults. */
export function choice(save: SaveData, data: EngineData, body: Record<string, unknown>):
  Reply<{ choice: Choice; supply: Supply }> {
  return guard(save, 409, () => {
    const out = game.resolveChoice(data, pick(body, game.CHOICE_KEYS), game.playerChoice(save, data, body.player));
    return { save, status: 200, body: { choice: out, supply: game.supply(save, data, out) } };
  });
}

/** `new`'s mode must be built (the engine itself starts any, for tests and simulations); an unknown one is the engine's error. */
function startable(mode: unknown = "gamemaster"): true {
  if ((game.MODES as unknown[]).includes(mode) && !(game.BUILT_MODES as unknown[]).includes(mode)) throw new GameError("mode_not_built", { mode });
  return true;
}

/** Actions without an acting seat: start, end, timed's clock (plan 159). */
const CLOCK = new Set(["new", "abandon", "expire"]);

type Action = (save: SaveData) => { save: SaveData; event?: JokerEvent };

/** POST /api/game/<action> */
export function gameAction(save: SaveData, data: EngineData, io: Io, action: string, body: Record<string, unknown>):
  Reply<{ game: Game | null; event?: JokerEvent }> {
  const index = () => pyInt("index" in body ? body.index : -1);
  const actions: Record<string, Action> = {
    new: (s) => startable(body.mode) && "players" in body ? game.newSession(s, data, io, body.players, pick(body, [...game.CHOICE_KEYS, "mode", "age_groups"]))
      : game.newGame(s, data, io, body.player, pick(body, [...game.CHOICE_KEYS, "mode"])),
    pick: (s) => game.pick(s, data, io, index(), body.seat),
    answer: (s) => game.answer(s, data, io, index(), body.seat),
    claim: (s) => game.claim(s, data, io, body.seat),
    expire: (s) => game.expire(s, data, io),
    reveal: (s) => game.reveal(s, data, io),
    skip: (s) => game.skip(s, data, io, pyTruthy(body.everyone)),
    undo: (s) => game.undo(s, io),
    abandon: (s) => game.abandon(s, io),
    jokers: (s) => game.setJokers(s, io, body.jokers ?? null),
    replace: (s) => game.replace(s, data, io, pyTruthy(body.seen)),
    level: (s) => game.jumpLevel(s, data, io, body.level),
    goto: (s) => game.goTo(s, data, io, body.id),
    settings: (s) => game.changeSettings(s, data, io, pick(body, ["age_group", "difficulty", "bundles", "answers"])),
    joker: (s) => game.joker(s, data, io, pyStr(body.joker), pick(body, ["purge", "subcategory", "index"]), body.seat),
  };
  if (!Object.hasOwn(actions, action)) return { save, status: 404, body: NOT_FOUND };
  return guard(save, 409, () => {
    if (!CLOCK.has(action)) game.checkActor(save, body.seat);
    const { save: out, event } = actions[action](save);
    const res: { game: Game | null; event?: JokerEvent } = { game: game.view(out, data, io) };
    if (action === "joker") res.event = event;
    return { save: out, status: 200, body: res };
  });
}

/** Supply outlook for the start screen (plan 65): body = choice + mode (+ players, or `age_groups` per seat: the session's lowest). */
export function outlook(save: SaveData, data: EngineData, body: Record<string, unknown>): Reply<Outlook> {
  return guard(save, 409, () => {
    const choice = game.resolveChoice(data, pick(body, game.CHOICE_KEYS));
    const mode = body.mode ?? "gamemaster";
    if (!(game.MODES as unknown[]).includes(mode)) throw new GameError("mode_unknown", { mode: String(mode) });
    const players = typeof body.players === "number" && Number.isInteger(body.players) && body.players > 0 ? body.players : 1;
    const seatGroups = Array.isArray(body.age_groups) ? body.age_groups.filter((g): g is string => typeof g === "string") : [];
    const full = { ...choice, mode: mode as GameMode, players };
    return { save, status: 200, body: seatGroups.length ? sessionOutlook(save, data, full, seatGroups).outlook : outlookOf(save, data, full) };
  });
}

/** Bundles shown as running out (plan 65): body = choice + `shown`. */
export function noteRunningOut(save: SaveData, data: EngineData, body: Record<string, unknown>): Reply<{ ok: true }> {
  return guard(save, 409, () => {
    const choice = game.resolveChoice(data, pick(body, game.CHOICE_KEYS));
    const shown = Array.isArray(body.shown) ? body.shown.filter((s) => typeof s === "string") : [];
    return { save: noteRunningOutIn(save, data, choice, shown), status: 200, body: { ok: true } };
  });
}

/** The one language (plan 126), any mode; one of `options`. Questions apply to the next game. */
export function setLanguage(save: SaveData, body: Record<string, unknown>, options: readonly string[]): Reply<{ language: Language }> {
  return guard(save, 409, () => {
    const language = body.language;
    if (typeof language !== "string" || !options.includes(language)) throw new GameError("language_unknown", { lang: String(language) });
    const out = { ...save, language };
    return { save: out, status: 200, body: { language: out.language } };
  });
}
