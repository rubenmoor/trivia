<script lang="ts">
  // The transition's veil over every screen (04, "Transitions"): black, or a VHS rewind for «rebobinar».
  import { FADE_MS } from "./timing.ts";

  let { on, kind }: { on: boolean; kind: "black" | "rewind" } = $props();
</script>

<div class="black {kind}" class:on style:transition-duration="{FADE_MS}ms">
  {#if kind === "rewind"}<span class="rewind-mark">◀◀</span>{/if}
</div>

<style>
  .black {
    position: fixed;
    inset: 0;
    background: #000;
    opacity: 0;
    pointer-events: none;
    transition-property: opacity;
    z-index: 20;
  }
  .black.on {
    opacity: 1;
    pointer-events: all;
  }
  /* VHS rewind (09, "Francotirador"): scanlines rushing up, a jittering ◀◀. */
  .black.rewind {
    display: grid;
    place-items: center;
    background:
      repeating-linear-gradient(rgba(238, 241, 246, 0.07) 0 2px, transparent 2px 6px),
      linear-gradient(rgba(76, 201, 240, 0.12), rgba(255, 84, 112, 0.12)),
      var(--night-900);
    background-size:
      100% 6px,
      100% 100%,
      100% 100%;
    animation: scan 0.25s linear infinite;
  }
  .rewind-mark {
    font-family: var(--font-display);
    font-size: calc(9 * var(--u));
    font-weight: 800;
    color: var(--paper);
    text-shadow:
      calc(0.4 * var(--u)) 0 rgba(255, 84, 112, 0.8),
      calc(-0.4 * var(--u)) 0 rgba(76, 201, 240, 0.8);
    animation: jitter 0.18s steps(2) infinite;
  }
  @keyframes scan {
    to {
      background-position:
        0 -60px,
        0 0,
        0 0;
    }
  }
  @keyframes jitter {
    50% {
      transform: translate(calc(0.3 * var(--u)), calc(-0.2 * var(--u))) skewX(-6deg);
    }
  }
</style>
