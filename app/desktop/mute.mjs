// Session mute for agents (plan 123); shared by the shell and the dev server.

/** Why the game starts muted, or null: `TRIVIA_SOUND=1` wins, then `PM_WORKER`, then `TRIVIA_MUTE=1`. */
export function muteReason(env) {
  if (env.TRIVIA_SOUND === "1") return null;
  if (env.PM_WORKER) return "PM_WORKER";
  if (env.TRIVIA_MUTE === "1") return "TRIVIA_MUTE";
  return null;
}
