// The running session's seat binding (plan 161): set by the join screen, kept in sessionStorage by game id for a
// reload, cleared when the session ends; without it (a restart) keyboard seats come back from the save's device
// kinds, pad seats wait for a pad (plan 172). Outside a session `seating.view` is null: no filter, every device acts.
import { CLAIM_PAD } from "./gamepad.ts";
import type { Keys } from "./input.svelte.ts";
import { claimKeys, padSeat, restoredBinding, type Binding, type SessionView } from "./seats.ts";
import type { Game } from "./types.ts";

/** `binding` per seat in join order, null: unbound (a lost pad, a restart's pad seat, decision 289). */
export const seating = $state({ id: null as number | null, binding: [] as (Binding | null)[], view: null as SessionView | null });

/** The seat an accepted action or click acts for, set while it runs (input.svelte.ts); game actions send it. */
export const acting: { seat: number | null } = { seat: null };

const storeKey = (id: number) => `trivia.seats.${id}`;

function store(id: number, binding: readonly (Binding | null)[]) {
  try {
    sessionStorage.setItem(storeKey(id), JSON.stringify(binding));
  } catch {
    /* private window: no reload rebind */
  }
}

function stored(id: number, view: SessionView): (Binding | null)[] {
  try {
    const list: unknown = JSON.parse(sessionStorage.getItem(storeKey(id)) ?? "null");
    if (Array.isArray(list) && list.length === view.seats.length) return list as Binding[];
  } catch {
    /* no storage or a broken entry: rebind */
  }
  return restoredBinding(view);
}

/** The Join screen's binding as its session starts (set by Game.svelte, plan 162). */
export function bindSession(id: number, binding: readonly Binding[]) {
  store(id, binding);
  seating.id = id;
  seating.binding = [...binding];
}

/** Game.svelte's game on every change: a running session turns the filter on, any other game ends it. */
export function watchGame(game: Game | null) {
  if (!game) return void (seating.view = null);
  if (!game.session || game.result !== null) return endSession();
  if (seating.id !== game.id) {
    if (seating.id !== null) endSession();
    seating.id = game.id;
    seating.binding = stored(game.id, game.session);
  }
  seating.view = game.session;
}

function endSession() {
  if (seating.id !== null) {
    try {
      sessionStorage.removeItem(storeKey(seating.id));
    } catch {
      /* nothing stored */
    }
  }
  Object.assign(seating, { id: null, binding: [], view: null });
}

/** The default seat of a game action that runs outside an accepted input (after an await): the turn or the claimer. */
export function actingSeat(): number | null {
  const view = seating.view;
  if (!view) return null;
  return acting.seat ?? (view.timed ? (view.timed.claim?.seat ?? null) : view.turn);
}

/** The `keys` and `pad` of the timed question scope (plan 164): the claim inputs of the session's seats; a claim
 * click is any `[data-claim]` control's handler, the mouse filter lets only the `kbm` seat through.
 * @public timed screens (plan 164) */
export function claimInput(): { keys: Keys; pad: typeof CLAIM_PAD } {
  return { keys: claimKeys(seating.binding), pad: CLAIM_PAD };
}

/** A pad is gone: its seat is unbound until a pad takes it (decision 289). */
export function unbindPad(index: number) {
  if (seating.id === null) return;
  seating.binding = seating.binding.map((b) => (b !== null && typeof b === "object" && "pad" in b && b.pad === index ? null : b));
  store(seating.id, seating.binding);
}

/** The pad seat that needs a pad now: round-robin the turn seat; `timed` the first one still in, at once (decision
 * 289). A seat that is out never asks; a keyboard seat is never lost. */
export function lostSeat(): number | null {
  const view = seating.view;
  if (!view || seating.id === null) return null;
  const lost = (i: number) => seating.binding[i] === null && view.seats[i]?.status === "playing" && padSeat(view, i);
  if (!view.timed) return lost(view.turn) ? view.turn : null;
  const i = view.seats.findIndex((_, at) => lost(at));
  return i < 0 ? null : i;
}

/** A pad takes `seat`. */
export function rebindSeat(seat: number, pad: number) {
  if (seating.id === null) return;
  seating.binding = seating.binding.map((b, i) => (i === seat ? { pad } : b));
  store(seating.id, seating.binding);
}
