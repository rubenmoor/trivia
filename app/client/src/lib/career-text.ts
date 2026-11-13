// Score and rank texts (plan 198, plans/24-career.md "Score", "Rank"): number format and rank names.
import { catalogFor } from "./i18n.ts";

/** A whole number in `locale`'s format; a negative one with the real minus «−». */
export function formatScore(n: number, locale: string): string {
  return new Intl.NumberFormat(locale).format(n).replace("-", "−");
}

/** The sign text of a score change: «+25», «−1». @internal used by the score display (part 6) */
export function formatDelta(d: number, locale: string): string {
  const c = catalogFor(locale).career.delta;
  return (d < 0 ? c.minus : c.plus).replace("{n}", formatScore(Math.abs(d), locale));
}

/** Rank name of rank value `n` (rounded half up, at least 1, at most 15). @internal used by the rank display (part 6) */
export function rankText(n: number, locale: string): string {
  const names = catalogFor(locale).career.ranks;
  return names[Math.min(names.length, Math.max(1, Math.floor(n + 0.5))) - 1];
}
