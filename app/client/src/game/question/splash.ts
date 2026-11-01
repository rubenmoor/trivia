// Category splash entrances and exits (plans 181, 191): tables of class names, offsets and sound cues; the keyframes are in Splash.svelte.
import type { Cue } from "../sound.svelte.ts";

/** A light move of the small line (the category since decision 353), with its offset against the category's (ms, negative = earlier). */
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

/** A silent entrance: the classes of the big and small line's keyframes in Splash.svelte; `letters`: the big line rises in letter by letter, `spread` the share of the entrance spent staggering. */
export type SplashEntrance = { id: string; category: string; sub: string; letters?: { spread: number } };

export const SPLASH_ENTRANCES: SplashEntrance[] = [
  { id: "slam", category: "in-slam", sub: "in-rise" },
  { id: "pop", category: "in-pop", sub: "in-rise" },
  { id: "slide", category: "in-slide", sub: "in-rise" },
  { id: "drop", category: "in-drop", sub: "in-rise" },
  { id: "letters", category: "in-letters", sub: "in-rise", letters: { spread: 0.5 } },
];

/** What each table remembers: exits the last 5, entrances the last 2 (fewer while a table is short). */
const EXITS_KEEP = 5;
const ENTRANCES_KEEP = 2;
const recentExits: string[] = [];
const recentEntrances: string[] = [];

function pick<T extends { id: string }>(table: T[], recent: string[], keep: number): T {
  const free = table.filter((e) => !recent.includes(e.id));
  const item = free[Math.floor(Math.random() * free.length)];
  recent.push(item.id);
  while (recent.length > Math.min(keep, table.length - 1)) recent.shift();
  return item;
}

/** A random exit not among the last 5 picked. */
export const pickExit = (table: SplashExit[] = SPLASH_EXITS): SplashExit => pick(table, recentExits, EXITS_KEEP);

/** A random entrance not among the last 2 picked. */
export const pickEntrance = (table: SplashEntrance[] = SPLASH_ENTRANCES): SplashEntrance => pick(table, recentEntrances, ENTRANCES_KEEP);

/** Gallery hook (trivia-gallery): `window.__gallerySplash` freezes the splash at its hold, optionally on another topic. */
export function galleryHold(): { topic?: { category: string; subcategory: string | null } } | undefined {
  return (window as unknown as { __gallerySplash?: { topic?: { category: string; subcategory: string | null } } }).__gallerySplash;
}
