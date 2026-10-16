// The gamepad source (plans/14-input.md, IN-4; plan 45): polls standard pads each frame while one
// is connected and dispatches their actions like keys (input.svelte.ts). Any pad drives the game; in a local
// multiplayer session only a pad whose seat may act (plan 161).
import { steam } from "./desktop.ts";
import { BUTTONS, CLAIM_PAD, FRESH, held, step, steamStyle, styleOf, type PadState, type PadStyle } from "./gamepad.ts";
import { show } from "./focus.ts";
import { dispatch, gate, keyLabel, lastDevice, padMap, release, resetTravel, type Device } from "./input.svelte.ts";
import { seating, unbindPad } from "./seats.svelte.ts";

/** The glyph set of the pad that acted last (IN-5). */
export const padStyle = $state({ current: "xbox" as PadStyle });

const prev = new Map<number, PadState>();
const warned = new Set<string>();
/** Under Steam Input the pads' real types (plan 85); null → `Gamepad.id`. */
let fromSteam: PadStyle | null = null;

async function refreshSteam() {
  if (steam?.available) fromSteam = steamStyle(await steam.inputTypes().catch(() => null));
}

function pads() {
  return navigator.getGamepads().filter((g): g is Gamepad => g !== null && g.mapping === "standard");
}

/** A pad's glyph set: all of Steam's pads PlayStation → PlayStation, else its id (Steam per handle unproven,
 * plans/14-input.md section 3). */
const styleFor = (g: Gamepad): PadStyle => (fromSteam === "playstation" ? fromSteam : styleOf(g.id));

/** The glyph set of the pad at `index`; `xbox` while it is gone. */
function padStyleOf(index: number): PadStyle {
  const g = navigator.getGamepads()[index];
  return g ? styleFor(g) : "xbox";
}

/** A seat's device for its prompts (turn banner, claim prompts): its pad's glyph set, else the keyboard; null: unbound.
 * @public turn banner and timed screens (plans 163, 164) */
export function seatDevice(seat: number): { device: Device; style?: PadStyle } | null {
  const b = seating.binding[seat];
  if (!b) return null;
  return typeof b === "object" && "pad" in b ? { device: "gamepad", style: padStyleOf(b.pad) } : { device: "keyboard" };
}

/** What a seat's claim prompt shows (decision 290): the bumpers' glyphs (`buttons`) of its pad, else a text («Espacio»
 * or the picked key); null: unbound.
 * @public timed screens (plan 164) */
export function claimLabel(seat: number): { buttons: number[]; style: PadStyle } | { text: string } | null {
  const b = seating.binding[seat];
  if (!b) return null;
  if (typeof b === "object" && "pad" in b) return { buttons: Object.keys(CLAIM_PAD).map(Number), style: padStyleOf(b.pad) };
  return { text: keyLabel({ type: "claim", key: typeof b === "object" && "key" in b ? b.key : undefined }) ?? "" };
}

/** A switch without an action: the focused control gets the ring if none has it (as a key press does). */
function showFocused() {
  const el = document.activeElement;
  if (el instanceof HTMLElement && el !== document.body && !document.querySelector("[data-nav]")) show(el);
}

/** Start polling (Game.svelte, once); `first` runs on every pad action (audio unlock). */
export function listenPads(first: () => void): () => void {
  let frame = 0;

  function poll() {
    frame = requestAnimationFrame(poll);
    const active = !document.hidden && document.hasFocus();
    if (!active) release();
    for (const g of pads()) {
      if (!active) {
        prev.set(g.index, held(g.buttons.length)); // held buttons don't fire on return
        continue;
      }
      const pad = { buttons: g.buttons.map((b) => b.pressed), axes: g.axes };
      const { next, actions, touched } = step(prev.get(g.index) ?? FRESH, pad, padMap(BUTTONS));
      prev.set(g.index, next);
      if (actions.length) void refreshSteam(); // Steam may list a new pad after Chromium does
      const source = { pad: g.index };
      const acts = touched && gate(source).ok; // in a session a pad that may not act leaves the prompts alone
      if (acts) {
        padStyle.current = styleFor(g);
        resetTravel();
      }
      if (touched && !actions.length) {
        first();
        if (acts) {
          lastDevice.current = "gamepad";
          showFocused();
        }
      }
      for (const intent of actions) {
        if (gate(source, intent).ok) padStyle.current = styleFor(g);
        first();
        dispatch({ ...intent, device: "gamepad", source });
      }
    }
  }

  function run() {
    if (!frame && pads().length) frame = requestAnimationFrame(poll);
  }

  function connected(e: GamepadEvent) {
    const g = e.gamepad;
    if (g.mapping !== "standard" && !warned.has(g.id)) {
      warned.add(g.id);
      console.warn(`Gamepad without standard mapping, ignored: ${g.id}`);
    }
    void refreshSteam();
    run();
  }

  function disconnected(e: GamepadEvent) {
    prev.delete(e.gamepad.index);
    unbindPad(e.gamepad.index);
    release();
    void refreshSteam();
    if (pads().length) return;
    cancelAnimationFrame(frame);
    frame = 0;
  }

  window.addEventListener("gamepadconnected", connected);
  window.addEventListener("gamepaddisconnected", disconnected);
  void refreshSteam();
  run();
  return () => {
    window.removeEventListener("gamepadconnected", connected);
    window.removeEventListener("gamepaddisconnected", disconnected);
    cancelAnimationFrame(frame);
    frame = 0;
  };
}
