import { test } from "node:test";
import assert from "node:assert/strict";
import { readdirSync } from "node:fs";
import { join } from "node:path";
import { deletePlayer, gameAction, getGame, getPlayers } from "./api.ts";
import { repair, supply } from "./game.ts";
import { mapOldKeys } from "./save.ts";
import { emptySave, engineData, type EngineData, type SaveData } from "./state.ts";
import { fixture, realAgeGroups, realBundles, slugFixtures } from "./test/fixtures.ts";
import { snapshot, upgradeDb, withoutOrphans } from "./test/save.ts";
import { seededRng } from "./rng.ts";
import { tapeRng, type TapeEntry } from "./test/tape.ts";

interface Step {
  now: string;
  pool: string;
  call: string;
  args: Record<string, unknown>;
  tape: TapeEntry[];
  response: { status: number; body: unknown };
  db?: Parameters<typeof upgradeDb>[0];
}

// The engine plays on slug keys (decision 259); the recordings have bare names, no `key`s (before D-99).
const { categories, oldKeys, back, catName, pool } = slugFixtures();
const bundles = realBundles();
const ageGroups = realAgeGroups();
const data: Record<string, EngineData> = {};
const dataFor = (name: string): EngineData => (data[name] ??= engineData(pool(name), categories, bundles, ageGroups));

const keyed = (args: Record<string, unknown>) =>
  (typeof args.subcategory === "string" ? { ...args, subcategory: oldKeys.subcategories[args.subcategory] ?? args.subcategory } : args);
/** An engine body or save as recorded: keys → names (a joker group's `key` → its `name`). */
const recorded = (v: unknown): unknown => {
  if (typeof v === "string") return back.get(v) ?? v.replace(/^colombia\//, "");
  if (Array.isArray(v)) return v.map(recorded);
  if (!v || typeof v !== "object") return v;
  const { key, ...rest } = v as Record<string, unknown>;
  const out = Object.fromEntries(Object.entries(rest).map(([k, x]) => [k, recorded(x)]));
  if (typeof key === "string" && "available" in rest) out.name = "slug" in rest ? catName.get(rest.slug as string) : recorded(key);
  return out;
};
/** A recorded `db` with its names mapped to keys, through the save loader's mapper. */
const keyedDb = (db: Step["db"] & {}) => {
  const tables = upgradeDb(db);
  const { games } = mapOldKeys({ ...emptySave(), ...tables }, oldKeys);
  return { ...tables, games };
};

const latestState = (save: SaveData) => save.games.reduce<SaveData["games"][number] | null>((m, g) => (m && m.id > g.id ? m : g), null)?.state;

const scenarios = readdirSync(join(import.meta.dirname, "fixtures/game")).filter((f) => f.endsWith(".json")).sort();

for (const file of scenarios) {
  test(`game/${file}`, () => {
    const { steps } = fixture(`game/${file}`) as { steps: Step[] };
    let save = emptySave();
    for (const [i, step] of steps.entries()) {
      const at = `step ${i} (${step.call})`;
      const rng = tapeRng(step.tape);
      const io = { rng, now: step.now };
      const d = dataFor(step.pool);
      // Python burned, the engine counts (plan 65): a seen question that this game can offer again
      // (a later game, or undo after a swap) differs from the recording.
      const seen = save.seen.filter((s) => d.byId.has(s.question_id)).map((s) => s.question_id);
      const offered = new Set(step.call === "new" ? [] : latestState(save)?.offered);
      if (seen.some((q) => !offered.has(q))) break;
      const r = step.call === "get_game" ? getGame(save, d, io, step.args.player as string | undefined)
        : step.call === "players" ? getPlayers(save)
        : step.call === "delete_player" ? deletePlayer(save, step.args)
        : gameAction(save, d, io, step.call, keyed(step.args));
      // Recorded get_game bodies carry a supply; getGame no longer does (plan 133).
      if (step.call === "get_game" && r.status === 200) {
        const { supply: _, ...want } = step.response.body as { supply: unknown };
        assert.deepEqual({ status: r.status, body: recorded(r.body) }, { status: step.response.status, body: want }, at);
      } else assert.deepEqual({ status: r.status, body: recorded(r.body) }, step.response, at);
      if (r.status !== 200) assert.deepEqual(r.save, save, `${at}: save changed on error`);
      if (step.db) assert.deepEqual(snapshot(withoutOrphans(r.save)), keyedDb(step.db), `${at}: db`);
      assert.equal(mapOldKeys(r.save, oldKeys), r.save, `${at}: keys mapped twice`);
      rng.done();
      save = r.save;
    }
  });
}

test("supply (plan 65): seen questions come back in the next game, only blocked ones count against it", () => {
  const d = dataFor("tight");
  const io = { rng: seededRng(1), now: "2026-01-01T00:00:00" };
  let save = gameAction(emptySave(), d, io, "new", { player: "Ana" }).save;
  save = gameAction(save, d, io, "pick", { index: 0 }).save;
  save = gameAction(save, d, io, "answer", { index: 0 }).save;
  assert.equal(save.seen.length, 1);
  const again = gameAction(save, d, io, "new", { player: "Ana" });
  assert.equal(again.status, 200);
  assert.ok(supply(save, d).ok);
  save = { ...again.save, blocked: [d.pool[0].id] };
  const short = gameAction(save, d, io, "new", { player: "Bea" });
  assert.equal(short.status, 409);
  assert.equal((short.body as { error: string }).error, "supply_short");
});

test("repair (plan 91): a running game whose question was dropped goes back to select, nothing seen", () => {
  const d = dataFor("main");
  const io = { rng: seededRng(1), now: "2026-01-01T00:00:00" };
  let save = gameAction(emptySave(), d, io, "new", { player: "Ana" }).save;
  save = gameAction(save, d, io, "pick", { index: 0 }).save;
  const { current, options } = latestState(save)!;
  const patched = engineData(d.pool.filter((q) => q.id !== current), categories, bundles, ageGroups);
  const out = repair(save, patched, io);
  const state = latestState(out)!;
  assert.equal(state.phase, "select");
  assert.equal(state.current, null);
  assert.deepEqual(state.options.slice(1), options.slice(1));
  assert.ok(patched.byId.has(state.options[0]));
  assert.deepEqual(out.seen, save.seen);
  assert.equal(repair(out, patched, io), out);
  assert.equal(gameAction(out, patched, io, "pick", { index: 0 }).status, 200);
});
