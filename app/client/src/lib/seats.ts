// Per-player controls (plans/14-input.md section 3, plan 161): which seat of a local multiplayer session a device
// acts for and whether it may act now. Pure, so a script can feed it fake pads; the state is seats.svelte.ts.
import type { Keys } from "./input.svelte.ts";
import type { Game } from "./types.ts";

/** Where an action came from: a pad by `Gamepad.index`, the keyboard, the mouse. */
export type Source = { pad: number } | "keyboard" | "mouse";
/** A seat's controls, join order: a pad; keyboard and mouse together; a keyboard-only `timed` player's claim key
 * (lower case); keyboard-only round-robin: no device, keyboard and mouse act for the turn (decision 273). */
export type Binding = { pad: number } | "kbm" | { key: string } | "shared";
export type SessionView = NonNullable<Game["session"]>;

const padOf = (b: Binding | null): number | null => (b !== null && typeof b === "object" && "pad" in b ? b.pad : null);
const keyOf = (b: Binding | null): string | null => (b !== null && typeof b === "object" && "key" in b ? b.key : null);

function find(binding: readonly (Binding | null)[], hit: (b: Binding | null) => boolean): number | null {
  const i = binding.findIndex(hit);
  return i < 0 ? null : i;
}

/** The seat `source` acts for, or null (a pad bound to no seat). Keyboard and mouse: the `kbm` seat, else (keyboard
 * only) a claim's key seat, the claimer (`timed`) or the turn seat (round-robin). */
export function seatOf(source: Source, intent: { type: string; key?: string } | undefined, view: SessionView,
  binding: readonly (Binding | null)[]): number | null {
  if (typeof source === "object") return find(binding, (b) => padOf(b) === source.pad);
  const kbm = find(binding, (b) => b === "kbm");
  if (kbm !== null) return kbm;
  if (intent?.type === "claim" && intent.key) return find(binding, (b) => keyOf(b) === intent.key!.toLowerCase());
  return view.timed ? (view.timed.claim?.seat ?? null) : view.turn;
}

/** May `seat` act now: round-robin the turn seat; `timed` any seat still in, once claimed only the claimer. */
export function may(seat: number | null, view: SessionView): boolean {
  if (seat === null || view.seats[seat]?.status !== "playing") return false;
  if (!view.timed) return seat === view.turn;
  return !view.timed.claim || view.timed.claim.seat === seat;
}

/** The pad of a confirm from a pad bound to no seat (join, a lost seat's rebind), else null.
 * @public join screen (plan 162), lost pads (task 1434) */
export function unboundPad(source: Source, intent: { type: string }, binding: readonly (Binding | null)[]): number | null {
  if (typeof source !== "object" || intent.type !== "confirm") return null;
  return binding.some((b) => padOf(b) === source.pad) ? null : source.pad;
}

/** A pad joins as a new seat; a lone keyboard seat becomes the `kbm` seat; null: already seated, or two or more
 * keyboard seats (decisions 274, 292).
 * @public join screen (plan 162) */
export function joinPad(binding: readonly Binding[], pad: number): Binding[] | null {
  if (binding.some((b) => padOf(b) === pad)) return null;
  if (binding.filter((b) => padOf(b) === null).length > 1) return null;
  return [...binding.map((b): Binding => (padOf(b) === null ? "kbm" : b)), { pad }];
}

/** The keyboard joins: with a pad seated the one `kbm` seat; without, a key seat (`timed`: its picked key) or a
 * shared one (round-robin, `key` null); null: keyboard and mouse already one seat (decisions 273, 274, 292).
 * @public join screen (plan 162) */
export function joinKeyboard(binding: readonly Binding[], key: string | null): Binding[] | null {
  if (binding.includes("kbm")) return null;
  if (binding.some((b) => padOf(b) !== null)) return [...binding, "kbm"];
  return [...binding, key === null ? "shared" : { key: key.toLowerCase() }];
}

/** The timed question scope's claim keys: Space for the `kbm` seat, each key seat's picked key (decision 290). */
export function claimKeys(binding: readonly (Binding | null)[]): Keys {
  const keys: Keys = binding.includes("kbm") ? { " ": { type: "claim" } } : {};
  for (const b of binding) {
    const key = keyOf(b);
    if (key) keys[key] = { type: "claim", key };
  }
  return keys;
}
