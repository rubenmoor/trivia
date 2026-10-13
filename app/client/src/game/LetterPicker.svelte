<script lang="ts">
  // The letter picker (plans/04-ui-tv-display.md, "Player"; plan 46, SW-4): a new name with a pad only;
  // `note`: the flag dialog's note (digits and punctuation too, may stay empty).
  // Opens only for a pad; A types the focused key, B deletes (closes on an empty name), Start closes.
  // Letters, Backspace, Enter and Esc work too (a Deck with a keyboard); the text stays on close.
  import { tick } from "svelte";
  import { t } from "../lib/i18n";
  import { focusControl, pushScope, type Keys } from "../lib/input.svelte";
  import { typeKey } from "./letters";
  import Prompt from "./Prompt.svelte";

  let {
    name = $bindable(),
    busy,
    note = false,
    onsubmit,
    onclose,
  }: {
    name: string;
    busy: boolean;
    note?: boolean;
    onsubmit?: () => void;
    onclose: () => void;
  } = $props();

  // svelte-ignore state_referenced_locally
  const LETTERS = [...t("picker.letters"), ...(note ? t("picker.marks") : "")];
  const KEYS: Keys = Object.fromEntries(LETTERS.map((l) => [l.toLowerCase(), { type: "letter", key: l.toLowerCase() }]));
  /** Characters shown of a long note: its end, where typing happens. */
  const SHOWN = 32;

  let panel = $state<HTMLDivElement>();
  const typed = $derived(name.trim());
  const shown = $derived(name.length > SHOWN ? `…${name.slice(-SHOWN)}` : name);

  function type(key: string) {
    name = typeKey(name, key, note);
  }

  function erase() {
    name = name.slice(0, -1);
  }

  function done() {
    if ((!typed && !note) || busy) return;
    onclose();
    onsubmit?.();
  }

  $effect(() => {
    const pop = pushScope({
      name: "letters",
      modal: true,
      whileBusy: true,
      keys: KEYS,
      root: () => panel,
      handle: (a) => {
        if (a.type === "letter") type(a.key);
        else if (a.type === "back") {
          if (name) erase();
          else onclose();
        } else if (a.type === "menu") onclose();
        else return false;
        return true;
      },
    });
    tick().then(() => focusControl(panel?.querySelector<HTMLElement>("[data-focus-default]")));
    return pop;
  });
</script>

<div class="backdrop">
  <div class="panel glass-strong" bind:this={panel} role="dialog" aria-labelledby="letters-title">
    <h2 id="letters-title">{t(note ? "flag.pickerTitle" : "picker.title")}</h2>
    <div class="name" class:empty={!name}>{shown || (note ? "" : t("screen.player.placeholder"))}</div>
    <div class="grid">
      {#each LETTERS as l, i (l)}
        <button class="key" onclick={() => type(l)} data-focus-default={i === 0 || undefined}>{l}</button>
      {/each}
    </div>
    <div class="row">
      <button class="secondary" onclick={() => type(" ")}>{t("picker.space")}</button>
      <button class="secondary" onclick={erase}>⌫ {t("picker.erase")} <Prompt action="back" padOnly /></button>
      <button class="candy" onclick={done} disabled={busy || (!typed && !note)}>{t("picker.done")}</button>
    </div>
  </div>
</div>

<style>
  .backdrop {
    position: fixed;
    inset: 0;
    z-index: 10;
    display: grid;
    place-items: center;
    background: var(--dim);
  }
  .panel {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: calc(1.2 * var(--u));
    padding: calc(1.8 * var(--u)) calc(2.2 * var(--u));
    animation: zoom-in 0.35s var(--spring) backwards;
  }
  h2 {
    margin: 0;
    font-family: var(--font-display);
    font-size: calc(2.4 * var(--u));
    font-weight: 800;
  }
  .name {
    box-sizing: border-box;
    width: calc(34 * var(--u));
    min-height: calc(4.4 * var(--u));
    padding: calc(0.6 * var(--u)) calc(1 * var(--u));
    border: 1px solid var(--sky);
    border-radius: calc(0.8 * var(--u));
    background: rgba(11, 17, 32, 0.6);
    font-family: var(--font-display);
    font-size: calc(2 * var(--u));
    font-weight: 700;
    text-align: left;
    white-space: pre;
    overflow: hidden;
  }
  .name.empty {
    color: var(--slate-400);
  }
  .grid {
    display: grid;
    grid-template-columns: repeat(9, calc(4.4 * var(--u)));
    gap: calc(0.6 * var(--u));
  }
  .key {
    height: calc(4.4 * var(--u));
    padding: 0;
    border: none;
    border-radius: calc(0.7 * var(--u));
    background: var(--cream);
    color: var(--ink);
    font-family: var(--font-display);
    font-size: calc(2 * var(--u));
    font-weight: 800;
    box-shadow: 0 calc(0.25 * var(--u)) 0 var(--cream-edge);
    transition: transform 0.15s var(--spring);
  }
  .key:hover,
  .key:focus-visible,
  .key:global([data-nav]) {
    transform: translateY(calc(-0.2 * var(--u))) scale(1.06);
  }
  .row {
    display: flex;
    gap: calc(1 * var(--u));
    align-items: center;
  }
</style>
