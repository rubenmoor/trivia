import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { join } from "node:path";
import { formatDelta, formatScore, rankText } from "./career-text.ts";

const doc = readFileSync(join(import.meta.dirname, "../../../../plans/24-career.md"), "utf8");
const rows = [...doc.matchAll(/^\| (\d+) \| ([^|]+) \| ([^|]+) \| ([^|]+) \|$/gm)].map((m) => ({ n: Number(m[1]), es: m[2].trim(), en: m[3].trim(), de: m[4].trim() }));

test("rank table of plans/24-career.md", () => {
  assert.equal(rows.length, 15);
  for (const r of rows) {
    assert.equal(rankText(r.n, "es"), r.es);
    assert.equal(rankText(r.n, "es-ES"), r.es);
    assert.equal(rankText(r.n, "en"), r.en);
    assert.equal(rankText(r.n, "de"), r.de);
  }
});

test("rank rounds half up and clamps", () => {
  assert.equal(rankText(2.5, "en"), "Student");
  assert.equal(rankText(2.49, "en"), "Apprentice");
  assert.equal(rankText(0, "en"), "Beginner");
  assert.equal(rankText(15.4, "en"), "Walking Encyclopedia");
});

test("number format per locale", () => {
  assert.equal(formatScore(1840, "en"), "1,840");
  assert.equal(formatScore(1840, "es"), "1840");
  assert.equal(formatScore(1840, "es-ES"), "1840");
  assert.equal(formatScore(1840, "de"), "1.840");
  assert.equal(formatScore(12840, "es"), "12.840");
  assert.equal(formatScore(-120, "en"), "−120");
  assert.equal(formatScore(-1840, "de"), "−1.840");
});

test("delta signs", () => {
  assert.equal(formatDelta(25, "en"), "+25");
  assert.equal(formatDelta(-1, "en"), "−1");
  assert.equal(formatDelta(225, "de"), "+225");
});
