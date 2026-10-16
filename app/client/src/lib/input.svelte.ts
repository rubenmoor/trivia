// The action layer (plans/14-input.md, IN-2; plan 44): keys and pad buttons (gamepad.svelte.ts) become
// actions, and the top scope of a stack gets them. The only keydown listener of the client. In a local multiplayer
// session only the seat that may act gets through (plan 161, seats.ts).
import { untrack } from "svelte";
import { forget, keyPressed, navigate, opener, press, show, track } from "./focus.ts";
import { t } from "./i18n.ts";
import { may, seatOf, type Source } from "./seats.ts";
import { acting, seating } from "./seats.svelte.ts";
import type { JokerName } from "./types.ts";

export type Device = "keyboard" | "mouse" | "gamepad";
export type Dir = "up" | "down" | "left" | "right";
export type Intent =
  | { type: "confirm" }
  | { type: "back" }
  | { type: "menu" }
  | { type: "pick"; n: number }
  | { type: "joker"; name: JokerName }
  | { type: "navigate"; dir: Dir }
  | { type: "replay" }
  | { type: "flag" }
  | { type: "new" }
  /** Start's language button (plan 126). */
  | { type: "language" }
  | { type: "submit" }
  | { type: "joker-focus"; step: 1 | -1 }
  /** The one hold (plan 113): down on press, up on release. */
  | { type: "peek"; down: boolean }
  /** A screen's own letter key (a bundle on Choice); `key` lower case. */
  | { type: "letter"; key: string }
  /** Timed (plan 161): claim the question; `key`: a keyboard-only player's picked key, lower case. */
  | { type: "claim"; key?: string };
export type Action = Intent & { device: Device; source: Source };
/** A scope's extra keys, lower case (e.g. `n` → new on Start). */
export type Keys = Record<string, Intent>;

export type Scope = {
  name: string;
  keys?: Keys;
  /** True if handled; false passes the action down (unless `modal`). */
  handle: (action: Action) => boolean;
  /** Where arrows move focus and confirm presses the focused control; a scope without one keeps confirm. */
  root?: () => HTMLElement | undefined;
  /** False: confirm on this shown control goes to `handle` instead of clicking it (a locked answer submits). */
  pressable?: (el: HTMLElement) => boolean;
  /** Keeps its focus memory when pushed again (Start); others start fresh (new content). */
  keep?: boolean;
  /** Blocks every scope below; always above the non-modal ones. */
  modal?: boolean;
  /** Gets actions while a transition runs (overlay, dialogs). */
  whileBusy?: boolean;
  /** Pad buttons (standard index) that differ here, e.g. face buttons pick answers (Question). */
  pad?: () => Record<number, Intent>;
  /** A letter no scope wants focuses this field and goes into it (Player). */
  text?: () => HTMLInputElement | undefined;
  /** In a session every device drives it and what opens above it (Esc menu, flag dialog, results; decision 288). */
  shared?: boolean;
};

export const lastDevice = $state({ current: "keyboard" as Device });
/** Bumped when scopes or focus change: prompts re-read the pad map (IN-5). */
export const scopes = $state({ version: 0 });
const bump = () => untrack(() => scopes.version++);

const ARROWS: Record<string, Dir> = { ArrowUp: "up", ArrowDown: "down", ArrowLeft: "left", ArrowRight: "right" };

type Key = Pick<KeyboardEvent, "key" | "ctrlKey" | "metaKey" | "altKey">;

/** Key + scope keys → intent; `text`: a text field has focus. */
function toIntent(e: Key, keys: Keys = {}, text = false): Intent | null {
  if (e.key === "Enter") return { type: "confirm" };
  if (e.key === "Escape") return { type: "menu" };
  const dir = ARROWS[e.key];
  if (text) return dir === "up" || dir === "down" ? { type: "navigate", dir } : null;
  if (dir) return { type: "navigate", dir };
  if (e.ctrlKey || e.metaKey || e.altKey) return null;
  if (e.key === " ") return keys[" "] ?? { type: "confirm" };
  if (e.key === "Backspace") return { type: "back" };
  const k = e.key.toLowerCase();
  if (k in keys) return keys[k];
  if (/^[1-9]$/.test(k)) return { type: "pick", n: Number(k) };
  if (k === t("flag.key").toLowerCase()) return { type: "flag" };
  return null;
}

/** On-screen key labels (IN-5): the one copy, read by Prompt.svelte. A function: catalogs load after import. */
const keyLabels = (): Partial<Record<Intent["type"], string>> => ({
  confirm: "Enter",
  submit: "Enter",
  back: "⌫",
  menu: "Esc",
  replay: t("screen.question.replayKey"),
  new: t("screen.start.newKey"),
  language: t("screen.start.languageKey"),
  flag: t("flag.key"),
  peek: t("screen.question.peekKey"),
});
const ARROW_LABELS: Record<Dir, string> = { up: "↑", down: "↓", left: "←", right: "→" };

/** The key shown for an intent, or null (jokers by letter, joker-focus has no key). */
export function keyLabel(i: Intent): string | null {
  if (i.type === "pick") return String(i.n);
  if (i.type === "navigate") return ARROW_LABELS[i.dir];
  if (i.type === "letter") return i.key.toUpperCase();
  if (i.type === "claim") return i.key?.toUpperCase() ?? t("picker.space");
  return keyLabels()[i.type] ?? null;
}

const stack: Scope[] = [];

/** Push a scope (in `$effect`); returns its pop. */
export function pushScope(scope: Scope): () => void {
  if (!scope.keep) forget(scope.name);
  if (scope.modal) release();
  const restore = scope.modal ? opener() : null; // dialogs give focus back to their opener
  const at = scope.modal ? stack.length : stack.findIndex((s) => s.modal);
  stack.splice(at < 0 ? stack.length : at, 0, scope);
  bump();
  return () => {
    const i = stack.indexOf(scope);
    if (i >= 0) stack.splice(i, 1);
    bump();
    restore?.();
  };
}

/** The scope whose root arrows move in: the top one with a root, never below a modal one. */
function rooted(): [Scope, HTMLElement] | null {
  for (let i = stack.length - 1; i >= 0; i--) {
    const root = stack[i].root?.();
    if (root) return [stack[i], root];
    if (stack[i].modal) return null;
  }
  return null;
}

/** Focus a control: with the ring, unless the mouse was last (a dialog's first button). */
export function focusControl(el: HTMLElement | null | undefined) {
  if (!el) return;
  if (lastDevice.current === "mouse") el.focus();
  else show(el);
}

/** The seat `source` acts for and whether it may act now (plan 161); outside a session every device acts, for no seat.
 * `menu` and shared scopes take everyone. */
export function gate(source: Source, intent?: Intent): { ok: boolean; seat: number | null } {
  const view = seating.view;
  if (!view) return { ok: true, seat: null };
  const seat = seatOf(source, intent, view, seating.binding);
  return { ok: intent?.type === "menu" || stack.some((s) => s.shared) || may(seat, view), seat };
}

let busy = () => false;
/** A peek is held; its key, if a key started it; the source that holds it. */
let holding = false;
let holdKey: string | null = null;
let holdSource: Source = "keyboard";

/** Run an action through the scopes, top first; true if one handled it. The gamepad loop calls it too. A dropped
 * action (another seat's turn) does nothing. */
export function dispatch(action: Action): boolean {
  const letGo = action.type === "peek" && !action.down;
  const { ok, seat } = gate(action.source, action);
  if (!ok && !letGo) return false;
  const was = acting.seat;
  acting.seat = seat;
  try {
    if (action.type !== "peek") return route(action);
    if (letGo && !holding) return false;
    const done = route(action);
    holding = action.down && done;
    if (holding) holdSource = action.source;
    return done;
  } finally {
    acting.seat = was;
  }
}

/** Ends a held peek (blur, hidden page, pad gone, a modal scope). */
export function release() {
  holdKey = null;
  if (holding) dispatch({ type: "peek", down: false, device: lastDevice.current, source: holdSource });
}

function route(action: Action): boolean {
  lastDevice.current = action.device;
  const always = action.type === "menu" || action.type === "flag" || (action.type === "peek" && !action.down);
  const top = stack.at(-1);
  const root = top?.root?.();
  if (action.type === "confirm" && root && !busy() && press(root, top?.pressable)) return true;
  for (let i = stack.length - 1; i >= 0; i--) {
    const s = stack[i];
    if ((always || s.whileBusy || !busy()) && s.handle(action)) return true;
    if (s.modal) break;
  }
  if (action.type !== "navigate" || busy()) return false;
  const at = rooted();
  return at ? navigate(action.dir, at[0].name, at[1]) : false;
}

/** The pad mapping: `base` with the scopes' overrides, top wins, none from below a modal scope. */
export function padMap(base: Record<number, Intent>): Record<number, Intent> {
  let from = stack.length - 1;
  while (from > 0 && !stack[from].modal) from--;
  return Object.assign({}, base, ...stack.slice(from).map((s) => s.pad?.() ?? {}));
}

function textField(el: Element | null) {
  if (el instanceof HTMLTextAreaElement) return true;
  return el instanceof HTMLInputElement && !["range", "checkbox", "radio", "button", "submit"].includes(el.type);
}

function keydown(e: KeyboardEvent, first: () => void) {
  keyPressed(e.key);
  if (e.repeat) return;
  first();
  const text = textField(document.activeElement);
  const keys = Object.assign({}, ...stack.map((s) => s.keys ?? {}));
  const intent = toIntent(e, keys, text);
  if (!gate("keyboard", intent ?? undefined).ok) return e.preventDefault(); // no Tab focus move either
  lastDevice.current = "keyboard";
  resetTravel();
  if (intent && dispatch({ ...intent, device: "keyboard", source: "keyboard" })) {
    if (intent.type === "peek") holdKey = e.key.toLowerCase();
    return e.preventDefault();
  }
  if (text || busy() || e.key.length !== 1 || !/\p{L}/u.test(e.key) || e.ctrlKey || e.metaKey) return;
  for (let i = stack.length - 1; i >= 0; i--) {
    const field = stack[i].text?.();
    if (field) return field.focus(); // the letter goes into the field
    if (stack[i].modal) return;
  }
}

/** Mouse travel (px) after the last key or pad input that flips the prompts back to keys (plan 156). */
const MOVE_PX = 4;
let travel = 0;
let seen: [number, number] | null = null;

/** A key or pad input restarts the mouse's travel count. */
export function resetTravel() {
  travel = 0;
}

function pointermove(e: PointerEvent) {
  if (e.pointerType !== "mouse") return;
  const from = seen;
  seen = [e.screenX, e.screenY];
  if (!from || lastDevice.current === "mouse" || !gate("mouse").ok) return;
  travel += Math.hypot(seen[0] - from[0], seen[1] - from[1]); // 0 for a synthetic move
  if (travel >= MOVE_PX) lastDevice.current = "mouse";
}

/** Capture phase, before any handler: in a session a click of a seat that may not act is dropped; an accepted one
 * runs as its seat. `[data-shared]` controls (the menu button) and `el.click()` from a pad's confirm always pass. */
function gateClick(e: Event) {
  if (!e.isTrusted || (e.target instanceof Element && e.target.closest("[data-shared]"))) return;
  const { ok, seat } = gate("mouse");
  if (!ok) {
    e.preventDefault();
    e.stopImmediatePropagation();
  } else if (e.type === "click" && seat !== null) {
    acting.seat = seat;
    setTimeout(() => (acting.seat = null)); // after every handler of this click
  }
}

/** Start listening (Game.svelte, once); `first` runs on every key and click (audio unlock). */
export function listen(opts: { busy: () => boolean; first: () => void }): () => void {
  busy = opts.busy;
  const onkey = (e: KeyboardEvent) => keydown(e, opts.first);
  const onpointer = () => gate("mouse").ok && (lastDevice.current = "mouse");
  const onkeyup = (e: KeyboardEvent) => e.key.toLowerCase() === holdKey && release();
  const onhidden = () => document.hidden && release();
  const untrackFocus = track();
  window.addEventListener("pointerdown", gateClick, true);
  window.addEventListener("click", gateClick, true);
  window.addEventListener("keydown", onkey);
  window.addEventListener("keyup", onkeyup);
  window.addEventListener("blur", release);
  document.addEventListener("visibilitychange", onhidden);
  window.addEventListener("pointerdown", onpointer);
  window.addEventListener("pointermove", pointermove);
  window.addEventListener("click", opts.first);
  window.addEventListener("focusin", bump);
  window.addEventListener("focusout", bump);
  return () => {
    window.removeEventListener("pointerdown", gateClick, true);
    window.removeEventListener("click", gateClick, true);
    window.removeEventListener("keydown", onkey);
    window.removeEventListener("keyup", onkeyup);
    window.removeEventListener("blur", release);
    document.removeEventListener("visibilitychange", onhidden);
    window.removeEventListener("pointerdown", onpointer);
    window.removeEventListener("pointermove", pointermove);
    window.removeEventListener("click", opts.first);
    window.removeEventListener("focusin", bump);
    window.removeEventListener("focusout", bump);
    untrackFocus();
  };
}
