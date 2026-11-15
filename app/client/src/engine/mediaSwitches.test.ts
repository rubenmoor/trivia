// The video and audio switches in every mode (decisions 33, 645): off → no such question drawn, offered or counted; not «customized».
import { test } from "node:test";
import assert from "node:assert/strict";
import { gameAction } from "./api.ts";
import * as game from "./game.ts";
import { outlook } from "./outlook.ts";
import type { GameMode } from "../lib/types.ts";
import type { AgeGroup, Bundle, PoolQuestion } from "./pool.ts";
import { seededRng } from "./rng.ts";
import { emptySave, engineData, type SaveData } from "./state.ts";

// 12 per difficulty 1–12: j 0–1 video, j 2–3 audio, the rest plain.
const subs = ["a1", "a2", "b1", "b2", "c1", "c2"];
const pool = Array.from({ length: 12 }, (_, d) => d + 1).flatMap((d) => Array.from({ length: 12 }, (_, j) => ({
  id: `q${d}-${j}`, status: "approved", difficulty: d, subcategory: subs[j % 6], bundle: "base", description: "", question: "",
  answer: "R", wrong_answers: ["W1", "W2", "W3"], hints: ["h"], fun_fact: "",
  media: j < 2 ? { type: "video" } : j < 4 ? { type: "audio" } : null, background: null,
}) as unknown as PoolQuestion));
const group = { id: "adults", name: "G", ages: [0, null], window: [1, 12], level_weights: {},
  levels: Array.from({ length: 12 }, (_, i) => [i + 1, i + 1] as const) } as AgeGroup;
const bundle: Bundle = { id: "base", kind: "base", languages: ["es"], name: "B", description: "" };
const data = engineData(pool, ["a", "b", "c"].map((c) => ({ slug: c, name: c, bundle: "base", subcategories: [`${c}1`, `${c}2`] })),
  [bundle], [group]);
const io = { rng: seededRng(1), now: "2026-01-01T00:00:00Z", ms: 0 };
const typeOf = (id: string) => data.byId.get(id)!.media?.type ?? null;

const SWITCHES: { video?: false; audio?: false }[] = [{ video: false }, { audio: false }, { video: false, audio: false }];
const banned = (s: { video?: boolean; audio?: boolean }) => (id: string) =>
  (s.video === false && typeOf(id) === "video") || (s.audio === false && typeOf(id) === "audio");

/** Starts a game of `mode` with `body` the way the Choice screen's body does; the game's state and the ids it could ever draw. */
function begin(mode: GameMode, body: Record<string, unknown>) {
  const common = { bundles: ["base"], age_group: "adults", ...body };
  let save: SaveData;
  if (mode === "solo" || mode === "gamemaster") {
    const r = gameAction(emptySave(), data, io, "new", { player: "Ana", mode, ...common });
    assert.equal(r.status, 200, JSON.stringify(r.body));
    save = r.save;
  } else save = game.newSession(emptySave(), data, io, ["Ana", "Beto"], { mode, ...common }).save;
  return save;
}

for (const mode of ["gamemaster", "solo", "rr-coop", "rr-competitive", "timed"] as const) {
  test(`${mode}: video and audio switches keep those questions out of the game, not customized`, () => {
    for (const sw of SWITCHES) {
      const save = begin(mode, sw);
      const row = save.games.at(-1)!;
      const state = row.seats?.[0]?.state ?? row.state;
      assert.equal(state.settings.customized ?? false, false);
      assert.equal(state.settings.video, sw.video === false ? false : undefined);
      const ids = [...state.offered, ...state.options];
      assert.ok(ids.length > 0);
      assert.ok(!ids.some(banned(sw)), `${mode} ${JSON.stringify(sw)}`);
      const avail = game.availableFor(save, data, game.gameChoice(state, data));
      assert.ok(avail.length > 0 && !avail.some((q) => banned(sw)(q.id)));
    }
  });
}

test("the outlook counts only what the switches allow, in any mode", () => {
  const base = { age_group: "adults", difficulty: null, bundles: ["base"], levels: 12, cards: 4, video: true, audio: true, answers: true,
    jokers: game.STANDARD_JOKERS };
  for (const mode of ["solo", "rr-coop", "rr-competitive", "timed"] as const) {
    const on = outlook(emptySave(), data, { ...base, mode });
    const off = outlook(emptySave(), data, { ...base, mode, video: false, audio: false });
    assert.ok(off.k <= on.k, mode);
    assert.equal(game.availableFor(emptySave(), data, { ...base, video: false, audio: false }).length, 12 * 8);
  }
});

test("the preset is the newest game's switches; a fresh player has both on", () => {
  assert.deepEqual([game.playerChoice(emptySave(), data, "Ana").video, game.playerChoice(emptySave(), data, "Ana").audio], [true, true]);
  const save = begin("solo", { video: false });
  const c = game.playerChoice(save, data, "Ana");
  assert.deepEqual([c.video, c.audio], [false, true]);
});
