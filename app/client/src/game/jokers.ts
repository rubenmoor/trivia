// The five joker tokens in tray order (plans/09-jokers.md): name, label, key and icon.
import type { IconName } from "./Icon.svelte";
import type { JokerBudget, JokerName } from "../lib/types.ts";
import { STANDARD_JOKERS } from "../lib/api.ts";
import { t } from "../lib/i18n.ts";

const ICONS: [JokerName, IconName][] = [
  ["hint", "bulb"],
  ["skip", "door"],
  ["easier", "stairs"],
  ["category", "compass"],
  ["snipe", "crosshair"],
];

/** Labels and keys in the UI language at import (a language change reloads the page). */
export const TOKENS: { name: JokerName; label: string; key: string; icon: IconName }[] = ICONS.map(([name, icon]) => ({
  name,
  label: t(`joker.${name}.name`),
  key: t(`joker.${name}.key`),
  icon,
}));

/** Most uses a budget stepper shows before ∞ (Customize, the gamemaster menu). */
export const MAX_USES = 9;

/** A budget stepper's next value: 0–9 uses, then ∞ (null), clamped at both ends. */
export function stepUses(now: number | null, by: number): number | null {
  const index = Math.min(MAX_USES + 1, Math.max(0, (now ?? MAX_USES + 1) + by));
  return index > MAX_USES ? null : index;
}

/** Pre-game joker presets (decision 99); any other budget is «custom». */
export const PRESETS = {
  standard: STANDARD_JOKERS,
  unlimited: Object.fromEntries(ICONS.map(([name]) => [name, null])) as JokerBudget,
};
export type Preset = keyof typeof PRESETS | "custom";

export function presetOf(budget: JokerBudget): Preset {
  const same = (p: JokerBudget) => ICONS.every(([name]) => budget[name] === p[name]);
  return same(PRESETS.standard) ? "standard" : same(PRESETS.unlimited) ? "unlimited" : "custom";
}

/** ←/→ on a preset row: Estándar ↔ Sin límite; from a custom budget → Estándar, ← Sin límite. */
export function stepPreset(budget: JokerBudget, by: number): JokerBudget {
  const now = presetOf(budget);
  const next = now === "custom" ? (by > 0 ? "standard" : "unlimited") : now === "standard" ? "unlimited" : "standard";
  return { ...PRESETS[next] };
}
