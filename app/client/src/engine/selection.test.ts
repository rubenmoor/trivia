import { test } from "node:test";
import assert from "node:assert/strict";
import { broadOf, catKey, categoryOf, type PoolQuestion } from "./pool.ts";
import { assign, available, draw, inRange, PER_LEVEL, supply } from "./selection.ts";
import { fixture, realAgeGroups, realBundles, slugFixtures } from "./test/fixtures.ts";
import { seededRng } from "./rng.ts";
import { tapeRng, type TapeEntry } from "./test/tape.ts";

interface Case {
  name: string;
  fn: "in_range" | "assign" | "supply" | "draw";
  args: Record<string, any>;
  tape: TapeEntry[];
  result: unknown;
}

// On slug keys (decision 259); recorded with bare names and category slugs.
const fx = slugFixtures();
const pools: Record<string, PoolQuestion[]> = { main: fx.pool("main"), tight: fx.pool("tight") };
const broad = categoryOf(broadOf(fx.categories));
const keyOf = new Map([...fx.categories.map((c) => [c.slug, catKey(c)] as const), ...Object.entries(fx.oldKeys.subcategories)]);
// Plan 18 recorded D-22 with every bundle: young_teens, all bundles on.
const ranges = realAgeGroups().find((g) => g.id === "young_teens")!.levels;
const bundles = new Set(realBundles().map((b) => b.id));

// Python JSON: int keys as strings.
const byLevel = <V>(m: Map<number, V>): Record<string, V> =>
  Object.fromEntries([...m].map(([k, v]) => [String(k), v]));

// Burned IDs as selection.burned_ids(player) sees the recorded DB.
function burned(args: Record<string, any>): string[] {
  const key = args.player?.toLowerCase();
  return (args.burns ?? [])
    .filter((b: { player: string | null }) => b.player === null || b.player.toLowerCase() === key)
    .map((b: { question_id: string }) => b.question_id);
}

function run(c: Case, rng: ReturnType<typeof tapeRng>): unknown {
  const { args } = c;
  const pool = pools[args.pool] ?? [];
  const without = new Set<string>(args.without ?? []);
  const questions = pool.filter((q) => !without.has(q.id));
  switch (c.fn) {
    case "in_range":
      return inRange({ difficulty: args.difficulty }, args.level, ranges);
    case "assign": {
      const { assignment, missing } = assign(questions, args.levels, ranges);
      return { assignment: byLevel(assignment), missing: byLevel(missing) };
    }
    case "supply":
      return supply(available(questions, burned(args), [], bundles), ranges);
    case "draw": {
      const keep = pool.filter((q) => (args.keep ?? []).includes(q.id));
      const drawn = draw(args.level, questions, {
        ranges,
        n: args.n ?? PER_LEVEL,
        keep,
        avoidCategories: (args.avoid_categories ?? []).map((c: string) => keyOf.get(c) ?? c),
        categoryOf: args.category_of === "broad" ? broad : undefined,
        rng,
      });
      return drawn && drawn.map((q) => q.id);
    }
  }
}

for (const c of fixture("selection.json") as Case[]) {
  test(c.name, () => {
    const rng = tapeRng(c.tape);
    assert.deepEqual(run(c, rng), c.result);
    rng.done();
  });
}

test("draw: lowest seen count first, category variety only breaks ties (plan 65)", () => {
  const [lo] = ranges[11];
  const q = (id: string, subcategory: string) => ({ id, difficulty: lo, subcategory });
  const qs = [q("a0", "A"), q("a1", "A"), q("b0", "B"), q("c1", "C"), q("d1", "D"), q("e2", "E")];
  const countOf = (x: { id: string }) => Number(x.id[1]);
  for (let seed = 1; seed <= 20; seed++) {
    const ids = draw(12, qs, { ranges, countOf, rng: seededRng(seed) })!.map((x) => x.id);
    assert.deepEqual(ids.slice(0, 2).sort(), ["a0", "b0"], `seed ${seed}`);
    assert.ok(["c1", "d1"].includes(ids[2]) && ["c1", "d1"].includes(ids[3]), `seed ${seed}: ${ids}`);
  }
});
