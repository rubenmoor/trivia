// The referee (PORT-3, plan 20): port of app/server/game.py. Public functions are pure:
// (save, data, io, …) → {save, …}; inside, they mutate a transact() copy like the Python port.
import type { Game, JokerBudget, JokerName, Player, Supply } from "../lib/types.ts";
import type { PoolQuestion } from "./pool.ts";
import { categoryOf } from "./pool.ts";
import { casefold, pyLen, pySplitJoin } from "./pycompat.ts";
import * as selection from "./selection.ts";
import type { EngineData, GameRow, GameState, Io, Outcome, SaveData } from "./state.ts";
import { GameError, UNLIMITED, nextId, transact, withDefaults } from "./state.ts";

export { GameError, UNLIMITED };

export const JOKERS: readonly JokerName[] = ["hint", "skip", "easier", "category", "snipe"];
/** «Como las cartas»: the printed card set (JK-11), for the overlay's preset (MD-4). */
export const CARDS: JokerBudget = { hint: 4, skip: 2, easier: 2, category: 2, snipe: 2 };

type Result = GameRow["result"];

/** A player name as typed: trimmed, inner spaces collapsed; GameError if empty or too long. */
export function cleanName(name: unknown): string {
  const s = pySplitJoin(name ? String(name) : "");
  if (!s) throw new GameError("name_missing");
  if (pyLen(s) > 30) throw new GameError("name_too_long", { max: 30 });
  return s;
}

/** Known players, the most recent first, with their game counts (UI-16). */
export function players(save: SaveData): Player[] {
  const rows = [...save.players].sort((a, b) => a.id - b.id).map((p) => {
    const games = save.games.filter((g) => g.player_id === p.id);
    const last = games.reduce<string | null>((m, g) => (m === null || g.started_on > m ? g.started_on : m), null);
    return { p, games: games.length, won: games.filter((g) => g.result === "won").length, last };
  });
  rows.sort((a, b) => {
    const ka = a.last ?? a.p.created_on, kb = b.last ?? b.p.created_on;
    return ka < kb ? 1 : ka > kb ? -1 : 0;
  });
  return rows.map((r) => ({ name: r.p.name, games: r.games, won: r.won, last_played: r.last }));
}

/** The ID of a known player, or null; names match by casefold. */
function playerId(work: SaveData, name: string): number | null {
  const key = casefold(name);
  return [...work.players].sort((a, b) => a.id - b.id).find((p) => casefold(p.name) === key)?.id ?? null;
}

/** Question IDs burned for this player or for everyone; null: only the global burns. */
function burnedFor(work: SaveData, pid: number | null): Set<string> {
  return new Set(work.burned.filter((b) => b.player_id === null || b.player_id === pid).map((b) => b.question_id));
}

/** Delete a player completely (GF-7): the player, their games (a running one too) and their burns. */
export function deletePlayer(save: SaveData, name: unknown): { save: SaveData } {
  return transact(save, (work) => {
    const pid = playerId(work, cleanName(name));
    if (pid === null) throw new GameError("player_unknown", { name });
    work.burned = work.burned.filter((b) => b.player_id !== pid);
    work.games = work.games.filter((g) => g.player_id !== pid);
    work.players = work.players.filter((p) => p.id !== pid);
  });
}

interface Latest {
  row: GameRow;
  state: GameState;
}

/** The newest game with its state (a copy, defaults filled in), or null. */
function latest(work: SaveData): Latest | null {
  const row = work.games.reduce<GameRow | null>((m, g) => (m === null || g.id > m.id ? g : m), null);
  return row ? { row, state: withDefaults(structuredClone(row.state)) } : null;
}

function saveGame(row: GameRow, state: GameState, io: Io, result: Result = null): void {
  row.state = structuredClone(state);
  row.result = result;
  row.finished_on = result ? io.now : null;
}

function running(work: SaveData): Latest {
  const game = latest(work);
  if (!game || game.row.result !== null) throw new GameError("no_game");
  return game;
}

function question(data: EngineData, id: string | null): PoolQuestion {
  const q = id === null ? undefined : data.byId.get(id);
  if (!q) throw new Error(`KeyError: ${id}`);
  return q;
}

function askedCategories(state: GameState, data: EngineData): Set<string | null> {
  const cat = categoryOf(data.broad);
  return new Set(state.history.filter((h) => data.byId.has(h.question_id)).map((h) => cat(data.byId.get(h.question_id)!)));
}

/** Questions that can still come up in this game: approved, not burned, not offered, not purged. */
export function availableNow(work: SaveData, pid: number | null, state: GameState, data: EngineData): PoolQuestion[] {
  const purged = new Set<string | null>(state.purged);
  return selection.available(data.pool, burnedFor(work, pid), state.offered).filter((q) => !purged.has(q.subcategory));
}

/** Draw n cards for the state's level from what's still available to the player in this game. */
function draw(
  work: SaveData, pid: number | null, state: GameState, data: EngineData, io: Io,
  n = selection.PER_LEVEL, keep: PoolQuestion[] = [],
): string[] {
  const drawn = selection.draw(state.level, availableNow(work, pid, state, data), {
    n, keep, avoidCategories: askedCategories(state, data), categoryOf: categoryOf(data.broad), rng: io.rng,
  });
  if (drawn === null) {
    const [lo, hi] = selection.LEVEL_RANGES[state.level];
    throw new GameError("level_empty", { level: state.level, lo, hi });
  }
  state.offered.push(...drawn.map((q) => q.id));
  return drawn.map((q) => q.id);
}

/** Burn a question for the player, or for everyone with pid null (D-28); INSERT OR IGNORE. */
function burn(work: SaveData, qid: string, pid: number | null, gid: number, io: Io): void {
  if (work.burned.some((b) => b.question_id === qid && b.player_id === pid)) return;
  work.burned.push({ question_id: qid, player_id: pid, game_id: gid, burned_on: io.now });
}

/** The supply check before a new game (GF-5); no name or a new one: the pool minus the global burns. */
export function supply(save: SaveData, data: EngineData, player?: unknown): Supply {
  const pid = player ? playerId(save, cleanName(player)) : null;
  const avail = selection.available(data.pool, burnedFor(save, pid));
  const levels = selection.supply(avail);
  return { ok: !levels.some((l) => l.missing), available: avail.length, levels };
}

/** Start a game for `player` (known or new, D-28); a running game is abandoned. */
export function newGame(save: SaveData, data: EngineData, io: Io, player: unknown): { save: SaveData; state: GameState } {
  const name = cleanName(player);
  const report = supply(save, data, name);
  if (!report.ok) {
    const short = report.levels.filter((l) => l.missing)
      .map((l) => ({ level: l.level, lo: l.range[0], hi: l.range[1], missing: l.missing }));
    throw new GameError("supply_short", { levels: short }, report);
  }
  return action(save, (work) => {
    const game = latest(work);
    if (game && game.row.result === null) saveGame(game.row, game.state, io, "abandoned");
    let pid = playerId(work, name);
    if (pid === null) {
      pid = nextId(work.players);
      work.players.push({ id: pid, name, created_on: io.now });
    }
    const state = withDefaults({
      level: 1, phase: "select", options: [], offered: [], current: null,
      answers: [], history: [], last: null, undo: null,
    } as unknown as GameState);
    state.options = draw(work, pid, state, data, io);
    work.games.push({
      id: nextId(work.games), started_on: io.now, finished_on: null, result: null, player_id: pid,
      state: structuredClone(state),
    });
    return state;
  });
}

function action(save: SaveData, fn: (work: SaveData) => GameState): { save: SaveData; state: GameState } {
  const { save: out, result } = transact(save, fn);
  return { save: out, state: result };
}

export function pick(save: SaveData, data: EngineData, io: Io, index: number): { save: SaveData; state: GameState } {
  return action(save, (work) => {
    const { row, state } = running(work);
    if (state.phase !== "select") throw new GameError("no_cards");
    if (!(0 <= index && index < state.options.length)) throw new GameError("card_invalid", { n: index + 1 });
    const q = question(data, state.options[index]);
    const answers = [q.answer, ...q.wrong_answers];
    io.rng.shuffle(answers, "pick");
    Object.assign(state, { phase: "question", current: q.id, answers, repeat: false });
    saveGame(row, state, io);
    return state;
  });
}

/** The final answer: check it, burn the question, move on (next level, won or lost). */
export function answer(save: SaveData, data: EngineData, io: Io, index: number): { save: SaveData; state: GameState } {
  return action(save, (work) => {
    const { row, state } = running(work);
    const pid = row.player_id;
    if (state.phase !== "question") throw new GameError("no_question");
    if (!(0 <= index && index < state.answers.length) || state.struck.includes(index))
      throw new GameError("answer_invalid", { n: index + 1 });
    const q = question(data, state.current);
    const before: GameState = { ...structuredClone(state), undo: null };
    const correct = state.answers[index] === q.answer;
    burn(work, q.id, pid, row.id, io);
    state.history.push({ level: state.level, question_id: q.id, correct, jokers: state.jokers });
    state.last = { question_id: q.id, chosen: index, correct, correct_index: state.answers.indexOf(q.answer) };
    state.undo = before;
    let result: Result = null;
    if (!correct) {
      state.phase = result = "lost";
    } else if (state.level === selection.LEVELS) {
      state.phase = result = "won";
    } else {
      Object.assign(state, { level: state.level + 1, phase: "select" });
      leaveQuestion(state);
      state.options = draw(work, pid, state, data, io);
    }
    saveGame(row, state, io, result);
    return state;
  });
}

/** Reset what belongs to the question on screen. */
export function leaveQuestion(state: GameState): void {
  Object.assign(state, { current: null, answers: [], hints_shown: 0, struck: [], jokers: [], swapped_to: null });
}

/** Burn the question on screen (for `burnFor`: a player ID, or null = everyone) and log it. */
export function dropCurrent(
  work: SaveData, gid: number, state: GameState, outcome: Outcome, burnFor: number | null, io: Io,
): void {
  burn(work, state.current!, burnFor, gid, io);
  state.history.push({ level: state.level, question_id: state.current!, outcome, jokers: state.jokers });
}

/** Drop the question on screen and refill the table (admin skip, «Paso»). With `purge`, its
 * subcategory leaves the game and its other cards on the table are replaced too (not burned). */
export function backToSelect(
  work: SaveData, gid: number, pid: number | null, state: GameState, data: EngineData, io: Io,
  outcome: Outcome, burnFor: number | null, purge = false,
): void {
  const sub = question(data, state.current).subcategory;
  dropCurrent(work, gid, state, outcome, burnFor, io);
  const removed = new Set([state.current!]);
  if (purge) {
    state.purged.push(sub as string);
    for (const i of state.options) if (question(data, i).subcategory === sub) removed.add(i);
  }
  const keep = state.options.filter((i) => !removed.has(i)).map((i) => question(data, i));
  let fresh: string[];
  try {
    fresh = draw(work, pid, state, data, io, removed.size, keep);
  } catch (e) {
    if (e instanceof GameError) throw new GameError(purge ? "purge_short" : "refill_empty");
    throw e;
  }
  state.options = state.options.map((i) => (removed.has(i) ? fresh.shift()! : i));
  state.phase = "select";
  leaveQuestion(state);
}

/** «Saltar pregunta» (admin): burn the question on screen for the player (for everyone with
 * `everyone`, D-28); a new card replaces it. Not a joker. */
export function skip(save: SaveData, data: EngineData, io: Io, everyone = false): { save: SaveData; state: GameState } {
  return action(save, (work) => {
    const { row, state } = running(work);
    if (state.phase !== "question") throw new GameError("skip_not_question");
    backToSelect(work, row.id, row.player_id, state, data, io,
      everyone ? "admin_burn" : "admin_skip", everyone ? null : row.player_id);
    saveGame(row, state, io);
    return state;
  });
}

/** Per joker: uses left in this game, or null = unlimited (MD-1). */
export function jokersLeft(state: GameState): JokerBudget {
  const used = [...state.history.flatMap((h) => h.jokers ?? []), ...state.jokers];
  return Object.fromEntries(Object.entries(state.settings.jokers).map(([name, limit]) =>
    [name, limit === null ? null : Math.max(0, limit - used.filter((j) => j === name).length)])) as JokerBudget;
}

/** Set the running game's joker budget (MD-4): {joker: count or null}; missing jokers stay. */
export function setJokers(save: SaveData, io: Io, budget: unknown): { save: SaveData; state: GameState } {
  if (budget === null || typeof budget !== "object" || Array.isArray(budget)
    || !Object.keys(budget).every((k) => (JOKERS as string[]).includes(k)))
    throw new GameError("budget_unknown_joker");
  for (const v of Object.values(budget))
    if (v !== null && !(Number.isInteger(v) && 0 <= (v as number) && (v as number) <= 99)) throw new GameError("budget_invalid");
  return action(save, (work) => {
    const { row, state } = running(work);
    Object.assign(state.settings.jokers, budget);
    saveGame(row, state, io);
    return state;
  });
}

/** Take back the last final answer: restore the state before it, un-burn the question for the player. */
export function undo(save: SaveData, io: Io): { save: SaveData; state: GameState } {
  return action(save, (work) => {
    const game = latest(work);
    if (!game || game.row.result === "abandoned" || !game.state.undo) throw new GameError("nothing_to_undo");
    const { row, state } = game;
    const qid = state.last!.question_id;
    work.burned = work.burned.filter((b) => !(b.question_id === qid && b.player_id === row.player_id && b.game_id === row.id));
    const restored = { ...state.undo!, settings: state.settings };
    saveGame(row, restored, io);
    return restored;
  });
}

export function abandon(save: SaveData, io: Io): { save: SaveData } {
  return transact(save, (work) => {
    const game = latest(work);
    if (game && game.row.result === null) saveGame(game.row, game.state, io, "abandoned");
  });
}

/** The newest game as the TV sees it: no correct answer before the final answer. */
export function view(save: SaveData, data: EngineData, _io: Io): Game | null {
  const game = latest(save);
  if (!game) return null;
  const { row, state } = game;
  const result = row.result;
  const by = data.byId;
  const jokers = null; // jokers_view: task 78
  const out: Game = {
    id: row.id, player: save.players.find((p) => p.id === row.player_id)?.name ?? null, result,
    level: state.level, phase: state.phase,
    options: state.options.filter((i) => by.has(i)).map((i) => ({ description: by.get(i)!.description })),
    history: state.history.filter((h) => h.correct !== undefined).map((h) => ({ level: h.level, correct: h.correct! })),
    can_undo: Boolean(state.undo) && result !== "abandoned",
    purged: state.purged, repeat: state.repeat, jokers,
    settings: state.settings, jokers_left: jokersLeft(state), question: null, last: null,
  };
  const q = state.current === null ? undefined : by.get(state.current);
  if (q) {
    // Only the hints shown through «Soplo» (D-26, D-27); no description (04, "Question").
    out.question = {
      id: q.id, question: q.question, media: q.media, background: q.background,
      answers: state.answers, hints: q.hints.slice(0, state.hints_shown),
      struck: state.struck, swapped_to: state.swapped_to,
    };
  }
  const last = state.last && by.get(state.last.question_id);
  if (state.last && last) out.last = { ...state.last, answer: last.answer, fun_fact: last.fun_fact };
  return out;
}
