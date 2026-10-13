<script lang="ts">
  // Dialog of the review page; its keys (Enter, Esc) stay in Review.svelte's one window listener.
  import type { Snippet } from "svelte";

  let { title, question, hint, warn = false, onclose, children }: {
    title: string;
    question: string;
    hint: string;
    warn?: boolean;
    onclose: () => void;
    children: Snippet;
  } = $props();
</script>

<!-- svelte-ignore a11y_click_events_have_key_events, a11y_no_static_element_interactions -->
<div class="backdrop" onclick={onclose}>
  <div class="modal" class:warn role="dialog" tabindex="-1" aria-modal="true" aria-labelledby="modal-title" onclick={(e) => e.stopPropagation()}>
    <h2 id="modal-title">{title}</h2>
    <p class="muted">{question}</p>
    {@render children()}
    <p class="muted">{hint}</p>
  </div>
</div>

<style>
  .backdrop {
    position: fixed;
    inset: 0;
    z-index: 10;
    display: grid;
    place-items: center;
    padding: 1rem;
    background: rgb(0 0 0 / 0.6);
  }
  .modal {
    width: min(640px, 100%);
    padding: 1.5rem;
    border-radius: 12px;
    background: var(--bg);
    border: 1px solid var(--accent);
    box-shadow: 0 20px 60px rgb(0 0 0 / 0.5);
  }
  .modal.warn {
    border-color: var(--warn);
  }
  h2 {
    margin: 0 0 0.4rem;
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--muted);
  }
</style>
