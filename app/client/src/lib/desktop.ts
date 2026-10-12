// The Electron shell's bridge (plan 54, SW-2): app/desktop/preload.cjs. Null in the browser.
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
}

export type BackupKind = "corrupt" | "newer";

declare global {
  interface Window {
    trivia?: DesktopBridge;
  }
}

export const desktop: DesktopBridge | null = window.trivia ?? null;
