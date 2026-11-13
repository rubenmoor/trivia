import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { join } from "node:path";
import {
  award, BADGE_NAMES, BADGES, countEnd, countRight, countWrong, emptyCareer, newBadges, rankIndex, rankOf, SUBJECTS, YEAR_GROUPS,
  type PlayerCareer,
} from "./career.ts";

const data = (f: string) => JSON.parse(readFileSync(join(import.meta.dirname, "../../../data", f), "utf8"));
const skills = (c: PlayerCareer) => newBadges(c).filter((n) => !n.startsWith("CAREER_SCORE_"));
const rights = (c: PlayerCareer, s: string, d: number, n: number) => { for (let i = 0; i < n; i++) c = countRight(c, s, d); return c; };

test("ids match the data files", () => {
  assert.deepEqual(SUBJECTS, data("subjects.json").subjects.map((s: { id: string }) => s.id));
  const groups = data("age-groups.json");
  const ids = (Array.isArray(groups) ? groups : groups.groups).map((g: { id: string }) => g.id);
  assert.deepEqual(YEAR_GROUPS, ids);
});

test("39 unique badges in live order", () => {
  assert.equal(BADGE_NAMES.length, 39);
  assert.equal(new Set(BADGE_NAMES).size, 39);
  assert.equal(BADGE_NAMES[0], "CAREER_HISTORY_ELEMENTARY");
  assert.equal(BADGE_NAMES[6], "CAREER_SPORT_ELEMENTARY");
  assert.equal(BADGE_NAMES[7], "CAREER_HISTORY_MIDDLE");
  assert.deepEqual(BADGE_NAMES.slice(21, 25), ["CAREER_DIPLOMA_ELEMENTARY", "CAREER_DIPLOMA_MIDDLE", "CAREER_DIPLOMA_HIGH", "CAREER_COLLEGE"]);
  assert.deepEqual(BADGE_NAMES.slice(25, 29), ["CAREER_YEAR_KIDS", "CAREER_YEAR_YOUNG_TEENS", "CAREER_YEAR_YOUNG_ADULTS", "CAREER_YEAR_ADULTS"]);
  assert.equal(BADGE_NAMES.at(-1), "CAREER_SCORE_100000");
});

test("countRight: d² and every band ≤ d; none without subject", () => {
  let c = countRight(emptyCareer(), "history", 5);
  assert.equal(c.score, 25);
  assert.deepEqual(c.right.history, [1, 1, 0, 0]);
  c = countRight(c, "history", 15);
  assert.deepEqual(c.right.history, [2, 2, 1, 1]);
  c = countRight(c, "history", 4);
  assert.deepEqual(c.right.history, [3, 2, 1, 1]);
  const none = countRight(emptyCareer(), undefined, 3);
  assert.equal(none.score, 9);
  assert.deepEqual(none.right, {});
  assert.deepEqual(countRight(emptyCareer(), "unknown", 3).right, {});
});

test("countWrong: −1, may go negative; reducers don't mutate", () => {
  const c0 = emptyCareer();
  assert.equal(countWrong(c0).score, -1);
  assert.equal(c0.score, 0);
});

test("countEnd: years +1, ranks keep 10", () => {
  let c = emptyCareer();
  for (let i = 0; i < 12; i++) c = countEnd(c, "kids", i);
  assert.equal(c.years.kids, 12);
  assert.deepEqual(c.ranks, [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]);
});

test("subject × grade thresholds 15 / 25 / 15", () => {
  assert.deepEqual(newBadges(rights(emptyCareer(), "nature", 1, 14)), []);
  assert.deepEqual(newBadges(rights(emptyCareer(), "nature", 1, 15)), ["CAREER_NATURE_ELEMENTARY"]);
  const m = rights(emptyCareer(), "arts", 5, 24);
  assert.deepEqual(skills(m), ["CAREER_ARTS_ELEMENTARY"]);
  assert.ok(newBadges(countRight(m, "arts", 5)).includes("CAREER_ARTS_MIDDLE"));
  assert.ok(!newBadges(rights(emptyCareer(), "arts", 9, 14)).includes("CAREER_ARTS_HIGH"));
  assert.ok(newBadges(rights(emptyCareer(), "arts", 9, 15)).includes("CAREER_ARTS_HIGH"));
});

test("diplomas need all 7 subjects; no order between grades", () => {
  let c = emptyCareer();
  for (const s of SUBJECTS.slice(0, 6)) c = rights(c, s, 9, 15);
  assert.ok(!newBadges(c).includes("CAREER_DIPLOMA_HIGH"));
  c = rights(c, SUBJECTS[6], 9, 15);
  const names = newBadges(c);
  for (const g of ["ELEMENTARY", "HIGH"]) assert.ok(names.includes(`CAREER_DIPLOMA_${g}`));
  assert.ok(!names.includes("CAREER_DIPLOMA_MIDDLE")); // 15 < 25 at middle
});

test("college: 15 right at 13+, any subject, mixed", () => {
  let c = rights(emptyCareer(), "history", 13, 7);
  c = rights(c, "sport", 15, 7);
  assert.ok(!newBadges(c).includes("CAREER_COLLEGE"));
  assert.ok(newBadges(countRight(c, "media", 13)).includes("CAREER_COLLEGE"));
  assert.ok(!newBadges(rights(emptyCareer(), "history", 12, 40)).includes("CAREER_COLLEGE"));
});

test("school years: 20 finished games per age group", () => {
  let c = emptyCareer();
  for (let i = 0; i < 19; i++) c = countEnd(c, "young_teens", 3);
  assert.deepEqual(newBadges(c), []);
  assert.deepEqual(newBadges(countEnd(c, "young_teens", 3)), ["CAREER_YEAR_YOUNG_TEENS"]);
  assert.deepEqual(newBadges(countEnd(c, "kids", 3)), []);
});

test("score badges at each milestone; kept when the score drops", () => {
  const at = (score: number) => newBadges({ ...emptyCareer(), score }).filter((n) => n.startsWith("CAREER_SCORE_"));
  assert.deepEqual(at(99), []);
  assert.deepEqual(at(100), ["CAREER_SCORE_100"]);
  assert.equal(at(100000).length, 10);
  assert.deepEqual(at(249), ["CAREER_SCORE_100"]);
  let c = award({ ...emptyCareer(), score: 250 }, "2026-11-01T10:00:00");
  assert.deepEqual(Object.keys(c.badges), ["CAREER_SCORE_100", "CAREER_SCORE_250"]);
  c = award({ ...c, score: -5 }, "2026-11-02T10:00:00");
  assert.equal(Object.keys(c.badges).length, 2);
  assert.equal(c.badges.CAREER_SCORE_100.on, "2026-11-01T10:00:00");
  assert.deepEqual(newBadges(c), []);
});

test("award keeps held badges and their shown mark", () => {
  const c = award({ ...emptyCareer(), score: 100, badges: { CAREER_SCORE_100: { on: "t0", shown: true } } }, "t1");
  assert.deepEqual(c.badges, { CAREER_SCORE_100: { on: "t0", shown: true } });
  assert.equal(BADGES.length, 39);
});

test("rankOf: empty, one, weights newest heaviest, at least 1", () => {
  assert.equal(rankOf([]), null);
  assert.equal(rankIndex([]), null);
  assert.equal(rankOf([7]), 7);
  assert.equal(rankOf([0]), 1);
  assert.equal(rankOf([0, 0, 0]), 1);
  assert.equal(rankOf([10, 13]), 12); // (1·10 + 2·13) / 3
  assert.equal(rankOf([4, 3]), 3); // 3.33
  assert.equal(rankOf([6, 4, 0, 0]), 2); // (7·6 + 8·4) / 34 = 2.18
  assert.equal(rankOf([5, 6, 0, 0, 0, 0]), 1); // 0.81 → at least 1
});

test("rankOf: only the last 10 count; half up", () => {
  assert.equal(rankOf([15, ...Array(10).fill(3)]), 3);
  assert.equal(rankOf([3, 0, 0, 3]), 2); // weights 7..10: 51 / 34 = 1.5
  assert.equal(rankOf([3, 0, 0, 2]), 1); // 41 / 34 = 1.2
  assert.equal(rankIndex([15, 15]), 14);
  assert.equal(rankIndex([1]), 0);
});
