import { test } from "node:test";
import assert from "node:assert/strict";
import { broadOf, categoryOf } from "./pool.ts";
import { seededRng } from "./rng.ts";
import { assign, available, draw, inRange, LEVELS, PER_LEVEL, supply } from "./selection.ts";
import { realAgeGroups, realCategories, realPool } from "./test/fixtures.ts";

const SEEDS = 50;
const BUNDLE_SETS = [["base"], ["base", "colombia"]];

for (const group of realAgeGroups()) {
  for (const set of BUNDLE_SETS) {
    test(`12-level walk on the real pool, ${group.id} × {${set}}: 4 cards per level, lowest seen count first`, () => {
      const pool = realPool();
      const cat = categoryOf(broadOf(realCategories()));
      const ranges = group.levels;
      const bundles = new Set(set);
      const approved = pool.filter((q) => q.status === "approved").map((q) => q.id);

      for (let seed = 1; seed <= SEEDS; seed++) {
        const rng = seededRng(seed);
        // Random seen counts 0–3 on up to 90% of the approved questions; a few blocked.
        const shuffled = [...approved];
        rng.shuffle(shuffled, "test");
        const counts = new Map<string, number>();
        const seen = (seed * 7919) % Math.floor(approved.length * 0.9 + 1);
        shuffled.slice(0, seen).forEach((id, i) => counts.set(id, 1 + ((i * 31 + seed) % 3)));
        const blocked = new Set(shuffled.slice(seen, seen + 5));
        const countOf = (q: { id: string }) => counts.get(q.id) ?? 0;
        assert.ok(supply(available(pool, blocked, [], bundles), ranges).every((s) => s.missing === 0), `seed ${seed}: supply`);

        const offered = new Set<string>();
        const asked = new Set<string | null>();
        for (let level = 1; level <= LEVELS; level++) {
          const avail = available(pool, blocked, offered, bundles);
          const cards = draw(level, avail, { ranges, avoidCategories: asked, categoryOf: cat, countOf, rng });
          assert.ok(cards, `seed ${seed}: no draw at level ${level} despite full supply`);
          assert.equal(new Set(cards.map((q) => q.id)).size, PER_LEVEL, `seed ${seed} level ${level}: 4 distinct`);
          const later = Array.from({ length: LEVELS - level }, (_, i) => level + 1 + i);
          cards.forEach((q, j) => {
            assert.ok(inRange(q, level, ranges), `seed ${seed} level ${level}: ${q.id} out of range`);
            assert.ok(bundles.has(q.bundle ?? "base"), `seed ${seed}: ${q.id} from inactive bundle ${q.bundle}`);
            assert.ok(!blocked.has(q.id), `seed ${seed}: blocked ${q.id} offered`);
            assert.ok(!offered.has(q.id), `seed ${seed}: ${q.id} offered twice`);
            // Never a count-k card while a count-<k card fits the slot and keeps the later levels fillable.
            const before = new Set(cards.slice(0, j).map((c) => c.id));
            for (const x of avail) {
              if (before.has(x.id) || countOf(x) >= countOf(q) || !inRange(x, level, ranges)) continue;
              const rest = avail.filter((y) => y.id !== x.id && !before.has(y.id));
              assert.ok(assign(rest, later, ranges).missing.size > 0,
                `seed ${seed} level ${level}: ${q.id} (count ${countOf(q)}) over ${x.id} (count ${countOf(x)})`);
            }
          });
          for (const q of cards) offered.add(q.id);
          asked.add(cat(cards[0]));
        }
      }
    });
  }
}
