<script lang="ts">
  // The tower of one block per level (12 by default, 1–20 per game, D-88), narrower towards the top (D-22, UI-3, VD-7). Materials get fancier
  // with height (stone → brick → marble → sapphire → gold); the newest block drops in and settles;
  // a full tower wears the crown; on Wrong the blocks fall away one by one.
  import Icon from "./Icon.svelte";
  import { DEFAULT_LEVELS, onTwelve } from "./levels.ts";

  let {
    filled,
    levels = DEFAULT_LEVELS,
    small = false,
    drop = false,
    crumble = false,
  }: {
    filled: number;
    levels?: number;
    small?: boolean;
    /** The newest block drops in from the top (the Level screen after a correct answer). */
    drop?: boolean;
    /** The blocks fall away (the Wrong screen, UI-4). */
    crumble?: boolean;
  } = $props();

  /** Block 1 is ~90 % of the foundation's width, the top block ~35 % (04-ui-tv-display.md). */
  const width = (level: number) => (levels === 1 ? 90 : 90 - ((level - 1) * 55) / (levels - 1));

  function material(at: number) {
    const level = onTwelve(at, levels);
    if (level <= 3) return "stone";
    if (level <= 6) return "brick";
    if (level <= 9) return "marble";
    if (level <= 11) return "sapphire";
    return "gold";
  }
</script>

<div class="tower" style:--n={levels} class:small class:crumble class:wobble={drop && filled > 0}>
  <div class="crown" class:on={filled >= levels}><Icon name="crown" size="100%" /></div>
  {#each Array.from({ length: levels }, (_, i) => levels - i) as level (level)}
    <div
      class="block {level <= filled ? material(level) : 'empty'}"
      class:newest={level === filled}
      class:drop={drop && level === filled}
      style:width="{width(level)}%"
      style:--fall-delay="{(filled - level) * 0.18 + 0.6}s"
    >
      {#if level <= filled && !small}<span class="num">{level}</span>{/if}
    </div>
  {/each}
  <div class="foundation"></div>
</div>

<style>
  /* --base-h: a block of the 12-level tower; with more levels the blocks get flatter (same height). */
  .tower {
    --base-h: calc(3.7 * var(--u));
    --block-h: calc(min(5, 44.4 / var(--n)) * var(--u));
    width: calc(30 * var(--u));
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: calc(min(0.3, 3.6 / var(--n)) * var(--u));
  }
  .tower.small {
    --base-h: calc(1.5 * var(--u));
    --block-h: calc(min(2, 18 / var(--n)) * var(--u));
    width: var(--tower-w, calc(14 * var(--u)));
    gap: calc(min(0.15, 1.8 / var(--n)) * var(--u));
  }
  .wobble {
    animation: wobble 0.9s 0.75s ease-out;
    transform-origin: 50% 100%;
  }
  @keyframes wobble {
    25% {
      transform: rotate(0.8deg);
    }
    55% {
      transform: rotate(-0.5deg);
    }
    80% {
      transform: rotate(0.2deg);
    }
  }

  .block {
    position: relative;
    height: var(--block-h);
    border-radius: calc(0.45 * var(--u));
    display: grid;
    place-items: center;
    font-family: var(--font-display);
    font-weight: 800;
    font-size: calc(1.4 * var(--u));
    color: rgba(11, 17, 32, 0.55);
    box-shadow:
      inset 0 calc(0.25 * var(--u)) 0 rgba(255, 255, 255, 0.22),
      inset 0 calc(-0.3 * var(--u)) 0 rgba(0, 0, 0, 0.22);
  }
  .small .block {
    border-radius: calc(0.25 * var(--u));
  }
  .empty {
    border: calc(0.15 * var(--u)) dotted var(--slate-400);
    opacity: 0.4;
    box-shadow: none;
  }
  .stone {
    background:
      radial-gradient(circle at 30% 35%, rgba(255, 255, 255, 0.14) 0 12%, transparent 16%) 0 0 /
        calc(1.3 * var(--u)) calc(1.1 * var(--u)),
      radial-gradient(circle at 70% 70%, rgba(0, 0, 0, 0.16) 0 14%, transparent 18%) 0 0 /
        calc(1.7 * var(--u)) calc(1.4 * var(--u)),
      var(--stone);
  }
  .brick {
    background:
      repeating-linear-gradient(90deg, transparent 0 calc(3.6 * var(--u)), rgba(60, 20, 10, 0.45) 0 calc(3.75 * var(--u))),
      linear-gradient(transparent 47%, rgba(60, 20, 10, 0.45) 0 53%, transparent 0),
      var(--brick);
  }
  .marble {
    background:
      linear-gradient(115deg, transparent 30%, rgba(76, 201, 240, 0.45) 31%, transparent 33%),
      linear-gradient(160deg, transparent 60%, rgba(76, 201, 240, 0.3) 61%, transparent 62.5%),
      var(--marble);
  }
  .sapphire {
    background: linear-gradient(135deg, #7fa2ff, var(--sapphire) 45%, #1f3f9e);
    color: rgba(238, 241, 246, 0.7);
  }
  .gold {
    background: linear-gradient(135deg, #ffe08a, var(--amber) 45%, var(--amber-deep));
  }
  .newest {
    animation: glow 2.4s 0.8s ease-out;
  }
  @keyframes glow {
    from {
      box-shadow: 0 0 calc(2.5 * var(--u)) var(--mint);
    }
  }
  .drop {
    animation:
      drop 0.75s cubic-bezier(0.55, 0, 1, 0.45) both,
      settle 0.45s 0.75s ease-out,
      glow 2.4s 0.8s ease-out;
  }
  @keyframes drop {
    from {
      transform: translateY(-110vh);
    }
  }
  @keyframes settle {
    30% {
      transform: scale(1.08, 0.82) translateY(10%);
    }
    65% {
      transform: scale(0.97, 1.05);
    }
  }
  .crumble .block:not(.empty) {
    animation: fall 1.1s var(--fall-delay) cubic-bezier(0.5, 0, 0.9, 0.5) forwards;
  }
  @keyframes fall {
    to {
      transform: translateY(60vh) rotate(25deg);
      opacity: 0;
    }
  }

  .num {
    text-shadow: none;
  }
  .foundation {
    width: 100%;
    height: calc(var(--base-h) * 0.7);
    background: var(--night-700);
    border-top: calc(0.25 * var(--u)) solid var(--amber);
    border-radius: calc(0.45 * var(--u));
  }
  .crown {
    width: calc(var(--base-h) * 1.6);
    height: calc(var(--base-h) * 1.6);
    color: var(--amber);
    opacity: 0;
    transform: translateY(-50%) scale(0.4);
    filter: drop-shadow(0 0 calc(1 * var(--u)) rgba(255, 184, 28, 0.7));
  }
  .crown.on {
    animation: crown 0.8s 1.3s var(--spring) forwards;
  }
  .small .crown {
    display: none;
  }
  @keyframes crown {
    to {
      opacity: 1;
      transform: none;
    }
  }
</style>
