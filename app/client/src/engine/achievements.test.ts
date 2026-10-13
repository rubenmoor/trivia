import { test } from "node:test";
import assert from "node:assert/strict";
import type { Category } from "../lib/types.ts";
import { earned, inSteamworks, qualifies } from "./achievements.ts";
import { STANDARD_JOKERS } from "./choice.ts";
import type { PoolQuestion } from "./pool.ts";
import { emptySave, engineData, type GameRow, type GameState } from "./state.ts";
import { realAgeGroups, realBundles } from "./test/fixtures.ts";

const categories: Category[] = [
  { slug: "art", name: "Arte", bundle: "base", subcategories: ["Pintura"] },
  { slug: "geo", name: "Geografía", bundle: "base", subcategories: ["Ríos"] },
  { slug: "col", name: "Colombia", bundle: "colombia", subcategories: ["Comida"] },
];
const q = (id: string, subcategory: string, bundle = "base"): PoolQuestion => ({
  id, status: "approved", difficulty: 1, subcategory, bundle, description: "", question: "", answer: "a",
  wrong_answers: ["b", "c", "d"], hints: ["h1", "h2"], fun_fact: "", media: null as never, background: null,
});
const data = engineData([q("q-1", "Pintura"), q("q-2", "Ríos"), q("q-3", "Comida", "colombia")], categories, realBundles(), realAgeGroups());

let nextId = 1;
function row(result: GameRow["result"], history: GameState["history"], settings: Partial<GameState["settings"]> = {}, on = "2026-10-13T20:00:00"): GameRow {
  const state = {
    level: 12, phase: result ?? "question", options: [], offered: [], current: null, answers: [], history, last: null, undo: null,
    purged: [], hints_shown: 0, struck: [], jokers: [], swapped_to: null, repeat: false,
    settings: { jokers: STANDARD_JOKERS, mode: "solo", age_group: "kids", ...settings },
  } as GameState;
  return { id: nextId++, started_on: on, finished_on: result ? on : null, result, player_id: 1, state };
}
const win = (jokers: GameState["history"][number]["jokers"] = []) => [{ level: 12, question_id: "q-1", correct: true, jokers }];

test("only qualifying games earn", () => {
  const save = emptySave();
  save.games = [
    row("won", win(), { customized: true }),
    row("won", win(), { mode: "gamemaster" }),
    row("won", win(), { levels: 6 }),
    row("won", [{ level: 3, question_id: "q-2", outcome: "admin_replace", jokers: [] }, ...win()]),
  ];
  assert.ok(save.games.every((g) => !qualifies(g)));
  assert.deepEqual(earned(save, data), []);
});

test("wins, jokers and categories", () => {
  const save = emptySave();
  save.games = [
    row("won", win(["hint", "hint"]), {}, "2026-12-24T02:00:00"),
    row("lost", [
      { level: 4, question_id: "q-1", outcome: "skipped", jokers: ["skip"] },
      { level: 4, question_id: "q-2", outcome: "easier", jokers: ["easier"] },
      { level: 4, question_id: "q-2", correct: true, jokers: [] },
      { level: 5, question_id: "q-3", correct: false, jokers: [] },
    ]),
  ];
  const got = new Set(earned(save, data));
  for (const id of ["FIRST_WIN", "FIRST_SOPLO", "ALL_HINTS", "SOPLO_SAVE", "NIGHT_OWL", "CHRISTMAS", "FIRST_PASO", "FIRST_BAJALE", "SUPER_PICKY", "ALL_CATEGORIES"])
    assert.ok(got.has(id as never), id);
  for (const id of ["WIN_NO_JOKERS", "WIN_ADULTS", "PURGE", "BUNDLE_COLOMBIA"]) assert.ok(!got.has(id as never), id);
  assert.ok(!inSteamworks("WIN_TIMED") && !inSteamworks("BUNDLE_COLOMBIA") && inSteamworks("FIRST_WIN"));
});
