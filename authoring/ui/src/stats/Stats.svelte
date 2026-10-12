<script lang="ts">
  // Statistics (plans/02-question-pool.md, QP-13): questions per broad category (D-19)
  // and per difficulty, approved questions only (the ones a game can use).
  // and media (RV-23).
  // URL: /stats/categories, /stats/subcategories, /stats/difficulty or /stats/media; ?bundle=colombia counts one
  // bundle only (RV-21), without it every bundle (the family's default, D-39).
  import { onMount } from "svelte";
  import { fetchAgeGroups, fetchBundles, fetchCategories, fetchMediaStats, fetchOverview, fetchQuestions, fetchTargets } from "../lib/api";
  import type { AgeGroups, Bundle, BundleTargets, Category, MediaStats as MediaStatsData, Question } from "../lib/types";
  import Nav from "../lib/Nav.svelte";
  import CategoryChart from "./CategoryChart.svelte";
  import DifficultyChart from "./DifficultyChart.svelte";
  import MediaStats from "./MediaStats.svelte";
  import SparseList from "./SparseList.svelte";
  import SubcategoryTable from "./SubcategoryTable.svelte";

  const page = location.pathname.startsWith("/stats/difficulty")
    ? "difficulty"
    : location.pathname.startsWith("/stats/subcategories")
      ? "subcategories"
      : location.pathname.startsWith("/stats/media")
        ? "media"
        : "categories";
  const bundle = new URLSearchParams(location.search).get("bundle");
  /** Link to a stats page or bundle, keeping the other choice. */
  function href(path: string, b: string | null = bundle) {
    return b ? `${path}?${new URLSearchParams({ bundle: b })}` : path;
  }
  const path = `/stats/${page}`;

  let questions = $state<Question[]>([]);
  let categories = $state<Category[]>([]);
  let ageGroups = $state<AgeGroups | null>(null);
  let bundles = $state<Bundle[]>([]);
  let mediaStats = $state<MediaStatsData | null>(null);
  /** The subcategories the next `qgen batch` picks; null until loaded or when it fails. */
  let nextBatch = $state<string[] | null>(null);
  /** The selected bundle's targets (D-53); null for all bundles or a bundle without targets. */
  let targets = $state<BundleTargets | null>(null);
  let loading = $state(true);
  let error = $state<string | null>(null);

  onMount(async () => {
    if (page === "subcategories") {
      // Only for the "next batch" marks: the page works without it.
      fetchOverview().then((o) => (nextBatch = o.next_batch_subcategories), () => {});
    }
    if (bundle && (page === "difficulty" || page === "categories")) {
      // Optional too: the charts work without targets.
      fetchTargets().then((t) => (targets = (t[bundle] as BundleTargets | undefined) ?? null), () => {});
    }
    try {
      if (page === "media") {
        [mediaStats, bundles] = await Promise.all([fetchMediaStats(bundle), fetchBundles()]);
        return;
      }
      [questions, categories, ageGroups, bundles] = await Promise.all([
        fetchQuestions({ status: "approved", bundle }),
        fetchCategories(),
        fetchAgeGroups(),
        fetchBundles(),
      ]);
    } catch (e) {
      error = e instanceof Error ? e.message : String(e);
    } finally {
      loading = false;
    }
  });

</script>

<main>
  <Nav current="stats" />
  <nav>
    <a href={href("/stats/categories")} class:current={page === "categories"}>Categories</a>
    <a href={href("/stats/subcategories")} class:current={page === "subcategories"}>Subcategories</a>
    <a href={href("/stats/difficulty")} class:current={page === "difficulty"}>Difficulty</a>
    <a href={href("/stats/media")} class:current={page === "media"}>Media</a>
  </nav>

  <p class="scope muted">
    Approved questions only · bundles:
    <a href={href(path, null)} class:current={!bundle}>all</a>
    {#each bundles as b (b.id)}{" · "}<a href={href(path, b.id)} class:current={bundle === b.id}>{b.name}</a>{/each}
  </p>

  {#if loading}
    <p class="muted">Loading…</p>
  {:else if error}
    <p class="error">{error}</p>
  {:else if page === "categories"}
    <CategoryChart {questions} {categories} {targets} {bundle} />
  {:else if page === "subcategories"}
    <SparseList {questions} {categories} {nextBatch} />
    <SubcategoryTable {questions} {categories} />
  {:else if page === "media"}
    {#if mediaStats}<MediaStats stats={mediaStats} />{/if}
  {:else if ageGroups}
    <DifficultyChart {questions} {ageGroups} {targets} />
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
  .scope {
    margin: 0 0 1.5rem;
    font-size: 0.9rem;
  }
  .scope a {
    color: var(--muted);
  }
  .scope a.current {
    color: var(--text);
    font-weight: 600;
    text-decoration: none;
  }
  .muted {
    color: var(--muted);
  }
  .error {
    color: var(--bad);
  }
</style>
