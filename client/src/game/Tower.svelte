<script lang="ts">
  // The tower of 12 blocks, narrower towards the top (D-22). Plain boxes for now:
  // PLACEHOLDER(UI-3): no textures, no drop-and-settle animation, no crown, no camera follow.
  import Placeholder from "./Placeholder.svelte";

  let { filled, small = false }: { filled: number; small?: boolean } = $props();

  const LEVELS = 12;
  /** Block 1 is ~90 % of the foundation's width, block 12 ~35 % (04-ui-tv-display.md). */
  const width = (level: number) => 90 - ((level - 1) * 55) / (LEVELS - 1);
</script>

<div class="tower" class:small>
  {#each Array.from({ length: LEVELS }, (_, i) => LEVELS - i) as level (level)}
    <div
      class="block"
      class:filled={level <= filled}
      class:newest={level === filled}
      style:width="{width(level)}%"
      style:--hue={(level * 29) % 360}
    >
      {level}
    </div>
  {/each}
  <div class="foundation"></div>
  {#if !small}
    <Placeholder task="UI-3" label="torre sin animación ni texturas" chip />
  {/if}
</div>

<style>
  .tower {
    width: min(34vw, 60vh);
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.4vh;
  }
  .tower.small {
    width: min(16vw, 28vh);
  }
  .block {
    height: 4.6vh;
    border: 0.15rem dotted rgba(255, 255, 255, 0.25);
    border-radius: 0.3rem;
    color: transparent;
    display: grid;
    place-items: center;
    font-weight: 700;
  }
  .small .block {
    height: 2.2vh;
    font-size: 0;
  }
  .block.filled {
    border: none;
    background: hsl(var(--hue) 60% 50%);
    color: rgba(0, 0, 0, 0.55);
  }
  .block.newest {
    outline: 0.25rem solid var(--accent);
  }
  .foundation {
    width: 100%;
    height: 2.5vh;
    background: #5a5d6e;
    border-radius: 0.3rem;
    margin-bottom: 1vh;
  }
</style>
