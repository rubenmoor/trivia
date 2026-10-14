// Where the save lives: the game server (GET/PUT /api/save, plan 49), the desktop's file (plan 55) or, without a
// Steam user, memory only (plan 87).
import { parseSave, SaveNewerError } from "../engine/save.ts";
import { emptySave, type SaveData } from "../engine/state.ts";
import type { Store } from "../engine/store.ts";
import { call, GameError, json, messageOf } from "./http.ts";
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
    this.flight ??= this.drain();
    return this.flight;
  }

  /** Resolves when nothing is in flight; failures are the caller's of `push`. */
  async flush(): Promise<void> {
    while (this.flight) await this.flight.catch(() => {});
  }

  /** Clears `flight` before it settles: a push in between starts a new drain, not a finished one. */
  private async drain(): Promise<void> {
    try {
      while (this.pending !== null) {
        const text = this.pending;
        this.pending = null;
        await this.write(text);
      }
    } finally {
      this.flight = null;
    }
  }
}

/** A save file that couldn't be used: moved to `path`, the game starts fresh; `unsaved`: memory-only save. */
export type SaveNotice = { kind: BackupKind; path: string } | { kind: "unsaved" };

/** Text in, parseSave here; a corrupt or newer file goes to the backup with a notice (D-72, decision 98). */
abstract class TextStore implements Store {
  notice: SaveNotice | null = null;
  protected abstract readonly queue: WriteQueue;
  /** The stored text, null when there is none. */
  protected abstract read(): Promise<string | null>;
  /** Moves the file away; the backup's path. */
  protected abstract backup(kind: BackupKind): Promise<string>;

  /** If the backup fails, this throws and nothing is written. */
  async load(): Promise<SaveData> {
    const text = await this.read();
    if (text === null) return emptySave();
    let kind: BackupKind;
    try {
      return parseSave(JSON.parse(text));
    } catch (e) {
      kind = e instanceof SaveNewerError ? "newer" : "corrupt";
    }
    this.notice = { kind, path: await this.backup(kind) };
    return emptySave();
  }

  save(data: SaveData): Promise<void> {
    return this.queue.push(JSON.stringify(data));
  }

  flush(): Promise<void> {
    return this.queue.flush();
  }
}

/** The game server's `state/game.json`; writes throw with the server's `error` code. */
export class ServerStore extends TextStore {
  protected readonly queue = new WriteQueue(async (body) => {
    await json(await call("/api/save", { method: "PUT", headers: { "Content-Type": "application/json" }, body }));
  });

  protected async read(): Promise<string | null> {
    const res = await call("/api/save");
    if (res.status === 404) return null;
    if (!res.ok) await json(res); // throws
    return res.text();
  }

  protected async backup(kind: BackupKind): Promise<string> {
    const res = await call(`/api/save/backup?kind=${kind}`, { method: "POST" });
    return (await json<{ path: string }>(res)).path;
  }
}

/** The desktop shell's save file; main only stores text (D-72). Writes throw GameError("save_locked"); the
 * caller keeps the save and writes it whole next time. */
export class FileStore extends TextStore {
  protected readonly queue: WriteQueue;
  private readonly bridge: DesktopBridge;

  constructor(bridge: DesktopBridge) {
    super();
    this.bridge = bridge;
    this.queue = new WriteQueue(async (text) => {
      try {
        await bridge.writeSave(text);
      } catch (e) {
        const msg = messageOf(e);
        throw new GameError(msg.includes("bad_save") ? "bad_save" : "save_locked", {}, `can't save: ${msg}`, null);
      }
    });
  }

  protected read(): Promise<string | null> {
    return this.bridge.loadSave();
  }

  protected backup(kind: BackupKind): Promise<string> {
    return this.bridge.backupSave(kind);
  }
}

/** No valid Steam user (decision 111): starts empty, keeps the save in memory, nothing on disk. */
export class MemoryStore extends TextStore {
  override notice: SaveNotice | null = { kind: "unsaved" };
  private text: string | null = null;
  protected readonly queue = new WriteQueue(async (text) => {
    this.text = text;
  });

  protected read(): Promise<string | null> {
    return Promise.resolve(this.text);
  }

  protected backup(): Promise<string> {
    return Promise.resolve("");
  }
}
