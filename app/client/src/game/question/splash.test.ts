import assert from "node:assert/strict";
import { test } from "node:test";
import { SPLASH_ENTRANCES, SPLASH_EXITS, pickEntrance, pickExit } from "./splash.ts";

test("no recent repeat for either table", () => {
  const exits: string[] = [];
  for (let i = 0; i < 500; i++) {
    const id = pickExit().id;
    assert.ok(!exits.slice(-5).includes(id));
    exits.push(id);
  }
  const ins: string[] = [];
  for (let i = 0; i < 500; i++) {
    const id = pickEntrance().id;
    assert.ok(!ins.slice(-2).includes(id));
    ins.push(id);
  }
});

test("the exits' memory is unaffected by entrance picks", () => {
  for (let i = 0; i < 200; i++) {
    const first = pickExit().id;
    for (let k = 0; k < 10; k++) pickEntrance();
    assert.notEqual(pickExit().id, first);
  }
  assert.ok(SPLASH_ENTRANCES.length > 3 && SPLASH_EXITS.length > 5);
});
