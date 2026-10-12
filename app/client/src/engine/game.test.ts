import { test } from "node:test";
import assert from "node:assert/strict";
import { readdirSync } from "node:fs";
import { join } from "node:path";
import type { Category } from "../lib/types.ts";
import { deletePlayer, gameAction, getGame, getPlayers } from "./api.ts";
import type { PoolQuestion } from "./pool.ts";
import { emptySave, engineData, type EngineData, type SaveData } from "./state.ts";
import { fixture } from "./test/fixtures.ts";
import { snapshot } from "./test/save.ts";
import { tapeRng, type TapeEntry } from "./test/tape.ts";

interface Step {
  now: string;
  pool: string;
  call: string;
  args: Record<string, unknown>;
  tape: TapeEntry[];
  response: { status: number; body: unknown };
  db?: Pick<SaveData, "players" | "games" | "burned">;
}

const categories = fixture("categories.json") as Category[];
const data: Record<string, EngineData> = {};
const dataFor = (pool: string): EngineData =>
  (data[pool] ??= engineData((fixture(`pools/${pool}.json`) as { questions: PoolQuestion[] }).questions, categories));

const scenarios = readdirSync(join(import.meta.dirname, "fixtures/game")).filter((f) => f.endsWith(".json")).sort();

for (const file of scenarios) {
  test(`game/${file}`, () => {
    const { steps } = fixture(`game/${file}`) as { steps: Step[] };
    let save = emptySave();
    steps.forEach((step, i) => {
      const at = `step ${i} (${step.call})`;
      const rng = tapeRng(step.tape);
      const io = { rng, now: step.now };
      const d = dataFor(step.pool);
      const r = step.call === "get_game" ? getGame(save, d, io, step.args.player as string | undefined)
        : step.call === "players" ? getPlayers(save)
        : step.call === "delete_player" ? deletePlayer(save, step.args)
        : gameAction(save, d, io, step.call, step.args);
      assert.deepEqual({ status: r.status, body: r.body }, step.response, at);
      if (r.status !== 200) assert.deepEqual(r.save, save, `${at}: save changed on error`);
      if (step.db) assert.deepEqual(snapshot(r.save), step.db, `${at}: db`);
      rng.done();
      save = r.save;
    });
  });
}
