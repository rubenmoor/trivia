<script lang="ts">
  // Select (UI-11): the envelopes on the table; the picked one tears open.
  import { t } from "../../lib/i18n.ts";
  import type { Game } from "../../lib/types.ts";
  import Envelopes from "../Envelopes.svelte";
  import Prompt from "../Prompt.svelte";

  let {
    game,
    picked,
    fresh,
    busy,
    onpick,
  }: { game: Game; picked: number | null; fresh: Set<number>; busy: boolean; onpick: (i: number) => void } = $props();
</script>

<section class="select">
  <h2 class="title">{t("screen.select.title")}</h2>
  {#if game.options.length === 0}
    <p class="error-box">{t("screen.select.empty")} <Prompt action="menu" /> → {t("action.home")}.</p>
  {/if}
  <Envelopes options={game.options} {picked} {fresh} {busy} seed={{ id: game.id, level: game.level }} {onpick} />
</section>

<style>
  section {
    position: absolute;
    inset: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: calc(1.4 * var(--u));
    padding: var(--safe-y) var(--safe-x);
    text-align: center;
  }
  p {
    margin: 0;
  }
  .error-box {
    color: var(--coral);
    background: rgba(40, 10, 18, 0.9);
    border: 1px solid var(--coral);
    border-radius: calc(0.6 * var(--u));
    padding: calc(0.5 * var(--u)) calc(1 * var(--u));
    font-size: calc(1.1 * var(--u));
  }
</style>
