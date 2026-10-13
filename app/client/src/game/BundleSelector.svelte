<script module lang="ts">
  import type { ChoiceOptions } from "../lib/api.ts";

  export type Bundle = ChoiceOptions["bundles"][number];

  /** `selected` after picking `b`: a base bundle replaces the other base bundle; another bundle toggles. */
  export function toggled(bundles: Bundle[], selected: string[], b: Bundle): string[] {
    const on = (x: Bundle) => (b.base && x.base ? x.id === b.id : x.id === b.id ? !selected.includes(x.id) : selected.includes(x.id));
    return bundles.filter(on).map((x) => x.id);
  }
</script>

<script lang="ts">
  // Shared bundle selector (D-88): the base bundles as a radio group, apart from the others (toggles);
  // exactly one base bundle (D-85). Configure screen; the gamemaster menu reuses it (MD-12).
  import { t } from "../lib/i18n.ts";
  import Icon from "./Icon.svelte";
  import Prompt from "./Prompt.svelte";

  let {
    bundles,
    selected,
    busy = false,
    keyOf = () => "",
    first = 0,
    onchange,
  }: {
    /** The language's bundles (`fetchChoiceOptions`, `bundlesFor`). */
    bundles: Bundle[];
    selected: string[];
    busy?: boolean;
    /** A bundle's letter key, "" for none. */
    keyOf?: (b: Bundle) => string;
    /** Animation index of the first tile. */
    first?: number;
    onchange: (ids: string[]) => void;
  } = $props();

  const base = $derived(bundles.filter((b) => b.base));
  const others = $derived(bundles.filter((b) => !b.base));

  function toggle(b: Bundle) {
    if (!busy) onchange(toggled(bundles, selected, b));
  }
</script>

<div class="bundles" data-line>
  <div class="group" role="radiogroup">
    {#each base as b, i (b.id)}
      {@render tile(b, "radio", first + i)}
    {/each}
  </div>
  {#if others.length}
    <span class="divider"></span>
    <div class="group">
      {#each others as b, i (b.id)}
        {@render tile(b, "switch", first + base.length + i)}
      {/each}
    </div>
  {/if}
</div>

{#snippet tile(b: Bundle, role: "radio" | "switch", i: number)}
  {@const on = selected.includes(b.id)}
  {@const key = keyOf(b)}
  <button
    class="tile bundle glass"
    class:on
    style:--i={i}
    {role}
    aria-checked={on}
    onclick={() => toggle(b)}
    disabled={busy}
    data-focus-id="bundle-{b.id}"
  >
    {#if key}<Prompt action={{ type: "letter", key }} hold />{/if}
    <span class="name-text">{b.name}</span>
    {#if role === "switch"}<span class="switch label">{t(on ? "choice.on" : "choice.off")}</span>{/if}
    <span class="label description">{b.description}</span>
    {#if b.source === "mod"}<span class="label made"><Icon name="puzzle" /> {t("bundles.playerMade", { mod: b.modName ?? "" })}</span>{/if}
  </button>
{/snippet}

<style>
  .bundles {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    align-items: stretch;
    gap: calc(1.2 * var(--u));
    max-width: calc(110 * var(--u));
  }
  .group {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: calc(1.2 * var(--u));
  }
  .divider {
    width: calc(0.15 * var(--u));
    background: var(--slate-600);
    border-radius: calc(0.1 * var(--u));
  }
  .tile {
    display: grid;
    grid-template-columns: auto 1fr;
    column-gap: calc(1 * var(--u));
    align-items: center;
    min-width: calc(20 * var(--u));
    max-width: calc(34 * var(--u));
    padding: calc(1 * var(--u)) calc(1.6 * var(--u));
    border-color: var(--slate-600);
    text-align: left;
    transition:
      transform 0.2s var(--spring),
      border-color 0.2s,
      opacity 0.2s;
    animation: arrive 0.5s calc(0.15s + var(--i) * 0.05s) var(--spring) backwards;
  }
  .tile > :global(kbd) {
    grid-row: span 4;
  }
  .tile > :not(:global(kbd)) {
    grid-column: 2;
  }
  .tile:hover:not(:disabled) {
    transform: translateY(calc(-0.3 * var(--u)));
  }
  .tile.on {
    border-color: var(--sky);
    background: rgba(76, 201, 240, 0.16);
    transform: translateY(calc(-0.3 * var(--u)));
  }
  .name-text {
    font-family: var(--font-display);
    font-size: calc(2 * var(--u));
    font-weight: 800;
    line-height: 1.1;
  }
  .bundle:not(.on) .name-text,
  .bundle:not(.on) .switch {
    color: var(--slate-400);
  }
  .switch {
    color: var(--sky);
  }
  .made {
    color: var(--amber);
  }
</style>
