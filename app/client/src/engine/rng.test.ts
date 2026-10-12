import { test } from "node:test";
import assert from "node:assert/strict";
import { randomSeed, seededRng } from "./rng.ts";
import { tapeRng } from "./test/tape.ts";

const range = (n: number): number[] => Array.from({ length: n }, (_, i) => i);

function perms(seed: number): number[][] {
  const rng = seededRng(seed);
  return [0, 1, 2, 5, 20, 100].map((n) => {
    const xs = range(n);
    rng.shuffle(xs, "draw");
    return xs;
  });
}

test("same seed, same permutations", () => {
  assert.deepEqual(perms(42), perms(42));
  assert.notDeepEqual(perms(42), perms(43));
});

test("shuffle yields permutations", () => {
  for (const seed of range(50)) {
    for (const xs of perms(seed)) {
      assert.deepEqual([...xs].sort((a, b) => a - b), range(xs.length));
    }
  }
});

test("randomSeed is a uint32", () => {
  const s = randomSeed();
  assert.ok(Number.isInteger(s) && s >= 0 && s < 2 ** 32);
});

test("tape applies perms in order", () => {
  const rng = tapeRng([
    { site: "draw", n: 3, perm: [2, 0, 1] },
    { site: "draw", n: 0, perm: [] },
    { site: "pick", n: 2, perm: [1, 0] },
  ]);
  const a = ["a", "b", "c"];
  rng.shuffle(a, "draw");
  assert.deepEqual(a, ["c", "a", "b"]);
  rng.shuffle([], "draw");
  const b = ["x", "y"];
  rng.shuffle(b, "pick");
  assert.deepEqual(b, ["y", "x"]);
  rng.done();
});

test("tape errors", () => {
  const entry = { site: "draw", n: 2, perm: [1, 0] };
  assert.throws(() => tapeRng([entry]).shuffle([1, 2, 3], "draw"), /n 2, got 3/);
  assert.throws(() => tapeRng([entry]).shuffle([1, 2], "pick"), /site draw, got pick/);
  assert.throws(() => tapeRng([]).shuffle([1, 2], "draw"), /missing entry/);
  assert.throws(() => tapeRng([entry]).done(), /1 leftover/);
});
