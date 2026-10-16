import * as engine from "../engine/api.ts";
import { gameChoice, jokersUsed, playerMode, view } from "../engine/game.ts";
import { seededRng } from "../engine/rng.ts";
import type { Outlook } from "../engine/outlook.ts";
export type { Outlook };
import { bundlesFor, type Bundle } from "../engine/pool.ts";
import { setFlag as saveFlag, setReported, type FlagInput } from "../engine/save.ts";
import { newest, withDefaults, type EngineData, type SaveData } from "../engine/state.ts";
import { messageOf } from "./http.ts";
import { language as fetchLanguage, nextLocale, read, run, type DataScope, type Route } from "./engine.ts";
import { emit, runAfter, runBefore } from "./mods.ts";
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

/** A report of `id` was sent (plan 93); returns every flagged question. */
export async function markReported(id: string): Promise<Flagged[]> {
  return run((save, data, io) => {
    try {
      const out = setReported(save, id, io.now);
      return { save: out, status: 200, body: flagList(out, data) };
    } catch (e) {
      return { save, status: 400, body: { error: "flag_invalid", message: messageOf(e) } };
    }
  });
}

export async function fetchGame(): Promise<{ game: Game | null }> {
  return read((save, data, io) => engine.getGame(save, data, io));
}

/** The body of a game action: `index` for pick/answer, `player` for new, `everyone` for skip (D-28),
 * `jokers` for the joker budget (MD-4); new: the configuration (D-88); cheats (MD-12): `seen` for
 * replace, `level` for level, age_group / difficulty / bundles / answers for settings; `id` for goto (dev mode). */
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
  answers?: boolean;
  seen?: boolean;
  id?: string;
  level?: number;
}

/** A configuration for `choice` and `new` (D-88): a missing field comes from the player's newest game. */
export type ChoiceBody = Pick<GameActionBody, "age_group" | "difficulty" | "bundles" | "levels" | "cards" | "video" | "audio" | "answers" | "jokers">;

/** What the Choice screen offers (plan 29): age groups in file order, the new game's locale's bundles
 * (plan 71), both with their names in that locale; `scope` "game": the running game's locale (MD-12). */
export interface ChoiceOptions {
  /** `span`: lowest and highest difficulty of its levels (the «Custom» start, D-88). */
  groups: { id: string; name: string; ages: readonly [number, number | null]; span: readonly [number, number] }[];
  /** `source`/`modName`: a mod's bundle (decision 128), marked player-made. */
  bundles: { id: string; base: boolean; name: string; description: string; source?: "mod"; modName?: string }[];
}

/** A bundle's name in the UI language (plan 127), else bundles.json's. */
const bundleName = (data: EngineData, b: Bundle): string => data.uiNames.bundles[b.id]?.name ?? b.name;

export async function fetchChoiceOptions(scope: DataScope = "next"): Promise<ChoiceOptions> {
  return read((save, data) => {
    const groups = data.ageGroups.map(({ id, name, ages, levels }) => ({
      id, name: data.uiNames.age_groups[id] ?? name, ages, span: [levels[0][0], levels[levels.length - 1][1]] as const,
    }));
    const bundles = bundlesFor(data).map((b) => {
      const n = data.uiNames.bundles[b.id];
      return {
        id: b.id, base: b.kind === "base", name: bundleName(data, b), description: n?.description ?? b.description,
        ...(b.source === "mod" && { source: b.source, modName: b.modName ?? b.mod ?? b.id }),
      };
    });
    return { save, status: 200, body: { groups, bundles } };
  }, scope);
}

/** Credits of the loaded mod bundles' media (decision 129): per bundle, deduped credit + source_url. */
export async function fetchModCredits(): Promise<{ bundle: string; name: string; mod: string; items: { credit: string | null; url: string | null }[] }[]> {
  return read((save, data) => {
    const body = data.bundles.filter((b) => b.source === "mod").flatMap((b) => {
      const seen = new Map<string, { credit: string | null; url: string | null }>();
      for (const q of data.pool) {
        if (q.bundle !== b.id) continue;
        for (const m of [q.media, q.background]) {
          if (!m?.file_url || (!m.credit && !m.source_url)) continue;
          seen.set(`${m.credit}\n${m.source_url}`, { credit: m.credit, url: m.source_url });
        }
      }
      return seen.size ? [{ bundle: b.id, name: bundleName(data, b), mod: b.modName ?? b.mod ?? b.id, items: [...seen.values()] }] : [];
    });
    return { save, status: 200, body };
  });
}

/** The running game's choice for the overlay (plan 29): group name or custom difficulty, active bundle
 * names (base first, then file order); missing keys read as the locale's defaults (`gameChoice`). */
export async function fetchGameChoice(settings: Game["settings"]): Promise<{ group: string | null; difficulty: Difficulty | null; bundles: string[] }> {
  return read((save, data) => {
    const c = gameChoice({ settings }, data);
    const group = c.age_group === null ? null : (data.uiNames.age_groups[c.age_group] ?? data.groupById.get(c.age_group)?.name ?? c.age_group);
    const on = data.bundles.filter((b) => c.bundles.includes(b.id));
    const bundles = [...on.filter((b) => b.kind === "base"), ...on.filter((b) => b.kind !== "base")]
      .map((b) => bundleName(data, b));
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

/** The supply outlook of a new game (plan 65, decision 31): tight levels, none left, bundle hint, bundles running out. */
export async function fetchOutlook(body: ChoiceBody & { mode: GameMode }): Promise<Outlook> {
  return read((save, data) => engine.outlook(save, data, { ...body }), "next");
}

/** At every game start: the bundles just shown as running out; prunes the rest (plan 65). */
export async function noteRunningOut(body: ChoiceBody, shown: string[]): Promise<void> {
  await run((save, data) => engine.noteRunningOut(save, data, { ...body, shown }), "next");
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
  return hooked("joker", body, "game") as Promise<{ game: Game; event: JokerEvent }>;
}

/** The newest game as it was before an action, for the mods' events (plan 117). */
interface Before {
  id: number;
  result: Game["result"];
  question: string | null;
  level: number;
  /** The running game's view, kept only when a `new` abandons it. */
  game: Game | null;
}

/** An engine action between the mods' `before` and `after` hooks; emits the game events. */
async function hooked(action: string, input: object, scope: DataScope): Promise<{ game: Game | null; event?: JokerEvent }> {
  const body = runBefore(action, { ...input });
  const seen: { before: Before | null } = { before: null };
  const route: Route<{ game: Game | null; event?: JokerEvent }> = (save, data, io) => {
    const row = newest(save.games);
    if (row) {
      const running = row.result === null;
      // A throwaway rng: the view's joker trials mustn't use up the action's.
      const game = action === "new" && running ? view(save, data, { ...io, rng: seededRng(0) }) : null;
      seen.before = { id: row.id, result: row.result, question: row.state.current ?? null, level: row.state.level, game };
    }
    return engine.gameAction(save, data, io, action, body as Record<string, unknown>);
  };
  const out = await run(route, scope);
  events(action, body, seen.before, out.game);
  runAfter(action, out.game);
  return out;
}

function events(action: string, body: GameActionBody, before: Before | null, game: Game | null): void {
  if (before?.result === null && before.game && game && game.id !== before.id) {
    emit("game:end", { game: { ...before.game, result: "abandoned" }, result: "abandoned" });
  }
  if (action === "answer" && before?.question && game?.last) {
    emit("question:answered", { id: before.question, level: before.level, index: body.index ?? -1, correct: game.last.correct });
  }
  if (action === "new" && game) emit("game:start", { game });
  if (game && before?.id === game.id && before.result === null && game.result !== null) {
    emit("game:end", { game, result: game.result });
  }
}

/** A game action on the engine (engine/api.ts); returns the game afterwards. */
export async function gameAction(
  action: "new" | "pick" | "answer" | "reveal" | "skip" | "undo" | "abandon" | "jokers" | "replace" | "level" | "goto" | "settings",
  body: GameActionBody = {},
): Promise<Game | null> {
  const scope = action === "new" ? "next" : "game";
  return (await hooked(action, body, scope)).game;
}

/** The stored language and the options (plans 68, 126); the next game's question locale. */
export { fetchLanguage, nextLocale };

/** Set the language; its questions apply to the next game, the UI after a reload. */
export async function setLanguage(language: Language): Promise<Language> {
  const { options } = await fetchLanguage();
  return (await run((save) => engine.setLanguage(save, { language }, options))).language;
}

/** Choice limits and defaults for the configure screen and overlay (engine/choice.ts). */
export { BUILT_MODES, CARDS_MAX, DEFAULT_AGE_GROUP, DIFFICULTY_MAX, LEVELS_MAX, STANDARD_JOKERS } from "../engine/game.ts";
