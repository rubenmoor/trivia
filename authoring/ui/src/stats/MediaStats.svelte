<script lang="ts">
  // Approved questions per media role and per image resolution (RV-23).
  import type { MediaStats } from "../lib/types";
  import "./chart.css";

  let { stats }: { stats: MediaStats } = $props();

  const TYPES = ["image", "audio", "video"] as const;
  const roleMax = $derived(Math.max(1, ...stats.roles.map((r) => r.questions)));
  const bandMax = $derived(Math.max(1, ...stats.bands.map((b) => b.questions)));
  const images = $derived(stats.bands.reduce((n, b) => n + b.questions, 0));
</script>

<section class="chart-panel">
  <h2>Questions per media role</h2>
  <p class="sub">{stats.questions} questions · split by media type and missing file</p>
  <table class="bars">
    <thead>
      <tr><th></th><th></th><th class="num">all</th>{#each TYPES as t (t)}<th class="num">{t}</th>{/each}<th class="num">no file</th></tr>
    </thead>
    <tbody>
      {#each stats.roles as r (r.role)}
        <tr>
          <td class="name">{r.role}</td>
          <td class="bar-cell"><span class="bar" style:width="{(r.questions / roleMax) * 100}%"></span></td>
          <td class="num strong">{r.questions}</td>
          {#each TYPES as t (t)}<td class="num">{r[t] ?? 0}</td>{/each}
          <td class="num" class:warn={r.no_file > 0}>{r.no_file}</td>
        </tr>
      {/each}
    </tbody>
  </table>
</section>

<section class="chart-panel">
  <h2>Questions per image resolution</h2>
  <p class="sub">{images} picked images · long edge in px, read from the cached file · the TV shows 1920 × 1080</p>
  <table class="bars">
    <tbody>
      {#each stats.bands as b (b.band)}
        <tr>
          <td class="name">{b.band}</td>
          <td class="bar-cell">
            {#if b.questions > 0}<span class="bar" style:width="{(b.questions / bandMax) * 100}%"></span>{/if}
          </td>
          <td class="num strong">{b.questions}</td>
        </tr>
      {/each}
    </tbody>
  </table>
  {#if stats.bands.some((b) => b.band === "not cached")}
    <p class="sub note">Not cached: run <code>trivia-media sync --status approved</code> to read their size.</p>
  {/if}
  {#if stats.sizes.length}
    <details class="table-view">
      <summary>Most common exact sizes</summary>
      <table>
        <tbody>
          {#each stats.sizes as s (s.size)}
            <tr><td>{s.size}</td><td class="num">{s.questions}</td></tr>
          {/each}
        </tbody>
      </table>
    </details>
  {/if}
</section>

<style>
  table.bars {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.9rem;
  }
  th {
    color: var(--muted);
    font-weight: 400;
    font-size: 0.8rem;
  }
  td,
  th {
    padding: 0.2rem 0.5rem 0.2rem 0;
  }
  .name {
    width: 9rem;
  }
  .bar-cell {
    width: 45%;
  }
  .bar {
    display: block;
    height: 8px;
    background: var(--bar);
    border-radius: 0 3px 3px 0;
  }
  .num {
    text-align: right;
    font-variant-numeric: tabular-nums;
    color: var(--muted);
  }
  .num.strong {
    color: var(--text);
  }
  .num.warn {
    color: var(--warn);
  }
  .note {
    margin: 0.75rem 0 0;
  }
</style>
