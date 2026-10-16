// The timed clock's pause for the Esc menu and the lost-pad dialog (decision 282, plan 161): the engine pauses on the
// first hold and resumes on the last release; outside `timed` a hold does nothing.
import { gameAction } from "./api.ts";
import { seating } from "./seats.svelte.ts";
import type { Game } from "./types.ts";

let holds = 0;

/** Pause the clock until the returned release runs; `apply` gets the game after each call. */
export function holdPause(apply: (game: Game | null) => void): () => void {
  if (!seating.view?.timed) return () => {};
  const call = (action: "pause" | "resume") => void gameAction(action).then(apply, () => {});
  if (holds++ === 0) call("pause");
  let done = false;
  return () => {
    if (done) return;
    done = true;
    if (--holds === 0) call("resume");
  };
}
