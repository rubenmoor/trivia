// Where the save lives (plan 49, PORT-4). ServerStore: lib/store.ts.
import { emptySave, type SaveData } from "./state.ts";

export interface Store {
  /** The stored save, emptySave() when there is none. */
  load(): Promise<SaveData>;
  /** Replace the stored save whole. */
  save(data: SaveData): Promise<void>;
}

/** In memory, for tests; copies in and out, so callers can't touch the stored document. */
export class MemoryStore implements Store {
  private data: SaveData | null;

  constructor(data: SaveData | null = null) {
    this.data = data && structuredClone(data);
  }

  async load(): Promise<SaveData> {
    return structuredClone(this.data ?? emptySave());
  }

  async save(data: SaveData): Promise<void> {
    this.data = structuredClone(data);
  }
}
