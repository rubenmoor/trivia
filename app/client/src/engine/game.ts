// The referee (PORT-3, plan 20): port of app/server/game.py. Public functions are pure:
// (save, data, io, …) → {save, …}; inside, they mutate a transact() copy like the Python port.
import type { Choice, Difficulty, Game, GameMode, JokerBudget, JokerEvent, JokerName, JokerState, Jokers, Player, Supply } from "../lib/types.ts";
import type { LevelRanges, PoolQuestion } from "./pool.ts";
import { bundlesFor, categoryOf } from "./pool.ts";
import { casefold, pyLen, pySplitJoin, pyTruthy } from "./pycompat.ts";
import * as selection from "./selection.ts";
import type { EngineData, GameRow, GameState, Io, Outcome, SaveData } from "./state.ts";
import { GameError, SPANISH, UNLIMITED, nextId, transact, trial, withDefaults } from "./state.ts";

export { GameError, UNLIMITED };

export const JOKERS: readonly JokerName[] = ["hint", "skip", "easier", "category", "snipe"];
/** «Como las cartas»: the printed card set (JK-11), for the overlay's preset (MD-4). */
export const CARDS: JokerBudget = { hint: 4, skip: 2, easier: 2, category: 2, snipe: 2 };
/** Standard joker set of every non-gamemaster game (13, "Implementation notes"). */
export const STANDARD_JOKERS: JokerBudget = { hint: 3, skip: 1, easier: 1, category: 1, snipe: 1 };

export const MODES: readonly GameMode[] = ["gamemaster", "solo", "rr-coop", "rr-competitive", "timed"];
/** Playable so far (plan 36); the multiplayer modes come with MD-8. */
export const BUILT_MODES: readonly GameMode[] = ["gamemaster", "solo"];

/** The game's mode; missing = gamemaster (games from before plan 36). */
export const gameMode = (state: GameState): GameMode => state.settings.mode ?? "gamemaster";

/** Undo, skip, replace, joker budget: gamemaster mode only (D-74). */
function gamemasterOnly(state: GameState, what: string): void {
  if (gameMode(state) !== "gamemaster") throw new GameError("gamemaster_only", { action: what });
}

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

/** Seen count per question: rows in the whole save, every player and mode (plan 65). */
export function countOf(save: SaveData): (q: PoolQuestion) => number {
  const counts = new Map<string, number>();
  for (const s of save.seen) counts.set(s.question_id, (counts.get(s.question_id) ?? 0) + 1);
  return (q) => counts.get(q.id) ?? 0;
}

/** Delete a player (GF-7): the name and their games (a running one too); the seen rows stay. */
export function deletePlayer(save: SaveData, name: unknown): { save: SaveData } {
  return transact(save, (work) => {
    const pid = playerId(work, cleanName(name));
    if (pid === null) throw new GameError("player_unknown", { name });
    const gone = new Set(work.games.filter((g) => g.player_id === pid).map((g) => g.id));
    for (const s of work.seen) if (gone.has(s.game_id)) s.game_id = 0;
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

// Age group and bundles per game (plan 27) ------------------------------------------------------

/** The age group of a game that doesn't name one (D-22's ranges). */
export const DEFAULT_AGE_GROUP = "young_teens";

/** Ranges of the configure screen's fields (D-88). */
export const LEVELS_MAX = 20;
export const CARDS_MAX = 4;
export const DIFFICULTY_MAX = 15;

/** The default age group; the locale's first base bundle plus every other bundle offered in it (plan 71);
 * 12 levels, 4 cards, media allowed; the standard joker set (configure screen only, D-88). */
export function defaultChoice(data: EngineData): Choice {
  const offered = bundlesFor(data);
  const base = offered.find((b) => b.kind === "base");
  return {
    age_group: DEFAULT_AGE_GROUP, difficulty: null,
    bundles: offered.filter((b) => b === base || b.kind !== "base").map((b) => b.id),
    levels: selection.LEVELS, cards: selection.PER_LEVEL, video: true, audio: true, jokers: { ...STANDARD_JOKERS },
  };
}

/** The game's choice; missing keys, an unknown group or bundles that don't resolve (plan 71) are the
 * defaults (jokers: the game's budget), resolved here and never written back. */
export function gameChoice(state: Pick<GameState, "settings">, data: EngineData): Choice {
  const d = defaultChoice(data);
  const { age_group, bundles, difficulty, levels, cards, video, audio, jokers } = state.settings;
  let out = d.bundles;
  if (bundles !== undefined) {
    try {
      out = resolveBundles(data, bundles);
    } catch (e) {
      if (!(e instanceof GameError)) throw e;
    }
  }
  return {
    age_group: difficulty ? null : age_group !== undefined && data.groupById.has(age_group) ? age_group : d.age_group,
    difficulty: difficulty ? { ...difficulty } : null, bundles: out,
    levels: levels ?? d.levels, cards: cards ?? d.cards, video: video !== false, audio: audio !== false, jokers: { ...jokers },
  };
}

/** Bundles offered in the locale, duplicates dropped, exactly one base bundle, bundles.json order. */
function resolveBundles(data: EngineData, wanted: unknown): string[] {
  if (!Array.isArray(wanted)) throw new GameError("bundles_not_list");
  const known = new Set(data.bundles.map((b) => b.id));
  const offered = new Set(bundlesFor(data).map((b) => b.id));
  for (const b of wanted) {
    if (typeof b !== "string" || !known.has(b)) throw new GameError("bundle_unknown", { bundle: String(b) });
    if (!offered.has(b)) throw new GameError("bundle_not_offered", { bundle: b, locale: data.locale });
  }
  const on = data.bundles.filter((b) => wanted.includes(b.id));
  const count = on.filter((b) => b.kind === "base").length;
  if (count !== 1) throw new GameError("base_bundle_count", { count });
  return on.map((b) => b.id);
}

/** What a choice may get from a request body (plan 27, D-88). */
export interface ChoiceInput {
  age_group?: unknown;
  /** Non-null: custom, then no age_group. */
  difficulty?: unknown;
  bundles?: unknown;
  levels?: unknown;
  cards?: unknown;
  video?: unknown;
  audio?: unknown;
  /** Merged into `base.jokers`. */
  jokers?: unknown;
}

export const CHOICE_KEYS = ["age_group", "difficulty", "bundles", "levels", "cards", "video", "audio", "jokers"] as const;

function checkDifficulty(d: unknown): Difficulty {
  const ok = (n: unknown): n is number => Number.isInteger(n) && 1 <= (n as number) && (n as number) <= DIFFICULTY_MAX;
  if (d === null || typeof d !== "object" || Array.isArray(d)) throw new GameError("difficulty_invalid");
  const { start, end } = d as Record<string, unknown>;
  if (!ok(start) || !ok(end) || end < start) throw new GameError("difficulty_invalid");
  return { start, end };
}

function checkCount(v: unknown, min: number, max: number, code: string): number {
  if (!Number.isInteger(v) || (v as number) < min || (v as number) > max) throw new GameError(code, { min, max });
  return v as number;
}

function checkSwitch(v: unknown, field: string): boolean {
  if (typeof v !== "boolean") throw new GameError("switch_invalid", { field });
  return v;
}

/** Validate and normalize a requested choice; a missing key comes from `base`. */
export function resolveChoice(data: EngineData, input: ChoiceInput, base: Choice = defaultChoice(data)): Choice {
  let age_group: string | null = null, difficulty: Difficulty | null = null;
  if (input.difficulty != null) {
    if (input.age_group != null) throw new GameError("difficulty_invalid");
    difficulty = checkDifficulty(input.difficulty);
  } else if (input.age_group === undefined && input.difficulty === undefined && base.difficulty) {
    difficulty = { ...base.difficulty };
  } else {
    const group = input.age_group !== undefined ? input.age_group : (base.age_group ?? DEFAULT_AGE_GROUP);
    if (typeof group !== "string" || !data.groupById.has(group)) throw new GameError("age_group_unknown", { group: String(group) });
    age_group = group;
  }
  const or = <T>(v: unknown, fallback: T, check: (v: unknown) => T): T => (v === undefined ? fallback : check(v));
  return {
    age_group, difficulty,
    bundles: resolveBundles(data, input.bundles === undefined ? base.bundles : input.bundles),
    levels: or(input.levels, base.levels, (v) => checkCount(v, 1, LEVELS_MAX, "levels_invalid")),
    cards: or(input.cards, base.cards, (v) => checkCount(v, 0, CARDS_MAX, "cards_invalid")),
    video: or(input.video, base.video, (v) => checkSwitch(v, "video")),
    audio: or(input.audio, base.audio, (v) => checkSwitch(v, "audio")),
    jokers: or(input.jokers, base.jokers, (v) => ({ ...base.jokers, ...checkBudget(v) })),
  };
}

/** [lo, hi] per level for `choice.levels` levels (decision 46): custom ramps evenly from start to end,
 * an age group's 12 ranges are stepped over n levels. */
export function rangesFor(data: EngineData, choice: Pick<Choice, "age_group" | "difficulty" | "levels">): LevelRanges {
  const n = choice.levels;
  const at = (i: number) => (n === 1 ? 0 : (i - 1) / (n - 1));
  const levels = Array.from({ length: n }, (_, k) => k + 1);
  if (choice.difficulty) {
    const { start, end } = choice.difficulty;
    return levels.map((i) => {
      const t = start + (end - start) * at(i);
      return [Math.floor(t), Math.ceil(t)] as const;
    });
  }
  const group = data.groupById.get(choice.age_group!)!.levels;
  if (n === group.length) return group;
  return levels.map((i) => group[Math.round((group.length - 1) * at(i))]);
}

const rangesOf = (state: GameState, data: EngineData): LevelRanges => rangesFor(data, gameChoice(state, data));

/** The game's number of levels and cards per level (D-88). */
export const levelsOf = (state: GameState): number => state.settings.levels ?? selection.LEVELS;
export const cardsOf = (state: GameState): number => state.settings.cards ?? selection.PER_LEVEL;
/** Questions the table and the supply need per level: with 0 cards still one. */
const perLevel = (cards: number): number => Math.max(cards, 1);

/** Video / audio questions off (D-88): images and backgrounds stay. */
export function mediaAllowed(s: { video?: boolean; audio?: boolean }): (q: PoolQuestion) => boolean {
  return (q) => !((s.video === false && q.media?.type === "video") || (s.audio === false && q.media?.type === "audio"));
}

/** What a game with `choice` could draw: approved, not blocked, in `bundles`, media allowed; any seen count. */
export function availableFor(save: SaveData, data: EngineData, choice: Choice, bundles: Iterable<string> = choice.bundles): PoolQuestion[] {
  return selection.available(data.pool, save.blocked, [], new Set(bundles)).filter(mediaAllowed(choice));
}

/** Questions that can still come up in this game: approved, not blocked, not offered, not purged; seen ones too. */
export function availableNow(work: SaveData, state: GameState, data: EngineData): PoolQuestion[] {
  const purged = new Set<string | null>(state.purged);
  const bundles = new Set(gameChoice(state, data).bundles);
  const media = mediaAllowed(state.settings);
  return selection.available(data.pool, work.blocked, state.offered, bundles).filter((q) => !purged.has(q.subcategory) && media(q));
}

/** Draw n cards for the state's level from what's still available in this game, lowest seen count first. */
function draw(
  work: SaveData, state: GameState, data: EngineData, io: Io, n = perLevel(cardsOf(state)), keep: PoolQuestion[] = [],
): string[] {
  const ranges = rangesOf(state, data);
  const drawn = selection.draw(state.level, availableNow(work, state, data), {
    ranges, n, perLevel: perLevel(cardsOf(state)), keep, avoidCategories: askedCategories(state, data), categoryOf: categoryOf(data.broad),
    countOf: countOf(work), rng: io.rng,
  });
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

/** What a new game may get from the request body besides the player (plan 27, plan 36, D-88). */
export interface ChoiceArgs extends ChoiceInput {
  mode?: unknown;
  /** Overrides of the mode's joker set (not of `Choice.jokers`); in `solo` a difference sets `customized`. */
  jokers?: unknown;
}

function newestGame(save: SaveData, player?: unknown): GameRow | null {
  const pid = player ? playerId(save, cleanName(player)) : null;
  return pid === null ? null
    : save.games.filter((g) => g.player_id === pid).reduce<GameRow | null>((m, g) => (m === null || g.id > m.id ? g : m), null);
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

/** Start a game for `player` (known or new, D-28); a running game is abandoned. The settings get
 * `age_group` / `difficulty` / `bundles` / `mode` / `levels` / `cards` only when `args` carries them,
 * `video` / `audio` only when off. */
export function newGame(
  save: SaveData, data: EngineData, io: Io, player: unknown, args: ChoiceArgs = {},
): { save: SaveData; state: GameState } {
  const name = cleanName(player);
  const locale = (save.language ?? SPANISH).questions;
  if (data.locale !== locale) throw new Error(`new game in ${locale} on the ${data.locale} pool`);
  const { jokers: _, ...rest } = args;
  const choice = resolveChoice(data, rest);
  const mode = args.mode ?? "gamemaster";
  if (!(MODES as unknown[]).includes(mode)) throw new GameError("mode_unknown", { mode: String(mode) });
  if (!(BUILT_MODES as unknown[]).includes(mode)) throw new GameError("mode_not_built", { mode });
  const overrides = args.jokers === undefined ? {} : checkBudget(args.jokers);
  const report = supply(save, data, choice);
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
    if (choice.difficulty) state.settings.difficulty = choice.difficulty;
    else if (args.age_group !== undefined) state.settings.age_group = choice.age_group!;
    if (args.bundles !== undefined) state.settings.bundles = choice.bundles;
    if (args.levels !== undefined) state.settings.levels = choice.levels;
    if (args.cards !== undefined) state.settings.cards = choice.cards;
    if (!choice.video) state.settings.video = false;
    if (!choice.audio) state.settings.audio = false;
    if (args.mode !== undefined) state.settings.mode = mode as GameMode;
    if (mode === "gamemaster") Object.assign(state.settings.jokers, overrides);
    else {
      const jokers = { ...STANDARD_JOKERS, ...overrides };
      state.settings.jokers = jokers;
      state.settings.customized = JOKERS.some((j) => jokers[j] !== STANDARD_JOKERS[j]);
    }
    deal(work, state, data, io);
    work.games.push({
      id: nextId(work.games), started_on: io.now, finished_on: null, result: null, player_id: pid,
      ...(locale === "es" ? {} : { locale }), state: structuredClone(state),
    });
    return state;
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

export function pick(save: SaveData, data: EngineData, io: Io, index: number): { save: SaveData; state: GameState } {
  return action(save, (work) => {
    const { row, state } = running(work);
    if (state.phase !== "select") throw new GameError("no_cards");
    if (!(0 <= index && index < state.options.length)) throw new GameError("card_invalid", { n: index + 1 });
    open(state, data, io, index);
    saveGame(row, state, io);
    return state;
  });
}

/** The final answer: check it, record it as seen, move on (next level, won or lost). */
export function answer(save: SaveData, data: EngineData, io: Io, index: number): { save: SaveData; state: GameState } {
  return action(save, (work) => {
    const { row, state } = running(work);
    if (state.phase !== "question") throw new GameError("no_question");
    if (!(0 <= index && index < state.answers.length) || state.struck.includes(index))
      throw new GameError("answer_invalid", { n: index + 1 });
    const q = question(data, state.current);
    const before: GameState = { ...structuredClone(state), undo: null };
    const correct = state.answers[index] === q.answer;
    see(work, q.id, row.id, io);
    state.history.push({ level: state.level, question_id: q.id, correct, jokers: state.jokers });
    state.last = { question_id: q.id, chosen: index, correct, correct_index: state.answers.indexOf(q.answer) };
    state.undo = before;
    let result: Result = null;
    if (!correct) {
      state.phase = result = "lost";
    } else if (state.level >= levelsOf(state)) {
      state.phase = result = "won";
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
export function leaveQuestion(state: GameState): void {
  Object.assign(state, { current: null, answers: [], hints_shown: 0, struck: [], jokers: [], swapped_to: null });
}

/** Record the question on screen as seen (`block`: blocked instead) and log it. */
export function dropCurrent(
  work: SaveData, gid: number, state: GameState, outcome: Outcome, io: Io, block_ = false,
): void {
  if (block_) block(work, state.current!);
  else see(work, state.current!, gid, io);
  state.history.push({ level: state.level, question_id: state.current!, outcome, jokers: state.jokers });
}

/** Drop the question on screen and refill the table (admin skip, «Paso»). With `purge`, its
 * subcategory leaves the game and its other cards on the table are replaced too (not seen). */
export function backToSelect(
  work: SaveData, gid: number, state: GameState, data: EngineData, io: Io, outcome: Outcome, purge = false,
): void {
  const sub = question(data, state.current).subcategory;
  dropCurrent(work, gid, state, outcome, io, outcome === "admin_block");
  const removed = new Set([state.current!]);
  if (purge) {
    state.purged.push(sub as string);
    for (const i of state.options) if (question(data, i).subcategory === sub) removed.add(i);
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
export function laterFill(avail: PoolQuestion[], level: number, ranges: LevelRanges, cards = selection.PER_LEVEL): Fill {
  const { assignment, missing } = selection.assign(avail, laterLevels(level, ranges), ranges, perLevel(cards));
  return [new Set([...assignment.values()].flat()), missing.size === 0];
}

function laterLevels(level: number, ranges: LevelRanges): number[] {
  return Array.from({ length: ranges.length - level }, (_, i) => level + 1 + i);
}

/** The best of `cands` by (seen count, `order`) (random among ties) whose removal still lets every
 * later level fill (GF-2), or null. */
export function replacement(
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

export function categoryCandidates(avail: PoolQuestion[], level: number, ranges: LevelRanges, sub: string): PoolQuestion[] {
  return avail.filter((q) => q.subcategory === sub && selection.inRange(q, level, ranges));
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

/** What a joker may get from the request body (main.py passes only these). */
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
  const sub = question(data, state.current).subcategory;
  backToSelect(work, gid, state, data, io, "skipped", pyTruthy(purge));
  return { purged: pyTruthy(purge) ? sub : null };
};

/** «Bájale»: an easier question of the same subcategory, the hardest of those below (09). */
const playEasier: Play = (work, gid, state, data, io) => {
  const cur = question(data, state.current);
  const avail = availableNow(work, state, data);
  const cands = avail.filter((q) => q.subcategory === cur.subcategory && q.difficulty < cur.difficulty);
  const fresh = replacement(avail, state.level, rangesOf(state, data), cands, (q) => -q.difficulty, countOf(work), io, undefined, cardsOf(state));
  if (!fresh) throw new GameError("easier_none");
  state.jokers.push("easier");
  swapIn(work, gid, state, fresh, "easier", io);
  return { from: cur.difficulty, to: fresh.difficulty };
};

/** «Cambiazo»: a question of the level's range from the chosen subcategory, nearest difficulty first (09). */
const playCategory: Play = (work, gid, state, data, io, { subcategory }) => {
  const cur = question(data, state.current);
  if (typeof subcategory !== "string" || !data.broad.has(subcategory)) throw new GameError("category_unknown");
  if (subcategory === cur.subcategory) throw new GameError("category_same");
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
  if (state.answers.length - state.struck.length <= 1) throw new GameError("snipe_last");
  if (!Number.isInteger(index) || !(0 <= (index as number) && (index as number) < state.answers.length)
    || state.struck.includes(index as number))
    throw new GameError("snipe_invalid");
  const i = index as number;
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
  Object.assign(state, { phase: "select", repeat: true });
  leaveQuestion(state);
  openIfNoCards(state, data, io);
  state.repeat = true;
  return { outcome: "hit", index: i, correct_index: correctIndex };
};

const PLAYS: Record<JokerName, Play> = {
  hint: playHint, skip: playSkip, easier: playEasier, category: playCategory, snipe: playSnipe,
};

/** Play a joker on the question on screen; `event` is what happened (for the animation). */
export function joker(
  save: SaveData, data: EngineData, io: Io, name: string, args: JokerArgs = {},
): { save: SaveData; state: GameState; event: JokerEvent } {
  if (!(JOKERS as string[]).includes(name)) throw new GameError("joker_unknown", { joker: name });
  const jname = name as JokerName;
  const { save: out, result } = transact(save, (work) => {
    const { row, state } = running(work);
    if (state.phase !== "question") throw new GameError("joker_not_question");
    if (jokersLeft(state)[jname] === 0) throw new GameError("joker_spent", { joker: jname });
    const event = PLAYS[jname](work, row.id, state, data, io, args);
    saveGame(row, state, io);
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
  const purge = { ...check(playSkip, { purge: true }), subcategory: cur.subcategory as string };

  const avail = availableNow(work, state, data);
  const ranges = rangesOf(state, data);
  const fill = laterFill(avail, state.level, ranges, cardsOf(state));
  const count = countOf(work);
  const active = new Set(gameChoice(state, data).bundles);
  const groups = data.categories.filter((c) => active.has(c.bundle)).map((c) => {
    const subs = c.subcategories.map((s) => ({
      name: s,
      available: s !== cur.subcategory
        && replacement(avail, state.level, ranges, categoryCandidates(avail, state.level, ranges, s), () => 0, count, io, fill, cardsOf(state)) !== null,
    }));
    return { slug: c.slug, name: c.name, available: subs.some((s) => s.available), subcategories: subs };
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
export function jokersLeft(state: GameState): JokerBudget {
  const used = [...state.history.flatMap((h) => h.jokers ?? []), ...state.jokers];
  return Object.fromEntries(Object.entries(state.settings.jokers).map(([name, limit]) =>
    [name, limit === null ? null : Math.max(0, limit - used.filter((j) => j === name).length)])) as JokerBudget;
}

/** A partial budget {joker: count or null} as sent; GameError if malformed. */
function checkBudget(budget: unknown): Partial<JokerBudget> {
  if (budget === null || typeof budget !== "object" || Array.isArray(budget)
    || !Object.keys(budget).every((k) => (JOKERS as string[]).includes(k)))
    throw new GameError("budget_unknown_joker");
  for (const v of Object.values(budget))
    if (v !== null && !(Number.isInteger(v) && 0 <= (v as number) && (v as number) <= 99)) throw new GameError("budget_invalid");
  return budget as Partial<JokerBudget>;
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
  const fresh = pickFrom(categoryCandidates(avail, state.level, ranges, cur.subcategory as string))
    ?? pickFrom(avail.filter((q) => q.subcategory !== cur.subcategory && selection.inRange(q, state.level, ranges)));
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
    const to = checkCount(level, 1, levelsOf(state), "level_invalid");
    clearTable(state, "level");
    state.level = to;
    deal(work, state, data, io);
    saveGame(row, state, io);
    return state;
  });
}

/** Difficulty and bundles mid-game: validated like `new`, the rest of the game (current level..levels)
 * must fill; a new table, history and level stay. */
export function changeSettings(
  save: SaveData, data: EngineData, io: Io, input: Pick<ChoiceInput, "age_group" | "difficulty" | "bundles">,
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
    const ranges = rangesOf(state, data);
    const avail = availableNow(work, state, data);
    const rest = laterLevels(state.level - 1, ranges);
    const { missing } = selection.assign(avail, rest, ranges, perLevel(cardsOf(state)));
    if (missing.size) {
      const levels = rest.map((level) => ({
        level, range: [ranges[level - 1][0], ranges[level - 1][1]] as [number, number],
        candidates: avail.filter((q) => selection.inRange(q, level, ranges)).length, missing: missing.get(level) ?? 0,
      }));
      const short = levels.filter((l) => l.missing).map((l) => ({ level: l.level, lo: l.range[0], hi: l.range[1], missing: l.missing }));
      throw new GameError("supply_short", { levels: short }, { ok: false, available: avail.length, levels });
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

/** The newest game as the TV sees it: no correct answer before the final answer. */
export function view(save: SaveData, data: EngineData, io: Io): Game | null {
  const game = latest(save);
  if (!game) return null;
  const { row, state } = game;
  const result = row.result;
  const by = data.byId;
  const playing = result === null && state.phase === "question" && state.current !== null && by.has(state.current);
  const jokers = playing ? jokersView(save, row, state, data, io) : null;
  const out: Game = {
    id: row.id, player: save.players.find((p) => p.id === row.player_id)?.name ?? null, result,
    level: state.level, phase: state.phase,
    options: state.options.filter((i) => by.has(i)).map((i) => ({ description: by.get(i)!.description })),
    history: state.history.filter((h) => h.correct !== undefined).map((h) => ({ level: h.level, correct: h.correct! })),
    can_undo: Boolean(state.undo) && result !== "abandoned" && gameMode(state) === "gamemaster",
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
