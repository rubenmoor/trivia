<script lang="ts">
  // Every subcategory with its approved questions, grouped by broad category in
  // app/data/categories.json order (RV-19). Each one links to its questions in the review tool.
  import type { Category, Question } from "../lib/types";
  import { breakdown, reviewLink } from "./breakdown";
  import "./chart.css";

  let { questions, categories }: { questions: Question[]; categories: Category[] } = $props();

  const rows = $derived(breakdown(questions, categories));
  const subMax = $derived(Math.max(1, ...rows.flatMap((r) => r.subs.map((s) => s.count))));
  const subCount = $derived(rows.reduce((n, r) => n + r.subs.length, 0));
</script>

<section class="chart-panel">
  <h2>Questions per subcategory</h2>
  <p class="sub">
    {questions.length} questions in {subCount} subcategories · grouped by category · a name opens its questions in
    the review tool
  </p>

  <div class="groups">
    {#each rows as row (row.name)}
      <section class="group">
        <h3>{row.name} <span class="total">{row.count}</span></h3>
        <table>
          <tbody>
            {#each row.subs as s (s.name)}
              <tr>
                <td class="name"><a href={reviewLink(s.name)}>{s.name}</a></td>
                <td class="bar-cell">
                  {#if s.count > 0}<span class="bar" style:width="{(s.count / subMax) * 100}%"></span>{/if}
                </td>
                <td class="num">{s.count}</td>
              </tr>
            {/each}
          </tbody>
        </table>
      </section>
    {/each}
  </div>
</section>

<style>
  .groups {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(min(100%, 280px), 1fr));
    gap: 1.25rem 2rem;
  }
  h3 {
    display: flex;
    justify-content: space-between;
    margin: 0 0 0.35rem;
    padding-bottom: 0.25rem;
    border-bottom: 1px solid #3a3d4a;
    font-size: 0.95rem;
  }
  .total {
    font-variant-numeric: tabular-nums;
    color: var(--muted);
    font-weight: 400;
  }
  table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.85rem;
  }
  td {
    padding: 0.12rem 0;
  }
  .name {
    width: 55%;
    padding-right: 0.5rem;
  }
  .name a {
    color: var(--text);
    text-decoration: none;
  }
  .name a:hover {
    text-decoration: underline;
  }
  .bar-cell {
    width: 35%;
  }
  .bar {
    display: block;
    height: 8px;
    background: var(--bar);
    border-radius: 0 3px 3px 0;
  }
  .num {
    width: 10%;
    text-align: right;
    font-variant-numeric: tabular-nums;
    color: var(--muted);
  }
</style>
