<script lang="ts">
  // Statistics (plans/02-question-pool.md, QP-13): questions per broad category (D-19)
  // and per difficulty. URL: /stats/categories or /stats/difficulty, ?status=approved.
  import { onMount } from "svelte";
  import { fetchCategories, fetchQuestions } from "../lib/api";
  import type { Category, Question, Status } from "../lib/types";
  import CategoryChart from "./CategoryChart.svelte";
  import DifficultyChart from "./DifficultyChart.svelte";

  type Filter = Status | "all";
  const FILTERS: Filter[] = ["all", "approved", "draft", "needs_work", "rejected"];
  const LABELS: Record<Filter, string> = {
    all: "All",
    approved: "Approved",
    draft: "Draft",
    needs_work: "Needs work",
    rejected: "Rejected",
  };

  const page = location.pathname.startsWith("/stats/difficulty") ? "difficulty" : "categories";
  const initial = new URLSearchParams(location.search).get("status") as Filter | null;

  let filter = $state<Filter>(initial && FILTERS.includes(initial) ? initial : "all");
  let questions = $state<Question[]>([]);
  let categories = $state<Category[]>([]);
  let loading = $state(true);
  let error = $state<string | null>(null);

  const shown = $derived(filter === "all" ? questions : questions.filter((q) => q.status === filter));
  const countOf = (f: Filter) => (f === "all" ? questions.length : questions.filter((q) => q.status === f).length);

  onMount(async () => {
    try {
      [questions, categories] = await Promise.all([fetchQuestions(null), fetchCategories()]);
    } catch (e) {
      error = e instanceof Error ? e.message : String(e);
    } finally {
      loading = false;
    }
  });

  function choose(f: Filter) {
    filter = f;
    const url = new URL(location.href);
    if (f === "all") url.searchParams.delete("status");
    else url.searchParams.set("status", f);
    history.replaceState(null, "", url);
  }

  /** Page links keep the status filter. */
  function href(p: string) {
    return `/stats/${p}${filter === "all" ? "" : `?status=${filter}`}`;
  }
</script>

<main>
  <nav>
    <a href={href("categories")} class:current={page === "categories"}>Categories</a>
    <a href={href("difficulty")} class:current={page === "difficulty"}>Difficulty</a>
    <a href="/" class="review">Review tool →</a>
  </nav>

  <div class="filters" role="group" aria-label="Filter by status">
    {#each FILTERS as f}
      <button class:active={filter === f} aria-pressed={filter === f} onclick={() => choose(f)}>
        {LABELS[f]} <span class="n">{countOf(f)}</span>
      </button>
    {/each}
  </div>

  {#if loading}
    <p class="muted">Loading…</p>
  {:else if error}
    <p class="error">{error}</p>
  {:else if page === "categories"}
    <CategoryChart questions={shown} {categories} />
  {:else}
    <DifficultyChart questions={shown} />
  {/if}
</main>

<style>
  main {
    max-width: 1000px;
    margin: 0 auto;
    padding: 1.5rem 1rem 4rem;
  }
  nav {
    display: flex;
    flex-wrap: wrap;
    gap: 0.25rem 1.5rem;
    align-items: baseline;
    margin-bottom: 1rem;
  }
  nav a {
    color: var(--muted);
    text-decoration: none;
    font-size: 1.25rem;
    font-weight: 600;
  }
  nav a.current {
    color: var(--text);
  }
  nav a:hover {
    color: var(--text);
  }
  nav .review {
    margin-left: auto;
    font-size: 0.95rem;
    font-weight: 400;
  }
  .filters {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-bottom: 1.5rem;
  }
  .filters button {
    font: inherit;
    font-size: 0.9rem;
    color: var(--muted);
    background: transparent;
    border: 1px solid var(--panel);
    border-radius: 999px;
    padding: 0.3rem 0.85rem;
    cursor: pointer;
  }
  .filters button.active {
    color: var(--text);
    background: var(--panel);
  }
  .n {
    font-variant-numeric: tabular-nums;
    opacity: 0.7;
  }
  .muted {
    color: var(--muted);
  }
  .error {
    color: var(--bad);
  }
</style>
