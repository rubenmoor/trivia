<script lang="ts">
  // «Cambiazo»'s two-step picker (plans/09-jokers.md, "Cambiazo", JK-7): every bundle's broad categories
  // (D-43), then the subcategories of the chosen one (D-19), by key (bundle + slug, decision 259). Tiles without a fitting question are disabled
  // (the engine decides, 09 "Availability"). Click, or arrows + Enter; Backspace goes back. Several bundles: a header
  // per bundle in the Bundles screen's order (plan 185); the categories scroll with focus.
  import { tick } from "svelte";
  import type { Jokers } from "../lib/types.ts";
  import { fetchChoiceOptions } from "../lib/api.ts";
  import { playerRegion } from "../lib/desktop.ts";
  import { lang, t } from "../lib/i18n.ts";
  import { displayName, questionLocale } from "../lib/names.svelte.ts";
  import { focusControl, pushScope } from "../lib/input.svelte.ts";
  import { orderBundles, type Bundle } from "./BundleSelector.svelte";
  import BundleMark from "./BundleMark.svelte";
  import Icon from "./Icon.svelte";
  import { jokerIcon } from "./jokers.ts";
  import Prompt from "./Prompt.svelte";
  import { scrollBox } from "./scrollBox.ts";

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
  let bundles = $state<Bundle[] | null>(null);

  /** Per bundle its categories and the index of its first tile; one section without `id` if only one bundle. */
  const sections = $derived.by(() => {
    if (!bundles) return [];
    const ids = new Set(categories.map((g) => g.bundle));
    if (ids.size < 2) return [{ id: null, bundle: null, categories, first: 0 }];
    const order = [...orderBundles(bundles, playerRegion).map((b) => b.id), ...ids];
    let first = 0;
    return [...new Set(order)].filter((id) => ids.has(id)).map((id) => {
      const own = categories.filter((g) => g.bundle === id);
      const s = { bundle: bundles!.find((b) => b.id === id) ?? null, id, categories: own, first };
      first += own.length;
      return s;
    });
  });

  async function focusFirst() {
    await tick();
    focusControl(grid?.querySelector<HTMLButtonElement>("button:not(:disabled)"));
  }
  fetchChoiceOptions("game").then(
    (o) => o.bundles,
    () => [],
  ).then((b) => {
    bundles = b;
    focusFirst();
  });

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
    <h2 lang={group ? questionLocale() : undefined}><Icon name={jokerIcon("category")} /> {group ? displayName("category", group.key) : t("joker.category.title")}</h2>
    {#key group}
      {#if group}
        <div class="grid subs" bind:this={grid} lang={questionLocale()}>
          {#each group.subcategories as s, i (s.key)}
            <button class="tile" disabled={!s.available} onclick={() => onpick(s.key)} style:--i={i}>{displayName("subcategory", s.key)}</button>
          {/each}
        </div>
      {:else}
        <div class="grid" bind:this={grid} lang={questionLocale()} {@attach scrollBox}>
          {#each sections as sec (sec.id)}
            {#if sec.id}
              <h3 class="head label" {lang} style:--i={sec.first}>
                {#if sec.bundle}<BundleMark bundle={sec.bundle} />{/if}
                {displayName("bundle", sec.id)}
              </h3>
            {/if}
            {#each sec.categories as g, i (g.key)}
              <button class="tile" data-key={g.key} disabled={!g.available} onclick={() => open(g)} style:--i={sec.first + i}>
                {displayName("category", g.key)}
              </button>
            {/each}
          {/each}
        </div>
      {/if}
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
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(5, 8, 16, 0.55);
  }
  .picker {
    width: min(92%, calc(100 * var(--u)));
    max-height: 92%;
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
    padding: calc(0.5 * var(--u));
  }
  .head {
    grid-column: 1 / -1;
    margin: calc(0.6 * var(--u)) 0 0;
    color: var(--slate-400);
    font-size: calc(1.3 * var(--u));
    letter-spacing: 0.1em;
    text-transform: uppercase;
    animation: deal 0.35s calc(var(--i) * 0.015s) var(--spring) backwards;
  }
  .head:first-child {
    margin-top: 0;
  }
  .head > :global(.flags) {
    vertical-align: -0.15em;
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
