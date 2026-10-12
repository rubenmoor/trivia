import { test } from "node:test";
import assert from "node:assert/strict";
import type { Category } from "../lib/types.ts";
import { broadOf, categoryOf, type PoolQuestion } from "./pool.ts";
import { assign, available, draw, inRange, PER_LEVEL, supply } from "./selection.ts";
import { fixture, realAgeGroups, realBundles } from "./test/fixtures.ts";
import { tapeRng, type TapeEntry } from "./test/tape.ts";

interface Case {
  name: string;
  fn: "in_range" | "assign" | "supply" | "draw";
  args: Record<string, any>;
  tape: TapeEntry[];
  result: any;
}

const pools: Record<string, PoolQuestion[]> = {
  main: (fixture("pools/main.json") as { questions: PoolQuestion[] }).questions,
  tight: (fixture("pools/tight.json") as { questions: PoolQuestion[] }).questions,
};
const broad = categoryOf(broadOf(fixture("categories.json") as Category[]));
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
        avoidCategories: args.avoid_categories ?? [],
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
