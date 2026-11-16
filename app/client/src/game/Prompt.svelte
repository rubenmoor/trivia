<script lang="ts">
  // A key prompt (plans/14-input.md, IN-5): the key with keyboard or mouse, the pad button's glyph
  // with a pad (from the pad map incl. the scopes' overrides); nothing if the pad has no binding.
  // A confirm chip inside a button says how that button is activated right now (section 4, task 2119): Enter/A on the
  // scope's primary; on another button Space/X while it has the ring, else nothing (space kept); on a list screen
  // Enter/A on the ringed button, or on every one while nothing is ringed.
  import { BUTTONS, padButton, type PadStyle } from "../lib/gamepad.ts";
  import { padStyle } from "../lib/gamepad.svelte.ts";
  import { keyLabel, lastDevice, padMap, primaryControl, scopes, type Device, type Intent } from "../lib/input.svelte.ts";
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
    /** Confirm on this button even while another control has the ring (the armed joker's bubble). */
    fixed?: boolean;
    /** No glyph, space kept: the button does nothing right now. */
    off?: boolean;
    /** This device's prompt, not the last input's: the turn seat's (`seatDevice`, plan 163). */
    device?: { device: Device; style?: PadStyle } | null;
  } = $props();

  let chip = $state<HTMLElement>();
  const pads = $derived((device?.device ?? lastDevice.current) === "gamepad");
  const style = $derived(device?.style ?? padStyle.current);

  const intent = (a: Named | Intent): Intent => (typeof a === "string" ? { type: a } : a);
  /** The ring, else (keys only: Enter clicks it natively) the focused button. */
  function ringed(): Element | null {
    const ring = document.querySelector("[data-nav]");
    if (ring || pads) return ring;
    return document.activeElement instanceof HTMLButtonElement ? document.activeElement : null;
  }
  /** What this chip stands for: the intent as given, `press` for a ringed non-primary button, null for nothing right now. */
  const shown = $derived.by((): Intent | null => {
    if (off) return null;
    void scopes.version;
    const own = chip?.closest("button");
    const a = intent(action);
    if (fixed || a.type !== "confirm" || !own) return a;
    const primary = primaryControl();
    const ring = ringed();
    if (primary) return primary === own ? a : ring === own ? { type: "press" } : null;
    return ring === null || ring === own ? a : null;
  });
  const key = $derived(keyLabel(shown ?? intent(action)));
  const button = $derived.by(() => {
    void scopes.version;
    return padButton(shown ?? intent(pad ?? action), padMap(BUTTONS));
  });
  const away = $derived(shown === null);
</script>

{#if !pads}
  {#if !padOnly && key}<kbd class:hold={away} bind:this={chip}>{key}</kbd>{/if}
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
