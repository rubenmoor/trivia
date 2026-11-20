<script lang="ts">
  // The fit view (plan 230): what `qgen batch --from base` kept, adapted and dropped, per base category and
  // subcategory; filters by verdict, reason, run; flips drop ↔ keep write fit.json (`by: developer`).
  import { onMount } from "svelte";
  import { messageOf } from "$app/lib/http.ts";
  import { fetchFit, flipFit } from "../lib/api.ts";
  import Nav from "../lib/Nav.svelte";
  import type { FitData, FitRow, FitText } from "../lib/types.ts";

  const bundle = new URLSearchParams(location.search).get("fit") || "chinese-base";
  const REASONS = ["euro_centric", "latam_centric", "wordplay", "sensitivity", "too_hard_here", "other"];

  let data = $state<FitData | null>(null);
  let error = $state<string | null>(null);
  let verdict = $state("");
  let reason = $state("");
  let run = $state("");
  let sample = $state(false);
  let busy = $state<string | null>(null);

  onMount(load);

  async function load() {
    try {
      data = await fetchFit(bundle);
    } catch (e) {
      error = messageOf(e);
    }
  }

  const sampled = $derived(new Set(run ? (data?.drop_sample[run] ?? []) : Object.values(data?.drop_sample ?? {}).flat()));
  const shown = $derived(
    (data?.rows ?? []).filter(
      (r) => (!verdict || r.verdict === verdict) && (!reason || r.reason === reason) && (!run || r.run === run) && (!sample || sampled.has(r.id)),
    ),
  );
  const counts = $derived.by(() => {
    const n = { keep: 0, adapt: 0, drop: 0 };
    for (const r of data?.rows ?? []) n[r.verdict]++;
    return n;
  });
  // [category, [subcategory, rows]]
  const groups = $derived.by(() => {
    const cats = new Map<string, Map<string, FitRow[]>>();
    for (const r of shown) {
      const subs = cats.get(r.category) ?? new Map<string, FitRow[]>();
      subs.set(r.subcategory, [...(subs.get(r.subcategory) ?? []), r]);
      cats.set(r.category, subs);
    }
    return [...cats].map(([c, subs]) => ({ c, subs: [...subs] }));
  });

  const tally = (rows: FitRow[]) => (["keep", "adapt", "drop"] as const).map((v) => `${v} ${rows.filter((r) => r.verdict === v).length}`).join(" · ");

  async function flip(r: FitRow, to: "keep" | "drop") {
    busy = r.id;
    error = null;
    try {
      await flipFit(bundle, r.id, to, to === "drop" ? "other" : undefined);
      await load();
    } catch (e) {
      error = messageOf(e);
    } finally {
      busy = null;
    }
  }

  const text = (t: FitText) => `${t.question} → ${t.answer}`;
</script>

<Nav current="review" />
<main>
  <h1>Fit pass: {bundle}</h1>
  <p class="muted small">
    Copies: <a href="/review?bundle={bundle}">/review?bundle={bundle}</a>. A flip drop → keep makes the next <code>qgen batch --bundle {bundle} --from base</code> copy it (no fit call); keep → drop rejects its copy now. Adapted copies change in their own review.
  </p>
  {#if error}<p class="error">{error}</p>{/if}
  {#if !data}
    {#if !error}<p class="muted">Loading…</p>{/if}
  {:else}
    <p class="counts">
      Judged {data.rows.length}: keep {counts.keep} · adapt {counts.adapt} · drop {counts.drop}; showing {shown.length}
    </p>
    <div class="filters">
      <label>Verdict
        <select bind:value={verdict}>
          <option value="">all</option>
          <option>keep</option><option>adapt</option><option>drop</option>
        </select>
      </label>
      <label>Reason
        <select bind:value={reason}>
          <option value="">all</option>
          {#each REASONS as r}<option>{r}</option>{/each}
        </select>
      </label>
      <label>Run
        <select bind:value={run}>
          <option value="">all</option>
          {#each data.runs as r}<option>{r}</option>{/each}
        </select>
      </label>
      <label><input type="checkbox" bind:checked={sample} /> drop sample ({Object.values(data.drop_sample)[0]?.length ?? 0} per run)</label>
      {#if run}
        <a href="/review?batch={run}&sample=1">spot-check sample of {run}</a>
      {/if}
    </div>
    {#each groups as g (g.c)}
      <h2>{g.c}</h2>
      {#each g.subs as [sub, rows] (sub)}
        <h3>{sub} <span class="muted small">{tally(rows)}</span></h3>
        <table>
          <tbody>
            {#each rows as r (r.id)}
              <tr class={r.verdict}>
                <td class="v"><b>{r.verdict}</b>{#if r.reason}<br />{r.reason}{/if}<br /><span class="muted small">{r.run}, {r.by}</span></td>
                <td>
                  <div>{r.id}: {text(r.source)} <span class="muted small">(level {r.source.difficulty})</span></div>
                  <div class="muted small">{r.note}</div>
                  {#if r.copy}
                    <div class="copy">
                      <a href="/review?id={r.copy.id}">{r.copy.id}</a> ({r.copy.status}): {text(r.copy)}
                      {#if r.verdict === "adapt"}
                        <div class="muted small">issue: {r.issue}</div>
                        <div class="muted small">wrong: {r.source.wrong_answers.join(" | ")} → {r.copy.wrong_answers.join(" | ")}</div>
                        <div class="muted small">hints: {r.source.hints.join(" | ")} → {r.copy.hints.join(" | ")}</div>
                      {/if}
                    </div>
                  {/if}
                </td>
                <td class="flip">
                  {#if r.by === "map" || r.by === "rule"}
                    <span class="muted small">by {r.by}</span>
                  {:else if r.verdict === "drop" && !r.copy}
                    <button disabled={busy === r.id} onclick={() => flip(r, "keep")}>→ keep</button>
                  {:else if r.verdict === "keep"}
                    <button disabled={busy === r.id} onclick={() => flip(r, "drop")}>→ drop</button>
                  {/if}
                </td>
              </tr>
            {/each}
          </tbody>
        </table>
      {/each}
    {/each}
  {/if}
</main>

<style>
  .filters {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem 1.25rem;
    align-items: center;
    margin-bottom: 1rem;
  }
  table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 0.75rem;
  }
  td {
    padding: 0.35rem 0.5rem;
    border-top: 1px solid var(--line);
    vertical-align: top;
  }
  td.v {
    white-space: nowrap;
    width: 9rem;
  }
  td.flip {
    width: 6rem;
  }
  tr.drop td.v b {
    color: var(--muted);
  }
  .copy {
    margin-top: 0.25rem;
    padding-left: 0.75rem;
    border-left: 3px solid var(--line);
  }
</style>
