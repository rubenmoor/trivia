import { test } from "node:test";
import assert from "node:assert/strict";
import { pickable } from "./i18n.ts";

test("gated languages (decision 222): only once their pool ships, or for the dev Steam user", async () => {
  const open = ["es", "es-ES", "en", "de"];
  assert.deepEqual(await pickable(async () => false, false), open);
  assert.deepEqual(await pickable(async () => false, true), [...open, "zh-Hans", "zh-Hant"]);
  assert.deepEqual(await pickable(async (l) => l === "zh-Hans", false), [...open, "zh-Hans"]);
});
