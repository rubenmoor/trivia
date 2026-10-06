// Every duration of the game in one place, to be tuned on the real TV (UI-6, 04-ui-tv-display.md).

/** Fade to black and back, each way. */
export const FADE_MS = 400;
/** «¡Hola, …!» on the Player screen before the transition to Level (UI-16). */
export const GREETING_MS = 1300;
/** The picked card pulses and the others slide off before the transition (UI-11). */
export const PICK_MS = 550;
/** Suspense beat plus the padlock moving away before «Respuesta final» appears (UI-12). */
export const PADLOCK_MS = 1400;
/** Wait between the final answer and the reveal, by level (index 0 = level 1). */
export const REVEAL_WAIT_S = [3, 3, 4, 4, 5, 5, 6, 6, 8, 8, 10, 12];
/** How long the revealed answer stays on screen before the result screen. */
export const AFTER_REVEAL_MS = 2500;

export const sleep = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));
