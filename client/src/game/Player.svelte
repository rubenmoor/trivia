<script lang="ts">
  // The Player screen (plans/04-ui-tv-display.md, "Player", D-28, UI-16): «¿Quién juega?» with the
  // known names (most recent first, keys 1–9) and a field for a new name. The server keeps the
  // players and burns questions per player (server/game.py). Each name can be deleted with all its
  // progress, after a confirmation (GF-7).
  import { onMount, tick } from "svelte";
  import { deletePlayer, fetchPlayers } from "../lib/api";
  import type { Player, Supply } from "../lib/types";
  import Icon from "./Icon.svelte";

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

  onMount(async () => {
    try {
      players = await fetchPlayers();
    } catch (e) {
      error = e instanceof Error ? e.message : String(e);
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
    if (p.games === 0) return "sin partidas";
    const n = p.games === 1 ? "1 partida" : `${p.games} partidas`;
    return p.won ? `${n} · ${p.won === 1 ? "1 ganada" : `${p.won} ganadas`}` : n;
  }

  async function askDelete(p: Player) {
    doomed = p;
    await tick();
    cancelButton?.focus(); // a stray Enter must not delete anyone
  }

  async function confirmDelete() {
    if (!doomed || deleting) return;
    deleting = true;
    try {
      players = await deletePlayer(doomed.name);
      error = null;
      ondeleted();
    } catch (e) {
      error = e instanceof Error ? e.message : String(e);
    } finally {
      deleting = false;
      doomed = null;
    }
  }

  /** True while the delete confirmation is open: it gets every key, Esc included. */
  export function dialogOpen() {
    return doomed !== null;
  }

  /** Keys from Game.svelte: 1–9 pick a name; any letter starts typing a new one. */
  export function key(e: KeyboardEvent) {
    if (doomed) {
      if (e.key === "Escape" || e.key === "Backspace") {
        e.preventDefault();
        doomed = null;
      }
      return; // Enter, Tab and arrows work on the dialog's buttons
    }
    if (document.activeElement === input) {
      if (e.key === "Enter") submit(e);
      return;
    }
    const i = "123456789".indexOf(e.key);
    if (e.key.length === 1 && i >= 0 && i < shown.length) {
      e.preventDefault();
      onchoose(shown[i].name);
    } else if (e.key.length === 1 && /\p{L}/u.test(e.key) && !e.ctrlKey && !e.metaKey) {
      input?.focus(); // the letter goes into the field
    }
  }
</script>

<section class="player">
  {#if greeting}
    <h1 class="title hello">¡Hola, <span class="name">{greeting}</span>!</h1>
  {:else}
    <h1 class="title">¿Quién juega?</h1>

    {#if shown.length}
      <div class="names">
        {#each shown as p, i (p.name)}
          <div class="entry" style:--i={i}>
            <button class="name-button glass" onclick={() => onchoose(p.name)} disabled={busy}>
              <kbd>{i + 1}</kbd>
              <span class="who">{p.name}</span>
              <span class="label">{games(p)}</span>
            </button>
            <button class="delete" onclick={() => askDelete(p)} disabled={busy} title="Borrar a {p.name}">
              <Icon name="trash" />
            </button>
          </div>
        {/each}
      </div>
    {/if}

    {#if loaded}
      <form class="new glass" onsubmit={submit}>
        <label class="label" for="new-player">{shown.length ? "¿Alguien nuevo?" : "Escriban su nombre"}</label>
        <div class="row">
          <input
            id="new-player"
            bind:this={input}
            bind:value={name}
            maxlength="30"
            autocomplete="off"
            spellcheck="false"
            placeholder="Nombre"
            disabled={busy}
          />
          <button class="candy" type="submit" disabled={busy || !typed}>¡A jugar! <kbd>Enter</kbd></button>
        </div>
      </form>
    {/if}

    {#if error}<p class="error">{error}</p>{/if}

    {#if doomed}
      <div class="backdrop">
        <div class="dialog" role="alertdialog" aria-labelledby="delete-title">
          <h2 id="delete-title">¿Borrar a <span class="doomed">{doomed.name}</span>?</h2>
          <p>
            Se borran {doomed.games === 1 ? "su partida" : doomed.games ? `sus ${doomed.games} partidas` : "sus datos"}
            y todo su progreso: las preguntas que ya vio vuelven a salir. No se puede deshacer.
          </p>
          <div class="row">
            <button class="secondary" bind:this={cancelButton} onclick={() => (doomed = null)}>Cancelar <kbd>Esc</kbd></button>
            <button class="danger" onclick={confirmDelete} disabled={deleting}>Sí, borrar</button>
          </div>
        </div>
      </div>
    {/if}
    {#if refused && !refused.ok}
      <div class="supply glass">
        <p>No hay suficientes preguntas para una partida completa ({refused.available} disponibles):</p>
        <ul>
          {#each refused.levels.filter((l) => l.missing) as l (l.level)}
            <li>Nivel {l.level} (dificultad {l.range[0]}–{l.range[1]}): faltan {l.missing}</li>
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
  .delete:focus-visible {
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
  .danger:focus-visible {
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
  .name-button:focus-visible {
    border-color: var(--sky);
    transform: translateY(calc(-0.3 * var(--u)));
  }
  .name-button kbd {
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
