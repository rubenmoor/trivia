<script lang="ts">
  // A seat's device glyph (decision 279): a pad, keyboard and mouse, or a keyboard-only player's claim key.
  import type { Binding } from "../lib/seats.ts";
  import Icon from "./Icon.svelte";

  let { binding }: { binding: Binding | null } = $props();
</script>

{#if binding !== null && typeof binding === "object" && "key" in binding}
  <kbd class="seat-key">{binding.key.toUpperCase()}</kbd>
{:else if binding !== null}
  <Icon name={typeof binding === "object" ? "gamepad" : "keyboard"} />
{/if}

<style>
  .seat-key {
    display: inline-grid;
    place-items: center;
    min-width: 1.5em;
    padding: 0 0.3em;
    border: 1px solid currentColor;
    border-radius: 0.3em;
    font-family: var(--font-display);
    font-weight: 800;
    line-height: 1.4;
  }
</style>
