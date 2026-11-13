// The celebration of new career badges (plan 197, decision 591): who gets a page after a game, and the reveal's pace.
import type { CareerView } from "../engine/career.ts";
import type { Game } from "./types.ts";

/** Pause per badge. @internal used by tests */
export const REVEAL_STEP_MS = 700;
/** The whole reveal stays under this (a backfill of many). @internal used by tests */
export const REVEAL_MAX_MS = 6000;

/** Delay between two badges of a reveal of `n`. */
export const revealStep = (n: number): number => Math.min(REVEAL_STEP_MS, REVEAL_MAX_MS / Math.max(1, n));

/** Badges of a career not shown yet, in live order; none while it's off (decision 515). */
export const unshown = (c: CareerView | undefined): string[] => (c && !c.off ? c.badges.filter((b) => !b.shown).map((b) => b.name) : []);

/** The players of `game` in seat order, once each, with badges to celebrate. */
export function celebrationQueue(game: Pick<Game, "player" | "session"> | null, careers: Record<string, CareerView>): string[] {
  const names = game?.session ? game.session.seats.map((s) => s.player) : [game?.player ?? null];
  return [...new Set(names.filter((n): n is string => !!n))].filter((n) => unshown(careers[n]).length > 0);
}
