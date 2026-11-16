import { test } from "node:test";
import assert from "node:assert/strict";
import { modePreset } from "./modePreset.ts";

const BUILT = ["solo", "gamemaster"] as const;
const ALL = ["solo", "gamemaster", "rr-coop", "rr-competitive", "timed"] as const;

test("Mode preset: no last choice → standard mode on the single-player step (task 2114)", () => {
  assert.deepEqual(modePreset(null, null, BUILT, 1), { pick: "solo", kind: "single", stage: "single" });
  // multiplayer modes shown: the kind step first, «Solo o en grupo» preselected
  assert.deepEqual(modePreset(null, null, ALL, 2), { pick: "solo", kind: "single", stage: "kind" });
});

test("Mode preset: the player's last mode wins when it is shown", () => {
  assert.deepEqual(modePreset(null, "gamemaster", BUILT, 1), { pick: "gamemaster", kind: "single", stage: "single" });
  assert.deepEqual(modePreset(null, "solo", BUILT, 1), { pick: "solo", kind: "single", stage: "single" });
  // a multiplayer last mode: its kind and tile, the kind step still first; Join asks for seats later
  assert.deepEqual(modePreset(null, "timed", ALL, 2), { pick: "timed", kind: "multi", stage: "kind" });
  // last mode not built (not shown): standard
  assert.deepEqual(modePreset(null, "timed", BUILT, 1), { pick: "solo", kind: "single", stage: "single" });
});

test("Mode preset: `?mode=` is the caller's `last`; Back from a later screen keeps the pick and opens its step", () => {
  assert.deepEqual(modePreset(null, "gamemaster", ALL, 2), { pick: "gamemaster", kind: "single", stage: "kind" });
  assert.deepEqual(modePreset("gamemaster", "solo", ALL, 2), { pick: "gamemaster", kind: "single", stage: "single" });
  assert.deepEqual(modePreset("rr-coop", null, ALL, 2), { pick: "rr-coop", kind: "multi", stage: "multi" });
});
