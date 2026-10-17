<script lang="ts">
  // Level (UI-14): the tower, «Nivel n de 12» and the milestone line; the new block drops after Correct.
  // In a round-robin session also the turn handover: «Turno de» and the turn seat's tag (decision 279).
  import { seatDevice } from "../../lib/gamepad.svelte.ts";
  import { t } from "../../lib/i18n.ts";
  import type { Game } from "../../lib/types.ts";
  import { milestone } from "../copy.ts";
  import Prompt from "../Prompt.svelte";
  import SeatTag from "../SeatTag.svelte";
  import Tower from "../Tower.svelte";

  let {
    game,
    levels,
    blocks,
    drop,
    busy,
    onnext,
  }: { game: Game; levels: number; blocks: number; drop: boolean; busy: boolean; onnext: () => void } = $props();

  const session = $derived(game.session);
</script>

<section class="screen level">
  <Tower filled={blocks} {levels} {drop} />
  <div class="level-text">
    {#if session}
      <div class="turn">
        <p class="turn-line">{t("seat.turn")}</p>
        <SeatTag {session} seat={session.turn} />
      </div>
    {/if}
    <p class="kicker">{t("screen.level.kicker")}</p>
    <h1 class="title big">{game.level} <span class="of">{t("screen.level.of", { n: levels })}</span></h1>
    {#if game.repeat}
      <p class="milestone again">{t("screen.level.again")}</p>
    {:else}
      {@const line = milestone(game.level, levels, game.id)}
      {#if line}<p class="milestone">{line}</p>{/if}
    {/if}
    <button class="secondary hint" onclick={onnext} disabled={busy} data-focus-default>{t("action.next")} <Prompt action="confirm" device={session ? seatDevice(session.turn) : null} /></button>
  </div>
</section>

<style>
  p {
    margin: 0;
  }
  .milestone.again {
    color: var(--coral);
  }
  .level {
    flex-direction: row;
    justify-content: space-evenly;
  }
  .level-text {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: calc(0.8 * var(--u));
    min-width: calc(34 * var(--u));
  }
  .turn {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: calc(0.5 * var(--u));
    margin-bottom: calc(1 * var(--u));
    animation: arrive 0.6s var(--spring) backwards;
  }
  .turn-line {
    font-family: var(--font-display);
    font-size: calc(2 * var(--u));
    font-weight: 700;
    color: var(--paper);
  }
  .kicker {
    font-family: var(--font-display);
    font-size: calc(1.8 * var(--u));
    color: var(--slate-200);
    letter-spacing: 0.2em;
    text-transform: uppercase;
  }
  .title.big {
    font-size: calc(7 * var(--u));
    color: var(--amber);
    animation: arrive 0.7s 0.3s var(--spring) backwards;
  }
  .of {
    font-size: 0.45em;
    color: var(--slate-200);
  }
  .milestone {
    font-family: var(--font-display);
    font-size: calc(2 * var(--u));
    font-weight: 700;
    color: var(--sky);
    animation: arrive 0.7s 0.9s var(--spring) backwards;
  }
  .hint {
    margin-top: calc(1.5 * var(--u));
  }
</style>
