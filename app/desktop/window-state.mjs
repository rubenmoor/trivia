// Remembered window state (task 1679): fullscreen yes/no and the windowed bounds, `<userData>/window.json`; not the game save.
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import path from "node:path";

export const MIN_SIZE = { width: 1024, height: 600 };
const SHARE = 0.8;
const SAVE_MS = 500;

const int = (v) => Number.isFinite(v) && Math.abs(v) < 1e6;

/** `{ fullscreen, bounds }`; missing or corrupt → first-start defaults (fullscreen, no bounds). */
export function loadWindowState(file) {
  try {
    const v = JSON.parse(readFileSync(file, "utf8"));
    const b = v.bounds;
    const ok = b && [b.x, b.y, b.width, b.height].every(int) && b.width >= MIN_SIZE.width && b.height >= MIN_SIZE.height;
    return { fullscreen: v.fullscreen !== false, bounds: ok ? { x: b.x, y: b.y, width: b.width, height: b.height } : null };
  } catch {
    return { fullscreen: true, bounds: null };
  }
}

/** ~80 % of the display's work area, centred. */
function defaultBounds(display) {
  const a = display.workArea;
  const width = Math.max(MIN_SIZE.width, Math.min(a.width, Math.round(a.width * SHARE)));
  const height = Math.max(MIN_SIZE.height, Math.min(a.height, Math.round(a.height * SHARE)));
  return { x: a.x + Math.round((a.width - width) / 2), y: a.y + Math.round((a.height - height) / 2), width, height };
}

/** Stored bounds when they still meet a display, else the default on the primary one. */
export function startBounds(state, screen) {
  const b = state.bounds;
  if (b && screen.getAllDisplays().some((d) => overlaps(b, d.workArea))) return b;
  return defaultBounds(screen.getPrimaryDisplay());
}

const overlaps = (b, a) => b.x < a.x + a.width && b.x + b.width > a.x && b.y < a.y + a.height && b.y + b.height > a.y;

/** Keeps `state` current from `win` and writes it (debounced; `flush()` at once). Bounds only while windowed. */
export function trackWindow(win, state, file) {
  let timer = null;
  const write = () => {
    try {
      mkdirSync(path.dirname(file), { recursive: true });
      writeFileSync(file, JSON.stringify(state));
    } catch (err) {
      console.error(`trivia: ${file}: ${err.message}`);
    }
  };
  const capture = () => {
    if (win.isDestroyed()) return;
    state.fullscreen = win.isFullScreen();
    if (!state.fullscreen && !win.isMaximized() && !win.isMinimized()) state.bounds = win.getBounds();
  };
  const later = () => {
    clearTimeout(timer);
    timer = setTimeout(() => (capture(), write()), SAVE_MS);
  };
  for (const e of ["resize", "move", "enter-full-screen", "leave-full-screen"]) win.on(e, later);
  return {
    flush() {
      clearTimeout(timer);
      capture();
      write();
    },
  };
}
