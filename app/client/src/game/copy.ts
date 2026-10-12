// Milestone and consolation lines (plans/04-ui-tv-display.md, UI-14); texts in the catalog
// (`copy.*`, D-70). {n} is the level.
import { fill, variants } from "../lib/i18n";

/** Levels with a line on the Level screen; null at the others. */
const MILESTONE_LEVELS = [4, 6, 8, 10, 12] as const;

/** After a wrong answer, by how far the players got: highest level of each bracket. */
const CONSOLATION_MAX = [3, 6, 9, 12] as const;

/** The same game and level always get the same line, so a re-render doesn't change it. */
const choose = (lines: readonly string[], seed: number) => lines[Math.abs(seed) % lines.length];

export function milestone(level: number, seed: number): string | null {
  const at = MILESTONE_LEVELS.find((l) => l === level);
  return at ? choose(variants(`copy.milestone.${at}`), seed) : null;
}

export function consolation(level: number, seed: number): string {
  const max = CONSOLATION_MAX.find((m) => level <= m) ?? CONSOLATION_MAX[CONSOLATION_MAX.length - 1];
  return fill(choose(variants(`copy.consolation.${max}`), seed), { n: level });
}
