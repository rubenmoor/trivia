// A scroll box with focus follow (plan 151): `[data-nav-scroll]` for lib/focus.ts, the focused control kept in
// view, a fade at a cut edge (theme.css "Scroll boxes"). Bundles screen, category joker.
import type { Attachment } from "svelte/attachments";

export const scrollBox: Attachment<HTMLElement> = (el) => {
  el.dataset.navScroll = "";
  el.dataset.scrollBox = "";
  const edges = () => {
    el.toggleAttribute("data-cut-top", el.scrollTop > 1);
    el.toggleAttribute("data-cut-bottom", el.scrollTop + el.clientHeight < el.scrollHeight - 1);
  };
  const follow = (e: FocusEvent) => (e.target as HTMLElement).scrollIntoView({ block: "nearest" });
  const ro = new ResizeObserver(edges);
  ro.observe(el);
  el.addEventListener("scroll", edges);
  el.addEventListener("animationend", edges);
  el.addEventListener("focusin", follow);
  return () => {
    ro.disconnect();
    el.removeEventListener("scroll", edges);
    el.removeEventListener("animationend", edges);
    el.removeEventListener("focusin", follow);
  };
};
