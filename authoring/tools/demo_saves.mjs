// Demo saves built with the engine: made-up players, seeded games (trivia-gallery, store screenshots, trailer).
import { answer, newGame, pick } from "../../app/client/src/engine/game.ts";
import { seededRng } from "../../app/client/src/engine/rng.ts";
import { emptySave, SAVE_VERSION } from "../../app/client/src/engine/state.ts";

// No family data; the first one plays.
export const PLAYERS = ["Luna", "Mateo", "Sofía", "Max", "Emma"];

// Session saves only: seats 6–8 for the Join screen's scroll (PLAYERS and the Player screen stay as they are).
export const EXTRA_PLAYERS = ["Noa", "Iker", "Vera"];

let seed = 1;
export const resetSeed = () => (seed = 1);
export const io = () => ({ rng: seededRng(seed++), now: "2026-10-13T20:00:00" });

export function baseSave(ui, questions) {
  const save = { ...emptySave(), language: { ui, questions } };
  save.players = PLAYERS.map((name, i) => ({ id: i + 1, name, created_on: `2026-10-0${9 - i}T18:00:00` })); // newest first: PLAYERS[0] tops the list
  return save;
}

/** `save` with the extra names known too, for the Join screen's name dialog with eight seats. */
export function withExtraPlayers(save) {
  const first = save.players.length;
  save.players.push(...EXTRA_PLAYERS.map((name, i) => ({ id: first + i + 1, name, created_on: `2026-10-0${3 - i}T18:00:00` })));
  return save;
}

export const latestState = (save) => save.games.at(-1).state;

/** The right answer's index on the current question. */
export const rightOf = (data, save) => {
  const s = latestState(save);
  return s.answers.indexOf(data.byId.get(s.current).answer);
};

/** `player` starts a game at `level`, the levels below won. */
export function playTo(data, save, player, level, opts) {
  ({ save } = newGame(save, data, io(), player, opts));
  for (let l = 1; l < level; l++) {
    ({ save } = pick(save, data, io(), 0));
    ({ save } = answer(save, data, io(), rightOf(data, save)));
  }
  return save;
}

/** A solo game of PLAYERS[0] at `level`: `qid` on screen, else the table. */
export function gameAt(data, ui, level, qid) {
  let save = playTo(data, baseSave(ui, data.locale), PLAYERS[0], level, { mode: "solo" });
  if (qid) {
    latestState(save).options[0] = qid;
    ({ save } = pick(save, data, io(), 0));
  }
  checkVersion(save);
  return save;
}

export function checkVersion(save) {
  if (save.version !== SAVE_VERSION) throw new Error("save version");
}
