// Steam achievement unlocks (plan 86): after the save loads and when a game ends; each id once per page load.
import { earned, inSteamworks } from "../engine/achievements.ts";
import type { EngineData, SaveData } from "../engine/state.ts";
import { steam, validUser } from "./desktop.ts";

const live = validUser && steam?.available === true;
const sent = new Set<string>();
let ended: Set<string> | null = null;

const endedGames = (save: SaveData) =>
  new Set(save.games.flatMap((g) => (g.result === null ? [] : [`${g.id}:${g.finished_on}`])));

/** Fire-and-forget; a refused or failed call is retried on the next page load. */
function unlockEarned(save: SaveData, data: EngineData): void {
  if (!live) return;
  for (const id of earned(save, data)) {
    if (sent.has(id) || !inSteamworks(id)) continue;
    sent.add(id);
    steam!.unlock(id).catch((e: unknown) => console.warn("achievements:", e));
  }
}

/** The save at page load: retroactive unlocks (imported saves, games before publishing, failed calls). */
export function achievementsLoad(save: SaveData, data: EngineData): void {
  ended = endedGames(save);
  unlockEarned(save, data);
}

/** After an adopted save: unlocks only when a game ended (won, lost, abandoned). */
export function achievementsCheckpoint(save: SaveData, data: EngineData): void {
  const now = endedGames(save);
  const fresh = [...now].some((k) => !ended?.has(k));
  ended = now;
  if (fresh) unlockEarned(save, data);
}
