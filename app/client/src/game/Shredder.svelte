<script lang="ts">
  // «Paso» with purge (plans/09-jokers.md, "Paso", JK-6): the subcategory name appears big, a red
  // «ELIMINADO» stamp slams onto it, then it drops through a paper shredder in strips.
  import { onMount } from "svelte";
  import { sfx } from "./sound.svelte";
  import { SHRED_MS, STAMP_MS } from "./timing";

  let { name, ondone }: { name: string; ondone: () => void } = $props();

  const STRIPS = 9;
  let stamped = $state(false);
  let shredding = $state(false);

  onMount(() => {
    const timers = [
      setTimeout(() => {
        stamped = true;
        sfx("sello: ¡pum!");
      }, 350),
      setTimeout(() => {
        shredding = true;
        sfx("trituradora");
      }, STAMP_MS),
      setTimeout(ondone, STAMP_MS + SHRED_MS),
    ];
    return () => timers.forEach(clearTimeout);
  });
</script>

<div class="shredder" aria-hidden="true">
  <div class="paper-stack" class:shredding>
    {#each Array.from({ length: STRIPS }, (_, i) => i) as i (i)}
      <div
        class="paper"
        style:clip-path="inset(0 {100 - ((i + 1) * 100) / STRIPS}% 0 {(i * 100) / STRIPS}%)"
        style:--drift="{(i - (STRIPS - 1) / 2) * 0.6}"
        style:--delay="{(i % 3) * 0.05}s"
      >
        <span class="name">{name}</span>
        {#if stamped}<span class="stamp">ELIMINADO</span>{/if}
      </div>
    {/each}
  </div>
  <div class="slot"></div>
</div>

<style>
  .shredder {
    position: absolute;
    inset: 0;
    z-index: 6;
    display: grid;
    place-items: center;
    background: rgba(5, 8, 16, 0.6);
    pointer-events: none;
  }
  .paper-stack {
    position: relative;
    display: grid;
    animation: arrive 0.35s var(--spring) backwards;
  }
  .paper {
    grid-area: 1 / 1;
    position: relative;
    min-width: calc(34 * var(--u));
    text-align: center;
    padding: calc(2.4 * var(--u)) calc(4 * var(--u));
    border-radius: calc(0.5 * var(--u));
    background: var(--cream);
    box-shadow: 0 calc(0.8 * var(--u)) calc(2 * var(--u)) rgba(0, 0, 0, 0.5);
  }
  .shredding .paper {
    animation: shred 0.9s var(--delay) cubic-bezier(0.5, 0, 0.9, 0.6) forwards;
  }
  .name {
    font-family: var(--font-display);
    font-size: calc(4.2 * var(--u));
    font-weight: 800;
    color: var(--ink);
    white-space: nowrap;
  }
  .stamp {
    position: absolute;
    left: 50%;
    top: 50%;
    padding: calc(0.2 * var(--u)) calc(1.2 * var(--u));
    border: calc(0.45 * var(--u)) solid var(--seal);
    border-radius: calc(0.6 * var(--u));
    color: var(--seal);
    font-family: var(--font-display);
    font-size: calc(2.6 * var(--u));
    font-weight: 800;
    letter-spacing: 0.08em;
    white-space: nowrap;
    mix-blend-mode: multiply;
    transform: translate(-50%, -50%) rotate(-12deg);
    animation: slam 0.28s cubic-bezier(0.5, 0, 0.75, 0) backwards;
  }
  .slot {
    position: absolute;
    left: 50%;
    top: calc(50% + 6 * var(--u));
    width: calc(56 * var(--u));
    height: calc(1.2 * var(--u));
    transform: translateX(-50%);
    border-radius: calc(0.6 * var(--u));
    background: var(--night-900);
    box-shadow:
      0 0 0 calc(0.4 * var(--u)) var(--slate-600),
      0 calc(1 * var(--u)) calc(2 * var(--u)) rgba(0, 0, 0, 0.6);
  }
  @keyframes slam {
    from {
      opacity: 0;
      transform: translate(-50%, -50%) rotate(-24deg) scale(3);
    }
  }
  @keyframes shred {
    40% {
      transform: translateY(calc(5 * var(--u)));
    }
    to {
      transform: translate(calc(var(--drift) * 2 * var(--u)), 70vh) rotate(calc(var(--drift) * 8deg));
      opacity: 0;
    }
  }
  @keyframes arrive {
    from {
      opacity: 0;
      transform: scale(0.6);
    }
  }
</style>
