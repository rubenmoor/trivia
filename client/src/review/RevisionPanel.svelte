<script lang="ts">
  // What `qgen.py revise` changed in a question, and why (plans/08-review-tool.md, RV-9).
  import type { Question } from "../lib/types";

  let { question }: { question: Question } = $props();

  const revision = $derived(question.revision!);
  const changes = $derived(Object.entries(revision.previous ?? {}));

  const LABELS: Record<string, string> = {
    difficulty: "Difficulty",
    description: "Description",
    question: "Question",
    answer: "Answer",
    wrong_answers: "Wrong answers",
    hints: "Hints",
    media: "Media",
    fun_fact: "Fun fact",
    needs_media: "Needs media",
    background: "Background",
  };

  function show(value: unknown): string {
    if (value === null || value === undefined) return "—";
    if (Array.isArray(value)) return value.join(" · ");
    if (typeof value === "object") {
      const m = value as Record<string, unknown>;
      return [m.type, m.role, m.query && `“${m.query}”`, m.note].filter(Boolean).join(" · ");
    }
    return String(value);
  }

  function current(field: string): unknown {
    return (question as unknown as Record<string, unknown>)[field];
  }
</script>

<section class="revision" class:drop={revision.action === "drop"}>
  {#if revision.action === "drop"}
    <h2>Proposed reject</h2>
    <p>{revision.reason}</p>
    <p class="muted"><kbd>r</kbd> confirms · <kbd>a</kbd> or <kbd>f</kbd> overrules</p>
  {:else}
    <h2>Revised ({revision.revised_on})</h2>
    <p>{revision.reason}</p>
    {#if changes.length}
      <table>
        <tbody>
          {#each changes as [field, old]}
            <tr>
              <th>{LABELS[field] ?? field}</th>
              <td class="old">{show(old)}</td>
              <td class="arrow">→</td>
              <td class="new">{show(current(field))}</td>
            </tr>
          {/each}
        </tbody>
      </table>
    {/if}
  {/if}
</section>

<style>
  .revision {
    margin-top: 1rem;
    padding: 0.8rem 1rem;
    border-radius: 10px;
    background: var(--panel);
    border-left: 4px solid var(--accent);
  }
  .revision.drop {
    border-color: var(--bad);
  }
  h2 {
    margin: 0 0 0.3rem;
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--accent);
  }
  .drop h2 {
    color: var(--bad);
  }
  p {
    margin: 0.2rem 0;
  }
  table {
    width: 100%;
    margin-top: 0.5rem;
    border-collapse: collapse;
    font-size: 0.9rem;
  }
  th {
    width: 8rem;
    padding: 0.3rem 0.5rem 0.3rem 0;
    text-align: left;
    vertical-align: top;
    color: var(--muted);
    font-weight: 600;
  }
  td {
    padding: 0.3rem 0.4rem;
    vertical-align: top;
  }
  .old {
    width: 45%;
    color: var(--muted);
    text-decoration: line-through;
    text-decoration-color: rgb(255 107 107 / 0.6);
  }
  .arrow {
    color: var(--muted);
  }
  .new {
    width: 45%;
    color: var(--good);
  }
  .muted {
    color: var(--muted);
  }
  kbd {
    padding: 0 0.35rem;
    font-family: inherit;
    font-weight: 700;
    border: 1px solid var(--muted);
    border-radius: 4px;
  }
</style>
