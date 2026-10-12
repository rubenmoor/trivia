import { test } from "node:test";
import assert from "node:assert/strict";
import { flaggedIds, parseSave, setFlag } from "./save.ts";
import { emptySave, SAVE_VERSION, SPANISH, type SaveData } from "./state.ts";
import { MemoryStore } from "./store.ts";
import { fixture } from "./test/fixtures.ts";
import { snapshot, upgradeDb } from "./test/save.ts";

const { steps } = fixture("game/abandon.json") as { steps: { db?: Parameters<typeof upgradeDb>[0] }[] };
const v2 = steps.findLast((s) => s.db)!.db!;
const db = upgradeDb(v2);
const full: SaveData = {
  version: SAVE_VERSION, ...db, notified_exhausted: [],
  flags: { q1: { flagged_on: "2026-10-01T20:00:00", player: "Ana" } }, reports: [], language: SPANISH,
};

test("parseSave accepts emptySave() and a fixture db; a save without a language is Spanish", () => {
  assert.deepEqual(parseSave(emptySave()), { ...emptySave(), language: SPANISH });
  assert.deepEqual(parseSave({ ...full, language: undefined }), full);
  assert.deepEqual(parseSave(JSON.stringify(full)), full);
  assert.ok(db.games.length > 0 && db.seen.length > 0);
});

test("parseSave fills missing flags; version 1 gets reports, version 2 seen rows", () => {
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

test("parseSave rejects newer versions and broken shapes", () => {
  assert.throws(() => parseSave({ ...full, version: SAVE_VERSION + 1 }), /newer game/);
  for (const bad of [null, [], "x", { ...full, version: undefined }, { ...full, version: 0 },
    { ...full, players: undefined }, { ...full, games: {} }, { ...full, seen: [1] }, { ...full, blocked: [1] },
    { ...full, notified_exhausted: undefined }, { ...full, version: 2, burned: [1] },
    { ...full, games: [{ id: 1 }] }, { ...full, flags: [] }, { ...full, reports: {} }, { ...full, language: "en" }, { ...full, language: { ui: "en" } }]) {
    assert.throws(() => parseSave(bad), JSON.stringify(bad)?.slice(0, 60));
  }
});

test("setFlag keeps the first flagged_on, unflag removes it, input unchanged", () => {
  const before = structuredClone(full);
  const a = setFlag(full, "q2", true, null, "2026-10-02T20:00:00");
  const b = setFlag(a, "q1", true, "Bo", "2026-10-03T20:00:00");
  assert.deepEqual(b.flags.q1, full.flags.q1);
  assert.deepEqual(flaggedIds(b), ["q1", "q2"]);
  const c = setFlag(b, "q1", false, null, "2026-10-04T20:00:00");
  assert.deepEqual(flaggedIds(c), ["q2"]);
  assert.deepEqual(setFlag(c, "q1", true, "Bo", "2026-10-05T20:00:00").flags.q1,
    { flagged_on: "2026-10-05T20:00:00", player: "Bo" });
  assert.deepEqual(full, before);
  assert.throws(() => setFlag(full, "", true, null, "2026-10-02T20:00:00"));
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
