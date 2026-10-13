import { test } from "node:test";
import assert from "node:assert/strict";
import { STANDARD_JOKERS } from "./game.ts";
import { noteExhausted, outlook } from "./outlook.ts";
import type { AgeGroup, Bundle, PoolQuestion } from "./pool.ts";
import { emptySave, engineData, type SaveData } from "./state.ts";

// Level l = difficulty l; 20 base questions per difficulty, 10 at 7; colombia adds 10 at 7.
const group = {
  id: "g", name: "G", ages: [0, null], window: [1, 12], level_weights: {},
  levels: Array.from({ length: 12 }, (_, i) => [i + 1, i + 1] as const),
} as AgeGroup;
const bundle = (id: string, kind: string): Bundle => ({ id, kind, languages: ["es"], name: id, description: "" });
const q = (id: string, difficulty: number, bundle = "base", subcategory = "Y") =>
  ({ id, difficulty, bundle, subcategory, status: "approved" }) as PoolQuestion;
const pool = [
  ...Array.from({ length: 12 }, (_, i) => i + 1).flatMap((d) =>
    Array.from({ length: d === 7 ? 10 : 20 }, (_, j) => q(`b${d}-${j}`, d, "base", d === 1 && j < 2 ? "X" : "Y"))),
  ...Array.from({ length: 10 }, (_, j) => q(`c7-${j}`, 7, "colombia", "Z")),
];
const data = engineData(pool, [{ slug: "s", name: "S", bundle: "base", subcategories: ["X", "Y"] },
  { slug: "z", name: "Z", bundle: "colombia", subcategories: ["Z"] }], [bundle("base", "base"), bundle("colombia", "region")], [group]);
const solo = {
  age_group: "g", difficulty: null, bundles: ["base"], levels: 12, cards: 4, video: true, audio: true,
  jokers: STANDARD_JOKERS, mode: "solo" as const,
};
const seen = (save: SaveData, ...ids: string[]) =>
  ({ ...save, seen: ids.map((id) => ({ question_id: id, game_id: 1, seen_on: "x" })) });

test("outlook: k, bottleneck (plan 65)", () => {
  // b = 16/12: 4 + ceil(4k/3) ≤ 10 → k = 4.
  assert.deepEqual(outlook(emptySave(), data, solo),
    { k: 4, bottleneck: [[7, 7]], tight: [], none: false, bundleHint: null, exhausted: [] });
  assert.equal(outlook(emptySave(), data, { ...solo, bundles: ["base", "colombia"] }).k, 12);
  assert.equal(outlook(seen(emptySave(), "b7-0", "b7-1"), data, solo).k, 3);
  assert.equal(outlook(emptySave(), data, { ...solo, mode: "rr-competitive", players: 2 }).k, 2);
  const dry = seen(emptySave(), ...pool.filter((x) => x.difficulty === 7).map((x) => x.id));
  assert.deepEqual(outlook(dry, data, solo).bottleneck, [[7, 7]]);
  assert.equal(outlook(dry, data, solo).k, 0);
});

test("outlook: tight levels, none left, bundle hint (decision 31)", () => {
  const sevens = pool.filter((x) => x.difficulty === 7 && x.bundle === "base").map((x) => x.id);
  const one = outlook(seen(emptySave(), ...sevens.slice(1)), data, solo);
  assert.deepEqual([one.tight, one.none, one.bundleHint], [[[7, 7]], false, "colombia"]);
  const dry = outlook(seen(emptySave(), ...sevens), data, solo);
  assert.deepEqual([dry.tight, dry.none, dry.bundleHint], [[[7, 7]], true, "colombia"]);
  assert.deepEqual(outlook(seen(emptySave(), ...sevens.slice(2)), data, solo).tight, []);
});

test("outlook: exhausted subcategories, noted once, pruned when unseen again", () => {
  const save = seen(emptySave(), "b1-0", "b1-1");
  assert.deepEqual(outlook(save, data, solo).exhausted, ["X"]);
  const noted = noteExhausted(save, data, solo, ["X"]);
  assert.deepEqual(noted.notified_exhausted, ["X"]);
  assert.deepEqual(outlook(noted, data, solo).exhausted, []);
  assert.deepEqual(noteExhausted({ ...noted, seen: [] }, data, solo, []).notified_exhausted, []);
});
