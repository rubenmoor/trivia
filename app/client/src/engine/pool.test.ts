import { test } from "node:test";
import assert from "node:assert/strict";
import type { Category } from "../lib/types.ts";
import {
  broadOf, byId, categoryOf, isModId, isOurs, loadCategories, modPool, parseAgeGroups, parseBundles, parsePool,
} from "./pool.ts";
import { data, fixture, realCategories } from "./test/fixtures.ts";

const subsOf = (cats: Category[], bundle: string) => cats.filter((c) => c.bundle === bundle).flatMap((c) => c.subcategories);

test("parsePool: version 1 only", () => {
  assert.deepEqual(parsePool({ version: 1, questions: [] }), []);
  assert.throws(() => parsePool({ version: 2, questions: [] }));
  assert.throws(() => parsePool({ questions: [] }));
  assert.throws(() => parsePool(null));
});

test("parsePool + byId on the real pool", () => {
  const pool = parsePool(data("pool.json"));
  assert.ok(pool.length > 0);
  const ids = byId(pool);
  assert.equal(ids.size, pool.length);
  const q = ids.get(pool[0].id)!;
  assert.equal(typeof q.answer, "string");
  assert.equal(q.wrong_answers.length, 3);
});

test("loadCategories: bundles.json order, base first, missing file = none", () => {
  const bundles = { bundles: [{ id: "base" }, { id: "x" }, { id: "y" }] };
  const cat = (slug: string) => ({ slug, name: slug, subcategories: [slug + "-1"] });
  const cats = loadCategories(bundles, { y: { categories: [cat("c")] }, base: { categories: [cat("a"), cat("b")] } });
  assert.deepEqual(cats.map((c) => [c.bundle, c.slug]), [["base", "a"], ["base", "b"], ["y", "c"]]);
});

test("real categories: base first, every subcategory once per bundle", () => {
  const cats = realCategories();
  const bundles = cats.map((c) => c.bundle);
  assert.equal(bundles[0], "base");
  assert.equal(bundles.lastIndexOf("base") + 1, bundles.indexOf("colombia"));
  const subs = cats.flatMap((c) => c.subcategories);
  const broad = broadOf(cats);
  assert.equal(broad.size, subs.length);
  assert.equal(subsOf(cats, "base").length + subsOf(cats, "colombia").length, subs.length);
  assert.equal(broad.get("drinks")?.slug, "food-and-drink");
  assert.equal(broad.get("colombia/regions-and-departments")?.slug, "geography");
  assert.equal(broad.get("colombia/regions-and-departments")?.bundle, "colombia");
  assert.equal(broad.get("regions-and-departments"), undefined);
  assert.equal(broad.get("Nada"), undefined);
});

test("fixture categories: broadOf, categoryOf", () => {
  const cats = fixture("categories.json") as Category[];
  assert.deepEqual(subsOf(cats, "base"), ["Planetas", "Inventos", "Música", "Fútbol"]);
  const cat = categoryOf(broadOf(cats));
  assert.equal(cat({ subcategory: "Planetas" }), "ciencia");
  assert.equal(cat({ subcategory: "Fútbol" }), "cultura");
  assert.equal(cat({ bundle: "colombia", subcategory: "Ciudades de Colombia" }), "colombia/colombia");
  assert.equal(cat({ subcategory: "Ciudades de Colombia" }), null);
  const twice = categoryOf(broadOf([...cats, { slug: "ciencia", name: "Ciencia", bundle: "colombia", subcategories: ["Planetas"] }]));
  assert.equal(twice({ bundle: "base", subcategory: "Planetas" }), "ciencia");
  assert.equal(twice({ bundle: "colombia", subcategory: "Planetas" }), "colombia/ciencia");
  assert.equal(cat({ subcategory: "Nada" }), null);
  assert.equal(cat({ subcategory: null }), null);
  assert.equal(cat({}), null);
});

// D-22, written out; checked once against the table in the former app/server/selection.py.
const D22 = [[1, 1], [2, 3], [3, 5], [4, 6], [4, 6], [4, 6], [5, 7], [6, 8], [6, 9], [7, 10], [8, 10], [9, 10]];
const LEVEL_WEIGHTS = { 1: 12, 2: 6, 3: 10, 4: 16, 5: 20, 6: 23, 7: 14, 8: 14, 9: 16, 10: 13 }; // qgen.py, D-31

test("parseAgeGroups on the real file: young_teens = D-22", () => {
  const groups = parseAgeGroups(data("age-groups.json"));
  assert.deepEqual(groups.map((g) => g.id), ["kids", "young_teens", "young_adults", "adults"]);
  const yt = groups.find((g) => g.id === "young_teens")!;
  assert.deepEqual(yt.levels, D22);
  assert.deepEqual(yt.level_weights, LEVEL_WEIGHTS);
});

test("parseAgeGroups: bad files throw", () => {
  const file = (levels: unknown, more: object[] = [], level_weights: unknown = LEVEL_WEIGHTS) =>
    ({ groups: [{ id: "young_teens", name: "x", ages: [11, 14], window: [1, 10], levels, level_weights }, ...more] });
  assert.equal(parseAgeGroups(file(D22)).length, 1);
  assert.throws(() => parseAgeGroups(file(D22.slice(1))), /12 levels/);
  assert.throws(() => parseAgeGroups(file([...D22.slice(0, 11), [9, 11]])), /level 12/);
  assert.throws(() => parseAgeGroups(file([[0, 1], ...D22.slice(1)])), /level 1 /);
  assert.throws(() => parseAgeGroups(file([[2, 1], ...D22.slice(1)])), /level 1 /);
  assert.throws(() => parseAgeGroups(file(D22, [], { ...LEVEL_WEIGHTS, 10: 12 })), /level_weights/);
  assert.throws(() => parseAgeGroups(file(D22, [], { ...LEVEL_WEIGHTS, 11: 0 })), /level_weights/);
  assert.throws(() => parseAgeGroups(file(D22, [], null)), /level_weights/);
  const twin = { id: "young_teens", window: [1, 10], levels: D22, level_weights: LEVEL_WEIGHTS };
  assert.throws(() => parseAgeGroups(file(D22, [twin])), /duplicate/);
  assert.throws(() => parseAgeGroups({ groups: [{ ...twin, id: "kids" }] }), /young_teens/);
  assert.throws(() => parseAgeGroups({}));
});

test("parseBundles on the real file: base first, the only base bundle, in every launch language", () => {
  const bundles = parseBundles(data("bundles.json"));
  assert.equal(bundles[0].id, "base");
  assert.deepEqual(bundles.filter((b) => b.kind === "base").map((b) => b.id), ["base"]);
  assert.deepEqual(bundles[0].languages, ["es", "es-ES", "en", "de"]);
  assert.ok(bundles.every((b) => b.name && b.description && !("rule" in b) && !("voice" in b)));
  assert.throws(() => parseBundles({ bundles: [] }));
  assert.throws(() => parseBundles({ bundles: [{ id: "x", kind: "base", languages: [] }] }), /languages/);
  assert.throws(() => parseBundles({ bundles: [{ id: "x", languages: ["es"] }] }), /kind/);
});

test("modPool: namespaced ids, media under the bundle folder, text-only, a reason per dropped question", () => {
  const q = (id: unknown, more: object = {}) => ({
    id, difficulty: 3, subcategory: "Búhos", question: "¿?", answer: "a", wrong_answers: ["b", "c", "d"], hints: ["x", "y", "z"], ...more,
  });
  const img = (file_url: string, role = "illustrative") => ({ media: { type: "image", role, file_url, credit: "Ana" } });
  const pool = {
    version: 1,
    questions: [
      q("owl", img("img/owl 1.jpg")),
      q("abs", img("https://x.org/a.jpg")),
      q("text", { media: null }),
      q("up", img("../../x.jpg", "essential")),
      q("Owl"),
      q(7),
      q("owl"),
      q("blank", { answer: " " }),
      q("short", { wrong_answers: ["b"] }),
      q("hintless", { hints: ["x"] }),
      q("hard", { difficulty: 16 }),
      q("bat", { subcategory: "Murciélagos" }),
      q("draft", { status: "draft" }),
    ],
  };
  const out = modPool(pool, "aves:pack", ["Búhos"]);
  assert.deepEqual(out.questions.map((x) => [x.id, x.bundle, x.media.file_url, x.media.role]), [
    ["aves:owl", "aves:pack", "/data/bundles/aves:pack/img/owl%201.jpg", "illustrative"],
    ["aves:abs", "aves:pack", null, "decorative"],
    ["aves:text", "aves:pack", null, "decorative"],
  ]);
  assert.deepEqual(out.reasons.map((r) => [r.id, r.reason, r.dropped]), [
    ["abs", "bad_media", false], ["up", "bad_media", true], ["Owl", "bad_id", true], ["#6", "bad_id", true],
    ["owl", "duplicate_id", true], ["blank", "no_text", true], ["short", "wrong_answers", true], ["hintless", "hints", true],
    ["hard", "difficulty", true], ["bat", "subcategory", true], ["draft", "status", true],
  ]);
  assert.equal(out.badQuestions, 10);
  assert.equal(out.badMedia, 2);
  assert.ok(isModId(out.questions[0].id) && isOurs("q-0001"));
});
