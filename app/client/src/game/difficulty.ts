// The difficulty lines of the configure screen and the gamemaster's settings: age groups, then «Custom».
import { DIFFICULTY_MAX, type ChoiceOptions } from "../lib/api.ts";
import type { Difficulty } from "../lib/types.ts";

export type DifficultyPick<G extends string | null> = { group: G; custom: boolean; difficulty: Difficulty };

export const clamp = (n: number, lo: number, hi: number) => Math.min(hi, Math.max(lo, n));

/** A group's lowest and highest difficulty: where «Custom» starts. */
export function spanOf(groups: ChoiceOptions["groups"], id: string | null): Difficulty {
  const [start, end] = groups.find((g) => g.id === id)?.span ?? [1, DIFFICULTY_MAX];
  return { start, end };
}

/** ←/→ on `difficulty` cycles the age groups, then «Custom»; on `start`/`end` moves that end. Null: not a difficulty line. */
export function stepDifficulty<G extends string | null>(
  groups: ChoiceOptions["groups"], pick: DifficultyPick<G>, id: string, by: number,
): DifficultyPick<G | string> | null {
  const { group, custom, difficulty } = pick;
  if (id === "difficulty") {
    const ids = [...groups.map((g) => g.id), ""];
    const at = custom ? ids.length - 1 : ids.indexOf(group ?? "");
    const next = ids[(at + by + ids.length) % ids.length];
    return next ? { group: next, custom: false, difficulty } : { group, custom: true, difficulty: spanOf(groups, group) };
  }
  if (id === "start") {
    const start = clamp(difficulty.start + by, 1, DIFFICULTY_MAX);
    return { group, custom, difficulty: { start, end: Math.max(start, difficulty.end) } };
  }
  if (id === "end") return { group, custom, difficulty: { ...difficulty, end: clamp(difficulty.end + by, difficulty.start, DIFFICULTY_MAX) } };
  return null;
}
