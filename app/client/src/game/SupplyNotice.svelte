<script module lang="ts">
  import type { Outlook } from "../lib/api.ts";

  /** Something to tell before level 1 (decision 31): tight levels, none left, exhausted subcategories. */
  export const worthShowing = (o: Outlook) => o.none || o.tight.length > 0 || o.exhausted.length > 0;
</script>

<script lang="ts">
  // The supply notice (plan 65, decision 31): after «¡A jugar!», before level 1; informational.
  // Enter presses the focused button («¡A jugar!» first), Backspace/Esc go back to the Choice screen.
  import { t } from "../lib/i18n.ts";
  import { focusControl, pushScope } from "../lib/input.svelte.ts";
  import { displayName } from "../lib/names.svelte.ts";
  import Prompt from "./Prompt.svelte";

  let { outlook, onplay, onback }: { outlook: Outlook; onplay: () => void; onback: () => void } = $props();

  let dialog = $state<HTMLDivElement>();
  const ranges = $derived(outlook.tight.map(([lo, hi]) => (lo === hi ? String(lo) : `${lo}–${hi}`)).join(", "));
  const warned = $derived(outlook.none || outlook.tight.length > 0);

  $effect(() => {
    const pop = pushScope({
      name: "supply-notice",
      modal: true,
      root: () => dialog,
      handle: (a) => {
        if (a.type === "back" || a.type === "menu") onback();
        else if (a.type === "confirm") onplay();
        else return false;
        return true;
      },
    });
    focusControl(dialog?.querySelector<HTMLElement>("[data-focus-default]"));
    return pop;
  });
</script>

<div class="backdrop">
  <div class="dialog" bind:this={dialog} role="dialog" aria-labelledby="notice-title">
    <h2 id="notice-title">{t("outlook.title")}</h2>
    {#if outlook.tight.length}<p>{t("outlook.tight", { ranges })}</p>{/if}
    {#if outlook.none}<p>{t("outlook.none")}</p>{/if}
    {#if warned && outlook.bundleHint}<p class="note">{t("outlook.bundle", { bundle: displayName("bundle", outlook.bundleHint) })}</p>{/if}
    {#if outlook.exhausted.length}
      <p>{t("outlook.exhausted", { list: outlook.exhausted.map((s) => displayName("subcategory", s)).join(", ") })}</p>
    {/if}
    <div class="choices">
      <button class="secondary" onclick={onback} data-focus-id="notice-back">{t("action.back")} <Prompt action="back" /></button>
      <button class="candy" onclick={onplay} data-focus-default data-focus-id="notice-play">{t("choice.start")} <Prompt action="confirm" /></button>
    </div>
  </div>
</div>

<style>
  .backdrop {
    position: fixed;
    inset: 0;
    z-index: 40;
    display: grid;
    place-items: center;
    background: var(--dim);
  }
  .dialog {
    display: flex;
    flex-direction: column;
    gap: calc(0.9 * var(--u));
    max-width: calc(60 * var(--u));
    padding: calc(2.4 * var(--u));
    border: 1px solid var(--slate-600);
    border-radius: calc(1.6 * var(--u));
    background: var(--night-700);
    box-shadow: 0 calc(1.5 * var(--u)) calc(4 * var(--u)) rgba(0, 0, 0, 0.6);
    text-align: center;
  }
  h2 {
    margin: 0;
    font-family: var(--font-display);
    font-size: calc(2.6 * var(--u));
    font-weight: 800;
  }
  p {
    margin: 0;
    font-size: calc(1.4 * var(--u));
  }
  .note {
    color: var(--slate-400);
  }
  .choices {
    display: flex;
    justify-content: center;
    gap: calc(1.2 * var(--u));
    margin-top: calc(0.6 * var(--u));
  }
</style>
