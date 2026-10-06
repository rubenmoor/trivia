<script lang="ts">
  // The common joker play animation (plans/09-jokers.md, "Common play animation", JK-5): the token
  // flies out of the tray to the centre of the screen, grows and spins, then bursts into sparkles.
  // Short on purpose (jokers are unlimited, D-27); with reduced motion it is a quick fade.
  import { onMount } from "svelte";
  import Icon, { type IconName } from "./Icon.svelte";
  import { JOKER_BURST_MS, JOKER_FLY_MS } from "./timing";

  let { from, icon, ondone }: { from: DOMRect; icon: IconName; ondone: () => void } = $props();

  let chip = $state<HTMLDivElement>();
  let burst = $state(false);
  const SPARKS = 12;

  onMount(() => {
    const reduced = matchMedia("(prefers-reduced-motion: reduce)").matches;
    const dx = innerWidth / 2 - (from.left + from.width / 2);
    const dy = innerHeight / 2 - (from.top + from.height / 2);
    const flight = chip!.animate(
      reduced
        ? [{ opacity: 1 }, { opacity: 0 }]
        : [
            { transform: "translate(0, 0) scale(1) rotate(0turn)" },
            { transform: `translate(${dx}px, ${dy}px) scale(2.6) rotate(1turn)`, offset: 0.85 },
            { transform: `translate(${dx}px, ${dy}px) scale(2.4) rotate(1turn)` },
          ],
      { duration: reduced ? 150 : JOKER_FLY_MS, easing: "cubic-bezier(0.3, 0, 0.2, 1)", fill: "forwards" },
    );
    flight.finished.then(async () => {
      if (reduced) return ondone();
      burst = true;
      setTimeout(ondone, JOKER_BURST_MS);
    });
    return () => flight.cancel();
  });
</script>

<div class="flight" aria-hidden="true">
  <div
    class="chip"
    class:burst
    bind:this={chip}
    style:left="{from.left}px"
    style:top="{from.top}px"
    style:width="{from.width}px"
    style:height="{from.height}px"
  >
    <span class="face"><Icon name={icon} size="100%" /></span>
  </div>
  {#if burst}
    <div class="sparks">
      {#each Array.from({ length: SPARKS }, (_, i) => i) as i (i)}
        <span class="spark" style:--a="{(i / SPARKS) * 360}deg" style:--d="{(i % 3) * 0.04}s"></span>
      {/each}
    </div>
  {/if}
</div>

<style>
  .flight {
    position: fixed;
    inset: 0;
    z-index: 8;
    pointer-events: none;
  }
  .chip {
    position: absolute;
    display: grid;
    place-items: center;
    border: calc(0.3 * var(--u)) dashed var(--amber);
    border-radius: 50%;
    background:
      radial-gradient(circle at 35% 30%, rgba(255, 255, 255, 0.18), transparent 60%),
      var(--night-700);
    color: var(--amber);
    box-shadow: 0 0 calc(2 * var(--u)) rgba(255, 184, 28, 0.55);
  }
  .chip.burst {
    animation: pop-out var(--burst, 0.25s) ease-out forwards;
  }
  .face {
    width: 52%;
    height: 52%;
  }
  .sparks {
    position: absolute;
    left: 50%;
    top: 50%;
  }
  .spark {
    position: absolute;
    width: calc(0.7 * var(--u));
    height: calc(2.2 * var(--u));
    margin: calc(-1.1 * var(--u)) 0 0 calc(-0.35 * var(--u));
    border-radius: calc(0.35 * var(--u));
    background: linear-gradient(var(--paper), var(--amber));
    transform: rotate(var(--a)) translateY(0);
    animation: spark 0.45s var(--d) ease-out forwards;
  }
  @keyframes spark {
    from {
      opacity: 1;
      transform: rotate(var(--a)) translateY(calc(-2 * var(--u))) scaleY(0.4);
    }
    to {
      opacity: 0;
      transform: rotate(var(--a)) translateY(calc(-11 * var(--u))) scaleY(1);
    }
  }
  @keyframes pop-out {
    to {
      opacity: 0;
      filter: brightness(2);
    }
  }
</style>
