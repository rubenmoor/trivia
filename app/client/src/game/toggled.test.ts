import assert from "node:assert/strict";
import { test } from "node:test";
import { toggled } from "./toggled.ts";

const bundles = [{ id: "base", base: true }, { id: "cn", base: true }, { id: "a", base: false }, { id: "b", base: false }];
const [base, cn, a, b] = bundles;

test("picking a base bundle deselects the other base bundle, add-ons stay", () => {
  assert.deepEqual(toggled(bundles, ["base", "a"], cn), ["cn", "a"]);
});
test("picking the selected base bundle turns it off", () => {
  assert.deepEqual(toggled(bundles, ["base", "a"], base), ["a"]);
});
test("a base bundle comes on beside add-ons from none", () => {
  assert.deepEqual(toggled(bundles, ["a"], cn), ["cn", "a"]);
});
test("add-ons toggle freely", () => {
  assert.deepEqual(toggled(bundles, ["base", "a"], b), ["base", "a", "b"]);
  assert.deepEqual(toggled(bundles, ["base", "a"], a), ["base"]);
});
