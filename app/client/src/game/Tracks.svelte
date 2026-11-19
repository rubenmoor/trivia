<script lang="ts">
  // Victory's side tracks (plan 163): one small tower per seat, its tag below; an out seat is a muted wreck (`final`: keeps its blocks and level).
  import { t } from "../lib/i18n.ts";
  import type { SessionView } from "../lib/seats.ts";
  import SeatTag from "./SeatTag.svelte";
  import Tower from "./Tower.svelte";
  import { seatBlocks, seatColor } from "./seats.ts";

  let {
    session,
    levels,
    seats = session.seats.map((_, i) => i),
    final = false,
  }: {
    session: SessionView;
    levels: number;
    /** The seats shown, by index. */
    seats?: number[];
    final?: boolean;
  } = $props();

  /** `final`: one row, shrunk with the number of seats so Victory's column fits at Deck size. */
  const cols = $derived(final || seats.length <= 4 ? seats.length : seats.length <= 8 ? Math.ceil(seats.length / 2) : 8);
  const zoom = $derived(!final || seats.length <= 2 ? 1 : seats.length <= 4 ? 0.85 : 0.7);
  const width = $derived(seats.length <= 4 ? 14 : seats.length <= 8 ? 11 : 7.5);
</script>

<div class="tracks" style:--cols={cols} style:zoom={zoom} style:--tower-w="calc({final ? 8 : width} * var(--u))">
  {#each seats as i (i)}
    {@const s = session.seats[i]}
    {@const gone = s.status === "out" || s.status === "lost"}
    <div class="track" class:gone style:--seat={seatColor(i)}>
      <Tower
        filled={gone && !final ? 0 : seatBlocks(session, i, levels)}
        {levels}
        small
      />
      <SeatTag {session} seat={i} small />
      {#if final}<span class="at">{t("hud.level", { n: s.level })}</span>{/if}
    </div>
  {/each}
</div>

<style>
  .tracks {
    display: grid;
    grid-template-columns: repeat(var(--cols), calc(16 * var(--u)));
    align-items: end;
    justify-content: center;
    gap: calc(2.4 * var(--u)) calc(2 * var(--u));
  }
  .track {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: calc(0.7 * var(--u));
    padding: calc(0.6 * var(--u));
    border-radius: calc(1.2 * var(--u));
    transition:
      box-shadow 0.3s,
      opacity 0.3s;
  }
  .track.gone {
    opacity: 0.6;
  }
  .at {
    font-family: var(--font-display);
    font-size: calc(1.1 * var(--u));
    font-weight: 700;
    color: var(--slate-200);
  }
</style>
