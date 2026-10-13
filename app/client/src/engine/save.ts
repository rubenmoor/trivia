// The save document on disk (plan 49, PORT-4): parse/upgrade and flags.
import { pyLen } from "./pycompat.ts";
import { SAVE_VERSION, SPANISH, type FlagEntry, type FlagText, type Language, type SaveData } from "./state.ts";

const isObject = (v: unknown): v is Record<string, any> => typeof v === "object" && v !== null && !Array.isArray(v);

// Version n → n + 1, keyed by n.
const UPGRADES: Record<number, (doc: Record<string, any>) => Record<string, any>> = {
  1: (doc) => ({ ...doc, reports: [] }), // plan 36: «Reportar pregunta»
  2: upgradeBurns, // plan 65: seen counters
  3: mergeReports, // decision 60: one entry per flag
};

/** v2 → v3: a player's burn → one seen row; a burn for everyone (player_id null) → blocked. */
function upgradeBurns({ burned, ...doc }: Record<string, any>): Record<string, any> {
  if (!Array.isArray(burned) || !burned.every(isObject)) throw new Error("burned must hold objects");
  const seen = burned.filter((b) => b.player_id !== null)
    .map((b) => ({ question_id: b.question_id, game_id: b.game_id, seen_on: b.burned_on }));
  const blocked = [...new Set(burned.filter((b) => b.player_id === null).map((b) => b.question_id))];
  return { ...doc, seen, blocked, notified_exhausted: [] };
}

/** v3 → v4: each report becomes a flag, or adds its note to the question's flag. */
function mergeReports({ reports, ...doc }: Record<string, any>): Record<string, any> {
  if (!Array.isArray(reports) || !reports.every(isObject)) throw new Error("reports must hold objects");
  const names = new Map(Array.isArray(doc.players) ? doc.players.map((p: Record<string, any>) => [p?.id, p?.name]) : []);
  const flags: Record<string, FlagEntry> = isObject(doc.flags) ? { ...doc.flags } : {};
  for (const r of reports) {
    const old = flags[r.question_id];
    const note = [old?.note, r.note].filter(Boolean).join(" · ");
    flags[r.question_id] = {
      ...(old ?? { flagged_on: r.reported_on, player: names.get(r.player_id) ?? null, level: r.level }),
      ...(note ? { note } : {}),
    };
  }
  return { ...doc, flags };
}

/** A save from a newer game (plan 55): the desktop backs it up as `newer`, not `corrupt`. */
export class SaveNewerError extends Error {
  readonly code = "save_newer";
  constructor() {
    super("save from a newer game");
  }
}

/** A stored document as SaveData; throws on a broken shape or a save from a newer game. */
export function parseSave(json: unknown): SaveData {
  let doc = typeof json === "string" ? JSON.parse(json) : json;
  if (!isObject(doc)) throw new Error("save must be a JSON object");
  if (!Number.isInteger(doc.version) || doc.version < 1) throw new Error("save has no valid version");
  if (doc.version > SAVE_VERSION) throw new SaveNewerError();
  while (doc.version < SAVE_VERSION) doc = { ...UPGRADES[doc.version](doc), version: doc.version + 1 };
  for (const key of ["players", "games", "seen"] as const) {
    if (!Array.isArray(doc[key])) throw new Error(`${key} must be a list`);
    if (!doc[key].every(isObject)) throw new Error(`${key} must hold objects`);
  }
  for (const key of ["blocked", "notified_exhausted"] as const) {
    if (!Array.isArray(doc[key]) || !doc[key].every((v: unknown) => typeof v === "string"))
      throw new Error(`${key} must be a list of IDs`);
  }
  if (!doc.games.every((g: Record<string, any>) => isObject(g.state))) throw new Error("every game needs a state");
  if (!doc.games.every((g: Record<string, any>) => g.locale === undefined || typeof g.locale === "string"))
    throw new Error("a game's locale must be text");
  const flags = doc.flags ?? {};
  if (!isObject(flags)) throw new Error("flags must be an object");
  const language = doc.language ?? SPANISH;
  if (!isObject(language) || typeof language.ui !== "string" || typeof language.questions !== "string")
    throw new Error("language must be {ui, questions}");
  return { ...doc, flags, language: { ui: language.ui, questions: language.questions } } as SaveData;
}

/** A fresh save's language (plan 68): per list, the exact tag, then its language part, else en, else es.
 * `es-ES` → UI es-ES, questions es. */
export function defaultLanguage(tag: string, ui: readonly string[], questions: readonly string[]): Language {
  const best = (options: readonly string[]): string => {
    const exact = options.find((o) => o.toLowerCase() === tag.toLowerCase());
    const base = tag.split("-")[0].toLowerCase();
    return exact ?? options.find((o) => o.toLowerCase() === base) ?? (options.includes("en") ? "en" : "es");
  };
  return { ui: best(ui), questions: best(questions) };
}

/** What the flag dialog sends; `null` unflags. `locale`/`shown`: the game's question (decision 102). */
export type FlagInput = { player: string | null; level?: number; note?: string; locale?: string; shown?: FlagText } | null;

/** Longest flag note, in code points. */
export const MAX_NOTE = 500;

/** Flag, re-note or unflag one question: a new save; a reflag keeps the first `flagged_on`, player, level, locale and text. */
export function setFlag(save: SaveData, qid: string, flag: FlagInput, now: string): SaveData {
  if (typeof qid !== "string" || !qid) throw new Error("id must be a question ID");
  const note = flag?.note?.trim() ?? "";
  if (pyLen(note) > MAX_NOTE) throw new Error(`the note is longer than ${MAX_NOTE} letters`);
  const flags = { ...save.flags };
  if (flag) {
    const first: FlagEntry = {
      flagged_on: now,
      player: flag.player,
      ...(flag.level ? { level: flag.level } : {}),
      ...(flag.locale ? { locale: flag.locale } : {}),
      ...(flag.shown ? { shown: flag.shown } : {}),
    };
    const entry: FlagEntry = { ...(flags[qid] ?? first) };
    if (note) entry.note = note;
    else delete entry.note;
    flags[qid] = entry;
  } else delete flags[qid];
  return { ...save, flags };
}
