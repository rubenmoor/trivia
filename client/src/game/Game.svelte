<script lang="ts">
  // The game on the TV (plans/04-ui-tv-display.md, D-21, D-25): a state machine over the
  // screens Start → Level → Select → Question → Correct / Wrong → … → Victory, with one
  // transition routine and the admin overlay on Esc. The server keeps the game (server/game.py).
  import { onMount } from "svelte";
  import { fetchGame, gameAction, GameError, type GameActionBody } from "../lib/api";
  import type { Game, Supply } from "../lib/types";
  import Captions from "./Captions.svelte";
  import Overlay from "./Overlay.svelte";
  import Placeholder from "./Placeholder.svelte";
  import Question from "./Question.svelte";
  import { music, sfx, type Track } from "./sound.svelte";
  import { FADE_MS, sleep } from "./timing";
  import Tower from "./Tower.svelte";

  type Screen = "start" | "level" | "select" | "question" | "correct" | "wrong" | "victory";

  const MUSIC: Record<Screen, Track | null> = {
    start: "normal",
    level: "normal",
    select: "normal",
    question: "question",
    correct: "normal", // PLACEHOLDER(UI-8): the fanfare plays over it at the reveal
    wrong: null,
    victory: null, // the victory jingle is an effect
  };

  let screen = $state<Screen>("start");
  let game = $state<Game | null>(null);
  let supply = $state<Supply | null>(null);
  let error = $state<string | null>(null);
  let loading = $state(true);
  /** The black layer of the transition routine. */
  let black = $state(false);
  /** A transition or a server call is running: input is ignored. */
  let busy = $state(false);
  let overlayOpen = $state(false);
  /** The first click unlocks audio and autoplay in the browser (04, "Start"). */
  let unlocked = false;
  let questionRef = $state<ReturnType<typeof Question>>();
  let overlayRef = $state<ReturnType<typeof Overlay>>();
  /** Media that was playing when the overlay opened; it resumes on close. */
  let pausedMedia: HTMLMediaElement[] = [];

  const running = $derived(game !== null && game.result === null);
  /** Blocks on the tower: correct answers in this game. */
  const blocks = $derived(game?.history.filter((h) => h.correct).length ?? 0);

  onMount(() => {
    music(MUSIC.start);
    refresh();
  });

  async function refresh() {
    try {
      ({ game, supply } = await fetchGame());
      error = null;
    } catch (e) {
      error = e instanceof Error ? e.message : String(e);
    } finally {
      loading = false;
    }
  }

  /** The transition routine (04, "Transitions"): effect, fade to black, switch, fade in, music. */
  async function go(next: Screen, effect: string) {
    busy = true;
    music(null);
    sfx(effect);
    black = true;
    await sleep(FADE_MS);
    music(MUSIC[next]);
    screen = next;
    // PLACEHOLDER(UI-7): no preloading of the next screen's media before fading in.
    black = false;
    await sleep(FADE_MS);
    busy = false;
  }

  /** Run a server action; errors show in the corner and leave the screen as it is. */
  async function act(action: Parameters<typeof gameAction>[0], body?: GameActionBody): Promise<boolean> {
    busy = true;
    try {
      game = await gameAction(action, body);
      error = null;
      return true;
    } catch (e) {
      error = e instanceof Error ? e.message : String(e);
      if (e instanceof GameError && e.supply) supply = e.supply;
      return false;
    } finally {
      busy = false;
    }
  }

  /** Where a game continues: the Level screen before a choice, else its question. */
  function resume() {
    if (game?.phase === "question") return go("question", "swoosh");
    return go("level", game?.level === 1 ? "listo" : "whoosh");
  }

  async function newGame() {
    unlocked = true;
    // PLACEHOLDER(UI-16): no Player screen yet; every game is played as «Familia».
    if (await act("new", { player: "Familia" })) await go("level", "whoosh");
  }

  async function pick(i: number) {
    if (!game || i >= game.options.length) return;
    sfx("pop: carta elegida");
    if (await act("pick", { index: i })) await go("question", "swoosh");
  }

  async function answered(next: Game | null) {
    game = next;
    if (!game) return;
    if (game.phase === "won") await go("victory", "boom");
    else if (game.phase === "lost") await go("wrong", "boom");
    else await go("correct", "boom");
  }

  async function toStart() {
    await refresh();
    await go("start", "whoosh");
  }

  // Admin overlay ---------------------------------------------------------------------------

  function openOverlay() {
    overlayOpen = true;
    sfx("menú abierto");
    pausedMedia = [...document.querySelectorAll<HTMLMediaElement>("audio, video")].filter((m) => !m.paused);
    pausedMedia.forEach((m) => m.pause());
  }

  function closeOverlay() {
    overlayOpen = false;
    sfx("menú cerrado");
    pausedMedia.forEach((m) => m.play().catch(() => {}));
    pausedMedia = [];
  }

  async function skip() {
    overlayOpen = false;
    if (await act("skip")) await go("select", "papel");
  }

  async function undo() {
    overlayOpen = false;
    pausedMedia = [];
    if (await act("undo")) await go("question", "rebobinar");
  }

  async function restart() {
    overlayOpen = false;
    pausedMedia = [];
    await act("abandon");
    await toStart();
  }

  /** The question's final answer is out: skip and undo would race the reveal. */
  const questionBusy = () => screen === "question" && (questionRef?.busy() ?? false);

  // Keyboard (04, "Input") ------------------------------------------------------------------

  function onkeydown(e: KeyboardEvent) {
    if (e.repeat) return;
    if (overlayOpen) return overlayRef?.key(e);
    if (e.key === "Escape") {
      e.preventDefault();
      return openOverlay();
    }
    if (busy) return;
    const next = e.key === "Enter" || e.key === " ";
    if (screen === "question") return questionRef?.key(e);
    if (screen === "start" && next) {
      e.preventDefault();
      if (running) resume();
      else newGame();
    } else if (screen === "start" && e.key.toLowerCase() === "n") newGame();
    else if (screen === "level" && next) go("select", "papel");
    else if (screen === "select" && "1234".includes(e.key) && e.key.length === 1) pick(Number(e.key) - 1);
    else if (screen === "correct" && next) go("level", "whoosh");
    else if ((screen === "wrong" || screen === "victory") && next) toStart();
    else return;
    e.preventDefault();
  }

  function onclick() {
    if (!unlocked) {
      unlocked = true; // PLACEHOLDER(UI-8): this is where the AudioContext gets resumed
      sfx("audio desbloqueado");
    }
  }

  // UI-14: final Spanish copy for milestones and consolation.
  function milestone(level: number) {
    if (level === 6) return "¡Ya vamos por la mitad!"; // PLACEHOLDER(UI-14)
    if (level === 4 || level === 8) return "¡Cada vez más alto!"; // PLACEHOLDER(UI-14)
    return null;
  }
</script>

<svelte:window {onkeydown} {onclick} />

<main class="game">
  {#if loading}
    <p class="center">Cargando…</p>
  {:else if screen === "start"}
    <section class="start">
      <!-- PLACEHOLDER(UI-1): no visual style or idle animation yet. -->
      <h1>Trivia</h1>
      <p class="subtitle">12 preguntas seguidas para ganar</p>
      <div class="buttons">
        {#if running}
          <button class="primary" onclick={resume} disabled={busy}>Continuar (nivel {game?.level}) <kbd>Enter</kbd></button>
          <button onclick={newGame} disabled={busy}>Nueva partida <kbd>N</kbd></button>
        {:else}
          <button class="primary" onclick={newGame} disabled={busy}>¡Jugar! <kbd>Enter</kbd></button>
        {/if}
      </div>
      {#if supply && !supply.ok}
        <div class="supply">
          <p>No hay suficientes preguntas para una partida completa ({supply.available} disponibles):</p>
          <ul>
            {#each supply.levels.filter((l) => l.missing) as l (l.level)}
              <li>Nivel {l.level} (dificultad {l.range[0]}–{l.range[1]}): faltan {l.missing}</li>
            {/each}
          </ul>
        </div>
      {/if}
      <Placeholder task="UI-1" label="estilo visual, título y animación de espera" chip />
    </section>
  {:else if screen === "level" && game}
    <section class="level">
      <Tower filled={blocks} />
      <div class="level-text">
        <h1>Nivel {game.level} de 12</h1>
        {#if milestone(game.level)}<p class="milestone">{milestone(game.level)}</p>{/if}
        <p class="hint"><kbd>Enter</kbd> para seguir</p>
      </div>
    </section>
  {:else if screen === "select" && game}
    <section class="select">
      <h2>Nivel {game.level}: elijan una pregunta</h2>
      {#if game.options.length === 0}
        <p class="error-box">No quedan preguntas para este nivel. <kbd>Esc</kbd> → Volver al inicio.</p>
      {/if}
      <div class="cards">
        {#each game.options as option, i (i)}
          <!-- PLACEHOLDER(UI-11): plain cards; no envelopes, tilt, deal-in or tear-open. -->
          <button class="card" onclick={() => pick(i)} disabled={busy}>
            <span class="number">{i + 1}</span>
            <span>{option.description}</span>
          </button>
        {/each}
      </div>
      <Placeholder task="UI-11" label="cartas sencillas, sin diseño ni animación" chip />
    </section>
  {:else if screen === "question" && game?.question}
    {#key game.question.id}
      <Question
        bind:this={questionRef}
        question={game.question}
        level={game.level}
        paused={overlayOpen}
        onanswered={answered}
      />
    {/key}
  {:else if screen === "correct" && game?.last}
    <section class="result">
      <!-- PLACEHOLDER(UI-9): fireworks overlay. -->
      <Placeholder task="UI-9" label="🎆 fuegos artificiales" />
      <h1 class="good">¡Correcto!</h1>
      <p class="answer">{game.last.answer}</p>
      <p class="fun-fact">{game.last.fun_fact}</p>
      <p class="hint"><kbd>Enter</kbd> para seguir</p>
    </section>
  {:else if screen === "wrong" && game?.last}
    <section class="result wrong">
      <!-- PLACEHOLDER(UI-4): desaturate, vignette, crumbling tower. -->
      <Placeholder task="UI-4" label="animación oscura: la torre se derrumba" />
      <div class="columns">
        <Tower filled={blocks} small />
        <div>
          <h1 class="bad">¡Oh no!</h1>
          <p>La respuesta correcta era</p>
          <p class="answer">{game.last.answer}</p>
          <p class="fun-fact">{game.last.fun_fact}</p>
          <!-- PLACEHOLDER(UI-14): several consolation messages per level band. -->
          <p class="consolation">¡Llegaron al nivel {game.level}!</p>
          <Placeholder task="UI-14" label="mensaje de consuelo" chip />
        </div>
      </div>
      <button class="primary" onclick={toStart} disabled={busy}>Volver al inicio <kbd>Enter</kbd></button>
    </section>
  {:else if screen === "victory" && game}
    <section class="result victory">
      <Tower filled={12} />
      <div class="stack">
        <h1 class="good">¡Ganaron!</h1>
        {#if game.last}<p class="fun-fact">{game.last.answer}: {game.last.fun_fact}</p>{/if}
        <!-- PLACEHOLDER(UI-4, UI-9): crown, long fireworks finale, victory jingle. -->
        <Placeholder task="UI-4 · UI-9" label="👑 corona y gran final de fuegos artificiales" />
        <button class="primary" onclick={toStart} disabled={busy}>Volver al inicio <kbd>Enter</kbd></button>
      </div>
    </section>
  {:else}
    <p class="center">Esta pantalla no tiene datos. <kbd>Esc</kbd> → Volver al inicio.</p>
  {/if}

  {#if error}
    <div class="error-box corner">{error}</div>
  {/if}

  <div class="black" class:on={black} style:transition-duration="{FADE_MS}ms"></div>
  <Captions />

  {#if overlayOpen}
    <Overlay
      bind:this={overlayRef}
      questionId={screen === "question" && game?.question ? game.question.id : (game?.last?.question_id ?? null)}
      questionLabel={screen === "question" ? "pregunta" : "última pregunta"}
      canSkip={screen === "question" && !questionBusy()}
      canUndo={!!game?.can_undo && !questionBusy()}
      canRestart={running || screen !== "start"}
      onclose={closeOverlay}
      onskip={skip}
      onundo={undo}
      onrestart={restart}
    />
  {/if}
</main>

<style>
  .game {
    position: fixed;
    inset: 0;
    overflow: hidden;
    font-size: 1.6vw;
  }
  section {
    position: absolute;
    inset: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 2vh;
    padding: 4vh 5vw;
    text-align: center;
  }
  h1 {
    margin: 0;
    font-size: 5vw;
  }
  h2 {
    margin: 0;
    font-size: 3vw;
  }
  kbd {
    font-size: 0.6em;
    opacity: 0.6;
  }
  button {
    font: inherit;
    color: var(--text);
    cursor: pointer;
  }
  button:disabled {
    cursor: default;
  }
  .buttons {
    display: flex;
    gap: 2vw;
    margin: 3vh 0;
  }
  .buttons button,
  .result button {
    font-size: 2.2vw;
    padding: 1.5vh 3vw;
    border-radius: 1vw;
    border: 0.25vw solid rgba(255, 255, 255, 0.2);
    background: var(--panel);
  }
  button.primary {
    background: var(--accent);
    border-color: var(--accent);
    color: #1a1a1a;
    font-weight: 800;
  }
  .subtitle,
  .hint {
    color: var(--muted);
  }
  .supply {
    color: var(--warn);
    font-size: 1.3vw;
    text-align: left;
  }
  .level {
    flex-direction: row;
    justify-content: space-evenly;
  }
  .level-text h1 {
    font-size: 6vw;
  }
  .milestone {
    font-size: 2.4vw;
    color: var(--accent);
  }
  .cards {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 2vw;
    width: 100%;
    margin: 3vh 0;
  }
  .card {
    display: flex;
    flex-direction: column;
    gap: 2vh;
    min-height: 38vh;
    padding: 3vh 1.5vw;
    border: 0.25vw solid rgba(255, 255, 255, 0.15);
    border-radius: 1.2vw;
    background: #f3ead6;
    color: #2b2116;
    font-size: 1.9vw;
    text-align: center;
    transition: transform 0.2s;
  }
  .card:hover {
    transform: translateY(-1.5vh);
  }
  .number {
    font-size: 3.5vw;
    font-weight: 800;
    color: #b0452b;
  }
  .result .answer {
    margin: 0;
    font-size: 3.4vw;
    font-weight: 800;
  }
  .fun-fact {
    max-width: 60vw;
    font-size: 1.9vw;
  }
  .good {
    color: var(--good);
  }
  .bad {
    color: var(--bad);
  }
  .wrong {
    background: radial-gradient(circle, #1d2030, #07070b 80%);
  }
  .columns {
    display: flex;
    align-items: center;
    gap: 5vw;
  }
  .stack {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 3vh;
  }
  .victory {
    flex-direction: row;
    justify-content: space-evenly;
  }
  .consolation {
    font-size: 2.2vw;
  }
  .center {
    position: absolute;
    inset: 0;
    display: grid;
    place-items: center;
  }
  .error-box {
    color: var(--bad);
    background: rgba(40, 10, 12, 0.9);
    border: 0.12rem solid var(--bad);
    border-radius: 0.5rem;
    padding: 0.5rem 1rem;
  }
  .corner {
    position: fixed;
    top: 1rem;
    right: 1rem;
    max-width: 40vw;
    font-size: 1rem;
    z-index: 35;
  }
  .black {
    position: fixed;
    inset: 0;
    background: #000;
    opacity: 0;
    pointer-events: none;
    transition-property: opacity;
    z-index: 20;
  }
  .black.on {
    opacity: 1;
    pointer-events: all;
  }
</style>
