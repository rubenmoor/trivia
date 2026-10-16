<script lang="ts">
  // Statistics (plans/02-question-pool.md, QP-13): questions per broad category (D-19)
  // and subcategory, per difficulty and per media (RV-23), approved questions only (the ones a game can use).
  // URL: /stats/categories, /stats/subcategories, /stats/difficulty or /stats/media; ?bundle=colombia counts one
  // bundle only (RV-21), without it every bundle (the family's default, D-39).
  // ?locale=<L>: the locale's pool, its own approved sources and playing translations with their own difficulty,
  // its names (plan 67, decision 235); without: every approved source, whatever its language.
  import { onMount } from "svelte";
  import { LOCALES } from "$app/lib/data.ts";
  import { messageOf } from "$app/lib/http.ts";
  import { fetchAgeGroups, fetchBundles, fetchCategories, fetchMediaStats, fetchNames, fetchOverview, fetchQuestions, fetchTargets } from "../lib/api.ts";
  import type { AgeGroups, Bundle, BundleTargets, Category, MediaStats as MediaStatsData, Names, Question } from "../lib/types.ts";
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
  const params = new URLSearchParams(location.search);
  const bundle = params.get("bundle");
  const locale = params.get("locale");
  /** Link to a stats page, bundle or locale, keeping the other choices. */
  function href(path: string, b: string | null = bundle, l: string | null = locale) {
    const q = new URLSearchParams({ ...(b ? { bundle: b } : {}), ...(l ? { locale: l } : {}) });
    return q.size ? `${path}?${q}` : path;
  }
  const path = `/stats/${page}`;

  let questions = $state<Question[]>([]);
  let categories = $state<Category[]>([]);
  let ageGroups = $state<AgeGroups | null>(null);
  let bundles = $state<Bundle[]>([]);
  let mediaStats = $state<MediaStatsData | null>(null);
  let names = $state<Names | null>(null);
  /** The base subcategories the next `qgen batch` picks; null until loaded or when it fails. */
  let nextBatch = $state<string[] | null>(null);
  /** The selected bundle's targets (D-53); null for all bundles or a bundle without targets. */
  let targets = $state<BundleTargets | null>(null);
  /** Bundles in view (`breakdown`): the chosen one, else the locale's (`languages`); null: every bundle. */
  const scope = $derived(
    bundle ? new Set([bundle]) : locale ? new Set(bundles.filter((b) => b.languages.includes(locale)).map((b) => b.id)) : null,
  );
  /** Questions per source language (decision 235): es-sourced vs. en-sourced. */
  const bySource = $derived(
    Object.entries(
      questions.reduce<Record<string, number>>((n, q) => {
        const l = q.source?.locale ?? q.locale ?? "es";
        n[l] = (n[l] ?? 0) + 1;
        return n;
      }, {}),
    ),
  );
  let loading = $state(true);
  let error = $state<string | null>(null);

  onMount(async () => {
    if (page === "subcategories" && !locale && (!bundle || bundle === "base")) {
      // Only for the "next batch" marks (base's): the page works without it.
      fetchOverview().then((o) => (nextBatch = o.next_batch_subcategories), () => {});
    }
    if (bundle && (page === "difficulty" || page === "categories")) {
      // Optional too: the charts work without targets.
      fetchTargets().then((t) => (targets = (t[bundle] as BundleTargets | undefined) ?? null), () => {});
    }
    try {
      if (page === "media") {
        [mediaStats, bundles, names] = await Promise.all([
          fetchMediaStats(bundle, locale),
          fetchBundles(),
          locale ? fetchNames(locale) : null,
        ]);
        return;
      }
      [questions, categories, ageGroups, bundles, names] = await Promise.all([
        fetchQuestions(locale ? { locale, plays: "1", bundle } : { status: "approved", bundle }),
        fetchCategories(),
        fetchAgeGroups(),
        fetchBundles(),
        locale ? fetchNames(locale) : null,
      ]);
    } catch (e) {
      error = messageOf(e);
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
    {locale ? `The ${locale} pool: approved sources in ${locale}, playing translations` : "Approved sources, any language"} · bundles:
    <a href={href(path, null)} class:current={!bundle}>all</a>
    {#each bundles as b (b.id)}{" · "}<a href={href(path, b.id)} class:current={bundle === b.id}
        >{names?.bundles[b.id]?.name ?? b.name}</a
      >{/each}
    · language:
    <a href={href(path, bundle, null)} class:current={!locale}>sources</a>
    {#each LOCALES as l (l)}{" · "}<a href={href(path, bundle, l)} class:current={l === locale}>{l}</a>{/each}
    {#if bySource.length}· by source language: {bySource.map(([l, n]) => `${l} ${n}`).join(" · ")}{/if}
  </p>

  {#if loading}
    <p class="muted">Loading…</p>
  {:else if error}
    <p class="error">{error}</p>
  {:else if page === "categories"}
    <CategoryChart {questions} {categories} {targets} {bundle} {names} {locale} {scope} />
  {:else if page === "subcategories"}
    <SparseList {questions} {categories} {nextBatch} {names} {locale} {scope} />
    <SubcategoryTable {questions} {categories} {names} {locale} {scope} />
  {:else if page === "media"}
    {#if mediaStats}<MediaStats stats={mediaStats} />{/if}
  {:else if ageGroups}
    <DifficultyChart {questions} {ageGroups} {targets} {names} />
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
  .error {
    color: var(--bad);
  }
</style>
