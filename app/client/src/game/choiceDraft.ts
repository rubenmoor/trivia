// The Choice screen's picks, kept in Game.svelte while the Bundles screen follows (plan 151).
import { CARDS_MAX, DEFAULT_AGE_GROUP, DIFFICULTY_MAX, STANDARD_JOKERS, type ChoiceBody } from "../lib/api.ts";
export { isSession } from "../lib/api.ts";
import type { Pace } from "../engine/choice.ts";
import type { Difficulty, GameMode, JokerBudget } from "../lib/types.ts";
import { presetOf } from "./jokers.ts";
import { DEFAULT_LEVELS } from "./levels.ts";

export interface ChoiceDraft {
  mode: GameMode;
  group: string;
  /** «Solo o en grupo»'s joker counts. */
  jokers: JokerBudget;
  /** Gamemaster mode (D-88); `custom`: the difficulty instead of the group. */
  custom: boolean;
  difficulty: Difficulty;
  levels: number;
  cards: number;
  video: boolean;
  audio: boolean;
  answers: boolean;
  /** Timed mode (Choice screen). */
  pace: Pace;
  budget: JokerBudget;
}

/** A fresh draft for the Mode screen's pick (the mode is never defaulted here, task 2114). */
export const defaultDraft = (mode: GameMode): ChoiceDraft => ({
  mode, group: DEFAULT_AGE_GROUP, jokers: { ...STANDARD_JOKERS }, custom: false,
  difficulty: { start: 1, end: DIFFICULTY_MAX }, levels: DEFAULT_LEVELS, cards: CARDS_MAX, video: true, audio: true, answers: true, pace: "normal",
  budget: { ...STANDARD_JOKERS },
});

/** The choice's body with the picked bundles (video and audio in every mode, decision 645); the jokers go only when they differ from the standard set (never in timed). */
export function bodyOf(d: ChoiceDraft, bundles: string[]): ChoiceBody {
  if (d.mode === "gamemaster") {
    return {
      ...(d.custom ? { difficulty: { ...d.difficulty } } : { age_group: d.group }),
      bundles: [...bundles], levels: d.levels, cards: d.cards, video: d.video, audio: d.audio, answers: d.answers, jokers: { ...d.budget },
    };
  }
  const jokers = d.mode !== "timed" && presetOf(d.jokers) !== "standard" ? { jokers: { ...d.jokers } } : {};
  // rr-competitive: every seat picks its own age group on the Join screen
  return { ...(d.mode === "rr-competitive" ? {} : { age_group: d.group }), bundles: [...bundles], video: d.video, audio: d.audio, ...(d.mode === "timed" ? { pace: d.pace } : {}), ...jokers };
}

export const choiceOf = (d: ChoiceDraft, bundles: string[]): ChoiceBody & { mode: GameMode } => ({ mode: d.mode, ...bodyOf(d, bundles) });
