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
  /** Missing in the dev server's shim. */
  readonly mods?: ModsBridge;
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

/** Mods in the shell (plan 114); changes apply on the next start. */
export interface ModsBridge {
  /** Fresh discovery per call: new subscriptions and finished downloads show up. */
  list(): Promise<ModList>;
  /** Load order, top first; ids left out keep their order after these. Rejects `bad_mods`. */
  set(order: { id: string; on: boolean }[]): Promise<ModList>;
}

export interface ModList {
  mods: ModEntry[];
  /** `--no-mods`: nothing loaded this run. */
  noMods: boolean;
  validUser: boolean;
}

/** One row; `id`, `name`, `version`, `description` null when unknown (downloading, no or bad `mod.json`). */
export interface ModEntry {
  id: string | null;
  name: string | null;
  version: string | null;
  description: string | null;
  source: "local" | "workshop";
  publishedFileId: string | null;
  kind: string[];
  languages: string[];
  /** Setting in `mods.json`. */
  on: boolean;
  /** In this run's overlay; differs from `on` until restart. */
  active: boolean;
  /** Load order index (0 = top, wins); null outside the order. */
  position: number | null;
  /** loaded, off, no_user, invalid, downloading, disabled. */
  state: string;
  /** Codes: needs_update, workshop_id_mismatch, game_version, unknown_key, unknown_language. */
  warnings: string[];
  error: { code: string; field?: string } | null;
  /** Folder basename, for the dev log. */
  dir: string | null;
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
export const mods: ModsBridge | null = desktop?.mods ?? null;
/** Saves and flags allowed (decision 111); the only check plan 87 and the flag UI read. */
export const validUser: boolean = steam?.user === true || desktop?.devServer === true;
/** Dev switch or dev server (plan 85): «Ir a pregunta…»; a real Steam user is not dev mode. */
export const devMode: boolean = steam?.dev === true || desktop?.devServer === true;
