<script lang="ts">
  // A timed seat's lives (plan 164): full hearts, the ones just lost cracking, grey when out. PLACEHOLDER(1453): look and pulses.
  import { LIVES } from "../engine/choice.ts";
  import Icon from "./Icon.svelte";

  let {
    lives,
    cracked = 0,
    out = false,
    small = false,
    pulse = null,
  }: {
    lives: number;
    /** Lost at the last round end: they crack here (the round screen). */
    cracked?: number;
    out?: boolean;
    small?: boolean;
    /** The seat's last chance in the round (hearts pulse), or its last heart too (stronger, faster). */
    pulse?: "chance" | "last" | null;
  } = $props();
</script>

<span class="hearts" class:out class:small class:chance={pulse === "chance"} class:last={pulse === "last"} aria-label={`${lives}/${LIVES}`}>
  {#each Array.from({ length: LIVES }, (_, i) => i) as i (i)}
    <span class="heart" class:full={i < lives} class:crack={i >= lives && i < lives + cracked}><Icon name="heart" /></span>
  {/each}
</span>

<style>
  .hearts {
    display: inline-flex;
    gap: calc(0.25 * var(--u));
    font-size: calc(2.4 * var(--u));
  }
  .hearts.small {
    font-size: calc(1.3 * var(--u));
    gap: calc(0.12 * var(--u));
  }
  .heart {
    display: inline-flex;
    color: var(--slate-600);
    --heart-fill: 0.3;
  }
  .heart.full {
    color: var(--coral);
    --heart-fill: 0.9;
  }
  .heart.crack {
    animation: crack 0.9s 0.9s ease-in backwards;
  }
  .chance .heart.full {
    animation: pulse 1.2s ease-in-out infinite;
  }
  .last .heart.full {
    animation: pulse 0.6s ease-in-out infinite;
    filter: drop-shadow(0 0 0.4em var(--coral));
    --pulse: 1.35;
  }
  .out .heart {
    color: var(--slate-600);
    --heart-fill: 0.3;
  }
  @keyframes pulse {
    50% {
      transform: scale(var(--pulse, 1.2));
    }
  }
  /* reduced motion: a steady highlight */
  @media (prefers-reduced-motion: reduce) {
    .chance .heart.full,
    .last .heart.full {
      animation: none;
      filter: drop-shadow(0 0 0.35em var(--coral));
    }
  }
  @keyframes crack {
    0% {
      color: var(--coral);
      transform: none;
    }
    30% {
      transform: scale(1.3) rotate(-8deg);
    }
    60% {
      color: var(--coral);
      transform: scale(1.1) rotate(10deg);
    }
    100% {
      transform: none;
    }
  }
</style>
