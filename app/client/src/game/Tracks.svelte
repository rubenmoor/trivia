<script lang="ts">
  // rr-competitive's towers (plan 163): one small tower per seat in join order, its tag below; the turn seat glows
  // in its colour, an out seat is a muted wreck (`final`: keeps its blocks and level, Victory's side tracks).
  import { t } from "../lib/i18n.ts";
  import type { SessionView } from "../lib/seats.ts";
  import SeatTag from "./SeatTag.svelte";
  import Tower from "./Tower.svelte";
  import { seatBlocks, seatColor } from "./seats.ts";

  let {
    session,
    levels,
    seats = session.seats.map((_, i) => i),
    drop = null,
    crumble = null,
    final = false,
  }: {
    session: SessionView;
    levels: number;
    /** The seats shown, by index. */
    seats?: number[];
    /** The seat whose newest block drops (after Correct). */
    drop?: number | null;
    /** The seat whose blocks fall away (Wrong). */
    crumble?: number | null;
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
    <div class="track" class:turn={!final && i === session.turn && s.status === "playing"} class:gone style:--seat={seatColor(i)}>
      <Tower
        filled={gone && !final && crumble !== i ? 0 : seatBlocks(session, i, levels)}
        {levels}
        small
        drop={drop === i}
        crumble={crumble === i}
      />
      <SeatTag {session} seat={i} small />
      {#if final}<span class="at">{t("hud.level", { n: s.level })}</span>{/if}
    </div>
  {/each}
</div>

<style>
  .tracks {
    display: grid;
    grid-template-columns: repeat(var(--cols), auto);
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
  .track.turn {
    box-shadow: 0 0 calc(2.2 * var(--u)) var(--seat);
    background: rgba(255, 255, 255, 0.04);
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
