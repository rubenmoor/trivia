// Score and rank texts (plan 198, plans/24-career.md "Score", "Rank"): number format and rank names.
import { catalogFor } from "./i18n.ts";

/** A whole number in `locale`'s format; a negative one with the real minus «−». */
export function formatScore(n: number, locale: string): string {
  return new Intl.NumberFormat(locale).format(n).replace("-", "−");
}

/** The sign text of a score change: «+25», «−1». */
export function formatDelta(d: number, locale: string): string {
  const c = catalogFor(locale).career.delta;
  return (d < 0 ? c.minus : c.plus).replace("{n}", formatScore(Math.abs(d), locale));
}

/** Shown rank of rank value `n`: rounded half up, 1 to 15. */
export const rankNumber = (n: number): number => Math.min(RANKS, Math.max(1, Math.floor(n + 0.5)));
const RANKS = 15;

/** Rank name of rank value `n` (as `rankNumber`). */
export function rankText(n: number, locale: string): string {
  return catalogFor(locale).career.ranks[rankNumber(n) - 1];
}
