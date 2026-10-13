// The five joker tokens in tray order (plans/09-jokers.md): name, label, key and icon.
import type { IconName } from "./Icon.svelte";
import type { JokerName } from "../lib/types";
import { t } from "../lib/i18n";

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
