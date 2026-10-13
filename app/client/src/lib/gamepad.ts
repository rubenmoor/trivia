// The gamepad core (plans/14-input.md, IN-4; plan 45): a standard pad's buttons and left stick
// become intents. Pure, so a script can feed it fake pads; the loop is gamepad.svelte.ts.
import type { Dir, Intent } from "./input.svelte";

export type Pad = { buttons: readonly boolean[]; axes: readonly number[] };
/** Buttons down last frame; the stick's direction, or "held" until it is let go. */
export type PadState = { buttons: readonly boolean[]; stick: Dir | "held" | null };
export type PadStyle = "xbox" | "playstation";

/** Standard mapping: A, B, Y, LB/RB, View, Start, D-pad; X and triggers only per scope (Scope.pad). */
export const BUTTONS: Record<number, Intent> = {
  0: { type: "confirm" },
  1: { type: "back" },
  3: { type: "replay" },
  4: { type: "joker-focus", step: -1 },
  5: { type: "joker-focus", step: 1 },
  8: { type: "flag" },
  9: { type: "menu" },
  12: { type: "navigate", dir: "up" },
  13: { type: "navigate", dir: "down" },
  14: { type: "navigate", dir: "left" },
  15: { type: "navigate", dir: "right" },
};
const ON = 0.5;
const OFF = 0.3;

export const FRESH: PadState = { buttons: [], stick: null };
/** Everything counts as down: nothing fires until released (focus return). */
export const HELD: PadState = { buttons: Array(32).fill(true), stick: "held" };

/** The dominant axis past the dead zone, or null. */
function stickDir(x: number, y: number): Dir | null {
  if (Math.max(Math.abs(x), Math.abs(y)) <= ON) return null;
  if (Math.abs(x) >= Math.abs(y)) return x > 0 ? "right" : "left";
  return y > 0 ? "down" : "up";
}

function along(d: Dir, x: number, y: number) {
  return d === "right" ? x : d === "left" ? -x : d === "down" ? y : -y;
}

/** One frame: press edges and stick moves → intents; no repeat while held. */
export function step(prev: PadState, pad: Pad, map = BUTTONS): { next: PadState; actions: Intent[] } {
  const actions: Intent[] = [];
  pad.buttons.forEach((down, i) => {
    if (down && !prev.buttons[i] && map[i]) actions.push(map[i]);
  });
  const [x = 0, y = 0] = pad.axes;
  let stick = prev.stick;
  if (stick === "held" ? Math.max(Math.abs(x), Math.abs(y)) < OFF : stick && along(stick, x, y) < OFF) stick = null;
  if (stick === null) {
    stick = stickDir(x, y);
    if (stick) actions.push({ type: "navigate", dir: stick });
  }
  return { next: { buttons: [...pad.buttons], stick }, actions };
}

const same = (a: Intent, b: Intent) =>
  Object.keys(a).length === Object.keys(b).length && Object.entries(a).every(([k, v]) => b[k as keyof Intent] === v);

/** The button bound to `intent` in `map` (lowest index), or null (IN-5). */
export function padButton(intent: Intent, map: Record<number, Intent>): number | null {
  const hit = Object.entries(map).find(([, i]) => same(i, intent));
  return hit ? Number(hit[0]) : null;
}

/** Glyph set from `Gamepad.id`; under Steam Input every pad is Xbox, so Steam's types win (steamStyle). */
export function styleOf(id: string): PadStyle {
  return /054c|playstation|dualshock|dualsense|wireless controller/i.test(id) ? "playstation" : "xbox";
}

/** Steam's pad types → one set: all PlayStation → playstation, mixed → xbox (per player: IN-6); none → null. */
export function steamStyle(types: readonly PadStyle[] | null): PadStyle | null {
  if (!types?.length) return null;
  return types.every((t) => t === "playstation") ? "playstation" : "xbox";
}
