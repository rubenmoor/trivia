import { parseSave } from "../save.ts";
import type { PlayerRow, SaveData } from "../state.ts";

type Tables = Pick<SaveData, "players" | "games" | "seen" | "blocked">;

/** A fixture's v2 `db` (Python recordings, `burned`) as the v3 tables, through parseSave's upgrade;
 * history outcome `admin_burn` → `admin_block` (plan 65). */
export function upgradeDb(db: { players: PlayerRow[]; games: SaveData["games"]; burned: unknown[] }): Tables {
  const json = JSON.stringify({ version: 2, ...db, reports: [] }).replaceAll('"outcome":"admin_burn"', '"outcome":"admin_block"');
  const { players, games, seen, blocked } = parseSave(json);
  return snapshot({ players, games, seen, blocked });
}

/** Python's GF-7 deletes the player's burns; the engine keeps their seen rows (game_id 0). Compare without them. */
export function withoutOrphans(save: Tables): Tables {
  return { ...save, seen: save.seen.filter((s) => s.game_id !== 0) };
}

/** The save as the fixtures' `db` snapshot: tables only, rows by id, seen rows by (game_id, question_id), blocked sorted. */
export function snapshot(save: Tables): Tables {
  const byId = <T extends { id: number }>(rows: T[]) => [...rows].sort((a, b) => a.id - b.id);
  const seen = [...save.seen].sort((a, b) =>
    a.game_id - b.game_id || (a.question_id < b.question_id ? -1 : a.question_id > b.question_id ? 1 : 0));
  return { players: byId(save.players), games: byId(save.games), seen, blocked: [...save.blocked].sort() };
}
