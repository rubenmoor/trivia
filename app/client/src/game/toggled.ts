import type { ChoiceOptions } from "../lib/api.ts";

type Bundle = ChoiceOptions["bundles"][number];

/** `selected` after picking `b`: every bundle toggles; turning a base bundle on turns the other base ones off (at
 * most one per session, decision 752). */
export function toggled(bundles: Pick<Bundle, "id" | "base">[], selected: string[], b: Pick<Bundle, "id" | "base">): string[] {
  const turnOn = !selected.includes(b.id);
  const on = (x: Pick<Bundle, "id" | "base">) => (x.id === b.id ? turnOn : selected.includes(x.id) && !(turnOn && b.base && x.base));
  return bundles.filter(on).map((x) => x.id);
}
