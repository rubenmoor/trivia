// Mod screens (plan 117): per screen ours or the top mod's replacement, read once when Game.svelte mounts.
import type { Component } from "svelte";
import { hookFailed, registrations, type DomRender, type Registration, type ScreenName, type ScreenReg } from "../../lib/mods.ts";
import DomScreen from "./DomScreen.svelte";

/** The registration behind each replaced screen. */
const used = new Map<string, Registration<ScreenReg>>();

/** A plain-DOM screen as a component: `DomScreen` with the screen's live props. */
const domScreen = (render: DomRender): Component<Record<string, unknown>> => (internals, props) =>
  DomScreen(internals, { render, props });

/** The top mod's replacement of `name`, else ours. */
export function screenFor<C extends Component<never>>(name: ScreenName, ours: C): C {
  const reg = registrations<ScreenReg>(`screen:${name}`).at(-1);
  if (!reg) return ours;
  used.set(name, reg);
  return ("render" in reg.fn ? domScreen(reg.fn.render) : reg.fn.component) as unknown as C;
}

/** A replacement threw: reported and dropped, the caller falls back to ours. False if `name` is ours. */
export function screenFailed(name: string, e: unknown): boolean {
  const reg = used.get(name);
  if (!reg) return false;
  used.delete(name);
  hookFailed(reg, e);
  return true;
}
