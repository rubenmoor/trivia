import { test } from "node:test";
import assert from "node:assert/strict";
import { baseBundlesFor, baseListsLocale, bundlesFor, packsFor, parseBundles, withPacks } from "../engine/pool.ts";

const bundles = parseBundles({
  bundles: [
    { id: "base", kind: "base", languages: ["es", "en"], name: "Base", description: "" },
    { id: "chinese-base", kind: "base", languages: ["zh-Hans", "en"], name: "ZH", description: "" },
    { id: "stem", kind: "theme", languages: ["en"], name: "STEM", description: "" },
  ],
});

test("zh-Hans: no base pool needed, chinese-base is the only base bundle (task 2422)", () => {
  assert.equal(baseListsLocale(bundles, "zh-Hans"), false);
  assert.equal(baseListsLocale(bundles, "en"), true);
  assert.deepEqual(baseBundlesFor(bundles, "zh-Hans").map((b) => b.id), ["chinese-base"]);
  assert.deepEqual(packsFor(bundles, "zh-Hans").map((b) => b.id), ["chinese-base"]);
  assert.deepEqual(baseBundlesFor(bundles, "en").map((b) => b.id), ["base", "chinese-base"]);
});

test("zh-Hans with only chinese-base's pack: empty base pool, bundlesFor gives chinese-base alone (task 2422)", () => {
  const pack = { version: 1, questions: [{ id: "z1" }] };
  const { pool, bundles: out } = withPacks([], bundles, "zh-Hans", { "chinese-base": pack });
  assert.deepEqual(pool.map((q) => q.id), ["z1"]);
  assert.deepEqual(bundlesFor({ bundles: out, locale: "zh-Hans" }).map((b) => b.id), ["chinese-base"]);
  assert.deepEqual(bundlesFor({ bundles: out, locale: "en" }).map((b) => b.id), ["base", "chinese-base", "stem"]);
});
