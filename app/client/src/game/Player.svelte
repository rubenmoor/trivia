<script lang="ts">
  // The Player screen (plans/04-ui-tv-display.md, "Player", D-28, UI-16): «¿Quién juega?» with the
  // known names (most recent first, keys 1–9) and a field for a new name. Names are labels; what the
  // family saw counts for the whole save (plan 65). Each name can be deleted with its games, after a
  // confirmation (GF-7); its seen questions stay seen.
  import { onMount } from "svelte";
  import { deletePlayer, fetchPlayers } from "../lib/api";
  import { errorText } from "../lib/errors";
  import { t } from "../lib/i18n";
  import { focusControl, pushScope } from "../lib/input.svelte";
  import type { Player, Supply } from "../lib/types";
  import Icon from "./Icon.svelte";
  import Prompt from "./Prompt.svelte";

  let {
    busy,
    greeting,
    refused,
    onchoose,
    ondeleted,
  }: {
    busy: boolean;
    /** The chosen name while «¡Hola, …!» plays into the transition, else null. */
    greeting: string | null;
    /** The supply report when the pool can't fill a game for the chosen player (GF-5). */
    refused: Supply | null;
    onchoose: (name: string) => void;
    /** A player was deleted (their running game may be gone too). */
    ondeleted: () => void;
  } = $props();

  const MAX_SHOWN = 9;

  let players = $state<Player[]>([]);
  let loaded = $state(false);
  let error = $state<string | null>(null);
  let name = $state("");
  let input = $state<HTMLInputElement>();
  /** The player waiting for «¿Borrar…?» to be confirmed, or null. */
  let doomed = $state<Player | null>(null);
  let deleting = $state(false);
  let cancelButton = $state<HTMLButtonElement>();
  let section = $state<HTMLElement>();
  let dialog = $state<HTMLDivElement>();

  onMount(async () => {
    try {
      players = await fetchPlayers();
    } catch (e) {
      error = errorText(e);
    }
    loaded = true;
    if (players.length === 0) input?.focus();
  });

  const shown = $derived(players.slice(0, MAX_SHOWN));
  const typed = $derived(name.trim().replace(/\s+/g, " "));

  function submit(e?: Event) {
    e?.preventDefault();
    if (typed && !busy) onchoose(typed);
  }

  function games(p: Player) {
    if (p.games === 0) return t("screen.player.gamesNone");
    const n = t("screen.player.games", { n: p.games });
    return p.won ? t("screen.player.gamesWon", { games: n, won: t("screen.player.won", { n: p.won }) }) : n;
  }

  function askDelete(p: Player) {
    doomed = p;
  }

  async function confirmDelete() {
    if (!doomed || deleting) return;
    deleting = true;
    try {
      players = await deletePlayer(doomed.name);
      error = null;
      ondeleted();
    } catch (e) {
      error = errorText(e);
    } finally {
      deleting = false;
      doomed = null;
    }
  }

  // 1–9 pick a name; Enter in the field sends it; a letter elsewhere goes into the field (input.svelte.ts).
  $effect(() =>
    pushScope({
      name: "player",
      root: () => section,
      text: () => input,
      handle: (a) => {
        if (a.type === "pick" && a.n <= shown.length) onchoose(shown[a.n - 1].name);
        else if (a.type === "confirm" && document.activeElement === input) submit();
        else return false;
        return true;
      },
    }),
  );

  // The delete confirmation gets every action; Esc/Backspace cancel, Enter and Tab work on its buttons.
  $effect(() => {
    if (!doomed) return;
    const pop = pushScope({
      name: "player-delete",
      modal: true,
      whileBusy: true,
      root: () => dialog,
      handle: (a) => (a.type === "back" || a.type === "menu") && ((doomed = null), true),
    });
    focusControl(cancelButton); // a stray Enter must not delete anyone
    return pop;
  });
</script>

<section class="player" bind:this={section}>
  {#if greeting}
    <h1 class="title hello">{t("screen.player.helloOpen")}<span class="name">{greeting}</span>{t("screen.player.helloClose")}</h1>
  {:else}
    <h1 class="title">{t("screen.player.title")}</h1>

    {#if shown.length}
      <div class="names">
        {#each shown as p, i (p.name)}
          <div class="entry" style:--i={i}>
            <button class="name-button glass" onclick={() => onchoose(p.name)} disabled={busy} data-focus-default>
              <Prompt action={{ type: "pick", n: i + 1 }} hold />
              <span class="who">{p.name}</span>
              <span class="label">{games(p)}</span>
            </button>
            <button class="delete" onclick={() => askDelete(p)} disabled={busy} title={t("screen.player.delete", { name: p.name })}>
              <Icon name="trash" />
            </button>
          </div>
        {/each}
      </div>
    {/if}

    {#if loaded}
      <form class="new glass" onsubmit={submit}>
        <label class="label" for="new-player">{t(shown.length ? "screen.player.newLabel" : "screen.player.firstLabel")}</label>
        <div class="row">
          <input
            id="new-player"
            bind:this={input}
            bind:value={name}
            maxlength="30"
            autocomplete="off"
            spellcheck="false"
            placeholder={t("screen.player.placeholder")}
            disabled={busy}
            data-focus-default
          />
          <button class="candy" type="submit" disabled={busy || !typed}>{t("screen.player.submit")} <Prompt action="confirm" off={!typed} /></button>
        </div>
      </form>
    {/if}

    {#if error}<p class="error">{error}</p>{/if}

    {#if doomed}
      <div class="backdrop">
        <div class="dialog" bind:this={dialog} role="alertdialog" aria-labelledby="delete-title">
          <h2 id="delete-title">{t("screen.player.confirmOpen")}<span class="doomed">{doomed.name}</span>{t("screen.player.confirmClose")}</h2>
          <p>
            {t("screen.player.confirmBody", {
              lose: doomed.games ? t("screen.player.lose", { n: doomed.games }) : t("screen.player.loseNone"),
            })}
          </p>
          <div class="row">
            <button class="secondary" bind:this={cancelButton} onclick={() => (doomed = null)} data-focus-default>{t("action.cancel")} <Prompt action="menu" pad="back" /></button>
            <button class="danger" onclick={confirmDelete} disabled={deleting}>{t("screen.player.confirm")}</button>
          </div>
        </div>
      </div>
    {/if}
    {#if refused && !refused.ok}
      <div class="supply glass">
        <p>{t("supply.short", { n: refused.available })}</p>
        <ul>
          {#each refused.levels.filter((l) => l.missing) as l (l.level)}
            <li>{t("supply.level", { level: l.level, lo: l.range[0], hi: l.range[1], missing: l.missing })}</li>
          {/each}
        </ul>
      </div>
    {/if}
  {/if}
</section>

<style>
  .player {
    position: absolute;
    inset: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: calc(2 * var(--u));
    padding: var(--safe-y) var(--safe-x);
    text-align: center;
  }
  .title {
    animation: arrive 0.6s var(--spring) backwards;
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
  .backdrop {
    position: fixed;
    inset: 0;
    z-index: 10;
    display: grid;
    place-items: center;
    background: rgba(5, 8, 16, 0.72);
  }
  .dialog {
    max-width: calc(48 * var(--u));
    padding: calc(2.2 * var(--u)) calc(2.6 * var(--u));
    border: 1px solid var(--slate-600);
    border-radius: calc(1.6 * var(--u));
    background: var(--night-700);
    box-shadow: 0 calc(1.5 * var(--u)) calc(4 * var(--u)) rgba(0, 0, 0, 0.6);
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: calc(1.2 * var(--u));
    animation: arrive 0.35s var(--spring) backwards;
  }
  .dialog h2 {
    margin: 0;
    font-family: var(--font-display);
    font-size: calc(2.4 * var(--u));
    font-weight: 800;
  }
  .doomed {
    color: var(--coral);
  }
  .dialog p {
    margin: 0;
    color: var(--slate-200);
  }
  .danger {
    padding: calc(0.7 * var(--u)) calc(2 * var(--u));
    border: none;
    border-radius: calc(1 * var(--u));
    background: var(--coral);
    color: var(--night-900);
    font-family: var(--font-display);
    font-size: calc(1.6 * var(--u));
    font-weight: 800;
  }
  .danger:focus-visible,
  .danger:global([data-nav]) {
    outline-color: var(--paper);
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
  .hello {
    font-size: calc(7 * var(--u));
    animation: hello 0.8s var(--spring) backwards;
  }
  .hello .name {
    color: var(--amber);
  }
  .error {
    margin: 0;
    color: var(--coral);
    font-size: calc(1.1 * var(--u));
  }
  .supply {
    padding: calc(1 * var(--u)) calc(1.6 * var(--u));
    font-size: calc(1.1 * var(--u));
    color: var(--amber);
    text-align: left;
  }
  .supply p {
    margin: 0;
  }
  .supply ul {
    margin: calc(0.4 * var(--u)) 0 0;
  }
  @keyframes arrive {
    from {
      opacity: 0;
      transform: translateY(calc(2 * var(--u))) scale(0.94);
    }
  }
  @keyframes hello {
    from {
      opacity: 0;
      transform: scale(0.5) rotate(-4deg);
    }
  }
</style>
