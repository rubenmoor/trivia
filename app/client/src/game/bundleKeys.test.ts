import assert from "node:assert/strict";
import { test } from "node:test";
import { bundleKeys } from "./bundleKeys.ts";

test("Latin names: first free letter, accents stripped", () => {
  assert.deepEqual(bundleKeys(["Base", "Brasil", "Ñandú"], ["f"]), ["b", "r", "n"]);
});
test("CJK names get a free Latin letter, never a CJK chip", () => {
  const keys = bundleKeys(["基础包：中国", "历史", "Base"], ["f"]);
  assert.ok(keys.every((k) => /^[a-z]$/.test(k)));
  assert.equal(new Set(keys).size, keys.length);
  assert.ok(!keys.includes("f"));
});
