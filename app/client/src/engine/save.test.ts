import { test } from "node:test";
import assert from "node:assert/strict";
import { parseSave, setFlag } from "./save.ts";
import { emptySave, SAVE_VERSION, SPANISH, type SaveData } from "./state.ts";
import { fixture } from "./test/fixtures.ts";
import { MemoryStore, snapshot, upgradeDb } from "./test/save.ts";

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

test("parseSave rejects newer versions and broken shapes", () => {
  assert.throws(() => parseSave({ ...full, version: SAVE_VERSION + 1 }), /newer game/);
  for (const bad of [null, [], "x", { ...full, version: undefined }, { ...full, version: 0 },
    { ...full, players: undefined }, { ...full, games: {} }, { ...full, seen: [1] }, { ...full, blocked: [1] },
    { ...full, notified_exhausted: undefined }, { ...full, version: 2, burned: [1] },
    { ...full, games: [{ id: 1 }] }, { ...full, flags: [] }, { ...full, version: 3, reports: {} }, { ...full, language: "en" }, { ...full, language: { ui: "en" } }]) {
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

test("MemoryStore round trip and isolation", async () => {
  assert.deepEqual(await new MemoryStore().load(), emptySave());
  const doc = structuredClone(full);
  const store = new MemoryStore();
  await store.save(doc);
  doc.players.push({ id: 99, name: "X", created_on: "2026-10-01T20:00:00" });
  const out = await store.load();
  assert.deepEqual(out, full);
  out.flags = {};
  assert.deepEqual(await store.load(), full);
});
