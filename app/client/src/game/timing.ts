// Every duration of the game in one place, to be tuned on the real TV (UI-6, 04-ui-tv-display.md).

/** Fade to black and back, each way. */
export const FADE_MS = 400;
/** A new tower block drops in after the fade (`drop` in Tower.svelte follows this). */
export const BLOCK_DROP_MS = 750;
/** The fade-in waits at most this long for the next question's media to load (UI-7). */
export const PRELOAD_MAX_MS = 2000;
/** «¡Hola, …!» on the Player screen before the transition to Level (UI-16). */
export const GREETING_MS = 1300;
/** The picked card pulses and tears open while the others slide off, before the transition (UI-11). */
export const PICK_MS = 1000;
/** When the flap of the picked card tears off (the CSS in Envelopes.svelte follows this). */
export const TEAR_MS = 300;
/** Suspense beat plus the padlock moving away before «Respuesta final» appears (UI-12). */
export const PADLOCK_MS = 1400;
/** Wait between the final answer and the reveal, by level on the 12-level scale (index 0 = level 1, game/levels.ts). */
export const REVEAL_WAIT_S = [3, 3, 4, 4, 5, 5, 6, 6, 8, 8, 10, 12];
/** An armed joker token drops back after this long (09, "Arming"). */
export const ARM_MS = 4000;
/** A played joker token flies to the centre, then bursts (JK-5); kept short, a joker plays many times a game. */
export const JOKER_FLY_MS = 450;
export const JOKER_BURST_MS = 250;
/** The token pops back into the tray after its joker (`pop-back` in JokerTray.svelte follows this). */
export const POP_BACK_MS = 500;
/** With reduced motion, the joker flight and the card flip are a quick fade. */
export const REDUCED_FADE_MS = 150;
/** The player asked for reduced motion (read each time: the setting can change mid-game). */
export const reducedMotion = () => matchMedia("(prefers-reduced-motion: reduce)").matches;
/** Each half of the card flip when Bájale or Cambiazo swaps the question (JK-7). */
export const FLIP_MS = 320;
/** Bájale's dial: a pause, one step per difficulty, then it stays a moment. */
export const DIAL_START_MS = 300;
export const DIAL_STEP_MS = 280;
export const DIAL_HOLD_MS = 1600;
/** «Paso»: the stamp scene before the shredder, the shredder, and the sweep off the screen (JK-6). */
export const STAMP_MS = 1300;
/** When the stamp lands (its `arrive` in Shredder.svelte follows this). */
export const STAMP_LAND_MS = 350;
export const SHRED_MS = 1100;
export const SWEEP_MS = 550;
/** Francotirador (JK-8): the beat of silence before the shot lands grows with the level; the shatter of a miss. */
export const SNIPE_BEAT_MS = (level: number) => 450 + level * 45;
export const SHATTER_MS = 850;
/** A Francotirador hit: the right answer glows this long before the level repeats (JK-8). */
export const SNIPE_HIT_MS = 2500;
/** How long the revealed answer stays on screen before the result screen. */
export const AFTER_REVEAL_MS = 2500;
/** Timed (decision 295): the beat between the claimer's pick and the reveal; then the result stays this long. */
export const TIMED_REVEAL_MS = 1200;
export const TIMED_RESULT_MS = 2200;
/** Timed round screen (decision 296): the hearts crack, then 3-2-1, one step each. */
export const ROUND_HOLD_MS = 1800;
export const COUNTDOWN_STEP_MS = 900;

/** Category splash (plan 181): it holds this long once the question is on screen, then leaves in at most SPLASH_EXIT_MS. */
export const SPLASH_HOLD_MS = 1000;
export const SPLASH_EXIT_MS = 700;
/** The subcategory's exit may start or end this much after the category's. */
export const SPLASH_SUB_MAX_MS = 100;

export const sleep = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));
