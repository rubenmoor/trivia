<script lang="ts">
  // A key prompt (plans/14-input.md, IN-5): the key with keyboard or mouse, the pad button's glyph
  // with a pad (from the pad map incl. the scopes' overrides); nothing if the pad has no binding.
  import { BUTTONS, padButton } from "../lib/gamepad";
  import { padStyle } from "../lib/gamepad.svelte";
  import { keyLabel, lastDevice, padMap, scopes, type Intent } from "../lib/input.svelte";
  import Glyph from "./Glyph.svelte";

  type Named = "confirm" | "back" | "menu" | "replay" | "flag" | "new" | "submit";

  let {
    action,
    pad,
    hold = false,
    padOnly = false,
    fixed = false,
    off = false,
  }: {
    action: Named | Intent;
    /** The pad's action where it differs (cancel: Esc on the keyboard, B on the pad). */
    pad?: Named | Intent;
    /** Keep the key's space when the pad has no binding. */
    hold?: boolean;
    /** Nothing with keyboard or mouse (the answer tiles' letters are the keys). */
    padOnly?: boolean;
    /** A on this button even while another control has the ring (the armed joker's bubble). */
    fixed?: boolean;
    /** No glyph, space kept: the pad button does nothing right now. */
    off?: boolean;
  } = $props();

  let chip = $state<HTMLElement>();

  const intent = (a: Named | Intent) => (typeof a === "string" ? { type: a } : a) as Intent;
  const key = $derived(keyLabel(intent(action)));
  const button = $derived.by(() => {
    if (lastDevice.current !== "gamepad") return null;
    void scopes.version;
    return padButton(intent(pad ?? action), padMap(BUTTONS));
  });
  // A presses the ringed control: on another button the A would mislead.
  const away = $derived.by(() => {
    void scopes.version;
    const own = chip?.closest("button");
    if (off) return true;
    if (fixed || intent(pad ?? action).type !== "confirm" || !own) return false;
    const ring = document.querySelector("[data-nav]");
    return ring !== null && ring !== own;
  });
</script>

{#if lastDevice.current !== "gamepad"}
  {#if !padOnly && key}<kbd>{key}</kbd>{/if}
{:else if button !== null}
  <kbd class="pad" class:hold={away} bind:this={chip}><Glyph {button} set={padStyle.current} size="1.7em" /></kbd>
{:else if hold && key}
  <kbd class="hold" aria-hidden="true">{key}</kbd>
{/if}

<style>
  .pad {
    padding: 0;
    border-color: transparent;
  }
  /* Bigger than the chip's text, same line box: no layout shift. */
  .pad :global(.glyph) {
    display: block;
    margin: -0.15em auto;
  }
  .hold {
    visibility: hidden;
  }
</style>
