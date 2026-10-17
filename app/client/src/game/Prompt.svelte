<script lang="ts">
  // A key prompt (plans/14-input.md, IN-5): the key with keyboard or mouse, the pad button's glyph
  // with a pad (from the pad map incl. the scopes' overrides); nothing if the pad has no binding.
  import { BUTTONS, padButton, type PadStyle } from "../lib/gamepad.ts";
  import { padStyle } from "../lib/gamepad.svelte.ts";
  import { keyLabel, lastDevice, padMap, scopes, type Device, type Intent } from "../lib/input.svelte.ts";
  import Glyph from "./Glyph.svelte";

  /** Intents without fields, named by their type. */
  type Bare<I> = I extends Intent ? (keyof I extends "type" ? I["type"] : never) : never;
  type Named = Bare<Intent>;

  let {
    action,
    pad,
    hold = false,
    padOnly = false,
    fixed = false,
    off = false,
    device = null,
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
    /** This device's prompt, not the last input's: the turn seat's (`seatDevice`, plan 163). */
    device?: { device: Device; style?: PadStyle } | null;
  } = $props();

  let chip = $state<HTMLElement>();
  const pads = $derived((device?.device ?? lastDevice.current) === "gamepad");
  const style = $derived(device?.style ?? padStyle.current);

  const intent = (a: Named | Intent): Intent => (typeof a === "string" ? { type: a } : a);
  const key = $derived(keyLabel(intent(action)));
  const button = $derived.by(() => {
    if (!pads) return null;
    void scopes.version;
    return padButton(intent(pad ?? action), padMap(BUTTONS));
  });
  // A presses the ringed control: on another button the A would mislead.
  const away = $derived.by(() => {
    if (off) return true;
    void scopes.version;
    const own = chip?.closest("button");
    if (fixed || intent(pad ?? action).type !== "confirm" || !own) return false;
    const ring = document.querySelector("[data-nav]");
    return ring !== null && ring !== own;
  });
</script>

{#if !pads}
  {#if !padOnly && key}<kbd>{key}</kbd>{/if}
{:else if button !== null}
  <kbd class="pad" class:hold={away} bind:this={chip}><Glyph {button} set={style} size="1.7em" /></kbd>
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
