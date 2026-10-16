// A game's configuration (plan 27, D-88): age group or difficulty, bundles, levels, cards, media, jokers.
import type { Choice, Difficulty, JokerBudget, JokerName } from "../lib/types.ts";
import type { LevelRanges, PoolQuestion } from "./pool.ts";
import { bundlesFor } from "./pool.ts";
import { LEVELS, PER_LEVEL } from "./selection.ts";
import type { EngineData, GameState } from "./state.ts";
import { GameError } from "./state.ts";

export const JOKERS: readonly JokerName[] = ["hint", "skip", "easier", "category", "snipe"];
/** Standard joker set of every non-gamemaster game (13, "Implementation notes"). */
export const STANDARD_JOKERS: JokerBudget = { hint: 3, skip: 1, easier: 1, category: 1, snipe: 1 };
/** Competitive timed (plan 159): per question, between hints, after a claim; lives per seat. */
export const QUESTION_MS = 30000;
export const HINT_MS = 8000;
export const CLAIM_MS = 6000;
export const LIVES = 3;

/** The age group of a game that doesn't name one (D-22's ranges). */
export const DEFAULT_AGE_GROUP = "young_teens";

/** Ranges of the configure screen's fields (D-88). */
export const LEVELS_MAX = 20;
export const CARDS_MAX = 4;
export const DIFFICULTY_MAX = 15;

/** The default age group; the locale's first base bundle plus every other bundle offered in it (plan 71);
 * 12 levels, 4 cards, media allowed, answers on; the standard joker set (configure screen only, D-88). */
export function defaultChoice(data: EngineData): Choice {
  const offered = bundlesFor(data);
  const base = offered.find((b) => b.kind === "base");
  return {
    age_group: DEFAULT_AGE_GROUP, difficulty: null,
    bundles: offered.filter((b) => b === base || b.kind !== "base").map((b) => b.id),
    levels: LEVELS, cards: PER_LEVEL, video: true, audio: true, answers: true, jokers: { ...STANDARD_JOKERS },
  };
}

/** The game's choice; missing keys, an unknown group or bundles that don't resolve (plan 71) are the
 * defaults (jokers: the game's budget), resolved here and never written back. */
export function gameChoice(state: Pick<GameState, "settings">, data: EngineData): Choice {
  const d = defaultChoice(data);
  const { age_group, bundles, difficulty, levels, cards, video, audio, answers, jokers } = state.settings;
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
    levels: levels ?? d.levels, cards: cards ?? d.cards, video: video !== false, audio: audio !== false,
    answers: answers !== false, jokers: { ...jokers },
  };
}

/** Bundles offered in the locale, duplicates dropped, any combination (plan 151), bundles.json order. */
function resolveBundles(data: EngineData, wanted: unknown): string[] {
  if (!Array.isArray(wanted)) throw new GameError("bundles_not_list");
  const known = new Set(data.bundles.map((b) => b.id));
  const offered = new Set(bundlesFor(data).map((b) => b.id));
  for (const b of wanted) {
    if (typeof b !== "string" || !known.has(b)) throw new GameError("bundle_unknown", { bundle: String(b) });
    if (!offered.has(b)) throw new GameError("bundle_not_offered", { bundle: b, locale: data.locale });
  }
  return data.bundles.filter((b) => wanted.includes(b.id)).map((b) => b.id);
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
  /** Gamemaster mode only (D-105). */
  answers?: unknown;
  /** Merged into `base.jokers`. */
  jokers?: unknown;
}

export const CHOICE_KEYS = ["age_group", "difficulty", "bundles", "levels", "cards", "video", "audio", "answers", "jokers"] as const;

const isInt = (v: unknown): v is number => Number.isInteger(v);

function checkDifficulty(d: unknown): Difficulty {
  const ok = (n: unknown): n is number => isInt(n) && 1 <= n && n <= DIFFICULTY_MAX;
  if (d === null || typeof d !== "object" || Array.isArray(d)) throw new GameError("difficulty_invalid");
  const { start, end } = d as Record<string, unknown>;
  if (!ok(start) || !ok(end) || end < start) throw new GameError("difficulty_invalid");
  return { start, end };
}

/** A whole number min..max; GameError `code` if not. */
export function checkCount(v: unknown, min: number, max: number, code: string): number {
  if (!isInt(v) || v < min || v > max) throw new GameError(code, { min, max });
  return v;
}

function checkSwitch(v: unknown, field: string): boolean {
  if (typeof v !== "boolean") throw new GameError("switch_invalid", { field });
  return v;
}

/** A partial budget {joker: count or null} as sent; GameError if malformed. */
export function checkBudget(budget: unknown): Partial<JokerBudget> {
  if (budget === null || typeof budget !== "object" || Array.isArray(budget)
    || !Object.keys(budget).every((k) => (JOKERS as string[]).includes(k)))
    throw new GameError("budget_unknown_joker");
  for (const v of Object.values(budget))
    if (v !== null && !(isInt(v) && 0 <= v && v <= 99)) throw new GameError("budget_invalid");
  return budget as Partial<JokerBudget>;
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
    answers: or(input.answers, base.answers, (v) => checkSwitch(v, "answers")),
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

/** Video / audio questions off (D-88): images and backgrounds stay. */
export function mediaAllowed(s: { video?: boolean; audio?: boolean }): (q: PoolQuestion) => boolean {
  return (q) => !((s.video === false && q.media?.type === "video") || (s.audio === false && q.media?.type === "audio"));
}
