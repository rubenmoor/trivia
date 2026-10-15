<script lang="ts">
  // Answers off (D-105): «Siguiente ronda» after a reveal, «Cuestionario completado» after the last level; neutral, no win or loss.
  import { t } from "../../lib/i18n.ts";
  import type { Game } from "../../lib/types.ts";
  import AnswerPanel from "../AnswerPanel.svelte";
  import Fireworks from "../Fireworks.svelte";
  import Prompt from "../Prompt.svelte";

  let {
    last,
    completed,
    busy,
    onnext,
  }: { last: NonNullable<Game["last"]>; completed: boolean; busy: boolean; onnext: () => void } = $props();
</script>

{#if completed}<Fireworks />{/if}
<section class="screen result">
  <h1 class="title">{t(completed ? "screen.result.completed" : "screen.result.next")}</h1>
  <AnswerPanel {last} />
  {#if completed}
    <button class="candy" onclick={onnext} disabled={busy} data-focus-default>{t("action.home")} <Prompt action="confirm" /></button>
  {:else}
    <button class="secondary hint" onclick={onnext} disabled={busy} data-focus-default>{t("action.next")} <Prompt action="confirm" /></button>
  {/if}
</section>

<style>
  .title {
    color: var(--sky);
    animation: arrive 0.6s var(--spring) backwards;
  }
  .hint {
    margin-top: calc(1.5 * var(--u));
  }
</style>
