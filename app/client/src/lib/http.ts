// fetch helpers and the request error; a leaf module (no imports from lib/), so api.ts, engine.ts, store.ts
// and data.ts import it without a cycle.
import type { ErrorInfo, Supply } from "./types.ts";

/** A refused request (D-57): `code` and `params` for errorText(), `message` in English; `supply` is set
 * when the pool can't fill a new game (GF-5). */
export class GameError extends Error implements ErrorInfo {
  readonly code: string;
  readonly params: ErrorInfo["params"];
  readonly supply: Supply | null;

  constructor(code: string, params: ErrorInfo["params"], message: string, supply: Supply | null) {
    super(message);
    this.code = code;
    this.params = params;
    this.supply = supply;
  }
}

/** The message of anything thrown. */
export const messageOf = (e: unknown): string => (e instanceof Error ? e.message : String(e));

/** The JSON error body of a refused request (engine/api.ts `ErrorBody`, app/server, authoring/server). */
interface ErrorJson {
  error?: unknown;
  params?: ErrorInfo["params"];
  message?: string;
  supply?: Supply | null;
}

/** The error of a failed response: GameError if the body has `error`, else a plain Error. */
function failure(res: Response, body: ErrorJson): Error {
  if (typeof body.error !== "string") return new Error(`HTTP ${res.status} ${res.statusText}`);
  return new GameError(body.error, body.params ?? {}, body.message ?? body.error, body.supply ?? null);
}

export async function json<T>(res: Response): Promise<T> {
  if (!res.ok) throw failure(res, await res.json().catch(() => ({})));
  return res.json();
}

/** fetch() that turns "server not running" into a readable error naming `server`. */
export async function call(url: string, init?: RequestInit, server = "the game server (`trivia`)"): Promise<Response> {
  try {
    return await fetch(url, init);
  } catch {
    throw new Error(`server not reachable — is ${server} running?`);
  }
}

export async function post<T>(url: string, body: unknown, server?: string): Promise<T> {
  const init = { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) };
  return json(await call(url, init, server));
}
