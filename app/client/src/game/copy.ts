// Milestone and consolation lines (plans/04-ui-tv-display.md, UI-14); texts in the catalog
// (`copy.*`, D-70). {n} is the level. Written for 12 levels; other counts (D-88) map onto them.
import { fill, variants } from "../lib/i18n.ts";
import { DEFAULT_LEVELS } from "./levels.ts";

type Line = 4 | 6 | 8 | 10 | 12;

/** The level of `levels` that gets each line: a third, half, two thirds, three to go, the last. */
function milestoneAt(levels: number): Map<number, Line> {
  const at = new Map<number, Line>([[levels, 12]]);
  if (levels - 2 >= 1 && !at.has(levels - 2)) at.set(levels - 2, 10);
  for (const [line, share] of [[4, 1 / 3], [6, 1 / 2], [8, 2 / 3]] as const) {
    const l = Math.round(levels * share);
    if (l > 1 && l <= levels - 3 && !at.has(l)) at.set(l, line);
  }
  return at;
}

/** After a wrong answer, by how far the players got: highest level of each bracket. */
const CONSOLATION_MAX = [3, 6, 9, 12] as const;

/** The same game and level always get the same line, so a re-render doesn't change it. */
const choose = (lines: readonly string[], seed: number) => lines[Math.abs(seed) % lines.length];

/** The Level screen's line, null at most levels. */
export function milestone(level: number, levels: number, seed: number): string | null {
  const at = milestoneAt(levels).get(level);
  return at ? fill(choose(variants(`copy.milestone.${at}`), seed)) : null; // fill traces it for the gallery
}

export function consolation(level: number, levels: number, seed: number): string {
  const scaled = (level * DEFAULT_LEVELS) / levels;
  const max = CONSOLATION_MAX.find((m) => scaled <= m) ?? CONSOLATION_MAX[CONSOLATION_MAX.length - 1];
  return fill(choose(variants(`copy.consolation.${max}`), seed), { n: level });
}
