// Server error codes → Spanish (D-57). Interim map; moves into the es catalog (plan 22, task 2).
import { GameError } from "./api";
import type { ErrorInfo, JokerName } from "./types";

const SPENT: Record<JokerName, string> = {
  hint: "ya no les quedan Soplos",
  skip: "ya no les quedan Pasos",
  easier: "ya no les quedan Bájales",
  category: "ya no les quedan Cambiazos",
  snipe: "ya no les quedan Francotiradores",
};

const SUPPLY_LEVEL = "nivel {level} (dificultad {lo}–{hi}): faltan {missing}";

/** Player-facing codes only; the others show the server's English message. */
const ES: Record<string, string> = {
  name_missing: "falta el nombre del jugador",
  name_too_long: "el nombre es demasiado largo (máximo {max} letras)",
  player_unknown: "no hay ningún jugador «{name}»",
  level_empty: "no quedan preguntas para el nivel {level} (dificultad {lo}–{hi})",
  supply_short: "no hay suficientes preguntas: {levels}",
  purge_short: "sin este tema no alcanzan las preguntas",
  refill_empty: "no hay otra pregunta para este nivel",
  hints_used_up: "no quedan pistas",
  easier_none: "no hay preguntas más fáciles de este tema",
  category_unknown: "ese tema no existe",
  category_same: "ya están en ese tema",
  category_empty: "no hay preguntas de ese tema para este nivel",
  category_none: "no hay preguntas de otros temas para este nivel",
  snipe_last: "solo queda una respuesta",
  snipe_invalid: "no se puede apuntar a esa respuesta",
  snipe_no_repeat: "si le dan a la correcta, no quedan preguntas para repetir el nivel",
  joker_not_question: "los comodines solo se juegan en una pregunta",
  age_group_unknown: "grupo de edad desconocido: '{group}'",
  bundle_unknown: "paquete desconocido: '{bundle}'",
  bundles_not_list: "los paquetes deben ser una lista",
};

function fill(template: string, params: Record<string, unknown>): string {
  return template.replace(/\{(\w+)\}/g, (m, k: string) => (k in params ? String(params[k]) : m));
}

/** Spanish text of a code, or null if it has none (internal code). */
function spanish({ code, params }: ErrorInfo): string | null {
  if (code === "joker_spent") return SPENT[params.joker as JokerName] ?? null;
  if (!(code in ES)) return null;
  if (code === "supply_short") {
    const levels = (params.levels ?? []) as Record<string, unknown>[];
    return fill(ES[code], { levels: levels.map((l) => fill(SUPPLY_LEVEL, l)).join(", ") });
  }
  return fill(ES[code], params);
}

/** What the corner error line shows for a caught error. */
export function errorText(e: unknown): string {
  if (e instanceof GameError) return spanish(e) ?? e.message;
  return e instanceof Error ? e.message : String(e);
}

/** Why a joker can't be played right now. */
export function reasonText(info: ErrorInfo): string {
  return spanish(info) ?? info.code;
}
