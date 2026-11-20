// poolFiles (app/client/poolFiles.ts): a base pack's every pool (no es pool needed), a DLC pack's es pool only (decision 753). `npm test`
import assert from "node:assert/strict";
import { mkdirSync, mkdtempSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join } from "node:path";
import { after, test } from "node:test";
import { poolFiles } from "../client/poolFiles.ts";

const tmp = mkdtempSync(join(tmpdir(), "trivia-poolfiles-"));
after(() => rmSync(tmp, { recursive: true, force: true }));
const put = (rel) => {
  mkdirSync(dirname(join(tmp, rel)), { recursive: true });
  writeFileSync(join(tmp, rel), "{}");
};
writeFileSync(join(tmp, "bundles.json"), JSON.stringify({ bundles: [{ id: "base", kind: "base" }, { id: "chinese-base", kind: "base" }, { id: "colombia", kind: "region" }] }));
for (const f of ["pool.json", "bundles/chinese-base/pool.en.json", "bundles/chinese-base/pool.zh-Hans.json", "bundles/chinese-base/names.en.json", "bundles/colombia/pool.json", "bundles/colombia/pool.en.json"]) put(f);
mkdirSync(join(tmp, "bundles", "stem"));

test("pool files with shipped media", () => {
  const rel = poolFiles(`${tmp}/`).map((f) => f.slice(tmp.length + 1));
  assert.deepEqual(rel, ["pool.json", "bundles/chinese-base/pool.en.json", "bundles/chinese-base/pool.zh-Hans.json", "bundles/colombia/pool.json"]);
});
