import { test } from "node:test";
import assert from "node:assert/strict";
import { broadOf, categoryOf, parsePool } from "./pool.ts";
import { seededRng } from "./rng.ts";
import { available, draw, inRange, LEVELS, PER_LEVEL, supply } from "./selection.ts";
import { data, realAgeGroups, realCategories } from "./test/fixtures.ts";

const SEEDS = 50;
const json = data("pool.json");
const BUNDLE_SETS = [["base"], ["base", "colombia"]];

for (const group of json === undefined ? [] : realAgeGroups()) {
  for (const set of BUNDLE_SETS) {
    test(`12-level walk on the real pool, ${group.id} × {${set}}: 4 fresh cards per level, burned never return`, () => {
      const pool = parsePool(json);
      const cat = categoryOf(broadOf(realCategories()));
      const ranges = group.levels;
      const bundles = new Set(set);
      const approved = pool.filter((q) => q.status === "approved").map((q) => q.id);
      let walks = 0;

      for (let seed = 1; seed <= SEEDS; seed++) {
        const rng = seededRng(seed);
        // Burned subset: 0–40% of the approved questions.
        const shuffled = [...approved];
        rng.shuffle(shuffled, "test");
        const burned = new Set(shuffled.slice(0, (seed * 7919) % Math.floor(approved.length * 0.4 + 1)));
        if (supply(available(pool, burned, [], bundles), ranges).some((s) => s.missing > 0)) continue;
        walks++;

        const offered = new Set<string>();
        const asked = new Set<string | null>();
        for (let level = 1; level <= LEVELS; level++) {
          const cards = draw(level, available(pool, burned, offered, bundles), { ranges, avoidCategories: asked, categoryOf: cat, rng });
          assert.ok(cards, `seed ${seed}: no draw at level ${level} despite full supply`);
          assert.equal(new Set(cards.map((q) => q.id)).size, PER_LEVEL, `seed ${seed} level ${level}: 4 distinct`);
          for (const q of cards) {
            assert.ok(inRange(q, level, ranges), `seed ${seed} level ${level}: ${q.id} out of range`);
            assert.ok(bundles.has(q.bundle ?? "base"), `seed ${seed}: ${q.id} from inactive bundle ${q.bundle}`);
            assert.ok(!burned.has(q.id), `seed ${seed}: burned ${q.id} offered`);
            assert.ok(!offered.has(q.id), `seed ${seed}: ${q.id} offered twice`);
            offered.add(q.id);
          }
          asked.add(cat(cards[0]));
        }
      }
      assert.ok(walks >= SEEDS / 2, `only ${walks}/${SEEDS} burned subsets left full supply`);
    });
  }
}

if (json === undefined) test("12-level walks on the real pool", { skip: "app/data/pool.json absent (qgen export)" }, () => {});
