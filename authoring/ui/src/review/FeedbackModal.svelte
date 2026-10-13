<script lang="ts">
  // "f": feedback text and problem kinds for a "needs work" decision.
  import { onMount } from "svelte";
  import Modal from "./Modal.svelte";

  let { id, question, kinds, text = $bindable(), problems = $bindable(), onclose }: {
    id: string;
    question: string;
    /** Problem kinds (qgen.py PROBLEMS). */
    kinds: string[];
    text: string;
    problems: string[];
    onclose: () => void;
  } = $props();

  let box = $state<HTMLTextAreaElement>();
  onMount(() => box?.focus());

  function toggle(kind: string) {
    problems = problems.includes(kind) ? problems.filter((k) => k !== kind) : [...problems, kind];
  }
</script>

<Modal
  title={`Feedback · ${id} needs work`}
  {question}
  hint="Enter: save and next · Shift+Enter: new line · Esc: cancel"
  warn
  {onclose}
>
  <textarea
    bind:this={box}
    bind:value={text}
    rows="4"
    placeholder="What should change? (e.g. too difficult, bad image, a wrong answer is also right…)"
  ></textarea>
  {#if kinds.length}
    <div class="kinds">
      {#each kinds as kind}
        <button class:on={problems.includes(kind)} onclick={() => toggle(kind)}>{kind}</button>
      {/each}
    </div>
  {/if}
</Modal>

<style>
  textarea {
    width: 100%;
    padding: 0.8rem;
    font: inherit;
    font-size: 1.1rem;
    color: var(--text);
    background: var(--panel);
    border: 2px solid var(--warn);
    border-radius: 8px;
  }
  .kinds {
    display: flex;
    flex-wrap: wrap;
    gap: 0.4rem;
    margin-top: 0.6rem;
  }
  button {
    padding: 0.2rem 0.6rem;
    font: inherit;
    font-size: 0.9rem;
    color: var(--text);
    background: var(--panel);
    border: 1px solid transparent;
    border-radius: 8px;
    cursor: pointer;
  }
  button.on {
    border-color: var(--warn);
    color: var(--warn);
  }
</style>
