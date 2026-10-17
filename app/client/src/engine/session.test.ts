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

// timed (plan 159): a seeded clock, every action at `ms`
const T0 = Date.parse("2026-10-16T00:00:00Z");
function timed(save: SaveData, action: string, body: Record<string, unknown>, ms: number): { save: SaveData; error?: string; params?: Record<string, unknown> } {
  const r = gameAction(save, data, { ...io(++step), ms }, action, body);
  if (r.status === 200) return { save: shown(r.save, ms) };
  const e = r.body as { error: string; params?: Record<string, unknown> };
  return { save, error: e.error, params: e.params };
}
/** The client's `show`, sent at once when a new question is drawn (decision 296). */
const shown = (save: SaveData, ms: number): SaveData =>
  row(save).state.timed?.shown_at === null && row(save).result === null ? gameAction(save, data, { ...io(++step), ms }, "show", {}).save : save;
const startTimed = (players: string[]) =>
  shown(game.newSession(emptySave(), data, { ...io(4), ms: T0 }, players, { mode: "timed", bundles: ["base"], age_group: "adults" }).save, T0);
const flow = (save: SaveData) => row(save).state.timed!;
const wrongOf = (save: SaveData) => [0, 1, 2, 3].find((i) => i !== correct(save))!;
/** `seat` claims at `ms` and answers a second later. */
const claimAnswer = (save: SaveData, seat: number, ok: boolean, ms: number) =>
  timed(timed(save, "claim", { seat }, ms).save, "answer", { seat, index: ok ? correct(save) : wrongOf(save) }, ms + 1000).save;
/** Every question of the round left unclaimed: expired one after the other. */
function idleRound(save: SaveData): SaveData {
  const level = row(save).state.level, repeat = flow(save).repeat;
  while (row(save).result === null && row(save).state.level === level && flow(save).repeat === repeat)
    save = timed(save, "expire", {}, flow(save).shown_at! + game.QUESTION_MS + 1).save;
  return save;
}

test("timed: claims, a claim run out, an unclaimed question, the round end's lives and size", () => {
  const players = ["Ana", "Beto", "Cami"];
  assert.throws(() => game.newSession(emptySave(), data, io(4), players, { mode: "timed", jokers: { hint: 1 } }), /no jokers/);
  let save = startTimed(players);
  const s = row(save).state;
  assert.deepEqual([s.phase, s.settings.cards, s.settings.customized, s.settings.jokers.hint, row(save).turn], ["question", 0, false, 0, undefined]);
  assert.deepEqual(row(save).seats!.map((x) => x.lives), [3, 3, 3]);
  assert.deepEqual(flow(save), { round_size: 3, round_done: 0, round_correct: [], shown_at: T0, claim: null, paused_at: null, repeat: 0 });

  assert.equal(timed(save, "answer", { seat: 0, index: 0 }, T0 + 1000).error, "claim_first");
  const early = timed(save, "expire", {}, T0 + game.QUESTION_MS);
  assert.deepEqual([early.error, early.params], ["not_expired", { ms: 0 }]);
  save = timed(save, "claim", { seat: 0 }, T0 + 29000).save; // a claim at 29 s still gets its 6 s
  assert.equal(timed(save, "claim", { seat: 1 }, T0 + 29500).error, "claim_taken");
  assert.equal(timed(save, "answer", { seat: 1, index: 0 }, T0 + 29500).error, "not_your_claim");
  assert.equal(timed(save, "joker", { joker: "hint", seat: 0 }, T0 + 29500).error, "timed_no_jokers");
  const q1 = data.byId.get(row(save).state.current!)!;
  save = timed(save, "answer", { seat: 0, index: correct(save) }, T0 + 29000 + game.CLAIM_MS).save;
  assert.deepEqual(row(save).state.history.at(-1), { level: 1, question_id: q1.id, seat: 0, chosen: row(save).state.last!.chosen, correct: true, hints: Math.min(q1.hints.length, 3) });
  assert.deepEqual([flow(save).round_correct, flow(save).round_done, flow(save).shown_at], [[0], 1, T0 + 35000]);

  save = timed(save, "claim", { seat: 1 }, T0 + 36000).save;
  assert.equal(timed(save, "expire", {}, T0 + 42000).error, "not_expired");
  save = timed(save, "expire", {}, T0 + 42001).save; // Beto's 6 s ran out: out at once
  assert.deepEqual([row(save).seats![1].out, row(save).seats![1].result], [true, "lost"]);
  assert.deepEqual([row(save).state.last!.timeout, row(save).state.history.at(-1)!.correct], [true, false]);
  assert.equal(timed(save, "claim", { seat: 1 }, T0 + 43000).error, "seat_out");

  save = timed(save, "claim", { seat: 2 }, flow(save).shown_at! + game.QUESTION_MS + 1).save; // too late: settled, no claim
  assert.equal(row(save).state.history.at(-1)!.unclaimed, true);
  assert.equal(row(save).state.history.at(-1)!.correct, undefined);
  // round end: Cami without a correct answer loses a life; round 2 has the two seats still in (decision 276)
  assert.deepEqual(row(save).seats!.map((x) => x.lives), [3, 3, 2]);
  assert.deepEqual([row(save).state.level, flow(save).round_size, flow(save).round_done, flow(save).claim], [2, 2, 0, null]);
  assert.equal(save.seen.filter((x) => x.game_id === row(save).id).length, 3);
  assert.equal(new Set(row(save).state.offered).size, 4);
});

test("timed: a correct answer in round 12 wins", () => {
  let save = startTimed(["Ana", "Beto"]);
  let ms = T0;
  for (let round = 1; round <= 11; round++) for (const seat of [0, 1]) save = claimAnswer(save, seat, true, ms += 2000);
  assert.deepEqual([row(save).state.level, row(save).result], [12, null]);
  assert.deepEqual(row(save).seats!.map((x) => x.lives), [3, 3]);
  save = claimAnswer(save, 1, true, ms += 2000);
  assert.deepEqual([row(save).result, row(save).state.phase], ["won", "won"]);
  assert.deepEqual(row(save).seats!.map((x) => x.result), ["lost", "won"]);
  assert.equal(save.seen.filter((x) => x.game_id === row(save).id).length, 23);
});

test("timed: a wrong answer leaves the last one standing", () => {
  let save = startTimed(["Ana", "Beto", "Cami"]);
  save = claimAnswer(save, 2, false, T0 + 1000);
  assert.equal(row(save).result, null);
  save = claimAnswer(save, 0, false, T0 + 3000);
  assert.deepEqual([row(save).result, row(save).seats!.map((x) => x.result)], ["won", ["lost", "won", "lost"]]);
  assert.ok(row(save).finished_on);
});

test("timed: round 12 without a correct answer repeats, everyone out means nobody wins", () => {
  let save = startTimed(["Ana", "Beto"]);
  let ms = T0;
  for (let round = 1; round <= 11; round++) for (const seat of [0, 1]) save = claimAnswer(save, seat, true, ms += 2000);
  save = idleRound(save);
  assert.deepEqual([row(save).state.level, flow(save).repeat, flow(save).round_size], [12, 1, 2]);
  assert.deepEqual(row(save).seats!.map((x) => x.lives), [2, 2]);
  save = idleRound(idleRound(save));
  assert.deepEqual([row(save).result, row(save).state.phase], ["lost", "lost"]);
  assert.deepEqual(row(save).seats!.map((x) => [x.lives, x.out, x.result]), [[0, true, "lost"], [0, true, "lost"]]);
});

test("timed: a pause shifts the question and claim deadlines and refuses play", () => {
  let save = startTimed(["Ana", "Beto"]);
  assert.equal(timed(save, "resume", {}, T0 + 1000).error, "not_paused");
  save = timed(save, "pause", {}, T0 + 10000).save;
  assert.equal(timed(save, "pause", {}, T0 + 11000).error, "already_paused");
  for (const a of ["claim", "answer", "expire"]) assert.equal(timed(save, a, { seat: 0, index: 0 }, T0 + 99000).error, "paused");
  const shown = game.view(save, data, { ...io(1), ms: T0 + 12000 })!;
  assert.deepEqual([shown.question, shown.session!.timed!.paused, shown.session!.timed!.deadline], [null, true, null]);
  save = timed(save, "resume", {}, T0 + 40000).save; // 30 s paused
  assert.equal(flow(save).shown_at, T0 + 30000);
  assert.equal(game.view(save, data, { ...io(1), ms: T0 + 40000 })!.session!.timed!.deadline, T0 + 30000 + game.QUESTION_MS);
  save = timed(save, "claim", { seat: 0 }, T0 + 41000).save;
  save = timed(save, "pause", {}, T0 + 43000).save;
  save = timed(save, "resume", {}, T0 + 50000).save;
  assert.equal(flow(save).claim!.at, T0 + 48000);
  assert.equal(timed(save, "expire", {}, T0 + 48000 + game.CLAIM_MS).error, "not_expired");
  const t = game.view(save, data, { ...io(1), ms: T0 + 51000 })!.session!;
  assert.deepEqual(t.timed!.claim, { seat: 0, deadline: T0 + 48000 + game.CLAIM_MS, question_left: game.QUESTION_MS - 11000 });
  assert.deepEqual(t.seats.map((s) => s.lives), [3, 3]);
});

test("timed: the question clock runs from show, not from the previous question's end", () => {
  const first = game.newSession(emptySave(), data, { ...io(4), ms: T0 }, ["Ana", "Beto"], { mode: "timed", bundles: ["base"], age_group: "adults" }).save;
  const send = (save: SaveData, action: string, body: Record<string, unknown>, ms: number) => {
    const r = gameAction(save, data, { ...io(++step), ms }, action, body);
    return r.status === 200 ? { save: r.save } : { save, error: (r.body as { error: string }).error };
  };
  assert.equal(flow(first).shown_at, null);
  assert.equal(game.view(first, data, { ...io(1), ms: T0 })!.session!.timed!.deadline, null);
  assert.equal(send(first, "claim", { seat: 0 }, T0 + 1000).error, "not_shown");
  assert.equal(send(first, "answer", { seat: 0, index: 0 }, T0 + 1000).error, "not_shown");
  assert.equal(send(first, "expire", {}, T0 + 99000).error, "not_expired");
  let save = send(first, "show", {}, T0 + 5000).save;
  assert.deepEqual(flow(send(save, "show", {}, T0 + 9000).save), flow(save)); // idempotent
  assert.equal(flow(send(save, "show", {}, T0 + 9000).save).shown_at, T0 + 5000);
  assert.equal(game.view(save, data, { ...io(1), ms: T0 + 5000 })!.session!.timed!.deadline, T0 + 5000 + game.QUESTION_MS);
  save = send(save, "claim", { seat: 0 }, T0 + 6000).save;
  save = send(save, "answer", { seat: 0, index: correct(save) }, T0 + 7000).save;
  assert.equal(flow(save).shown_at, null);
  assert.equal(send(save, "claim", { seat: 1 }, T0 + 8000).error, "not_shown");
  save = send(save, "show", {}, T0 + 20000).save;
  assert.equal(send(save, "expire", {}, T0 + 20000 + game.QUESTION_MS).error, "not_expired");
  assert.equal(row(send(save, "expire", {}, T0 + 20001 + game.QUESTION_MS).save).state.level, 2); // the round's second question ended
});
