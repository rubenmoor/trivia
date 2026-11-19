<script lang="ts">
  // Picking a name (plans/04-ui-tv-display.md, "Player"; task 2119): the known names (most recent first, keys 1–9) with
  // exactly one selected while any exist, a field for a new one, and one big button at the bottom that goes on with the
  // selection (the scope's primary: Enter/A anywhere, also in the field). Click, Space/X or a digit select a name; typing
  // makes the field the selection. The badges button has its letter and the pad's View button. With a pad, Y writes:
  // Steam's floating keyboard (Big Picture/Deck, plan 85), else the letter picker (plan 46). The Player screen and the
  // Join screen's name dialog (plan 162).
  import { untrack } from "svelte";
  import { steam } from "../lib/desktop.ts";
  import { show } from "../lib/focus.ts";
  import { t, variants } from "../lib/i18n.ts";
  import { focusControl, lastDevice, pushScope, type Intent } from "../lib/input.svelte.ts";
  import type { Player } from "../lib/types.ts";
  import Icon from "./Icon.svelte";
  import { MAX_NAME } from "./letters.ts";
  import LetterPicker from "./LetterPicker.svelte";
  import OptionButton from "./OptionButton.svelte";
  import Prompt from "./Prompt.svelte";

  let {
    players,
    busy,
    scope,
    modal = false,
    suggest = false,
    refusal = null,
    submitLabel = t("screen.player.submit"),
    onchoose,
    ondelete,
    onbadges,
    onclose,
  }: {
    players: Player[];
    busy: boolean;
    /** The input scope's name. */
    scope: string;
    /** In a dialog: the focus starts inside, Back and Esc close it. */
    modal?: boolean;
    /** With no known names: a funny team name is filled in, Enter or A confirms it. */
    suggest?: boolean;
    /** Why the last pick was refused, under the field. */
    refusal?: string | null;
    /** The bottom button. */
    submitLabel?: string;
    onchoose: (name: string) => void;
    /** A delete control per name (the Player screen). */
    ondelete?: (p: Player) => void;
    /** The badges button, for the selected name (the Player screen, not in the demo). */
    onbadges?: (p: Player) => void;
    onclose?: () => void;
  } = $props();

  const MAX_SHOWN = 9;

  const suggestion = untrack(() => {
    const names = variants("screen.player.teamNames");
    return suggest && players.length === 0 ? names[Math.floor(Math.random() * names.length)] : "";
  });
  let name = $state(suggestion);
  let input = $state<HTMLInputElement>();
  let box = $state<HTMLElement>();
  let playButton = $state<HTMLButtonElement>();
  let picking = $state(false);
  const BADGES: Extract<Intent, { type: "letter" }> = { type: "letter", key: t("screen.player.badgesKey").toLowerCase() };
  /** The name selected by click, Space or digit; null: none yet. */
  let picked = $state<string | null>(null);
  /** Typed since the last pick: the field is the selection while it has text. */
  let typing = $state(false);

  const shown = $derived(players.slice(0, MAX_SHOWN));
  const typed = $derived(name.trim().replace(/\s+/g, " "));
  /** The selection: a known name, or the field's new one (`fresh`); null only with no names and an empty field. */
  const choice = $derived.by((): { name: string; fresh: boolean } | null => {
    if (typing && typed) return { name: typed, fresh: true };
    const p = shown.find((x) => x.name === picked) ?? shown[0];
    if (p) return { name: p.name, fresh: false };
    return typed ? { name: typed, fresh: true } : null;
  });
  const selected = $derived(choice && !choice.fresh ? choice.name : null);
  const selectedPlayer = $derived(shown.find((p) => p.name === selected));

  // Once usable: a dialog focuses its first control; with no names the field gets focus.
  let focused = false;
  $effect(() => {
    if (busy || focused || !box) return;
    focused = true;
    if (modal) focusControl(box.querySelector<HTMLElement>(".name-button") ?? input);
    else if (players.length === 0) input?.focus();
  });

  function select(p: Player) {
    picked = p.name;
    typing = false;
  }

  function submit(e?: Event) {
    e?.preventDefault();
    if (choice && !busy) onchoose(choice.name);
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

  // 1–9 select a name and take the ring; Enter/A is the bottom button; the badges letter (or View) opens the selected name's
  // badges; Y writes; any other letter goes into the field (input.svelte.ts).
  $effect(() =>
    pushScope({
      name: scope,
      modal,
      root: () => box,
      text: () => input,
      keys: onbadges ? { [BADGES.key]: BADGES } : undefined,
      pad: (): Record<number, Intent> => (onbadges ? { 3: { type: "write" }, 8: BADGES } : { 3: { type: "write" } }),
      primary: () => playButton,
      handle: (a) => {
        if (a.type === "pick" && a.n <= shown.length) {
          select(shown[a.n - 1]);
          if (box) show(box.querySelector<HTMLElement>(`[data-focus-id="name-${a.n}"]`), scope, box);
        } else if (a.type === "letter" && onbadges) {
          if (selectedPlayer) onbadges(selectedPlayer);
        } else if (a.type === "write") void write();
        else if (modal && (a.type === "back" || a.type === "menu")) onclose?.();
        else return false;
        return true;
      },
    }),
  );
</script>

<div class="name-picker" bind:this={box}>
  {#if shown.length}
    <div class="pick-row names" role="radiogroup">
      {#each shown as p, i (p.name)}
        <div class="entry">
          <OptionButton
            class="name-button"
            on={selected === p.name}
            style="--i:{i + 1}"
            role="radio"
            aria-checked={selected === p.name}
            onclick={() => select(p)}
            disabled={busy}
            data-focus-id="name-{i + 1}"
            data-focus-default={selected === p.name || undefined}
            caption={p.name}
          >
            {#snippet icon()}<Icon name="person" />{/snippet}
            {#snippet chip()}<Prompt action={{ type: "pick", n: i + 1 }} hold />{/snippet}
            <span class="label">{games(p)}</span>
          </OptionButton>
          {#if ondelete}
            <button class="delete" onclick={() => ondelete(p)} disabled={busy} title={t("screen.player.delete", { name: p.name })}>
              <Icon name="trash" />
            </button>
          {/if}
        </div>
      {/each}
    </div>
    {#if onbadges}
      <button class="secondary badges" onclick={() => selectedPlayer && onbadges(selectedPlayer)} disabled={busy || !selectedPlayer}>
        <Icon name="award" /> {t("screen.player.showBadges")} <Prompt action={BADGES} off={!selectedPlayer} />
      </button>
    {/if}
  {/if}

  <form class="new glass" class:on={choice?.fresh} onsubmit={submit}>
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
        data-focus-default={shown.length === 0 || undefined}
        oninput={() => (typing = true)}
      />
      {#if lastDevice.current === "gamepad"}
        <button class="secondary" type="button" onclick={() => void write()} disabled={busy} data-nofocus tabindex="-1">
          <Prompt action="write" />
          <Icon name="pencil" /> {t("picker.write")}
        </button>
      {/if}
    </div>
    {#if refusal}<p class="error">{refusal}</p>{/if}
  </form>

  <button class="candy play" bind:this={playButton} onclick={submit} disabled={busy || !choice} data-focus-id="play">
    <Icon name={choice?.fresh ? "person-plus" : "rocket"} /> {submitLabel} <Prompt action="confirm" off={!choice} />
  </button>

  {#if picking}<LetterPicker bind:name {busy} onsubmit={submit} onclose={() => (picking = false)} />{/if}
</div>

<style>
  .name-picker {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: calc(1.6 * var(--u));
  }
  .names {
    max-width: calc(96 * var(--u));
  }
  .entry {
    position: relative;
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
    transition:
      color 0.15s,
      border-color 0.15s;
  }
  .delete:hover:not(:disabled),
  .delete:focus-visible,
  .delete:global([data-nav]) {
    color: var(--coral);
    border-color: var(--coral);
  }
  .badges {
    padding: calc(0.8 * var(--u)) calc(2.2 * var(--u));
    border-color: var(--sky);
    font-size: calc(1.8 * var(--u));
    font-weight: 800;
    animation: arrive 0.5s 0.3s var(--spring) backwards;
  }
  .badges :global(.icon) {
    color: var(--amber);
  }
  .badges:disabled {
    border-color: var(--slate-600);
    color: var(--slate-400);
  }
  .badges:disabled :global(.icon) {
    color: inherit;
  }
  .new {
    display: flex;
    flex-direction: column;
    gap: calc(0.6 * var(--u));
    padding: calc(1.2 * var(--u)) calc(1.6 * var(--u));
    transition: border-color 0.2s, background-color 0.2s;
    animation: arrive 0.5s 0.35s var(--spring) backwards;
  }
  .new.on {
    border-color: var(--sky);
    background: rgba(76, 201, 240, 0.16);
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
  .play {
    margin-top: calc(0.4 * var(--u));
    font-size: calc(2.4 * var(--u));
    padding: calc(1 * var(--u)) calc(3 * var(--u));
    animation: arrive 0.5s 0.45s var(--spring) backwards;
  }
  .error {
    margin: 0;
    color: var(--coral);
    font-size: calc(1.1 * var(--u));
  }
</style>
