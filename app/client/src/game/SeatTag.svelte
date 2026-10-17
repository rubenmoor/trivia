<script lang="ts">
  // A seat on screen (plan 163): its colour, name and device glyph; out (not a team's loss): muted and struck, won: a crown.
  // Hud (small), Level's turn line (large), Correct, Wrong, Victory, the tracks and the timed screens.
  import type { SessionView } from "../lib/seats.ts";
  import { seating } from "../lib/seats.svelte.ts";
  import Icon from "./Icon.svelte";
  import SeatDevice from "./SeatDevice.svelte";
  import { seatColor } from "./seats.ts";

  let { session, seat, small = false }: { session: SessionView; seat: number; small?: boolean } = $props();

  const s = $derived(session.seats[seat]);
</script>

{#if s}
  <span class="seat-tag glass" class:small class:out={s.status === "out" || (s.status === "lost" && session.mode !== "rr-coop")} style:--seat={seatColor(seat)}>
    {#if s.status === "won"}<Icon name="crown" />{:else}<span class="dot" aria-hidden="true"></span>{/if}
    <span class="name">{s.player ?? seat + 1}</span>
    <span class="device"><SeatDevice binding={seating.binding[seat] ?? null} /></span>
  </span>
{/if}

<style>
  .seat-tag {
    display: inline-flex;
    align-items: center;
    gap: calc(0.7 * var(--u));
    padding: calc(0.5 * var(--u)) calc(1.4 * var(--u));
    border: 2px solid var(--seat);
    border-radius: calc(1.2 * var(--u));
    font-family: var(--font-display);
    font-size: calc(2.6 * var(--u));
    font-weight: 800;
    color: var(--seat);
    white-space: nowrap;
  }
  .seat-tag.small {
    gap: calc(0.5 * var(--u));
    padding: calc(0.35 * var(--u)) calc(1 * var(--u));
    border-width: 1px;
    border-radius: calc(0.9 * var(--u));
    font-size: calc(1.1 * var(--u));
    font-weight: 700;
  }
  .dot {
    width: 0.55em;
    height: 0.55em;
    border-radius: 50%;
    background: var(--seat);
  }
  .name {
    max-width: 12em;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  .device {
    display: inline-flex;
    color: var(--slate-200);
    font-size: 0.8em;
  }
  .out {
    opacity: 0.5;
    filter: grayscale(1);
  }
  .out .name {
    text-decoration: line-through;
  }
</style>
