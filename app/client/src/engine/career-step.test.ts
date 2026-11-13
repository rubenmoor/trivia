// The career's catch-up step (plan 195): per mode, backfill, demo, gamemaster, deleted players.
import { test } from "node:test";
import assert from "node:assert/strict";
import type { Category } from "../lib/types.ts";
import { deletePlayer, gameAction } from "./api.ts";
import { catchUp, emptyCareer, rankMean, rankSteps, scoreStep } from "./career.ts";
import { STANDARD_JOKERS } from "./choice.ts";
import type { PoolQuestion } from "./pool.ts";
import { actionRng } from "./rng.ts";
import { parseSave } from "./save.ts";
import { emptySave, engineData, type GameRow, type GameState, type SaveData, type Seat } from "./state.ts";
import { realAgeGroups, realBundles, realCategories, realPool } from "./test/fixtures.ts";

const categories: Category[] = [
  { slug: "past", name: "Pasado", bundle: "base", subject: "history", subcategories: ["roma"] },
  { slug: "misc", name: "Varios", bundle: "base", subcategories: ["otros"] },
];
const q = (id: string, difficulty: number, subcategory = "roma"): PoolQuestion => ({
  id, status: "approved", difficulty, subcategory, bundle: "base", description: "", question: "", answer: "a",
  wrong_answers: ["b", "c", "d"], hints: [], fun_fact: "", media: null as never, background: null,
});
const data = engineData([q("d2", 2), q("d5", 5), q("d9", 9), q("misc", 3, "otros")], categories, realBundles(), realAgeGroups());
const ON = "2026-11-01T20:00:00";

type Entry = GameState["history"][number];
function state(history: Entry[], settings: Partial<GameState["settings"]> = {}, phase: GameState["phase"] = "lost"): GameState {
  return {
    level: 12, phase, options: [], offered: [], current: null, answers: [], history, last: null, undo: null,
    purged: [], hints_shown: 0, struck: [], jokers: [], swapped_to: null, repeat: false,
    settings: { jokers: STANDARD_JOKERS, mode: "solo", age_group: "kids", ...settings },
  } as GameState;
}
const row = (id: number, s: GameState, result: GameRow["result"], extra: Partial<GameRow> = {}): GameRow =>
  ({ id, started_on: ON, finished_on: result ? ON : null, result, player_id: 1, state: s, ...extra });
const players = (n: number) => Array.from({ length: n }, (_, i) => ({ id: i + 1, name: `P${i + 1}`, created_on: ON }));
const saveOf = (games: GameRow[], n = 3): SaveData => ({ ...emptySave(), players: players(n), games });
const career = (save: SaveData, id: number) => save.players.find((p) => p.id === id)!.career;

const right = (question_id: string, level = 1, seat?: number): Entry => ({ level, question_id, correct: true, jokers: [], ...(seat === undefined ? {} : { seat }) });
const wrong = (question_id: string, level = 1, seat?: number): Entry => ({ ...right(question_id, level, seat), correct: false });

test("solo: right +d², wrong −1, subject bands, jokers and missing questions count nothing; the end once", () => {
  const history = [
    right("d5"), { level: 2, question_id: "d2", outcome: "skipped", jokers: ["skip"] } as Entry, right("misc", 2), right("gone", 3), wrong("d9", 4),
  ];
  const save = catchUp(saveOf([row(1, state(history), "lost")]), data, null);
  assert.deepEqual(career(save, 1), { ...emptyCareer(), score: 25 + 9 - 1, right: { history: [1, 1, 0, 0] }, years: { kids: 1 }, ranks: [5] });
  assert.deepEqual(save.games[0].career, { cursor: [5], ended: true });
  assert.equal(career(save, 2), undefined);
  assert.equal(catchUp(save, data, null), save, "a second step changes nothing");
});

test("solo, step by step: only new entries count; a running game has no end yet", () => {
  let save = catchUp(saveOf([row(1, state([right("d5")], {}, "select"), null)]), data, "2026-11-02T10:00:00");
  assert.equal(career(save, 1)!.score, 25);
  save.games[0] = { ...save.games[0], state: state([right("d5"), right("d9", 2)]), result: "lost", finished_on: ON };
  save = catchUp(save, data, "2026-11-02T10:05:00");
  assert.equal(career(save, 1)!.score, 25 + 81);
  assert.deepEqual(career(save, 1)!.ranks, [9]);
  assert.deepEqual(career(save, 1)!.badges, { CAREER_SCORE_100: { on: "2026-11-02T10:05:00" } });
});

test("rr-coop: the answering seat earns; a team win gives every seat the window top", () => {
  const seats: Seat[] = [{ player_id: 1 }, { player_id: 2 }, { player_id: 3 }];
  const s = state([right("d5", 1, 0), wrong("d2", 2, 1), right("d2", 12, 2)], { mode: "rr-coop" }, "won");
  const save = catchUp(saveOf([row(1, s, "won", { player_id: null, seats, turn: 0 })]), data);
  assert.equal(career(save, 1)!.score, 25);
  assert.equal(career(save, 2)!.score, -1);
  assert.equal(career(save, 3)!.score, 4);
  for (const id of [1, 2, 3]) assert.deepEqual([career(save, id)!.ranks, career(save, id)!.years], [[6], { kids: 1 }]);
});

test("rr-competitive: each seat's own game; only a tower win ranks as the window top", () => {
  const own = (h: Entry[], phase: GameState["phase"], age = "kids") => state(h, { mode: "rr-competitive", age_group: age }, phase);
  const seats: Seat[] = [
    { player_id: 1, state: own([right("d5", 1), wrong("d2", 2)], "lost"), out: true, result: "lost" },
    { player_id: 2, state: own([right("d2", 1), right("d9", 12)], "won", "adults"), result: "won" },
  ];
  const save = catchUp(saveOf([row(1, state([], { mode: "rr-competitive" }, "won"), "won", { player_id: null, seats, turn: 0 })]), data);
  assert.deepEqual([career(save, 1)!.score, career(save, 1)!.ranks, career(save, 1)!.years], [24, [5], { kids: 1 }]);
  assert.deepEqual([career(save, 2)!.score, career(save, 2)!.ranks, career(save, 2)!.years], [85, [15], { adults: 1 }]);
  assert.deepEqual(save.games[0].career, { cursor: [0, 2, 2], ended: true });
});

test("rr-competitive: a last-standing win ranks by its hardest right answer", () => {
  const own = (h: Entry[], phase: GameState["phase"]) => state(h, { mode: "rr-competitive" }, phase);
  const seats: Seat[] = [
    { player_id: 1, state: own([wrong("d2", 1)], "lost"), out: true, result: "lost" },
    { player_id: 2, state: own([right("d5", 1)], "won"), result: "won" },
  ];
  const save = catchUp(saveOf([row(1, state([], { mode: "rr-competitive" }, "won"), "won", { player_id: null, seats, turn: 0 })]), data);
  assert.deepEqual([career(save, 1)!.ranks, career(save, 2)!.ranks], [[0], [5]]);
});

test("timed: unclaimed answers and a deleted player's seat count for nobody", () => {
  const seats: Seat[] = [{ player_id: 1, result: "lost", out: true }, { player_id: null, result: "won" }, { player_id: 2, result: "lost", out: true }];
  const s = state([
    right("d5", 1, 0), { level: 1, question_id: "d2", chosen: null, unclaimed: true, jokers: [] } as Entry, right("d9", 2, 1),
    { ...wrong("d2", 3, 2), timeout: true }, wrong("d2", 3, 0),
  ], { mode: "timed", cards: 0 }, "won");
  const save = catchUp(saveOf([row(1, s, "won", { player_id: null, seats })]), data);
  assert.deepEqual([career(save, 1)!.score, career(save, 1)!.ranks], [24, [5]]);
  assert.deepEqual([career(save, 2)!.score, career(save, 2)!.ranks], [-1, [0]]);
  assert.equal(career(save, 3), undefined);
});

test("deleting a player: their career goes, the session's counted answers stay counted, nobody else gains", () => {
  const seats: Seat[] = [{ player_id: 1 }, { player_id: 2 }];
  const s = state([right("d5", 1, 0), right("d2", 2, 1), { ...right("d2", 3, 0) }], { mode: "rr-coop" }, "select");
  let save = catchUp(saveOf([row(1, { ...s, history: s.history.slice(0, 2) }, null, { player_id: null, seats, turn: 0 })], 2), data);
  save.games[0] = { ...save.games[0], state: s };
  const kept = career(save, 2);
  save = deletePlayer(save, { name: "P1" }, { rng: actionRng(data), now: ON }).save;
  save = catchUp(save, data, ON);
  assert.deepEqual(save.players.map((p) => p.id), [2]);
  assert.deepEqual(career(save, 2), kept);
  assert.deepEqual(save.games[0].career, { cursor: [3] });
});

test("demo rows, gamemaster and non-qualifying games count nothing; the cursor moves to the end", () => {
  const games = [
    row(1, state([right("d9")]), "lost", { demo: true }),
    row(2, state([right("d9")], { mode: "gamemaster" }), "lost"),
    row(3, state([right("d9")], { customized: true }), "lost"),
    row(4, state([right("d9")], { mode: "solo" }, "won"), "abandoned"),
  ];
  const save = catchUp(saveOf(games), data);
  assert.equal(career(save, 1)?.score ?? 0, 81, "only the abandoned solo game's answer");
  assert.deepEqual(career(save, 1)!.years, {}, "an abandoned game has no end");
  assert.deepEqual(save.games.map((g) => g.career), [{ cursor: [1], ended: true }, { cursor: [1], ended: true }, { cursor: [1], ended: true }, { cursor: [1] }]);
  const demo = engineData(data.pool, categories, realBundles(), realAgeGroups(), "es", undefined, null, true);
  const before = saveOf([row(1, state([right("d9")]), "lost")]);
  assert.equal(catchUp(before, demo), before, "the demo build counts nothing");
});

test("rows of another locale wait for their own pool", () => {
  const save = saveOf([row(1, state([right("d5")]), "lost", { locale: "en" })]);
  assert.equal(catchUp(save, data), save);
});

test("a v5 save is backfilled once; badges dated by the game", () => {
  const v5 = {
    version: 5, players: players(1), seen: [], blocked: [], notified_exhausted: [], flags: {},
    games: [
      { ...row(1, state(Array.from({ length: 4 }, () => right("d5")), {}, "won"), "won"), finished_on: "2026-10-01T21:00:00" },
      { ...row(2, state([right("d2")], {}, "select"), null), started_on: "2026-10-02T21:00:00" },
    ],
  };
  const save = catchUp(parseSave(JSON.stringify(v5)), data);
  assert.equal(save.version, 6);
  assert.equal(career(save, 1)!.score, 104);
  assert.deepEqual(career(save, 1)!.badges, { CAREER_SCORE_100: { on: "2026-10-01T21:00:00" } });
  assert.deepEqual(career(save, 1)!.ranks, [6], "a solo win: the kids' window top");
  const again = catchUp(parseSave(JSON.stringify(save)), data);
  assert.deepEqual(again, parseSave(JSON.stringify(save)));
});

test("engine actions run the step: a real solo game counts as it goes", () => {
  const real = engineData(realPool(), realCategories(), realBundles(), realAgeGroups());
  const io = (n: number) => ({ rng: actionRng(real), now: `2026-11-03T20:00:0${n}` });
  const act = (save: SaveData, n: number, action: string, body: Record<string, unknown> = {}) => {
    const r = gameAction(save, real, io(n), action, body);
    assert.equal(r.status, 200, `${action}: ${JSON.stringify(r.body)}`);
    return r.save;
  };
  let save = act(emptySave(), 0, "new", { player: "Ana", mode: "solo", bundles: ["base"], age_group: "adults" });
  save = act(save, 1, "pick", { index: 0 });
  const cur = () => real.byId.get(save.games[0].state.current!)!;
  const d = cur().difficulty;
  save = act(save, 2, "answer", { index: save.games[0].state.answers.indexOf(cur().answer) });
  assert.equal(save.players[0].career!.score, d * d);
  assert.deepEqual(save.games[0].career, { cursor: [1] });
  save = act(save, 3, "pick", { index: 0 });
  save = act(save, 4, "answer", { index: save.games[0].state.answers.findIndex((a) => a !== cur().answer) });
  assert.equal(save.players[0].career!.score, d * d - 1);
  assert.deepEqual(save.players[0].career!.years, { adults: 1 });
  assert.deepEqual(save.games[0].career, { cursor: [2], ended: true });
});

test("scoreStep: the answering player's score and delta; nothing for reveals, career off, gamemaster, demo, unclaimed", () => {
  const solo = catchUp(saveOf([row(1, state([right("d5"), wrong("d9", 2)], {}, "select"), null)]), data, ON);
  const last = { question_id: "d9", correct: false };
  assert.deepEqual(scoreStep(solo, data, last), { name: "P1", score: 24, delta: -1 });
  assert.deepEqual(scoreStep(solo, data, { question_id: "d5", correct: true }), { name: "P1", score: 24, delta: 25 });
  assert.equal(scoreStep(solo, data, { ...last, revealed: true }), null);
  assert.equal(scoreStep(solo, data, null), null);
  assert.equal(scoreStep(solo, { ...data, demo: true }, last), null);
  const off = { ...solo, players: solo.players.map((p) => (p.id === 1 ? { ...p, career: { ...p.career!, off: true as const } } : p)) };
  assert.equal(scoreStep(off, data, last), null);
  const gm = catchUp(saveOf([row(1, state([right("d5")], { mode: "gamemaster" }, "select"), null)]), data, ON);
  assert.equal(scoreStep(gm, data, last), null);
  const seats: Seat[] = [{ player_id: 1 }, { player_id: 2 }];
  const timed = catchUp(saveOf([row(1, state([right("d5", 1, 1)], { mode: "timed", cards: 0 }, "select"), null, { seats, turn: 0 })]), data, ON);
  assert.deepEqual(scoreStep(timed, data, { question_id: "d5", correct: true, seat: 1 }), { name: "P2", score: 25, delta: 25 });
  assert.equal(scoreStep(timed, data, { question_id: "d5", correct: true }), null, "unclaimed: nobody");
});

test("rankSteps: every seat with a player at a finished, counted game; nothing for running games, career off, gamemaster, demo", () => {
  const seats: Seat[] = [{ player_id: 1 }, { player_id: 2 }, { player_id: null }];
  const coop = (result: GameRow["result"]) => saveOf([row(1, state([right("d5", 1, 0), wrong("d2", 2, 1)], { mode: "rr-coop" }, result ? "lost" : "select"), result, { player_id: null, seats, turn: 0 })]);
  const withPast = (save: SaveData) => ({ ...save, players: save.players.map((p) => (p.id === 1 ? { ...p, career: { ...emptyCareer(), ranks: [3, 4] } } : p)) });
  const ended = catchUp(withPast(coop("lost")), data, ON);
  assert.deepEqual(rankSteps(ended, data), [
    { name: "P1", from: rankMean([3, 4]), to: rankMean([3, 4, 5]) },
    { name: "P2", from: null, to: 0 },
  ]);
  assert.deepEqual(rankSteps(catchUp(withPast(coop(null)), data, ON), data), [], "running");
  assert.deepEqual(rankSteps(withPast(coop("lost")), data), [], "not counted yet");
  assert.deepEqual(rankSteps(ended, { ...data, demo: true }), []);
  const off = { ...ended, players: ended.players.map((p) => (p.id === 1 ? { ...p, career: { ...p.career!, off: true as const } } : p)) };
  assert.deepEqual(rankSteps(off, data).map((s) => s.name), ["P2"]);
  const gm = catchUp(saveOf([row(1, state([right("d5")], { mode: "gamemaster" }), "lost")]), data, ON);
  assert.deepEqual(rankSteps(gm, data), []);
  assert.equal(rankMean([]), null);
  assert.equal(rankMean([5, 10]), (9 * 5 + 10 * 10) / 19);
});
