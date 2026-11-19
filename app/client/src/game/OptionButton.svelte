<script lang="ts">
  // The shared option button (task 2270; decision 518, decision 679): icon column | caption | more text | shortcut chip.
  // Bundles, modes, age groups, names, Join's open seat. A long caption wraps inside its column; the icon stays centred.
  // The chip is the button's one fixed shortcut (a `Prompt`), never focus-bound.
  import type { Snippet } from "svelte";
  import type { HTMLButtonAttributes } from "svelte/elements";

  let {
    icon,
    caption,
    chip,
    children,
    on = false,
    dim = false,
    compact = false,
    ...rest
  }: {
    /** The icon column: an `Icon`, a flag, a bundle mark. */
    icon?: Snippet;
    caption: string;
    /** The shortcut chip, last column. */
    chip?: Snippet;
    /** More text under the caption. */
    children?: Snippet;
    /** Selected: outline + tint (decision 314). */
    on?: boolean;
    /** Unselected looks muted (switches). */
    dim?: boolean;
    /** The small look of the Bundles screen. */
    compact?: boolean;
  } & HTMLButtonAttributes = $props();
</script>

<button {...rest} class={["option glass", rest.class]} class:on class:dim class:compact>
  {#if icon}<span class="icon-col">{@render icon()}</span>{/if}
  <span class="text">
    <span class="caption">{caption}</span>
    {@render children?.()}
  </span>
  {#if chip}<span class="chip-col">{@render chip()}</span>{/if}
</button>

<style>
  .option {
    display: flex;
    align-items: center;
    gap: calc(1 * var(--u));
    min-width: calc(20 * var(--u));
    max-width: calc(34 * var(--u));
    padding: calc(1 * var(--u)) calc(1.6 * var(--u));
    border-color: var(--slate-600);
    text-align: left;
    transition:
      transform 0.2s var(--spring),
      border-color 0.2s,
      opacity 0.2s;
    animation: arrive 0.5s calc(0.15s + var(--i, 0) * 0.05s) var(--spring) backwards;
  }
  .option:hover:not(:disabled) {
    transform: translateY(calc(-0.3 * var(--u)));
  }
  .option.on {
    border-color: var(--sky);
    background: rgba(76, 201, 240, 0.16);
    transform: translateY(calc(-0.3 * var(--u)));
  }
  .icon-col {
    flex: none;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: calc(3 * var(--u));
  }
  .text {
    flex: 1;
    min-width: 0;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
  }
  .chip-col {
    flex: none;
    display: flex;
    align-items: center;
  }
  .caption {
    font-family: var(--font-display);
    font-size: calc(2 * var(--u));
    font-weight: 800;
    line-height: 1.1;
    overflow-wrap: anywhere;
  }
  .dim:not(.on) .caption {
    color: var(--slate-400);
  }
  .compact {
    position: relative;
    min-width: 0;
    max-width: none;
    padding: calc(1 * var(--u)) calc(3.4 * var(--u)) calc(1 * var(--u)) calc(1.4 * var(--u));
  }
  .compact .icon-col {
    font-size: calc(2.85 * var(--u));
  }
  .compact .text {
    gap: calc(0.2 * var(--u));
  }
  .compact .caption {
    font-size: calc(1.9 * var(--u));
  }
  .compact.on {
    transform: none;
  }
  .compact:hover:not(:disabled) {
    border-color: var(--slate-400);
  }
  .compact.on:hover:not(:disabled) {
    border-color: var(--sky);
  }
</style>
