import { test } from "node:test";
import assert from "node:assert/strict";
import { emptySave } from "../engine/state.ts";
import { MemoryStore } from "./store.ts";

test("MemoryStore: the language survives a reload, nothing else (task 2097)", async () => {
  const session = new Map<string, string>();
  (globalThis as { sessionStorage?: unknown }).sessionStorage = {
    getItem: (k: string) => session.get(k) ?? null,
    setItem: (k: string, v: string) => void session.set(k, v),
  };
  try {
    assert.equal((await new MemoryStore().load()).language, undefined); // fresh: the first-start screen asks
    await new MemoryStore().save({ ...emptySave(), language: "de", players: [{ id: 1, name: "Ana", created_on: "2026-01-01T00:00:00" }] });
    const again = await new MemoryStore().load(); // a new page: new store
    assert.equal(again.language, "de");
    assert.deepEqual(again.players, []);
  } finally {
    delete (globalThis as { sessionStorage?: unknown }).sessionStorage;
  }
});
