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

const seatOf = (save: SaveData, seat: number) => row(save).seats![seat].state!;
const right = (save: SaveData, seat: number) => seatOf(save, seat).answers.indexOf(data.byId.get(seatOf(save, seat).current!)!.answer);
const competitive = (players: string[], age_groups: string[]) =>
  game.newSession(emptySave(), data, io(2), players, { mode: "rr-competitive", bundles: ["base"], age_group: "adults", age_groups }).save;
/** The turn's seat picks the first card and answers: right, or with `wrong` a wrong answer. */
function turn(save: SaveData, wrong = false): SaveData {
  const seat = row(save).turn!;
  save = act(save, "pick", { index: 0, seat }).save;
  const ok = right(save, seat);
  return act(save, "answer", { index: wrong ? [0, 1, 2, 3].find((i) => i !== ok)! : ok, seat }).save;
}
/** No question on two seats' tables or in two seats' offered. */
function noCardTwice(save: SaveData): void {
  const offered = row(save).seats!.flatMap((s) => s.state!.offered);
  assert.equal(new Set(offered).size, offered.length);
}

test("rr-competitive: own games and age groups, an out seat skipped, the last one standing wins", () => {
  let save = competitive(["Ana", "Beto", "Cami"], ["kids"]);
  assert.equal(row(save).state.settings.age_group, undefined);
  assert.equal(row(save).state.history.length, 0);
  assert.deepEqual(row(save).seats!.map((s) => s.state!.settings.age_group), ["kids", "adults", "adults"]);
  assert.ok(row(save).seats!.every((s) => s.state!.options.length === 4));
  noCardTwice(save);

  save = act(save, "pick", { index: 0, seat: 0 }).save;
  save = act(save, "joker", { joker: "hint", seat: 0 }).save;
  const seats = () => game.view(save, data, io(0))!.session!.seats;
  assert.equal(seats()[0].jokers_left.hint, game.STANDARD_JOKERS.hint! - 1);
  assert.equal(seats()[1].jokers_left.hint, game.STANDARD_JOKERS.hint);
  save = act(save, "answer", { index: right(save, 0), seat: 0 }).save;
  assert.equal(seatOf(save, 0).level, 2);
  save = turn(save, true); // Beto out
  assert.deepEqual([row(save).seats![1].out, row(save).seats![1].result, seatOf(save, 1).phase], [true, "lost", "lost"]);
  assert.equal(row(save).turn, 2);
  save = turn(save);
  assert.equal(row(save).turn, 0);
  save = turn(save);
  assert.equal(row(save).turn, 2);
  assert.equal(act(save, "pick", { index: 0, seat: 1 }).error, "seat_out");
  assert.equal(game.view(save, data, io(0))!.player, "Cami");
  assert.equal(game.view(save, data, io(0))!.level, 2);
  noCardTwice(save);

  save = turn(save, true); // Cami out: Ana, at level 3, wins (decision 278)
  assert.equal(row(save).result, "won");
  assert.equal(row(save).state.phase, "won");
  assert.ok(row(save).finished_on);
  const v = game.view(save, data, io(0))!;
  assert.deepEqual(v.session!.seats.map((s) => [s.status, s.level, s.age_group]), [["won", 3, "kids"], ["lost", 1, "adults"], ["lost", 2, "adults"]]);
  assert.deepEqual([v.player, v.level, v.last!.seat, v.last!.correct], ["Ana", 3, 2, false]);
  assert.equal(save.seen.filter((s) => s.game_id === row(save).id).length, 5);
});

test("rr-competitive: the first to the last level wins, the others lose", () => {
  let save = competitive(["Ana", "Beto"], ["kids", "young_teens"]);
  while (row(save).result === null) save = turn(save);
  assert.deepEqual(row(save).seats!.map((s) => [s.result, s.state!.level]), [["won", 12], ["lost", 12]]);
  assert.equal(seatOf(save, 0).phase, "won");
  assert.equal(seatOf(save, 1).history.length, 11);
  noCardTwice(save);
  assert.equal(game.view(save, data, io(0))!.player, "Ana");
});

test("rr-competitive: the supply check counts every seat's levels", () => {
  const players = Array.from({ length: 40 }, (_, i) => `P${i}`);
  const r = gameAction(emptySave(), data, io(3), "new", { players, mode: "rr-competitive", bundles: ["base"] });
  assert.equal(r.status, 409);
  assert.equal((r.body as { error: string }).error, "mode_not_built");
  assert.equal(game.newSession(emptySave(), data, io(3), players, { mode: "rr-coop", bundles: ["base"] }).save.games.length, 1);
  let short: unknown = null;
  try {
    game.newSession(emptySave(), data, io(3), players, { mode: "rr-competitive", bundles: ["base"] });
  } catch (e) {
    short = e;
  }
  assert.ok(short instanceof game.GameError && short.code === "supply_short");
  assert.ok(short.details!.levels.some((l) => l.seat === 39));
});
