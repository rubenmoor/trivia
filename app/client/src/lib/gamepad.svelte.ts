// The gamepad source (plans/14-input.md, IN-4; plan 45): polls standard pads each frame while one
// is connected and dispatches their actions like keys (input.svelte.ts). Any pad drives the game.
import { steam } from "./desktop.ts";
import { BUTTONS, FRESH, held, step, steamStyle, styleOf, type PadState, type PadStyle } from "./gamepad.ts";
import { dispatch, padMap } from "./input.svelte.ts";

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

/** Start polling (Game.svelte, once); `first` runs on every pad action (audio unlock). */
export function listenPads(first: () => void): () => void {
  let frame = 0;

  function poll() {
    frame = requestAnimationFrame(poll);
    const active = !document.hidden && document.hasFocus();
    for (const g of pads()) {
      if (!active) {
        prev.set(g.index, held(g.buttons.length)); // held buttons don't fire on return
        continue;
      }
      const pad = { buttons: g.buttons.map((b) => b.pressed), axes: g.axes };
      const { next, actions } = step(prev.get(g.index) ?? FRESH, pad, padMap(BUTTONS));
      prev.set(g.index, next);
      if (actions.length) void refreshSteam(); // Steam may list a new pad after Chromium does
      for (const intent of actions) {
        padStyle.current = fromSteam ?? styleOf(g.id);
        first();
        dispatch({ ...intent, device: "gamepad" });
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
