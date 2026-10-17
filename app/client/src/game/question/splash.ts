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
  /** The category is split into letters: `spread` is the share of the exit spent staggering their starts, `order` staggers left to right, else randomly. */
  letters?: { spread: number; order: boolean; reverse?: boolean };
};

export const SPLASH_EXITS: SplashExit[] = [
  { id: "fly-left", category: "fly-left", sub: "drift-left", subOffsetMs: 0, cue: "splash-left" },
  { id: "fly-right", category: "fly-right", sub: "drift-right", subOffsetMs: 0, cue: "splash-right" },
  { id: "fade", category: "fade", sub: "fade", subOffsetMs: -100, cue: "splash-fade" },
  { id: "spin", category: "spin", sub: "shrink", subOffsetMs: 100, cue: "splash-spin" },
  { id: "dissolve", category: "dissolve", sub: "blur", subOffsetMs: 0, cue: "splash-dissolve", letters: { spread: 0.3, order: false } },
  { id: "explode", category: "explode", sub: "fade", subOffsetMs: -100, cue: "splash-explode", letters: { spread: 0.1, order: false } },
  { id: "rocket", category: "rocket", sub: "down", subOffsetMs: 100, cue: "splash-rocket" },
  { id: "drop", category: "drop", sub: "shrink", subOffsetMs: 100, cue: "splash-drop" },
  { id: "wind", category: "wind", sub: "drift-right", subOffsetMs: 100, cue: "splash-wind", letters: { spread: 0.5, order: true } },
  { id: "blind", category: "blind", sub: "fade", subOffsetMs: -100, cue: "splash-blind" },
  { id: "drain", category: "drain", sub: "shrink", subOffsetMs: 0, cue: "splash-drain" },
  { id: "zoom", category: "zoom", sub: "blur", subOffsetMs: 0, cue: "splash-zoom" },
  { id: "shatter", category: "shatter", sub: "down", subOffsetMs: 100, cue: "splash-shatter", letters: { spread: 0.15, order: false } },
  { id: "melt", category: "melt", sub: "down", subOffsetMs: 0, cue: "splash-melt" },
  { id: "blackhole", category: "blackhole", sub: "shrink", subOffsetMs: 0, cue: "splash-blackhole" },
  { id: "birds", category: "birds", sub: "fade", subOffsetMs: -100, cue: "splash-birds", letters: { spread: 0.25, order: false } },
  { id: "typewriter", category: "typewriter", sub: "fade", subOffsetMs: 100, cue: "splash-typewriter", letters: { spread: 0.9, order: true, reverse: true } },
  { id: "plane", category: "plane", sub: "drift-right", subOffsetMs: 100, cue: "splash-plane" },
  { id: "jelly", category: "jelly", sub: "shrink", subOffsetMs: 100, cue: "splash-jelly" },
  { id: "pop", category: "pop", sub: "shrink", subOffsetMs: -100, cue: "splash-pop" },
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

/** Gallery hook (trivia-gallery): `window.__gallerySplash` freezes the splash at its hold, optionally on another topic. */
export function galleryHold(): { topic?: { category: string; subcategory: string | null } } | undefined {
  return (window as unknown as { __gallerySplash?: { topic?: { category: string; subcategory: string | null } } }).__gallerySplash;
}
