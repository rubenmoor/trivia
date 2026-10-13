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
  /** Missing in the browser game and the dev server's shim (plan 106). */
  readonly telemetry?: TelemetryBridge;
  /** Missing in the dev server's shim (plan 93). */
  readonly report?: ReportBridge;
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

/** Opt-in telemetry store in the shell (plan 106); no-ops without a valid user. */
export interface TelemetryBridge {
  /** Ask when `available && consent === null`. */
  state(): Promise<TelemetryState>;
  /** Yes: install id, session starts; no: id and every session file deleted. */
  setConsent(yes: boolean): Promise<TelemetryState>;
  /** This run's current session buffer; null without a yes. */
  load(): Promise<TelemetryBuffer | null>;
  /** Replaces this run's games (index parallel); ignored without a yes; rejects `bad_telemetry`. */
  record(buffer: TelemetryBuffer): Promise<void>;
}

export interface TelemetryState {
  available: boolean;
  consent: boolean | null;
}

/** `games`: plan 105's contract games; `index[i]` is the page's bookkeeping for `games[i]`, never sent. */
export interface TelemetryBuffer {
  games: object[];
  index: { key: string; from: number }[];
}

/** Question reports (plan 93): one POST from the shell's main process per `send`, never on its own. */
export interface ReportBridge {
  /** Report URL configured and a valid Steam user (or the dev switch). */
  available(): Promise<boolean>;
  /** Plan 103's limits; rejects `bad_report` for a field outside them. */
  send(fields: ReportFields): Promise<ReportResult>;
}

/** Plan 103's `POST /reports` body minus the ticket; `pool` null for a pool without hash. */
export interface ReportFields {
  question: string;
  /** Question language (flag `locale`), not the UI's. */
  lang: string;
  text: string;
  note?: string;
  version: string;
  pool: string | null;
}

/** `status` 0: no response (`no_connection`, `timeout`, `no_ticket`, `unavailable`, `too_large`); else plan 103's code. */
export type ReportResult =
  | { ok: true; id: number }
  | { ok: false; status: number; error: string; retryAfter?: number };

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
export const telemetry: TelemetryBridge | null = desktop?.telemetry ?? null;
export const report: ReportBridge | null = desktop?.report ?? null;
/** Saves and flags allowed (decision 111); the only check plan 87 and the flag UI read. */
export const validUser: boolean = steam?.user === true || desktop?.devServer === true;
/** Dev switch or dev server (plan 85): «Ir a pregunta…»; a real Steam user is not dev mode. */
export const devMode: boolean = steam?.dev === true || desktop?.devServer === true;
