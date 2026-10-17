<script lang="ts">
  // The category splash (plan 181): category big and centred, subcategory small below; after a hold both leave with
  // one of the exits in splash.ts and its sound. Over the whole screen, never in the way of play.
  import { untrack } from "svelte";
  import { displayName, questionLocale } from "../../lib/names.svelte.ts";
  import { sfx } from "../sound.svelte.ts";
  import { SPLASH_EXIT_MS, SPLASH_HOLD_MS, SPLASH_SUB_MAX_MS, reducedMotion } from "../timing.ts";
  import { pickExit, type SplashExit } from "./splash.ts";

  let {
    category,
    subcategory,
    start,
    delay = 0,
    exit: forced,
  }: {
    category: string;
    subcategory: string | null;
    /** The question has faded in (or flipped in): the hold begins. */
    start: boolean;
    /** Extra wait after `start` (ms). */
    delay?: number;
    /** A given exit (the effects demo); else a random one. */
    exit?: SplashExit;
  } = $props();

  const picked = untrack(() => forced ?? pickExit());
  const reduced = reducedMotion();
  let phase = $state<"wait" | "hold" | "exit" | "gone">("wait");
  const catName = $derived(displayName("category", category));
  const subName = $derived(subcategory ? displayName("subcategory", subcategory) : null);
  const long = $derived(catName.length > 24);
  const subShift = $derived(picked.subOffsetMs);

  $effect(() => {
    if (!start) return;
    const timers: ReturnType<typeof setTimeout>[] = [];
    timers.push(
      setTimeout(() => {
        phase = "hold";
        timers.push(
          setTimeout(() => {
            phase = "exit";
            sfx(picked.cue);
            timers.push(setTimeout(() => (phase = "gone"), SPLASH_EXIT_MS + SPLASH_SUB_MAX_MS));
          }, SPLASH_HOLD_MS),
        );
      }, delay),
    );
    return () => timers.forEach(clearTimeout);
  });
</script>

{#if phase === "hold" || phase === "exit"}
  <div class="splash" aria-hidden="true" style:--exit="{SPLASH_EXIT_MS}ms">
    <div class="box" class:long>
      <p
        class="category {reduced ? 'fade' : picked.category}"
        class:go={phase === "exit"}
        style:--delay="{Math.max(0, -subShift)}ms"
        lang={questionLocale()}
      >
        {catName}
      </p>
      {#if subName}
        <p
          class="sub {reduced ? 'fade' : `sub-${picked.sub}`}"
          class:go={phase === "exit"}
          style:--delay="{Math.max(0, subShift)}ms"
          lang={questionLocale()}
        >
          {subName}
        </p>
      {/if}
    </div>
  </div>
{/if}

<style>
  .splash {
    position: absolute;
    inset: 0;
    z-index: 20;
    display: grid;
    place-items: center;
    pointer-events: none;
    overflow: hidden;
  }
  .box {
    width: 88%;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: calc(0.6 * var(--u));
    text-align: center;
  }
  p {
    margin: 0;
    max-width: 100%;
    color: white;
    font-family: var(--font-display);
    line-height: 1.05;
    text-wrap: balance;
    overflow-wrap: anywhere;
    paint-order: stroke fill;
    -webkit-text-stroke: calc(0.5 * var(--u)) rgb(0 0 0 / 0.85);
    text-shadow: 0 calc(0.3 * var(--u)) calc(1 * var(--u)) rgb(0 0 0 / 0.7);
    animation-duration: var(--exit);
    animation-delay: var(--delay);
    animation-fill-mode: both;
    animation-play-state: paused;
  }
  .go {
    animation-play-state: running;
  }
  .category {
    font-size: calc(9 * var(--u));
    font-weight: 800;
  }
  .long .category {
    font-size: calc(6 * var(--u));
  }
  .sub {
    font-size: calc(2.6 * var(--u));
    font-weight: 500;
    -webkit-text-stroke-width: calc(0.3 * var(--u));
  }

  /* Category exits; each runs paused until `.go`, so the hold shows its first frame */
  .fly-left {
    animation-name: fly-left;
    animation-timing-function: cubic-bezier(0.6, 0, 0.9, 0.5);
  }
  .fly-right {
    animation-name: fly-right;
    animation-timing-function: cubic-bezier(0.6, 0, 0.9, 0.5);
  }
  .fade {
    animation-name: fade;
  }
  .spin {
    animation-name: spin;
    animation-timing-function: cubic-bezier(0.5, 0, 0.9, 0.6);
  }
  @keyframes fly-left {
    to { transform: translateX(-120vw) skewX(12deg); opacity: 0; }
  }
  @keyframes fly-right {
    to { transform: translateX(120vw) skewX(-12deg); opacity: 0; }
  }
  @keyframes fade {
    to { opacity: 0; }
  }
  @keyframes spin {
    to { transform: rotate(540deg) scale(0); opacity: 0; }
  }

  /* Subcategory exits */
  .sub-fade {
    animation-name: fade;
  }
  .sub-down {
    animation-name: sub-down;
  }
  .sub-shrink {
    animation-name: sub-shrink;
  }
  .sub-blur {
    animation-name: sub-blur;
  }
  .sub-drift-left {
    animation-name: sub-drift-left;
  }
  .sub-drift-right {
    animation-name: sub-drift-right;
  }
  @keyframes sub-down {
    to { transform: translateY(6vh); opacity: 0; }
  }
  @keyframes sub-shrink {
    to { transform: scale(0.7); opacity: 0; }
  }
  @keyframes sub-blur {
    to { filter: blur(1vw); opacity: 0; }
  }
  @keyframes sub-drift-left {
    to { transform: translateX(-6vw); opacity: 0; }
  }
  @keyframes sub-drift-right {
    to { transform: translateX(6vw); opacity: 0; }
  }
</style>
