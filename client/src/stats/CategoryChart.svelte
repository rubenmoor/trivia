<script lang="ts">
  // Questions per broad category (D-19), most first. Hover a row for its subcategories.
  import type { Category, Question } from "../lib/types";
  import "./chart.css";

  let { questions, categories }: { questions: Question[]; categories: Category[] } = $props();

  interface Row {
    name: string;
    count: number;
    subs: { name: string; count: number }[];
  }

  const rows = $derived.by(() => {
    const perSub = new Map<string, number>();
    for (const q of questions) perSub.set(q.subcategory, (perSub.get(q.subcategory) ?? 0) + 1);
    const known = new Set(categories.flatMap((c) => c.subcategories));
    const out: Row[] = categories.map((c) => {
      const subs = c.subcategories.map((s) => ({ name: s, count: perSub.get(s) ?? 0 }));
      return { name: c.name, count: subs.reduce((n, s) => n + s.count, 0), subs };
    });
    const unknown = [...perSub].filter(([s]) => !known.has(s)).map(([name, count]) => ({ name, count }));
    if (unknown.length) {
      out.push({ name: "(not in categories.json)", count: unknown.reduce((n, s) => n + s.count, 0), subs: unknown });
    }
    // Stable sort: ties keep the order of data/categories.json.
    return out.sort((a, b) => b.count - a.count);
  });
  const max = $derived(Math.max(1, ...rows.map((r) => r.count)));
  const empty = $derived(rows.filter((r) => r.count === 0).length);

  let hover = $state<{ row: Row; x: number; y: number } | null>(null);

  function move(row: Row, e: PointerEvent) {
    // Keep the tooltip inside the window.
    const x = Math.min(e.clientX + 16, window.innerWidth - 360);
    const y = Math.min(e.clientY + 16, window.innerHeight - 280);
    hover = { row, x: Math.max(8, x), y: Math.max(8, y) };
  }
</script>

<section class="chart-panel">
  <h2>Questions per category</h2>
  <p class="sub">
    {questions.length} questions in {rows.length - empty} of {rows.length} categories{empty
      ? ` · ${empty} without questions`
      : ""} · hover a bar for its subcategories
  </p>

  <ol class="bars">
    {#each rows as row (row.name)}
      <li
        onpointermove={(e) => move(row, e)}
        onpointerleave={() => (hover = null)}
        class:dim={hover && hover.row !== row}
      >
        <span class="label">{row.name}</span>
        <span class="track">
          {#if row.count > 0}
            <span class="bar" style:width="{(row.count / max) * 100}%"></span>
          {/if}
          <span class="value">{row.count}</span>
        </span>
      </li>
    {/each}
  </ol>

  <details class="table-view">
    <summary>Table with subcategories</summary>
    <table>
      <thead><tr><th>Category</th><th>Subcategory</th><th class="num">Questions</th></tr></thead>
      <tbody>
        {#each rows as row}
          {#each row.subs as s, i}
            <tr>
              <td>{i === 0 ? `${row.name} (${row.count})` : ""}</td>
              <td>{s.name}</td>
              <td class="num">{s.count}</td>
            </tr>
          {/each}
        {/each}
      </tbody>
    </table>
  </details>
</section>

{#if hover}
  {@const used = hover.row.subs.filter((s) => s.count > 0).sort((a, b) => b.count - a.count)}
  {@const unused = hover.row.subs.length - used.length}
  <div class="tooltip" style:left="{hover.x}px" style:top="{hover.y}px">
    <strong>{hover.row.name} · {hover.row.count}</strong>
    {#each used as s}
      <div>{s.name} · {s.count}</div>
    {/each}
    {#if unused}
      <div class="muted">{unused} subcategor{unused === 1 ? "y" : "ies"} without questions</div>
    {/if}
  </div>
{/if}

<style>
  .bars {
    list-style: none;
    margin: 0;
    padding: 0;
  }
  li {
    display: grid;
    grid-template-columns: minmax(8rem, 15rem) 1fr;
    align-items: center;
    gap: 0.75rem;
    /* The whole row is the hover target, not just the bar. */
    padding: 4px 0;
    transition: opacity 0.12s;
  }
  li.dim {
    opacity: 0.45;
  }
  .label {
    text-align: right;
    font-size: 0.9rem;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  .track {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    min-width: 0;
    /* Room for the value label after the longest bar. */
    padding-right: 2.5rem;
    border-left: 1px solid #3a3d4a;
  }
  .bar {
    height: 18px;
    background: var(--bar);
    border-radius: 0 4px 4px 0;
    flex: none;
  }
  .value {
    font-size: 0.85rem;
    font-variant-numeric: tabular-nums;
    color: var(--muted);
  }
  li:hover .value {
    color: var(--text);
  }
  @media (max-width: 560px) {
    li {
      grid-template-columns: 1fr;
      gap: 0.15rem;
    }
    .label {
      text-align: left;
    }
  }
</style>
