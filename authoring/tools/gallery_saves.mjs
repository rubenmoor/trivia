#!/usr/bin/env node
// trivia-gallery's demo saves (plan 100): built with the engine on the es pool, made-up players.
// Usage: node authoring/tools/gallery_saves.mjs <ui locale> → JSON {saves: {name: save}, meta: {name: {...}}} on stdout.
import { QUESTION_MS } from "../../app/client/src/engine/choice.ts";
import { answer, claim, expire, newSession, pick, show, view } from "../../app/client/src/engine/game.ts";
import { baseSave, EXTRA_PLAYERS, checkVersion, io, latestState, PLAYERS, playTo, rightOf, withExtraPlayers } from "./demo_saves.mjs";
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
// A UI language with a pool of its own plays it (engine.ts localeOf), so these three also mark and block from it.
const lpool = (loadData(ui) ?? data).pool;
const midlevels = ui === "es" ? [] : lpool.filter((q) => q.bundle === "base" && q.difficulty >= 5 && q.difficulty <= 9).slice(1);
// A game on base + colombia, every colombia question seen: the supply notice before level 1.
saves.seen = play(structuredClone(done), PLAYERS[0], 1, { mode: "solo", bundles: ["base", "colombia"] }, true);
({ save: saves.seen } = answer(saves.seen, data, io(), (rightOf(data, saves.seen) + 1) % latestState(saves.seen).answers.length));
saves.seen.seen.push(...data.pool.filter((q) => q.bundle === "colombia").concat(midlevels)
  .map((q) => ({ question_id: q.id, game_id: 0, seen_on: "2026-10-01T20:00:00" })));
// Every question blocked: the start reason on Bundles (no question for the choice).
saves.blocked = structuredClone(done);
saves.blocked.blocked = [...new Set([...data.pool, ...lpool].map((q) => q.id))];
// All but a few blocked: short supply, the report on Bundles.
saves.short = structuredClone(done);
saves.short.blocked = [...new Set([...data.pool.slice(40), ...lpool.slice(40)].map((q) => q.id))];

// Eight known names: the Join screen with up to eight seats.
saves.crowd = withExtraPlayers(structuredClone(done));
// A running round-robin co-op session of three: Start's resume line, the Esc menu. `bound`: the seats' devices
// (pad 0, pad 1, keyboard and mouse), written to sessionStorage by the page (plan 161).
saves.session = newSession(structuredClone(done), data, io(), PLAYERS.slice(0, 3), { mode: "rr-coop" }).save;
meta.session = { id: saves.session.games.at(-1).id, bound: [{ pad: 0 }, { pad: 1 }, "kbm"] };

// Round-robin scenes (plans 163, 165): built with the engine's session actions, one acting seat per call.
const gameRow = (save) => save.games.at(-1);
const turnOf = (save) => gameRow(save).turn;
/** The seat's own game in rr-competitive, else the shared one. */
const seatState = (save, seat) => gameRow(save).seats[seat].state ?? gameRow(save).state;
const rightIn = (save, seat) => {
  const st = seatState(save, seat);
  return st.answers.indexOf(data.byId.get(st.current).answer);
};

/** The turn seat picks card 0 and answers: right, or wrong when `rightly` is false. */
function turnAnswers(save, rightly = true) {
  const seat = turnOf(save);
  ({ save } = pick(save, data, io(), 0, seat));
  const right = rightIn(save, seat);
  ({ save } = answer(save, data, io(), rightly ? right : (right + 1) % 4, seat));
  return save;
}

/** A session of `n` seats; each entry of `plan` is one answer by whoever has the turn (false: wrong). */
function session(mode, n, plan = []) {
  let save = newSession(structuredClone(done), data, io(), PLAYERS.slice(0, n), { mode }).save;
  for (const rightly of plan) save = turnAnswers(save, rightly);
  return save;
}

/** The turn seat has its question on screen and keyboard and mouse (the clicks of the page) are its device; the
 * other seats hold pads (`bound` goes to sessionStorage, plan 161). */
function onQuestion(save) {
  const seat = turnOf(save);
  ({ save } = pick(save, data, io(), 0, seat));
  const n = gameRow(save).seats.length;
  let pad = 0;
  return { save, meta: { id: gameRow(save).id, right: rightIn(save, seat),
    bound: Array.from({ length: n }, (_, i) => (i === seat ? "kbm" : { pad: pad++ })) } };
}
/** The table of the turn seat, bound the same way. */
function onTable(save) {
  const n = gameRow(save).seats.length;
  let pad = 0;
  return { save, meta: { id: gameRow(save).id, bound: Array.from({ length: n }, (_, i) => (i === turnOf(save) ? "kbm" : { pad: pad++ })) } };
}
const scene = (name, { save, meta: m }) => ((saves[name] = save), (meta[name] = m));
const rounds = (n, rightly = true) => Array(n).fill(rightly);

// rr-coop: level 4 after three answers (a table: Level, Select); its question (Correct, the team's loss); the last level.
scene("coop", onTable(session("rr-coop", 3, rounds(3))));
scene("coop-q", onQuestion(session("rr-coop", 3, rounds(3))));
scene("coop-q12", onQuestion(session("rr-coop", 3, rounds(11))));
// rr-competitive: three seats, the second one out after a wrong answer; level 3 for the others.
const mixed = [true, false, true, true, true, true];
scene("comp", onTable(session("rr-competitive", 3, mixed)));
scene("comp-q", onQuestion(session("rr-competitive", 3, rounds(1))));
// Seat 0 on the last level of its own game (the others each answered 11 times).
scene("comp-q12", onQuestion(session("rr-competitive", 3, rounds(33))));
// Two seats: the second one's question, a wrong answer leaves the first one standing.
scene("comp-last", onQuestion(session("rr-competitive", 2, rounds(5))));

// Timed scenes (plans 164, 165): every action at an explicit epoch ms; `meta.now` the last one, the page clock is set
// from it (plus the seconds a shot needs).
let ms = Date.UTC(2026, 9, 13, 20);
const tio = (dt) => ({ ...io(), ms: (ms += dt) });
const timedRight = (save) => {
  const st = gameRow(save).state;
  return st.answers.indexOf(data.byId.get(st.current).answer);
};
/** The question fades in a second after the last action: its 30 s run. */
const shown = (save) => show(save, data, tio(1000)).save;
/** Unclaimed: its 30 s run out. */
const timeUp = (save) => expire(shown(save), data, tio(QUESTION_MS + 1000)).save;
/** `seat` claims after 3 s and answers a second later: right, or wrong (out) when `rightly` is false. */
function claims(save, seat, rightly = true) {
  save = claim(shown(save), data, tio(3000), seat).save;
  return answer(save, data, tio(1000), (timedRight(save) + (rightly ? 0 : 1)) % 4, seat).save;
}
/** A timed session of `n` seats; `steps` run in order on it. */
function timedSession(n, steps) {
  let save = newSession(structuredClone(done), data, tio(0), PLAYERS.slice(0, n), { mode: "timed" }).save;
  for (const step of steps) save = step(save);
  return save;
}
/** Seat 0 is keyboard and mouse, the others hold pads. */
const timedScene = (save, extra = {}) => ({
  save, meta: { id: gameRow(save).id, now: ms, bound: gameRow(save).seats.map((_, i) => (i ? { pad: i - 1 } : "kbm")), ...extra },
});
const by = (seat, rightly) => (s) => claims(s, seat, rightly);
const round = (...steps) => steps;

// Four seats, round 1: Max out (wrong), Luna and Mateo right, the last question on screen: Sofía's last chance.
scene("timed-q", timedScene(timedSession(4, round(by(3, false), by(0), by(1), shown))));
// Three seats: Sofía on her last heart, Mateo on his last chance in round 3.
scene("timed-heart", timedScene(timedSession(3, [
  ...round(by(0), by(1), timeUp), ...round(by(0), by(1), timeUp), ...round(by(0), timeUp, shown),
])));
// Three seats on one heart each, Luna out in round 3: both left at risk on the round's last question.
scene("timed-risk", timedScene(timedSession(3, [
  ...round(timeUp, timeUp, timeUp), ...round(timeUp, timeUp, timeUp), ...round(by(0, false), timeUp, shown),
])));
// Two seats right every round up to round 12: the sudden-death round screen; its question claimed by Luna.
const toTwelve = Array.from({ length: 11 }, () => round(by(0), by(1))).flat();
scene("timed-12", timedScene(timedSession(2, toTwelve)));
const last = claim(shown(saves["timed-12"]), data, tio(3000), 0).save;
scene("timed-12-claim", timedScene(last, { right: timedRight(last) }));

for (const s of Object.values(saves)) checkVersion(s);
process.stdout.write(JSON.stringify({ saves, meta, players: [...PLAYERS, ...EXTRA_PLAYERS] }));
