#!/usr/bin/env node
// trivia-gallery's demo saves (plan 100): built with the engine on the es pool, made-up players.
// Usage: node authoring/tools/gallery_saves.mjs <ui locale> → JSON {saves: {name: save}, meta: {name: {...}}} on stdout.
import { answer, pick, view } from "../../app/client/src/engine/game.ts";
import { baseSave, checkVersion, io, latestState, PLAYERS, playTo, rightOf } from "./demo_saves.mjs";
import { loadData } from "./engine_data.mjs";

const ui = process.argv[2];
if (!ui) throw new Error("usage: gallery_saves.mjs <ui locale>");
const data = loadData("es");

/** Image questions with hints first: no video or audio waiting on the screen, Soplo has something to show. */
function best(ids) {
  const score = (id) => {
    const q = data.byId.get(id);
    return (q.media.type === "image" ? 2 : 0) + (q.hints.length ? 1 : 0);
  };
  return ids.reduce((b, id) => (score(id) > score(b) ? id : b));
}

const base = () => baseSave(ui, "es");

/** `player` plays to `level` (the levels below won); `onQuestion`: its best card picked, every joker playable first. */
function play(save, player, level, opts, onQuestion) {
  save = playTo(data, save, player, level, opts);
  if (!onQuestion) return save;
  const { options } = latestState(save);
  const picked = options.map((id) => pick(structuredClone(save), data, io(), options.indexOf(id)).save);
  const allJokers = (s) => Object.values(view(s, data, io()).jokers).every((j) => j.available);
  const ok = options.filter((_, i) => allJokers(picked[i]));
  return picked[options.indexOf(best(ok.length ? ok : options))];
}

/** History: a won and a lost game, so Player, Victory and Wrong have counts to show. */
function history() {
  let save = play(base(), PLAYERS[1], 13, { mode: "solo" });
  save = play(save, PLAYERS[2], 3, { mode: "solo" }, true);
  ({ save } = answer(save, data, io(), (rightOf(data, save) + 1) % latestState(save).answers.length));
  return save;
}

const flagged = (save, ids) => {
  for (const [i, id] of ids.entries()) {
    const q = data.byId.get(id);
    save.flags[id] = {
      flagged_on: `2026-10-1${i}T20:00:00`, player: PLAYERS[i], level: 3 + i, note: i ? "" : "?", locale: "es",
      shown: { question: q.question, answer: q.answer, wrong_answers: q.wrong_answers },
      ...(i ? { reported_on: "2026-10-12T21:00:00" } : {}),
    };
  }
  return save;
};

const saves = {};
const meta = {};
const done = history();
saves.base = done;

// Gamemaster mode on a question at level 4: Esc cheats, jokers, flag dialog.
saves.question = play(structuredClone(done), PLAYERS[0], 4, { mode: "gamemaster" }, true);
meta.question = { right: rightOf(data, saves.question) };
// Solo on a question: the Esc menu's read-only budget, a correct answer.
saves.solo = play(structuredClone(done), PLAYERS[0], 5, { mode: "solo" }, true);
meta.solo = { right: rightOf(data, saves.solo) };
// The last level's question: victory.
saves.final = play(structuredClone(done), PLAYERS[0], 12, { mode: "solo" }, true);
meta.final = { right: rightOf(data, saves.final) };
// A table at level 3, gamemaster mode: «Difficulty and bundles».
saves.table = play(structuredClone(done), PLAYERS[0], 3, { mode: "gamemaster" });
// Flags for the flag list.
saves.flags = flagged(structuredClone(saves.question), data.pool.slice(0, 2).map((q) => q.id));
// A game on base + colombia, every colombia question seen: the supply notice before level 1.
saves.seen = play(structuredClone(done), PLAYERS[0], 1, { mode: "solo", bundles: ["base", "colombia"] }, true);
({ save: saves.seen } = answer(saves.seen, data, io(), (rightOf(data, saves.seen) + 1) % latestState(saves.seen).answers.length));
saves.seen.seen.push(...data.pool.filter((q) => q.bundle === "colombia")
  .map((q) => ({ question_id: q.id, game_id: 0, seen_on: "2026-10-01T20:00:00" })));
// Every question blocked: the start reason on Bundles (no question for the choice).
saves.blocked = structuredClone(done);
saves.blocked.blocked = data.pool.map((q) => q.id);
// All but a few blocked: short supply, the report on Bundles.
saves.short = structuredClone(done);
saves.short.blocked = data.pool.slice(40).map((q) => q.id);

for (const s of Object.values(saves)) checkVersion(s);
process.stdout.write(JSON.stringify({ saves, meta, players: PLAYERS }));
