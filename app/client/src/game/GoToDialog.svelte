<script lang="ts">
  // «Ir a pregunta…» (dev mode, plan 85): a question id (`q-0007` or `7`) replaces the one on screen.
  // Enter opens it, Esc/⌫ cancel; a pad's A on the field opens Steam's keyboard, else the letter picker.
  import { tick } from "svelte";
  import { steam } from "../lib/desktop.ts";
  import { t } from "../lib/i18n.ts";
  import { focusControl, lastDevice, pushScope } from "../lib/input.svelte.ts";
  import LetterPicker from "./LetterPicker.svelte";
  import Prompt from "./Prompt.svelte";

  let {
    ongo,
    onclose,
  }: {
    /** The refusal's text, or null when it opened. */
    ongo: (id: string) => Promise<string | null>;
    onclose: () => void;
  } = $props();

  let id = $state("");
  let busy = $state(false);
  let error = $state<string | null>(null);
  let picking = $state(false);
  let dialog = $state<HTMLDivElement>();
  let input = $state<HTMLInputElement>();
  let onField = $state(false);

  async function submit() {
    if (busy || !id.trim()) return;
    busy = true;
    error = await ongo(id.trim());
    busy = false;
  }

  /** Steam's keyboard when it shows one, else the letter picker. */
  async function write() {
    if (input && steam?.available) {
      input.focus();
      const r = input.getBoundingClientRect();
      const d = window.devicePixelRatio;
      const rect = { x: r.x * d, y: r.y * d, width: r.width * d, height: r.height * d };
      if (await steam.showTextInput(rect, id).catch(() => false)) return;
    }
    picking = true;
  }

  $effect(() => {
    const pop = pushScope({
      name: "goto-dialog",
      modal: true,
      whileBusy: true,
      root: () => dialog,
      text: () => input,
      handle: (a) => {
        if (a.type === "back" || a.type === "menu") onclose();
        else if (a.type === "confirm" && document.activeElement === input) {
          if (a.device === "gamepad") void write();
          else void submit();
        } else return false;
        return true;
      },
    });
    tick().then(() => focusControl(input));
    return pop;
  });
</script>

<div class="backdrop">
  <div class="dialog" bind:this={dialog} role="alertdialog" aria-labelledby="goto-title">
    <h2 id="goto-title">{t("overlay.goTo")}</h2>
    <p>{t("overlay.goToBody")}</p>
    <div class="field">
      <input
        bind:this={input}
        bind:value={id}
        maxlength={20}
        autocomplete="off"
        spellcheck="false"
        data-focus-default
        onfocus={() => (onField = true)}
        onblur={() => (onField = false)}
      />
      {#if lastDevice.current === "gamepad"}
        <button class="secondary" onclick={() => void write()} data-nofocus tabindex="-1">
          <Prompt action="confirm" fixed off={!onField} />
          {t("picker.write")}
        </button>
      {/if}
    </div>
    {#if error}<p class="error">{error}</p>{/if}
    <div class="choices">
      <button class="secondary" onclick={onclose}>{t("action.cancel")} <Prompt action="menu" pad="back" /></button>
      <button class="candy" onclick={submit} disabled={busy || !id.trim()}>{t("overlay.goToOpen")} <Prompt action="confirm" /></button>
    </div>
  </div>
  {#if picking}<LetterPicker bind:name={id} {busy} note onsubmit={submit} onclose={() => (picking = false)} />{/if}
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
  .error {
    color: var(--coral);
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
  .choices {
    display: flex;
    gap: calc(1 * var(--u));
  }
  .choices button {
    white-space: nowrap;
  }
</style>
