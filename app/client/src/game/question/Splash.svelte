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
  /** Per-letter vectors for the exits that split the name (the words stay whole, so wrapping works). */
  const words = $derived.by(() => {
    const spec = reduced ? undefined : picked.letters;
    if (!spec) return null;
    const parts = catName.split(" ");
    const total = parts.join("").length;
    let i = 0;
    return parts.map((w) =>
      [...w].map((ch) => {
        const at = i++;
        const stagger = (spec.order ? (spec.reverse ? total - 1 - at : at) / Math.max(1, total - 1) : Math.random()) * spec.spread * SPLASH_EXIT_MS;
        return {
          ch,
          vars: `--ld:${stagger}ms;--lx:${Math.round(Math.random() * 100 - 50)}vw;--ly:${Math.round(Math.random() * 100 - 50)}vh;--lr:${Math.round(Math.random() * 720 - 360)}deg`,
        };
      }),
    );
  });
  const letterMs = picked.letters ? SPLASH_EXIT_MS * (1 - picked.letters.spread) : SPLASH_EXIT_MS;
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
        {#if words}
          {#each words as word, w (w)}
            <span class="w" style:--lms="{letterMs}ms">{#each word as { ch, vars }, k (k)}<span class="l" style={vars}>{ch}</span>{/each}</span>{" "}
          {/each}
        {:else}
          {catName}
        {/if}
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
  .rocket {
    animation-name: rocket;
    animation-timing-function: cubic-bezier(0.5, 0, 0.9, 0.5);
  }
  .drop {
    animation-name: drop;
    animation-timing-function: linear;
  }
  .blind {
    animation-name: blind;
    animation-timing-function: cubic-bezier(0.6, 0, 0.8, 0.6);
  }
  .drain {
    animation-name: drain;
    animation-timing-function: cubic-bezier(0.5, 0, 0.9, 0.7);
  }
  .pop {
    animation-name: pop;
  }
  /* Letters: the category is spans, each with its own start (--ld) and vector */
  .w {
    display: inline-block;
    white-space: nowrap;
  }
  .l {
    display: inline-block;
    animation-duration: var(--lms);
    animation-delay: calc(var(--delay) + var(--ld));
    animation-fill-mode: both;
    animation-play-state: paused;
  }
  .go .l {
    animation-play-state: running;
  }
  .dissolve .l {
    animation-name: dissolve;
  }
  .explode .l {
    animation-name: explode;
    animation-timing-function: cubic-bezier(0.2, 0.6, 0.5, 1);
  }
  .wind .l {
    animation-name: wind;
    animation-timing-function: ease-in;
  }
  .zoom {
    animation-name: zoom;
    animation-timing-function: cubic-bezier(0.6, 0, 0.9, 0.5);
  }
  .melt {
    animation-name: melt;
    animation-timing-function: ease-in;
    transform-origin: top;
  }
  .blackhole {
    animation-name: blackhole;
    animation-timing-function: cubic-bezier(0.5, 0, 0.9, 0.6);
  }
  .plane {
    animation-name: plane;
    animation-timing-function: ease-in;
  }
  .jelly {
    animation-name: jelly;
    transform-origin: bottom;
  }
  .shatter .l {
    animation-name: shatter;
    animation-timing-function: ease-in;
  }
  .birds .l {
    animation-name: birds;
    animation-timing-function: cubic-bezier(0.3, 0, 0.8, 0.6);
  }
  .typewriter .l {
    animation-name: typewriter;
    animation-timing-function: step-end;
  }
  @keyframes zoom {
    to { transform: scale(9); filter: blur(1.2vw); opacity: 0; }
  }
  @keyframes melt {
    30% { transform: translateY(1vh) scale(1, 1.15); opacity: 1; }
    to { transform: translateY(18vh) scale(1.05, 2.6); filter: blur(0.5vw); opacity: 0; }
  }
  @keyframes blackhole {
    to { transform: scale(0) rotate(-540deg); filter: blur(0.5vw) brightness(0.2); }
  }
  @keyframes plane {
    35% { transform: perspective(1200px) rotateX(55deg) scale(0.6, 0.4); opacity: 1; }
    to { transform: translate(85vw, -70vh) rotate(-25deg) scale(0.08); opacity: 0; }
  }
  @keyframes jelly {
    18% { transform: scale(1.15, 0.85); }
    32% { transform: scale(0.9, 1.12); }
    46% { transform: scale(1.08, 0.92); }
    to { transform: scale(1.7, 0) translateY(2vh); opacity: 0; }
  }
  @keyframes shatter {
    15% { transform: translate(calc(var(--lx) * 0.02), 0) rotate(calc(var(--lr) * 0.02)); }
    to { transform: translate(calc(var(--lx) * 0.2), calc(55vh + var(--ly) * 0.3)) rotate(calc(var(--lr) * 0.4)); opacity: 0; }
  }
  @keyframes birds {
    to { transform: translate(calc(var(--lx) * 1.3), calc(-75vh + var(--ly) * 0.4)) rotate(calc(var(--lr) * 0.2)) scale(0.3); opacity: 0; }
  }
  @keyframes typewriter {
    from { opacity: 1; }
    to { opacity: 0; }
  }
  @keyframes dissolve {
    to { transform: translate(calc(var(--lx) * 0.2), calc(var(--ly) * 0.2 - 4vh)) scale(0.4); filter: blur(1vw); opacity: 0; }
  }
  @keyframes explode {
    to { transform: translate(var(--lx), var(--ly)) rotate(var(--lr)) scale(1.6); opacity: 0; }
  }
  @keyframes wind {
    to { transform: translate(110vw, calc(var(--ly) * 0.3)) rotate(var(--lr)); opacity: 0; }
  }
  @keyframes rocket {
    15% { transform: translateY(1.5vh) scaleY(0.94); }
    to { transform: translateY(-130vh) scaleY(1.4); }
  }
  @keyframes drop {
    35% { transform: translateY(26vh); animation-timing-function: ease-out; }
    52% { transform: translateY(14vh); animation-timing-function: ease-in; }
    65% { transform: translateY(26vh); animation-timing-function: ease-out; }
    75% { transform: translateY(22vh); animation-timing-function: ease-in; }
    to { transform: translateY(110vh); }
  }
  @keyframes blind {
    from { clip-path: inset(-20% -5% -20% -5%); }
    to { clip-path: inset(-20% -5% 120% -5%); transform: translateY(-3vh); }
  }
  @keyframes drain {
    to { transform: translateY(22vh) rotate(720deg) scale(0); }
  }
  @keyframes pop {
    70% { transform: scale(0.03); opacity: 1; animation-timing-function: ease-out; }
    85% { transform: scale(0.2); opacity: 1; }
    to { transform: scale(0.5); opacity: 0; }
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
