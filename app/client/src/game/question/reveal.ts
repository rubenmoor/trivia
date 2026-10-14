// An answer tile's look from the Question screen's state (screens/Question.svelte): lock, reveal, Francotirador.
import type { Game } from "../../lib/types.ts";
import type { IconName } from "../Icon.svelte";

export type AnswerView = {
  struck: number[];
  locked: number | null;
  /** Francotirador is aiming, at `target`. */
  snipe: boolean;
  target: number | null;
  /** Francotirador's shot hit the correct answer. */
  hit: number | null;
  revealed: boolean;
  result: Game["last"];
};

export function answerClass(i: number, v: AnswerView) {
  if (v.hit !== null) return i === v.hit ? "right" : "dim";
  if (v.struck.includes(i)) return "struck";
  if (v.snipe) return i === v.target ? "target" : "";
  if (v.revealed && v.result) {
    if (i === v.result.correct_index) return "right";
    if (i === v.result.chosen) return "wrong";
    return "dim";
  }
  if (v.locked === null) return "";
  return i === v.locked ? "locked" : "dim";
}

export function answerBadge(i: number, v: AnswerView): IconName | null {
  if (v.hit === i) return "check";
  if (v.struck.includes(i)) return "cross";
  if (v.revealed && v.result && i === v.result.correct_index) return "check";
  if (v.revealed && v.result && i === v.result.chosen) return "cross";
  if (v.locked === i) return "lock";
  return null;
}
