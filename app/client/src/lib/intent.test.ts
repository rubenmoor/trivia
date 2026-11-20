import { test } from "node:test";
import assert from "node:assert/strict";
import { activation, toIntent } from "./intent.ts";

const key = (k: string) => ({ key: k, ctrlKey: false, metaKey: false, altKey: false });

test("keys → intents: Enter is confirm, Space is press, also in a text field Enter confirms and Space types (task 2114)", () => {
  assert.deepEqual(toIntent(key("Enter")), { type: "confirm" });
  assert.deepEqual(toIntent(key(" ")), { type: "press" });
  assert.deepEqual(toIntent(key("Enter"), {}, true), { type: "confirm" });
  assert.equal(toIntent(key(" "), {}, true), null);
  assert.equal(toIntent(key("a"), {}, true), null);
  // a scope's Space (a timed claim) beats press
  assert.deepEqual(toIntent(key(" "), { " ": { type: "claim" } }), { type: "claim" });
  assert.deepEqual(toIntent(key("Backspace")), { type: "back" });
  assert.deepEqual(toIntent(key("Escape")), { type: "menu" });
  assert.deepEqual(toIntent(key("g"), { g: { type: "letter", key: "g" } }), { type: "letter", key: "g" });
  assert.deepEqual(toIntent(key("3")), { type: "pick", n: 3 });
  assert.deepEqual(toIntent(key("m"), {}, false, "M"), { type: "flag" });
  assert.equal(toIntent({ ...key(" "), ctrlKey: true }), null);
});

test("Enter on a screen with a primary action clicks it whatever has focus; Space presses the ring's control only", () => {
  for (const focused of [true, false]) assert.equal(activation("confirm", "yes", focused), "primary"); // a tile, a switch, a button, nothing
  assert.equal(activation("press", "yes", true), "focused"); // Space picks the tile / toggles the bundle
  assert.equal(activation("press", "yes", false), "press"); // Space on nothing (or a text field): never the primary action
  // the scope takes this confirm itself (an unbound pad's A joins)
  assert.equal(activation("confirm", "later", true), "confirm");
});

test("a list screen (no primary action): Enter and Space press the ring's control, else the screen's default", () => {
  assert.equal(activation("confirm", "no", true), "focused");
  assert.equal(activation("press", "no", true), "focused");
  assert.equal(activation("confirm", "no", false), "confirm");
  assert.equal(activation("press", "no", false), "confirm");
});

test("in-game Question (task 2115): Enter submits whatever has the ring, Space locks the ringed tile; an armed joker is a list", () => {
  assert.equal(activation("confirm", "yes", true), "primary"); // «Respuesta final», also with the ring on a tile
  assert.equal(activation("press", "yes", true), "focused"); // lock / unlock the tile, or press a joker token
  assert.equal(activation("press", "yes", false), "press"); // nothing to press: nothing happens
  assert.equal(activation("confirm", "no", false), "confirm"); // armed joker, Francotirador: Enter fires
  assert.equal(activation("press", "no", false), "confirm"); // and so does Space
});

test("an IME's Process or a non-Latin key falls back to e.code (plan 142)", () => {
  const ime = (code: string, k = "Process") => ({ ...key(k), code, isComposing: true });
  assert.deepEqual(toIntent(ime("KeyG"), { g: { type: "letter", key: "g" } }), { type: "letter", key: "g" });
  assert.deepEqual(toIntent(ime("Digit3")), { type: "pick", n: 3 });
  assert.deepEqual(toIntent({ ...key("ち"), code: "KeyA" }, { a: { type: "pick", n: 1 } }), { type: "pick", n: 1 });
  assert.equal(toIntent(ime("KeyG"), { g: { type: "letter", key: "g" } }, true), null);
  assert.equal(toIntent(ime("Comma")), null);
  assert.deepEqual(toIntent({ ...key("a"), code: "KeyQ" }, { a: { type: "letter", key: "a" } }), { type: "letter", key: "a" }); // AZERTY: e.key wins
});
