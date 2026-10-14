import { test } from "node:test";
import assert from "node:assert/strict";
import { readdirSync } from "node:fs";
import { join } from "node:path";
import type { Category } from "../lib/types.ts";
import { deletePlayer, gameAction, getGame, getPlayers } from "./api.ts";
import { repair } from "./game.ts";
import { subKey, type PoolQuestion } from "./pool.ts";
import { emptySave, engineData, type EngineData, type SaveData } from "./state.ts";
import { fixture, realAgeGroups, realBundles } from "./test/fixtures.ts";
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

const categories = fixture("categories.json") as Category[];
const bundles = realBundles();
const ageGroups = realAgeGroups();
const data: Record<string, EngineData> = {};
const dataFor = (pool: string): EngineData =>
  (data[pool] ??= engineData((fixture(`pools/${pool}.json`) as { questions: PoolQuestion[] }).questions, categories, bundles, ageGroups));

// Recorded before bundle-scoped keys (D-99): `subcategory` args are bare names; bodies and saves have no `key`s, bare names.
const keyOf = new Map(categories.flatMap((c) => c.subcategories.map((s) => [s, subKey(c.bundle, s)] as const)));
const keyed = (args: Record<string, unknown>) =>
  (typeof args.subcategory === "string" ? { ...args, subcategory: keyOf.get(args.subcategory) ?? args.subcategory } : args);
const recorded = (v: unknown): unknown =>
  typeof v === "string" ? v.replace(/^colombia\//, "")
  : Array.isArray(v) ? v.map(recorded)
  : v && typeof v === "object" ? Object.fromEntries(Object.entries(v).filter(([k]) => k !== "key").map(([k, x]) => [k, recorded(x)]))
  : v;

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
      // (a later game, or undo after a swap) and the player-scoped supply differ from the recording.
      const seen = save.seen.filter((s) => d.byId.has(s.question_id)).map((s) => s.question_id);
      const offered = new Set(step.call === "new" ? [] : latestState(save)?.offered);
      if (seen.some((q) => !offered.has(q))) break;
      const r = step.call === "get_game" ? getGame(save, d, io, step.args.player as string | undefined)
        : step.call === "players" ? getPlayers(save)
        : step.call === "delete_player" ? deletePlayer(save, step.args)
        : gameAction(save, d, io, step.call, keyed(step.args));
      if (seen.length && step.call === "get_game" && r.status === 200) {
        const { supply: _, ...body } = recorded(r.body) as { supply: unknown };
        const { supply: __, ...want } = step.response.body as { supply: unknown };
        assert.deepEqual({ status: r.status, body }, { status: step.response.status, body: want }, at);
      } else assert.deepEqual({ status: r.status, body: recorded(r.body) }, step.response, at);
      if (r.status !== 200) assert.deepEqual(r.save, save, `${at}: save changed on error`);
      if (step.db) assert.deepEqual(recorded(snapshot(withoutOrphans(r.save))), upgradeDb(step.db), `${at}: db`);
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
  assert.ok(getGame(save, d, io, "Ana").body.supply.ok);
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
