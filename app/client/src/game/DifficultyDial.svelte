<script lang="ts">
  // «Bájale»'s difficulty dial (plans/09-jokers.md, "Bájale", JK-7): a staircase in the corner
  // that ticks down from the old difficulty to the new one, then fades away.
  import { onMount } from "svelte";
  import { DIAL_HOLD_MS, DIAL_STEP_MS } from "./timing";

  let { from, to }: { from: number; to: number } = $props();

  let shown = $state(0);
  let gone = $state(false);

  onMount(() => {
    shown = from;
    const timers: ReturnType<typeof setTimeout>[] = [];
    for (let d = from - 1, i = 1; d >= to; d--, i++) timers.push(setTimeout(() => (shown = d), 300 + i * DIAL_STEP_MS));
    timers.push(setTimeout(() => (gone = true), 300 + (from - to) * DIAL_STEP_MS + DIAL_HOLD_MS));
    return () => timers.forEach(clearTimeout);
  });
</script>

<div class="dial glass-strong" class:gone aria-hidden="true">
  <span class="label">Dificultad</span>
  <span class="stairs">
    {#each Array.from({ length: 10 }, (_, i) => i + 1) as d (d)}
      <span class="step" class:lit={d <= shown} class:now={d === shown} style:--h={d}></span>
    {/each}
  </span>
  {#key shown}<span class="number">{shown}</span>{/key}
</div>

<style>
  .dial {
    display: flex;
    align-items: flex-end;
    gap: calc(0.8 * var(--u));
    padding: calc(0.6 * var(--u)) calc(1.1 * var(--u));
    border-radius: calc(0.9 * var(--u));
    animation: arrive 0.4s var(--spring) backwards;
    transition: opacity 0.6s;
  }
  .dial.gone {
    opacity: 0;
  }
  .label {
    align-self: center;
    font-family: var(--font-display);
    font-size: calc(1.1 * var(--u));
    font-weight: 700;
    color: var(--slate-200);
  }
  .stairs {
    display: flex;
    align-items: flex-end;
    gap: calc(0.15 * var(--u));
    height: calc(2.6 * var(--u));
  }
  .step {
    width: calc(0.55 * var(--u));
    height: calc(var(--h) * 0.26 * var(--u));
    border-radius: calc(0.1 * var(--u));
    background: var(--slate-600);
    transition: background 0.2s;
  }
  .step.lit {
    background: var(--sky);
  }
  .step.now {
    background: var(--amber);
  }
  .number {
    min-width: 1.2em;
    font-family: var(--font-display);
    font-size: calc(2.4 * var(--u));
    font-weight: 800;
    line-height: 1;
    color: var(--amber);
    text-align: center;
    animation: tick 0.25s var(--spring);
  }
  @keyframes tick {
    from {
      transform: translateY(-60%);
      opacity: 0;
    }
  }
  @keyframes arrive {
    from {
      opacity: 0;
      transform: scale(0.8);
    }
  }
</style>
