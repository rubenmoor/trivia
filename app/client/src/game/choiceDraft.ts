// The Choice screen's picks, kept in Game.svelte while the Bundles screen follows (plan 151).
import { CARDS_MAX, DEFAULT_AGE_GROUP, DIFFICULTY_MAX, STANDARD_JOKERS, type ChoiceBody } from "../lib/api.ts";
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
  budget: JokerBudget;
}

export const defaultDraft = (): ChoiceDraft => ({
  mode: "gamemaster", group: DEFAULT_AGE_GROUP, jokers: { ...STANDARD_JOKERS }, custom: false,
  difficulty: { start: 1, end: DIFFICULTY_MAX }, levels: DEFAULT_LEVELS, cards: CARDS_MAX, video: true, audio: true, answers: true,
  budget: { ...STANDARD_JOKERS },
});

/** The choice's body with the picked bundles; solo sends its jokers only when they differ from the standard set. */
export function bodyOf(d: ChoiceDraft, bundles: string[]): ChoiceBody {
  if (d.mode === "gamemaster") {
    return {
      ...(d.custom ? { difficulty: { ...d.difficulty } } : { age_group: d.group }),
      bundles: [...bundles], levels: d.levels, cards: d.cards, video: d.video, audio: d.audio, answers: d.answers, jokers: { ...d.budget },
    };
  }
  return { age_group: d.group, bundles: [...bundles], ...(presetOf(d.jokers) !== "standard" ? { jokers: { ...d.jokers } } : {}) };
}

export const choiceOf = (d: ChoiceDraft, bundles: string[]): ChoiceBody & { mode: GameMode } => ({ mode: d.mode, ...bodyOf(d, bundles) });
