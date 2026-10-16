import { test } from "node:test";
import assert from "node:assert/strict";
import { mapOldKeys, parseSave, setFlag, setReported } from "./save.ts";
import { emptySave, SAVE_VERSION, SPANISH, type SaveData } from "./state.ts";
import { fixture } from "./test/fixtures.ts";
import { snapshot, upgradeDb } from "./test/save.ts";

const { steps } = fixture("game/abandon.json") as { steps: { db?: Parameters<typeof upgradeDb>[0] }[] };
const v2 = steps.findLast((s) => s.db)!.db!;
const db = upgradeDb(v2);
const full: SaveData = {
  version: SAVE_VERSION, ...db, notified_exhausted: [],
  flags: { q1: { flagged_on: "2026-10-01T20:00:00", player: "Ana" } }, language: SPANISH,
};

test("parseSave accepts emptySave() and a fixture db; a save without a language is Spanish", () => {
  assert.deepEqual(parseSave(emptySave()), { ...emptySave(), language: SPANISH });
  assert.deepEqual(parseSave({ ...full, language: undefined }), full);
  assert.deepEqual(parseSave(JSON.stringify(full)), full);
  assert.equal(parseSave({ ...full, language: { ui: "de", questions: "es" } }).language, "de"); // before plan 126
  assert.ok(db.games.length > 0 && db.seen.length > 0);
});

test("parseSave fills missing flags; version 1 and 2 upgrade", () => {
  assert.deepEqual(parseSave({ ...full, flags: undefined }), { ...full, flags: {} });
  const up = (v: number) => {
    const out = parseSave({ version: v, ...v2, ...(v === 2 ? { reports: [] } : {}) });
    return { ...out, ...snapshot(out) };
  };
  assert.deepEqual(up(1), { ...full, flags: {} });
  assert.deepEqual(up(2), { ...full, flags: {} });
});

test("v2 → v3: a player's burn is one seen row, two players count 2, null → blocked once", () => {
  const burned = [
    { question_id: "a", player_id: 1, game_id: 1, burned_on: "t1" },
    { question_id: "a", player_id: 2, game_id: 2, burned_on: "t2" },
    { question_id: "b", player_id: null, game_id: 1, burned_on: "t1" },
    { question_id: "b", player_id: null, game_id: 2, burned_on: "t2" },
    { question_id: "c", player_id: 2, game_id: 2, burned_on: "t2" },
  ];
  const out = parseSave({ version: 2, players: [], games: [], burned, flags: {}, reports: [] });
  assert.equal(out.version, SAVE_VERSION);
  assert.deepEqual(out.seen, [
    { question_id: "a", game_id: 1, seen_on: "t1" },
    { question_id: "a", game_id: 2, seen_on: "t2" },
    { question_id: "c", game_id: 2, seen_on: "t2" },
  ]);
  assert.deepEqual(out.blocked, ["b"]);
  assert.deepEqual(out.notified_exhausted, []);
  assert.ok(!("burned" in out));
});

test("v3 → v4: reports become flags or add their note", () => {
  const reports = [
    { question_id: "q1", game_id: 1, player_id: 1, level: 3, reported_on: "t1", note: "mal" },
    { question_id: "q2", game_id: 1, player_id: 1, level: 4, reported_on: "t2" },
  ];
  const out = parseSave({ ...full, version: 3, players: [{ id: 1, name: "Bo", created_on: "t0" }], reports });
  assert.deepEqual(out.flags, {
    q1: { ...full.flags.q1, note: "mal" },
    q2: { flagged_on: "t2", player: "Bo", level: 4 },
  });
  assert.ok(!("reports" in out));
});

test("v4 → v5 unchanged; a session row round-trips parseSave and mapOldKeys", () => {
  assert.deepEqual(parseSave({ ...full, version: 4 }), full);
  const state = { ...db.games[0].state, purged: ["old"] };
  const session = {
    ...db.games[0], id: 99, player_id: null, turn: 1, seats: [{ player_id: 1 }, { player_id: null, state, lives: 3, out: true as const }],
  };
  const doc = { ...full, games: [...full.games, session] };
  assert.deepEqual(parseSave(JSON.stringify(doc)), doc);
  const mapped = mapOldKeys(doc, { categories: {}, subcategories: { old: "new" } });
  assert.deepEqual(mapped.games.at(-1)!.seats?.[1].state?.purged, ["new"]);
  assert.deepEqual(mapped.games.at(-1)!.seats?.[0], { player_id: 1 });
  for (const bad of [{ seats: [] }, { seats: [1] }, { seats: [{ player_id: "a" }] }, { seats: [{ player_id: 1, state: 1 }] },
    { seats: [{ player_id: 1 }], turn: 1 }, { turn: 1.5 }])
    assert.throws(() => parseSave({ ...full, games: [{ ...session, ...bad }] }), JSON.stringify(bad));
});

test("parseSave rejects newer versions and broken shapes", () => {
  assert.throws(() => parseSave({ ...full, version: SAVE_VERSION + 1 }), /newer game/);
  for (const bad of [null, [], "x", { ...full, version: undefined }, { ...full, version: 0 },
    { ...full, players: undefined }, { ...full, games: {} }, { ...full, seen: [1] }, { ...full, blocked: [1] },
    { ...full, notified_exhausted: undefined }, { ...full, version: 2, burned: [1] },
    { ...full, games: [{ id: 1 }] }, { ...full, flags: [] }, { ...full, version: 3, reports: {} }, { ...full, language: 3 }, { ...full, language: { questions: "en" } }]) {
    assert.throws(() => parseSave(bad), JSON.stringify(bad)?.slice(0, 60));
  }
});

test("setFlag keeps the first flagged_on, edits the note, unflag removes it, input unchanged", () => {
  const before = structuredClone(full);
  const a = setFlag(full, "q2", { player: null, level: 2, note: " mal " }, "2026-10-02T20:00:00");
  assert.deepEqual(a.flags.q2, { flagged_on: "2026-10-02T20:00:00", player: null, level: 2, note: "mal" });
  const b = setFlag(a, "q2", { player: "Bo", note: "" }, "2026-10-03T20:00:00");
  assert.deepEqual(b.flags.q2, { flagged_on: "2026-10-02T20:00:00", player: null, level: 2 });
  assert.deepEqual(Object.keys(setFlag(b, "q1", null, "2026-10-04T20:00:00").flags), ["q2"]);
  assert.deepEqual(full, before);
  assert.throws(() => setFlag(full, "", { player: null }, "2026-10-02T20:00:00"));
  assert.throws(() => setFlag(full, "q3", { player: null, note: "x".repeat(501) }, "2026-10-02T20:00:00"));
});

test("setReported adds reported_on (no version bump); it survives parse and a re-note", () => {
  const a = setReported(full, "q1", "2026-11-02T21:00:00");
  assert.deepEqual(a.flags.q1, { ...full.flags.q1, reported_on: "2026-11-02T21:00:00" });
  assert.deepEqual(parseSave(JSON.parse(JSON.stringify(a))), a);
  assert.equal(setFlag(a, "q1", { player: "Bo", note: "x" }, "2026-11-03T20:00:00").flags.q1.reported_on, "2026-11-02T21:00:00");
  assert.throws(() => setReported(full, "q9", "2026-11-02T21:00:00"));
});
