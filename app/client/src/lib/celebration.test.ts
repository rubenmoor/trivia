import { test } from "node:test";
import assert from "node:assert/strict";
import type { CareerView } from "../engine/career.ts";
import { celebrationQueue, REVEAL_MAX_MS, REVEAL_STEP_MS, revealStep, unshown } from "./celebration.ts";

const view = (badges: [string, boolean][], off = false): CareerView => ({
  off, score: 0, rank: null, rank_index: null, right: {}, years: {}, badges: badges.map(([name, shown]) => ({ name, on: "2026-11-01", shown })),
});
const seats = (...players: (string | null)[]) =>
  ({ mode: "rr-coop", turn: 0, seats: players.map((player) => ({ player })) }) as never;

test("unshown: not-shown badges, none while off", () => {
  assert.deepEqual(unshown(view([["A", true], ["B", false], ["C", false]])), ["B", "C"]);
  assert.deepEqual(unshown(view([["B", false]], true)), []);
  assert.deepEqual(unshown(undefined), []);
});

test("celebrationQueue: seat order, once each, only with new badges", () => {
  const careers = { Ana: view([["A", false]]), Luis: view([["A", true]]), Eva: view([["B", false]]), Off: view([["B", false]], true) };
  assert.deepEqual(celebrationQueue({ player: "Ana", session: undefined }, careers), ["Ana"]);
  assert.deepEqual(celebrationQueue({ player: "Luis", session: undefined }, careers), []);
  assert.deepEqual(celebrationQueue({ player: "Ana", session: seats("Eva", "Luis", null, "Off", "Ana", "Eva") }, careers), ["Eva", "Ana"]);
  assert.deepEqual(celebrationQueue({ player: null, session: undefined }, careers), []);
  assert.deepEqual(celebrationQueue(null, careers), []);
});

test("revealStep: capped total", () => {
  assert.equal(revealStep(1), REVEAL_STEP_MS);
  assert.ok(revealStep(39) * 39 <= REVEAL_MAX_MS);
  assert.ok(revealStep(8) * 8 <= REVEAL_MAX_MS);
});
