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

<section class="screen select">
  <h2 class="title">{t("screen.select.title")}</h2>
  {#if game.options.length === 0}
    <p class="error-box">{t("screen.select.empty")} <Prompt action="menu" /> → {t("action.home")}.</p>
  {/if}
  <Envelopes options={game.options} {picked} {fresh} {busy} seed={{ id: game.id, level: game.level }} {onpick} />
</section>

<style>
  p {
    margin: 0;
  }
</style>
