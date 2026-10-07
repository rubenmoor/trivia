// The card flip when «Bájale» or «Cambiazo» swaps the question in place (plans/09-jokers.md, JK-7).
// Game.svelte sets `swap.active` just before the new question mounts; the transitions below only
// run then, so ordinary screen changes (behind the fade to black) stay instant.
import { cubicIn, cubicOut } from "svelte/easing";
import { FLIP_MS } from "./timing";

export const swap = { active: false };

const reduced = () => matchMedia("(prefers-reduced-motion: reduce)").matches;

/** The old side turns away (out) or the new side turns in after it (in), around the Y axis. */
export function cardFlip(_node: Element, { side }: { side: "in" | "out" }) {
  if (!swap.active) return { duration: 0 };
  if (reduced()) return { duration: 150, css: (t: number) => `opacity: ${t}` };
  return {
    delay: side === "in" ? FLIP_MS : 0,
    duration: FLIP_MS,
    easing: side === "in" ? cubicOut : cubicIn,
    css: (t: number) =>
      `transform: perspective(${1600}px) rotateY(${(1 - t) * (side === "in" ? -90 : 90)}deg); backface-visibility: hidden`,
  };
}

/** The picture crossfades under the flip. */
export function crossfade(_node: Element) {
  if (!swap.active) return { duration: 0 };
  return { duration: FLIP_MS * 2, css: (t: number) => `opacity: ${t}` };
}
