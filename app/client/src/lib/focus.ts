// Spatial focus (plans/14-input.md, IN-3; plan 44): arrows move DOM focus inside the top scope's root,
// the ring shows on `[data-nav]`, and confirm presses only a control focused by arrows or Tab.
import type { Dir } from "./input.svelte";

export type Rect = { left: number; top: number; width: number; height: number };

/** The candidate nearest to `from` in `dir`, no wrap; -1 if none. Those in line (overlapping on the cross
 * axis) first, then edge distance + 2 × cross-axis gap; ties: the nearer centre. */
export function nearest(from: Rect, dir: Dir, rects: Rect[]): number {
  const h = dir === "left" || dir === "right";
  const lo = (r: Rect) => (h ? r.left : r.top);
  const hi = (r: Rect) => lo(r) + (h ? r.width : r.height);
  const mid = (r: Rect) => (lo(r) + hi(r)) / 2;
  const xlo = (r: Rect) => (h ? r.top : r.left);
  const xhi = (r: Rect) => xlo(r) + (h ? r.height : r.width);
  const xmid = (r: Rect) => (xlo(r) + xhi(r)) / 2;
  const fwd = dir === "right" || dir === "down";
  let best = -1;
  let score = Infinity;
  rects.forEach((r, i) => {
    if (fwd ? lo(r) < mid(from) : hi(r) > mid(from)) return;
    const gap = Math.max(0, fwd ? lo(r) - hi(from) : lo(from) - hi(r));
    const cross = Math.max(0, xlo(r) - xhi(from), xlo(from) - xhi(r));
    const s = (cross > 0 ? 1e6 : 0) + gap + 2 * cross + Math.abs(xmid(r) - xmid(from)) / 1e3;
    if (s < score) [best, score] = [i, s];
  });
  return best;
}

const CANDIDATES = "button, input, a[href], [data-focusable]";

export function candidates(root: HTMLElement): HTMLElement[] {
  return [...root.querySelectorAll<HTMLElement>(CANDIDATES)].filter(
    (el) =>
      !(el as HTMLButtonElement).disabled &&
      el.getAttribute("tabindex") !== "-1" &&
      !el.closest("[data-nofocus]") &&
      el.getClientRects().length > 0,
  );
}

/** The control focused by arrows or Tab: it shows the ring and confirm presses it. */
let shown: HTMLElement | null = null;
/** Per scope: the last shown control's `data-focus-id`, else its index among the candidates. */
const memory = new Map<string, string | number>();

/** Focus `el` with the ring (null: hide it); remembered for `scope` if given. */
export function show(el: HTMLElement | null, scope?: string, root?: HTMLElement) {
  shown?.removeAttribute("data-nav");
  shown = el;
  if (!el) return;
  el.setAttribute("data-nav", "");
  if (document.activeElement !== el) el.focus();
  if (scope && root) memory.set(scope, el.dataset.focusId ?? candidates(root).indexOf(el));
}

function recalled(scope: string, list: HTMLElement[]) {
  const m = memory.get(scope);
  if (typeof m === "string") return list.find((el) => el.dataset.focusId === m);
  return m === undefined ? undefined : list[m];
}

/** Arrows: from the focused control to its nearest neighbour; with nothing focused, the remembered or default one. */
export function navigate(dir: Dir, scope: string, root: HTMLElement): boolean {
  const list = candidates(root);
  const at = list.indexOf(document.activeElement as HTMLElement);
  if (at < 0) {
    const first = recalled(scope, list) ?? list.find((el) => el.hasAttribute("data-focus-default")) ?? list[0];
    if (first) show(first, scope, root);
    return true;
  }
  const i = nearest(list[at].getBoundingClientRect(), dir, list.map((el) => el.getBoundingClientRect()));
  show(i < 0 ? list[at] : list[i], scope, root); // at the edge the ring stays (and shows)
  return true;
}

/** Confirm: clicks the shown control if it's inside `root`; false otherwise (the screen's default runs). */
export function press(root: HTMLElement): boolean {
  const el = shown;
  if (!el || el !== document.activeElement || !root.contains(el) || !candidates(root).includes(el)) return false;
  if (el instanceof HTMLInputElement) return false;
  el.click();
  return true;
}

/** A new scope starts without memory, unless it keeps it (Start). */
export function forget(scope: string) {
  memory.delete(scope);
}

/** For a dialog: what had focus before it opened, given back by the returned function. */
export function opener(): () => void {
  const el = document.activeElement instanceof HTMLElement && document.activeElement !== document.body ? document.activeElement : null;
  const wasShown = el !== null && el === shown;
  return () =>
    setTimeout(() => {
      if (!el?.isConnected || (document.activeElement && document.activeElement !== document.body)) return;
      if (wasShown) show(el);
      else el.focus();
    });
}

let tabbing = false;

/** Every key press (input.svelte.ts's listener): a Tab's focus counts as shown. */
export function keyPressed(key: string) {
  tabbing = key === "Tab";
}

/** Tab counts as shown focus; a click or touch hides the ring. */
export function track(): () => void {
  const onfocus = (e: FocusEvent) => {
    if (tabbing && e.target instanceof HTMLElement) show(e.target);
    else if (e.target !== shown) show(null);
    tabbing = false;
  };
  const onpointer = () => show(null);
  window.addEventListener("focusin", onfocus);
  window.addEventListener("pointerdown", onpointer, true);
  return () => {
    window.removeEventListener("focusin", onfocus);
    window.removeEventListener("pointerdown", onpointer, true);
  };
}
