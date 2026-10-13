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
  readonly steam: SteamBridge;
  /** Set by the dev server's page shim (plan 99): its save dir is the dev switch. */
  readonly devServer?: true;
}

export type BackupKind = "corrupt" | "newer";

/** Steam client calls (plan 85, SW-8); everything null/false when `available` is false. */
export interface SteamBridge {
  readonly available: boolean;
  /** Valid Steam user (non-zero SteamID) or the dev switch `TRIVIA_DEV_STEAM_USER` (decision 111). */
  readonly user: boolean;
  /** Dev switch on and no real Steam user: dev tools such as «Ir a pregunta…». */
  readonly dev: boolean;
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
/** Saves and flags allowed (decision 111); the only check plan 87 and the flag UI read. */
export const validUser: boolean = steam?.user === true || desktop?.devServer === true;
/** Dev switch or dev server (plan 85): «Ir a pregunta…»; a real Steam user is not dev mode. */
export const devMode: boolean = steam?.dev === true || desktop?.devServer === true;
