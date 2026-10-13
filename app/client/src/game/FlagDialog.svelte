<script lang="ts">
  // The flag dialog (GM-5, decision 60): flag icon or M. An optional note; Enter flags (or saves the
  // note of a flagged question), Esc/⌫ cancel. A pad's A on the field opens the letter picker.
  import { tick } from "svelte";
  import { t } from "../lib/i18n";
  import { focusControl, lastDevice, pushScope } from "../lib/input.svelte";
  import LetterPicker from "./LetterPicker.svelte";
  import { MAX_NOTE } from "./letters";
  import Prompt from "./Prompt.svelte";

  let {
    flagged,
    note: initial,
    busy,
    onflag,
    onunflag,
    onclose,
  }: {
    /** The question is already flagged: save the note or unflag. */
    flagged: boolean;
    note: string;
    busy: boolean;
    onflag: (note: string) => void;
    onunflag: () => void;
    onclose: () => void;
  } = $props();

  // svelte-ignore state_referenced_locally
  let note = $state(initial);
  let picking = $state(false);
  let dialog = $state<HTMLDivElement>();
  let input = $state<HTMLInputElement>();
  let onField = $state(false);

  function submit() {
    if (!busy) onflag(note);
  }

  $effect(() => {
    const pop = pushScope({
      name: "flag-dialog",
      modal: true,
      whileBusy: true,
      root: () => dialog,
      text: () => input,
      handle: (a) => {
        if (a.type === "back" || a.type === "menu" || (a.type === "flag" && a.device === "gamepad")) onclose();
        else if (a.type === "confirm" && document.activeElement === input) {
          if (a.device === "gamepad") picking = true;
          else submit();
        } else if (a.type !== "flag") return false;
        return true;
      },
    });
    tick().then(() => focusControl(input));
    return pop;
  });
</script>

<div class="backdrop">
  <div class="dialog" bind:this={dialog} role="alertdialog" aria-labelledby="flag-title">
    <h2 id="flag-title">{t(flagged ? "flag.titleOn" : "flag.title")}</h2>
    <p>{t("flag.body")}</p>
    <div class="field">
      <input
        bind:this={input}
        bind:value={note}
        maxlength={MAX_NOTE}
        autocomplete="off"
        placeholder={t("flag.notePlaceholder")}
        data-focus-default
        onfocus={() => (onField = true)}
        onblur={() => (onField = false)}
      />
      {#if lastDevice.current === "gamepad"}
        <button class="secondary" onclick={() => (picking = true)} data-nofocus tabindex="-1">
          <Prompt action="confirm" fixed off={!onField} />
          {t("picker.write")}
        </button>
      {/if}
    </div>
    <div class="choices">
      <button class="secondary" onclick={onclose}>{t("action.cancel")} <Prompt action="menu" pad="back" /></button>
      {#if flagged}<button class="secondary" onclick={onunflag} disabled={busy}>{t("flag.unflag")}</button>{/if}
      <button class="candy" onclick={submit} disabled={busy}>{t(flagged ? "flag.save" : "flag.confirm")} <Prompt action="confirm" /></button>
    </div>
  </div>
  {#if picking}<LetterPicker bind:name={note} {busy} note onclose={() => (picking = false)} />{/if}
</div>

<style>
  .backdrop {
    position: fixed;
    inset: 0;
    z-index: 45;
    display: grid;
    place-items: center;
    background: var(--dim);
  }
  .dialog {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: calc(1 * var(--u));
    max-width: calc(60 * var(--u));
    padding: calc(2.4 * var(--u));
    border: 1px solid var(--slate-600);
    border-radius: calc(1.6 * var(--u));
    background: var(--night-700);
    box-shadow: 0 calc(1.5 * var(--u)) calc(4 * var(--u)) rgba(0, 0, 0, 0.6);
  }
  h2 {
    margin: 0;
    font-family: var(--font-display);
    font-size: calc(2.6 * var(--u));
    font-weight: 800;
  }
  p {
    margin: 0;
    color: var(--slate-200);
  }
  .field {
    display: flex;
    gap: calc(1 * var(--u));
    align-self: stretch;
  }
  input {
    flex: 1;
    min-width: 0;
    padding: calc(0.6 * var(--u)) calc(1 * var(--u));
    border: 1px solid var(--slate-400);
    border-radius: calc(0.8 * var(--u));
    background: rgba(11, 17, 32, 0.6);
    color: var(--paper);
    font: inherit;
    font-size: calc(1.4 * var(--u));
  }
  input:focus {
    outline: none;
    border-color: var(--sky);
    box-shadow: 0 0 0 calc(0.2 * var(--u)) rgba(76, 201, 240, 0.35);
  }
  input::placeholder {
    color: var(--slate-400);
  }
  .choices {
    display: flex;
    gap: calc(1 * var(--u));
  }
  .choices button {
    white-space: nowrap;
  }
</style>
