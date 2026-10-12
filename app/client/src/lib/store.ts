// Where the save lives: the game server (GET/PUT /api/save, plan 49) or the desktop's file (plan 55).
import { parseSave, SaveNewerError } from "../engine/save.ts";
import { emptySave, type SaveData } from "../engine/state.ts";
import type { Store } from "../engine/store.ts";
import { call, GameError, json } from "./api.ts";
import type { BackupKind, DesktopBridge } from "./desktop.ts";

/** One write in flight; saves made meanwhile coalesce to the newest, so an older document never wins. */
class WriteQueue {
  private pending: string | null = null;
  private flight: Promise<void> | null = null;
  private readonly write: (text: string) => Promise<void>;

  constructor(write: (text: string) => Promise<void>) {
    this.write = write;
  }

  /** Resolves once this document, or a newer one, is written. */
  push(text: string): Promise<void> {
    this.pending = text;
    this.flight ??= this.drain().finally(() => (this.flight = null));
    return this.flight;
  }

  /** Resolves when nothing is in flight; failures are the caller's of `push`. */
  async flush(): Promise<void> {
    while (this.flight) await this.flight.catch(() => {});
  }

  private async drain(): Promise<void> {
    while (this.pending !== null) {
      const text = this.pending;
      this.pending = null;
      await this.write(text);
    }
  }
}

export class ServerStore implements Store {
  private readonly base: string;
  private readonly queue: WriteQueue;

  constructor(base = "") {
    this.base = base;
    this.queue = new WriteQueue(async (body) => {
      await json(await call(`${base}/api/save`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body,
      }));
    });
  }

  async load(): Promise<SaveData> {
    const res = await call(`${this.base}/api/save`);
    if (res.status === 404) return emptySave();
    return parseSave(await json<unknown>(res));
  }

  /** Throws with the server's `error` code. */
  save(data: SaveData): Promise<void> {
    return this.queue.push(JSON.stringify(data));
  }

  flush(): Promise<void> {
    return this.queue.flush();
  }
}

/** A save file that couldn't be used: moved to `path`, the game starts fresh. */
export interface SaveNotice {
  kind: BackupKind;
  path: string;
}

/** The desktop shell's save file; main only stores text, validation is parseSave here (D-72). */
export class FileStore implements Store {
  notice: SaveNotice | null = null;
  private readonly bridge: DesktopBridge;
  private readonly queue: WriteQueue;

  constructor(bridge: DesktopBridge) {
    this.bridge = bridge;
    this.queue = new WriteQueue(async (text) => {
      try {
        await bridge.writeSave(text);
      } catch (e) {
        const msg = e instanceof Error ? e.message : String(e);
        throw new GameError(msg.includes("bad_save") ? "bad_save" : "save_locked", {}, `can't save: ${msg}`, null);
      }
    });
  }

  /** A broken or newer file goes to the backup first; if that fails, this throws and nothing is written. */
  async load(): Promise<SaveData> {
    const text = await this.bridge.loadSave();
    if (text === null) return emptySave();
    let kind: BackupKind;
    try {
      return parseSave(JSON.parse(text));
    } catch (e) {
      kind = e instanceof SaveNewerError ? "newer" : "corrupt";
    }
    this.notice = { kind, path: await this.bridge.backupSave(kind) };
    return emptySave();
  }

  /** Throws GameError("save_locked"); the caller keeps the save and writes it whole next time. */
  save(data: SaveData): Promise<void> {
    return this.queue.push(JSON.stringify(data));
  }

  flush(): Promise<void> {
    return this.queue.flush();
  }
}
