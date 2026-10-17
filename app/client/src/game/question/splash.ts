// Category splash exits (plan 181): a table of category exit, subcategory exit and sound cue; the keyframes are in Splash.svelte.
import type { Cue } from "../sound.svelte.ts";

/** A light move of the small subcategory line, with its offset against the category's (ms, negative = earlier). */
export type SubExit = "fade" | "down" | "shrink" | "blur" | "drift-left" | "drift-right";

export type SplashExit = {
  id: string;
  /** The class of the category's keyframes in Splash.svelte. */
  category: string;
  sub: SubExit;
  subOffsetMs: number;
  cue: Cue;
};

export const SPLASH_EXITS: SplashExit[] = [
  { id: "fly-left", category: "fly-left", sub: "drift-left", subOffsetMs: 0, cue: "splash-left" },
  { id: "fly-right", category: "fly-right", sub: "drift-right", subOffsetMs: 0, cue: "splash-right" },
  { id: "fade", category: "fade", sub: "fade", subOffsetMs: -100, cue: "splash-fade" },
  { id: "spin", category: "spin", sub: "shrink", subOffsetMs: 100, cue: "splash-spin" },
];

const recent: string[] = [];

/** A random exit not among the last 5 picked (fewer while the table is short). */
export function pickExit(table: SplashExit[] = SPLASH_EXITS): SplashExit {
  const free = table.filter((e) => !recent.includes(e.id));
  const exit = free[Math.floor(Math.random() * free.length)];
  recent.push(exit.id);
  while (recent.length > Math.min(5, table.length - 1)) recent.shift();
  return exit;
}
