// The career's ops and reads (plan 195): opt-out, shown marks, player view, Steam's union.
import { test } from "node:test";
import assert from "node:assert/strict";
import { careerShown, deletePlayer, getCareers, setCareer } from "./api.ts";
import { type CareerView, careerUnlocks, catchUp, emptyCareer, type PlayerCareer } from "./career.ts";
import { STANDARD_JOKERS } from "./choice.ts";
import type { PoolQuestion } from "./pool.ts";
import { actionRng } from "./rng.ts";
import { emptySave, engineData, type GameRow, type GameState, type SaveData } from "./state.ts";
import { realAgeGroups, realBundles } from "./test/fixtures.ts";

const ON = "2026-11-01T20:00:00";
const q = (id: string, difficulty: number): PoolQuestion => ({
  id, status: "approved", difficulty, subcategory: "roma", bundle: "base", description: "", question: "", answer: "a",
  wrong_answers: ["b", "c", "d"], hints: [], fun_fact: "", media: null as never, background: null,
});
const data = engineData([q("d10", 10)], [{ slug: "past", name: "Pasado", bundle: "base", subject: "history", subcategories: ["roma"] }], realBundles(), realAgeGroups());

const game = (id: number, pid: number, n: number): GameRow => ({
  id, started_on: ON, finished_on: ON, result: "lost", player_id: pid,
  state: {
    level: 12, phase: "lost", options: [], offered: [], current: null, answers: [], last: null, undo: null, purged: [], hints_shown: 0,
    struck: [], jokers: [], swapped_to: null, repeat: false, settings: { jokers: STANDARD_JOKERS, mode: "solo", age_group: "kids" },
    history: Array.from({ length: n }, () => ({ level: 1, question_id: "d10", correct: true, jokers: [] })),
  } as unknown as GameState,
});
const base = (): SaveData => ({ ...emptySave(), players: [1, 2].map((id) => ({ id, name: `P${id}`, created_on: ON })) });
const career = (s: SaveData, id: number) => s.players.find((p) => p.id === id)!.career as PlayerCareer;
const io = { rng: actionRng(data), now: ON };

test("off → games still count → on: nothing lost, badges stay not shown", () => {
  let save = setCareer(base(), { name: "P1", off: true }).save;
  assert.equal(career(save, 1).off, true);
  save = catchUp({ ...save, games: [game(1, 1, 1)] }, data, ON);
  assert.equal(career(save, 1).score, 100);
  assert.deepEqual(Object.keys(career(save, 1).badges), ["CAREER_SCORE_100"]);
  const view = (getCareers(save).body as Record<string, CareerView>).P1;
  assert.deepEqual([view.off, view.score, view.rank, view.rank_index, view.badges], [true, 100, 10, 9, [{ name: "CAREER_SCORE_100", on: ON, shown: false }]]);
  save = setCareer(save, { name: "p1", off: false }).save;
  assert.equal(career(save, 1).off, undefined);
  assert.equal(career(save, 1).score, 100);
  assert.equal(career(save, 1).badges.CAREER_SCORE_100.shown, undefined, "turning on celebrates nothing by itself");
});

test("career_shown marks held badges only", () => {
  let save = catchUp({ ...base(), games: [game(1, 1, 1)] }, data, ON);
  save = careerShown(save, { name: "P1", badges: ["CAREER_SCORE_100", "CAREER_SCORE_250", 7] }).save;
  assert.deepEqual(career(save, 1).badges, { CAREER_SCORE_100: { on: ON, shown: true } });
  const res = careerShown(save, { name: "nobody", badges: [] });
  assert.equal(res.status, 409);
});

test("careerUnlocks: union of players with the career on, live order", () => {
  const save = base();
  save.players[0].career = { ...emptyCareer(), badges: { CAREER_SCORE_250: { on: ON } } };
  save.players[1].career = { ...emptyCareer(), badges: { CAREER_SCORE_100: { on: ON }, CAREER_SCORE_250: { on: ON } } };
  assert.deepEqual(careerUnlocks(save), ["CAREER_SCORE_100", "CAREER_SCORE_250"]);
  save.players[1].career!.off = true;
  assert.deepEqual(careerUnlocks(save), ["CAREER_SCORE_250"]);
});

test("deleting a player removes only their career", () => {
  const save = catchUp({ ...base(), games: [game(1, 1, 1), game(2, 2, 1)] }, data, ON);
  const out = deletePlayer(save, { name: "P1" }, io).save;
  assert.deepEqual(out.players.map((p) => p.id), [2]);
  assert.deepEqual(out.players[0].career, career(save, 2));
});
