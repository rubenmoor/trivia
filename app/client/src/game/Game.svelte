<script lang="ts">
  // The game on the TV (plans/04-ui-tv-display.md, D-21, D-25): a state machine over the
  // screens Start → Player → Choice → Level → Select → Question → Correct / Wrong → … → Victory, with one
  // transition routine and the admin overlay on Esc. The engine keeps the game (engine/, lib/api.ts).
  import { onDestroy, onMount, tick } from "svelte";
  import { fetchFlags, fetchGame, gameAction, GameError, noteExhausted, playJoker, setFlag, type GameActionBody } from "../lib/api";
  import { steam } from "../lib/desktop";
  import { language, saveError, takeSaveNotice } from "../lib/engine";
  import { errorText } from "../lib/errors";
  import { t } from "../lib/i18n";
  import { listenPads } from "../lib/gamepad.svelte";
  import { listen, pushScope, type Action } from "../lib/input.svelte";
  import { questionLocale } from "../lib/names.svelte";
  import type { Game, GameMode, JokerBudget, JokerEvent, Flagged, Supply } from "../lib/types";
  import Choice from "./Choice.svelte";
  import { consolation, milestone } from "./copy";
  import Fireworks from "./Fireworks.svelte";
  import FlagDialog from "./FlagDialog.svelte";
  import FlagList from "./FlagList.svelte";
  import Hud from "./Hud.svelte";
  import Icon from "./Icon.svelte";
  import Prompt from "./Prompt.svelte";
  import JokerTray from "./JokerTray.svelte";
  import { levelsOf, onTwelve } from "./levels";
  import LanguageScreen from "./LanguageScreen.svelte";
  import Overlay from "./Overlay.svelte";
  import Player from "./Player.svelte";
  import Question, { type JokerPlay } from "./Question.svelte";
  import { music, sfx, unlock, type Cue, type Track } from "./sound.svelte";
  import Stage from "./Stage.svelte";
  import SupplyReport from "./SupplyReport.svelte";
  import { swap } from "./swap";
  import "./theme.css";
  import { FADE_MS, FLIP_MS, GREETING_MS, PICK_MS, PRELOAD_MAX_MS, TEAR_MS, sleep } from "./timing";
  import Tower from "./Tower.svelte";

  type Screen = "language" | "start" | "player" | "choice" | "level" | "select" | "question" | "correct" | "wrong" | "victory";

  const MUSIC: Record<Screen, Track | null> = {
    language: "normal",
    start: "normal",
    player: "normal",
    choice: "normal",
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
  let main = $state<HTMLElement>();
  /** The chosen name while «¡Hola, …!» plays (UI-16). */
  let greeting = $state<string | null>(null);
  /** The name picked on Player, for the Choice screen. */
  let chosen = $state<string | null>(null);
  /** Why `new` refused the Choice screen's choice (plan 29). */
  let refused = $state<GameError | null>(null);
  /** The save file was unusable and moved to a backup (plan 55): shown once on Start. */
  let notice = $state<ReturnType<typeof takeSaveNotice>>(null);
  /** Media that was playing when the overlay opened; it resumes on close. */
  let pausedMedia: HTMLMediaElement[] = [];

  /** Questions flagged for review (GM-5, decision 60); `trivia-authoring` turns them into reviews. */
  let flags = $state<Flagged[]>([]);
  const flagged = $derived(new Set(flags.map((f) => f.question_id)));
  /** The flag dialog is open (flag icon, M). */
  let flagOpen = $state(false);
  let flagBusy = $state(false);
  /** «Preguntas marcadas» opens over the overlay, so the screen below stays mounted. */
  let flagListOpen = $state(false);

  const running = $derived(game !== null && game.result === null);
  /** The question the flag button acts on: the one on screen, or the one just answered. */
  const flagTarget = $derived(
    screen === "question"
      ? (game?.question?.id ?? null)
      : ["correct", "wrong", "victory"].includes(screen)
        ? (game?.last?.question_id ?? null)
        : null,
  );
  const mode = $derived(game?.settings.mode ?? "gamemaster");
  const levels = $derived(levelsOf(game));
  /** Blocks on the tower: correct answers in this game. */
  const blocks = $derived(game?.history.filter((h) => h.correct).length ?? 0);

  onMount(() => {
    music(MUSIC.start);
    refresh();
    loadFlags();
  });

  async function loadFlags() {
    flags = await fetchFlags().catch(() => flags);
  }

  async function refresh() {
    try {
      ({ game, supply } = await fetchGame());
      if (loading && (await language()).ask) screen = "language"; // a fresh save, once (plan 68)
      notice ??= takeSaveNotice();
      error = saveWarning();
    } catch (e) {
      error = errorText(e);
    } finally {
      loading = false;
    }
  }

  /** A save that couldn't be written stays in the corner until one is (plan 55). */
  function saveWarning(): string | null {
    const e = saveError();
    return e ? errorText(e) : null;
  }

  /** The transition routine (04, "Transitions"): effect, fade to black, switch, fade in, music. */
  /** `apply` runs behind the black: a new game state that the old screen can't show (no question
   * any more, a different `last`) must not land before the screen switches. */
  async function go(next: Screen, effect: Cue, apply?: () => void) {
    busy = true;
    music(null);
    sfx(effect);
    veil = effect === "rewind" ? "rewind" : "black";
    black = true;
    await sleep(FADE_MS);
    apply?.();
    music(MUSIC[next]);
    previous = screen;
    screen = next;
    picked = null;
    swappedBy = null;
    if (next !== "select") fresh = new Set();
    if (next === "question") {
      await tick();
      await Promise.race([questionRef?.ready() ?? Promise.resolve(), sleep(PRELOAD_MAX_MS)]);
    }
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
      error = saveWarning();
      return next;
    } catch (e) {
      error = errorText(e);
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

  /** A joker goes to the engine; errors show in the corner (09-jokers.md). */
  async function playJokerAction(body: JokerPlay) {
    try {
      const res = await playJoker(body);
      error = saveWarning();
      return res;
    } catch (e) {
      error = errorText(e);
      return null;
    }
  }

  /** The joker is done on the Question screen: Paso goes back to Select, a Francotirador hit to Level. */
  async function jokerPlayed(next: Game, event: JokerEvent) {
    error = saveWarning();
    if (event.joker === "easier" || event.joker === "category") {
      // The card flip (JK-7): the transitions in Question.svelte only run while this is set.
      swap.active = true;
      swappedBy = event;
      sfx(event.joker === "easier" ? "whistle-down" : "swoosh-up");
      setTimeout(() => (swap.active = false), FLIP_MS * 2 + 100);
    }
    if (event.joker === "skip") {
      const cards = newCards(next);
      await go(table(next), "paper", () => ((game = next), (fresh = cards)));
    } else if (event.joker === "snipe" && event.outcome === "hit") {
      await go("level", "rewind", () => (game = next));
    } else game = next;
  }

  /** After «¡Correcto!»: the Level screen, where the new block drops and lands with a thud. */
  async function toLevel() {
    const level = blocks;
    const landed = sleep(FADE_MS * 2 + 750).then(() => sfx("block", onTwelve(level, levels))); // the fall in Tower.svelte
    await go("level", "whoosh");
    await landed;
  }

  /** The table after the Level screen; with `cards: 0` the engine already opened the question (D-88). */
  const table = (g: Game | null): Screen => (g?.phase === "question" ? "question" : "select");

  /** Where a game continues: the Level screen before a choice, else its question. */
  function resume() {
    if (game?.phase === "question") return go("question", "swoosh");
    return go("level", game?.level === 1 ? "ready" : "whoosh");
  }

  async function newGame() {
    unlocked = true;
    greeting = null;
    refused = null;
    await go("player", "whoosh");
  }

  /** A name was picked or typed: their age group and bundles next (plan 29). */
  async function choosePlayer(name: string) {
    if (busy) return;
    chosen = name;
    refused = null;
    await go("choice", "whoosh");
  }

  /** The Choice screen's «¡A jugar!»: start the game, greet, then the Level screen. */
  async function startGame(choice: GameActionBody & { mode: GameMode }, exhausted: string[]) {
    if (busy || chosen === null) return;
    busy = true;
    try {
      game = await gameAction("new", { player: chosen, ...choice });
      await noteExhausted(choice, exhausted).catch(() => {}); // every start: it prunes too
      error = saveWarning();
      refused = null;
    } catch (e) {
      if (e instanceof GameError && e.code !== "server_error") refused = e;
      else error = errorText(e);
      busy = false;
      return;
    }
    greeting = game?.player ?? chosen;
    sfx("ready");
    busy = true;
    await sleep(GREETING_MS);
    await go("level", "ready");
    greeting = null;
  }

  async function pick(i: number) {
    if (!game || i >= game.options.length) return;
    sfx("pop");
    picked = i;
    setTimeout(() => sfx("tear"), TEAR_MS);
    const [ok] = await Promise.all([act("pick", { index: i }), sleep(PICK_MS)]);
    if (ok) await go("question", "swoosh");
    else picked = null;
  }

  async function answered(next: Game | null) {
    if (!next) return;
    error = saveWarning();
    const apply = () => (game = next);
    if (next.phase === "won") await go("victory", "applause-big", apply);
    else if (next.phase === "lost") await go("wrong", "boom", apply);
    else await go("correct", "applause", apply);
  }

  async function toStart() {
    await refresh();
    await go("start", "whoosh");
  }

  // Admin overlay ---------------------------------------------------------------------------

  function openOverlay() {
    overlayOpen = true;
    sfx("menu-open");
    pausedMedia = [...document.querySelectorAll<HTMLMediaElement>("audio, video")].filter((m) => !m.paused);
    pausedMedia.forEach((m) => m.pause());
  }

  function closeOverlay() {
    overlayOpen = false;
    sfx("menu-close");
    pausedMedia.forEach((m) => m.play().catch(() => {}));
    pausedMedia = [];
  }

  async function skip(everyone: boolean) {
    overlayOpen = false;
    const next = await request("skip", { everyone });
    if (next === undefined) return;
    const cards = newCards(next);
    await go(table(next), "paper", () => ((game = next), (fresh = cards)));
  }

  async function undo() {
    overlayOpen = false;
    pausedMedia = [];
    const next = await request("undo");
    if (next !== undefined) await go("question", "rewind", () => (game = next));
  }

  /** «Cambiar pregunta» (MD-12): a new question on screen. */
  async function replace(seen: boolean) {
    overlayOpen = false;
    pausedMedia = [];
    const next = await request("replace", { seen });
    if (next !== undefined) await go("question", "paper", () => (game = next));
  }

  /** «Saltar a nivel» (MD-12): the Level screen at the new level, then its table. */
  async function jumpLevel(level: number) {
    overlayOpen = false;
    pausedMedia = [];
    const next = await request("level", { level });
    if (next !== undefined) await go("level", "whoosh", () => (game = next));
  }

  /** Difficulty and bundles mid-game (MD-12): a new table; a refusal stays in the dialog. */
  async function changeSettings(body: GameActionBody): Promise<string | null> {
    let next: Game | null;
    busy = true;
    try {
      next = await gameAction("settings", body);
    } catch (e) {
      return errorText(e);
    } finally {
      busy = false;
    }
    error = saveWarning();
    overlayOpen = false;
    pausedMedia = [];
    const cards = newCards(next);
    await go(table(next), "paper", () => ((game = next), (fresh = cards)));
    return null;
  }

  /** The joker budget of the running game, from the overlay (MD-4); the screen stays as it is. */
  async function setBudget(budget: Partial<JokerBudget>) {
    await act("jokers", { jokers: budget });
  }

  async function openFlagList() {
    await loadFlags();
    flagListOpen = true;
  }

  /** Abandon, then the same player's configure screen (D-88); without a player, Start. */
  async function restart() {
    overlayOpen = false;
    pausedMedia = [];
    const player = game?.player ?? null;
    await act("abandon");
    if (player === null) return toStart();
    await refresh();
    chosen = player;
    refused = null;
    await go("choice", "whoosh");
  }

  /** The flag dialog (decision 60); media pauses like under the overlay. */
  function openFlag() {
    if (!flagTarget || flagOpen) return;
    flagOpen = true;
    sfx("menu-open");
    pausedMedia = [...document.querySelectorAll<HTMLMediaElement>("audio, video")].filter((m) => !m.paused);
    pausedMedia.forEach((m) => m.pause());
  }

  function closeFlag() {
    flagOpen = false;
    pausedMedia.forEach((m) => m.play().catch(() => {}));
    pausedMedia = [];
  }

  /** Flag (or re-note, `note` "" = none) or unflag (null) the question for review (GM-5); errors show in the corner. */
  async function writeFlag(note: string | null) {
    const id = flagTarget;
    if (!id || flagBusy) return;
    const level = screen === "question" ? game?.level : game?.history.at(-1)?.level;
    flagBusy = true;
    try {
      flags = await setFlag(id, note === null ? null : { player: game?.player ?? null, level, note });
      sfx(note === null ? "menu-close" : "menu-open");
      error = saveWarning();
    } catch (e) {
      error = errorText(e);
    } finally {
      flagBusy = false;
      closeFlag();
    }
  }

  /** The question's final answer is out: skip and undo would race the reveal. */
  const questionBusy = () => screen === "question" && (questionRef?.busy() ?? false);

  // Input (04, "Input"; lib/input.svelte.ts) ------------------------------------------------

  /** Screen actions; the scope of the screen on top passes the rest down. */
  function onScreen(on: Screen, a: Action): boolean {
    if (on === "start" && notice && (a.type === "confirm" || a.type === "new")) notice = null;
    else if (on === "start" && a.type === "confirm") {
      if (running) resume();
      else newGame();
    } else if (on === "start" && a.type === "new") newGame();
    else if (on === "level" && a.type === "confirm") go(table(game), "paper");
    else if (on === "select" && a.type === "pick" && a.n <= 4 && picked === null) pick(a.n - 1);
    else if (on === "correct" && a.type === "confirm") toLevel();
    else if ((on === "wrong" || on === "victory") && a.type === "confirm") toStart();
    else return false;
    return true;
  }

  // Global: Esc opens the overlay, M flags; under every screen.
  const popGame = pushScope({
    name: "game",
    handle: (a) => {
      if (a.type === "menu") openOverlay();
      else if (a.type === "flag" && flagTarget) openFlag();
      else return false;
      return true;
    },
  });
  onDestroy(popGame);

  $effect(() => {
    const on = screen;
    if (on === "language" || on === "player" || on === "choice" || on === "question") return; // they push their own
    return pushScope({
      name: on,
      keys: on === "start" ? { [NEW_KEY]: { type: "new" } } : undefined,
      handle: (a) => onScreen(on, a),
      root: () => main,
      keep: on === "start",
    });
  });

  // Steam rich presence «Nivel 7 de 12» while playing (plan 85).
  let presence = "";
  $effect(() => {
    const level = ["level", "select", "question", "correct"].includes(screen) ? game?.level : undefined;
    const next = level ? `${level}/${levels}` : "";
    if (!steam?.available || next === presence) return;
    presence = next;
    void steam.setPresence(level ? "#Level" : "", level ? { level: String(level), levels: String(levels) } : {});
  });

  onMount(() => listen({ busy: () => busy, first: onclick }));
  onMount(() => listenPads(onclick));

  /** The first click or key press unlocks audio and autoplay (04, "Start"). A pad press may not
   * count as user activation (plan 45), so every input resumes the context again. */
  function onclick() {
    unlock();
    if (!unlocked) {
      unlocked = true;
      sfx("unlocked");
    }
  }

  const NEW_KEY = t("screen.start.newKey").toLowerCase();
  const FLAG_KEY = t("flag.key");

  /** /?fuegos=<variant> or ?fuegos=finale plays fireworks over the Start screen (preview, UI-9). */
  const preview = new URLSearchParams(location.search).get("fuegos");

  /** Each card's tilt, within ±3° (10, "Cards"); fixed per game and level, so a re-render keeps it. */
  function tilt(i: number) {
    const seed = ((game?.id ?? 0) * 31 + (game?.level ?? 0) * 7 + i * 13) % 13;
    return (seed / 12) * 6 - 3;
  }
</script>

<main class="game" bind:this={main}>
  {#if loading}
    <Stage />
    <p class="center label">{t("screen.loading")}</p>
  {:else if screen === "language"}
    <Stage />
    <LanguageScreen onpicked={() => go("start", "whoosh")} />
  {:else if screen === "start"}
    <Stage />
    {#if preview}<Fireworks mode={preview === "finale" ? "finale" : "single"} variant={preview} />{/if}
    <section class="start">
      <h1 class="wordmark"><span class="bang">{t("screen.start.open")}</span>{t("screen.start.name")}<span class="bang">{t("screen.start.close")}</span></h1>
      <p class="subtitle">{t("screen.start.subtitle", { n: levelsOf(game) })}</p>
      <div class="buttons">
        {#if notice}
          <div class="notice glass">
            <p>{t(notice.kind === "newer" ? "save.newer" : "save.corrupt", { path: notice.path })}</p>
            <button class="candy" onclick={() => (notice = null)} data-focus-default data-focus-id="notice">{t("action.next")} <Prompt action="confirm" /></button>
          </div>
        {:else if running}
          <button class="candy breathe" onclick={resume} disabled={busy} data-focus-default data-focus-id="main">
            {game?.player
              ? t("screen.start.resumePlayer", { name: game.player, level: game.level })
              : t("screen.start.resume", { level: game?.level ?? 0 })}
            <Prompt action="confirm" />
          </button>
          <button class="secondary" onclick={newGame} disabled={busy} data-focus-id="new">{t("screen.start.new")} <Prompt action="new" /></button>
        {:else}
          <button class="candy breathe" onclick={newGame} disabled={busy} data-focus-default data-focus-id="main">{t("screen.start.play")} <Prompt action="confirm" /></button>
        {/if}
      </div>
      {#if supply}<SupplyReport {supply} />{/if}
    </section>
  {:else if screen === "player"}
    <Stage />
    <Player {busy} onchoose={choosePlayer} ondeleted={refresh} />
  {:else if screen === "choice" && chosen !== null}
    <Stage />
    <Choice player={chosen} {busy} {greeting} {refused} onstart={startGame} onback={() => go("player", "whoosh")} />
  {:else if screen === "level" && game}
    <Stage />
    <div class="corner-hud">{#if game.player}<span class="chip glass">{game.player}</span>{/if}</div>
    <aside class="side-tray"><JokerTray readonly left={game.jokers_left} /></aside>
    <section class="level">
      <Tower filled={blocks} {levels} drop={previous === "correct"} />
      <div class="level-text">
        <p class="kicker">{t("screen.level.kicker")}</p>
        <h1 class="title big">{game.level} <span class="of">{t("screen.level.of", { n: levels })}</span></h1>
        {#if game.repeat}
          <p class="milestone again">{t("screen.level.again")}</p>
        {:else if milestone(game.level, levels, game.id)}
          <p class="milestone">{milestone(game.level, levels, game.id)}</p>
        {/if}
        <button class="secondary hint" onclick={() => go(table(game), "paper")} disabled={busy} data-focus-default>{t("action.next")} <Prompt action="confirm" /></button>
      </div>
    </section>
  {:else if screen === "select" && game}
    <Stage />
    <div class="corner-hud"><Hud level={game.level} {levels} player={game.player} /></div>
    <aside class="side-tray"><JokerTray readonly left={game.jokers_left} /></aside>
    <section class="select">
      <h2 class="title">{t("screen.select.title")}</h2>
      {#if game.options.length === 0}
        <p class="error-box">{t("screen.select.empty")} <Prompt action="menu" /> → {t("action.home")}.</p>
      {/if}
      <div class="cards" style:--n={game.options.length}>
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
            data-focus-default
          >
            <span class="flap"></span>
            <span class="seal">{i + 1}</span>
            {#if picked === i}
              <span class="tear"></span>
              <span class="letter-slot"><span class="letter">?</span></span>
            {/if}
            {#if fresh.has(i)}<span class="new-badge">{t("screen.select.fresh")}</span>{/if}
            <span class="description" lang={questionLocale()}>{option.description}</span>
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
        {levels}
        playerName={game.player}
        paused={overlayOpen}
        shown={!black}
        jokers={game.jokers}
        jokersLeft={game.jokers_left}
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
      <h1 class="title good">{t("screen.result.correct")}</h1>
      <div class="panel glass" lang={questionLocale()}>
        <p class="answer"><span class="badge good-badge"><Icon name="check" /></span>{game.last.answer}</p>
        <p class="fun-fact">{game.last.fun_fact}</p>
      </div>
      <button class="secondary hint" onclick={toLevel} disabled={busy} data-focus-default>{t("action.next")} <Prompt action="confirm" /></button>
    </section>
  {:else if screen === "wrong" && game?.last}
    <Stage mood="wrong" />
    <section class="result wrong">
      <div class="columns">
        <Tower filled={blocks} {levels} small crumble />
        <div class="stack">
          <h1 class="title bad">{t("screen.result.wrong")}</h1>
          <div class="panel glass">
            <p class="label">{t("screen.result.answerWas")}</p>
            <p class="answer" lang={questionLocale()}><span class="badge good-badge"><Icon name="check" /></span>{game.last.answer}</p>
            <p class="fun-fact" lang={questionLocale()}>{game.last.fun_fact}</p>
          </div>
          <p class="consolation">{consolation(game.level, levels, game.id)}</p>
        </div>
      </div>
      <button class="candy" onclick={toStart} disabled={busy} data-focus-default>{t("action.home")} <Prompt action="confirm" /></button>
    </section>
  {:else if screen === "victory" && game}
    <Stage mood="victory" />
    <Fireworks mode="finale" />
    <section class="result victory">
      <Tower filled={levels} {levels} drop />
      <div class="stack">
        <h1 class="title big gold">{t("screen.victory.title")}</h1>
        {#if game.player}<p class="milestone">{t("screen.victory.top", { name: game.player })}</p>{/if}
        {#if game.last}
          <div class="panel glass" lang={questionLocale()}>
            <p class="answer"><span class="badge good-badge"><Icon name="check" /></span>{game.last.answer}</p>
            <p class="fun-fact">{game.last.fun_fact}</p>
          </div>
        {/if}

        <button class="candy breathe" onclick={toStart} disabled={busy} data-focus-default>{t("action.home")} <Prompt action="confirm" /></button>
      </div>
    </section>
  {:else}
    <Stage />
    <p class="center">{t("screen.noData")} <Prompt action="menu" /> → {t("action.home")}.</p>
  {/if}

  {#if error}
    <div class="error-box corner">{error}</div>
  {/if}

  {#if !loading && !overlayOpen && !flagOpen && flagTarget}
    <!-- Flag for review (GM-5): as faint as the menu button; no focus, like it. -->
    <button
      class="flag-button"
      class:on={flagged.has(flagTarget)}
      onclick={openFlag}
      onmousedown={(e) => e.preventDefault()}
      tabindex="-1"
      data-nofocus
      aria-label={t(flagged.has(flagTarget) ? "flag.on" : "flag.off", { key: FLAG_KEY })}
      title={t(flagged.has(flagTarget) ? "flag.on" : "flag.off", { key: FLAG_KEY })}
    >
      <Icon name="flag" />
    </button>
  {/if}

  {#if !loading && !overlayOpen && screen !== "language"}
    <!-- The overlay for the mouse (IN-1); no focus, so a later Enter can't open it. -->
    <button
      class="menu-button"
      onclick={openOverlay}
      onmousedown={(e) => e.preventDefault()}
      tabindex="-1"
      data-nofocus
      aria-label={t("a11y.menu")}
      title={t("a11y.menu")}
    >
      <span></span><span></span><span></span>
    </button>
  {/if}

  <div class="black {veil}" class:on={black} style:transition-duration="{FADE_MS}ms">
    {#if veil === "rewind"}<span class="rewind-mark">◀◀</span>{/if}
  </div>

  {#if overlayOpen}
    <Overlay
      {mode}
      questionId={screen === "question" && game?.question ? game.question.id : (game?.last?.question_id ?? null)}
      questionLabel={t(screen === "question" ? "overlay.question" : "overlay.lastQuestion")}
      {game}
      {running}
      canSkip={screen === "question" && !questionBusy()}
      canTable={running && (game?.phase === "select" || (screen === "question" && game?.settings.cards === 0 && !questionBusy()))}
      canUndo={!!game?.can_undo && !questionBusy()}
      canRestart={running || screen !== "start"}
      onflags={openFlagList}
      onclose={closeOverlay}
      onskip={() => skip(false)}
      onskipall={() => skip(true)}
      onundo={undo}
      onreplace={replace}
      onlevel={jumpLevel}
      onsettings={changeSettings}
      onrestart={restart}
      onbudget={setBudget}
    />
  {/if}
  {#if overlayOpen && flagListOpen}
    <FlagList {flags} onclose={() => (flagListOpen = false)} />
  {/if}
  {#if flagOpen && flagTarget}
    <FlagDialog
      flagged={flagged.has(flagTarget)}
      note={flags.find((f) => f.question_id === flagTarget)?.note ?? ""}
      busy={flagBusy}
      onflag={(note) => writeFlag(note)}
      onunflag={() => writeFlag(null)}
      onclose={() => (sfx("menu-close"), closeFlag())}
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
  .notice {
    max-width: calc(48 * var(--u));
    padding: calc(1 * var(--u)) calc(1.6 * var(--u));
    font-size: calc(1.1 * var(--u));
    color: var(--amber);
    overflow-wrap: anywhere;
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
    grid-template-columns: repeat(var(--n), minmax(0, calc(23.5 * var(--u))));
    justify-content: center;
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
  .card:focus-visible,
  .card:global([data-nav]) {
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
  .menu-button {
    position: fixed;
    top: calc(var(--safe-y) * 0.5);
    right: calc(var(--safe-x) * 0.5);
    z-index: 30;
    display: flex;
    flex-direction: column;
    justify-content: center;
    gap: calc(0.35 * var(--u));
    width: calc(3.2 * var(--u));
    height: calc(3.2 * var(--u));
    padding: 0 calc(0.8 * var(--u));
    border: 1px solid transparent;
    border-radius: calc(0.8 * var(--u));
    background: transparent;
    opacity: 0.35;
    transition:
      opacity 0.2s,
      background 0.2s;
  }
  .menu-button:hover {
    opacity: 1;
    background: var(--glass-strong);
    border-color: var(--slate-400);
  }
  .menu-button span {
    height: calc(0.25 * var(--u));
    border-radius: calc(0.15 * var(--u));
    background: var(--paper);
  }
  .flag-button {
    position: fixed;
    top: calc(var(--safe-y) * 0.5);
    right: calc(var(--safe-x) * 0.5 + 3.8 * var(--u));
    z-index: 30;
    display: grid;
    place-items: center;
    width: calc(3.2 * var(--u));
    height: calc(3.2 * var(--u));
    padding: 0;
    border: 1px solid transparent;
    border-radius: calc(0.8 * var(--u));
    background: transparent;
    color: var(--paper);
    font-size: calc(1.6 * var(--u));
    opacity: 0.35;
    transition:
      opacity 0.2s,
      background 0.2s;
  }
  .flag-button:hover {
    opacity: 1;
    background: var(--glass-strong);
    border-color: var(--slate-400);
  }
  .flag-button.on {
    --flag-fill: 1;
    color: var(--amber);
    opacity: 0.7;
  }
  /* Beside the flag and menu buttons, above the question card (B-18). */
  .corner {
    position: fixed;
    top: calc(var(--safe-y) * 0.5);
    right: calc(var(--safe-x) * 0.5 + 7.6 * var(--u));
    max-width: 55vw;
    min-height: calc(3.2 * var(--u));
    display: flex;
    align-items: center;
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
