#!/usr/bin/env node
// trivia-gallery's demo saves (plan 100): built with the engine on the es pool, made-up players.
// Usage: node authoring/tools/gallery_saves.mjs <ui locale> → JSON {saves: {name: save}, meta: {name: {...}}} on stdout.
import { answer, newGame, pick } from "../../app/client/src/engine/game.ts";
import { seededRng } from "../../app/client/src/engine/rng.ts";
import { emptySave, SAVE_VERSION } from "../../app/client/src/engine/state.ts";
import { loadData } from "./engine_data.mjs";

const ui = process.argv[2];
if (!ui) throw new Error("usage: gallery_saves.mjs <ui locale>");
const data = loadData("es");

const PLAYERS = ["Luna", "Mateo", "Sofía", "Max", "Emma"];
let seed = 1;
const io = () => ({ rng: seededRng(seed++), now: "2026-10-13T20:00:00" });
const latest = (save) => save.games.at(-1).state;
const rightOf = (save) => {
  const s = latest(save);
  return s.answers.indexOf(data.byId.get(s.current).answer);
};

/** Image questions with hints first: no video or audio waiting on the screen, Soplo has something to show. */
function best(ids) {
  const score = (id) => {
    const q = data.byId.get(id);
    return (q.media.type === "image" ? 2 : 0) + (q.hints.length ? 1 : 0);
  };
  return ids.reduce((b, id) => (score(id) > score(b) ? id : b));
}

function base() {
  const save = { ...emptySave(), language: { ui, questions: "es" } };
  save.players = PLAYERS.map((name, i) => ({ id: i + 1, name, created_on: `2026-10-0${9 - i}T18:00:00` }));
  return save;
}

/** `player` plays to `level` (the levels below won); `onQuestion`: its best card picked. */
function play(save, player, level, opts, onQuestion) {
  ({ save } = newGame(save, data, io(), player, opts));
  for (let l = 1; l < level; l++) {
    ({ save } = pick(save, data, io(), 0));
    ({ save } = answer(save, data, io(), rightOf(save)));
  }
  if (onQuestion) {
    const s = latest(save);
    ({ save } = pick(save, data, io(), s.options.indexOf(best(s.options))));
  }
  return save;
}

/** History: a won and a lost game, so Player, Victory and Wrong have counts to show. */
function history() {
  let save = play(base(), PLAYERS[1], 13, { mode: "solo" });
  save = play(save, PLAYERS[2], 3, { mode: "solo" }, true);
  ({ save } = answer(save, data, io(), (rightOf(save) + 1) % latest(save).answers.length));
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
meta.question = { right: rightOf(saves.question) };
// Solo on a question: the Esc menu's read-only budget, a correct answer.
saves.solo = play(structuredClone(done), PLAYERS[0], 5, { mode: "solo" }, true);
meta.solo = { right: rightOf(saves.solo) };
// The last level's question: victory.
saves.final = play(structuredClone(done), PLAYERS[0], 12, { mode: "solo" }, true);
meta.final = { right: rightOf(saves.final) };
// A table at level 3, gamemaster mode: «Difficulty and bundles».
saves.table = play(structuredClone(done), PLAYERS[0], 3, { mode: "gamemaster" });
// Flags for the flag list.
saves.flags = flagged(structuredClone(saves.question), data.pool.slice(0, 2).map((q) => q.id));
// Three subcategories seen through: the supply notice before level 1.
const subs = [...new Set(data.pool.map((q) => q.subcategory))].slice(0, 3);
saves.seen = structuredClone(done);
saves.seen.seen = data.pool.filter((q) => subs.includes(q.subcategory))
  .map((q) => ({ question_id: q.id, game_id: 0, seen_on: "2026-10-01T20:00:00" }));
// Every question blocked: the supply report on Choice.
saves.blocked = structuredClone(done);
saves.blocked.blocked = data.pool.map((q) => q.id);

for (const s of Object.values(saves)) if (s.version !== SAVE_VERSION) throw new Error("save version");
process.stdout.write(JSON.stringify({ saves, meta, players: PLAYERS }));
