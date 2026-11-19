import type { Cue } from "./sound.svelte.ts";

/** The wrong screen's transition sound: none after a reveal that already played the wrong sound. */
export function wrongTransitionCue(revealSounded: boolean): Cue | null {
  return revealSounded ? null : "boom";
}
