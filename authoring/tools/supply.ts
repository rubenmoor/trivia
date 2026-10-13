// Supply check for qgen report and the authoring start page (plan 51, D-60): selection.ts under Node.
// stdin: {questions, burned, age_group?, bundles?} or an array of them; stdout: {per_level, ranges, supply} per input.
// Defaults: young_teens (the default age group), every bundle.
import { stdin } from "node:process";
import ageGroups from "../../app/data/age-groups.json" with { type: "json" };
import { parseAgeGroups, type PoolQuestion } from "../../app/client/src/engine/pool.ts";
import { PER_LEVEL, available, supply } from "../../app/client/src/engine/selection.ts";

interface Input {
  questions: (Pick<PoolQuestion, "id" | "status" | "difficulty"> & { bundle?: string })[];
  burned: string[];
  age_group?: string;
  bundles?: string[];
}

const groups = parseAgeGroups(ageGroups);

function run({ questions, burned, age_group = "young_teens", bundles }: Input) {
  const group = groups.find((g) => g.id === age_group);
  if (!group) throw new Error(`unknown age group ${age_group}`);
  const active = new Set(bundles ?? questions.map((q) => q.bundle ?? "base"));
  return {
    per_level: PER_LEVEL,
    ranges: Object.fromEntries(group.levels.map((r, i) => [i + 1, r])),
    supply: supply(available(questions, burned, [], active), group.levels),
  };
}

let raw = "";
for await (const chunk of stdin) raw += chunk;
const input = JSON.parse(raw) as Input | Input[];
console.log(JSON.stringify(Array.isArray(input) ? input.map(run) : run(input)));
