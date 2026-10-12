import { test } from "node:test";
import assert from "node:assert/strict";
import type { Category } from "../lib/types.ts";
import { broadOf, bundleOf, byId, categoryOf, loadCategories, parsePool, subcategories } from "./pool.ts";
import { data, fixture, realCategories } from "./test/fixtures.ts";

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

test("real categories: base first, every subcategory once", () => {
  const cats = realCategories();
  const bundles = cats.map((c) => c.bundle);
  assert.equal(bundles[0], "base");
  assert.equal(bundles.lastIndexOf("base") + 1, bundles.indexOf("colombia"));
  const subs = subcategories(cats);
  assert.equal(new Set(subs).size, subs.length);
  assert.equal(subcategories(cats, "base").length + subcategories(cats, "colombia").length, subs.length);
  const broad = broadOf(cats);
  assert.equal(broad.get("Bebidas")?.slug, "comida-bebida");
  assert.equal(bundleOf(cats, "Bebidas"), "base");
  assert.equal(broad.get("Regiones de Colombia")?.slug, "colombia-pais");
  assert.equal(bundleOf(cats, "Regiones de Colombia"), "colombia");
  assert.equal(bundleOf(cats, "Nada"), null);
});

test("fixture categories: broadOf, categoryOf", () => {
  const cats = fixture("categories.json") as Category[];
  assert.deepEqual(subcategories(cats, "base"), ["Planetas", "Inventos", "Música", "Fútbol"]);
  const cat = categoryOf(broadOf(cats));
  assert.equal(cat({ subcategory: "Planetas" }), "ciencia");
  assert.equal(cat({ subcategory: "Fútbol" }), "cultura");
  assert.equal(cat({ subcategory: "Ciudades de Colombia" }), "colombia");
  assert.equal(cat({ subcategory: "Nada" }), null);
  assert.equal(cat({ subcategory: null }), null);
  assert.equal(cat({}), null);
  assert.equal(bundleOf(cats, "Comida colombiana"), "colombia");
});
