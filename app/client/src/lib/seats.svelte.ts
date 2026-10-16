// The running session's seat binding (plan 161): set by the join screen, kept in sessionStorage by game id for a
// reload, cleared when the session ends. Outside a session `seating.view` is null: no filter, every device acts.
import type { Binding, SessionView } from "./seats.ts";
import type { Game } from "./types.ts";

/** `binding` per seat in join order, null: unbound (a lost pad, a reload without the stored binding, decision 289). */
export const seating = $state({ id: null as number | null, binding: [] as (Binding | null)[], view: null as SessionView | null });

/** The seat an accepted action or click acts for, set while it runs (input.svelte.ts); game actions send it. */
export const acting: { seat: number | null } = { seat: null };

const storeKey = (id: number) => `trivia.seats.${id}`;

function stored(id: number, seats: number): (Binding | null)[] {
  try {
    const list: unknown = JSON.parse(sessionStorage.getItem(storeKey(id)) ?? "null");
    if (Array.isArray(list) && list.length === seats) return list as Binding[];
  } catch {
    /* no storage or a broken entry: rebind */
  }
  return Array(seats).fill(null);
}

/** The join screen's binding as its session starts.
 * @public join screen (plan 162) */
export function bindSession(id: number, binding: readonly Binding[]) {
  try {
    sessionStorage.setItem(storeKey(id), JSON.stringify(binding));
  } catch {
    /* private window: no reload rebind */
  }
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
    seating.binding = stored(game.id, game.session.seats.length);
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
