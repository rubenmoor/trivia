<script lang="ts">
  // A seat's pad is gone (decision 289): shown when the seat is needed. A on any pad bound to no seat takes it.
  // The clock of a timed game waits meanwhile; the Esc menu stays reachable.
  import { onMount } from "svelte";
  import { t } from "../lib/i18n.ts";
  import { padStyle } from "../lib/gamepad.svelte.ts";
  import { pushScope } from "../lib/input.svelte.ts";
  import { holdPause } from "../lib/pause.ts";
  import { unboundPad } from "../lib/seats.ts";
  import { rebindSeat, seating } from "../lib/seats.svelte.ts";
  import type { Game } from "../lib/types.ts";
  import Glyph from "./Glyph.svelte";
  import Prompt from "./Prompt.svelte";

  let { seat, onmenu, onpause }: { seat: number; onmenu: () => void; onpause: (game: Game | null) => void } = $props();

  const name = $derived(seating.view?.seats[seat]?.player ?? String(seat + 1));

  onMount(() => holdPause(onpause));

  $effect(() =>
    pushScope({
      name: "seat-lost",
      modal: true,
      shared: true,
      whileBusy: true,
      handle: (a) => {
        if (a.type === "menu") onmenu();
        else {
          const pad = unboundPad(a.source, a, seating.binding);
          if (pad === null) return false;
          rebindSeat(seat, pad);
        }
        return true;
      },
    }),
  );
</script>

<div class="backdrop">
  <div class="dialog" role="alertdialog" aria-labelledby="seat-lost-title">
    <h2 id="seat-lost-title">{t("seat.lostTitle", { name })}</h2>
    <p>{t("seat.lostBody")}</p>
    <div class="choices">
      <button class="secondary" onclick={onmenu}>{t("overlay.title")} <Prompt action="menu" /></button>
      <span class="take"><Glyph button={0} set={padStyle.current} size="1.7em" /> {t("seat.take")}</span>
    </div>
  </div>
</div>

<style>
  .backdrop {
    position: fixed;
    inset: 0;
    z-index: 38; /* under the Esc menu (40), which stays reachable */
    display: grid;
    place-items: center;
    background: var(--dim);
  }
  .dialog {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: calc(1 * var(--u));
    max-width: calc(60 * var(--u));
    padding: calc(2.4 * var(--u));
    border: 1px solid var(--slate-600);
    border-radius: calc(1.6 * var(--u));
    background: var(--night-700);
  }
  h2 {
    margin: 0;
    font-family: var(--font-display);
    font-size: calc(2.6 * var(--u));
    font-weight: 800;
  }
  p {
    margin: 0;
    color: var(--slate-200);
  }
  .choices {
    display: flex;
    align-items: center;
    gap: calc(2 * var(--u));
  }
  .take {
    display: inline-flex;
    align-items: center;
    gap: 0.4em;
  }
</style>
