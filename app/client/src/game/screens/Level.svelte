<script lang="ts">
  // Level (UI-14): the tower (rr-competitive: every seat's), «Nivel n de 12» and the milestone line; the new block drops after Correct.
  // In a round-robin session also the turn handover: «Turno de» and the turn seat's tag (decision 279).
  // Timed: the round screen (decision 296): «Ronda n de 12», every seat's hearts (the ones just lost crack), then 3-2-1.
  import { onMount } from "svelte";
  import { LIVES } from "../../engine/choice.ts";
  import { seatDevice } from "../../lib/gamepad.svelte.ts";
  import { t } from "../../lib/i18n.ts";
  import type { SessionView } from "../../lib/seats.ts";
  import type { Game } from "../../lib/types.ts";
  import { milestone } from "../copy.ts";
  import Hearts from "../Hearts.svelte";
  import Prompt from "../Prompt.svelte";
  import SeatTag from "../SeatTag.svelte";
  import Tower from "../Tower.svelte";
  import Tracks from "../Tracks.svelte";
  import { sfx } from "../sound.svelte.ts";
  import { COUNTDOWN_STEP_MS, FADE_MS, ROUND_HOLD_MS, sleep } from "../timing.ts";

  let {
    game,
    levels,
    blocks,
    drop,
    busy,
    before = null,
    paused = false,
    onnext,
  }: {
    game: Game;
    levels: number;
    blocks: number;
    drop: boolean;
    busy: boolean;
    /** Timed: the seats before the last round's end, for the hearts lost there. */
    before?: SessionView | null;
    /** Timed: the Esc menu is open, the countdown waits. */
    paused?: boolean;
    onnext: () => void;
  } = $props();

  const session = $derived(game.session);
  const timed = $derived(session?.timed ?? null);
  const lost = (i: number) => Math.max(0, (before?.seats[i]?.lives ?? LIVES) - (session?.seats[i]?.lives ?? LIVES));
  /** The countdown's number; null before it. */
  let count = $state<number | null>(null);

  /** Waits ms, but not while the Esc menu is open or a transition runs. */
  async function wait(ms: number, alive: () => boolean) {
    for (let left = ms; left > 0 && alive(); ) {
      await sleep(100);
      if (!paused && !busy) left -= 100;
    }
  }

  onMount(() => {
    if (!timed) return;
    let alive = true;
    const on = () => alive;
    if (session!.seats.some((_, i) => lost(i) > 0)) setTimeout(() => alive && sfx("glass-break"), FADE_MS + 900); // the crack in Hearts.svelte
    (async () => {
      await wait(FADE_MS + ROUND_HOLD_MS, on);
      for (let n = 3; n > 0 && alive; n--) {
        count = n;
        sfx("tick");
        await wait(COUNTDOWN_STEP_MS, on);
      }
      if (alive) onnext();
    })();
    return () => (alive = false);
  });
</script>

{#if timed && session}
<section class="screen round">
  <p class="kicker">{t("screen.timed.kicker")}</p>
  <h1 class="title big">{timed.round} <span class="of">{t("screen.level.of", { n: levels })}</span></h1>
  <div class="seats">
    {#each session.seats as s, i (i)}
      <div class="seat-card glass-light" class:out={s.status !== "playing"}>
        <SeatTag {session} seat={i} />
        <Hearts lives={s.lives ?? LIVES} cracked={lost(i)} out={s.status !== "playing"} />
      </div>
    {/each}
  </div>
  {#key count}<p class="countdown" class:ready={count === null}>{count ?? t("screen.timed.ready")}</p>{/key}
  <span class="label placeholder">{"PLACEHOLDER(1453)"}</span>
</section>
{:else}
<section class="screen level">
  {#if session?.mode === "rr-competitive"}
    <Tracks {session} {levels} drop={drop ? (game.last?.seat ?? null) : null} />
  {:else}
    <Tower filled={blocks} {levels} {drop} />
  {/if}
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
{/if}

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
  .seats {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: calc(1 * var(--u));
    max-width: 90%;
    animation: arrive 0.7s 0.5s var(--spring) backwards;
  }
  .seat-card {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: calc(0.5 * var(--u));
    padding: calc(0.8 * var(--u)) calc(1.2 * var(--u));
  }
  .seat-card.out {
    opacity: 0.5;
    filter: grayscale(1);
  }
  .countdown {
    display: grid;
    place-items: center;
    height: calc(6 * var(--u));
    margin: 0;
    font-family: var(--font-display);
    font-size: calc(6 * var(--u));
    font-weight: 800;
    line-height: 1;
    color: var(--paper);
    animation: zoom-in 0.4s var(--spring) backwards;
  }
  .countdown.ready {
    font-size: calc(3 * var(--u));
    color: var(--sky);
  }
  .placeholder {
    color: var(--amber);
  }
</style>
