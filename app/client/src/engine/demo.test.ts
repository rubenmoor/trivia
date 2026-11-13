// Demo selection (plan 175, decision 340): equal play, equal questions; seen counts ignored.
import { test } from "node:test";
import assert from "node:assert/strict";
import { gameAction } from "./api.ts";
import * as game from "./game.ts";
import { actionRng } from "./rng.ts";
import { parseSave } from "./save.ts";
import { emptySave, engineData, type EngineData, type SaveData } from "./state.ts";
import { realAgeGroups, realBundles, realCategories, realPool } from "./test/fixtures.ts";

const data: EngineData = engineData(realPool(), realCategories(), realBundles(), realAgeGroups(), "es", undefined, null, true);
const T0 = Date.parse("2026-10-16T00:00:00Z");
const io = (ms = T0) => ({ rng: actionRng(data), now: "2026-10-16T00:00:00", ms });
const row = (save: SaveData) => save.games.at(-1)!;
const correct = (save: SaveData) => row(save).state.answers.indexOf(data.byId.get(row(save).state.current!)!.answer);

function act(save: SaveData, action: string, body: Record<string, unknown> = {}, ms = T0): SaveData {
  const r = gameAction(save, data, io(ms), action, body);
  assert.equal(r.status, 200, `${action}: ${JSON.stringify(r.body)}`);
  return r.save;
}

const trace = (save: SaveData) => save.games.map((g) => ({ offered: g.state.offered, current: g.state.current, answers: g.state.answers }));

/** Solo: picks, answers, «Bájale», «Cambiazo», «Paso»; the trace after every step. */
function solo(save: SaveData): { save: SaveData; steps: unknown[] } {
  const steps: unknown[] = [];
  const step = (s: SaveData) => (steps.push(trace(s)), s);
  save = step(act(save, "new", { player: "Ana", bundles: ["base"], age_group: "adults" }));
  save = step(act(save, "pick", { index: 0 }));
  save = step(act(save, "answer", { index: correct(save) }));
  save = step(act(save, "pick", { index: 1 }));
  save = step(act(save, "joker", { joker: "easier" }));
  save = step(act(save, "answer", { index: correct(save) }));
  save = step(act(save, "pick", { index: 0 }));
  const cats = game.view(save, data, io())!.jokers!.category.categories;
  const sub = cats.flatMap((c) => c.subcategories).find((s) => s.available)!.key;
  save = step(act(save, "joker", { joker: "category", subcategory: sub }));
  save = step(act(save, "answer", { index: correct(save) }));
  save = step(act(save, "pick", { index: 2 }));
  save = step(act(save, "joker", { joker: "skip" }));
  save = step(act(save, "pick", { index: 0 }));
  save = step(act(save, "answer", { index: (correct(save) + 1) % row(save).state.answers.length }));
  return { save, steps };
}

/** Timed, two seats: a few rounds of claims and answers. */
function timed(save: SaveData): unknown[] {
  let ms = T0;
  save = game.newSession(save, data, io(ms), ["Ana", "Beto"], { mode: "timed", bundles: ["base"], age_group: "adults" }).save;
  const steps: unknown[] = [];
  for (let i = 0; i < 6; i++) {
    if (row(save).state.timed!.shown_at === null) save = act(save, "show", {}, ms);
    const seat = i % 2;
    save = act(save, "claim", { seat }, (ms += 1000));
    save = act(save, "answer", { seat, index: correct(save) }, (ms += 1000));
    steps.push(trace(save));
  }
  return steps;
}

test("demo: equal play gives equal questions and answer orders", () => {
  const a = solo(emptySave()), b = solo(emptySave());
  assert.deepEqual(a.steps, b.steps);
  assert.deepEqual(timed(emptySave()), timed(emptySave()));
});

test("demo: a second game gets the first's questions, seen counts ignored", () => {
  const first = solo(emptySave());
  assert.ok(first.save.seen.length > 0);
  const second = solo(first.save);
  const last = (steps: unknown[]) => (steps as ReturnType<typeof trace>[]).map((t) => t.at(-1));
  assert.deepEqual(last(second.steps), last(first.steps));
});

test("full game: actionRng is fresh randomness", () => {
  const order = () => {
    const xs = Array.from({ length: 20 }, (_, i) => i);
    actionRng({ demo: false }).shuffle(xs, "draw");
    return xs;
  };
  assert.notDeepEqual(order(), order());
});

test("demo: game and session rows carry demo: true, full-build rows don't, a reload keeps it", () => {
  const full = engineData(realPool(), realCategories(), realBundles(), realAgeGroups(), "es", undefined, null, false);
  const fio = { rng: actionRng(full), now: "2026-10-16T00:00:00", ms: T0 };
  let save = game.newGame(emptySave(), data, io(), "Ana", { mode: "solo", bundles: ["base"], age_group: "adults" }).save;
  assert.equal(row(save).demo, true);
  save = game.newSession(save, data, io(), ["Ana", "Beto"], { mode: "timed", bundles: ["base"], age_group: "adults" }).save;
  assert.equal(row(save).demo, true);
  assert.equal(parseSave(JSON.stringify(save)).games.every((g) => g.demo === true), true);
  let other = game.newGame(emptySave(), full, fio, "Ana", { mode: "solo", bundles: ["base"], age_group: "adults" }).save;
  other = game.newSession(other, full, fio, ["Ana", "Beto"], { mode: "timed", bundles: ["base"], age_group: "adults" }).save;
  for (const g of other.games) assert.equal("demo" in g, false);
  assert.throws(() => parseSave({ ...JSON.parse(JSON.stringify(save)), games: save.games.map((g) => ({ ...g, demo: false })) }));
});
