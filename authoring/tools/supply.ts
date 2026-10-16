// Supply check for qgen report and the authoring start page (plan 51, D-60): selection.ts under Node.
// stdin: {questions, burned, age_group?, bundles?} or an array of them; stdout: {per_level, ranges, bundles, supply} per input.
// Defaults: the default game (decision 103): young_teens, es's first base bundle only (decision 33).
import { readFileSync } from "node:fs";
import ageGroups from "../../app/data/age-groups.json" with { type: "json" };
import bundlesJson from "../../app/data/bundles.json" with { type: "json" };
import { DEFAULT_AGE_GROUP } from "../../app/client/src/engine/choice.ts";
import { bundlesFor, parseAgeGroups, parseBundles, type PoolQuestion } from "../../app/client/src/engine/pool.ts";
import { PER_LEVEL, available, supply } from "../../app/client/src/engine/selection.ts";

interface Input {
  questions: (Pick<PoolQuestion, "id" | "status" | "difficulty"> & { bundle?: string })[];
  burned: string[];
  age_group?: string;
  bundles?: string[];
}

const groups = parseAgeGroups(ageGroups);
const base = bundlesFor({ bundles: parseBundles(bundlesJson), locale: "es" }).find((b) => b.kind === "base")!.id;

function run({ questions, burned, age_group = DEFAULT_AGE_GROUP, bundles = [base] }: Input) {
  const group = groups.find((g) => g.id === age_group);
  if (!group) throw new Error(`unknown age group ${age_group}`);
  return {
    per_level: PER_LEVEL,
    ranges: Object.fromEntries(group.levels.map((r, i) => [i + 1, r])),
    bundles,
    supply: supply(available(questions, burned, [], new Set(bundles)), group.levels),
  };
}

const input = JSON.parse(readFileSync(0, "utf8")) as Input | Input[];
console.log(JSON.stringify(Array.isArray(input) ? input.map(run) : run(input)));
