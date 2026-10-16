// The referee (PORT-3, plan 20): port of the former app/server/game.py (deleted in PORT-8). Public functions are pure:
// (save, data, io, …) → {save, …}; inside, they mutate a transact() copy like the Python port.
import type { Choice, Game, GameMode, JokerBudget, JokerEvent, JokerName, JokerState, Jokers, Player, Supply } from "../lib/types.ts";
import type { ChoiceInput } from "./choice.ts";
import { CLAIM_MS, HINT_MS, JOKERS, LIVES, QUESTION_MS, STANDARD_JOKERS, checkBudget, checkCount, defaultChoice, gameChoice, mediaAllowed, rangesFor, resolveChoice } from "./choice.ts";
import type { LevelRanges, PoolQuestion } from "./pool.ts";
import { catKey, categoryOf, subKey, subOf } from "./pool.ts";
import { casefold, pyLen, pySplitJoin, pyTruthy } from "./pycompat.ts";
import * as selection from "./selection.ts";
import type { EngineData, GameRow, GameState, Io, Outcome, SaveData, Seat, TimedState } from "./state.ts";
import { GameError, UNLIMITED, gameLocale, newest, nextId, rowPlayers, rowStates, seatResult, transact, trial, withDefaults } from "./state.ts";

export { GameError, UNLIMITED };
export {
  CARDS_MAX, CHOICE_KEYS, CLAIM_MS, DEFAULT_AGE_GROUP, DIFFICULTY_MAX, LEVELS_MAX, QUESTION_MS, STANDARD_JOKERS, defaultChoice,
  gameChoice, rangesFor, resolveChoice,
} from "./choice.ts";

export const MODES: readonly GameMode[] = ["gamemaster", "solo", "rr-coop", "rr-competitive", "timed"];
/** Playable so far (plan 36); the multiplayer modes come with MD-8. */
export const BUILT_MODES: readonly GameMode[] = ["gamemaster", "solo"];

/** The game's mode; missing = gamemaster (games from before plan 36). */
export const gameMode = (state: GameState): GameMode => state.settings.mode ?? "gamemaster";

/** Undo, skip, joker budget and the other cheats: gamemaster mode only (D-74, D-88). */
function gamemasterOnly(state: GameState, what: string): void {
  if (gameMode(state) !== "gamemaster") throw new GameError("gamemaster_only", { action: what });
}

type Result = GameRow["result"];

/** Fewest seats in a session. */
const MIN_SEATS = 2;

/** The acting seat of an action (plan 157): index into `row.seats`, 0 in a one-player game; refused before any mode logic. */
export function actor(row: GameRow, seat: unknown): number {
  if (!row.seats) {
    if (seat === undefined || seat === 0) return 0;
    throw new GameError("seat_unknown");
  }
  if (seat === undefined || seat === null) throw new GameError("seat_missing");
  if (typeof seat !== "number" || !Number.isInteger(seat) || seat < 0 || seat >= row.seats.length) throw new GameError("seat_unknown");
  if (row.seats[seat].out) throw new GameError("seat_out");
  const mode = gameMode(row.state);
  if ((mode === "rr-coop" || mode === "rr-competitive") && seat !== row.turn) throw new GameError("not_your_turn");
  return seat;
}

/** The newest running game's actor check (every action but `new` and `abandon`); no game: left to the action's `no_game`. */
export function checkActor(save: SaveData, seat: unknown): void {
  const row = newest(save.games);
  if (row && row.result === null) actor(row, seat);
  else if (seat !== undefined && seat !== 0 && seat !== null) throw new GameError("seat_unknown");
}

/** Longest player name, in code points. */
export const MAX_NAME = 30;

/** A player name as typed: trimmed, inner spaces collapsed; GameError if empty or too long. */
export function cleanName(name: unknown): string {
  const s = pySplitJoin(name ? String(name) : "");
  if (!s) throw new GameError("name_missing");
  if (pyLen(s) > MAX_NAME) throw new GameError("name_too_long", { max: MAX_NAME });
  return s;
}

/** Session names (join order) as `players[]` ids: known names reuse their row, new ones get one. */
function seatPlayers(work: SaveData, names: string[], io: Io): number[] {
  return names.map((name) => {
    let pid = playerId(work, name);
    if (pid === null) {
      pid = nextId(work.players);
      work.players.push({ id: pid, name, created_on: io.now });
    }
    return pid;
  });
}

/** Known players, the most recent first, with their game counts (UI-16). */
export function players(save: SaveData): Player[] {
  const rows = [...save.players].sort((a, b) => a.id - b.id).map((p) => {
    const games = save.games.flatMap((g) => rowPlayers(g).flatMap((id, i) => (id === p.id ? [{ g, i }] : [])));
    const last = games.reduce<string | null>((m, { g }) => (m === null || g.started_on > m ? g.started_on : m), null);
    return { p, games: games.length, won: games.filter(({ g, i }) => seatResult(g, i) === "won").length, last }; // `completed`: not a win (D-105)
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

/** Seen count per question: rows in the whole save, every player and mode (plan 65). */
export function countOf(save: SaveData): (q: PoolQuestion) => number {
  const counts = new Map<string, number>();
  for (const s of save.seen) counts.set(s.question_id, (counts.get(s.question_id) ?? 0) + 1);
  return (q) => counts.get(q.id) ?? 0;
}

/** Delete a player (GF-7): the name and their games (a running one too); the seen rows stay. A session stays
 * with the seat's player_id null, abandoned if it was running. */
export function deletePlayer(save: SaveData, name: unknown, io: Io): { save: SaveData } {
  return transact(save, (work) => {
    const pid = playerId(work, cleanName(name));
    if (pid === null) throw new GameError("player_unknown", { name });
    const gone = new Set(work.games.filter((g) => g.player_id === pid).map((g) => g.id));
    for (const s of work.seen) if (gone.has(s.game_id)) s.game_id = 0;
    work.games = work.games.filter((g) => g.player_id !== pid);
    for (const g of work.games) {
      const seats = g.seats?.filter((x) => x.player_id === pid) ?? [];
      for (const x of seats) x.player_id = null;
      if (seats.length && g.result === null) {
        g.result = "abandoned";
        g.finished_on = io.now;
      }
    }
    work.players = work.players.filter((p) => p.id !== pid);
  });
}

interface Latest {
  row: GameRow;
  state: GameState;
}

/** The newest game with its state (a copy, defaults filled in), or null. */
function latest(work: SaveData): Latest | null {
  const row = newest(work.games);
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

/** The game `seat` plays (a copy, defaults filled in): rr-competitive's own, else the row's. */
function seatState(row: GameRow, seat: number): GameState {
  return withDefaults(structuredClone(row.seats?.[seat]?.state ?? row.state));
}

/** Save `state` back where `seatState` found it. */
function saveSeat(row: GameRow, seat: number, state: GameState, io: Io): void {
  const own = row.seats?.[seat];
  if (own?.state) own.state = structuredClone(state);
  else saveGame(row, state, io);
}

/** The next seat on turn after `seat`, in join order, skipping out seats. */
function nextTurn(seats: Seat[], seat: number): number {
  for (let i = 1; i < seats.length; i++) if (!seats[(seat + i) % seats.length].out) return (seat + i) % seats.length;
  return seat;
}

function question(data: EngineData, id: string | null): PoolQuestion {
  const q = id === null ? undefined : data.byId.get(id);
  if (!q) throw new Error(`KeyError: ${id}`);
  return q;
}

function askedCategories(state: GameState, data: EngineData): Set<string | null> {
  const cat = categoryOf(data.broad);
  return new Set(state.history.flatMap((h) => {
    const q = data.byId.get(h.question_id);
    return q ? [cat(q)] : [];
  }));
}

const rangesOf = (state: GameState, data: EngineData): LevelRanges => rangesFor(data, gameChoice(state, data));

/** The game's number of levels and cards per level (D-88). */
const levelCount = (state: GameState): number => state.settings.levels ?? selection.LEVELS;
const cardsOf = (state: GameState): number => state.settings.cards ?? selection.PER_LEVEL;
/** Questions the table and the supply need per level: with 0 cards still one. */
const perLevel = (cards: number): number => Math.max(cards, 1);

/** What a game with `choice` could draw: approved, not blocked, in `bundles`, media allowed; any seen count. */
export function availableFor(save: SaveData, data: EngineData, choice: Choice, bundles: Iterable<string> = choice.bundles): PoolQuestion[] {
  return selection.available(data.pool, save.blocked, [], new Set(bundles)).filter(mediaAllowed(choice));
}

/** rr-competitive: what the session's seats hold (no card twice in a session, plan 158): every seat's offered, with
 * `tables` only their tables. The state's own seat in `work` may be stale; its `offered` covers that. */
function sessionTaken(work: SaveData, state: GameState, tables: boolean): string[] {
  if (gameMode(state) !== "rr-competitive") return [];
  return newest(work.games)?.seats?.flatMap((s) => (s.state ? (tables ? s.state.options : s.state.offered) : [])) ?? [];
}

/** Questions that can still come up in this game: approved, not blocked, not offered, not purged; seen ones too.
 * rr-competitive: not held by another seat either (`sessionTaken`). */
function availableNow(work: SaveData, state: GameState, data: EngineData, tables = false): PoolQuestion[] {
  const purged = new Set<string | null>(state.purged);
  const bundles = new Set(gameChoice(state, data).bundles);
  const media = mediaAllowed(state.settings);
  return selection.available(data.pool, work.blocked, [...state.offered, ...sessionTaken(work, state, tables)], bundles)
    .filter((q) => !purged.has(subOf(q)) && media(q));
}

/** Draw n cards for the state's level from what's still available in this game, lowest seen count first. */
function draw(
  work: SaveData, state: GameState, data: EngineData, io: Io, n = perLevel(cardsOf(state)), keep: PoolQuestion[] = [],
): string[] {
  const ranges = rangesOf(state, data);
  const opts = {
    ranges, n, perLevel: perLevel(cardsOf(state)), keep, avoidCategories: askedCategories(state, data), categoryOf: categoryOf(data.broad),
    countOf: countOf(work), rng: io.rng,
  };
  let drawn = selection.draw(state.level, availableNow(work, state, data), opts);
  // rr-competitive: other seats' past questions rather than none
  if (drawn === null && gameMode(state) === "rr-competitive") drawn = selection.draw(state.level, availableNow(work, state, data, true), opts);
  if (drawn === null) {
    const [lo, hi] = ranges[state.level - 1];
    throw new GameError("level_empty", { level: state.level, lo, hi });
  }
  state.offered.push(...drawn.map((q) => q.id));
  return drawn.map((q) => q.id);
}

/** One seen event (plan 65): a row per event, no dedupe. */
function see(work: SaveData, qid: string, gid: number, io: Io): void {
  work.seen.push({ question_id: qid, game_id: gid, seen_on: io.now });
}

/** «Bloquear pregunta»: a broken question, never offered again. */
function block(work: SaveData, qid: string): void {
  if (!work.blocked.includes(qid)) work.blocked.push(qid);
}

/** The supply check before a new game (GF-5): the pool minus blocked, any seen count (plan 65).
 * `choice`: the whole configuration, default defaultChoice. */
export function supply(save: SaveData, data: EngineData, choice: Choice = defaultChoice(data)): Supply {
  const avail = availableFor(save, data, choice);
  const levels = selection.supply(avail, rangesFor(data, choice), perLevel(choice.cards));
  return { ok: !levels.some((l) => l.missing), available: avail.length, levels };
}

/** rr-competitive's supply check: one matching over every seat's levels (seat × level), each seat with its own
 * ranges; `choices` per seat, the same but for the age group. */
function seatsSupply(save: SaveData, data: EngineData, choices: Choice[]): Supply {
  const avail = availableFor(save, data, choices[0]);
  const ranges = choices.flatMap((c) => rangesFor(data, c));
  const n = choices[0].levels;
  const levels = selection.supply(avail, ranges, perLevel(choices[0].cards))
    .map((l) => ({ ...l, level: (l.level - 1) % n + 1, seat: Math.floor((l.level - 1) / n) }));
  return { ok: !levels.some((l) => l.missing), available: avail.length, levels };
}

/** «supply_short» naming the levels that miss questions; `report` goes to the client. */
function supplyShort(report: Supply): GameError {
  const short = report.levels.filter((l) => l.missing)
    .map((l) => ({ level: l.level, lo: l.range[0], hi: l.range[1], missing: l.missing, ...(l.seat === undefined ? {} : { seat: l.seat }) }));
  return new GameError("supply_short", { levels: short }, report);
}

/** What a new game may get from the request body besides the player (plan 27, plan 36, D-88). */
export interface ChoiceArgs extends ChoiceInput {
  mode?: unknown;
  /** Overrides of the mode's joker set (not of `Choice.jokers`); in `solo` a difference sets `customized`. */
  jokers?: unknown;
  /** rr-competitive: one age group per player, join order; a missing entry = `age_group`. */
  age_groups?: unknown;
}

function newestGame(save: SaveData, player?: unknown): GameRow | null {
  const pid = player ? playerId(save, cleanName(player)) : null;
  return pid === null ? null
    : newest(save.games.filter((g) => g.player_id === pid));
}

/** The mode of the player's newest game if built, else gamemaster (MD-7). */
export function playerMode(save: SaveData, player?: unknown): GameMode {
  const row = newestGame(save, player);
  const mode = row ? gameMode(withDefaults(structuredClone(row.state))) : "gamemaster";
  return BUILT_MODES.includes(mode) ? mode : "gamemaster";
}

/** The choice of the player's newest game (its budget as now), else the defaults with the first base
 * bundle only (pm decision 33). */
export function playerChoice(save: SaveData, data: EngineData, player?: unknown): Choice {
  const row = newestGame(save, player);
  if (row) return gameChoice(withDefaults(structuredClone(row.state)), data);
  const d = defaultChoice(data);
  return { ...d, bundles: d.bundles.filter((id) => data.bundles.find((b) => b.id === id)?.kind === "base") };
}

/** A new game's state before the first table: settings from `args` as `newGame` documents. */
function freshState(args: ChoiceArgs, choice: Choice, mode: GameMode, overrides: Partial<JokerBudget>): GameState {
  const state = withDefaults({
    level: 1, phase: "select", options: [], offered: [], current: null,
    answers: [], history: [], last: null, undo: null,
  } as unknown as GameState);
  if (choice.difficulty) state.settings.difficulty = choice.difficulty;
  else if (args.age_group !== undefined) state.settings.age_group = choice.age_group!;
  if (args.bundles !== undefined) state.settings.bundles = choice.bundles;
  if (args.levels !== undefined) state.settings.levels = choice.levels;
  if (args.cards !== undefined) state.settings.cards = choice.cards;
  if (!choice.video) state.settings.video = false;
  if (!choice.audio) state.settings.audio = false;
  if (!choice.answers) state.settings.answers = false;
  if (args.mode !== undefined) state.settings.mode = mode;
  if (mode === "gamemaster") Object.assign(state.settings.jokers, overrides);
  else {
    const jokers = { ...STANDARD_JOKERS, ...overrides };
    state.settings.jokers = jokers;
    state.settings.customized = JOKERS.some((j) => jokers[j] !== STANDARD_JOKERS[j]);
  }
  return state;
}

/** Start a game for `player` (known or new, D-28); a running game is abandoned. The settings get
 * `age_group` / `difficulty` / `bundles` / `mode` / `levels` / `cards` only when `args` carries them,
 * `video` / `audio` / `answers` only when off; `answers` in gamemaster mode only (D-105). */
export function newGame(
  save: SaveData, data: EngineData, io: Io, player: unknown, args: ChoiceArgs = {},
): { save: SaveData; state: GameState } {
  const name = cleanName(player);
  const locale = data.locale; // the question locale (plan 126): the caller loads its pool
  const { jokers: _, ...rest } = args;
  const choice = resolveChoice(data, rest);
  const mode = args.mode ?? "gamemaster";
  if (!(MODES as unknown[]).includes(mode)) throw new GameError("mode_unknown", { mode: String(mode) });
  if (args.answers !== undefined && mode !== "gamemaster") throw new GameError("gamemaster_only", { action: "answers" });
  const overrides = args.jokers === undefined ? {} : checkBudget(args.jokers);
  const report = supply(save, data, choice);
  if (!report.ok) throw supplyShort(report);
  return action(save, (work) => {
    const game = latest(work);
    if (game && game.row.result === null) saveGame(game.row, game.state, io, "abandoned");
    let pid = playerId(work, name);
    if (pid === null) {
      pid = nextId(work.players);
      work.players.push({ id: pid, name, created_on: io.now });
    }
    const state = freshState(args, choice, mode as GameMode, overrides);
    deal(work, state, data, io);
    work.games.push({
      id: nextId(work.games), started_on: io.now, finished_on: null, result: null, player_id: pid,
      ...(locale === "es" ? {} : { locale }), state: structuredClone(state),
    });
    return state;
  });
}

/** `new` for a session (body `players`, join order; plan 158): rr-coop plays in `row.state`, the seats carry no state;
 * rr-competitive: every seat its own game (`age_groups`), `row.state` the shared settings only; timed (plan 159): the
 * shared question flow in `row.state`, no jokers, no cards, N questions per level, lives per seat, no turn.
 * Unbuilt modes start here too; `api.ts` refuses them (`mode_not_built`). */
export function newSession(
  save: SaveData, data: EngineData, io: Io, players: unknown, args: ChoiceArgs = {},
): { save: SaveData; state: GameState } {
  const mode = args.mode ?? "gamemaster";
  if (!(MODES as unknown[]).includes(mode)) throw new GameError("mode_unknown", { mode: String(mode) });
  if (!Array.isArray(players)) throw new GameError("players_too_few", { min: MIN_SEATS });
  const names = players.map(cleanName);
  if (new Set(names.map(casefold)).size < names.length) {
    const seen = new Set<string>();
    throw new GameError("player_twice", { name: names.find((n) => seen.size === seen.add(casefold(n)).size)! });
  }
  if (names.length < MIN_SEATS) throw new GameError("players_too_few", { min: MIN_SEATS });
  if (mode === "gamemaster" || mode === "solo") throw new GameError("mode_single", { mode });
  const timed = mode === "timed";
  const { jokers: _, age_groups, ...rest } = timed ? { ...args, cards: 0 } : args;
  const choice = resolveChoice(data, rest);
  if (args.answers !== undefined) throw new GameError("gamemaster_only", { action: "answers" });
  if (timed && args.jokers !== undefined) throw new GameError("timed_no_jokers");
  const overrides = args.jokers === undefined ? {} : checkBudget(args.jokers);
  const competitive = mode === "rr-competitive";
  if (age_groups !== undefined && !Array.isArray(age_groups)) throw new GameError("age_group_unknown", { group: String(age_groups) });
  const groups = (age_groups ?? []) as unknown[];
  const seatArgs = names.map((_, i) => (groups[i] == null ? rest : { ...rest, age_group: groups[i] }));
  const choices = competitive ? seatArgs.map((a) => resolveChoice(data, a)) : [choice];
  const report = competitive ? seatsSupply(save, data, choices)
    : supply(save, data, timed ? { ...choice, cards: names.length } : choice);
  if (!report.ok) throw supplyShort(report);
  return action(save, (work) => {
    const game = latest(work);
    if (game && game.row.result === null) saveGame(game.row, game.state, io, "abandoned");
    const ids = seatPlayers(work, names, io);
    const row: GameRow = {
      id: nextId(work.games), started_on: io.now, finished_on: null, result: null, player_id: null,
      ...(data.locale === "es" ? {} : { locale: data.locale }), ...(timed ? {} : { turn: 0 }),
      seats: ids.map((player_id, i) => (competitive
        ? { player_id, state: freshState({ ...seatArgs[i], age_group: choices[i].age_group ?? undefined }, choices[i], mode as GameMode, overrides) }
        : timed ? { player_id, lives: LIVES } : { player_id })),
      state: freshState(competitive ? { ...rest, age_group: undefined } : timed ? rest : args, choice, mode as GameMode, overrides),
    };
    work.games.push(row);
    if (timed) timedStart(work, row, data, io);
    else if (!competitive) deal(work, row.state, data, io);
    // one seat after the other: each draw sees the tables dealt before it
    for (const seat of row.seats!) if (seat.state) deal(work, seat.state, data, io);
    return seatState(row, 0);
  });
}

function action(save: SaveData, fn: (work: SaveData) => GameState): { save: SaveData; state: GameState } {
  const { save: out, result } = transact(save, fn);
  return { save: out, state: result };
}

/** Turn card `index` over: its question goes on screen. */
function open(state: GameState, data: EngineData, io: Io, index: number): void {
  const q = question(data, state.options[index]);
  const answers = [q.answer, ...q.wrong_answers];
  io.rng.shuffle(answers, "pick");
  Object.assign(state, { phase: "question", current: q.id, answers, repeat: false });
}

/** With `cards: 0` (D-88) the one card on the table opens at once. */
function openIfNoCards(state: GameState, data: EngineData, io: Io): void {
  if (cardsOf(state) === 0 && state.phase === "select") open(state, data, io, 0);
}

/** A new table for the state's level. */
function deal(work: SaveData, state: GameState, data: EngineData, io: Io): void {
  state.options = draw(work, state, data, io);
  openIfNoCards(state, data, io);
}

export function pick(save: SaveData, data: EngineData, io: Io, index: number, seat?: unknown): { save: SaveData; state: GameState } {
  return action(save, (work) => {
    const { row } = running(work);
    const who = actor(row, seat);
    const state = seatState(row, who);
    if (state.phase !== "select") throw new GameError("no_cards");
    if (!(0 <= index && index < state.options.length)) throw new GameError("card_invalid", { n: index + 1 });
    open(state, data, io, index);
    saveSeat(row, who, state, io);
    return state;
  });
}

/** The final answer: check it, record it as seen, move on (next level, won or lost). */
export function answer(save: SaveData, data: EngineData, io: Io, index: number, seat?: unknown): { save: SaveData; state: GameState } {
  return action(save, (work) => {
    const { row } = running(work);
    const who = actor(row, seat);
    if (gameMode(row.state) === "timed") return timedAnswer(work, row, who, index, data, io);
    const state = seatState(row, who);
    if (state.phase !== "question") throw new GameError("no_question");
    if (state.settings.answers === false) throw new GameError("answers_off");
    if (!(0 <= index && index < state.answers.length) || state.struck.includes(index))
      throw new GameError("answer_invalid", { n: index + 1 });
    const q = question(data, state.current);
    const before: GameState = { ...structuredClone(state), undo: null };
    const correct = state.answers[index] === q.answer;
    see(work, q.id, row.id, io);
    const by = row.seats ? { seat: who } : {};
    state.history.push({ level: state.level, question_id: q.id, correct, jokers: state.jokers, ...by });
    state.last = { question_id: q.id, chosen: index, correct, correct_index: state.answers.indexOf(q.answer), ...by };
    state.undo = before;
    let result: Result = null;
    if (!correct) {
      state.phase = result = "lost";
    } else if (state.level >= levelCount(state)) {
      state.phase = result = "won";
    } else {
      Object.assign(state, { level: state.level + 1, phase: "select" });
      leaveQuestion(state);
      deal(work, state, data, io);
    }
    if (row.seats?.[who].state) seatAnswered(row, who, state, io);
    else saveGame(row, state, io, result);
    if (row.seats && row.result === null) row.turn = nextTurn(row.seats, who);
    return state;
  });
}

/** rr-competitive after a final answer: the seat's game back into its seat, the session's `last` into `row.state`; a wrong
 * answer puts the seat out; its win at the last level or the last seat in (decision 278) ends the session. */
function seatAnswered(row: GameRow, who: number, state: GameState, io: Io): void {
  const seats = row.seats!;
  if (state.phase === "lost") Object.assign(seats[who], { out: true, result: "lost" });
  const left = seats.flatMap((s, i) => (s.out ? [] : [i]));
  const winner = state.phase === "won" ? who : left.length === 1 ? left[0] : null;
  seats[who].state = structuredClone(state);
  const shared = withDefaults(structuredClone(row.state));
  shared.last = state.last;
  if (winner !== null) {
    for (const i of left) seats[i].result = i === winner ? "won" : "lost";
    seats[winner].state!.phase = shared.phase = "won";
  }
  saveGame(row, shared, io, winner === null ? null : "won");
}

/** With answers off (D-105): the correct answer is shown, seen, one level up; after the last level `completed`. */
export function reveal(save: SaveData, data: EngineData, io: Io): { save: SaveData; state: GameState } {
  return action(save, (work) => {
    const { row, state } = running(work);
    if (state.phase !== "question") throw new GameError("no_question");
    if (state.settings.answers !== false) throw new GameError("answers_on");
    const q = question(data, state.current);
    const before: GameState = { ...structuredClone(state), undo: null };
    see(work, q.id, row.id, io);
    state.history.push({ level: state.level, question_id: q.id, revealed: true, jokers: state.jokers });
    state.last = { question_id: q.id, chosen: null, correct: false, revealed: true, correct_index: state.answers.indexOf(q.answer) };
    state.undo = before;
    let result: Result = null;
    if (state.level >= levelCount(state)) {
      state.phase = result = "completed";
    } else {
      Object.assign(state, { level: state.level + 1, phase: "select" });
      leaveQuestion(state);
      deal(work, state, data, io);
    }
    saveGame(row, state, io, result);
    return state;
  });
}

/** Reset what belongs to the question on screen. */
function leaveQuestion(state: GameState): void {
  Object.assign(state, { current: null, answers: [], hints_shown: 0, struck: [], jokers: [], swapped_to: null });
}

/** Record the question on screen as seen (`block`: blocked instead) and log it. */
function dropCurrent(
  work: SaveData, gid: number, state: GameState, outcome: Outcome, io: Io, block_ = false,
): void {
  if (block_) block(work, state.current!);
  else see(work, state.current!, gid, io);
  state.history.push({ level: state.level, question_id: state.current!, outcome, jokers: state.jokers });
}

/** Drop the question on screen and refill the table (admin skip, «Paso»). With `purge`, its
 * subcategory leaves the game and its other cards on the table are replaced too (not seen). */
function backToSelect(
  work: SaveData, gid: number, state: GameState, data: EngineData, io: Io, outcome: Outcome, purge = false,
): void {
  const sub = subOf(question(data, state.current))!;
  dropCurrent(work, gid, state, outcome, io, outcome === "admin_block");
  const removed = new Set([state.current!]);
  if (purge) {
    state.purged.push(sub);
    for (const i of state.options) if (subOf(question(data, i)) === sub) removed.add(i);
  }
  const keep = state.options.filter((i) => !removed.has(i)).map((i) => question(data, i));
  let fresh: string[];
  try {
    fresh = draw(work, state, data, io, removed.size, keep);
  } catch (e) {
    if (e instanceof GameError) throw new GameError(purge ? "purge_short" : "refill_empty");
    throw e;
  }
  state.options = state.options.map((i) => (removed.has(i) ? fresh.shift()! : i));
  state.phase = "select";
  leaveQuestion(state);
  openIfNoCards(state, data, io);
}

/** «Saltar pregunta» (admin): the question on screen counts as seen (blocked with `everyone`,
 * «Bloquear pregunta»); a new card replaces it. Not a joker. */
export function skip(save: SaveData, data: EngineData, io: Io, everyone = false): { save: SaveData; state: GameState } {
  return action(save, (work) => {
    const { row, state } = running(work);
    gamemasterOnly(state, "skip");
    if (state.phase !== "question") throw new GameError("skip_not_question");
    backToSelect(work, row.id, state, data, io, everyone ? "admin_block" : "admin_skip");
    saveGame(row, state, io);
    return state;
  });
}

// Jokers (plans/09-jokers.md, JK-2) ---------------------------------------------------------------

type Fill = [Set<string>, boolean];

/** (question IDs the matching uses for the levels after `level`, whether they all fill); the game's
 * levels = `ranges.length`, `cards` per level. */
function laterFill(avail: PoolQuestion[], level: number, ranges: LevelRanges, cards = selection.PER_LEVEL): Fill {
  const { assignment, missing } = selection.assign(avail, laterLevels(level, ranges), ranges, perLevel(cards));
  return [new Set([...assignment.values()].flat()), missing.size === 0];
}

function laterLevels(level: number, ranges: LevelRanges): number[] {
  return Array.from({ length: ranges.length - level }, (_, i) => level + 1 + i);
}

/** The best of `cands` by (seen count, `order`) (random among ties) whose removal still lets every
 * later level fill (GF-2), or null. */
function replacement(
  avail: PoolQuestion[], level: number, ranges: LevelRanges, cands: PoolQuestion[], order: (q: PoolQuestion) => number,
  count: (q: PoolQuestion) => number, io: Io, fill?: Fill, cards = selection.PER_LEVEL,
): PoolQuestion | null {
  const [used, ok] = fill ?? laterFill(avail, level, ranges, cards);
  if (!ok) return null;
  const later = laterLevels(level, ranges);
  const list = [...cands];
  io.rng.shuffle(list, "replacement");
  list.sort((a, b) => count(a) - count(b) || order(a) - order(b));
  return list.find((q) => !used.has(q.id)
    || selection.assign(avail.filter((x) => x.id !== q.id), later, ranges, perLevel(cards)).missing.size === 0) ?? null;
}

function categoryCandidates(avail: PoolQuestion[], level: number, ranges: LevelRanges, sub: string): PoolQuestion[] {
  return avail.filter((q) => subOf(q) === sub && selection.inRange(q, level, ranges));
}

/** Replace the question on screen in place with `fresh` (Bájale, Cambiazo). */
function swapIn(work: SaveData, gid: number, state: GameState, fresh: PoolQuestion, outcome: Outcome, io: Io): void {
  dropCurrent(work, gid, state, outcome, io);
  putOn(state, fresh, io);
}

/** `fresh` takes the place of the question on screen (already logged). */
function putOn(state: GameState, fresh: PoolQuestion, io: Io): void {
  const old = state.current;
  const answers = [fresh.answer, ...fresh.wrong_answers];
  io.rng.shuffle(answers, "swap_in");
  state.options = state.options.map((i) => (i === old ? fresh.id : i));
  state.offered.push(fresh.id);
  leaveQuestion(state);
  Object.assign(state, { current: fresh.id, answers });
}

/** What a joker may get from the request body (api.ts passes only these). */
export interface JokerArgs {
  purge?: unknown;
  subcategory?: unknown;
  index?: unknown;
}

type Play = (work: SaveData, gid: number, state: GameState, data: EngineData, io: Io, args: JokerArgs) => object;

/** «Soplo»: show the next hint. */
const playHint: Play = (_work, _gid, state, data) => {
  if (state.hints_shown >= question(data, state.current).hints.length) throw new GameError("hints_used_up");
  state.hints_shown += 1;
  state.jokers.push("hint");
  return { hint: state.hints_shown };
};

/** «Paso»: back to Select with a new card; optionally the subcategory leaves the game. */
const playSkip: Play = (work, gid, state, data, io, { purge }) => {
  state.jokers.push("skip");
  const sub = subOf(question(data, state.current));
  backToSelect(work, gid, state, data, io, "skipped", pyTruthy(purge));
  return { purged: pyTruthy(purge) ? sub : null };
};

/** «Bájale»: an easier question of the same subcategory, the hardest of those below (09). */
const playEasier: Play = (work, gid, state, data, io) => {
  const cur = question(data, state.current);
  const avail = availableNow(work, state, data);
  const cands = avail.filter((q) => subOf(q) === subOf(cur) && q.difficulty < cur.difficulty);
  const fresh = replacement(avail, state.level, rangesOf(state, data), cands, (q) => -q.difficulty, countOf(work), io, undefined, cardsOf(state));
  if (!fresh) throw new GameError("easier_none");
  state.jokers.push("easier");
  swapIn(work, gid, state, fresh, "easier", io);
  return { from: cur.difficulty, to: fresh.difficulty };
};

/** «Cambiazo»: a question of the level's range from the chosen subcategory (its key), nearest difficulty first (09). */
const playCategory: Play = (work, gid, state, data, io, { subcategory }) => {
  const cur = question(data, state.current);
  if (typeof subcategory !== "string" || !data.broad.has(subcategory)) throw new GameError("category_unknown");
  if (subcategory === subOf(cur)) throw new GameError("category_same");
  const avail = availableNow(work, state, data);
  const ranges = rangesOf(state, data);
  const fresh = replacement(avail, state.level, ranges, categoryCandidates(avail, state.level, ranges, subcategory),
    (q) => Math.abs(q.difficulty - cur.difficulty), countOf(work), io, undefined, cardsOf(state));
  if (!fresh) throw new GameError("category_empty");
  state.jokers.push("category");
  swapIn(work, gid, state, fresh, "category", io);
  state.swapped_to = subcategory;
  return { subcategory };
};

/** «Francotirador» (JK-3): a wrong answer is struck out; the right one drops the question (seen) and repeats the level (D-27). */
const playSnipe: Play = (work, gid, state, data, io, { index }) => {
  if (state.settings.answers === false) throw new GameError("snipe_answers_off");
  if (state.answers.length - state.struck.length <= 1) throw new GameError("snipe_last");
  if (typeof index !== "number" || !Number.isInteger(index) || index < 0 || index >= state.answers.length
    || state.struck.includes(index))
    throw new GameError("snipe_invalid");
  const i = index;
  const q = question(data, state.current);
  state.jokers.push("snipe");
  const correctIndex = state.answers.indexOf(q.answer);
  if (i !== correctIndex) {
    state.struck.push(i);
    return { outcome: "miss", index: i };
  }
  dropCurrent(work, gid, state, "sniped", io);
  try {
    state.options = draw(work, state, data, io);
  } catch (e) {
    if (e instanceof GameError) throw new GameError("snipe_no_repeat");
    throw e;
  }
  state.phase = "select";
  leaveQuestion(state);
  openIfNoCards(state, data, io);
  state.repeat = true; // after open(), which clears it
  return { outcome: "hit", index: i, correct_index: correctIndex };
};

const PLAYS: Record<JokerName, Play> = {
  hint: playHint, skip: playSkip, easier: playEasier, category: playCategory, snipe: playSnipe,
};

/** Play a joker on the question on screen; `event` is what happened (for the animation). */
export function joker(
  save: SaveData, data: EngineData, io: Io, name: string, args: JokerArgs = {}, seat?: unknown,
): { save: SaveData; state: GameState; event: JokerEvent } {
  if (!(JOKERS as string[]).includes(name)) throw new GameError("joker_unknown", { joker: name });
  const jname = name as JokerName;
  const { save: out, result } = transact(save, (work) => {
    const { row } = running(work);
    const who = actor(row, seat);
    const state = seatState(row, who);
    if (gameMode(state) === "timed") throw new GameError("timed_no_jokers");
    if (state.phase !== "question") throw new GameError("joker_not_question");
    if (jokersLeft(state)[jname] === 0) throw new GameError("joker_spent", { joker: jname });
    const before = state.history.length;
    const event = PLAYS[jname](work, row.id, state, data, io, args);
    if (row.seats) for (const h of state.history.slice(before)) h.seat = who;
    saveSeat(row, who, state, io);
    return { state, event: { joker: jname, ...event } as JokerEvent };
  });
  return { save: out, ...result };
}

/** Per joker: available, and the reason if not (09, "Availability"); «Cambiazo» lists the possible subcategories. */
function jokersView(work: SaveData, row: GameRow, state: GameState, data: EngineData, io: Io): Jokers {
  const check = (fn: Play, args: JokerArgs = {}): JokerState => {
    const reason = trial(work, (c) => fn(c, row.id, structuredClone(state), data, io, args));
    return { available: reason === null, reason };
  };
  const cur = question(data, state.current);
  const hint = check(playHint), skipJ = check(playSkip), easier = check(playEasier);
  // Availability tries the worst case, a hit; the client only learns yes or no.
  const snipe = check(playSnipe, { index: state.answers.indexOf(cur.answer) });
  const purge = { ...check(playSkip, { purge: true }), subcategory: subOf(cur)! };

  const avail = availableNow(work, state, data);
  const ranges = rangesOf(state, data);
  const fill = laterFill(avail, state.level, ranges, cardsOf(state));
  const count = countOf(work);
  const active = new Set(gameChoice(state, data).bundles);
  const groups = data.categories.filter((c) => active.has(c.bundle)).map((c) => {
    const subs = c.subcategories.map((sub) => {
      const key = subKey(c.bundle, sub);
      return {
        key,
        available: key !== subOf(cur)
          && replacement(avail, state.level, ranges, categoryCandidates(avail, state.level, ranges, key), () => 0, count, io, fill, cardsOf(state)) !== null,
      };
    });
    return { slug: c.slug, key: catKey(c), available: subs.some((s) => s.available), subcategories: subs };
  });
  const possible = groups.some((g) => g.available);
  const out: Jokers = {
    hint, skip: { ...skipJ, purge }, easier, snipe,
    category: { available: possible, reason: possible ? null : new GameError("category_none").info(), categories: groups },
  };
  for (const [name, left] of Object.entries(jokersLeft(state)) as [JokerName, number | null][])
    if (left === 0) Object.assign(out[name], { available: false, reason: new GameError("joker_spent", { joker: name }).info() });
  return out;
}

/** Per joker: uses left in this game, or null = unlimited (MD-1). */
function jokersLeft(state: GameState): JokerBudget {
  const used = jokersUsed(state);
  return Object.fromEntries(Object.entries(state.settings.jokers).map(([name, limit]) =>
    [name, limit === null ? null : Math.max(0, limit - used[name as JokerName])])) as JokerBudget;
}

/** Per joker: uses in this game so far, the question on screen included. */
export function jokersUsed(state: Pick<GameState, "history" | "jokers">): Record<JokerName, number> {
  const used = [...state.history.flatMap((h) => h.jokers ?? []), ...state.jokers];
  return Object.fromEntries(JOKERS.map((name) => [name, used.filter((j) => j === name).length])) as Record<JokerName, number>;
}

/** Set the running game's joker budget (MD-4): {joker: count or null}; missing jokers stay. */
export function setJokers(save: SaveData, io: Io, budget: unknown): { save: SaveData; state: GameState } {
  checkBudget(budget);
  return action(save, (work) => {
    const { row, state } = running(work);
    gamemasterOnly(state, "jokers");
    Object.assign(state.settings.jokers, budget);
    saveGame(row, state, io);
    return state;
  });
}

// Competitive timed (plan 159) ----------------------------------------------------------------

/** A timed action's working set: `state` a copy of `row.state`, `t` its timed part, `ms` the action's time. */
interface Timed {
  work: SaveData;
  row: GameRow;
  state: GameState;
  t: TimedState;
  data: EngineData;
  io: Io;
  ms: number;
}

/** The action's epoch ms; missing (tests, fixtures) = `io.now`. */
const msOf = (io: Io): number => io.ms ?? Date.parse(io.now);

function timedOf(work: SaveData, row: GameRow, data: EngineData, io: Io, what: string): Timed {
  const state = withDefaults(structuredClone(row.state));
  if (gameMode(state) !== "timed") throw new GameError("timed_only", { action: what });
  return { work, row, state, t: state.timed!, data, io, ms: msOf(io) };
}

/** Save the flow back; a won or lost phase ends the session. */
function timedSave(c: Timed): GameState {
  const p = c.state.phase;
  saveGame(c.row, c.state, c.io, p === "won" || p === "lost" ? p : null);
  return c.state;
}

/** Seat indexes still in. */
const seatsIn = (row: GameRow): number[] => row.seats!.flatMap((s, i) => (s.out ? [] : [i]));

/** The session's first question (`row.state` in place): no budget, every seat in for round 1. */
function timedStart(work: SaveData, row: GameRow, data: EngineData, io: Io): void {
  const state = row.state;
  state.settings.jokers = Object.fromEntries(JOKERS.map((j) => [j, 0])) as JokerBudget;
  state.settings.customized = false;
  const t: TimedState = { round_size: row.seats!.length, round_done: 0, round_correct: [], shown_at: null, claim: null, paused_at: null, repeat: 0 };
  state.timed = t;
  nextQuestion({ work, row, state, t, data, io, ms: msOf(io) });
}

/** One question at the level, every later level keeping `round_size`; none: the age group's whole range (decision 281);
 * null if that is empty too. Never one offered earlier in the session. */
function timedDraw(c: Timed): string | null {
  const { work, state, data, io, t } = c;
  const ranges = rangesOf(state, data);
  const avail = availableNow(work, state, data);
  const opts = {
    n: 1, perLevel: t.round_size, avoidCategories: askedCategories(state, data), categoryOf: categoryOf(data.broad),
    countOf: countOf(work), rng: io.rng,
  };
  const whole: LevelRanges = [[Math.min(...ranges.map((r) => r[0])), Math.max(...ranges.map((r) => r[1]))]];
  const drawn = selection.draw(state.level, avail, { ...opts, ranges }) ?? selection.draw(1, avail, { ...opts, ranges: whole });
  return drawn?.[0].id ?? null;
}

/** The next question on screen, its clock from now; nothing left to draw: nobody wins. */
function nextQuestion(c: Timed): void {
  const { state, t } = c;
  state.phase = "select";
  leaveQuestion(state);
  const id = timedDraw(c);
  if (id === null) return timedEnd(c, null);
  state.options = [id];
  state.offered.push(id);
  open(state, c.data, c.io, 0);
  t.shown_at = null;
}

/** The session ends: `winner` won, every other seat still in lost; null: nobody wins (decision 280). */
function timedEnd(c: Timed, winner: number | null): void {
  for (const i of seatsIn(c.row)) c.row.seats![i].result = i === winner ? "won" : "lost";
  c.state.phase = winner === null ? "lost" : "won";
  c.t.claim = null;
}

interface Ending {
  seat?: number;
  chosen: number | null;
  correct?: boolean;
  /** The claim's time, or the question's end when unclaimed: what the hints shown count to. */
  at: number;
  timeout?: true;
  unclaimed?: true;
}

/** A question ends: seen, logged; a correct answer at the last level wins, a wrong one puts the seat out; then the
 * next question or the round end. */
function questionEnd(c: Timed, e: Ending): void {
  const { work, row, state, t, data, io } = c;
  const q = question(data, state.current);
  const { at, ...rest } = e;
  see(work, q.id, row.id, io);
  state.history.push({ level: state.level, question_id: q.id, ...rest, hints: Math.min(q.hints.length, Math.floor((at - t.shown_at!) / HINT_MS)) });
  const { correct: _, ...flags } = rest;
  state.last = { ...flags, question_id: q.id, correct: e.correct ?? false, correct_index: state.answers.indexOf(q.answer) };
  t.claim = null;
  t.round_done += 1;
  if (e.correct) {
    t.round_correct.push(e.seat!);
    if (state.level >= levelCount(state)) return timedEnd(c, e.seat!);
  } else if (e.seat !== undefined) {
    Object.assign(row.seats![e.seat], { out: true, result: "lost" });
    const left = seatsIn(row);
    if (left.length === 1) return timedEnd(c, left[0]);
  }
  if (t.round_done >= t.round_size) roundEnd(c);
  else nextQuestion(c);
}

/** Seats in without a correct answer lose a life; then the end, the next level or, at the last, another sudden-death
 * round (decision 281); the new round's size: seats in (decision 276). */
function roundEnd(c: Timed): void {
  const { row, state, t } = c;
  for (const i of seatsIn(row)) {
    if (t.round_correct.includes(i)) continue;
    const seat = row.seats![i];
    seat.lives = (seat.lives ?? LIVES) - 1;
    if (seat.lives <= 0) Object.assign(seat, { out: true, result: "lost" });
  }
  const left = seatsIn(row);
  if (left.length <= 1) return timedEnd(c, left[0] ?? null);
  if (state.level < levelCount(state)) state.level += 1;
  else t.repeat += 1;
  Object.assign(t, { round_size: left.length, round_done: 0, round_correct: [] });
  nextQuestion(c);
}

/** A passed deadline first in every timed action: a claim past `CLAIM_MS` is a wrong answer, an unclaimed question past
 * `QUESTION_MS` ends (deadlines inclusive); true if one did. Not while paused. */
function settle(c: Timed): boolean {
  const { t } = c;
  if (t.paused_at !== null) return false;
  if (t.claim) {
    if (c.ms <= t.claim.at + CLAIM_MS) return false;
    questionEnd(c, { seat: t.claim.seat, chosen: null, correct: false, at: t.claim.at, timeout: true });
  } else {
    if (t.shown_at === null || c.ms <= t.shown_at + QUESTION_MS) return false;
    questionEnd(c, { chosen: null, at: t.shown_at + QUESTION_MS, unclaimed: true });
  }
  return true;
}

/** Claim the question on screen: `CLAIM_MS` to answer, the question clock stops; too late: the settled flow, no error. */
export function claim(save: SaveData, data: EngineData, io: Io, seat?: unknown): { save: SaveData; state: GameState } {
  return action(save, (work) => {
    const { row } = running(work);
    const who = actor(row, seat);
    const c = timedOf(work, row, data, io, "claim");
    if (!settle(c)) {
      if (c.t.paused_at !== null) throw new GameError("paused");
      if (c.t.shown_at === null) throw new GameError("not_shown");
      if (c.t.claim) throw new GameError("claim_taken");
      c.t.claim = { seat: who, at: c.ms };
    }
    return timedSave(c);
  });
}

/** The claimer's answer; late: settled as the timeout, not an error. */
function timedAnswer(work: SaveData, row: GameRow, who: number, index: number, data: EngineData, io: Io): GameState {
  const c = timedOf(work, row, data, io, "answer");
  if (settle(c)) return timedSave(c);
  const { t, state } = c;
  if (t.paused_at !== null) throw new GameError("paused");
  if (t.shown_at === null) throw new GameError("not_shown");
  if (!t.claim) throw new GameError("claim_first");
  if (t.claim.seat !== who) throw new GameError("not_your_claim");
  if (!(0 <= index && index < state.answers.length)) throw new GameError("answer_invalid", { n: index + 1 });
  questionEnd(c, { seat: who, chosen: index, correct: state.answers[index] === question(data, state.current).answer, at: t.claim.at });
  return timedSave(c);
}

/** The client's clock ran out: settle; nothing passed yet → `not_expired` with the ms left. */
export function expire(save: SaveData, data: EngineData, io: Io): { save: SaveData; state: GameState } {
  return action(save, (work) => {
    const c = timedOf(work, running(work).row, data, io, "expire");
    if (!settle(c)) {
      if (c.t.paused_at !== null) throw new GameError("paused");
      const deadline = c.t.claim ? c.t.claim.at + CLAIM_MS : (c.t.shown_at ?? c.ms) + QUESTION_MS;
      throw new GameError("not_expired", { ms: deadline - c.ms });
    }
    return timedSave(c);
  });
}

/** The Esc menu or the Steam overlay opened (decision 282): the clock stops, the question is hidden. */
export function pause(save: SaveData, data: EngineData, io: Io): { save: SaveData; state: GameState } {
  return action(save, (work) => {
    const c = timedOf(work, running(work).row, data, io, "pause");
    if (c.t.paused_at !== null) throw new GameError("already_paused");
    settle(c);
    if (c.state.phase === "question") c.t.paused_at = c.ms;
    return timedSave(c);
  });
}

/** Back from the pause: every running deadline (question, claim) moves by the paused time. */
export function resume(save: SaveData, data: EngineData, io: Io): { save: SaveData; state: GameState } {
  return action(save, (work) => {
    const c = timedOf(work, running(work).row, data, io, "resume");
    const { t } = c;
    if (t.paused_at === null) throw new GameError("not_paused");
    const span = Math.max(0, c.ms - t.paused_at);
    if (t.shown_at !== null) t.shown_at += span;
    if (t.claim) t.claim.at += span;
    t.paused_at = null;
    return timedSave(c);
  });
}

/** The question is on screen (decision 296): its 30 s run from now. Idempotent: a reload re-sends it. */
export function show(save: SaveData, data: EngineData, io: Io): { save: SaveData; state: GameState } {
  return action(save, (work) => {
    const c = timedOf(work, running(work).row, data, io, "show");
    if (c.t.paused_at !== null) throw new GameError("paused");
    settle(c);
    if (c.state.phase === "question" && c.t.shown_at === null) c.t.shown_at = c.ms;
    return timedSave(c);
  });
}

/** Hints shown at `ms`: one per `HINT_MS` of the question's clock (it stops at a claim), at most the question's. */
const timedHints = (t: TimedState, ms: number, count: number): number =>
  t.shown_at === null ? 0 : Math.min(count, Math.max(0, Math.floor(((t.claim?.at ?? ms) - t.shown_at) / HINT_MS)));

// Gamemaster cheats (MD-12, D-88) --------------------------------------------------------------

/** «Cambiar pregunta» on `state`: same level, same subcategory, else any in range; the old one is logged
 * `admin_replace`, seen only with `seen`. */
function replaceCurrent(work: SaveData, gid: number, state: GameState, data: EngineData, io: Io, seen: boolean): void {
  const cur = question(data, state.current);
  const avail = availableNow(work, state, data);
  const ranges = rangesOf(state, data);
  const fill = laterFill(avail, state.level, ranges, cardsOf(state));
  const pickFrom = (cands: PoolQuestion[]) => replacement(avail, state.level, ranges, cands,
    (q) => Math.abs(q.difficulty - cur.difficulty), countOf(work), io, fill, cardsOf(state));
  const fresh = pickFrom(categoryCandidates(avail, state.level, ranges, subOf(cur)!))
    ?? pickFrom(avail.filter((q) => subOf(q) !== subOf(cur) && selection.inRange(q, state.level, ranges)));
  if (!fresh) throw new GameError("replace_empty");
  if (seen) see(work, cur.id, gid, io);
  state.history.push({ level: state.level, question_id: cur.id, outcome: "admin_replace", jokers: state.jokers });
  putOn(state, fresh, io);
}

/** «Cambiar pregunta»: a new question on screen (MD-12). */
export function replace(save: SaveData, data: EngineData, io: Io, seen = false): { save: SaveData; state: GameState } {
  return action(save, (work) => {
    const { row, state } = running(work);
    gamemasterOnly(state, "replace");
    if (state.phase !== "question") throw new GameError("no_question");
    replaceCurrent(work, row.id, state, data, io, seen);
    saveGame(row, state, io);
    return state;
  });
}

/** `q-0007`, `Q-7` or `7` → `q-0007`; anything else as typed. */
function questionId(id: unknown): string {
  const s = String(id ?? "").trim().toLowerCase();
  const n = /^(?:q-?)?(\d+)$/.exec(s);
  return n ? `q-${n[1].padStart(4, "0")}` : s;
}

/** «Ir a pregunta» (dev mode, plan 85): question `id` on screen at the current level, like «Cambiar
 * pregunta» (not seen) but any mode, ignoring level range, age group, bundles and seen. */
export function goTo(save: SaveData, data: EngineData, io: Io, id: unknown): { save: SaveData; state: GameState } {
  return action(save, (work) => {
    const { row } = running(work);
    const who = row.turn ?? 0;
    const state = seatState(row, who);
    if (state.phase !== "question") throw new GameError("no_question");
    const fresh = data.byId.get(questionId(id));
    if (!fresh) throw new GameError("question_unknown", { id: String(id ?? "") });
    if (fresh.id === state.current) return state;
    state.options = state.options.filter((i) => i !== fresh.id);
    state.history.push({ level: state.level, question_id: state.current!, outcome: "admin_replace", jokers: state.jokers });
    putOn(state, fresh, io);
    saveSeat(row, who, state, io);
    return state;
  });
}

/** Before a new table (level, settings): select phase, or with `cards: 0` the question on screen is
 * replaced (not seen); the cards on the table go back to the pool. */
function clearTable(state: GameState, what: string): void {
  if (state.phase === "question") {
    if (cardsOf(state) !== 0) throw new GameError("cheat_not_select", { action: what });
    const cur = state.current!;
    state.history.push({ level: state.level, question_id: cur, outcome: "admin_replace", jokers: state.jokers });
    state.options = state.options.filter((i) => i !== cur);
  }
  const back = new Set(state.options);
  state.offered = state.offered.filter((i) => !back.has(i));
  Object.assign(state, { phase: "select", options: [], repeat: false });
  leaveQuestion(state);
}

/** «Saltar a nivel»: a new table at `level`; no rows for the levels in between; the undo snapshot stays. */
export function jumpLevel(save: SaveData, data: EngineData, io: Io, level: unknown): { save: SaveData; state: GameState } {
  return action(save, (work) => {
    const { row, state } = running(work);
    gamemasterOnly(state, "level");
    const to = checkCount(level, 1, levelCount(state), "level_invalid");
    clearTable(state, "level");
    state.level = to;
    deal(work, state, data, io);
    saveGame(row, state, io);
    return state;
  });
}

/** Difficulty, bundles and answers (D-105) mid-game: validated like `new`, the rest of the game (current
 * level..levels) must fill; a new table, history and level stay. */
export function changeSettings(
  save: SaveData, data: EngineData, io: Io, input: Pick<ChoiceInput, "age_group" | "difficulty" | "bundles" | "answers">,
): { save: SaveData; state: GameState } {
  return action(save, (work) => {
    const { row, state } = running(work);
    gamemasterOnly(state, "settings");
    const choice = resolveChoice(data, input, gameChoice(state, data));
    clearTable(state, "settings");
    const s = state.settings;
    if (input.age_group !== undefined || input.difficulty !== undefined) {
      delete s.age_group;
      delete s.difficulty;
      if (choice.difficulty) s.difficulty = choice.difficulty;
      else s.age_group = choice.age_group!;
    }
    if (input.bundles !== undefined) s.bundles = choice.bundles;
    if (input.answers !== undefined) {
      if (choice.answers) delete s.answers;
      else s.answers = false;
    }
    const ranges = rangesOf(state, data);
    const avail = availableNow(work, state, data);
    const rest = laterLevels(state.level - 1, ranges);
    const { missing } = selection.assign(avail, rest, ranges, perLevel(cardsOf(state)));
    if (missing.size) {
      const levels = rest.map((level) => ({
        level, range: [ranges[level - 1][0], ranges[level - 1][1]] as [number, number],
        candidates: avail.filter((q) => selection.inRange(q, level, ranges)).length, missing: missing.get(level) ?? 0,
      }));
      throw supplyShort({ ok: false, available: avail.length, levels });
    }
    deal(work, state, data, io);
    saveGame(row, state, io);
    return state;
  });
}

/** Take back the last final answer: restore the state before it, drop that answer's seen row. */
export function undo(save: SaveData, io: Io): { save: SaveData; state: GameState } {
  return action(save, (work) => {
    const game = latest(work);
    if (game) gamemasterOnly(game.state, "undo");
    if (!game || game.row.result === "abandoned" || !game.state.undo) throw new GameError("nothing_to_undo");
    const { row, state } = game;
    const qid = state.last!.question_id;
    const i = work.seen.findIndex((s) => s.question_id === qid && s.game_id === row.id);
    if (i >= 0) work.seen.splice(i, 1);
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

/** Question ids a game state needs (table, screen, last answer) that the pool lacks. */
function lacks(state: GameState | null, data: EngineData): boolean {
  const gone = (id: string | null) => id !== null && !data.byId.has(id);
  return state !== null && (state.options.some(gone) || gone(state.current) || gone(state.last?.question_id ?? null));
}

/** After a patch (plan 91): the running game drops ids its pool lacks; no seen rows; the same save if none. */
export function repair(save: SaveData, data: EngineData, io: Io): SaveData {
  const game = latest(save);
  if (!game || game.row.result !== null || gameLocale(game.row) !== data.locale) return save;
  if (!rowStates(game.row).map((s) => withDefaults(structuredClone(s))).some((s) => lacks(s, data) || lacks(s.undo, data))) return save;
  return transact(save, (work) => {
    const { row } = running(work);
    const owners: { state: GameState; set: (s: GameState) => void }[] =
      rowStates(row)[0] === row.state ? [{ state: row.state, set: (s) => saveGame(row, s, io) }]
        : row.seats!.flatMap((seat) => (seat.state ? [{ state: seat.state, set: (s: GameState) => { seat.state = structuredClone(s); } }] : []));
    for (const o of owners) {
      const state = withDefaults(structuredClone(o.state));
      mend(work, state, data, io);
      o.set(state);
    }
  }).save;
}

/** repair's fix for one game state. */
function mend(work: SaveData, state: GameState, data: EngineData, io: Io): void {
  const has = (id: string) => data.byId.has(id);
  if (state.current !== null && !has(state.current)) {
    const jokers = state.jokers;
    state.phase = "select";
    leaveQuestion(state);
    state.jokers = jokers;
  }
  if (state.last && !has(state.last.question_id)) state.last = null;
  if (lacks(state.undo, data)) state.undo = null;
  const missing = state.options.filter((i) => !has(i)).length;
  if (missing) {
    let fresh: string[] = [];
    try {
      fresh = draw(work, state, data, io, missing, state.options.filter(has).map((i) => data.byId.get(i)!));
    } catch (e) {
      if (!(e instanceof GameError)) throw e;
    }
    state.options = state.options.flatMap((i) => (has(i) ? [i] : fresh.splice(0, 1)));
  }
  if (state.options.length) openIfNoCards(state, data, io);
}

/** The seat whose game a session's view shows: the turn's; a finished session: the winner's, else the last answerer's. */
function shownSeat(row: GameRow): number {
  const won = row.seats!.findIndex((s) => s.result === "won");
  return won >= 0 ? won : row.result === null ? row.turn ?? 0 : row.state.last?.seat ?? row.turn ?? 0;
}

/** `session.timed` of the view: the clock as deadlines in epoch ms (the client counts down, decision 282). */
function timedView(row: GameRow, t: TimedState, state: GameState, data: EngineData, io: Io): NonNullable<Game["session"]>["timed"] {
  const live = row.result === null && state.phase === "question";
  const paused = t.paused_at !== null;
  const q = state.current === null ? undefined : data.byId.get(state.current);
  const chance = (i: number) => t.round_done === t.round_size - 1 && !t.round_correct.includes(i);
  const left = seatsIn(row);
  return {
    round: state.level, sudden_death: state.level >= levelCount(state), repeat: t.repeat,
    round_size: t.round_size, question_in_round: Math.min(t.round_done + 1, t.round_size),
    shown: t.shown_at !== null,
    deadline: live && !paused && !t.claim && t.shown_at !== null ? t.shown_at + QUESTION_MS : null,
    claim: live && !paused && t.claim ? { seat: t.claim.seat, deadline: t.claim.at + CLAIM_MS } : null,
    paused, hints_shown: live && !paused && q ? timedHints(t, msOf(io), q.hints.length) : null,
    all_at_risk: live && left.length > 0 && left.every((i) => row.seats![i].lives === 1 && chance(i)),
  };
}

/** The newest game as the TV sees it: no correct answer before the final answer. In a session the top-level
 * fields are the shown seat's game, `last` the session's last final answer. */
export function view(save: SaveData, data: EngineData, io: Io): Game | null {
  const game = latest(save);
  if (!game) return null;
  const { row } = game;
  const shown = row.seats ? shownSeat(row) : 0;
  const state = seatState(row, shown);
  const result = row.result;
  const by = data.byId;
  const playing = result === null && state.phase === "question" && state.current !== null && by.has(state.current);
  const t = row.seats && gameMode(state) === "timed" ? state.timed : undefined;
  const hidden = t?.paused_at != null;
  const jokers = playing && !t ? jokersView(save, row, state, data, io) : null;
  const named = (id: number | null) => save.players.find((p) => p.id === id)?.name ?? null;
  const out: Game = {
    id: row.id, player: named(row.seats ? row.seats[shown].player_id : row.player_id), result,
    level: state.level, phase: state.phase,
    options: state.options.filter((i) => by.has(i)).map((i) => ({ description: by.get(i)!.description })),
    history: state.history.filter((h) => h.correct !== undefined).map((h) => ({ level: h.level, correct: h.correct! })),
    can_undo: !t && Boolean(state.undo) && result !== "abandoned" && gameMode(state) === "gamemaster",
    purged: state.purged, repeat: state.repeat, jokers,
    settings: state.settings, jokers_left: jokersLeft(state), question: null, last: null,
  };
  if (row.seats) {
    out.session = {
      mode: gameMode(state), turn: row.turn ?? 0,
      seats: row.seats.map((seat, i) => {
        const r = seatResult(row, i);
        const status = r === "won" || r === "lost" ? r : seat.out ? ("out" as const) : ("playing" as const);
        const own = seatState(row, i);
        const base = { player: named(seat.player_id), status, level: own.level, age_group: gameChoice(own, data).age_group ?? null, jokers_left: jokersLeft(own) };
        if (!t) return base;
        const last_chance = result === null && !seat.out && t.round_done === t.round_size - 1 && !t.round_correct.includes(i);
        return { ...base, lives: seat.lives ?? LIVES, correct_this_round: t.round_correct.includes(i), last_chance };
      }),
      ...(t ? { timed: timedView(row, t, state, data, io) } : {}),
    };
  }
  const q = state.current === null ? undefined : by.get(state.current);
  if (q && !hidden) {
    // Only the hints shown through «Soplo» (D-26, D-27); no description (04, "Question").
    out.question = {
      id: q.id, question: q.question, media: q.media, background: q.background,
      answers: state.answers, hints: q.hints.slice(0, t ? timedHints(t, msOf(io), q.hints.length) : state.hints_shown),
      struck: state.struck, swapped_to: state.swapped_to,
    };
  }
  const final = row.seats ? row.state.last : state.last;
  const last = final && by.get(final.question_id);
  if (final && last) out.last = { ...final, answer: last.answer, fun_fact: last.fun_fact };
  return out;
}
