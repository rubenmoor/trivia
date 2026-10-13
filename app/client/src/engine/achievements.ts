// Steam achievements (plan 86, SW-11, decision 73): derived from the save, never stored.
import type { GameMode, JokerName } from "../lib/types.ts";
import { DEFAULT_AGE_GROUP } from "./choice.ts";
import { BUILT_MODES, gameMode, jokersUsed } from "./game.ts";
import { categoryOf, isModId } from "./pool.ts";
import { LEVELS, PER_LEVEL } from "./selection.ts";
import type { EngineData, GameRow, GameState, SaveData } from "./state.ts";
import { gameLocale } from "./state.ts";

/** API names in Steamworks; `mode`: entered with that mode (MD-8). */
export const ACHIEVEMENTS = [
  { id: "FIRST_WIN" }, { id: "WINS_10" }, { id: "WINS_50" }, { id: "WIN_ADULTS" }, { id: "WIN_ALL_AGES" },
  { id: "FIRST_SOPLO" }, { id: "FIRST_PASO" }, { id: "FIRST_BAJALE" }, { id: "FIRST_CAMBIAZO" }, { id: "FIRST_FRANCOTIRADOR" },
  { id: "ALL_HINTS" }, { id: "PURGE" }, { id: "SUPER_PICKY" }, { id: "WIN_NO_JOKERS" }, { id: "ALL_JOKERS_WIN" },
  { id: "SNIPER_TOP" }, { id: "SOPLO_SAVE" },
  { id: "ALL_CATEGORIES" }, { id: "SPECIALIST" }, { id: "QUESTIONS_1000" }, { id: "POLYGLOT" },
  { id: "GAME_NIGHTS" }, { id: "CHRISTMAS" }, { id: "NIGHT_OWL" }, { id: "FIRST_FLAG" },
  { id: "WIN_RR_COOP", mode: "rr-coop" }, { id: "WIN_RR_COMPETITIVE", mode: "rr-competitive" }, { id: "WIN_TIMED", mode: "timed" },
] as const satisfies readonly { id: string; mode?: GameMode }[];

/** One per regional bundle, entered with its DLC: `BUNDLE_COLOMBIA`. */
export type AchievementId = (typeof ACHIEVEMENTS)[number]["id"] | `BUNDLE_${string}`;

/** Regional bundles whose DLC (and achievement) is in Steamworks. */
export const DLC_BUNDLES: readonly string[] = [];

export const bundleAchievement = (bundle: string): AchievementId => `BUNDLE_${bundle.toUpperCase()}`;

const FIRST_USE: Record<JokerName, AchievementId> = {
  hint: "FIRST_SOPLO", skip: "FIRST_PASO", easier: "FIRST_BAJALE", category: "FIRST_CAMBIAZO", snipe: "FIRST_FRANCOTIRADOR",
};
const JOKER_MODES: readonly GameMode[] = ["solo", "rr-coop", "rr-competitive"];
const MODE_WIN = new Map<GameMode, AchievementId>(ACHIEVEMENTS.flatMap((a) => ("mode" in a ? [[a.mode, a.id]] : [])));
const MANY = 50;
const SEEN = 1000;
const DAYS = 7;
const LANGUAGES = 2;
/** «After midnight»: finished before 05:00, local clock. */
const NIGHT_END = 5;

/** In Steamworks now: mode wins with their mode built, bundle ones with their DLC. */
export function inSteamworks(id: AchievementId): boolean {
  const mode = ACHIEVEMENTS.find((a) => a.id === id && "mode" in a);
  if (mode && "mode" in mode) return BUILT_MODES.includes(mode.mode);
  return id.startsWith("BUNDLE_") ? DLC_BUNDLES.some((b) => bundleAchievement(b) === id) : true;
}

/** Standard rules only (decisions 19, 74): not gamemaster, not customized, 12 levels, 4 cards, no «Ir a pregunta…». */
export function qualifies(row: GameRow): boolean {
  const s = row.state.settings ?? {};
  return gameMode(row.state) !== "gamemaster" && !s.customized && !s.difficulty
    && (s.levels ?? LEVELS) === LEVELS && (s.cards ?? PER_LEVEL) === PER_LEVEL
    && !(row.state.history ?? []).some((h) => h.outcome === "admin_replace");
}

type Entry = GameState["history"][number];

/** The history plus the question on screen (its jokers so far). */
function entries(state: GameState): Entry[] {
  const history = state.history ?? [];
  return state.phase === "question" && state.current !== null
    ? [...history, { level: state.level, question_id: state.current, jokers: state.jokers ?? [] }]
    : history;
}

/** Every achievement the save has earned; questions outside `data`'s pool are ignored. */
export function earned(save: SaveData, data: EngineData): AchievementId[] {
  const out = new Set<AchievementId>();
  const games = save.games.filter(qualifies);
  const won = games.filter((g) => g.result === "won");
  const cat = categoryOf(data.broad);
  const correct = games.flatMap((g) => (g.state.history ?? []).filter((h) => h.correct === true))
    .flatMap((h) => data.byId.get(h.question_id) ?? []);
  const count = <T>(items: T[], key: (x: T) => string | null): Map<string, number> => {
    const m = new Map<string, number>();
    for (const x of items) {
      const k = key(x);
      if (k !== null) m.set(k, (m.get(k) ?? 0) + 1);
    }
    return m;
  };

  if (won.length) out.add("FIRST_WIN");
  if (won.length >= 10) out.add("WINS_10");
  if (won.length >= MANY) out.add("WINS_50");
  const ages = new Set(won.map((g) => g.state.settings.age_group ?? DEFAULT_AGE_GROUP));
  if (ages.has("adults")) out.add("WIN_ADULTS");
  if (data.ageGroups.length && data.ageGroups.every((a) => ages.has(a.id))) out.add("WIN_ALL_AGES");

  for (const g of games) {
    const all = entries(g.state);
    for (const e of all) {
      const jokers = e.jokers ?? [];
      for (const j of jokers) out.add(FIRST_USE[j]);
      const hints = data.byId.get(e.question_id)?.hints.length ?? 0;
      if (hints && jokers.filter((j) => j === "hint").length >= hints) out.add("ALL_HINTS");
      if (e.outcome === "sniped" && e.level === LEVELS) out.add("SNIPER_TOP");
    }
    if ((g.state.purged ?? []).length) out.add("PURGE");
    const levels = (outcome: Entry["outcome"]) => new Set(all.filter((e) => e.outcome === outcome).map((e) => e.level));
    const easier = levels("easier");
    if ([...levels("skipped")].some((l) => easier.has(l))) out.add("SUPER_PICKY");
  }

  for (const g of won) {
    const used = Object.values(jokersUsed({ history: g.state.history ?? [], jokers: g.state.jokers ?? [] }));
    const mode = gameMode(g.state);
    if (used.every((n) => n === 0) && JOKER_MODES.includes(mode)) out.add("WIN_NO_JOKERS");
    if (used.every((n) => n > 0)) out.add("ALL_JOKERS_WIN");
    if (g.state.history?.at(-1)?.jokers?.includes("hint")) out.add("SOPLO_SAVE");
    if (g.finished_on && Number(g.finished_on.slice(11, 13)) < NIGHT_END) out.add("NIGHT_OWL");
    const modeWin = MODE_WIN.get(mode);
    if (modeWin) out.add(modeWin);
  }

  const base = data.categories.filter((c) => c.bundle === "base").map((c) => c.slug);
  const offered = new Set(data.pool.filter((q) => q.status === "approved").map(cat));
  const hit = count(correct, cat);
  if (base.some((c) => offered.has(c)) && base.every((c) => !offered.has(c) || hit.has(c))) out.add("ALL_CATEGORIES");
  if ([...hit.values()].some((n) => n >= MANY)) out.add("SPECIALIST");
  if (new Set(games.flatMap((g) => (g.state.history ?? []).map((h) => h.question_id))).size >= SEEN) out.add("QUESTIONS_1000");
  if (new Set(won.map(gameLocale)).size >= LANGUAGES) out.add("POLYGLOT");

  const days = games.flatMap((g) => [g.started_on, g.finished_on ?? g.started_on].map((d) => d.slice(0, 10)));
  if (new Set(games.map((g) => g.started_on.slice(0, 10))).size >= DAYS) out.add("GAME_NIGHTS");
  if (days.some((d) => d.endsWith("-12-24") || d.endsWith("-12-25"))) out.add("CHRISTMAS");
  if (Object.keys(save.flags).length) out.add("FIRST_FLAG");

  const fromBundle = count(correct, (q) => q.bundle);
  for (const b of data.bundles)
    if (b.kind === "region" && !isModId(b.id) && (fromBundle.get(b.id) ?? 0) >= MANY) out.add(bundleAchievement(b.id));
  return [...out];
}
