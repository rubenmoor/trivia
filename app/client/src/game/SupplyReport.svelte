<script lang="ts">
  // The supply report (GF-5): the pool can't fill a game; levels short, with their difficulty range.
  import { t } from "../lib/i18n.ts";
  import type { Supply } from "../lib/types.ts";

  let { supply }: { supply: Supply } = $props();
  const short = $derived(supply.levels.filter((l) => l.missing));
</script>

{#if !supply.ok}
  <div class="supply glass">
    <p>{t("supply.short", { n: supply.available })}</p>
    <ul class:many={short.length > 4}>
      {#each short as l (l.level)}
        <li>{t("supply.level", { level: l.level, lo: l.range[0], hi: l.range[1], missing: l.missing })}</li>
      {/each}
    </ul>
  </div>
{/if}

<style>
  .supply {
    padding: calc(1 * var(--u)) calc(1.6 * var(--u));
    font-size: calc(1.1 * var(--u));
    color: var(--amber);
    text-align: left;
  }
  .supply p {
    margin: 0;
  }
  .supply ul {
    margin: calc(0.4 * var(--u)) 0 0;
  }
  /* Many short levels: in columns, so Choice fits at 720p (plan 46). */
  .supply ul.many {
    columns: 4;
    column-gap: calc(2 * var(--u));
    padding: 0;
    list-style: none;
  }
  .supply li {
    break-inside: avoid;
  }
</style>
