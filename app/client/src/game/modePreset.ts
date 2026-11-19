// The Mode screen's preset (plans/04-ui-tv-display.md, "Mode"; MD-7, task 2114): the pick kept for Back, else `?mode=`,
// else the last mode played (the save's newest game's), else the standard mode. Pure, for the tests.
import type { GameMode } from "../lib/types.ts";
import { isSession } from "../engine/game.ts";

export type Kind = "single" | "multi";
export type Stage = "kind" | Kind;
const STANDARD_MODE: GameMode = "solo";

export interface ModePreset {
  pick: GameMode;
  kind: Kind;
  /** The step shown first: the kind step when there is one, except coming back from a later screen. */
  stage: Stage;
}

const kindOf = (mode: GameMode): Kind => (isSession(mode) ? "multi" : "single");

/** `kept`: Game.svelte's pick from an earlier visit; `last`: `?mode=`, else the last mode played, null without one;
 * `shown`: the modes on the screen (built, or marked in dev mode); `kinds`: 2 with a multiplayer mode shown. */
export function modePreset(kept: GameMode | null, last: GameMode | null, shown: readonly GameMode[], kinds: number): ModePreset {
  if (kept) return { pick: kept, kind: kindOf(kept), stage: kindOf(kept) };
  const stage: Stage = kinds > 1 ? "kind" : "single";
  if (last && shown.includes(last)) return { pick: last, kind: kindOf(last), stage };
  return { pick: STANDARD_MODE, kind: "single", stage };
}
