<script lang="ts">
  // A key chip (plans/14-input.md, IN-5 and section 4; decision 671): the control's one fixed shortcut, the key with
  // keyboard or mouse, the pad button's glyph with a pad (from the pad map incl. the scopes' overrides); nothing if the
  // pad has no binding. A label, never a prediction: it reads no focus, ring or hover, so it can't change when the ring
  // moves. `confirm` (Enter/A) belongs on a scope's primary button only; ring + Space/X presses any control unlabelled.
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
    /** No glyph, space kept: the control is disabled right now. */
    off?: boolean;
    /** This device's prompt, not the last input's: the turn seat's (`seatDevice`, plan 163). */
    device?: { device: Device; style?: PadStyle } | null;
  } = $props();

  const pads = $derived((device?.device ?? lastDevice.current) === "gamepad");
  const style = $derived(device?.style ?? padStyle.current);

  const intent = (a: Named | Intent): Intent => (typeof a === "string" ? { type: a } : a);
  const key = $derived(keyLabel(intent(action)));
  const button = $derived.by(() => {
    void scopes.version;
    return padButton(intent(pad ?? action), padMap(BUTTONS));
  });
</script>

{#if !pads}
  {#if !padOnly && key}<kbd class:hold={off}>{key}</kbd>{/if}
{:else if button !== null}
  <kbd class="pad" class:hold={off}><Glyph {button} set={style} size="1.7em" /></kbd>
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
