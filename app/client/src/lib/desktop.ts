// The Electron shell's bridge (plan 54, SW-2): app/desktop/preload.cjs. Null in the browser.
export interface DesktopBridge {
  readonly desktop: true;
  toggleFullscreen(): Promise<void>;
  quit(): Promise<void>;
}

declare global {
  interface Window {
    trivia?: DesktopBridge;
  }
}

export const desktop: DesktopBridge | null = window.trivia ?? null;
