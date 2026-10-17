// A local multiplayer session's seats on screen (plan 162): the Join screen's draft and the seat colours, which the
// round-robin and timed screens show too (decision 279). Bindings and the input filter: lib/seats.ts.
import { lang, t } from "../lib/i18n.ts";
import type { Binding, SessionView } from "../lib/seats.ts";

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

/** The tower of `seat` in its own game (rr-competitive): the levels behind it, all of them once it won. */
export function seatBlocks(session: SessionView, seat: number, levels: number): number {
  const s = session.seats[seat];
  return s.status === "won" ? levels : s.level - 1;
}

/** The session's names, the first `max` of them and «y n más» (Victory's team line, Start's resume line). */
export function seatNames(session: SessionView, max: number): string {
  const names = session.seats.map((s, i) => s.player ?? String(i + 1));
  const shown = names.length > max ? [...names.slice(0, max), t("seat.more", { n: names.length - max })] : names;
  return new Intl.ListFormat(lang === "xx" ? "es" : lang, { type: "conjunction" }).format(shown);
}

const MODE_NAME = { "rr-coop": "mode.rrCoop", "rr-competitive": "mode.rrCompetitive", timed: "mode.timed" } as const;

/** A session mode's name on the mode row (Choice). */
export const modeName = (session: SessionView): string =>
  t(MODE_NAME[session.mode as keyof typeof MODE_NAME] ?? "mode.solo");
