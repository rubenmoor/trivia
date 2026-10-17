// The Question screen's own keys (plan 44), one copy: the screen's scope and the claim-key check (decision 290).
import type { Intent, Keys } from "../../lib/input.svelte.ts";
import { t } from "../../lib/i18n.ts";
import { TOKENS } from "../jokers.ts";
import { LETTERS } from "./Answers.svelte";

/** A–D pick, joker letters, replay, peek; 1–9 and the flag key are every scope's (input.svelte.ts). */
export function questionKeys(): Keys {
  return {
    ...Object.fromEntries(TOKENS.map((t) => [t.key.toLowerCase(), { type: "joker", name: t.name }])),
    ...Object.fromEntries(LETTERS.map((l, i) => [l.toLowerCase(), { type: "pick", n: i + 1 }])),
    [t("screen.question.replayKey").toLowerCase()]: { type: "replay" },
    [t("screen.question.peekKey").toLowerCase()]: { type: "peek", down: true },
  };
}

/** Pad (decision 9): Y/B/X/A pick by position; the Question and Timed screens. */
export const PAD_PICKS: Record<number, Intent> = Object.fromEntries([3, 1, 2, 0].map((b, i) => [b, { type: "pick", n: i + 1 }]));

/** A keyboard-only `timed` player's claim key: one letter or digit no Question key, not 1–9 or the flag key, distinct
 * from `taken` (decision 290). */
export function claimKeyOk(key: string, taken: readonly string[]): boolean {
  const k = key.toLowerCase();
  if (!/^(\p{L}|\d)$/u.test(k) || /[1-9]/.test(k) || k === t("flag.key").toLowerCase() || k in questionKeys()) return false;
  return !taken.some((x) => x.toLowerCase() === k);
}
