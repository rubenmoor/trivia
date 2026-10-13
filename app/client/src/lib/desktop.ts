// The Electron shell's bridge (plan 54, SW-2): app/desktop/preload.cjs. Null in the browser.
import type { PadStyle } from "./gamepad.ts";

export interface DesktopBridge {
  readonly desktop: true;
  toggleFullscreen(): Promise<void>;
  quit(): Promise<void>;
  /** The save file's text, null when there is none (plan 55, SW-3). */
  loadSave(): Promise<string | null>;
  /** Rejects with `save_locked` or `bad_save` in the message. */
  writeSave(text: string): Promise<void>;
  /** Moves the save to `save/backup/`; the new path. */
  backupSave(kind: BackupKind): Promise<string>;
  /** Under Steam with no save of this user's: `local/game.json`'s text, else null (plan 87). */
  localSave(): Promise<string | null>;
  /** Copies `local/game.json` into this user's folder (`local/` stays); its text. */
  adoptLocalSave(): Promise<string>;
  readonly steam: SteamBridge;
}

export type BackupKind = "corrupt" | "newer";

/** Steam client calls (plan 85, SW-8); everything null/false when `available` is false. */
export interface SteamBridge {
  readonly available: boolean;
  steamId(): Promise<string | null>;
  /** Steam's API language name (`german`, `latam`, …): the game's in Steam, else the client's. */
  language(): Promise<string | null>;
  overlay: { enabled(): Promise<boolean> };
  /** Steam's floating keyboard at the field (types into the focused input); false outside Big Picture/Deck. */
  showTextInput(field: TextFieldRect, current: string): Promise<boolean>;
  inputTypes(): Promise<PadStyle[] | null>;
  /** Rich presence token (`#Level`) and its values; `""` clears. */
  setPresence(key: string, values: Record<string, string>): Promise<void>;
  /** Achievement API name; true when Steam took it. */
  unlock(id: string): Promise<boolean>;
}

/** Window position in device pixels. */
export interface TextFieldRect {
  x: number;
  y: number;
  width: number;
  height: number;
}

declare global {
  interface Window {
    trivia?: DesktopBridge;
  }
}

export const desktop: DesktopBridge | null = window.trivia ?? null;
export const steam: SteamBridge | null = desktop?.steam ?? null;
