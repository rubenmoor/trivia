<script lang="ts">
  // «Cambiazo»'s two-step picker (plans/09-jokers.md, "Cambiazo", JK-7): every bundle's broad categories
  // (D-43), then the subcategories of the chosen one (D-19), by key (bundle + name, D-99). Tiles without a fitting question are disabled
  // (the engine decides, 09 "Availability"). Click, or arrows + Enter; Backspace goes back.
  import { tick } from "svelte";
  import type { Jokers } from "../lib/types.ts";
  import { t } from "../lib/i18n.ts";
  import { displayName, questionLocale } from "../lib/names.svelte.ts";
  import { focusControl, pushScope } from "../lib/input.svelte.ts";
  import Prompt from "./Prompt.svelte";

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
  let picker = $state<HTMLDivElement>();

  async function focusFirst() {
    await tick();
    focusControl(grid?.querySelector<HTMLButtonElement>("button:not(:disabled)"));
  }
  focusFirst();

  async function open(g: Group) {
    group = g;
    await focusFirst();
  }

  async function back() {
    if (!group) return oncancel();
    const key = group.key;
    group = null;
    await tick();
    focusControl(grid?.querySelector<HTMLButtonElement>(`[data-key="${CSS.escape(key)}"]`));
  }

  // Esc cancels, Backspace goes back; arrows move over the picker (lib/focus.ts); Enter and Space press the focused tile.
  $effect(() =>
    pushScope({
      name: "cambiazo",
      modal: true,
      root: () => picker,
      handle: (a) => {
        if (a.type === "menu") oncancel();
        else if (a.type === "back") back();
        else return false;
        return true;
      },
    }),
  );
</script>

<div class="backdrop">
  <div class="picker glass-strong" bind:this={picker}>
    <h2 lang={group ? questionLocale() : undefined}>{group ? displayName("category", group.key) : t("joker.category.title")}</h2>
    {#key group}
      <div class="grid" class:subs={group} bind:this={grid} lang={questionLocale()}>
        {#if group}
          {#each group.subcategories as s, i (s.key)}
            <button class="tile" disabled={!s.available} onclick={() => onpick(s.key)} style:--i={i}>{displayName("subcategory", s.key)}</button>
          {/each}
        {:else}
          {#each categories as g, i (g.key)}
            <button class="tile" data-key={g.key} disabled={!g.available} onclick={() => open(g)} style:--i={i}>
              {displayName("category", g.key)}
            </button>
          {/each}
        {/if}
      </div>
    {/key}
    <div class="actions label">
      {#if group}<button class="secondary" onclick={back}>{t("action.back")} <Prompt action="back" /></button>{/if}
      <button class="secondary" onclick={oncancel}>{t("action.cancel")} <Prompt action="menu" pad={group ? "menu" : "back"} /></button>
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
    animation: zoom-in 0.35s var(--spring) backwards;
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
    box-shadow: 0 calc(0.25 * var(--u)) 0 var(--cream-edge);
    transition: transform 0.15s var(--spring);
    animation: deal 0.35s calc(var(--i) * 0.015s) var(--spring) backwards;
  }
  .tile:hover:not(:disabled),
  .tile:focus-visible,
  .tile:global([data-nav]) {
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
  @keyframes deal {
    from {
      opacity: 0;
      transform: translateY(calc(1.5 * var(--u)));
    }
  }
</style>
