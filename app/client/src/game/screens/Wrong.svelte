<script lang="ts">
  // «¡Oh no!»: the tower crumbles, the right answer, a consolation line; back to Start. In a session the
  // answerer's tag; with `onnext` (rr-competitive, one seat out, decision 279) «Seguir» instead of Start.
  import { seatDevice } from "../../lib/gamepad.svelte.ts";
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

  /** rr-competitive: one seat is out, the others play on (decision 279). */
  /** Timed: everyone is out at one round end (decision 280). */
  const nobody = $derived(game.session?.mode === "timed");
  const knockout = $derived(game.session?.mode === "rr-competitive" && last.seat !== undefined);
</script>

<section class="screen result wrong">
  <div class="columns">
    <Tower filled={blocks} {levels} small crumble />
    <div class="stack">
      {#if nobody}
        <h1 class="title bad">{t("screen.timed.nobody")}</h1>
        <div class="muted">
          {#each game.session!.seats as _, i (i)}<SeatTag session={game.session!} seat={i} small />{/each}
        </div>
      {:else if knockout}
        <h1 class="title bad">{t("screen.result.out", { name: game.session!.seats[last.seat!].player ?? last.seat! + 1 })}</h1>
        <SeatTag session={game.session!} seat={last.seat!} />
      {:else}
        <h1 class="title bad">{t("screen.result.wrong")}</h1>
        {#if game.session && last.seat !== undefined}<SeatTag session={game.session} seat={last.seat} />{/if}
      {/if}
      <AnswerPanel {last} label={t("screen.result.answerWas")} />
      {#if !knockout && !nobody}<p class="consolation">{consolation(game.level, levels, game.id)}</p>{/if}
    </div>
  </div>
  {#if onnext}
    <button class="candy" onclick={onnext} disabled={busy} data-focus-default>{t("action.next")} <Prompt action="confirm" device={game.session && game.result === null ? seatDevice(game.session.turn) : null} /></button>
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
  .muted {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: calc(0.6 * var(--u));
    opacity: 0.45;
    filter: grayscale(1);
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
