// Configure settings (decision 33) and gamemaster cheats (decision 34): newer than the frozen fixtures.
import { test } from "node:test";
import assert from "node:assert/strict";
import { gameAction } from "./api.ts";
import { rangesFor } from "./choice.ts";
import { view } from "./game.ts";
import type { AgeGroup, Bundle, PoolQuestion } from "./pool.ts";
import { seededRng } from "./rng.ts";
import { inRange } from "./selection.ts";
import { emptySave, engineData, type GameState, type SaveData } from "./state.ts";

// 12 questions per difficulty 1–15 over 3 broad categories; j 0 is a video, j 1 an audio question.
const subs = ["a1", "a2", "b1", "b2", "c1", "c2"];
const pool = Array.from({ length: 15 }, (_, d) => d + 1).flatMap((d) => Array.from({ length: 12 }, (_, j) => ({
  id: `q${d}-${j}`, status: "approved", difficulty: d, subcategory: subs[j % 6], bundle: "base", description: "", question: "",
  answer: "R", wrong_answers: ["W1", "W2", "W3"], hints: ["h"], fun_fact: "",
  media: j === 0 ? { type: "video" } : j === 1 ? { type: "audio" } : null, background: null,
}) as unknown as PoolQuestion));
const group = { id: "young_teens", name: "G", ages: [0, null], window: [1, 12], level_weights: {},
  levels: Array.from({ length: 12 }, (_, i) => [i + 1, i + 1] as const) } as AgeGroup;
const bundle: Bundle = { id: "base", kind: "base", languages: ["es"], name: "B", description: "" };
const data = engineData(pool, ["a", "b", "c"].map((c) => ({ slug: c, name: c, bundle: "base", subcategories: [`${c}1`, `${c}2`] })),
  [bundle], [group]);

const io = { rng: seededRng(1), now: "2026-01-01T00:00:00" };
const stateOf = (save: SaveData): GameState => save.games.at(-1)!.state;
const q = (id: string | null) => data.byId.get(id!)!;
const right = (s: GameState) => s.answers.indexOf(q(s.current).answer);

/** An action that must succeed. */
function ok(save: SaveData, action: string, body: Record<string, unknown> = {}): SaveData {
  const r = gameAction(save, data, io, action, body);
  assert.equal(r.status, 200, `${action}: ${JSON.stringify(r.body)}`);
  return r.save;
}

/** An action refused with `code`, the save unchanged. */
function refused(save: SaveData, action: string, body: Record<string, unknown>, code: string): void {
  const r = gameAction(save, data, io, action, body);
  assert.deepEqual([r.status, (r.body as { error: string }).error], [409, code], `${action} ${JSON.stringify(body)}`);
  assert.equal(r.save, save);
}

const start = (body: Record<string, unknown> = {}) => ok(emptySave(), "new", { player: "Ana", ...body });

/** Answer every question right (picking card 0) to the end; checks each table against the game's ranges. */
function playOut(save: SaveData, check: (s: GameState) => void = () => {}): SaveData {
  for (let s = stateOf(save); s.phase !== "won"; s = stateOf(save)) {
    check(s);
    save = s.phase === "select" ? ok(save, "pick", { index: 0 }) : ok(save, "answer", { index: right(s) });
  }
  return save;
}

const cardsInRange = (body: Record<string, unknown>) => (s: GameState) => {
  const ranges = rangesFor(data, { age_group: "young_teens", difficulty: null, levels: 12, ...body });
  for (const id of s.options) assert.ok(inRange(q(id), s.level, ranges), `${id} at level ${s.level}`);
};

test("levels 1: the first right answer wins; levels 20 step the 12 ranges", () => {
  const one = ok(start({ levels: 1 }), "pick", { index: 0 });
  assert.equal(ok(one, "answer", { index: right(stateOf(one)) }).games[0].result, "won");
  assert.deepEqual(rangesFor(data, { age_group: "young_teens", difficulty: null, levels: 20 }).map(([lo]) => lo),
    Array.from({ length: 20 }, (_, i) => Math.round(1 + (11 * i) / 19)));
  const won = playOut(start({ levels: 20 }), cardsInRange({ levels: 20 }));
  assert.equal(stateOf(won).history.length, 20);
});

test("custom difficulty ramps, cards 1–4 per table, video/audio off offers no such question", () => {
  const difficulty = { start: 3, end: 9 };
  for (const cards of [1, 2, 3, 4]) {
    const save = playOut(start({ difficulty, cards, video: false, audio: false }), (s) => {
      cardsInRange({ difficulty })(s);
      if (s.phase === "select") assert.equal(s.options.length, cards);
    });
    assert.ok(stateOf(save).offered.every((id) => q(id).media === null), `cards ${cards}`);
  }
});

test("cards 0: the question opens at once after deal, refill and snipe", () => {
  let save = start({ cards: 0 });
  assert.equal(stateOf(save).phase, "question");
  save = ok(save, "answer", { index: right(stateOf(save)) });
  assert.deepEqual([stateOf(save).level, stateOf(save).phase], [2, "question"]);
  save = ok(save, "skip");
  assert.equal(stateOf(save).phase, "question");
  save = ok(save, "joker", { joker: "snipe", index: right(stateOf(save)) });
  assert.deepEqual([stateOf(save).phase, stateOf(save).repeat], ["question", true]);
});

test("jokers: null never runs out, a number does", () => {
  let save = start({ jokers: { skip: null, easier: 1 } });
  save = ok(save, "pick", { index: 0 });
  for (let i = 0; i < 6; i++) save = ok(ok(save, "joker", { joker: "skip" }), "pick", { index: 0 });
  assert.equal(view(save, data, io)!.jokers_left.skip, null);
  save = ok(save, "answer", { index: right(stateOf(save)) });
  save = ok(ok(save, "pick", { index: 0 }), "joker", { joker: "easier" });
  refused(save, "joker", { joker: "easier" }, "joker_spent");
});

test("configure refusals → 409, save unchanged", () => {
  const save = start();
  for (const [body, code] of [
    [{ levels: 0 }, "levels_invalid"], [{ levels: 21 }, "levels_invalid"], [{ cards: 5 }, "cards_invalid"],
    [{ difficulty: { start: 5, end: 4 } }, "difficulty_invalid"],
  ] as const) refused(save, "new", { player: "Bea", ...body }, code);
});

test("cheats: replace, skip, block, level jump", () => {
  let save = ok(start(), "pick", { index: 0 });
  const first = stateOf(save).current!;
  save = ok(save, "replace");
  assert.notEqual(stateOf(save).current, first);
  assert.deepEqual([stateOf(save).history.at(-1)?.outcome, save.seen.length], ["admin_replace", 0]);
  const second = stateOf(save).current!;
  save = ok(save, "replace", { seen: true });
  assert.deepEqual(save.seen.map((s) => s.question_id), [second]);
  save = ok(ok(save, "skip"), "pick", { index: 0 });
  assert.equal(stateOf(save).history.at(-1)?.outcome, "admin_skip");
  const third = stateOf(save).current!;
  save = ok(save, "skip", { everyone: true });
  assert.deepEqual([stateOf(save).history.at(-1)?.outcome, save.blocked], ["admin_block", [third]]);
  for (const level of [0, 13]) refused(save, "level", { level }, "level_invalid");
  save = ok(save, "level", { level: 12 });
  assert.equal(stateOf(save).level, 12);
  cardsInRange({})(stateOf(save));
});

test("cheats: settings mid-game; a refusal keeps the game", () => {
  let save = ok(start(), "pick", { index: 0 });
  save = ok(save, "answer", { index: right(stateOf(save)) });
  save = ok(save, "settings", { difficulty: { start: 10, end: 14 } });
  const s = stateOf(save);
  assert.deepEqual([s.level, s.settings.difficulty, s.settings.age_group, s.history.length], [2, { start: 10, end: 14 }, undefined, 1]);
  cardsInRange({ difficulty: { start: 10, end: 14 } })(s);
  refused(save, "settings", { difficulty: { start: 15, end: 15 } }, "supply_short");
  refused(save, "settings", { bundles: [] }, "base_bundle_count");
  save = ok(save, "settings", { age_group: "young_teens" });
  assert.deepEqual([stateOf(save).settings.age_group, stateOf(save).settings.difficulty], ["young_teens", undefined]);
});

test("cheats: refused in the wrong phase and outside gamemaster mode", () => {
  const select = start();
  refused(select, "replace", {}, "no_question");
  refused(select, "skip", {}, "skip_not_question");
  const asked = ok(select, "pick", { index: 0 });
  refused(asked, "level", { level: 2 }, "cheat_not_select");
  refused(asked, "settings", { age_group: "young_teens" }, "cheat_not_select");
  let solo = ok(start({ mode: "solo" }), "pick", { index: 0 });
  for (const [action, body] of [["replace", {}], ["skip", {}], ["jokers", { jokers: { hint: 5 } }]] as const)
    refused(solo, action, body, "gamemaster_only");
  solo = ok(solo, "answer", { index: right(stateOf(solo)) });
  for (const [action, body] of [["level", { level: 3 }], ["settings", { age_group: "young_teens" }], ["undo", {}]] as const)
    refused(solo, action, body, "gamemaster_only");
});

test("undo after cheats: the state before the answer, the cheats' seen rows stay", () => {
  let save = ok(start(), "pick", { index: 0 });
  const before = structuredClone(stateOf(save));
  save = ok(save, "answer", { index: right(before) });
  save = ok(ok(save, "level", { level: 5 }), "pick", { index: 0 });
  const replaced = stateOf(save).current!;
  save = ok(save, "replace", { seen: true });
  save = ok(save, "undo");
  const s = stateOf(save);
  assert.deepEqual([s.level, s.phase, s.current, s.answers, s.offered], [1, "question", before.current, before.answers, before.offered]);
  assert.deepEqual(save.seen.map((r) => r.question_id), [replaced]);
});
