import { test } from "node:test";
import assert from "node:assert/strict";
import { wrongTransitionCue } from "./wrongCue.ts";

test("Wrong answer: the transition to the wrong screen adds no second sound after the reveal", () => {
  assert.equal(wrongTransitionCue(true), null);
  assert.equal(wrongTransitionCue(false), "boom");
});
