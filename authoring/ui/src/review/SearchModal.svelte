<script lang="ts">
  // "m": a new search term for the media or background slot.
  import { onMount } from "svelte";
  import Modal from "./Modal.svelte";

  let { title, question, licenceMode, value = $bindable(), onclose }: {
    title: string;
    question: string;
    licenceMode: boolean;
    value: string;
    onclose: () => void;
  } = $props();

  let box = $state<HTMLInputElement>();
  onMount(() => box?.select());
</script>

<Modal {title} {question} hint="Enter: search · Esc: cancel · 2–4 concrete words work best" {onclose}>
  <input
    bind:this={box}
    bind:value
    placeholder={licenceMode
      ? "Search term (English works best; every source, for a licence replacement)"
      : "Search term (English works best; Commons first, then the other sources)"}
  />
</Modal>

<style>
  input {
    width: 100%;
    padding: 0.8rem;
    font: inherit;
    font-size: 1.2rem;
    color: var(--text);
    background: var(--panel);
    border: 2px solid var(--accent);
    border-radius: 8px;
  }
</style>
