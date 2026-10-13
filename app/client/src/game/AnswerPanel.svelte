<script lang="ts">
  // The right answer and its fun fact, in the question's language: Correct, Wrong, Victory.
  import { questionLocale } from "../lib/names.svelte.ts";
  import type { Game } from "../lib/types.ts";
  import Icon from "./Icon.svelte";

  let { last, label }: { last: NonNullable<Game["last"]>; label?: string } = $props();
</script>

<div class="panel glass">
  {#if label}<p class="label">{label}</p>{/if}
  <p class="answer" lang={questionLocale()}><span class="badge good-badge"><Icon name="check" /></span>{last.answer}</p>
  <p class="fun-fact" lang={questionLocale()}>{last.fun_fact}</p>
</div>

<style>
  p {
    margin: 0;
  }
  .panel {
    max-width: calc(64 * var(--u));
    padding: calc(1.4 * var(--u)) calc(2.4 * var(--u));
    display: flex;
    flex-direction: column;
    gap: calc(0.6 * var(--u));
    animation: arrive 0.6s 0.25s var(--spring) backwards;
  }
  .answer {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: calc(0.8 * var(--u));
    font-family: var(--font-display);
    font-size: calc(2.6 * var(--u));
    font-weight: 800;
  }
  .good-badge {
    display: grid;
    place-items: center;
    width: calc(2.6 * var(--u));
    height: calc(2.6 * var(--u));
    border-radius: 50%;
    background: var(--mint);
    color: var(--night-900);
    font-size: calc(1.6 * var(--u));
  }
  .fun-fact {
    font-size: calc(1.5 * var(--u));
    color: var(--slate-200);
  }
</style>
