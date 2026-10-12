// The TS referee in the browser (plan 50, PORT-7): data and save loaded once per page, one action at a time.
import type { ErrorBody, Reply } from "../engine/api.ts";
import { randomSeed, seededRng } from "../engine/rng.ts";
import type { EngineData, Io, SaveData } from "../engine/state.ts";
import { MemoryStore } from "../engine/store.ts";
import { GameError } from "./api.ts";
import { loadEngineData } from "./data.ts";
import { desktop } from "./desktop.ts";
import { ServerStore } from "./store.ts";

interface Loaded {
  data: EngineData;
  save: SaveData;
}

const store = desktop ? new MemoryStore() : new ServerStore(); // desktop: in memory until SW-3
let loading: Promise<Loaded> | null = null;
let chain: Promise<unknown> = Promise.resolve();

/** Data files + save, once per page load; a failure is retried on the next call. */
export function ready(): Promise<Loaded> {
  loading ??= Promise.all([loadEngineData(), store.load()]).then(
    ([data, save]) => ({ data, save }),
    (e) => {
      loading = null;
      throw new Error(`can't load the game: ${e instanceof Error ? e.message : String(e)}`);
    },
  );
  return loading;
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

export type Route<T> = (save: SaveData, data: EngineData, io: Io) => Reply<T>;

async function exec<T>(route: Route<T>, write: boolean): Promise<T> {
  const loaded = await ready();
  let reply: Reply<T>;
  try {
    reply = route(loaded.save, loaded.data, io());
  } catch (e) {
    throw new GameError("server_error", {}, `engine error: ${e instanceof Error ? e.message : String(e)}`, null);
  }
  if (reply.status !== 200) {
    const b = reply.body as ErrorBody;
    throw new GameError(b.error, b.params ?? {}, b.message ?? b.error, b.supply ?? null);
  }
  if (write) {
    loaded.save = reply.save;
    await store.save(reply.save); // on failure the new save stays; the next action PUTs it again
  }
  return reply.body as T;
}

/** A read: never PUTs. */
export function read<T>(route: Route<T>): Promise<T> {
  return exclusive(() => exec(route, false));
}

/** An action: 200 → adopt the new save and PUT it whole; else the save stays. */
export function run<T>(route: Route<T>): Promise<T> {
  return exclusive(() => exec(route, true));
}
