// Where the save lives (plan 49, PORT-4). ServerStore, FileStore: lib/store.ts.
import type { SaveData } from "./state.ts";

export interface Store {
  /** The stored save, emptySave() when there is none. */
  load(): Promise<SaveData>;
  /** Replace the stored save whole. */
  save(data: SaveData): Promise<void>;
}
