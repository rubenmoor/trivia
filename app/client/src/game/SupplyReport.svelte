<script lang="ts">
  // The supply report (GF-5): the pool can't fill a game; levels short, with their difficulty range.
  import { t } from "../lib/i18n";
  import type { Supply } from "../lib/types";

  let { supply }: { supply: Supply } = $props();
</script>

{#if !supply.ok}
  <div class="supply glass">
    <p>{t("supply.short", { n: supply.available })}</p>
    <ul>
      {#each supply.levels.filter((l) => l.missing) as l (l.level)}
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
</style>
