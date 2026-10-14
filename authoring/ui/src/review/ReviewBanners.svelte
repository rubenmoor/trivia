<script lang="ts" module>
  import type { Decision } from "../lib/types.ts";

  /** Spot checks compare accept vs. not (plan 16). */
  export const accepts = (d: Decision) => d === "approved";
</script>

<script lang="ts">
  // Banners above the question: spot-check reveal, stale, doesn't travel, played data, previous review, audit.
  import type { AgeGroups, PlayedCell, Question, SpotCheckItem } from "../lib/types.ts";

  // blind: sample mode before the human's decision, nothing of the LLM review or audit (plan 16).
  let { current, spot, blind, ageGroups, onTravels }: {
    current: Question;
    spot: SpotCheckItem | undefined;
    blind: boolean;
    ageGroups: AgeGroups | null;
    onTravels: () => void;
  } = $props();

  /** «adultos 37 resp., 92 % bien, dificultad 11 → jugada ≤ 7» (plan 109). */
  const playedText = (c: PlayedCell) =>
    `${ageGroups?.groups.find((g) => g.id === c.group)?.name.toLowerCase() ?? c.group} ${c.n} resp., ` +
    `${Math.round((c.right / c.n) * 100)} % bien, dificultad ${c.rated}` +
    (c.observed === null ? "" : ` → jugada ${c.bound ? `${c.bound} ` : ""}${c.observed}`);
</script>

{#if spot}
  <div class="spot" class:disagree={accepts(spot.llm) !== accepts(spot.human)}>
    Spot check: you <b>{spot.human.replace("_", " ")}</b> · LLM review <b>{spot.llm.replace("_", " ")}</b> ·
    <b>{accepts(spot.llm) === accepts(spot.human) ? "agree" : "disagree"}</b>
    · audit: {spot.audit === "problem" ? "major finding" : spot.audit === "ok" ? "no major finding" : "not audited"}
    {#if spot.difficulty[0] !== spot.difficulty[1]}· difficulty {spot.difficulty[0]} → {spot.difficulty[1]}{/if}
    <span class="muted">· → next · u undo</span>
  </div>
{/if}

{#if current.stale}
  <div class="previous stale">
    Stale: the Spanish source changed since this translation. No approve; the next <code>--translate</code> run redoes it.
  </div>
{/if}
{#if current.translatable === false}
  <div class="previous rejected">
    The source doesn't travel (<code>translatable: false</code>); its translations are rejected.
    <button onclick={onTravels}>travels again</button>
  </div>
{/if}

{#if current.played.length && !blind}
  <div class="previous played">Datos de juego: {current.played.map(playedText).join(" · ")}</div>
{/if}

{#if current.review && !blind}
  <div class="previous {current.status}">
    {current.review.reviewer === "llm" ? `Reviewed by ${current.review.model}` : "Already reviewed"}:
    <b>{current.status.replace("_", " ")}</b> ({current.review.reviewed_on})
    {#if current.review.feedback}: “{current.review.feedback}”{/if}
    {#if current.review.previous}
      <span class="muted">· before: {current.review.previous.model}
        {current.review.previous.decision.replace("_", " ")}{#if current.review.previous.feedback}:
          “{current.review.previous.feedback}”{/if}</span>
    {/if}
  </div>
{/if}

{#if current.audit && !blind}
  <div class="previous audit" class:major={current.audit.verdict === "problem" && current.audit.severity === "major"}>
    Audit ({current.audit.model}): <b>{current.audit.verdict}</b>{#if current.audit.verdict === "problem"}
      , {current.audit.severity}: {current.audit.problems.join(", ") || "other"}{/if}
    · difficulty {current.audit.difficulty_estimate} · “{current.audit.notes}”
  </div>
{/if}

<style>
  .previous {
    margin-top: 1rem;
    padding: 0.5rem 0.8rem;
    border-radius: 8px;
    background: var(--panel);
    border-left: 4px solid var(--muted);
  }
  .previous.approved { border-color: var(--good); }
  .previous.rejected { border-color: var(--bad); }
  .previous.needs_work { border-color: var(--warn); }
  .previous.audit { border-color: var(--accent); }
  .previous.stale { border-color: var(--warn); }
  .previous.audit.major { border-color: var(--bad); }
  .spot {
    margin-top: 1rem;
    padding: 0.5rem 0.8rem;
    border-radius: 8px;
    background: var(--good-bg);
    border-left: 4px solid var(--good);
  }
  .spot.disagree {
    background: var(--bad-bg);
    border-color: var(--bad);
  }
  button {
    padding: 0.5rem 0.9rem;
    font: inherit;
    color: var(--text);
    background: var(--panel);
    border: 1px solid transparent;
    border-radius: 8px;
    cursor: pointer;
  }
</style>
