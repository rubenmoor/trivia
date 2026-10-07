<script lang="ts">
  // The game on the TV (plans/04-ui-tv-display.md, D-21, D-25): a state machine over the
  // screens Start → Player → Level → Select → Question → Correct / Wrong → … → Victory, with one
  // transition routine and the admin overlay on Esc. The server keeps the game (app/server/game.py).
  import { onMount } from "svelte";
  import { fetchGame, gameAction, GameError, playJoker, type GameActionBody } from "../lib/api";
  import type { Game, JokerEvent, Supply } from "../lib/types";
  import { consolation, milestone } from "./copy";
  import Fireworks from "./Fireworks.svelte";
  import Hud from "./Hud.svelte";
  import Icon from "./Icon.svelte";
  import JokerTray from "./JokerTray.svelte";
  import Overlay from "./Overlay.svelte";
  import Player from "./Player.svelte";
  import Question, { type JokerPlay } from "./Question.svelte";
  import { music, sfx, unlock, type Track } from "./sound.svelte";
  import Stage from "./Stage.svelte";
  import { swap } from "./swap";
  import "./theme.css";
  import { FADE_MS, FLIP_MS, GREETING_MS, PICK_MS, TEAR_MS, sleep } from "./timing";
  import Tower from "./Tower.svelte";

  type Screen = "start" | "player" | "level" | "select" | "question" | "correct" | "wrong" | "victory";

  const MUSIC: Record<Screen, Track | null> = {
    start: "normal",
    player: "normal",
    level: "normal",
    select: "normal",
    question: "question",
    correct: "normal", // the fanfare plays at the reveal, then this comes back
    wrong: null,
    victory: "victory", // «Pomp and Circumstance», over the cheers
  };

  let screen = $state<Screen>("start");
  /** The screen before this one: the Level screen drops the new block only after Correct. */
  let previous = $state<Screen | null>(null);
  /** The card just picked on Select (it tears open, the others slide off). */
  let picked = $state<number | null>(null);
  /** The joker that swapped the question on screen in place (Bájale, Cambiazo), for its flip and dial. */
  let swappedBy = $state<JokerEvent | null>(null);
  /** Cards on the table that replaced a skipped or purged one: they deal in with «¡Nueva!» (JK-6). */
  let fresh = $state<Set<number>>(new Set());
  let game = $state<Game | null>(null);
  let supply = $state<Supply | null>(null);
  let error = $state<string | null>(null);
  let loading = $state(true);
  /** The black layer of the transition routine. */
  let black = $state(false);
  /** The veil of the transition: black, or a VHS rewind for «rebobinar» (undo, Francotirador hit). */
  let veil = $state<"black" | "rewind">("black");
  /** A transition or a server call is running: input is ignored. */
  let busy = $state(false);
  let overlayOpen = $state(false);
  /** The first click unlocks audio and autoplay in the browser (04, "Start"). */
  let unlocked = false;
  let questionRef = $state<ReturnType<typeof Question>>();
  let playerRef = $state<ReturnType<typeof Player>>();
  /** The chosen name while «¡Hola, …!» plays (UI-16). */
  let greeting = $state<string | null>(null);
  /** The supply report when the pool can't fill a game for the chosen player. */
  let refused = $state<Supply | null>(null);
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
  /** `apply` runs behind the black: a new game state that the old screen can't show (no question
   * any more, a different `last`) must not land before the screen switches. */
  async function go(next: Screen, effect: string, apply?: () => void) {
    busy = true;
    music(null);
    sfx(effect);
    veil = effect === "rebobinar" ? "rewind" : "black";
    black = true;
    await sleep(FADE_MS);
    apply?.();
    music(MUSIC[next]);
    previous = screen;
    screen = next;
    picked = null;
    swappedBy = null;
    if (next !== "select") fresh = new Set();
    // PLACEHOLDER(UI-7): no preloading of the next screen's media before fading in.
    black = false;
    await sleep(FADE_MS);
    busy = false;
  }

  /** Run a server action; errors show in the corner and leave the screen as it is. */
  async function act(action: Parameters<typeof gameAction>[0], body?: GameActionBody): Promise<boolean> {
    const next = await request(action, body);
    if (next === undefined) return false;
    game = next;
    return true;
  }

  /** A server action without taking its game yet (see `go`); undefined if it failed. */
  async function request(action: Parameters<typeof gameAction>[0], body?: GameActionBody) {
    busy = true;
    try {
      const next = await gameAction(action, body);
      error = null;
      return next;
    } catch (e) {
      error = e instanceof Error ? e.message : String(e);
      if (e instanceof GameError && e.supply) supply = e.supply;
      return undefined;
    } finally {
      busy = false;
    }
  }

  /** Cards on the new table that weren't on the old one (JK-6). */
  function newCards(next: Game | null) {
    const before = game?.options.map((o) => o.description) ?? [];
    return new Set(next?.options.flatMap((o, i) => (before.includes(o.description) ? [] : [i])) ?? []);
  }

  /** A joker goes to the server; errors show in the corner (09-jokers.md). */
  async function playJokerAction(body: JokerPlay) {
    try {
      const res = await playJoker(body);
      error = null;
      return res;
    } catch (e) {
      error = e instanceof Error ? e.message : String(e);
      return null;
    }
  }

  /** The joker is done on the Question screen: Paso goes back to Select, a Francotirador hit to Level. */
  async function jokerPlayed(next: Game, event: JokerEvent) {
    if (event.joker === "easier" || event.joker === "category") {
      // The card flip (JK-7): the transitions in Question.svelte only run while this is set.
      swap.active = true;
      swappedBy = event;
      sfx(event.joker === "easier" ? "silbato que baja" : "swoosh que sube");
      setTimeout(() => (swap.active = false), FLIP_MS * 2 + 100);
    }
    if (event.joker === "skip") {
      const cards = newCards(next);
      await go("select", "papel", () => ((game = next), (fresh = cards)));
    } else if (event.joker === "snipe" && event.outcome === "hit") {
      await go("level", "rebobinar", () => (game = next));
    } else game = next;
  }

  /** After «¡Correcto!»: the Level screen, where the new block drops and lands with a thud. */
  async function toLevel() {
    const level = blocks;
    const landed = sleep(FADE_MS * 2 + 750).then(() => sfx(`bloque ${level}`)); // the fall in Tower.svelte
    await go("level", "whoosh");
    await landed;
  }

  /** Where a game continues: the Level screen before a choice, else its question. */
  function resume() {
    if (game?.phase === "question") return go("question", "swoosh");
    return go("level", game?.level === 1 ? "listo" : "whoosh");
  }

  async function newGame() {
    unlocked = true;
    greeting = null;
    refused = null;
    await go("player", "whoosh");
  }

  /** A name was picked or typed: start the game for that player, greet, then the Level screen. */
  async function choosePlayer(name: string) {
    if (busy) return;
    refused = null;
    const before = supply;
    if (!(await act("new", { player: name }))) {
      if (supply !== before && supply && !supply.ok) refused = supply; // act() stored this player's report
      return;
    }
    greeting = game?.player ?? name;
    sfx("¡hola!");
    busy = true;
    await sleep(GREETING_MS);
    await go("level", "listo");
    greeting = null;
  }

  async function pick(i: number) {
    if (!game || i >= game.options.length) return;
    sfx("pop: carta elegida");
    picked = i;
    setTimeout(() => sfx("papel rasgado"), TEAR_MS);
    const [ok] = await Promise.all([act("pick", { index: i }), sleep(PICK_MS)]);
    if (ok) await go("question", "swoosh");
    else picked = null;
  }

  async function answered(next: Game | null) {
    if (!next) return;
    const apply = () => (game = next);
    if (next.phase === "won") await go("victory", "gran aplausos", apply);
    else if (next.phase === "lost") await go("wrong", "boom", apply);
    else await go("correct", "aplausos", apply);
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

  async function skip(everyone: boolean) {
    overlayOpen = false;
    const next = await request("skip", { everyone });
    if (next === undefined) return;
    const cards = newCards(next);
    await go("select", "papel", () => ((game = next), (fresh = cards)));
  }

  async function undo() {
    overlayOpen = false;
    pausedMedia = [];
    const next = await request("undo");
    if (next !== undefined) await go("question", "rebobinar", () => (game = next));
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
    onclick();
    if (overlayOpen) return overlayRef?.key(e);
    if (screen === "player" && playerRef?.dialogOpen()) return playerRef.key(e);
    if (screen === "question" && !busy && questionRef?.dialogOpen()) return questionRef.key(e);
    if (e.key === "Escape") {
      e.preventDefault();
      return openOverlay();
    }
    if (busy) return;
    const next = e.key === "Enter" || e.key === " ";
    if (screen === "question") return questionRef?.key(e);
    if (screen === "player") return playerRef?.key(e);
    if (screen === "start" && next) {
      e.preventDefault();
      if (running) resume();
      else newGame();
    } else if (screen === "start" && e.key.toLowerCase() === "n") newGame();
    else if (screen === "level" && next) go("select", "papel");
    else if (screen === "select" && picked === null && "1234".includes(e.key) && e.key.length === 1)
      pick(Number(e.key) - 1);
    else if (screen === "correct" && next) toLevel();
    else if ((screen === "wrong" || screen === "victory") && next) toStart();
    else return;
    e.preventDefault();
  }

  /** The first click or key press unlocks audio and autoplay (04, "Start"). */
  function onclick() {
    if (!unlocked) {
      unlocked = true;
      unlock();
      sfx("audio desbloqueado");
    }
  }

  /** /?fuegos=<variant> or ?fuegos=finale plays fireworks over the Start screen (preview, UI-9). */
  const preview = new URLSearchParams(location.search).get("fuegos");

  /** Each card's tilt, within ±3° (10, "Cards"); fixed per game and level, so a re-render keeps it. */
  function tilt(i: number) {
    const seed = ((game?.id ?? 0) * 31 + (game?.level ?? 0) * 7 + i * 13) % 13;
    return (seed / 12) * 6 - 3;
  }
</script>

<svelte:window {onkeydown} {onclick} />

<main class="game">
  {#if loading}
    <Stage />
    <p class="center label">Cargando…</p>
  {:else if screen === "start"}
    <Stage />
    {#if preview}<Fireworks mode={preview === "finale" ? "finale" : "single"} variant={preview} />{/if}
    <section class="start">
      <h1 class="wordmark"><span class="bang">¡</span>Trivia<span class="bang">!</span></h1>
      <p class="subtitle">12 preguntas seguidas para llegar a la cima</p>
      <div class="buttons">
        {#if running}
          <button class="candy breathe" onclick={resume} disabled={busy}>
            Continuar{game?.player ? `: ${game.player}` : ""}, nivel {game?.level} <kbd>Enter</kbd>
          </button>
          <button class="secondary" onclick={newGame} disabled={busy}>Nueva partida <kbd>N</kbd></button>
        {:else}
          <button class="candy breathe" onclick={newGame} disabled={busy}>¡Jugar! <kbd>Enter</kbd></button>
        {/if}
      </div>
      {#if supply && !supply.ok}
        <div class="supply glass">
          <p>No hay suficientes preguntas para una partida completa ({supply.available} disponibles):</p>
          <ul>
            {#each supply.levels.filter((l) => l.missing) as l (l.level)}
              <li>Nivel {l.level} (dificultad {l.range[0]}–{l.range[1]}): faltan {l.missing}</li>
            {/each}
          </ul>
        </div>
      {/if}
    </section>
  {:else if screen === "player"}
    <Stage />
    <Player bind:this={playerRef} {busy} {greeting} {refused} onchoose={choosePlayer} ondeleted={refresh} />
  {:else if screen === "level" && game}
    <Stage />
    <div class="corner-hud">{#if game.player}<span class="chip glass">{game.player}</span>{/if}</div>
    <aside class="side-tray"><JokerTray readonly /></aside>
    <section class="level">
      <Tower filled={blocks} drop={previous === "correct"} />
      <div class="level-text">
        <p class="kicker">Nivel</p>
        <h1 class="title big">{game.level} <span class="of">de 12</span></h1>
        {#if game.repeat}
          <p class="milestone again">¡Otra vez! Le dieron a la correcta.</p>
        {:else if milestone(game.level, game.id)}
          <p class="milestone">{milestone(game.level, game.id)}</p>
        {/if}
        <p class="hint label"><kbd>Enter</kbd> para seguir</p>
      </div>
    </section>
  {:else if screen === "select" && game}
    <Stage />
    <div class="corner-hud"><Hud level={game.level} player={game.player} /></div>
    <aside class="side-tray"><JokerTray readonly /></aside>
    <section class="select">
      <h2 class="title">Elijan una pregunta</h2>
      {#if game.options.length === 0}
        <p class="error-box">No quedan preguntas para este nivel. <kbd>Esc</kbd> → Volver al inicio.</p>
      {/if}
      <div class="cards">
        {#each game.options as option, i (i)}
          <button
            class="card"
            class:chosen={picked === i}
            class:gone={picked !== null && picked !== i}
            class:fresh={fresh.has(i)}
            style:--tilt="{tilt(i)}deg"
            style:--deal-delay="{i * 0.12}s"
            onclick={() => picked === null && pick(i)}
            disabled={busy}
          >
            <span class="flap"></span>
            <span class="seal">{i + 1}</span>
            {#if picked === i}
              <span class="tear"></span>
              <span class="letter-slot"><span class="letter">?</span></span>
            {/if}
            {#if fresh.has(i)}<span class="new-badge">¡Nueva!</span>{/if}
            <span class="description">{option.description}</span>
          </button>
        {/each}
      </div>
    </section>
  {:else if screen === "question" && game?.question}
    {#key game.question.id}
      <Question
        bind:this={questionRef}
        question={game.question}
        level={game.level}
        playerName={game.player}
        paused={overlayOpen}
        jokers={game.jokers}
        {swappedBy}
        play={playJokerAction}
        onplayed={jokerPlayed}
        onanswered={answered}
      />
    {/key}
  {:else if screen === "correct" && game?.last}
    <Stage mood="correct" />
    <section class="result">
      <Fireworks />
      <h1 class="title good">¡Correcto!</h1>
      <div class="panel glass">
        <p class="answer"><span class="badge good-badge"><Icon name="check" /></span>{game.last.answer}</p>
        <p class="fun-fact">{game.last.fun_fact}</p>
      </div>
      <p class="hint label"><kbd>Enter</kbd> para seguir</p>
    </section>
  {:else if screen === "wrong" && game?.last}
    <Stage mood="wrong" />
    <section class="result wrong">
      <div class="columns">
        <Tower filled={blocks} small crumble />
        <div class="stack">
          <h1 class="title bad">¡Oh no!</h1>
          <div class="panel glass">
            <p class="label">La respuesta correcta era</p>
            <p class="answer"><span class="badge good-badge"><Icon name="check" /></span>{game.last.answer}</p>
            <p class="fun-fact">{game.last.fun_fact}</p>
          </div>
          <p class="consolation">{consolation(game.level, game.id)}</p>
        </div>
      </div>
      <button class="candy" onclick={toStart} disabled={busy}>Volver al inicio <kbd>Enter</kbd></button>
    </section>
  {:else if screen === "victory" && game}
    <Stage mood="victory" />
    <Fireworks mode="finale" />
    <section class="result victory">
      <Tower filled={12} drop />
      <div class="stack">
        <h1 class="title big gold">¡Ganaron!</h1>
        {#if game.player}<p class="milestone">¡{game.player} llegó a la cima!</p>{/if}
        {#if game.last}
          <div class="panel glass">
            <p class="answer"><span class="badge good-badge"><Icon name="check" /></span>{game.last.answer}</p>
            <p class="fun-fact">{game.last.fun_fact}</p>
          </div>
        {/if}

        <button class="candy breathe" onclick={toStart} disabled={busy}>Volver al inicio <kbd>Enter</kbd></button>
      </div>
    </section>
  {:else}
    <Stage />
    <p class="center">Esta pantalla no tiene datos. <kbd>Esc</kbd> → Volver al inicio.</p>
  {/if}

  {#if error}
    <div class="error-box corner">{error}</div>
  {/if}

  <div class="black {veil}" class:on={black} style:transition-duration="{FADE_MS}ms">
    {#if veil === "rewind"}<span class="rewind-mark">◀◀</span>{/if}
  </div>

  {#if overlayOpen}
    <Overlay
      bind:this={overlayRef}
      questionId={screen === "question" && game?.question ? game.question.id : (game?.last?.question_id ?? null)}
      questionLabel={screen === "question" ? "pregunta" : "última pregunta"}
      canSkip={screen === "question" && !questionBusy()}
      canUndo={!!game?.can_undo && !questionBusy()}
      canRestart={running || screen !== "start"}
      onclose={closeOverlay}
      onskip={() => skip(false)}
      onskipall={() => skip(true)}
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
  }
  section {
    position: absolute;
    inset: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: calc(1.4 * var(--u));
    padding: var(--safe-y) var(--safe-x);
    text-align: center;
  }
  p {
    margin: 0;
  }

  /* Start */
  .wordmark {
    margin: 0;
    font-family: var(--font-display);
    font-size: calc(11 * var(--u));
    font-weight: 800;
    line-height: 1;
    color: var(--paper);
    text-shadow:
      0 calc(0.4 * var(--u)) 0 var(--slate-600),
      0 calc(0.8 * var(--u)) calc(2.5 * var(--u)) rgba(0, 0, 0, 0.5);
    animation: arrive 0.9s var(--spring) backwards;
  }
  .bang {
    display: inline-block;
    color: var(--amber);
    animation: bob 3s ease-in-out infinite;
  }
  .bang:last-child {
    animation-delay: -1.5s;
  }
  .subtitle {
    font-size: calc(1.6 * var(--u));
    color: var(--slate-200);
  }
  .buttons {
    display: flex;
    align-items: center;
    gap: calc(1.6 * var(--u));
    margin-top: calc(2 * var(--u));
  }
  .supply {
    padding: calc(1 * var(--u)) calc(1.6 * var(--u));
    font-size: calc(1.1 * var(--u));
    color: var(--amber);
    text-align: left;
  }
  .supply ul {
    margin: calc(0.4 * var(--u)) 0 0;
  }

  /* Level */
  .corner-hud {
    position: absolute;
    top: var(--safe-y);
    left: var(--safe-x);
    z-index: 1;
  }
  .side-tray {
    position: absolute;
    left: var(--safe-x);
    top: 50%;
    transform: translateY(-50%);
    z-index: 1;
  }
  .milestone.again {
    color: var(--coral);
  }
  .chip {
    display: inline-block;
    padding: calc(0.35 * var(--u)) calc(1 * var(--u));
    border-radius: calc(0.9 * var(--u));
    font-family: var(--font-display);
    font-size: calc(1.1 * var(--u));
    font-weight: 700;
    color: var(--slate-200);
  }
  .level {
    flex-direction: row;
    justify-content: space-evenly;
  }
  .level-text {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: calc(0.8 * var(--u));
    min-width: calc(34 * var(--u));
  }
  .kicker {
    font-family: var(--font-display);
    font-size: calc(1.8 * var(--u));
    color: var(--slate-200);
    letter-spacing: 0.2em;
    text-transform: uppercase;
  }
  .big {
    font-size: calc(7 * var(--u));
    color: var(--amber);
    animation: arrive 0.7s 0.3s var(--spring) backwards;
  }
  .of {
    font-size: 0.45em;
    color: var(--slate-200);
  }
  .milestone {
    font-family: var(--font-display);
    font-size: calc(2 * var(--u));
    font-weight: 700;
    color: var(--sky);
    animation: arrive 0.7s 0.9s var(--spring) backwards;
  }
  .hint {
    margin-top: calc(1.5 * var(--u));
  }

  /* Select: paper envelopes on the night table (VD-5, UI-11) */
  .cards {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: calc(2 * var(--u));
    width: 100%;
    max-width: calc(100 * var(--u));
    margin: calc(2 * var(--u)) 0;
  }
  .card {
    /* The torn edge of the flap, shared by the flap and what it leaves behind */
    --ragged: polygon(
      0 0, 100% 0, 100% 88%, 94% 100%, 88% 86%, 81% 98%, 75% 84%, 68% 97%, 62% 87%, 55% 100%, 49% 85%,
      43% 96%, 37% 84%, 30% 99%, 24% 86%, 18% 97%, 11% 85%, 5% 98%, 0 88%
    );
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: calc(1.2 * var(--u));
    min-height: calc(26 * var(--u));
    padding: calc(5 * var(--u)) calc(1.4 * var(--u)) calc(2 * var(--u));
    border: none;
    border-radius: calc(0.8 * var(--u));
    background: var(--cream);
    color: var(--ink);
    font-size: calc(1.6 * var(--u));
    font-weight: 700;
    line-height: 1.3;
    box-shadow:
      0 calc(0.4 * var(--u)) 0 #d9cfb6,
      0 calc(1.2 * var(--u)) calc(2.4 * var(--u)) rgba(0, 0, 0, 0.45);
    transform: rotate(var(--tilt));
    transition:
      transform 0.3s var(--spring),
      opacity 0.3s;
    animation: deal 0.6s var(--deal-delay) var(--spring) backwards;
  }
  /* The envelope flap, on a strip of paper with a ragged lower edge that tears off when picked */
  .flap {
    position: absolute;
    inset: 0 0 auto;
    height: calc(6.6 * var(--u));
    background: var(--cream);
    border-radius: calc(0.8 * var(--u)) calc(0.8 * var(--u)) 0 0;
    clip-path: var(--ragged);
    z-index: 1;
  }
  .flap::before {
    content: "";
    position: absolute;
    inset: 0 0 auto;
    height: calc(6 * var(--u));
    background: linear-gradient(to bottom, #e8dcc0, #efe4cb);
    clip-path: polygon(0 0, 100% 0, 50% 100%);
  }
  /* What the torn flap leaves behind: the shadowed inside of the envelope, with the same ragged edge */
  .tear {
    position: absolute;
    inset: 0 0 auto;
    height: calc(6.6 * var(--u));
    background: linear-gradient(to bottom, #6b5d45, #b9ab8a 70%, #d9cfb6);
    clip-path: var(--ragged);
    animation: tear-show 0.15s 0.3s backwards;
  }
  /* The letter slides up out of the open envelope; the slot hides it below the card's top edge. */
  .letter-slot {
    position: absolute;
    left: 14%;
    right: 14%;
    bottom: calc(100% - 3 * var(--u));
    height: calc(11 * var(--u));
    overflow: hidden;
  }
  .letter {
    position: absolute;
    inset: 0;
    display: grid;
    place-items: center;
    border-radius: calc(0.4 * var(--u)) calc(0.4 * var(--u)) 0 0;
    background: repeating-linear-gradient(to bottom, #fffaf0 0 calc(1.6 * var(--u)), #e6dcc6 0 calc(1.7 * var(--u)));
    color: var(--seal);
    font-family: var(--font-display);
    font-size: calc(5 * var(--u));
    font-weight: 800;
    box-shadow: 0 0 calc(1 * var(--u)) rgba(0, 0, 0, 0.3);
    transform: translateY(100%);
    animation: letter-up 0.4s 0.58s var(--spring) forwards;
  }
  .seal {
    position: absolute;
    z-index: 2;
    top: calc(3.6 * var(--u));
    left: 50%;
    translate: -50% 0;
    display: grid;
    place-items: center;
    width: calc(4.4 * var(--u));
    height: calc(4.4 * var(--u));
    border-radius: 50%;
    background: radial-gradient(circle at 35% 30%, #e0584a, var(--seal) 60%, #8e2a20);
    color: var(--amber);
    font-family: var(--font-display);
    font-size: calc(2.2 * var(--u));
    font-weight: 800;
    box-shadow: 0 calc(0.2 * var(--u)) calc(0.4 * var(--u)) rgba(0, 0, 0, 0.35);
  }
  .description {
    margin-top: calc(2.4 * var(--u));
  }
  .card.fresh {
    box-shadow:
      0 calc(0.4 * var(--u)) 0 #d9cfb6,
      0 0 calc(2.4 * var(--u)) rgba(76, 201, 240, 0.7);
    animation-delay: calc(var(--deal-delay) + 0.5s);
  }
  .new-badge {
    position: absolute;
    top: calc(-1 * var(--u));
    right: calc(-1 * var(--u));
    padding: calc(0.2 * var(--u)) calc(0.8 * var(--u));
    border-radius: calc(0.8 * var(--u));
    background: var(--sky);
    color: var(--night-900);
    font-family: var(--font-display);
    font-size: calc(1.3 * var(--u));
    font-weight: 800;
    transform: rotate(8deg);
    box-shadow: 0 calc(0.2 * var(--u)) calc(0.6 * var(--u)) rgba(0, 0, 0, 0.4);
  }
  .card:hover:not(:disabled),
  .card:focus-visible {
    transform: translateY(calc(-1.2 * var(--u))) rotate(0deg) scale(1.03);
    outline: calc(0.25 * var(--u)) solid var(--sky);
  }
  .card.chosen {
    z-index: 1;
    animation: chosen 0.5s var(--spring) forwards;
  }
  /* Tear-open (UI-11, TEAR_MS): the seal cracks off, then the flap rips away to the upper right. */
  .card.chosen .seal {
    animation: seal-crack 0.4s 0.1s ease-in forwards;
  }
  .card.chosen .flap {
    transform-origin: 0 100%;
    animation: flap-off 0.45s 0.3s ease-in forwards;
  }
  .card.gone {
    animation: gone 0.4s ease-in forwards;
  }
  @keyframes deal {
    from {
      opacity: 0;
      transform: translateY(-60vh) rotate(calc(var(--tilt) * -6));
    }
  }
  @keyframes chosen {
    40% {
      transform: rotate(0deg) scale(1.12);
    }
    to {
      transform: rotate(0deg) scale(1.06);
      box-shadow: 0 0 calc(3 * var(--u)) var(--amber);
    }
  }
  @keyframes seal-crack {
    30% {
      transform: scale(1.25) rotate(-12deg);
    }
    to {
      opacity: 0;
      transform: translate(calc(-6 * var(--u)), calc(-10 * var(--u))) scale(0.9) rotate(-70deg);
    }
  }
  @keyframes flap-off {
    20% {
      transform: rotate(-4deg);
    }
    to {
      opacity: 0;
      transform: translate(calc(14 * var(--u)), calc(-16 * var(--u))) rotate(28deg);
    }
  }
  @keyframes tear-show {
    from {
      opacity: 0;
    }
  }
  @keyframes letter-up {
    to {
      transform: translateY(30%);
    }
  }
  @keyframes gone {
    to {
      opacity: 0;
      transform: translateY(40vh) rotate(calc(var(--tilt) * 4));
    }
  }

  /* Results */
  .panel {
    max-width: calc(64 * var(--u));
    padding: calc(1.4 * var(--u)) calc(2.4 * var(--u));
    display: flex;
    flex-direction: column;
    gap: calc(0.6 * var(--u));
    animation: arrive 0.6s 0.25s var(--spring) backwards;
  }
  .result .answer {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: calc(0.8 * var(--u));
    font-family: var(--font-display);
    font-size: calc(2.6 * var(--u));
    font-weight: 800;
  }
  .good-badge {
    display: grid;
    place-items: center;
    width: calc(2.6 * var(--u));
    height: calc(2.6 * var(--u));
    border-radius: 50%;
    background: var(--mint);
    color: var(--night-900);
    font-size: calc(1.6 * var(--u));
  }
  .fun-fact {
    font-size: calc(1.5 * var(--u));
    color: var(--slate-200);
  }
  .result .title {
    animation: arrive 0.6s var(--spring) backwards;
  }
  .good {
    color: var(--mint);
  }
  .bad {
    color: var(--coral);
  }
  .gold {
    color: var(--amber);
  }
  .columns {
    display: flex;
    align-items: center;
    gap: calc(4 * var(--u));
  }
  .stack {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: calc(1.4 * var(--u));
  }
  .victory {
    flex-direction: row;
    justify-content: space-evenly;
  }
  .consolation {
    max-width: calc(56 * var(--u));
    font-family: var(--font-display);
    font-size: calc(2 * var(--u));
    font-weight: 600;
    color: var(--paper);
    animation: arrive 0.6s 1.2s var(--spring) backwards;
  }

  .center {
    position: absolute;
    inset: 0;
    display: grid;
    place-items: center;
  }
  .error-box {
    color: var(--coral);
    background: rgba(40, 10, 18, 0.9);
    border: 1px solid var(--coral);
    border-radius: calc(0.6 * var(--u));
    padding: calc(0.5 * var(--u)) calc(1 * var(--u));
    font-size: calc(1.1 * var(--u));
  }
  .corner {
    position: fixed;
    top: var(--safe-y);
    right: var(--safe-x);
    max-width: 40vw;
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
  /* VHS rewind (09, "Francotirador"): scanlines rushing up, a jittering ◀◀. */
  .black.rewind {
    display: grid;
    place-items: center;
    background:
      repeating-linear-gradient(rgba(238, 241, 246, 0.07) 0 2px, transparent 2px 6px),
      linear-gradient(rgba(76, 201, 240, 0.12), rgba(255, 84, 112, 0.12)),
      var(--night-900);
    background-size:
      100% 6px,
      100% 100%,
      100% 100%;
    animation: scan 0.25s linear infinite;
  }
  .rewind-mark {
    font-family: var(--font-display);
    font-size: calc(9 * var(--u));
    font-weight: 800;
    color: var(--paper);
    text-shadow:
      calc(0.4 * var(--u)) 0 rgba(255, 84, 112, 0.8),
      calc(-0.4 * var(--u)) 0 rgba(76, 201, 240, 0.8);
    animation: jitter 0.18s steps(2) infinite;
  }
  @keyframes scan {
    to {
      background-position:
        0 -60px,
        0 0,
        0 0;
    }
  }
  @keyframes jitter {
    50% {
      transform: translate(calc(0.3 * var(--u)), calc(-0.2 * var(--u))) skewX(-6deg);
    }
  }

  @keyframes arrive {
    from {
      opacity: 0;
      transform: translateY(calc(2 * var(--u))) scale(0.94);
    }
  }
  @keyframes bob {
    50% {
      transform: translateY(calc(-0.6 * var(--u))) rotate(-6deg);
    }
  }
</style>
