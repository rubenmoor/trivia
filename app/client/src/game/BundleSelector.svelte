<script module lang="ts">
  import type { ChoiceOptions } from "../lib/api.ts";

  export type Bundle = ChoiceOptions["bundles"][number];

  /** Display order (plan 151): base bundles, then the optional ones: regional of the player's `region`, non-regional,
   * regional of other countries; file order (ours, then mods) within each group. */
  export function orderBundles(bundles: Bundle[], region: string): Bundle[] {
    const rank = (b: Bundle) => (b.base ? 0 : !b.region ? 2 : region && b.country === region ? 1 : 3);
    return [...bundles].sort((a, b) => rank(a) - rank(b));
  }

  /** A non-region bundle's symbol (decision 367): its `icon`, else `puzzle` (mods), `book` (base), `pin`. */
  export const bundleIcon = (b: Pick<Bundle, "base" | "icon" | "source">) => b.icon ?? (b.source === "mod" ? "puzzle" : b.base ? "book" : "pin");

  /** The count a tile shows (decision 267): shipped bundles fixed 6000+ (base) / 2000+, a mod's own count rounded
   * down (hundreds from 100, tens from 10), capped at the fixed string of its kind; the demo's base tile is counted
   * like a mod's, uncapped (decision 341). */
  export function countShown(b: Bundle): { n: number; plus: boolean } {
    const cap = b.base ? 6000 : 2000;
    const n = b.count;
    if (n === undefined || (n >= cap && !buildInfo().demo)) return { n: cap, plus: true };
    const n10 = n >= 100 ? Math.floor(n / 100) * 100 : n >= 10 ? Math.floor(n / 10) * 10 : n;
    return { n: n10, plus: n10 !== n };
  }

  /** One key per bundle (plan 29): the first letter of its name (after a «Regional:»-style prefix), accents
   * stripped, not taken by an earlier bundle nor in `reserved`, else the name's next letter; "" if none is left. */
  export function bundleKeys(names: string[], reserved: string[]): string[] {
    const taken = new Set(reserved.map((k) => k.toLowerCase()));
    return names.map((name) => {
      const ordered = name.includes(":") ? name.slice(name.lastIndexOf(":") + 1) + name : name;
      const letters = [...ordered.normalize("NFD").replace(/\p{M}/gu, "").toLowerCase()].filter((c) => /\p{L}/u.test(c));
      const key = letters.find((c) => !taken.has(c)) ?? "";
      if (key) taken.add(key);
      return key;
    });
  }
</script>

<script lang="ts">
  // Shared bundle selector (D-88): every bundle a toggle, base ones apart from the others; at most one base
  // bundle (decision 752). Bundles screen in every mode (plan 151): narrow base column, ruler, flowing optional
  // tiles (names, counts) that scroll with focus; «Ajustes de la partida» (MD-12): compact, with descriptions.
  import { toggled } from "./toggled.ts";
  import { buildInfo } from "../lib/build.ts";
  import { playerRegion } from "../lib/desktop.ts";
  import { t } from "../lib/i18n.ts";
  import BundleMark from "./BundleMark.svelte";
  import Icon from "./Icon.svelte";
  import OptionButton from "./OptionButton.svelte";
  import Prompt from "./Prompt.svelte";
  import { scrollBox } from "./scrollBox.ts";
  import { sfx } from "./sound.svelte.ts";

  let {
    bundles,
    selected,
    busy = false,
    keyOf = () => "",
    first = 0,
    large = false,
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
    /** The Bundles screen's layout. */
    large?: boolean;
    onchange: (ids: string[]) => void;
  } = $props();

  const ordered = $derived(orderBundles(bundles, playerRegion));
  const base = $derived(ordered.filter((b) => b.base));
  const others = $derived(ordered.filter((b) => !b.base));

  function toggle(b: Bundle) {
    if (busy) return;
    sfx("tick");
    onchange(toggled(bundles, selected, b));
  }
</script>

{#if large}
  <div class="bundles large" data-line>
    <div class="column base">
      <div class="group">
        {#each base as b, i (b.id)}
          {@render tile(b, first + i)}
        {/each}
      </div>
    </div>
    {#if others.length}
      <span class="ruler"></span>
      <div class="column">
        <div class="group grid" {@attach scrollBox}>
          {#each others as b, i (b.id)}
            {@render tile(b, first + base.length + i)}
          {/each}
        </div>
      </div>
    {/if}
  </div>
{:else}
  <div class="bundles" data-line>
    <div class="group">
      {#each base as b, i (b.id)}
        {@render tile(b, first + i)}
      {/each}
    </div>
    {#if others.length}
      <span class="divider"></span>
      <div class="group">
        {#each others as b, i (b.id)}
          {@render tile(b, first + base.length + i)}
        {/each}
      </div>
    {/if}
  </div>
{/if}

{#snippet tile(b: Bundle, i: number)}
  {@const on = selected.includes(b.id)}
  {@const key = keyOf(b)}
  <OptionButton
    class="bundle"
    {on}
    dim
    compact={large}
    style="--i:{i}"
    role="switch"
    aria-checked={on}
    onclick={() => toggle(b)}
    disabled={busy}
    data-focus-id="bundle-{b.id}"
    caption={b.base && buildInfo().demo ? t("bundles.demoName") : b.name}
  >
    {#snippet icon()}<BundleMark bundle={b} />{/snippet}
    {#snippet chip()}{#if key}<Prompt action={{ type: "letter", key }} hold />{/if}{/snippet}
    {#if large}
      {@const c = countShown(b)}
      <span class="label count">{t(c.plus ? "bundles.countPlus" : "bundles.count", { n: c.n })}</span>
      {#if on}<span class="check"><Icon name="check" /></span>{/if}
    {:else}
      <span class="switch label">{t(on ? "choice.on" : "choice.off")}</span>
      <span class="label description">{b.description}</span>
    {/if}
    {#if b.source === "mod"}<span class="label made"><Icon name="puzzle" /> {t("bundles.playerMade", { mod: b.modName ?? "" })}</span>{/if}
  </OptionButton>
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
  :global(.bundle:not(.on)) .switch {
    color: var(--slate-400);
  }
  .switch {
    color: var(--sky);
  }
  .made {
    color: var(--amber);
  }
  /* Bundles screen (plan 151): a narrow base column, a ruler, fixed-width optional tiles flowing in a grid that
     scrolls (scrollBox.ts). */
  .bundles.large {
    flex-wrap: nowrap;
    align-items: stretch;
    gap: calc(2.4 * var(--u));
    min-height: 0;
    max-width: calc(100 * var(--u));
  }
  .column {
    display: flex;
    flex-direction: column;
    min-height: 0;
  }
  .large .group {
    padding: calc(0.6 * var(--u));
  }
  .large .base .group {
    flex-direction: column;
    flex-wrap: nowrap;
    justify-content: flex-start;
    gap: calc(1 * var(--u));
  }
  .ruler {
    flex: none;
    width: calc(0.15 * var(--u));
    background: var(--slate-600);
    border-radius: calc(0.1 * var(--u));
  }
  .grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, calc(26 * var(--u)));
    justify-content: start;
    align-content: start;
    gap: calc(1 * var(--u));
  }
  .large .label {
    font-size: calc(1.2 * var(--u));
  }
  .count {
    color: var(--slate-400);
  }
  .check {
    position: absolute;
    top: calc(0.5 * var(--u));
    right: calc(0.6 * var(--u));
    width: calc(2 * var(--u));
    color: var(--sky);
  }
</style>
