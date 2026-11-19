<script lang="ts">
  // Turn handover (decision 747): the last player small and grey, replaced by the next one big and bright; no button, Game.svelte goes on by itself.
  import { t } from "../../lib/i18n.ts";
  import type { SessionView } from "../../lib/seats.ts";
  import SeatTag from "../SeatTag.svelte";

  let { session, from }: { session: SessionView; from: number } = $props();
</script>

<section class="screen turn-screen">
  <div class="old"><SeatTag {session} seat={from} small /></div>
  <p class="turn-line">{t("seat.turn")}</p>
  <div class="now"><SeatTag {session} seat={session.turn} /></div>
</section>

<style>
  .turn-screen {
    gap: calc(2 * var(--u));
  }
  .old {
    opacity: 0.35;
    filter: grayscale(1);
    animation: leave 0.6s ease-in 0.2s forwards;
  }
  .turn-line {
    margin: 0;
    font-family: var(--font-display);
    font-size: calc(3 * var(--u));
    font-weight: 700;
    color: var(--paper);
    animation: arrive 0.6s 0.5s var(--spring) backwards;
  }
  .now {
    display: flex;
    transform: scale(1.8);
    transform-origin: top center;
    margin-bottom: calc(5 * var(--u));
    animation: enter 0.7s 0.5s var(--spring) backwards;
  }
  @keyframes leave {
    to {
      opacity: 0;
      transform: scale(0.7) translateY(calc(-2 * var(--u)));
    }
  }
  @keyframes enter {
    from {
      opacity: 0;
      transform: scale(0.8);
    }
  }
</style>
