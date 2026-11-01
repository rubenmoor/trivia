import assert from "node:assert/strict";
import { test } from "node:test";
import { pickVariant } from "./variant.ts";

test("never repeats the last pick", () => {
  for (let i = 0; i < 200; i++) assert.notEqual(pickVariant(["a", "b", "c"], "b"), "b");
});

test("a lone variant repeats, an empty list gives nothing", () => {
  assert.equal(pickVariant(["a"], "a"), "a");
  assert.equal(pickVariant([], "a"), undefined);
});

test("a failed variant is skipped when the caller passes only the loaded ones", () => {
  const loaded = ["a", "b", "c"].filter((x) => x !== "c");
  for (let i = 0; i < 200; i++) assert.notEqual(pickVariant(loaded), "c");
});

test("every other variant can come up", () => {
  const seen = new Set([0, 0.5, 0.99].map((r) => pickVariant(["a", "b", "c"], "a", () => r)));
  assert.deepEqual([...seen].sort(), ["b", "c"]);
});
