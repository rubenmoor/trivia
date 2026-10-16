import { test } from "node:test";
import assert from "node:assert/strict";
import { gameAction } from "./api.ts";
import * as game from "./game.ts";
import { seededRng } from "./rng.ts";
import { emptySave, engineData, type EngineData, type SaveData } from "./state.ts";
import { realAgeGroups, realBundles, realCategories, realPool } from "./test/fixtures.ts";

const io = (seed: number) => ({ rng: seededRng(seed), now: "2026-10-16T00:00:00Z" });
const data: EngineData = engineData(realPool(), realCategories(), realBundles(), realAgeGroups());
const row = (save: SaveData) => save.games.at(-1)!;

let step = 0;
/** One engine call through the API; a refusal returns its error code. */
function act(save: SaveData, action: string, body: Record<string, unknown>): { save: SaveData; error?: string } {
  const r = gameAction(save, data, io(++step), action, body);
  return r.status === 200 ? { save: r.save } : { save, error: (r.body as { error: string }).error };
}
const correct = (save: SaveData) => row(save).state.answers.indexOf(data.byId.get(row(save).state.current!)!.answer);
const start = (jokers?: Record<string, number>) =>
  game.newSession(emptySave(), data, io(1), ["Ana", "Beto", "Cami"], { mode: "rr-coop", bundles: ["base"], ...(jokers ? { jokers } : {}) }).save;

test("rr-coop: turns rotate, shared jokers, «Paso» keeps the turn, a wrong answer loses for all", () => {
  let save = start();
  assert.equal(row(save).turn, 0);
  assert.equal(row(save).player_id, null);
  assert.deepEqual(row(save).seats!.map((s) => s.state), [undefined, undefined, undefined]);
  assert.equal(act(save, "pick", { index: 0, seat: 1 }).error, "not_your_turn");

  save = act(save, "pick", { index: 0, seat: 0 }).save;
  save = act(save, "joker", { joker: "skip", seat: 0 }).save; // the shared set's one «Paso»
  assert.equal(row(save).turn, 0);
  assert.equal(row(save).state.history.at(-1)!.seat, 0);
  save = act(save, "pick", { index: 0, seat: 0 }).save;
  save = act(save, "answer", { index: correct(save), seat: 0 }).save;
  assert.equal(row(save).turn, 1);
  assert.equal(row(save).state.level, 2);

  save = act(save, "pick", { index: 0, seat: 1 }).save;
  assert.equal(act(save, "joker", { joker: "skip", seat: 1 }).error, "joker_spent");
  const v = game.view(save, data, io(0))!;
  assert.equal(v.player, "Beto");
  assert.equal(v.last!.seat, 0);
  assert.deepEqual(v.session!.seats.map((s) => s.status), ["playing", "playing", "playing"]);
  const wrong = [0, 1, 2, 3].find((i) => i !== correct(save))!;
  save = act(save, "answer", { index: wrong, seat: 1 }).save;
  assert.equal(row(save).result, "lost");
  assert.equal(row(save).state.history.at(-1)!.seat, 1);
  assert.deepEqual(game.view(save, data, io(0))!.session!.seats.map((s) => s.status), ["lost", "lost", "lost"]);
});

test("rr-coop: turns wrap around and a run to the last level is won by all", () => {
  let save = start();
  for (let i = 0; i < 12; i++) {
    const seat = row(save).turn!;
    assert.equal(seat, i % 3);
    save = act(save, "pick", { index: 0, seat }).save;
    save = act(save, "answer", { index: correct(save), seat }).save;
  }
  assert.equal(row(save).result, "won");
  assert.deepEqual(game.view(save, data, io(0))!.session!.seats.map((s) => s.status), ["won", "won", "won"]);
});
