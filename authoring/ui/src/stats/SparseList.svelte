<script lang="ts">
  // Sparse areas of the approved pool, worst first (RV-20): categories with fewer questions
  // than a game asks, and subcategories a player sees whole in a game or two. A subcategory the
  // next `qgen batch` will pick (the 30 with the fewest approved questions) is marked.
  import type { Category, Question } from "../lib/types";
  import { breakdown, reviewLink, SPARSE_CATEGORY, SPARSE_SUBCATEGORY } from "./breakdown";
  import "./chart.css";

  let {
    questions,
    categories,
    nextBatch,
  }: { questions: Question[]; categories: Category[]; nextBatch: string[] | null } = $props();

  const rows = $derived(breakdown(questions, categories));
  // Stable sorts: ties keep the order of app/data/categories.json.
  const sparseCategories = $derived(rows.filter((r) => r.count < SPARSE_CATEGORY).sort((a, b) => a.count - b.count));
  const sparseSubs = $derived(
    rows
      .flatMap((r) => r.subs.map((s) => ({ ...s, category: r.name })))
      .filter((s) => s.count < SPARSE_SUBCATEGORY)
      .sort((a, b) => a.count - b.count),
  );
  const picked = $derived(new Set(nextBatch ?? []));
  const covered = $derived(sparseSubs.filter((s) => picked.has(s.name)).length);
</script>

<section class="chart-panel">
  <h2>Sparse areas</h2>
  <p class="sub">
    Categories with fewer than {SPARSE_CATEGORY} approved questions (a game asks {SPARSE_CATEGORY}), subcategories with
    fewer than {SPARSE_SUBCATEGORY}
    {#if nextBatch}· <span class="next">next batch</span>: the next <code>qgen batch</code> picks it ({covered} of {sparseSubs.length}){/if}
  </p>

  <div class="cols">
    <div>
      <h3>Categories <span class="n">{sparseCategories.length}</span></h3>
      {#if sparseCategories.length}
        <ul>
          {#each sparseCategories as c (c.name)}
            <li><span>{c.name}</span><span class="num">{c.count}</span></li>
          {/each}
        </ul>
      {:else}
        <p class="none">None.</p>
      {/if}
    </div>
    <div>
      <h3>Subcategories <span class="n">{sparseSubs.length}</span></h3>
      {#if sparseSubs.length}
        <ul>
          {#each sparseSubs as s (s.name)}
            <li>
              <span>
                <a href={reviewLink(s.name)}>{s.name}</a>
                <span class="cat">{s.category}</span>
                {#if picked.has(s.name)}<span class="next">next batch</span>{/if}
              </span>
              <span class="num">{s.count}</span>
            </li>
          {/each}
        </ul>
      {:else}
        <p class="none">None.</p>
      {/if}
    </div>
  </div>
</section>

<style>
  .cols {
    display: grid;
    grid-template-columns: minmax(0, 1fr) minmax(0, 2fr);
    gap: 1rem 2rem;
  }
  @media (max-width: 640px) {
    .cols {
      grid-template-columns: 1fr;
    }
  }
  h3 {
    margin: 0 0 0.35rem;
    padding-bottom: 0.25rem;
    border-bottom: 1px solid #3a3d4a;
    font-size: 0.95rem;
  }
  .n {
    color: var(--muted);
    font-weight: 400;
  }
  ul {
    list-style: none;
    margin: 0;
    padding: 0;
    font-size: 0.85rem;
  }
  li {
    display: flex;
    justify-content: space-between;
    gap: 0.75rem;
    padding: 0.12rem 0;
  }
  a {
    color: var(--text);
    text-decoration: none;
  }
  a:hover {
    text-decoration: underline;
  }
  .cat {
    margin-left: 0.4rem;
    color: var(--muted);
    font-size: 0.8rem;
  }
  .next {
    margin-left: 0.4rem;
    padding: 0 0.35rem;
    border-radius: 4px;
    background: var(--good-bg);
    color: var(--good);
    font-size: 0.75rem;
    white-space: nowrap;
  }
  .num {
    color: var(--warn);
    font-variant-numeric: tabular-nums;
  }
  .none {
    margin: 0;
    color: var(--muted);
    font-size: 0.85rem;
  }
</style>
