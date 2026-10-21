import { test } from "node:test";
import assert from "node:assert/strict";
import { choice, gameAction } from "./api.ts";
import * as game from "./game.ts";
import { seededRng } from "./rng.ts";
import { inRange } from "./selection.ts";
import { emptySave, engineData, type EngineData, type GameState, type SaveData } from "./state.ts";
import { realAgeGroups, realBundles, realCategories, realPool } from "./test/fixtures.ts";

const NOW = "2026-10-11T00:00:00Z";
const io = (seed: number) => ({ rng: seededRng(seed), now: NOW });

const data: EngineData = engineData(realPool(), realCategories(), realBundles(), realAgeGroups());
const stateOf = (save: SaveData): GameState => save.games.at(-1)!.state;

/** Play one game to the end with correct answers, each joker once where available; checks every card. */
function playOut(save: SaveData, seed: number, check: (s: GameState, eased: Set<string>, save: SaveData) => void): SaveData {
  const used = new Set<string>();
  const eased = new Set<string>();
  for (let step = 0; step < 200; step++) {
    const s = stateOf(save);
    check(s, eased, save);
    if (s.phase === "won" || s.phase === "lost") return save;
    const r = io(seed * 1000 + step);
    if (s.phase === "select") {
      save = game.pick(save, data, r, 0).save;
      continue;
    }
    const view = game.view(save, data, r)!;
    const j = view.jokers!;
    const q = data.byId.get(s.current!)!;
    const correct = s.answers.indexOf(q.answer);
    const tryJoker = (name: string, args = {}) => {
      save = game.joker(save, data, r, name, args).save;
      used.add(name);
    };
    if (!used.has("hint") && j.hint.available) tryJoker("hint");
    else if (!used.has("snipe") && j.snipe.available)
      tryJoker("snipe", { index: s.answers.findIndex((_, i) => i !== correct && !s.struck.includes(i)) });
    else if (!used.has("easier") && j.easier.available) {
      tryJoker("easier");
      eased.add(stateOf(save).current!);
    } else if (!used.has("category") && j.category.available) {
      const sub = j.category.categories.flatMap((c) => c.subcategories).find((x) => x.available)!;
      tryJoker("category", { subcategory: sub.key });
    } else if (!used.has("skip") && j.skip.available) tryJoker("skip");
    else save = game.answer(save, data, r, correct).save;
  }
  throw new Error("game didn't end");
}

// Bájale's card is only "easier", not bounded by the range (09).
const inWindow = (group: string) => (s: GameState, eased: Set<string>) => {
  const ranges = data.groupById.get(group)!.levels;
  for (const id of s.options.filter((i) => !eased.has(i)))
    assert.ok(inRange(data.byId.get(id)!, s.level, ranges), `${group}: ${id} out of range at level ${s.level}`);
};

for (const group of data.ageGroups) {
  test(`a ${group.id} game plays to won, every card in the group's range`, () => {
    let save = game.newGame(emptySave(), data, io(1), "ana", { age_group: group.id, bundles: ["base", "colombia"] }).save;
    assert.deepEqual(
      { age_group: stateOf(save).settings.age_group, bundles: stateOf(save).settings.bundles },
      { age_group: group.id, bundles: ["base", "colombia"] });
    save = playOut(save, 7, inWindow(group.id));
    assert.equal(stateOf(save).phase, "won");
    const jokers = stateOf(save).history.flatMap((h) => h.jokers ?? []);
    for (const name of ["hint", "snipe", "easier", "category", "skip"]) assert.ok(jokers.includes(name as never), `${group.id}: ${name} never played`);
  });
}

test("colombia off: no colombia question or Cambiazo group", () => {
  let save = game.newGame(emptySave(), data, io(2), "ana", { bundles: ["base"] }).save;
  assert.deepEqual(stateOf(save).settings.bundles, ["base"]);
  let views = 0;
  assert.ok(data.categories.some((c) => c.bundle === "colombia"));
  save = playOut(save, 3, (s, _eased, cur) => {
    for (const id of [...s.offered, ...s.history.map((h) => h.question_id)])
      assert.equal(data.byId.get(id)!.bundle ?? "base", "base", id);
    if (s.phase === "question") {
      const j = game.view(cur, data, io(0))?.jokers;
      if (j) {
        views++;
        const base = data.categories.filter((c) => c.bundle === "base").map((c) => c.slug);
        assert.deepEqual(j.category.categories.map((c) => c.slug), base);
      }
    }
  });
  assert.ok(views > 0);
});

const enData = engineData(data.pool, data.categories, data.bundles, data.ageGroups, "en");
const twoBases = engineData(data.pool, data.categories,
  [...data.bundles, { id: "base2", kind: "base", languages: ["es"], name: "B2", description: "" }], data.ageGroups);

test("bundles are normalized: bundles.json order, no duplicates, nothing added", () => {
  assert.deepEqual(game.resolveChoice(data, { bundles: ["colombia", "base", "colombia"] }).bundles, ["base", "colombia"]);
  assert.deepEqual(game.resolveChoice(twoBases, { bundles: ["base2"] }).bundles, ["base2"]);
});

const others = (d: typeof data) => d.bundles.filter((b) => b.kind !== "base" && b.languages.includes(d.locale)).map((b) => b.id);

test("defaults per locale: the first base bundle and the locale's other bundles", () => {
  assert.deepEqual(game.defaultChoice(data).bundles, ["base", ...others(data)]);
  assert.deepEqual(game.defaultChoice(enData).bundles, ["base", "usa", "uk"]);
  assert.deepEqual(game.defaultChoice(twoBases).bundles, ["base", ...others(data)]);
});

test("an empty selection or a bundle not offered → 409, save unchanged; base off is fine", () => {
  assert.deepEqual(game.resolveChoice(data, { bundles: ["colombia"] }).bundles, ["colombia"]);
  assert.deepEqual(game.resolveChoice(twoBases, { bundles: ["base", "base2"] }).bundles, ["base", "base2"]);
  const save = game.newGame(emptySave(), data, io(11), "ana").save;
  for (const [d, bundles, code] of [
    [data, [], "no_questions"],
    [enData, ["base", "colombia"], "bundle_not_offered"],
  ] as const) {
    const at = { ...save, language: d.locale };
    const r = gameAction(at, d, io(12), "new", { player: "bea", bundles });
    assert.equal(r.status, 409, `${bundles}`);
    assert.equal((r.body as { error: string }).error, code);
    assert.equal(r.save, at);
  }
});

test("stored bundles that don't resolve play with the defaults, never written back", () => {
  let save = game.newGame(emptySave(), data, io(13), "ana", { bundles: ["base"] }).save;
  stateOf(save).settings.bundles = ["colombia", "mars"];
  assert.deepEqual(game.gameChoice(stateOf(save), data).bundles, ["base", ...others(data)]);
  save = game.pick(save, data, io(14), 0).save;
  assert.equal(stateOf(save).phase, "question");
  assert.deepEqual(stateOf(save).settings.bundles, ["colombia", "mars"]);
});

test("unknown group or bundle → 409, save unchanged", () => {
  const save = game.newGame(emptySave(), data, io(4), "ana").save;
  for (const [args, code] of [
    [{ age_group: "babies" }, "age_group_unknown"],
    [{ age_group: 3 }, "age_group_unknown"],
    [{ bundles: ["mars"] }, "bundle_unknown"],
    [{ bundles: "colombia" }, "bundles_not_list"],
  ] as const) {
    const r = gameAction(save, data, io(5), "new", { player: "bea", ...args });
    assert.equal(r.status, 409);
    assert.equal((r.body as { error: string }).error, code);
    assert.equal(r.save, save);
    assert.equal(choice(save, data, { ...args }).status, 409);
  }
});

test("a state without the new keys draws like the explicit default", () => {
  const plain = game.newGame(emptySave(), data, io(6), "ana").save;
  const explicit = game.newGame(emptySave(), data, io(6), "ana", game.defaultChoice(data)).save;
  assert.equal(stateOf(plain).settings.age_group, undefined);
  assert.deepEqual(stateOf(plain).options, stateOf(explicit).options);
  const a = playOut(plain, 8, () => {});
  const b = playOut(explicit, 8, () => {});
  assert.deepEqual(stateOf(a).history, stateOf(b).history);
});

test("choice route: preset from the player's newest game, defaults otherwise, supply per choice", () => {
  let save = game.newGame(emptySave(), data, io(9), "ana", { age_group: "kids", bundles: ["base"] }).save;
  const r = choice(save, data, { player: "ana" });
  assert.equal(r.status, 200);
  const body = r.body as { choice: unknown; supply: { levels: { range: number[] }[] } };
  const kids = { ...game.defaultChoice(data), age_group: "kids", bundles: ["base"], jokers: game.UNLIMITED };
  assert.deepEqual(body.choice, kids);
  assert.deepEqual(body.supply.levels.map((l) => l.range), data.groupById.get("kids")!.levels);
  assert.deepEqual(choice(save, data, { player: "bea" }).body, {
    choice: { ...game.defaultChoice(data), bundles: ["base"] }, supply: game.supply(save, data, { ...game.defaultChoice(data), bundles: ["base"] }),
  });
  const adults = choice(save, data, { player: "ana", age_group: "adults" }).body as { choice: unknown };
  assert.deepEqual(adults.choice, { ...kids, age_group: "adults" });
  save = game.newGame(save, data, io(10), "ana").save;
  assert.deepEqual((choice(save, data, { player: "ana" }).body as { choice: unknown }).choice,
    { ...game.defaultChoice(data), jokers: game.UNLIMITED });
  save = game.newGame(save, data, io(15), "ana", { age_group: "kids", bundles: ["base", "colombia"] }).save;
  assert.deepEqual((choice(save, enData, { player: "ana" }).body as { choice: unknown }).choice,
    { ...game.defaultChoice(enData), age_group: "kids", jokers: game.UNLIMITED });
});
