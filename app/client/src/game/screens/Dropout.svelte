<script lang="ts">
  // Drop-out (task 2404): every player as a tile, the earlier ones grey and struck with a cross; the one just out plays a game over (four variants, by `seed`);
  // with a winner (`final`) the fallen then fade away until only the winner is left. No button, Game.svelte goes on by itself.
  import { onDestroy, onMount } from "svelte";
  import type { SessionView } from "../../lib/seats.ts";
  import Icon from "../Icon.svelte";
  import SeatTag from "../SeatTag.svelte";
  import { sfx } from "../sound.svelte.ts";
  import { DROPOUT_FADE_MS, DROPOUT_HIT_MS, DROPOUT_LEAD_MS } from "../timing.ts";

  let { session, recent, final, seed }: { session: SessionView; recent: number[]; final: boolean; seed: number } = $props();

  const VARIANTS = ["topple", "explode", "spin", "melt"] as const;
  const variant = $derived(VARIANTS[seed % VARIANTS.length]);
  const SHARDS = Array.from({ length: 10 }, (_, i) => i);
  const gone = (i: number) => session.seats[i].status !== "playing" && session.seats[i].status !== "won";

  /** lead: all alive-looking; hit: the recent ones play; fade: the fallen leave. */
  let phase = $state<"lead" | "hit" | "fade">("lead");
  const timers: ReturnType<typeof setTimeout>[] = [];
  onMount(() => {
    timers.push(
      setTimeout(() => ((phase = "hit"), sfx("boom")), DROPOUT_LEAD_MS),
      setTimeout(() => (phase = "fade"), DROPOUT_LEAD_MS + DROPOUT_HIT_MS),
    );
  });
  onDestroy(() => timers.forEach(clearTimeout));
</script>

<section class="screen dropout" style:--hit="{DROPOUT_HIT_MS}ms" style:--fade="{DROPOUT_FADE_MS}ms">
  {#each session.seats as _, i (i)}
    {@const fresh = recent.includes(i)}
    {@const fallen = gone(i)}
    <div
      class="tile"
      class:fallen={fallen && (!fresh || phase !== "lead")}
      class:fresh={fresh && phase !== "lead"}
      class:leaving={final && fallen && phase === "fade"}
      class:winner={!fallen}
      class:crowned={final && !fallen && phase === "fade"}
      data-variant={variant}
    >
      <SeatTag {session} seat={i} alive={fresh && phase === "lead"} />
      {#if fallen && (!fresh || phase !== "lead")}<span class="grave"><Icon name="cross" /></span>{/if}
      {#if fresh && phase !== "lead" && variant === "explode"}
        {#each SHARDS as k (k)}<span class="shard" style:--a="{k * 36}deg"></span>{/each}
      {/if}
    </div>
  {/each}
</section>

<style>
  .dropout {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: calc(2 * var(--u));
  }
  .tile {
    position: relative;
    display: flex;
    align-items: center;
    gap: calc(1 * var(--u));
    transition: transform 0.5s var(--spring);
  }
  .grave {
    display: inline-flex;
    color: var(--slate-200);
    font-size: calc(2.6 * var(--u));
    animation: grave 0.5s var(--spring) backwards;
  }
  .tile.fresh[data-variant="topple"] {
    transform-origin: bottom left;
    animation: topple var(--hit) cubic-bezier(0.5, 0, 0.9, 0.5) forwards;
  }
  .tile.fresh[data-variant="spin"] {
    animation: spin var(--hit) ease-in forwards;
  }
  .tile.fresh[data-variant="melt"] {
    transform-origin: bottom center;
    animation: melt var(--hit) ease-in forwards;
  }
  .tile.fresh[data-variant="explode"] {
    animation: blast var(--hit) ease-out forwards;
  }
  .shard {
    position: absolute;
    left: 50%;
    top: 50%;
    width: calc(0.9 * var(--u));
    height: calc(0.9 * var(--u));
    border-radius: 30%;
    background: var(--paper);
    animation: shard 0.9s ease-out forwards;
  }
  .tile.leaving {
    animation: leave var(--fade) ease-in forwards;
  }
  .tile.crowned {
    transform: scale(1.5);
  }
  @keyframes topple {
    30% {
      transform: rotate(-8deg);
    }
    70% {
      transform: rotate(75deg) translateY(calc(2 * var(--u)));
      opacity: 1;
    }
    100% {
      transform: rotate(80deg) translateY(calc(2 * var(--u)));
      opacity: 0.4;
      filter: grayscale(1);
    }
  }
  @keyframes spin {
    to {
      transform: rotate(540deg) scale(0.4);
      opacity: 0.4;
      filter: grayscale(1);
    }
  }
  @keyframes melt {
    40% {
      transform: scaleY(0.9);
      filter: brightness(1.6);
    }
    to {
      transform: scaleY(0.25) scaleX(1.15);
      opacity: 0.4;
      filter: grayscale(1) blur(1px);
    }
  }
  @keyframes blast {
    15% {
      transform: scale(1.5);
      filter: brightness(2);
    }
    35% {
      transform: scale(0.1);
      opacity: 0;
    }
    to {
      transform: scale(1);
      opacity: 0.4;
      filter: grayscale(1);
    }
  }
  @keyframes shard {
    from {
      transform: rotate(var(--a)) translateX(0);
      opacity: 1;
    }
    to {
      transform: rotate(var(--a)) translateX(calc(14 * var(--u)));
      opacity: 0;
    }
  }
  @keyframes leave {
    to {
      opacity: 0;
      transform: scale(0.6);
      filter: grayscale(1) blur(4px);
    }
  }
  @keyframes grave {
    from {
      opacity: 0;
      transform: scale(2);
    }
  }
  @media (prefers-reduced-motion: reduce) {
    .tile.fresh,
    .shard {
      animation: none;
      opacity: 0.4;
    }
    .shard {
      display: none;
    }
  }
</style>
