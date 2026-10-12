// The action layer (plans/14-input.md, IN-2; plan 44): keys (later the gamepad) become actions, and
// the top scope of a stack gets them. The only keydown listener of the client.
import { t } from "./i18n";
import type { JokerName } from "./types";

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
  | { type: "new" };
export type Action = Intent & { device: Device };
/** A scope's extra keys, lower case (e.g. `n` → new on Start). */
export type Keys = Record<string, Intent>;

export type Scope = {
  name: string;
  keys?: Keys;
  /** True if handled; false passes the action down (unless `modal`). */
  handle: (action: Action) => boolean;
  root?: () => HTMLElement | undefined;
  /** Blocks every scope below; always above the non-modal ones. */
  modal?: boolean;
  /** Gets actions while a transition runs (overlay, dialogs). */
  whileBusy?: boolean;
  /** A letter no scope wants focuses this field and goes into it (Player). */
  text?: () => HTMLInputElement | undefined;
  /** Temporary: gets the raw key first while on top (Question, Cambiazo; plan 44 task 2). */
  raw?: (e: KeyboardEvent) => boolean;
};

export const lastDevice = $state({ current: "keyboard" as Device });

const ARROWS: Record<string, Dir> = { ArrowUp: "up", ArrowDown: "down", ArrowLeft: "left", ArrowRight: "right" };
const FLAG_KEY = t("flag.key").toLowerCase();

type Key = Pick<KeyboardEvent, "key" | "ctrlKey" | "metaKey" | "altKey">;

/** Key + scope keys → intent; `text`: a text field has focus. */
export function toIntent(e: Key, keys: Keys = {}, text = false): Intent | null {
  if (e.key === "Enter") return { type: "confirm" };
  if (e.key === "Escape") return { type: "menu" };
  const dir = ARROWS[e.key];
  if (text) return dir === "up" || dir === "down" ? { type: "navigate", dir } : null;
  if (dir) return { type: "navigate", dir };
  if (e.ctrlKey || e.metaKey || e.altKey) return null;
  if (e.key === " ") return { type: "confirm" };
  if (e.key === "Backspace") return { type: "back" };
  const k = e.key.toLowerCase();
  if (k in keys) return keys[k];
  if (/^[1-9]$/.test(k)) return { type: "pick", n: Number(k) };
  if (k === FLAG_KEY) return { type: "flag" };
  return null;
}

const stack: Scope[] = [];

/** Push a scope (in `$effect`); returns its pop. */
export function pushScope(scope: Scope): () => void {
  const at = scope.modal ? stack.length : stack.findIndex((s) => s.modal);
  stack.splice(at < 0 ? stack.length : at, 0, scope);
  return () => {
    const i = stack.indexOf(scope);
    if (i >= 0) stack.splice(i, 1);
  };
}

let busy = () => false;

/** Run an action through the scopes, top first; true if one handled it. Part 5's gamepad calls it too. */
export function dispatch(action: Action): boolean {
  lastDevice.current = action.device;
  const always = action.type === "menu" || action.type === "flag";
  for (let i = stack.length - 1; i >= 0; i--) {
    const s = stack[i];
    if ((always || s.whileBusy || !busy()) && s.handle(action)) return true;
    if (s.modal) return false;
  }
  return false;
}

function textField(el: Element | null) {
  if (el instanceof HTMLTextAreaElement) return true;
  return el instanceof HTMLInputElement && !["range", "checkbox", "radio", "button", "submit"].includes(el.type);
}

function keydown(e: KeyboardEvent, first: () => void) {
  if (e.repeat) return;
  first();
  lastDevice.current = "keyboard";
  const top = stack.at(-1);
  if (top?.raw?.(e)) return;
  const text = textField(document.activeElement);
  const keys = Object.assign({}, ...stack.map((s) => s.keys ?? {}));
  const intent = toIntent(e, keys, text);
  if (intent && dispatch({ ...intent, device: "keyboard" })) return e.preventDefault();
  if (text || busy() || e.key.length !== 1 || !/\p{L}/u.test(e.key) || e.ctrlKey || e.metaKey) return;
  for (let i = stack.length - 1; i >= 0; i--) {
    const field = stack[i].text?.();
    if (field) return field.focus(); // the letter goes into the field
    if (stack[i].modal) return;
  }
}

/** Start listening (Game.svelte, once); `first` runs on every key and click (audio unlock). */
export function listen(opts: { busy: () => boolean; first: () => void }): () => void {
  busy = opts.busy;
  const onkey = (e: KeyboardEvent) => keydown(e, opts.first);
  const onpointer = () => (lastDevice.current = "mouse");
  window.addEventListener("keydown", onkey);
  window.addEventListener("pointerdown", onpointer);
  window.addEventListener("click", opts.first);
  return () => {
    window.removeEventListener("keydown", onkey);
    window.removeEventListener("pointerdown", onpointer);
    window.removeEventListener("click", opts.first);
  };
}
