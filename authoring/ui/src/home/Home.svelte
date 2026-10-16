<script lang="ts">
  // Start page of the authoring tool (plans/08-review-tool.md, "Start page", RV-14): what waits
  // for the developer, the batches, game readiness and the approved pool at a glance. Read-only:
  // every number links to the page or review queue that works it off.
  import { onMount } from "svelte";
  import { messageOf } from "$app/lib/http.ts";
  import { fetchAgeGroups, fetchCategories, fetchNames, fetchOverview, fetchQuestions } from "../lib/api.ts";
  import Nav from "../lib/Nav.svelte";
  import type { AgeGroups, Category, Names, Overview, Question } from "../lib/types.ts";
  import CategoryChart from "../stats/CategoryChart.svelte";
  import DifficultyChart from "../stats/DifficultyChart.svelte";
  import SparseList from "../stats/SparseList.svelte";

  let overview = $state<Overview | null>(null);
  let approved = $state<Question[]>([]);
  let categories = $state<Category[]>([]);
  let ageGroups = $state<AgeGroups | null>(null);
  let names = $state<Names | null>(null);
  let error = $state<string | null>(null);
  let goId = $state("");

  onMount(async () => {
    try {
      [overview, approved, categories, ageGroups, names] = await Promise.all([
        fetchOverview(),
        fetchQuestions({ status: "approved" }),
        fetchCategories(),
        fetchAgeGroups(),
        fetchNames(),
      ]);
    } catch (e) {
      error = messageOf(e);
    }
  });

  const review = (filter: Record<string, string>) => `/review?${new URLSearchParams(filter)}`;
  const plural = (n: number, one: string, many: string) => `${n} ${n === 1 ? one : many}`;

  interface Task {
    count: number;
    text: string;
    href?: string;
    /** A command to run instead of a page to open. */
    command?: string;
  }

  /** Section 1, in order of urgency; a queue with nothing in it is left out. */
  const tasks = $derived.by((): Task[] => {
    if (!overview) return [];
    const q = overview.queues;
    const out: Task[] = [
      ...overview.unfinished_runs.map((run) => {
        const locale = /^tr-(.+)-\d+$/.exec(run)?.[1];
        return locale
          ? { count: 1, text: `unfinished translation run ${run}: resume it with`, command: `qgen batch --translate ${locale}` }
          : { count: 1, text: `unfinished batch ${run}: resume it with`, command: "qgen batch" };
      }),
      {
        count: q.needs_work,
        text: `${q.needs_work === 1 ? "question needs" : "questions need"} work: approve, reject or give new feedback`,
        href: review({ status: "needs_work" }),
      },
      { count: q.drafts, text: `${q.drafts === 1 ? "draft" : "drafts"} nobody has reviewed`, href: review({ status: "draft" }) },
      {
        count: q.approved_without_media,
        text: `approved ${q.approved_without_media === 1 ? "question" : "questions"} without picked media`,
        href: review({ status: "approved", media: "missing" }),
      },
      {
        count: q.licence_replace,
        text: `${q.licence_replace === 1 ? "question" : "questions"} with a licence to replace: pick new media files`,
        href: review({ licence: "replace" }),
      },
      ...q.bundles.map((b) => ({
        count: b.unreviewed,
        text: `of ${b.questions} questions in the bundle ${b.name} without a human review: check they belong there`,
        href: review({ bundle: b.id }),
      })),
      {
        count: q.not_cached,
        text: `picked media ${q.not_cached === 1 ? "file" : "files"} not in the cache yet: run`,
        command: "trivia-media sync --status approved",
      },
    ];
    return out.filter((t) => t.count > 0);
  });

  const llmBatches = $derived(overview?.batches.filter((b) => !b.locale && b.llm_approved > 0) ?? []);

  /** "123", "q-123" or "q-0123" → "q-0123". */
  function questionId(input: string): string | null {
    const m = input.trim().match(/^(?:q-?)?(\d+)$/i);
    return m ? `q-${m[1].padStart(4, "0")}` : null;
  }
  function go(e: SubmitEvent) {
    e.preventDefault();
    const id = questionId(goId);
    if (id) location.href = `/review/${id}`;
  }
</script>

<svelte:head><title>Trivia authoring</title></svelte:head>

<main>
  <Nav current="start" />
  <h1>Trivia authoring</h1>

  {#if error}
    <p class="error">{error}</p>
  {:else if !overview}
    <p class="muted">Loading…</p>
  {:else}
    <section class="panel">
      <h2>Waiting for you</h2>
      {#if tasks.length}
        <ul class="tasks">
          {#each tasks as t}
            <li>
              <b class="count">{t.count}</b>
              {#if t.href}
                <a href={t.href}>{t.text} →</a>
              {:else}
                <span>{t.text} <code>{t.command}</code></span>
              {/if}
            </li>
          {/each}
        </ul>
      {:else}
        <p class="muted">Nothing. Every question has a decision and its media.</p>
      {/if}
    </section>

    {#if overview.llm_approved}
      <section class="panel">
        <h2>Check the LLM's approvals <span class="muted small">optional (D-42)</span></h2>
        <p>
          <a href={review({ status: "approved", reviewer: "llm" })}
            >{plural(overview.llm_approved, "approved question", "approved questions")} only an LLM has reviewed →</a
          >
        </p>
        <p class="per-batch">
          {#each llmBatches as b, i (b.name)}{i ? " · " : ""}<a href={review({ batch: b.name, status: "approved", reviewer: "llm" })}
              >{b.name} ({b.llm_approved})</a
            >{/each}
        </p>
      </section>
    {/if}

    <section class="panel">
      <h2>Batches</h2>
      <div class="scroll">
        <table>
          <thead>
            <tr>
              <th>Batch</th>
              <th title="source language of its questions">From</th>
              <th>Last review</th>
              <th class="num">Merged</th>
              <th class="num">Approved</th>
              <th class="num">Needs work</th>
              <th class="num">Rejected</th>
              <th class="num">Draft</th>
              <th class="num">By you</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {#each overview.batches as b (b.name)}
              <tr>
                <td>
                  <a href={review(b.locale ? { batch: b.name, locale: b.locale } : { batch: b.name })}
                    >{b.name === "none" ? "(no batch)" : b.name}</a
                  >
                  {#if b.locale}<a class="muted small" href={review({ batch: b.name, locale: b.locale, sample: "1" })}>sample</a>{/if}
                </td>
                <td class="muted">{b.sources.join(", ")}</td>
                <td class="muted">{b.date ?? "–"}</td>
                <td class="num">{b.merged}</td>
                <td class="num">{b.approved}</td>
                <td class="num" class:warn={b.needs_work > 0}>{b.needs_work}</td>
                <td class="num">{b.rejected}</td>
                <td class="num" class:warn={b.draft > 0}>{b.draft}</td>
                <td class="num">{Math.round((b.human / b.merged) * 100)} %</td>
                <td>{#if b.report}<a href={b.report}>report</a>{/if}</td>
              </tr>
            {/each}
          </tbody>
        </table>
      </div>
    </section>

    {#if overview.locales.length}
      <section class="panel">
        <h2>Question locales</h2>
        <p class="muted small">
          Per locale its pool: approved sources written in it, then its translations by status (approved: per source
          language); stale: the source text changed since. Approved sources in other languages not translatable or
          without a translation yet.
        </p>
        <div class="scroll">
          <table>
            <thead>
              <tr>
                <th>Locale</th>
                <th class="num">Own sources</th>
                <th class="num">Approved</th>
                <th class="num">Needs work</th>
                <th class="num">Draft</th>
                <th class="num">Rejected</th>
                <th class="num">Stale</th>
                <th class="num">Not translatable</th>
                <th class="num">Untranslated</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {#each overview.locales as l (l.locale)}
                <tr>
                  <td><a href={review({ locale: l.locale })}>{l.locale}</a></td>
                  <td class="num">{l.own}</td>
                  <td class="num"><a href={review({ locale: l.locale, status: "approved" })}>{l.approved}</a>
                    {#if l.approved}<span class="muted small"
                        >({Object.entries(l.from).map(([s, n]) => `${s} ${n}`).join(" · ")})</span
                      >{/if}</td
                  >
                  <td class="num" class:warn={l.needs_work > 0}
                    ><a href={review({ locale: l.locale, status: "needs_work" })}>{l.needs_work}</a></td
                  >
                  <td class="num" class:warn={l.draft > 0}><a href={review({ locale: l.locale, status: "draft" })}>{l.draft}</a></td>
                  <td class="num"><a href={review({ locale: l.locale, status: "rejected" })}>{l.rejected}</a></td>
                  <td class="num" class:warn={l.stale > 0}><a href={review({ locale: l.locale, stale: "1" })}>{l.stale}</a></td>
                  <td class="num">{l.not_translatable}</td>
                  <td class="num">{l.untranslated}</td>
                  <td><a href="/stats/difficulty?{new URLSearchParams({ locale: l.locale })}">stats</a></td>
                </tr>
              {/each}
            </tbody>
          </table>
        </div>
      </section>
    {/if}

    <section class="panel">
      <h2>Game readiness</h2>
      <p class="muted small">
        Candidates per game level in the default game: young teens, bundle {overview.supply.bundles.join(', ')} (approved, not blocked); a game needs {overview.per_level} per level (D-22).
        "unseen": questions this save never saw; once they run out, games repeat the least-seen ones (plan 65). Red: the
        level can't be filled.
      </p>
      <p class="small">
        Unseen approved: {overview.supply.unseen} (seen once: {overview.supply.seen_once}, twice+:
        {overview.supply.seen_twice}); blocked: {overview.supply.blocked}
      </p>
      <div class="scroll">
        <table class="supply">
          <thead>
            <tr>
              <th>Seen</th>
              {#each overview.supply.rows[0].levels as l (l.level)}
                <th class="num" title="difficulty {l.range[0]}–{l.range[1]}">{l.level}</th>
              {/each}
            </tr>
          </thead>
          <tbody>
            {#each overview.supply.rows as s (s.label)}
              <tr>
                <td>{s.label}</td>
                {#each s.levels as l (l.level)}
                  <td class="num" class:bad={l.missing > 0} title="difficulty {l.range[0]}–{l.range[1]}{l.missing ? `, ${l.missing} missing` : ''}">
                    {l.candidates}
                  </td>
                {/each}
              </tr>
            {/each}
          </tbody>
        </table>
      </div>
    </section>

    <section class="stats">
      <h2>Approved questions <a class="small" href="/stats/categories">all statistics →</a></h2>
      <div class="two">
        {#if ageGroups}
          <div>
            <DifficultyChart questions={approved} {ageGroups} compact />
            <a class="more" href="/stats/difficulty">difficulty →</a>
          </div>
        {/if}
        <div>
          <SparseList questions={approved} {categories} nextBatch={overview.next_batch_subcategories} {names} compact />
          <a class="more" href="/stats/subcategories">subcategories →</a>
        </div>
      </div>
      <CategoryChart questions={approved} {categories} {names} compact />
      <a class="more" href="/stats/categories">categories →</a>
    </section>

    <section class="panel">
      <h2>Go to</h2>
      <form onsubmit={go}>
        <label>
          Question
          <input bind:value={goId} placeholder="q-0123 or 123" size="14" />
        </label>
        <button disabled={!questionId(goId)}>Open</button>
      </form>
      <p class="links">
        <a href="/stats/categories">Categories</a> · <a href="/stats/subcategories">Subcategories</a> ·
        <a href="/stats/difficulty">Difficulty</a> · <a href="/review">Whole pool in the review tool</a> ·
        <a href="/comodines">Joker cards to print</a> · <a href="/gallery">Screen gallery (UI wording)</a>
      </p>
      <p class="muted small">
        Pool:
        {#each Object.entries(overview.counts.status) as [k, n], i}{i ? " · " : ""}{n} {k.replace("_", " ")}{/each}.
        Approved per bundle:
        {#each Object.entries(overview.counts.bundle) as [k, n], i}{i ? " · " : ""}{n} {k}{/each}.
      </p>
    </section>
  {/if}
</main>

<style>
  main {
    max-width: 1000px;
    margin: 0 auto;
    padding: 1.5rem 1rem 4rem;
  }
  h1 {
    margin: 0 0 1.25rem;
    font-size: 1.5rem;
  }
  h2 {
    margin: 0 0 0.6rem;
    font-size: 1.05rem;
  }
  .panel {
    background: var(--panel);
    border-radius: 12px;
    padding: 1.1rem 1.25rem;
    margin-bottom: 1.5rem;
  }
  .panel p {
    margin: 0.3rem 0;
  }
  a {
    color: var(--text);
  }
  a:hover {
    color: var(--accent);
  }
  .small {
    font-size: 0.85rem;
    font-weight: 400;
  }
  .error,
  .bad {
    color: var(--bad);
  }
  .warn {
    color: var(--warn);
  }
  .tasks {
    list-style: none;
    margin: 0;
    padding: 0;
  }
  .tasks li {
    display: flex;
    gap: 0.75rem;
    align-items: baseline;
    padding: 0.3rem 0;
  }
  .count {
    min-width: 2.5rem;
    text-align: right;
    font-size: 1.15rem;
    font-variant-numeric: tabular-nums;
    color: var(--accent);
  }
  code {
    padding: 0.05rem 0.3rem;
    border-radius: 4px;
    background: var(--field);
    font-size: 0.85em;
  }
  .per-batch {
    font-size: 0.9rem;
  }
  .per-batch a {
    color: var(--muted);
  }
  .scroll {
    overflow-x: auto;
  }
  table {
    border-collapse: collapse;
    width: 100%;
    font-size: 0.9rem;
  }
  th,
  td {
    text-align: left;
    padding: 0.25rem 0.75rem 0.25rem 0;
    border-bottom: 1px solid var(--line);
    white-space: nowrap;
  }
  th {
    color: var(--muted);
    font-weight: 600;
  }
  .num {
    text-align: right;
    font-variant-numeric: tabular-nums;
  }
  .supply td.num,
  .supply th.num {
    padding-right: 0.5rem;
  }
  .stats {
    margin-bottom: 1.5rem;
  }
  .stats > h2 {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
  }
  .stats a.small {
    color: var(--muted);
  }
  .two {
    display: grid;
    grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
    gap: 1.5rem;
    margin-bottom: 1.5rem;
  }
  @media (max-width: 760px) {
    .two {
      grid-template-columns: 1fr;
    }
  }
  .more {
    display: block;
    margin-top: 0.4rem;
    text-align: right;
    font-size: 0.85rem;
    color: var(--muted);
  }
  form {
    display: flex;
    gap: 0.5rem;
    align-items: center;
    margin-bottom: 0.5rem;
  }
  input {
    margin-left: 0.4rem;
    padding: 0.3rem 0.5rem;
    border: 1px solid var(--border);
    border-radius: 6px;
    background: var(--field);
    color: var(--text);
    font: inherit;
  }
  button {
    padding: 0.3rem 0.8rem;
    border: 0;
    border-radius: 6px;
    background: var(--accent);
    color: #1a1b22;
    font: inherit;
    font-weight: 600;
    cursor: pointer;
  }
  button:disabled {
    opacity: 0.4;
    cursor: default;
  }
  .links {
    font-size: 0.9rem;
  }
</style>
