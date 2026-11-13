// Steam achievement unlocks (plan 86): after the save loads and when a game ends; each id once per page load.
import { steamUnlocks } from "../engine/achievements.ts";
import type { EngineData, SaveData } from "../engine/state.ts";
import { steam, validUser } from "./desktop.ts";

const live = validUser && steam?.available === true;
const sent = new Set<string>();
let ended: Set<string> | null = null;
let careerOn: Set<number> | null = null;

const endedGames = (save: SaveData) =>
  new Set(save.games.flatMap((g) => (g.result === null ? [] : [`${g.id}:${g.finished_on}`])));

/** Fire-and-forget; a refused or failed call is retried on the next page load. */
function unlockEarned(save: SaveData, data: EngineData): void {
  if (!live) return;
  for (const id of steamUnlocks(save, data)) {
    if (sent.has(id)) continue;
    sent.add(id);
    steam!.unlock(id).catch((e: unknown) => console.warn("achievements:", e));
  }
}

/** The save at page load: retroactive unlocks (imported saves, games before publishing, failed calls). */
export function achievementsLoad(save: SaveData, data: EngineData): void {
  ended = endedGames(save);
  careerOn = careerOnPlayers(save);
  unlockEarned(save, data);
}

const careerOnPlayers = (save: SaveData) => new Set(save.players.filter((p) => !p.career?.off).map((p) => p.id));

/** After an adopted save: unlocks when a game ended (won, lost, abandoned) or a player turned the career on; a badge earned mid-game waits for the end. */
export function achievementsCheckpoint(save: SaveData, data: EngineData): void {
  const now = endedGames(save);
  const fresh = [...now].some((k) => !ended?.has(k));
  const on = careerOnPlayers(save);
  const turnedOn = [...on].some((p) => !careerOn?.has(p));
  ended = now;
  careerOn = on;
  if (fresh || turnedOn) unlockEarned(save, data);
}
