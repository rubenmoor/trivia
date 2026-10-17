<script lang="ts">
  // «¡Oh no!»: the tower crumbles, the right answer, a consolation line; back to Start. In a session the
  // answerer's tag; with `onnext` (rr-competitive, one seat out, decision 279) «Seguir» instead of Start.
  import { t } from "../../lib/i18n.ts";
  import type { Game } from "../../lib/types.ts";
  import AnswerPanel from "../AnswerPanel.svelte";
  import { consolation } from "../copy.ts";
  import Prompt from "../Prompt.svelte";
  import SeatTag from "../SeatTag.svelte";
  import Tower from "../Tower.svelte";

  let {
    game,
    last,
    levels,
    blocks,
    busy,
    onhome,
    onnext,
  }: {
    game: Game;
    last: NonNullable<Game["last"]>;
    levels: number;
    blocks: number;
    busy: boolean;
    onhome: () => void;
    onnext?: () => void;
  } = $props();
</script>

<section class="screen result wrong">
  <div class="columns">
    <Tower filled={blocks} {levels} small crumble />
    <div class="stack">
      <h1 class="title bad">{t("screen.result.wrong")}</h1>
      {#if game.session && last.seat !== undefined}<SeatTag session={game.session} seat={last.seat} />{/if}
      <AnswerPanel {last} label={t("screen.result.answerWas")} />
      <p class="consolation">{consolation(game.level, levels, game.id)}</p>
    </div>
  </div>
  {#if onnext}
    <button class="candy" onclick={onnext} disabled={busy} data-focus-default>{t("action.next")} <Prompt action="confirm" /></button>
  {:else}
    <button class="candy" onclick={onhome} disabled={busy} data-focus-default>{t("action.home")} <Prompt action="confirm" /></button>
  {/if}
</section>

<style>
  p {
    margin: 0;
  }
  .title {
    animation: arrive 0.6s var(--spring) backwards;
  }
  .bad {
    color: var(--coral);
  }
  .columns {
    display: flex;
    align-items: center;
    gap: calc(4 * var(--u));
  }
  .stack {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: calc(1.4 * var(--u));
  }
  .consolation {
    max-width: calc(56 * var(--u));
    font-family: var(--font-display);
    font-size: calc(2 * var(--u));
    font-weight: 600;
    color: var(--paper);
    animation: arrive 0.6s 1.2s var(--spring) backwards;
  }
</style>
