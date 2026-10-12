import type { BurnRow, SaveData } from "../state.ts";

const nullFirst = (a: number | null, b: number | null): number =>
  a === b ? 0 : a === null ? -1 : b === null ? 1 : a - b;

/** The save as the fixtures' `db` snapshot: tables only, rows by id, burns by (game_id, question_id, player_id). */
export function snapshot(save: Pick<SaveData, "players" | "games" | "burned">): Pick<SaveData, "players" | "games" | "burned"> {
  const byId = <T extends { id: number }>(rows: T[]) => [...rows].sort((a, b) => a.id - b.id);
  const burned = [...save.burned].sort((a: BurnRow, b: BurnRow) =>
    a.game_id - b.game_id
    || (a.question_id < b.question_id ? -1 : a.question_id > b.question_id ? 1 : 0)
    || nullFirst(a.player_id, b.player_id));
  return { players: byId(save.players), games: byId(save.games), burned };
}
