<script lang="ts">
  // Statistics (plans/02-question-pool.md, QP-13): questions per broad category (D-19)
  // and per difficulty, approved questions only (the ones a game can use).
  // URL: /stats/categories or /stats/difficulty.
  import { onMount } from "svelte";
  import { fetchCategories, fetchQuestions } from "../lib/api";
  import type { Category, Question } from "../lib/types";
  import CategoryChart from "./CategoryChart.svelte";
  import DifficultyChart from "./DifficultyChart.svelte";

  const page = location.pathname.startsWith("/stats/difficulty") ? "difficulty" : "categories";

  let questions = $state<Question[]>([]);
  let categories = $state<Category[]>([]);
  let loading = $state(true);
  let error = $state<string | null>(null);

  onMount(async () => {
    try {
      [questions, categories] = await Promise.all([fetchQuestions({ status: "approved" }), fetchCategories()]);
    } catch (e) {
      error = e instanceof Error ? e.message : String(e);
    } finally {
      loading = false;
    }
  });

</script>

<main>
  <nav>
    <a href="/stats/categories" class:current={page === "categories"}>Categories</a>
    <a href="/stats/difficulty" class:current={page === "difficulty"}>Difficulty</a>
    <a href="/review" class="review">Review tool →</a>
  </nav>

  <p class="scope muted">Approved questions only</p>

  {#if loading}
    <p class="muted">Loading…</p>
  {:else if error}
    <p class="error">{error}</p>
  {:else if page === "categories"}
    <CategoryChart {questions} {categories} />
  {:else}
    <DifficultyChart {questions} />
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
  .scope {
    margin: 0 0 1.5rem;
    font-size: 0.9rem;
  }
  .muted {
    color: var(--muted);
  }
  .error {
    color: var(--bad);
  }
</style>
