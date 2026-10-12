import { test } from "node:test";
import assert from "node:assert/strict";
import { flaggedIds, parseSave, setFlag } from "./save.ts";
import { emptySave, type SaveData } from "./state.ts";
import { MemoryStore } from "./store.ts";
import { fixture } from "./test/fixtures.ts";

const { steps } = fixture("game/abandon.json") as { steps: { db?: Pick<SaveData, "players" | "games" | "burned"> }[] };
const db = steps.findLast((s) => s.db)!.db!;
const full: SaveData = { version: 1, ...db, flags: { q1: { flagged_on: "2026-10-01T20:00:00", player: "Ana" } } };

test("parseSave accepts emptySave() and a fixture db", () => {
  assert.deepEqual(parseSave(emptySave()), emptySave());
  assert.deepEqual(parseSave(JSON.stringify(full)), full);
  assert.ok(db.games.length > 0 && db.burned.length > 0);
});

test("parseSave fills missing flags", () => {
  assert.deepEqual(parseSave({ version: 1, ...db }), { version: 1, ...db, flags: {} });
});

test("parseSave rejects newer versions and broken shapes", () => {
  assert.throws(() => parseSave({ ...full, version: 2 }), /newer game/);
  for (const bad of [null, [], "x", { ...full, version: undefined }, { ...full, version: 0 },
    { ...full, players: undefined }, { ...full, games: {} }, { ...full, burned: [1] },
    { ...full, games: [{ id: 1 }] }, { ...full, flags: [] }]) {
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
