// Server error codes → catalog texts `error.<code>` (D-57, plan 22).
import { GameError, messageOf } from "./http";
import { has, t, type Params } from "./i18n";
import type { ErrorInfo } from "./types";

/** Catalog text of a code, or null if it has none (internal code). */
function text({ code, params }: ErrorInfo): string | null {
  if (code === "joker_spent") {
    const key = `error.joker_spent.${params.joker}`;
    return has(key) ? t(key) : null;
  }
  const key = `error.${code}`;
  if (!has(key)) return null;
  if (code === "supply_short") {
    const levels = (params.levels ?? []) as Params[];
    return t(key, { levels: levels.map((l) => t("error.supply_level", l)).join(", ") });
  }
  return t(key, params as Params);
}

/** What the corner error line shows for a caught error. */
export function errorText(e: unknown): string {
  if (e instanceof GameError) return text(e) ?? e.message;
  return messageOf(e);
}

/** Why a joker can't be played right now. */
export function reasonText(info: ErrorInfo): string {
  return text(info) ?? info.code;
}
