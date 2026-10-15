<script lang="ts">
  // One-time notice before the first mod runs (plan 118, decision 151): Allow or Cancel; Esc/B cancels.
  import { t } from "../lib/i18n.ts";
  import { focusControl, pushScope } from "../lib/input.svelte.ts";
  import Icon from "./Icon.svelte";
  import Prompt from "./Prompt.svelte";

  let { onallow, oncancel }: { onallow: () => void; oncancel: () => void } = $props();

  let dialog = $state<HTMLDivElement>();
  let cancel = $state<HTMLButtonElement>();

  $effect(() => {
    const pop = pushScope({
      name: "mods-notice",
      modal: true,
      whileBusy: true,
      root: () => dialog,
      handle: (a) => {
        if (a.type !== "back" && a.type !== "menu") return false;
        oncancel();
        return true;
      },
    });
    focusControl(cancel);
    return pop;
  });
</script>

<div class="backdrop-dim">
  <div class="dialog glass-strong" bind:this={dialog} role="alertdialog" aria-labelledby="mods-notice-title">
    <h2 id="mods-notice-title">{t("mods.notice.title")}</h2>
    <p>{t("mods.notice.body")}</p>
    <p class="crash">{t("mods.notice.crash")}</p>
    <div class="buttons">
      <button class="candy" onclick={onallow}><Icon name="check" /> {t("mods.notice.allow")}</button>
      <button class="secondary" bind:this={cancel} onclick={oncancel} data-focus-default><Icon name="back" /> {t("action.cancel")} <Prompt action="menu" pad="back" /></button>
    </div>
  </div>
</div>

<style>
  .backdrop-dim {
    position: fixed;
    inset: 0;
    z-index: 50;
    display: grid;
    place-items: center;
    background: rgba(5, 8, 16, 0.55);
  }
  .dialog {
    display: flex;
    flex-direction: column;
    gap: calc(1 * var(--u));
    max-width: calc(52 * var(--u));
    padding: calc(1.8 * var(--u)) calc(2.2 * var(--u));
    animation: arrive 0.35s var(--spring) backwards;
  }
  h2 {
    margin: 0;
    font-family: var(--font-display);
    font-size: calc(2.4 * var(--u));
  }
  p {
    margin: 0;
    font-size: calc(1.3 * var(--u));
    line-height: 1.4;
  }
  .crash {
    color: var(--slate-200);
  }
  .buttons {
    display: flex;
    gap: calc(1.2 * var(--u));
    justify-content: flex-end;
    margin-top: calc(0.6 * var(--u));
  }

  @keyframes arrive {
    from {
      opacity: 0;
      transform: translateY(calc(1.5 * var(--u))) scale(0.96);
    }
  }
</style>
