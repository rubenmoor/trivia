<script lang="ts">
  // Top line of the review page: progress, counts, the question's meta, links and locales.
  import type { Bundle, Names, Question } from "../lib/types";
  import { LOCALES } from "$app/lib/data";
  import { localeHref } from "./url";

  let { current, index, total, singleId, locale, downloads, spotCount, agreed, counts, names, bundles, difficultyInput }: {
    current: Question;
    index: number;
    total: number;
    singleId: string | null;
    locale: string | null;
    /** Media downloads running in the background. */
    downloads: number;
    /** Sample mode: spot checks decided (null otherwise). */
    spotCount: number | null;
    agreed: number;
    counts: { approved: number; rejected: number; needs_work: number; open: number; llm: number };
    names: Names | null;
    bundles: Bundle[];
    /** After "d": the digits typed so far; null = not typing. */
    difficultyInput: string | null;
  } = $props();
</script>

<header>
  {#if singleId}
    <span class="progress">Single question</span>
  {:else}
    <span class="progress">{index + 1} / {total}</span>
  {/if}
  {#if locale}<span class="locale">{locale}</span>{/if}
  {#if downloads}<span class="downloads">⬇ downloading media… ({downloads})</span>{/if}
  {#if spotCount !== null}
    <span class="counts">spot check: {spotCount} decided · agree {agreed}</span>
  {:else if !singleId}
    <span class="counts">
      ✓ {counts.approved} · ✎ {counts.needs_work} · ✗ {counts.rejected} · open {counts.open}{#if counts.llm}
        (LLM-reviewed {counts.llm}){/if}
    </span>
  {/if}
  <span class="meta">
    {current.id} ·
    {#if names?.subcategories[current.subcategory]}{names.subcategories[current.subcategory]}
      <span class="key">({current.subcategory})</span>{:else}{current.subcategory}{/if} ·
    <span class:pending={difficultyInput !== null}
      >difficulty {difficultyInput !== null ? `${difficultyInput}▏ (Enter)` : current.difficulty}</span
    >
    {#if current.difficulty_original != null && current.difficulty_original !== current.difficulty}
      (was {current.difficulty_original})
    {/if}
    {#if current.style}· {current.style.split(":")[0]}{/if}
    · <span class="bundle" class:other={current.bundle !== "base"}
      >{names?.bundles[current.bundle]?.name ?? bundles.find((b) => b.id === current.bundle)?.name ?? current.bundle}</span
    >{#if names}&nbsp;<span class="key">({current.bundle})</span>{/if}
  </span>
  <span><a class="stats" href="/">Start</a> · <a class="stats" href="/stats/categories">Stats</a> ·
    {#each LOCALES as l, k}{#if k}&nbsp;·&nbsp;{/if}{#if l === (locale ?? "es")}<b>{l}</b>{:else}<a class="stats" href={localeHref(l)}>{l}</a
      >{/if}{/each}</span>
</header>

<style>
  header {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 0.5rem 1.5rem;
    font-size: 0.95rem;
    color: var(--muted);
  }
  .pending {
    color: var(--accent);
    font-weight: 700;
  }
  .downloads {
    color: var(--accent);
  }
  .progress {
    color: var(--text);
    font-weight: 700;
  }
  .meta {
    margin-left: auto;
  }
  .stats {
    color: var(--muted);
  }
  .locale {
    color: var(--accent);
    font-weight: 700;
    text-transform: uppercase;
  }
  .key {
    color: var(--muted);
    font-size: 0.85em;
  }
  .bundle.other {
    font-weight: 600;
    color: var(--accent);
  }
</style>
