// The TS referee in the browser (plan 50, PORT-7): data and save loaded once per page, one action at a time.
import type { ErrorBody, Reply } from "../engine/api.ts";
import { randomSeed, seededRng } from "../engine/rng.ts";
import { repair, supply } from "../engine/game.ts";
import { defaultLanguage } from "../engine/save.ts";
import { gameLocale, newest, type EngineData, type Io, type Language, type SaveData } from "../engine/state.ts";
import { GameError, messageOf } from "./http.ts";
import { availableLocales, loadEngineData } from "./data.ts";
import { desktop, steam, validUser } from "./desktop.ts";
import { UI_LANGS } from "./i18n.ts";
import { useNames } from "./names.svelte.ts";
import { FileStore, MemoryStore, type SaveNotice } from "./store.ts";
import { telemetryCheckpoint, telemetryLoad } from "./telemetry.ts";
import { achievementsCheckpoint, achievementsLoad } from "./achievements.ts";

interface Loaded {
  save: SaveData & { language: Language };
  /** Question locales with a pool file (plan 68). */
  locales: string[];
  /** No save stored yet (no file, 404, backed-up broken file): the first-start screen may ask (plan 68). */
  fresh: boolean;
}

/** Saves need a valid Steam user (decision 111); else memory only, every start fresh. */
const store = desktop && validUser ? new FileStore(desktop) : new MemoryStore();
let loading: Promise<Loaded> | null = null;
let chain: Promise<unknown> = Promise.resolve();
let lastSaveError: GameError | null = null;

/** Steam's API language names → our tags (plan 85); unknown → null. */
const STEAM_LANGS = new Map([
  ["latam", "es"],
  ["spanish", "es-ES"],
  ["english", "en"],
  ["german", "de"],
  ["schinese", "zh-Hans"],
  ["russian", "ru"],
  ["brazilian", "pt-BR"],
]);

function fromSteam(name: string | null): string | null {
  return (name && STEAM_LANGS.get(name)) ?? null;
}

/** The player's language tag: Steam's game/client language, else the browser's (plans 68, 85). */
async function guessTag(): Promise<string> {
  const fromClient = steam?.available ? fromSteam(await steam.language().catch(() => null)) : null;
  return fromClient ?? globalThis.navigator?.language ?? "es";
}

/** Save + available locales, once per page load; a fresh save gets the guessed language (plan 68).
 * A failure is retried on the next call. */
function ready(): Promise<Loaded> {
  loading ??= load().catch((e) => {
    loading = null;
    throw new Error(`can't load the game: ${messageOf(e)}`);
  });
  return loading;
}

async function load(): Promise<Loaded> {
  const [save, locales] = await Promise.all([store.load(), availableLocales()]);
  const language = save.language ?? defaultLanguage(await guessTag(), UI_LANGS);
  const fresh = !save.language;
  const loaded = { save: { ...save, language }, locales, fresh };
  const data = await dataFor(loaded, "game"); // a missing data file fails here, not on the first action
  loaded.save = { ...repair(loaded.save, data, io()), language }; // dropped questions (plan 91); written with the next action
  telemetryLoad(loaded.save);
  achievementsLoad(loaded.save, data);
  return loaded;
}

/** The notice of a backed-up save file (plan 55, decision 98) or of a memory-only save (plan 87), once; null after that. */
export function takeSaveNotice(): SaveNotice | null {
  const notice = store.notice;
  store.notice = null;
  return notice;
}

/** `save_locked` of the last write, until one succeeds. */
export function saveError(): GameError | null {
  return lastSaveError;
}

/** Resolves when every save is written (before «Salir del juego»). */
export function flush(): Promise<void> {
  return store.flush();
}

/** Python's datetime.now().isoformat(timespec="seconds"): local, no zone. */
function localIsoSeconds(d = new Date()): string {
  const p = (n: number) => String(n).padStart(2, "0");
  return `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())}T${p(d.getHours())}:${p(d.getMinutes())}:${p(d.getSeconds())}`;
}

function io(): Io {
  return { rng: seededRng(randomSeed()), now: localIsoSeconds() };
}

/** Promise-chain mutex: one call at a time (was the server's _lock). */
function exclusive<T>(fn: () => Promise<T>): Promise<T> {
  const out = chain.then(fn);
  chain = out.catch(() => {});
  return out;
}

/** The stored language (fresh save: the default), the options a player can pick from, and whether
 * the first-start screen asks (a fresh save with something to pick). */
export async function language(): Promise<{ language: Language; options: string[]; ask: boolean }> {
  const { save, fresh } = await ready();
  return { language: save.language, options: UI_LANGS, ask: fresh && UI_LANGS.length > 1 };
}

/** The questions of `lang` (plan 126): its own pool if it has one whose default bundles' supply passes, else es. */
async function localeOf({ save, locales }: Loaded, lang: Language): Promise<string> {
  if (lang === "es" || !locales.includes(lang)) return "es";
  return supply(save, await loadEngineData(lang)).ok ? lang : "es";
}

/** The question locale of the save's language: what a new game plays. */
export async function nextLocale(): Promise<string> {
  const loaded = await ready();
  return localeOf(loaded, loaded.save.language);
}

/** `game`: the newest game's data (it keeps its locale), else the language's; `next`: the language's
 * (a new game). No mid-game pool swap. */
export type DataScope = "game" | "next";

async function dataFor(loaded: Loaded, scope: DataScope): Promise<EngineData> {
  const row = newest(loaded.save.games);
  return loadEngineData(scope === "game" && row ? gameLocale(row) : await localeOf(loaded, loaded.save.language), loaded.save.language);
}

export type Route<T> = (save: SaveData, data: EngineData, io: Io) => Reply<T>;

async function exec<T>(route: Route<T>, write: boolean, scope: DataScope): Promise<T> {
  const loaded = await ready();
  const data = await dataFor(loaded, scope);
  useNames(data);
  let reply: Reply<T>;
  try {
    reply = route(loaded.save, data, io());
  } catch (e) {
    throw new GameError("server_error", {}, `engine error: ${messageOf(e)}`, null);
  }
  if (reply.status !== 200) {
    const b = reply.body as ErrorBody;
    throw new GameError(b.error, b.params ?? {}, b.message ?? b.error, b.supply ?? null);
  }
  if (write) {
    loaded.save = { ...reply.save, language: reply.save.language ?? loaded.save.language };
    loaded.fresh = false;
    telemetryCheckpoint(loaded.save);
    achievementsCheckpoint(loaded.save, data);
    try {
      await store.save(reply.save); // on failure the new save stays; the next action PUTs it again
      lastSaveError = null;
    } catch (e) {
      if (!(e instanceof GameError && e.code === "save_locked")) throw e;
      lastSaveError = e; // the action stands (plan 55): the UI moves on with the in-memory save
    }
  }
  return reply.body as T;
}

/** A read: never PUTs. */
export function read<T>(route: Route<T>, scope: DataScope = "game"): Promise<T> {
  return exclusive(() => exec(route, false, scope));
}

/** An action: 200 → adopt the new save and PUT it whole; else the save stays. */
export function run<T>(route: Route<T>, scope: DataScope = "game"): Promise<T> {
  return exclusive(() => exec(route, true, scope));
}
