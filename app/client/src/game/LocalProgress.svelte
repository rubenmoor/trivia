<script lang="ts">
  // First Steam start (plan 87): this computer's save without Steam, adopted or not; never merged.
  // Enter takes the local progress, the other button starts from scratch.
  import { adoptLocal, type LocalOffer } from "../lib/engine";
  import { errorText } from "../lib/errors";
  import { t } from "../lib/i18n";
  import { focusControl, pushScope } from "../lib/input.svelte";
  import Prompt from "./Prompt.svelte";

  let { offer, onfresh }: { offer: LocalOffer; onfresh: () => void } = $props();

  let dialog = $state<HTMLDivElement>();
  let busy = $state(false);
  let error = $state<string | null>(null);

  async function use() {
    if (busy) return;
    busy = true;
    try {
      await adoptLocal();
    } catch (e) {
      error = errorText(e);
      busy = false;
    }
  }

  $effect(() => {
    const pop = pushScope({
      name: "local-progress",
      modal: true,
      root: () => dialog,
      handle: (a) => {
        if (a.type === "confirm") use();
        else return a.type === "menu" || a.type === "back"; // a choice is required
        return true;
      },
    });
    focusControl(dialog?.querySelector<HTMLElement>("[data-focus-default]"));
    return pop;
  });
</script>

<div class="backdrop">
  <div class="dialog" bind:this={dialog} role="dialog" aria-labelledby="local-title">
    <h2 id="local-title">{t("save.local.title")}</h2>
    <p>{t("save.local.body", { players: t("save.local.players", { n: offer.players }), games: t("save.local.games", { n: offer.games }) })}</p>
    {#if error}<p class="error">{error}</p>{/if}
    <div class="choices">
      <button class="secondary" onclick={onfresh} disabled={busy} data-focus-id="local-fresh">{t("save.local.fresh")}</button>
      <button class="candy" onclick={use} disabled={busy} data-focus-default data-focus-id="local-use">{t("save.local.use")} <Prompt action="confirm" /></button>
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
    background: rgba(5, 8, 16, 0.72);
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
  .error {
    color: var(--slate-400);
  }
  .choices {
    display: flex;
    justify-content: center;
    gap: calc(1.2 * var(--u));
    margin-top: calc(0.6 * var(--u));
  }
</style>
