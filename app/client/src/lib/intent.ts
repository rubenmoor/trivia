// Keys → intents and what Enter and Space do (plans/14-input.md, "Before the session"; task 2114). Pure, so a test
// can run it; input.svelte.ts routes.
import type { Dir, Intent, Keys } from "./input.svelte.ts";

const ARROWS: Record<string, Dir> = { ArrowUp: "up", ArrowDown: "down", ArrowLeft: "left", ArrowRight: "right" };

export type Key = Pick<KeyboardEvent, "key" | "ctrlKey" | "metaKey" | "altKey"> & Partial<Pick<KeyboardEvent, "code" | "isComposing">>;

/** The key's Latin letter or digit: `e.key`, or `e.code` (`KeyA` → `a`, `Digit1` → `1`) when an IME makes `e.key`
 * `Process` or a non-Latin character (Chinese keyboards, plan 142). */
export function latinKey(e: Key): string {
  const plain = !/^\p{L}$/u.test(e.key) || /^\p{Script=Latin}$/u.test(e.key);
  if (plain && !e.isComposing && e.key !== "Process") return e.key;
  const m = /^(?:Key([A-Z])|Digit([0-9]))$/.exec(e.code ?? "");
  return m ? (m[1] ?? m[2]).toLowerCase() : e.key;
}

/** Key + scope keys → intent; `text`: a text field has focus (letters and Space go into it). Enter is `confirm`
 * everywhere, Space `press` (a scope key for Space wins, e.g. a `timed` claim). */
export function toIntent(e: Key, keys: Keys = {}, text = false, flagKey = ""): Intent | null {
  if (e.key === "Enter") return { type: "confirm" };
  if (e.key === "Escape") return { type: "menu" };
  const dir = ARROWS[e.key];
  if (text) return dir === "up" || dir === "down" ? { type: "navigate", dir } : null;
  if (dir) return { type: "navigate", dir };
  if (e.ctrlKey || e.metaKey || e.altKey) return null;
  if (e.key === " ") return keys[" "] ?? { type: "press" };
  if (e.key === "Backspace") return { type: "back" };
  const k = latinKey(e).toLowerCase();
  if (k in keys) return keys[k];
  if (/^[1-9]$/.test(k)) return { type: "pick", n: Number(k) };
  if (flagKey && k === flagKey.toLowerCase()) return { type: "flag" };
  return null;
}

/** What a `confirm` (Enter, A) or `press` (Space, X) does on the top scope: `primary` clicks its primary button
 * (`yes`; `later`: the scope wants this confirm itself, e.g. an unbound pad's A joins); `focused` presses the ring's control
 * (`focusedPressable`); else the scope's handler gets `confirm` or `press`. Without a primary action Enter and Space are
 * the same (a list screen); with one, Space never reaches the primary action. */
export function activation(type: "confirm" | "press", primary: "yes" | "no" | "later", focusedPressable: boolean): "primary" | "focused" | "confirm" | "press" {
  if (type === "confirm" && primary === "yes") return "primary";
  if (type === "confirm" && primary === "later") return "confirm";
  if (focusedPressable) return "focused";
  return type === "press" && primary !== "no" ? "press" : "confirm";
}
