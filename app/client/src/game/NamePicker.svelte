<script lang="ts">
  // Picking a name (plans/04-ui-tv-display.md, "Player"): the known names (most recent first, keys 1–9) and a field for
  // a new one. With a pad, A on the field opens Steam's floating keyboard (Big Picture/Deck, plan 85), else the letter
  // picker (plan 46). The Player screen and the Join screen's name dialog (plan 162).
  import { steam } from "../lib/desktop.ts";
  import { t } from "../lib/i18n.ts";
  import { focusControl, lastDevice, pushScope, scopes } from "../lib/input.svelte.ts";
  import type { Player } from "../lib/types.ts";
  import Icon from "./Icon.svelte";
  import { MAX_NAME } from "./letters.ts";
  import LetterPicker from "./LetterPicker.svelte";
  import Prompt from "./Prompt.svelte";

  let {
    players,
    busy,
    scope,
    modal = false,
    refusal = null,
    submitLabel = t("screen.player.submit"),
    onchoose,
    ondelete,
    onclose,
  }: {
    players: Player[];
    busy: boolean;
    /** The input scope's name. */
    scope: string;
    /** In a dialog: the focus starts inside, Back and Esc close it. */
    modal?: boolean;
    /** Why the last pick was refused, under the field. */
    refusal?: string | null;
    /** The new name's button. */
    submitLabel?: string;
    onchoose: (name: string) => void;
    /** A delete control per name (the Player screen). */
    ondelete?: (p: Player) => void;
    onclose?: () => void;
  } = $props();

  const MAX_SHOWN = 9;

  let name = $state("");
  let input = $state<HTMLInputElement>();
  let box = $state<HTMLElement>();
  let picking = $state(false);
  let onField = $state(false);

  const shown = $derived(players.slice(0, MAX_SHOWN));
  const typed = $derived(name.trim().replace(/\s+/g, " "));
  /** Nothing in here has focus: Enter picks the most recent name. */
  const free = $derived.by(() => {
    void scopes.version;
    return shown.length > 0 && !box?.contains(document.activeElement);
  });

  // Once usable: a dialog focuses its first control; with no names the field gets focus.
  let focused = false;
  $effect(() => {
    if (busy || focused || !box) return;
    focused = true;
    if (modal) focusControl(box.querySelector<HTMLElement>(".name-button") ?? input);
    else if (players.length === 0) input?.focus();
  });

  function submit(e?: Event) {
    e?.preventDefault();
    if (typed && !busy) onchoose(typed);
  }

  /** Steam's keyboard when it shows one, else the letter picker. */
  async function write() {
    if (input && steam?.available) {
      input.focus();
      const r = input.getBoundingClientRect();
      const d = window.devicePixelRatio;
      const rect = { x: r.x * d, y: r.y * d, width: r.width * d, height: r.height * d };
      if (await steam.showTextInput(rect, name).catch(() => false)) return;
    }
    picking = true;
  }

  function games(p: Player) {
    if (p.games === 0) return t("screen.player.gamesNone");
    const n = t("screen.player.games", { n: p.games });
    return p.won ? t("screen.player.gamesWon", { games: n, won: t("screen.player.won", { n: p.won }) }) : n;
  }

  // 1–9 pick a name; Enter in the field sends it, with nothing focused the most recent name; a letter
  // elsewhere goes into the field (input.svelte.ts).
  $effect(() =>
    pushScope({
      name: scope,
      modal,
      root: () => box,
      text: () => input,
      handle: (a) => {
        if (a.type === "pick" && a.n <= shown.length) onchoose(shown[a.n - 1].name);
        else if (a.type === "confirm" && document.activeElement === input) {
          if (a.device === "gamepad") void write();
          else submit();
        }
        else if (a.type === "confirm" && free && !busy) onchoose(shown[0].name);
        else if (modal && (a.type === "back" || a.type === "menu")) onclose?.();
        else return false;
        return true;
      },
    }),
  );
</script>

<div class="name-picker" bind:this={box}>
  {#if shown.length}
    <div class="names">
      {#each shown as p, i (p.name)}
        <div class="entry" style:--i={i}>
          <button class="name-button glass" onclick={() => onchoose(p.name)} disabled={busy} data-focus-default>
            <Prompt action={{ type: "pick", n: i + 1 }} hold />
            <span class="who"><Icon name="person" /> {p.name}{#if i === 0 && free}<Prompt action="confirm" />{/if}</span>
            <span class="label">{games(p)}</span>
          </button>
          {#if ondelete}
            <button class="delete" onclick={() => ondelete(p)} disabled={busy} title={t("screen.player.delete", { name: p.name })}>
              <Icon name="trash" />
            </button>
          {/if}
        </div>
      {/each}
    </div>
  {/if}

  <form class="new glass" onsubmit={submit}>
    <label class="label" for="new-player">{t(shown.length ? "screen.player.newLabel" : "screen.player.firstLabel")}</label>
    <div class="row">
      <input
        id="new-player"
        bind:this={input}
        bind:value={name}
        maxlength={MAX_NAME}
        autocomplete="off"
        spellcheck="false"
        placeholder={t("screen.player.placeholder")}
        disabled={busy}
        data-focus-default
        onfocus={() => (onField = true)}
        onblur={() => (onField = false)}
      />
      {#if lastDevice.current === "gamepad"}
        <button class="secondary" type="button" onclick={() => void write()} disabled={busy} data-nofocus tabindex="-1">
          <Prompt action="confirm" fixed off={!onField} />
          <Icon name="pencil" /> {t("picker.write")}
        </button>
      {/if}
      <button class="candy" type="submit" disabled={busy || !typed}><Icon name="person-plus" /> {submitLabel} <Prompt action="confirm" off={!typed} /></button>
    </div>
    {#if refusal}<p class="error">{refusal}</p>{/if}
  </form>

  {#if picking}<LetterPicker bind:name {busy} onsubmit={submit} onclose={() => (picking = false)} />{/if}
</div>

<style>
  .name-picker {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: calc(2 * var(--u));
  }
  .names {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: calc(1.2 * var(--u));
    max-width: calc(96 * var(--u));
  }
  .entry {
    position: relative;
    animation: arrive 0.5s calc(0.15s + var(--i) * 0.06s) var(--spring) backwards;
  }
  .delete {
    position: absolute;
    top: calc(-0.7 * var(--u));
    right: calc(-0.7 * var(--u));
    display: grid;
    place-items: center;
    width: calc(2.4 * var(--u));
    height: calc(2.4 * var(--u));
    padding: 0;
    border: 1px solid var(--slate-600);
    border-radius: 50%;
    background: var(--night-700);
    color: var(--slate-400);
    font-size: calc(1.2 * var(--u));
    opacity: 0;
    transition:
      opacity 0.15s,
      color 0.15s,
      border-color 0.15s;
  }
  .entry:hover .delete,
  .delete:focus-visible,
  .delete:global([data-nav]) {
    opacity: 1;
  }
  .delete:hover {
    color: var(--coral);
    border-color: var(--coral);
  }
  .name-button {
    display: grid;
    grid-template-columns: auto 1fr;
    grid-template-rows: auto auto;
    column-gap: calc(1 * var(--u));
    align-items: center;
    min-width: calc(20 * var(--u));
    padding: calc(1 * var(--u)) calc(1.6 * var(--u));
    border-color: var(--slate-600);
    text-align: left;
    transition:
      transform 0.2s var(--spring),
      border-color 0.2s;
  }
  .name-button:hover:not(:disabled),
  .name-button:focus-visible,
  .name-button:global([data-nav]) {
    border-color: var(--sky);
    transform: translateY(calc(-0.3 * var(--u)));
  }
  .name-button :global(kbd) {
    grid-row: span 2;
  }
  .who {
    font-family: var(--font-display);
    font-size: calc(2.2 * var(--u));
    font-weight: 800;
    line-height: 1.1;
  }
  .who :global(kbd) {
    margin-left: 0.5em;
    vertical-align: middle;
  }
  .new {
    display: flex;
    flex-direction: column;
    gap: calc(0.6 * var(--u));
    padding: calc(1.2 * var(--u)) calc(1.6 * var(--u));
    animation: arrive 0.5s 0.35s var(--spring) backwards;
  }
  .row {
    display: flex;
    gap: calc(1 * var(--u));
    align-items: center;
  }
  input {
    width: calc(26 * var(--u));
    padding: calc(0.6 * var(--u)) calc(1 * var(--u));
    border: 1px solid var(--slate-400);
    border-radius: calc(0.8 * var(--u));
    background: rgba(11, 17, 32, 0.6);
    color: var(--paper);
    font-family: var(--font-display);
    font-size: calc(2 * var(--u));
    font-weight: 700;
  }
  input:focus {
    outline: none;
    border-color: var(--sky);
    box-shadow: 0 0 0 calc(0.2 * var(--u)) rgba(76, 201, 240, 0.35);
  }
  input::placeholder {
    color: var(--slate-400);
  }
  .error {
    margin: 0;
    color: var(--coral);
    font-size: calc(1.1 * var(--u));
  }
</style>
