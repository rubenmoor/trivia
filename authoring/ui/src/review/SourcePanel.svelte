<script lang="ts">
  // Locale view (plan 67): the Spanish source (read-only) next to the translation, row by row.
  import type { Question } from "../lib/types";

  let { question }: { question: Question } = $props();

  const source = $derived(question.source!);
  const indexes = (a: string[], b: string[]) => [...Array(Math.max(a.length, b.length)).keys()];
</script>

<div class="side">
  <h2>Español · difficulty {source.difficulty} · {source.status.replace("_", " ")}</h2>
  <h2>{question.locale} · difficulty {question.difficulty} · {question.status.replace("_", " ")}</h2>

  <p class="description">{source.description}</p>
  <p class="description">{question.description}</p>

  <p class="question">{source.question}</p>
  <p class="question">{question.question}</p>

  <p class="option correct">{source.answer}</p>
  <p class="option correct">{question.answer}</p>

  {#each indexes(source.wrong_answers, question.wrong_answers) as i}
    <p class="option">{source.wrong_answers[i] ?? ""}</p>
    <p class="option">{question.wrong_answers[i] ?? ""}</p>
  {/each}

  <h2>Hints</h2>
  <h2>Hints</h2>
  {#each indexes(source.hints, question.hints) as i}
    <p>{source.hints[i] ? `${i + 1}. ${source.hints[i]}` : ""}</p>
    <p>{question.hints[i] ? `${i + 1}. ${question.hints[i]}` : ""}</p>
  {/each}

  <h2>Fun fact</h2>
  <h2>Fun fact</h2>
  <p>{source.fun_fact}</p>
  <p>{question.fun_fact}</p>
</div>

<style>
  .side {
    display: grid;
    grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
    gap: 0.5rem 2rem;
    margin-top: 1.5rem;
  }
  .side > :nth-child(odd) {
    color: var(--muted);
  }
  p {
    margin: 0;
  }
  h2 {
    margin: 1rem 0 0;
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--muted);
  }
  .description {
    font-style: italic;
    font-size: 1.2rem;
    color: var(--accent);
  }
  .question {
    font-size: 1.6rem;
    line-height: 1.25;
    font-weight: 700;
  }
  .option {
    padding: 0.5rem 0.9rem;
    border-radius: 10px;
    background: var(--panel);
    font-size: 1.15rem;
  }
  .option.correct {
    background: var(--good-bg);
    outline: 2px solid var(--good);
  }
</style>
