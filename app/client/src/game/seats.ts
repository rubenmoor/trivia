// A local multiplayer session's seats on screen (plan 162): the Join screen's draft and the seat colours, which the
// round-robin and timed screens show too (decision 279). Bindings and the input filter: lib/seats.ts.
import type { Binding } from "../lib/seats.ts";

/** A seat before the session starts: `shared` in a keyboard-only `timed` session is a key seat without its key yet. */
export interface SeatDraft {
  binding: Binding;
  name: string | null;
  /** rr-competitive's own age group (decision 291). */
  group: string;
}

/** By join order, repeating past the end; each ≥ 8:1 on `--night-900`. */
const SEAT_COLORS = ["var(--amber)", "var(--sky)", "var(--mint)", "var(--pink)", "#ff9a52", "#b7a4ff", "#d2ee4a", "var(--quit-line)"];

/** The colour of the seat at `index` (join order); the round-robin and timed screens too (plans 163, 164). */
export const seatColor = (index: number): string => SEAT_COLORS[index % SEAT_COLORS.length];
