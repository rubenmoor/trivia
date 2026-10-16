import { test } from "node:test";
import assert from "node:assert/strict";
import type { Category } from "../lib/types.ts";
import { earned, inSteamworks, qualifies } from "./achievements.ts";
import { gameAction } from "./api.ts";
import { STANDARD_JOKERS } from "./choice.ts";
import { newSession } from "./game.ts";
import type { PoolQuestion } from "./pool.ts";
import { seededRng } from "./rng.ts";
import { emptySave, engineData, type GameRow, type GameState, type SaveData } from "./state.ts";
import { realAgeGroups, realBundles, realCategories, realPool } from "./test/fixtures.ts";

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

// sessions (decision 285): scripted through the engine
const real = engineData(realPool(), realCategories(), realBundles(), realAgeGroups());
const T0 = Date.parse("2026-10-16T00:00:00Z");
let step = 0;
const io = (ms: number) => ({ rng: seededRng(++step), now: "2026-10-16T20:00:00", ms });
const last = (save: SaveData) => save.games.at(-1)!;
/** `seat` answers its question on screen (picking the first card first): right or wrong. */
function play(save: SaveData, seat: number, ok: boolean, ms = T0): SaveData {
  const r = last(save);
  const state = r.seats![seat].state ?? r.state;
  const send = (action: string, body: Record<string, unknown>, at: number) => {
    const res = gameAction(save, real, io(at), action, { seat, ...body });
    assert.equal(res.status, 200, JSON.stringify(res.body));
    return (save = res.save);
  };
  if (r.state.settings.mode === "timed") send("claim", {}, ms);
  else if (state.phase === "select") send("pick", { index: 0 }, ms);
  const now = last(save).seats![seat].state ?? last(save).state;
  const right = now.answers.indexOf(real.byId.get(now.current!)!.answer);
  send("answer", { index: ok ? right : [0, 1, 2, 3].find((i) => i !== right)! }, ms + 1000);
  const t = last(save).state.timed;
  if (t?.shown_at === null && last(save).result === null) save = gameAction(save, real, io(ms + 1000), "show", {}).save;
  return save;
}
const session = (players: string[], args: Record<string, unknown>) =>
  gameAction(newSession(emptySave(), real, io(T0), players, { bundles: ["base"], ...args }).save, real, io(T0), "show", {}).save;
const WIN_BASED = ["FIRST_WIN", "WIN_ADULTS", "WIN_NO_JOKERS", "SOPLO_SAVE", "ALL_JOKERS_WIN", "POLYGLOT", "NIGHT_OWL"];
const has = (save: SaveData, ids: string[]) => {
  const got = new Set<string>(earned(save, real));
  return ids.filter((id) => got.has(id));
};

test("rr-coop: the team's win at the top level is a tower win", () => {
  let save = session(["Ana", "Beto"], { mode: "rr-coop", age_group: "adults" });
  while (last(save).result === null) save = play(save, last(save).turn!, true);
  assert.ok(qualifies(last(save)));
  assert.deepEqual(has(save, ["FIRST_WIN", "WIN_ADULTS", "WIN_NO_JOKERS", "WIN_RR_COOP"]), ["FIRST_WIN", "WIN_ADULTS", "WIN_NO_JOKERS", "WIN_RR_COOP"]);
});

test("rr-competitive: the winning seat's game counts; a last-standing win only the mode's", () => {
  let save = session(["Ana", "Beto"], { mode: "rr-competitive", age_group: "kids", age_groups: ["adults"] });
  save = play(save, 0, true);
  save = play(save, 1, false);
  assert.equal(last(save).result, "won");
  assert.deepEqual(has(save, [...WIN_BASED, "WIN_RR_COMPETITIVE"]), ["WIN_RR_COMPETITIVE"]);

  save = session(["Ana", "Beto"], { mode: "rr-competitive", age_group: "kids", age_groups: ["adults"] });
  while (last(save).result === null) save = play(save, last(save).turn!, true);
  assert.deepEqual(last(save).seats!.map((s) => s.result), ["won", "lost"]);
  assert.deepEqual(has(save, ["FIRST_WIN", "WIN_ADULTS", "WIN_NO_JOKERS", "WIN_RR_COMPETITIVE"]), ["FIRST_WIN", "WIN_ADULTS", "WIN_NO_JOKERS", "WIN_RR_COMPETITIVE"]);
});

test("timed: the sudden-death answer is a tower win; a drop-out win only the mode's", () => {
  let save = session(["Ana", "Beto", "Cami"], { mode: "timed", age_group: "adults" });
  assert.ok(qualifies(last(save)));
  save = play(save, 2, false, T0 + 1000);
  save = play(save, 0, false, T0 + 3000);
  assert.equal(last(save).result, "won");
  assert.deepEqual(has(save, [...WIN_BASED, "WIN_TIMED"]), ["WIN_TIMED"]);

  save = session(["Ana", "Beto"], { mode: "timed", age_group: "adults" });
  let ms = T0;
  while (last(save).result === null) save = play(save, last(save).state.timed!.round_done % 2, true, ms += 2000);
  assert.equal(last(save).state.history.at(-1)!.level, 12);
  assert.deepEqual(has(save, ["FIRST_WIN", "WIN_ADULTS", "WIN_NO_JOKERS", "WIN_TIMED"]), ["FIRST_WIN", "WIN_ADULTS", "WIN_TIMED"]);
});
