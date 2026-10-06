<script lang="ts">
  // The HUD (plans/10-visual-design.md, "Layout"): the level with a 12-tick mini tower, and the
  // player's name (D-28). Shown on Select and Question, so the family always sees what's at stake.
  let { level, player }: { level: number; player: string | null } = $props();
</script>

<div class="hud">
  <div class="chip glass">
    <span class="level">Nivel {level}</span>
    <span class="ticks" aria-hidden="true">
      {#each Array.from({ length: 12 }, (_, i) => i + 1) as l (l)}
        <span class="tick" class:done={l < level} class:now={l === level}></span>
      {/each}
    </span>
  </div>
  {#if player}<div class="chip glass player">{player}</div>{/if}
</div>

<style>
  .hud {
    display: flex;
    gap: calc(0.8 * var(--u));
  }
  .chip {
    display: flex;
    align-items: center;
    gap: calc(0.9 * var(--u));
    padding: calc(0.35 * var(--u)) calc(1 * var(--u));
    border-radius: calc(0.9 * var(--u));
    font-family: var(--font-display);
    font-size: calc(1.1 * var(--u));
    font-weight: 700;
  }
  .level {
    color: var(--amber);
  }
  .ticks {
    display: flex;
    align-items: flex-end;
    gap: calc(0.18 * var(--u));
  }
  .tick {
    width: calc(0.45 * var(--u));
    height: calc(1 * var(--u));
    border-radius: calc(0.1 * var(--u));
    background: var(--slate-600);
  }
  .tick.done {
    background: var(--mint);
  }
  .tick.now {
    background: var(--amber);
    height: calc(1.3 * var(--u));
  }
  .player {
    color: var(--slate-200);
  }
</style>
