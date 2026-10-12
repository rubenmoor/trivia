// Levels per game (D-88, `settings.levels` 1–20): screens tuned for 12 map a level onto that scale.
import type { Game } from "../lib/types";

export const DEFAULT_LEVELS = 12;

export const levelsOf = (game: Game | null): number => game?.settings.levels ?? DEFAULT_LEVELS;

/** Level `level` of `levels` on the 1–12 scale (decision 46's steps); a 1-level game is the last level. */
export const onTwelve = (level: number, levels: number): number =>
  levels === 1 ? DEFAULT_LEVELS : Math.round(1 + ((DEFAULT_LEVELS - 1) * (level - 1)) / (levels - 1));
