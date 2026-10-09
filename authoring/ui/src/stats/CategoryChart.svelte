<script lang="ts">
  // Questions per broad category (D-19), most first. Click a bar to open its subcategories
  // (RV-19); each one links to its approved questions in the review tool.
  import type { Category, Question } from "../lib/types";
  import { breakdown, reviewLink, type CategoryRow } from "./breakdown";
  import "./chart.css";

  let { questions, categories }: { questions: Question[]; categories: Category[] } = $props();

  // Stable sort: ties keep the order of app/data/categories.json.
  const rows = $derived(breakdown(questions, categories).sort((a, b) => b.count - a.count));
  const max = $derived(Math.max(1, ...rows.map((r) => r.count)));
  /** Subcategory bars share one scale across categories, so they compare. */
  const subMax = $derived(Math.max(1, ...rows.flatMap((r) => r.subs.map((s) => s.count))));
  const empty = $derived(rows.filter((r) => r.count === 0).length);

  let open = $state(new Set<string>());
  const allOpen = $derived(rows.length > 0 && rows.every((r) => open.has(r.name)));

  function toggle(row: CategoryRow) {
    const next = new Set(open);
    if (!next.delete(row.name)) next.add(row.name);
    open = next;
  }
  function toggleAll() {
    open = allOpen ? new Set() : new Set(rows.map((r) => r.name));
  }
  const bySize = (row: CategoryRow) => [...row.subs].sort((a, b) => b.count - a.count);
</script>

<section class="chart-panel">
  <h2>Questions per category</h2>
  <p class="sub">
    {questions.length} questions in {rows.length - empty} of {rows.length} categories{empty
      ? ` · ${empty} without questions`
      : ""} · click a bar for its subcategories ·
    <button class="link" onclick={toggleAll}>{allOpen ? "close all" : "open all"}</button>
  </p>

  <ol class="bars">
    {#each rows as row (row.name)}
      <li>
        <button class="row" aria-expanded={open.has(row.name)} onclick={() => toggle(row)}>
          <span class="label">{row.name}</span>
          <span class="track">
            {#if row.count > 0}
              <span class="bar" style:width="{(row.count / max) * 100}%"></span>
            {/if}
            <span class="value">{row.count}</span>
            <span class="more">{row.subs.length} sub{open.has(row.name) ? " ▴" : " ▾"}</span>
          </span>
        </button>
        {#if open.has(row.name)}
          <ol class="subs">
            {#each bySize(row) as s (s.name)}
              <li class="row">
                <a class="label" href={reviewLink(s.name)} title="Review its approved questions">{s.name}</a>
                <span class="track">
                  {#if s.count > 0}
                    <span class="bar sub-bar" style:width="{(s.count / subMax) * 100}%"></span>
                  {/if}
                  <span class="value">{s.count}</span>
                </span>
              </li>
            {/each}
          </ol>
        {/if}
      </li>
    {/each}
  </ol>
</section>

<style>
  .bars,
  .subs {
    list-style: none;
    margin: 0;
    padding: 0;
  }
  .subs {
    margin: 0.15rem 0 0.6rem;
    font-size: 0.85rem;
  }
  .row {
    display: grid;
    grid-template-columns: minmax(8rem, 15rem) 1fr;
    align-items: center;
    gap: 0.75rem;
    width: 100%;
    padding: 4px 0;
    border: 0;
    background: none;
    color: inherit;
    font: inherit;
    text-align: left;
  }
  button.row {
    cursor: pointer;
  }
  button.row:hover .value,
  button.row:hover .label {
    color: var(--text);
  }
  button.row:focus-visible {
    outline: 2px solid var(--accent);
    outline-offset: 2px;
    border-radius: 4px;
  }
  .label {
    text-align: right;
    font-size: 0.9rem;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  .subs .label {
    font-size: 0.85rem;
    color: var(--muted);
    text-decoration: none;
  }
  .subs a.label:hover {
    color: var(--text);
    text-decoration: underline;
  }
  .track {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    min-width: 0;
    /* Room for the value label after the longest bar. */
    padding-right: 6.5rem;
    border-left: 1px solid #3a3d4a;
  }
  .bar {
    height: 18px;
    background: var(--bar);
    border-radius: 0 4px 4px 0;
    flex: none;
  }
  .sub-bar {
    height: 10px;
    opacity: 0.7;
  }
  .value {
    font-size: 0.85rem;
    font-variant-numeric: tabular-nums;
    color: var(--muted);
  }
  .more {
    flex: none;
    white-space: nowrap;
    font-size: 0.75rem;
    color: var(--muted);
    opacity: 0.7;
  }
  .link {
    border: 0;
    padding: 0;
    background: none;
    color: var(--muted);
    font: inherit;
    text-decoration: underline;
    cursor: pointer;
  }
  .link:hover {
    color: var(--text);
  }
  @media (max-width: 560px) {
    .row {
      grid-template-columns: 1fr;
      gap: 0.15rem;
    }
    .label {
      text-align: left;
    }
  }
</style>
