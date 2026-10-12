// The save document on disk (plan 49, PORT-4): parse/upgrade and flags.
import { SAVE_VERSION, type SaveData } from "./state.ts";

const isObject = (v: unknown): v is Record<string, any> => typeof v === "object" && v !== null && !Array.isArray(v);

// Version n → n + 1, keyed by n; empty while version 1 is the only one.
const UPGRADES: Record<number, (doc: Record<string, any>) => Record<string, any>> = {};

/** A stored document as SaveData; throws on a broken shape or a save from a newer game. */
export function parseSave(json: unknown): SaveData {
  let doc = typeof json === "string" ? JSON.parse(json) : json;
  if (!isObject(doc)) throw new Error("save must be a JSON object");
  if (!Number.isInteger(doc.version) || doc.version < 1) throw new Error("save has no valid version");
  if (doc.version > SAVE_VERSION) throw new Error("save from a newer game");
  while (doc.version < SAVE_VERSION) doc = { ...UPGRADES[doc.version](doc), version: doc.version + 1 };
  for (const key of ["players", "games", "burned"] as const) {
    if (!Array.isArray(doc[key])) throw new Error(`${key} must be a list`);
    if (!doc[key].every(isObject)) throw new Error(`${key} must hold objects`);
  }
  if (!doc.games.every((g: Record<string, any>) => isObject(g.state))) throw new Error("every game needs a state");
  const flags = doc.flags ?? {};
  if (!isObject(flags)) throw new Error("flags must be an object");
  return { ...doc, flags } as SaveData;
}

/** Flag or unflag one question (flags.set_flag): a new save; a reflag keeps the first `flagged_on`. */
export function setFlag(save: SaveData, qid: string, flagged: boolean, player: string | null, now: string): SaveData {
  if (typeof qid !== "string" || !qid) throw new Error("id must be a question ID");
  const flags = { ...save.flags };
  if (flagged) flags[qid] ??= { flagged_on: now, player };
  else delete flags[qid];
  return { ...save, flags };
}

/** Every flagged question ID, sorted. */
export function flaggedIds(save: SaveData): string[] {
  return Object.keys(save.flags).sort();
}
