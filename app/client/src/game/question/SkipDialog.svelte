<script lang="ts">
  // «Paso»'s choice (plans/09-jokers.md, "Paso", JK-6): 1 skip, 2 skip and purge the subcategory, Esc cancels.
  import { reasonText } from "../../lib/errors.ts";
  import { t } from "../../lib/i18n.ts";
  import { pushScope } from "../../lib/input.svelte.ts";
  import { displayName } from "../../lib/names.svelte.ts";
  import type { Jokers } from "../../lib/types.ts";
  import Icon from "../Icon.svelte";
  import { jokerIcon } from "../jokers.ts";
  import Prompt from "../Prompt.svelte";

  let {
    purge,
    onpick,
    oncancel,
  }: {
    purge: Jokers["skip"]["purge"];
    onpick: (purge: boolean) => void;
    oncancel: () => void;
  } = $props();

  let dialog = $state<HTMLDivElement>();

  $effect(() =>
    pushScope({
      name: "question-skip",
      modal: true,
      root: () => dialog,
      handle: (a) => {
        if (a.type === "back" || a.type === "menu") oncancel();
        else if (a.type === "pick" && a.n === 1) onpick(false);
        else if (a.type === "pick" && a.n === 2 && purge.available) onpick(true);
        else return false;
        return true;
      },
    }),
  );
</script>

<div class="backdrop-dim">
  <div class="dialog glass-strong" bind:this={dialog}>
    <h2><Icon name={jokerIcon("skip")} /> {t("joker.skip.name")}</h2>
    <button class="candy" onclick={() => onpick(false)}>{t("joker.skip.pass")} <Prompt action={{ type: "pick", n: 1 }} hold /></button>
    <button class="secondary purge" onclick={() => onpick(true)} disabled={!purge.available}>
      {t("joker.skip.purge", { name: displayName("subcategory", purge.subcategory) })} <Prompt action={{ type: "pick", n: 2 }} hold />
      {#if purge.reason}<span class="reason">{reasonText(purge.reason)}</span>{/if}
    </button>
    <button class="secondary" onclick={oncancel}>{t("action.cancel")} <Prompt action="menu" pad="back" /></button>
  </div>
</div>

<style>
  .backdrop-dim {
    position: absolute;
    inset: 0;
    z-index: 5;
    display: grid;
    place-items: center;
    background: rgba(5, 8, 16, 0.55);
  }
  .dialog {
    display: flex;
    flex-direction: column;
    align-items: stretch;
    gap: calc(0.9 * var(--u));
    min-width: calc(36 * var(--u));
    padding: calc(1.8 * var(--u)) calc(2.2 * var(--u));
    text-align: center;
    animation: rise 0.35s var(--spring) backwards;
  }
  .dialog h2 {
    margin: 0;
    font-family: var(--font-display);
    font-size: calc(2.6 * var(--u));
  }
  .dialog .candy,
  .dialog .secondary {
    justify-content: center;
  }
  .purge {
    flex-direction: column;
  }
  .reason {
    font-family: var(--font-text);
    font-size: calc(1.1 * var(--u));
    color: var(--slate-200);
  }
</style>
