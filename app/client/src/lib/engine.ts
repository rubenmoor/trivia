// The TS referee in the browser (plan 50, PORT-7): data and save loaded once per page, one action at a time.
import type { ErrorBody, Reply } from "../engine/api.ts";
import { randomSeed, seededRng } from "../engine/rng.ts";
import { defaultLanguage } from "../engine/save.ts";
import { gameLocale, type EngineData, type Io, type Language, type SaveData } from "../engine/state.ts";
import { GameError } from "./api.ts";
import { availableLocales, loadEngineData } from "./data.ts";
import { desktop } from "./desktop.ts";
import { UI_LANGS } from "./i18n.ts";
import { FileStore, ServerStore, type SaveNotice } from "./store.ts";

interface Loaded {
  save: SaveData & { language: Language };
  /** Question locales with a pool (plan 68). */
  locales: string[];
}

const store = desktop ? new FileStore(desktop) : new ServerStore();
let loading: Promise<Loaded> | null = null;
let chain: Promise<unknown> = Promise.resolve();
let lastSaveError: GameError | null = null;

/** Save + available locales, once per page load; a fresh save gets the browser's language (plan 68).
 * A failure is retried on the next call. */
export function ready(): Promise<Loaded> {
  loading ??= Promise.all([store.load(), availableLocales()]).then(
    async ([save, locales]) => {
      let language = save.language ?? defaultLanguage(globalThis.navigator?.language ?? "es", UI_LANGS, locales);
      if (!locales.includes(language.questions)) language = { ...language, questions: "es" }; // pool gone
      const loaded = { save: { ...save, language }, locales };
      await dataFor(loaded, "game"); // a missing data file fails here, not on the first action
      return loaded;
    },
    (e) => {
      loading = null;
      throw new Error(`can't load the game: ${e instanceof Error ? e.message : String(e)}`);
    },
  );
  return loading;
}

/** The notice of a backed-up save file (plan 55), once; null after that and in the browser. */
export function takeSaveNotice(): SaveNotice | null {
  if (!(store instanceof FileStore)) return null;
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
export function localIsoSeconds(d = new Date()): string {
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

/** The stored language (fresh save: the default), and the options a player can pick from. */
export async function language(): Promise<{ language: Language; ui: string[]; questions: string[] }> {
  const { save, locales } = await ready();
  return { language: save.language, ui: UI_LANGS, questions: locales };
}

/** `game`: the newest game's data (it keeps its locale), else the language's; `next`: the language's
 * (a new game). No mid-game pool swap. */
export type Scope = "game" | "next";

function dataFor({ save }: Loaded, scope: Scope): Promise<EngineData> {
  const newest = save.games.reduce<SaveData["games"][number] | null>((m, g) => (m && m.id > g.id ? m : g), null);
  return loadEngineData("", scope === "game" && newest ? gameLocale(newest) : save.language.questions);
}

export type Route<T> = (save: SaveData, data: EngineData, io: Io) => Reply<T>;

async function exec<T>(route: Route<T>, write: boolean, scope: Scope): Promise<T> {
  const loaded = await ready();
  const data = await dataFor(loaded, scope);
  let reply: Reply<T>;
  try {
    reply = route(loaded.save, data, io());
  } catch (e) {
    throw new GameError("server_error", {}, `engine error: ${e instanceof Error ? e.message : String(e)}`, null);
  }
  if (reply.status !== 200) {
    const b = reply.body as ErrorBody;
    throw new GameError(b.error, b.params ?? {}, b.message ?? b.error, b.supply ?? null);
  }
  if (write) {
    loaded.save = { ...reply.save, language: reply.save.language ?? loaded.save.language };
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
export function read<T>(route: Route<T>, scope: Scope = "game"): Promise<T> {
  return exclusive(() => exec(route, false, scope));
}

/** An action: 200 → adopt the new save and PUT it whole; else the save stays. */
export function run<T>(route: Route<T>, scope: Scope = "game"): Promise<T> {
  return exclusive(() => exec(route, true, scope));
}
