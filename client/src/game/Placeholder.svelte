<script lang="ts">
  // A visible stand-in for an unpolished part of the game (D-25). Every use names the task
  // that replaces it; `grep -rn PLACEHOLDER client/src` lists them all.
  import type { Snippet } from "svelte";

  let { task, label, chip = false, children }: { task: string; label: string; chip?: boolean; children?: Snippet } =
    $props();
</script>

<div class="placeholder" class:chip>
  <span class="tag">PLACEHOLDER · {task}</span>
  <span class="label">{label}</span>
  {@render children?.()}
</div>

<style>
  .placeholder {
    border: 0.15rem dashed #ff7ad9;
    border-radius: 0.6rem;
    padding: 0.6rem 1rem;
    color: #ffb8ec;
    background: rgba(60, 10, 50, 0.55);
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 0.3rem;
  }
  .chip {
    display: inline-flex;
    flex-direction: row;
    padding: 0.2rem 0.6rem;
    font-size: 0.8rem;
  }
  .tag {
    font-family: ui-monospace, monospace;
    font-size: 0.8rem;
    letter-spacing: 0.05em;
    opacity: 0.85;
  }
  .label {
    font-size: 1rem;
  }
</style>
