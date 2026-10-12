// The save on the game server: GET/PUT /api/save (plan 49, PORT-4).
import { parseSave } from "../engine/save.ts";
import { emptySave, type SaveData } from "../engine/state.ts";
import type { Store } from "../engine/store.ts";
import { call, json } from "./api.ts";

/** One PUT in flight; saves made meanwhile coalesce to the newest, so an older document never wins. */
export class ServerStore implements Store {
  private pending: string | null = null;
  private flight: Promise<void> | null = null;

  private readonly base: string;

  constructor(base = "") {
    this.base = base;
  }

  async load(): Promise<SaveData> {
    const res = await call(`${this.base}/api/save`);
    if (res.status === 404) return emptySave();
    return parseSave(await json<unknown>(res));
  }

  /** Resolves once this document, or a newer one, is written; throws with the server's `error` code. */
  save(data: SaveData): Promise<void> {
    this.pending = JSON.stringify(data);
    this.flight ??= this.drain().finally(() => (this.flight = null));
    return this.flight;
  }

  private async drain(): Promise<void> {
    while (this.pending !== null) {
      const body = this.pending;
      this.pending = null;
      await json(await call(`${this.base}/api/save`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body,
      }));
    }
  }
}
