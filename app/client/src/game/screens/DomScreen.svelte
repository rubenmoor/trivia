<script lang="ts">
  // A mod's plain-DOM screen or layer (plan 117): `render(el, props)` draws, its return cleans up.
  // A layer (`onclose`) is modal with its own input scope: Esc and pad B close it.
  import { onMount } from "svelte";
  import { pushScope } from "../../lib/input.svelte.ts";
  import type { DomRender } from "../../lib/mods.ts";

  let {
    render,
    props = {},
    onclose,
    onerror,
  }: {
    render: DomRender;
    props?: Record<string, unknown>;
    onclose?: () => void;
    /** Without it a throw goes up to Game.svelte's boundary. */
    onerror?: (e: unknown) => void;
  } = $props();

  let el = $state<HTMLElement>();

  onMount(() => {
    let cleanup: unknown;
    try {
      cleanup = render(el!, props);
    } catch (e) {
      if (!onerror) throw e;
      return onerror(e);
    }
    return () => {
      try {
        if (typeof cleanup === "function") cleanup();
      } catch (e) {
        console.error("mod cleanup", e);
      }
    };
  });

  $effect(() => {
    if (!onclose) return;
    const close = onclose;
    return pushScope({
      name: "mod-layer",
      modal: true,
      whileBusy: true,
      root: () => el,
      handle: (a) => (a.type === "menu" || a.type === "back" ? (close(), true) : false),
    });
  });
</script>

<div class="dom" class:layer={!!onclose} bind:this={el}></div>

<style>
  .dom {
    position: absolute;
    inset: 0;
  }
  .layer {
    position: fixed;
    z-index: 30;
    background: var(--night-700);
  }
</style>
