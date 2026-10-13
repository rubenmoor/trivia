import * as engine from "../engine/api.ts";
import { gameChoice, jokersUsed, playerMode } from "../engine/game.ts";
import type { Outlook } from "../engine/outlook.ts";
export type { Outlook };
import { bundlesFor } from "../engine/pool.ts";
import { setFlag as saveFlag, type FlagInput } from "../engine/save.ts";
import { newest, withDefaults, type EngineData, type SaveData } from "../engine/state.ts";
import { messageOf } from "./http.ts";
import { language as fetchLanguage, localeSupply, read, run, type DataScope } from "./engine.ts";
import type { Choice, Difficulty, Flagged, Game, GameMode, JokerBudget, JokerEvent, JokerName, Language, Player, Supply } from "./types.ts";

// The game's only door to the referee: the TS engine on an in-memory save, persisted by lib/store.ts (plan 50, PORT-7).

/** Known players, the most recent first (D-28). */
export async function fetchPlayers(): Promise<Player[]> {
  return read((save) => engine.getPlayers(save));
}

/** Delete a player's name and games (GF-7), not what the family saw; returns the remaining players. */
export async function deletePlayer(name: string): Promise<Player[]> {
  return run((save) => engine.deletePlayer(save, { name }));
}

/** Flagged questions (GM-5, decision 60), newest first; the running question's answer stays hidden. */
function flagList(save: SaveData, data: EngineData): Flagged[] {
  const g = newest(save.games);
  const live = g?.result === null && g.state.phase === "question" ? g.state.current : null;
  return Object.entries(save.flags)
    .map(([id, f]) => {
      const { shown, ...rest } = f;
      const q = shown ?? data.byId.get(id);
      return { ...rest, question_id: id, question: q?.question ?? null, answer: id === live ? null : (q?.answer ?? null) };
    })
    .sort((a, b) => (a.flagged_on < b.flagged_on ? 1 : a.flagged_on > b.flagged_on ? -1 : 0));
}

export async function fetchFlags(): Promise<Flagged[]> {
  return read((save, data) => ({ save, status: 200, body: flagList(save, data) }));
}

/** Flag, re-note or unflag (null) a question; returns every flagged question. */
export async function setFlag(id: string, flag: FlagInput): Promise<Flagged[]> {
  return run((save, data, io) => {
    try {
      const q = data.byId.get(id);
      const shown = q && { question: q.question, answer: q.answer, wrong_answers: q.wrong_answers };
      const out = saveFlag(save, id, flag && { ...flag, locale: data.locale, ...(shown ? { shown } : {}) }, io.now);
      return { save: out, status: 200, body: flagList(out, data) };
    } catch (e) {
      return { save, status: 400, body: { error: "flag_invalid", message: messageOf(e) } };
    }
  });
}

export async function fetchGame(): Promise<{ game: Game | null; supply: Supply }> {
  return read((save, data, io) => engine.getGame(save, data, io));
}

/** The body of a game action: `index` for pick/answer, `player` for new, `everyone` for skip (D-28),
 * `jokers` for the joker budget (MD-4); new: the configuration (D-88); cheats (MD-12): `seen` for
 * replace, `level` for level, age_group / difficulty / bundles for settings; `id` for goto (dev mode). */
export interface GameActionBody {
  index?: number;
  player?: string;
  everyone?: boolean;
  jokers?: Partial<JokerBudget>;
  mode?: GameMode;
  age_group?: string | null;
  difficulty?: Difficulty | null;
  bundles?: string[];
  levels?: number;
  cards?: number;
  video?: boolean;
  audio?: boolean;
  seen?: boolean;
  id?: string;
  level?: number;
}

/** A configuration for `choice` and `new` (D-88): a missing field comes from the player's newest game. */
export type ChoiceBody = Pick<GameActionBody, "age_group" | "difficulty" | "bundles" | "levels" | "cards" | "video" | "audio" | "jokers">;

/** What the Choice screen offers (plan 29): age groups in file order, the new game's locale's bundles
 * (plan 71), both with their names in that locale; `scope` "game": the running game's locale (MD-12). */
export interface ChoiceOptions {
  /** `span`: lowest and highest difficulty of its levels (the «Custom» start, D-88). */
  groups: { id: string; name: string; ages: readonly [number, number | null]; span: readonly [number, number] }[];
  bundles: { id: string; base: boolean; name: string; description: string }[];
}

export async function fetchChoiceOptions(scope: DataScope = "next"): Promise<ChoiceOptions> {
  return read((save, data) => {
    const groups = data.ageGroups.map(({ id, name, ages, levels }) => ({
      id, name: data.names.age_groups[id] ?? name, ages, span: [levels[0][0], levels[levels.length - 1][1]] as const,
    }));
    const bundles = bundlesFor(data).map((b) => {
      const n = data.names.bundles[b.id];
      return { id: b.id, base: b.kind === "base", name: n?.name ?? b.name, description: n?.description ?? b.description };
    });
    return { save, status: 200, body: { groups, bundles } };
  }, scope);
}

/** The running game's choice for the overlay (plan 29): group name or custom difficulty, active bundle
 * names (base first, then file order); missing keys read as the locale's defaults (`gameChoice`). */
export async function fetchGameChoice(settings: Game["settings"]): Promise<{ group: string | null; difficulty: Difficulty | null; bundles: string[] }> {
  return read((save, data) => {
    const c = gameChoice({ settings }, data);
    const group = c.age_group === null ? null : (data.names.age_groups[c.age_group] ?? data.groupById.get(c.age_group)?.name ?? c.age_group);
    const on = data.bundles.filter((b) => c.bundles.includes(b.id));
    const bundles = [...on.filter((b) => b.kind === "base"), ...on.filter((b) => b.kind !== "base")]
      .map((b) => data.names.bundles[b.id]?.name ?? b.name);
    return { save, status: 200, body: { group, difficulty: c.difficulty, bundles } };
  });
}

/** The running game's choice as ids (`gameChoice`), for the menu's difficulty and bundles (MD-12). */
export async function fetchGameSettings(settings: Game["settings"]): Promise<Choice> {
  return read((save, data) => ({ save, status: 200, body: gameChoice({ settings }, data) }));
}

/** Joker uses so far in the running game (MD-12: the menu edits uses left), null without one. */
export async function fetchJokersUsed(): Promise<Record<JokerName, number> | null> {
  return read((save) => {
    const g = newest(save.games);
    return { save, status: 200, body: g?.result === null ? jokersUsed(withDefaults(structuredClone(g.state))) : null };
  });
}

/** The player's preset (missing fields) and the supply of a choice (plan 27's `choice` route); a
 * refused choice throws GameError (`base_bundle_count`, `bundle_not_offered`). */
export async function fetchChoice(body: ChoiceBody & { player?: string }): Promise<{ choice: Choice; supply: Supply }> {
  return read((save, data) => engine.choice(save, data, { ...body }), "next");
}

/** The supply outlook of a new game (plan 65, decision 31): tight levels, none left, bundle hint, exhausted subcategories. */
export async function fetchOutlook(body: ChoiceBody & { mode: GameMode }): Promise<Outlook> {
  return read((save, data) => engine.outlook(save, data, { ...body }), "next");
}

/** At every game start: the exhausted subcategories just shown; prunes the rest (plan 65). */
export async function noteExhausted(body: ChoiceBody, subcategories: string[]): Promise<void> {
  await run((save, data) => engine.noteExhausted(save, data, { ...body, subcategories }), "next");
}

/** The mode of the player's newest game, else gamemaster (MD-7). */
export async function fetchPlayerMode(player: string): Promise<GameMode> {
  return read((save) => ({ save, status: 200, body: playerMode(save, player) }), "next");
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

/** A game action on the engine (engine/api.ts); returns the game afterwards. */
export async function gameAction(
  action: "new" | "pick" | "answer" | "skip" | "undo" | "abandon" | "jokers" | "replace" | "level" | "goto" | "settings",
  body: GameActionBody = {},
): Promise<Game | null> {
  const scope = action === "new" ? "next" : "game";
  return (await run((save, data, io) => engine.gameAction(save, data, io, action, { ...body }), scope)).game;
}

/** The stored UI and question language, and the options (plan 68). */
export { fetchLanguage, localeSupply };

/** Set both languages; a question language applies to the next game, a UI language after a reload. */
export async function setLanguage(language: Language): Promise<Language> {
  const { ui, questions } = await fetchLanguage();
  return (await run((save) => engine.setLanguage(save, { ...language }, { ui, questions }))).language;
}

/** Choice limits and defaults for the configure screen and overlay (engine/choice.ts). */
export { BUILT_MODES, CARDS_MAX, DEFAULT_AGE_GROUP, DIFFICULTY_MAX, LEVELS_MAX, STANDARD_JOKERS } from "../engine/game.ts";
