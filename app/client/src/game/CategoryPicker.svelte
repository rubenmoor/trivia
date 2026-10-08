<script lang="ts">
  // «Cambiazo»'s two-step picker (plans/09-jokers.md, "Cambiazo", JK-7): every bundle's broad categories
  // (D-43), then the subcategories of the chosen one (D-19). Tiles without a fitting question are disabled
  // (the server decides, 09 "Availability"). Click, or arrows + Enter; Backspace goes back.
  import { tick } from "svelte";
  import type { Jokers } from "../lib/types";

  type Group = Jokers["category"]["categories"][number];

  let {
    categories,
    onpick,
    oncancel,
  }: {
    categories: Group[];
    onpick: (subcategory: string) => void;
    oncancel: () => void;
  } = $props();

  let group = $state<Group | null>(null);
  let grid = $state<HTMLDivElement>();

  async function focusFirst() {
    await tick();
    grid?.querySelector<HTMLButtonElement>("button:not(:disabled)")?.focus();
  }
  focusFirst();

  async function open(g: Group) {
    group = g;
    await focusFirst();
  }

  async function back() {
    if (!group) return oncancel();
    const slug = group.slug;
    group = null;
    await tick();
    grid?.querySelector<HTMLButtonElement>(`[data-slug="${slug}"]`)?.focus();
  }

  /** Arrow keys move the focus over the enabled tiles, row by row. */
  function move(e: KeyboardEvent) {
    const tiles = [...(grid?.querySelectorAll<HTMLButtonElement>("button") ?? [])];
    const at = tiles.indexOf(document.activeElement as HTMLButtonElement);
    const cols = getComputedStyle(grid!).gridTemplateColumns.split(" ").length;
    const step = { ArrowRight: 1, ArrowLeft: -1, ArrowDown: cols, ArrowUp: -cols }[e.key] ?? 0;
    for (let i = at < 0 ? 0 : at + step; i >= 0 && i < tiles.length; i += step || 1) {
      if (!tiles[i].disabled) return tiles[i].focus();
      if (!step) break;
    }
  }

  export function key(e: KeyboardEvent) {
    if (e.key === "Escape") {
      e.preventDefault();
      oncancel();
    } else if (e.key === "Backspace") {
      e.preventDefault();
      back();
    } else if (e.key.startsWith("Arrow")) {
      e.preventDefault();
      move(e);
    }
    // Enter and Space press the focused tile natively.
  }
</script>

<div class="backdrop">
  <div class="picker glass-strong">
    <h2>{group ? group.name : "Cambiazo: ¿qué tema quieren?"}</h2>
    {#key group}
      <div class="grid" class:subs={group} bind:this={grid}>
        {#if group}
          {#each group.subcategories as s, i (s.name)}
            <button class="tile" disabled={!s.available} onclick={() => onpick(s.name)} style:--i={i}>{s.name}</button>
          {/each}
        {:else}
          {#each categories as g, i (g.slug)}
            <button class="tile" data-slug={g.slug} disabled={!g.available} onclick={() => open(g)} style:--i={i}>
              {g.name}
            </button>
          {/each}
        {/if}
      </div>
    {/key}
    <div class="actions label">
      {#if group}<button class="secondary" onclick={back}>Atrás <kbd>⌫</kbd></button>{/if}
      <button class="secondary" onclick={oncancel}>Cancelar <kbd>Esc</kbd></button>
    </div>
  </div>
</div>

<style>
  .backdrop {
    position: absolute;
    inset: 0;
    z-index: 5;
    display: grid;
    place-items: center;
    background: rgba(5, 8, 16, 0.55);
  }
  .picker {
    width: min(92%, calc(100 * var(--u)));
    padding: calc(1.6 * var(--u)) calc(2 * var(--u));
    display: flex;
    flex-direction: column;
    gap: calc(1.2 * var(--u));
    animation: arrive 0.35s var(--spring) backwards;
  }
  h2 {
    margin: 0;
    text-align: center;
    font-family: var(--font-display);
    font-size: calc(2.4 * var(--u));
    font-weight: 800;
  }
  .grid {
    display: grid;
    grid-template-columns: repeat(6, 1fr);
    gap: calc(0.7 * var(--u));
  }
  .grid.subs {
    grid-template-columns: repeat(4, 1fr);
  }
  .tile {
    min-height: calc(5 * var(--u));
    padding: calc(0.6 * var(--u));
    border: none;
    border-radius: calc(0.7 * var(--u));
    background: var(--cream);
    color: var(--ink);
    font-family: var(--font-display);
    font-size: calc(1.3 * var(--u));
    font-weight: 700;
    line-height: 1.15;
    box-shadow: 0 calc(0.25 * var(--u)) 0 #d9cfb6;
    transition: transform 0.15s var(--spring);
    animation: deal 0.35s calc(var(--i) * 0.015s) var(--spring) backwards;
  }
  .tile:hover:not(:disabled),
  .tile:focus-visible {
    transform: translateY(calc(-0.3 * var(--u))) scale(1.04);
    outline: calc(0.22 * var(--u)) solid var(--sky);
    outline-offset: calc(0.15 * var(--u));
  }
  .tile:disabled {
    opacity: 0.25;
  }
  .actions {
    display: flex;
    justify-content: center;
    gap: calc(1 * var(--u));
  }
  @keyframes arrive {
    from {
      opacity: 0;
      transform: scale(0.94);
    }
  }
  @keyframes deal {
    from {
      opacity: 0;
      transform: translateY(calc(1.5 * var(--u)));
    }
  }
</style>
