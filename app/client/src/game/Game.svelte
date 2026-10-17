<script lang="ts">
  // The game on the TV (plans/04-ui-tv-display.md, D-21, D-25): a state machine over the screens
  // Start → Player → Choice → (Join, multiplayer) → Bundles → Level → Select → Question → Correct / Wrong → … → Victory (answers off, D-105:
  // Question → Next → … → Completed; timed, plan 164: Level as round screen → Timed → … → Level → …), with one transition routine and the admin overlay on Esc. The engine
  // keeps the game (engine/, lib/api.ts).
  import { onDestroy, onMount, tick, untrack } from "svelte";
  import { fetchFlags, fetchGame, gameAction, noteRunningOut, playJoker, setFlag, type GameActionBody } from "../lib/api.ts";
  import { isOurs } from "../engine/pool.ts";
  import { GameError } from "../lib/http.ts";
  import { steam, validUser, type ModList } from "../lib/desktop.ts";
  import { language, saveError, takeSaveNotice } from "../lib/engine.ts";
  import { errorText } from "../lib/errors.ts";
  import { telemetryState } from "../lib/telemetry.ts";
  import { t } from "../lib/i18n.ts";
  import { listenPads } from "../lib/gamepad.svelte.ts";
  import { listen, pushScope, type Action } from "../lib/input.svelte.ts";
  import { holdPause } from "../lib/pause.ts";
  import { bindSession, lostSeat, watchGame } from "../lib/seats.svelte.ts";
  import type { SessionView } from "../lib/seats.ts";
  import { emit, loadedMods, watchLayers, type ModLayer } from "../lib/mods.ts";
  import type { Game, GameMode, JokerBudget, JokerEvent, Flagged } from "../lib/types.ts";
  import FlagDialog from "./FlagDialog.svelte";
  import FlagList from "./FlagList.svelte";
  import Hud from "./Hud.svelte";
  import Prompt from "./Prompt.svelte";
  import JokerTray from "./JokerTray.svelte";
  import { levelsOf, onTwelve } from "./levels.ts";
  import Overlay from "./Overlay.svelte";
  import SeatLost from "./SeatLost.svelte";
  import SeatTag from "./SeatTag.svelte";
  import { music, sfx, unlock, type Cue, type Track } from "./sound.svelte.ts";
  import Stage from "./Stage.svelte";
  import { swap } from "./swap.ts";
  import CornerButtons from "./CornerButtons.svelte";
  import { isSession, type ChoiceDraft } from "./choiceDraft.ts";
  import { seatBlocks, type SeatDraft } from "./seats.ts";
  import Bundles from "./screens/Bundles.svelte";
  import Choice from "./screens/Choice.svelte";
  import Consent from "./screens/Consent.svelte";
  import Correct from "./screens/Correct.svelte";
  import DomScreen from "./screens/DomScreen.svelte";
  import Language from "./screens/Language.svelte";
  import Level from "./screens/Level.svelte";
  import Mods, { fetchModList, heldOff } from "./screens/Mods.svelte";
  import Join from "./screens/Join.svelte";
  import Player from "./screens/Player.svelte";
  import Question, { type JokerPlay } from "./screens/Question.svelte";
  import Revealed from "./screens/Revealed.svelte";
  import { screenFailed, screenFor } from "./screens/registry.ts";
  import Select from "./screens/Select.svelte";
  import Start from "./screens/Start.svelte";
  import Timed from "./screens/Timed.svelte";
  import Victory from "./screens/Victory.svelte";
  import Wrong from "./screens/Wrong.svelte";
  import "./theme.css";
  import { BLOCK_DROP_MS, FADE_MS, FLIP_MS, GREETING_MS, PICK_MS, PRELOAD_MAX_MS, TEAR_MS, sleep } from "./timing.ts";
  import Veil from "./Veil.svelte";

  type Screen = "language" | "consent" | "start" | "player" | "bundles" | "choice" | "join" | "level" | "select" | "question" | "timed" | "correct" | "wrong" | "victory" | "next" | "completed";

  const MUSIC: Record<Screen, Track | null> = {
    language: "normal",
    consent: "normal",
    start: "normal",
    player: "normal",
    bundles: "normal",
    choice: "normal",
    join: "normal",
    level: "normal",
    select: "normal",
    question: "question",
    timed: "question", // PLACEHOLDER(1451): the timed track
    correct: "normal", // the fanfare plays at the reveal, then this comes back
    wrong: null,
    victory: "victory", // «Pomp and Circumstance», over the cheers
    next: "normal",
    completed: "normal", // no victory music (D-105)
  };

  // Next and Completed: both `Revealed` (answers off, D-105).
  const OURS = { Start, Language, Player, Bundles, Choice, Join, Level, Select, Question, Timed, Correct, Wrong, Next: Revealed, Completed: Revealed, Victory };
  type Name = keyof typeof OURS;
  /** Each screen: ours or a mod's (plan 117), read once; a failing one falls back to ours. */
  let S = $state.raw(Object.fromEntries(Object.entries(OURS).map(([n, c]) => [n, screenFor(n as Name, c)])) as typeof OURS);
  /** Mod layers over the game (`trivia.screens.show`). */
  let layers = $state.raw<readonly ModLayer[]>([]);
  onMount(() => watchLayers((l) => (layers = l)));

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
  let timedRef = $state<ReturnType<typeof Timed>>();
  /** Timed: the seats before the last round's end, for the round screen's hearts lost. */
  let roundBefore = $state<SessionView | null>(null);
  let main = $state<HTMLElement>();
  /** The chosen name while «¡Hola, …!» plays (UI-16). */
  let greeting = $state<string | null>(null);
  /** The name picked on Player, for the Choice and Bundles screens. */
  let chosen = $state<string | null>(null);
  /** The Choice screen's picks, kept for Back from Bundles; null: a fresh visit (plan 151). */
  let draft = $state<ChoiceDraft | null>(null);
  /** The Join screen's seats (plan 162), kept across Choice ↔ Join ↔ Bundles. */
  let seats = $state<SeatDraft[]>([]);
  /** The Bundles screen's pick; null until its preset loads. */
  let bundlePick = $state<string[] | null>(null);
  /** Why `new` refused the choice on the Bundles screen (plan 29). */
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
  /** The shell's mod list (plan 118); null outside the shell. */
  let modList = $state<ModList | null>(null);
  /** The Mods screen, over Start or the overlay. */
  let modsOpen = $state(false);
  /** Start screen's Mods button: loaded this run, held off until the notice. */
  const startMods = $derived(modList ? { loaded: loadedMods().length, held: heldOff(modList) } : null);

  const running = $derived(game !== null && game.result === null);
  /** The question the flag button acts on: the one on screen, or the one just answered. */
  const flagTarget = $derived.by(() => {
    const id = screen === "question"
      ? (game?.question?.id ?? null)
      : ["correct", "wrong", "victory", "next", "completed"].includes(screen)
        ? (game?.last?.question_id ?? null)
        : null;
    return validUser && id && isOurs(id) ? id : null; // mod questions: no flags, no reports (plan 93)
  });
  const mode = $derived(game?.settings.mode ?? "gamemaster");
  const levels = $derived(levelsOf(game));
  /** The multiplayer session (plan 163); null: every screen as for one player. */
  const session = $derived(game?.session ?? null);
  /** Blocks on the tower: correct answers in this game; answers off (D-105): the levels behind. rr-competitive:
   * the answerer's tower on Correct and Wrong, else the turn seat's; rr-coop: the team's game, as solo. */
  const blocks = $derived.by(() => {
    if (session?.mode === "rr-competitive") {
      const answered = (screen === "correct" || screen === "wrong") && game?.last?.seat !== undefined;
      return seatBlocks(session, answered ? game!.last!.seat! : session.turn, levels);
    }
    return game?.settings.answers === false ? game.level - 1 : (game?.history.filter((h) => h.correct).length ?? 0);
  });

  onMount(() => {
    music(MUSIC.start);
    refresh();
    loadFlags();
    fetchModList().then(
      (l) => {
        modList = l;
        if (l?.safeStart?.reason === "crashed") modsOpen = true; // before the start screen
      },
      (e) => console.error("mods:list", e),
    );
  });

  function closeMods(l: ModList | null) {
    modList = l ?? modList;
    modsOpen = false;
  }

  async function loadFlags() {
    flags = await fetchFlags().catch(() => flags);
  }

  async function refresh() {
    try {
      ({ game } = await fetchGame());
      if (loading) await askLanguage();
      notice ??= takeSaveNotice();
      error = saveWarning();
    } catch (e) {
      error = errorText(e);
    } finally {
      loading = false;
    }
  }

  /** A fresh save picks its language once (plan 68); then the install's telemetry answer, once (plan 108). */
  async function askLanguage() {
    if ((await language()).ask) screen = "language";
    else if (await askConsent()) screen = "consent";
  }

  /** Valid Steam user in the shell, never answered on this install (decision 121). */
  async function askConsent(): Promise<boolean> {
    const { available, consent } = await telemetryState();
    return available && consent === null;
  }

  async function languagePicked() {
    if (languageFromStart) return backToStart();
    await go((await askConsent()) ? "consent" : "start", "whoosh");
  }

  /** The language screen opened from Start's button (plan 126): back returns to Start. */
  let languageFromStart = $state(false);

  async function openLanguage() {
    if (busy) return;
    languageFromStart = true;
    await go("language", "whoosh");
  }

  async function backToStart() {
    await go("start", "whoosh", () => (languageFromStart = false));
  }

  /** A save that couldn't be written stays in the corner until one is (plan 55). */
  function saveWarning(): string | null {
    const e = saveError();
    return e ? errorText(e) : null;
  }

  /** The transition routine (04, "Transitions"): effect, fade to black, switch, fade in, music.
   * `apply` runs behind the black: a new game state that the old screen can't show (no question
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
    if (next === "question" || next === "timed") {
      await tick();
      await Promise.race([(next === "question" ? questionRef : timedRef)?.ready?.() ?? Promise.resolve(), sleep(PRELOAD_MAX_MS)]);
    }
    emit("screen", { name: nameOf(next) });
    if (next === "question" && game?.question) emit("question:shown", { id: game.question.id, level: game.level });
    black = false;
    await sleep(FADE_MS);
    busy = false;
  }

  const nameOf = (s: Screen) => (s[0].toUpperCase() + s.slice(1)) as Name;

  /** The screens' boundary: a mod's screen threw, ours instead. */
  function screenError(e: unknown, reset: () => void) {
    const name = nameOf(screen);
    if (!screenFailed(name, e)) throw e;
    S = { ...S, [name]: OURS[name] };
    queueMicrotask(reset);
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
    const was = busy;
    busy = true;
    try {
      const next = await gameAction(action, body);
      error = saveWarning();
      return next;
    } catch (e) {
      error = errorText(e);
      return undefined;
    } finally {
      busy = was;
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
      // The card flip (JK-7): the transitions in screens/Question.svelte only run while this is set.
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
    const landed = sleep(FADE_MS * 2 + BLOCK_DROP_MS).then(() => sfx("block", onTwelve(level, levels))); // the fall in Tower.svelte
    await go("level", "whoosh");
    await landed;
  }

  /** The table after the Level screen; with `cards: 0` the engine already opened the question (D-88); timed: its question. */
  const table = (g: Game | null): Screen => (g?.session?.timed ? "timed" : g?.phase === "question" ? "question" : "select");

  /** Where a game continues: the Level screen before a choice, else its question; timed: the round screen until the
   * question is shown, a pause left by a reload ends. */
  async function resume() {
    roundBefore = null;
    const timed = game?.session?.timed;
    if (timed?.paused) await act("resume");
    if (timed) return go(game?.session?.timed?.shown ? "timed" : "level", "whoosh");
    if (game?.phase === "question") return go("question", "swoosh");
    return go("level", game?.level === 1 ? "ready" : "whoosh");
  }

  async function newGame() {
    unlocked = true;
    greeting = null;
    refused = null;
    await go("player", "whoosh");
  }

  /** A name was picked or typed: their choice next, fresh picks (plan 151). */
  async function choosePlayer(name: string) {
    if (busy) return;
    chosen = name;
    draft = null;
    seats = [];
    bundlePick = null;
    refused = null;
    await go("choice", "whoosh");
  }

  /** The Choice screen's «Seguir»: the Join screen (multiplayer) or the Bundles screen, with these picks kept. */
  async function choicePicked(d: ChoiceDraft) {
    if (busy) return;
    draft = d;
    refused = null;
    await go(isSession(d.mode) ? "join" : "bundles", "whoosh");
  }

  /** The Bundles screen's «¡A jugar!»: start the game, greet, then the Level screen. */
  async function startGame(choice: GameActionBody & { mode: GameMode }, runningOut: string[]) {
    if (busy || chosen === null) return;
    busy = true;
    try {
      const session = isSession(choice.mode);
      const names = seats.map((x) => x.name ?? "");
      game = await gameAction("new", session
        ? { ...choice, players: names, ...(choice.mode === "rr-competitive" ? { age_groups: seats.map((x) => x.group) } : {}) }
        : { player: chosen, ...choice });
      if (session && game) bindSession(game.id, seats.map((x) => x.binding));
      await noteRunningOut(choice, runningOut).catch((e) => console.warn("noteRunningOut:", e)); // every start: it prunes too
      error = saveWarning();
      refused = null;
    } catch (e) {
      if (e instanceof GameError && e.code !== "server_error") refused = e;
      else error = errorText(e);
      busy = false;
      return;
    }
    greeting = isSession(choice.mode) ? seats.map((x) => x.name).join(", ") : (game?.player ?? chosen);
    roundBefore = null;
    sfx("ready");
    await sleep(GREETING_MS);
    await go("level", "ready");
    greeting = null;
  }

  async function pick(i: number) {
    if (!game || i >= game.options.length) return;
    sfx("pop");
    picked = i;
    busy = true; // until the question is on screen
    setTimeout(() => sfx("tear"), TEAR_MS);
    const [ok] = await Promise.all([act("pick", { index: i }), sleep(PICK_MS)]);
    if (ok) await go("question", "swoosh");
    else {
      picked = null;
      busy = false;
    }
  }

  async function answered(next: Game | null) {
    if (!next) return;
    error = saveWarning();
    const apply = () => (game = next);
    if (next.session) {
      // on the answer and the session's end: rr-competitive's top level is already the next seat's game
      if (!next.last?.correct) await go("wrong", "boom", apply);
      else if (next.result === null) await go("correct", "applause", apply);
      else await go("victory", "applause-big", apply);
    } else if (next.phase === "won") await go("victory", "applause-big", apply);
    else if (next.phase === "lost") await go("wrong", "boom", apply);
    else if (next.phase === "completed") await go("completed", "whoosh", apply);
    else if (next.last?.revealed) await go("next", "whoosh", apply);
    else await go("correct", "applause", apply);
  }

  /** Timed: a round ended; its round screen. */
  async function toRound(next: Game, before: SessionView) {
    await go("level", "whoosh", () => ((game = next), (roundBefore = before)));
  }

  /** Timed: the session ended (PLACEHOLDER(1452): the timed ends). */
  async function timedEnd(next: Game) {
    if (next.result === "won") await go("victory", "applause-big", () => (game = next));
    else await go("wrong", "boom", () => (game = next));
  }

  /** rr-competitive's Wrong «Seguir» (one seat out, decision 279): the next turn, or the last one standing wins. */
  async function afterOut() {
    if (game?.result === null) await go("level", "whoosh");
    else await go("victory", "applause-big");
  }
  const outGoesOn = $derived(session?.mode === "rr-competitive");

  async function toStart() {
    await refresh();
    await go("start", "whoosh");
  }

  // Admin overlay ---------------------------------------------------------------------------

  function pauseMedia() {
    pausedMedia = [...document.querySelectorAll<HTMLMediaElement>("audio, video")].filter((m) => !m.paused);
    pausedMedia.forEach((m) => m.pause());
  }

  function resumeMedia() {
    pausedMedia.forEach((m) => m.play().catch(() => {}));
    pausedMedia = [];
  }

  /** Timed: the Esc menu pauses the clock (decision 282); released on close or leave. */
  let releasePause = () => {};
  /** The game after a pause or resume, if it is still the one on screen. */
  const applyClock = (g: Game | null) => {
    if (g && g.id === game?.id) game = g;
  };

  /** Not during a transition: an action from the overlay would run a second `go` (the mouse button; keys wait anyway). */
  function openOverlay() {
    if (busy || overlayOpen) return;
    overlayOpen = true;
    releasePause = holdPause(applyClock);
    sfx("menu-open");
    pauseMedia();
  }

  function closeOverlay() {
    overlayOpen = false;
    releasePause();
    sfx("menu-close");
    resumeMedia();
  }

  /** An overlay action closes it; the screen changes, so the paused media stays paused. */
  function leaveOverlay() {
    overlayOpen = false;
    releasePause();
    pausedMedia = [];
  }

  async function skip(everyone: boolean) {
    leaveOverlay();
    const next = await request("skip", { everyone });
    if (next === undefined) return;
    const cards = newCards(next);
    await go(table(next), "paper", () => ((game = next), (fresh = cards)));
  }

  async function undo() {
    leaveOverlay();
    const next = await request("undo");
    if (next !== undefined) await go("question", "rewind", () => (game = next));
  }

  /** «Cambiar pregunta» (MD-12): a new question on screen. */
  async function replace(seen: boolean) {
    leaveOverlay();
    const next = await request("replace", { seen });
    if (next !== undefined) await go("question", "paper", () => (game = next));
  }

  /** «Saltar a nivel» (MD-12): the Level screen at the new level, then its table. */
  async function jumpLevel(level: number) {
    leaveOverlay();
    const next = await request("level", { level });
    if (next !== undefined) await go("level", "whoosh", () => (game = next));
  }

  /** «Ir a pregunta…» (dev mode, plan 85): that question on screen; a refusal stays in the dialog. */
  async function goTo(id: string): Promise<string | null> {
    let next: Game | null;
    busy = true;
    try {
      next = await gameAction("goto", { id });
    } catch (e) {
      return errorText(e);
    } finally {
      busy = false;
    }
    error = saveWarning();
    leaveOverlay();
    await go("question", "paper", () => (game = next));
    return null;
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
    leaveOverlay();
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

  /** Abandon, then Start (milestone 9, replaces D-88's configure screen). */
  async function restart() {
    leaveOverlay();
    if (!(await act("abandon"))) return;
    await toStart();
  }

  /** The flag dialog (decision 60); media pauses like under the overlay. */
  function openFlag() {
    if (!flagTarget || flagOpen || busy) return;
    flagOpen = true;
    sfx("menu-open");
    pauseMedia();
  }

  function closeFlag() {
    flagOpen = false;
    resumeMedia();
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
  const questionBusy = () => screen === "question" && (questionRef?.busy?.() ?? false);

  // Input (04, "Input"; lib/input.svelte.ts) ------------------------------------------------

  /** Screen actions; the scope of the screen on top passes the rest down. */
  function onScreen(on: Screen, a: Action): boolean {
    if (on === "start" && notice && (a.type === "confirm" || a.type === "new")) notice = null;
    else if (on === "start" && a.type === "confirm") {
      if (running) resume();
      else newGame();
    } else if (on === "start" && a.type === "new") newGame();
    else if (on === "start" && a.type === "language" && !notice) openLanguage();
    else if (on === "level" && a.type === "confirm" && !game?.session?.timed) go(table(game), "paper"); // timed: the countdown
    else if (on === "select" && a.type === "pick" && a.n <= 4 && picked === null) pick(a.n - 1);
    else if ((on === "correct" || on === "next") && a.type === "confirm") toLevel();
    else if (on === "wrong" && a.type === "confirm" && outGoesOn) afterOut();
    else if ((on === "wrong" || on === "victory" || on === "completed") && a.type === "confirm") toStart();
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
    if (on === "language" || on === "consent" || on === "player" || on === "bundles" || on === "choice" || on === "join" || on === "question" || on === "timed") return; // they push their own
    return pushScope({
      name: on,
      keys: on === "start" ? { [NEW_KEY]: { type: "new" }, [LANGUAGE_KEY]: { type: "language" } } : undefined,
      pad: on === "start" ? () => ({ 3: { type: "language" } }) : undefined,
      handle: (a) => onScreen(on, a),
      root: () => main,
      keep: on === "start",
      shared: on === "start" || on === "wrong" || on === "victory" || on === "completed", // Start: timed has no seat to act
    });
  });

  // Local multiplayer: the running session's seats filter input (plan 161).
  $effect(() => {
    const g = game;
    untrack(() => watchGame(g));
  });

  // Steam rich presence «Nivel 7 de 12» while playing (plan 85).
  let presence = "";
  $effect(() => {
    const level = ["level", "select", "question", "correct", "next"].includes(screen) ? game?.level : undefined;
    const next = level ? `${level}/${levels}` : "";
    if (!steam?.available || next === presence) return;
    presence = next;
    void steam.setPresence(level ? "#Level" : "", level ? { level: String(level), levels: String(levels) } : {});
  });

  onMount(() => listen({ busy: () => busy, first: firstInput }));
  onMount(() => listenPads(firstInput));

  /** The first click or key press unlocks audio and autoplay (04, "Start"). A pad press may not
   * count as user activation (plan 45), so every input resumes the context again. */
  function firstInput() {
    unlock();
    if (!unlocked) {
      unlocked = true;
      sfx("unlocked");
    }
  }

  const NEW_KEY = t("screen.start.newKey").toLowerCase();
  const LANGUAGE_KEY = t("screen.start.languageKey").toLowerCase();
</script>

{#snippet tray(g: Game)}
  <aside class="side-tray">
    {#if g.session?.mode === "rr-coop"}<p class="tray-label">{t("seat.team")}</p>
    {:else if g.session?.mode === "rr-competitive"}<div class="tray-label">{t("seat.jokers")}<br /><SeatTag session={g.session} seat={g.session.turn} small /></div>{/if}
    <JokerTray readonly left={g.jokers_left} />
  </aside>
{/snippet}

<main class="game" bind:this={main}>
  <svelte:boundary onerror={screenError}>
    {#if loading}
      <Stage />
      <p class="center label">{t("screen.loading")}</p>
    {:else if screen === "language"}
      <Stage />
      <S.Language onpicked={languagePicked} onback={languageFromStart ? backToStart : undefined} />
    {:else if screen === "consent"}
      <Stage />
      <Consent ondone={() => go("start", "whoosh")} />
    {:else if screen === "start"}
      <Stage />
      <S.Start {game} {running} {levels} {notice} {busy} mods={startMods} onmods={() => (modsOpen = true)} onlanguage={openLanguage} onresume={resume} onnew={newGame} ondismiss={() => (notice = null)} />
    {:else if screen === "player"}
      <Stage />
      <S.Player {busy} onchoose={choosePlayer} ondeleted={refresh} />
    {:else if screen === "choice" && chosen !== null}
      <Stage />
      <S.Choice player={chosen} {busy} {draft} onnext={choicePicked} onback={() => go("player", "whoosh")} />
    {:else if screen === "join" && chosen !== null && draft}
      <Stage />
      <S.Join mode={draft.mode} player={chosen} {busy} {seats} onseats={(s) => (seats = s)} onnext={() => go("bundles", "whoosh")} onback={() => go("choice", "whoosh")} />
    {:else if screen === "bundles" && chosen !== null && draft}
      <Stage />
      <S.Bundles player={chosen} {draft} {seats} {busy} {greeting} {refused} picked={bundlePick} onpick={(ids) => (bundlePick = ids)} onstart={startGame} onback={() => go(isSession(draft!.mode) ? "join" : "choice", "whoosh")} />
    {:else if screen === "level" && game}
      <Stage />
      {#if !session?.timed}
        <div class="corner-hud"><Hud level={null} player={game.player} {session} /></div>
        {@render tray(game)}
      {/if}
      <S.Level {game} {levels} {blocks} drop={previous === "correct" || previous === "next"} {busy} before={roundBefore} paused={overlayOpen} onnext={() => go(table(game), "paper")} />
    {:else if screen === "select" && game}
      <Stage />
      <div class="corner-hud"><Hud level={game.level} {levels} player={game.player} {session} /></div>
      {@render tray(game)}
      <S.Select {game} {picked} {fresh} {busy} onpick={pick} />
    {:else if screen === "question" && game?.question}
      {#key game.question.id}
        <S.Question
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
          answersOff={game.settings.answers === false}
          {session}
          play={playJokerAction}
          onplayed={jokerPlayed}
          onanswered={answered}
        />
      {/key}
    {:else if screen === "timed" && game?.session?.timed}
      <S.Timed
        bind:this={timedRef}
        {game}
        {levels}
        paused={overlayOpen}
        shown={!black && !busy}
        onupdate={(g) => (game = g)}
        onround={toRound}
        onend={timedEnd}
      />
    {:else if screen === "correct" && game?.last}
      <Stage mood="correct" />
      <S.Correct last={game.last} {busy} onnext={toLevel} {session} />
    {:else if screen === "wrong" && game?.last}
      <Stage mood="wrong" />
      <S.Wrong {game} last={game.last} {levels} {blocks} {busy} onhome={toStart} onnext={outGoesOn ? afterOut : undefined} />
    {:else if screen === "next" && game?.last}
      <Stage />
      <S.Next last={game.last} completed={false} {busy} onnext={toLevel} />
    {:else if screen === "completed" && game?.last}
      <Stage />
      <S.Completed last={game.last} completed {busy} onnext={toStart} />
    {:else if screen === "victory" && game}
      <Stage mood="victory" />
      <S.Victory {game} {levels} {busy} onhome={toStart} />
    {:else}
      <Stage />
      <p class="center">{t("screen.noData")} <Prompt action="menu" /> → {t("action.home")}.</p>
    {/if}
  </svelte:boundary>

  <CornerButtons
    {error}
    flagged={!loading && !overlayOpen && !flagOpen && flagTarget ? flagged.has(flagTarget) : null}
    menu={!loading && !overlayOpen && screen !== "language" && screen !== "consent"}
    onflag={openFlag}
    onmenu={openOverlay}
  />
  <Veil on={black} kind={veil} />
  {#each layers as layer (layer)}
    <DomScreen render={layer.render} props={{ close: layer.close }} onclose={layer.close} onerror={layer.fail} />
  {/each}

  {#if lostSeat() !== null}
    <SeatLost seat={lostSeat()!} onmenu={openOverlay} onpause={applyClock} />
  {/if}
  {#if overlayOpen}
    <Overlay
      {mode}
      questionId={screen === "question" && game?.question ? game.question.id : (game?.last?.question_id ?? null)}
      questionLabel={t(screen === "question" ? "overlay.question" : "overlay.lastQuestion")}
      {game}
      {running}
      canSkip={screen === "question" && !questionBusy()}
      questionOn={screen === "question"}
      canTable={running && (game?.phase === "select" || (screen === "question" && game?.settings.cards === 0 && !questionBusy()))}
      canUndo={!!game?.can_undo && !questionBusy()}
      canRestart={(running || screen !== "start") && !questionBusy()}
      canBudget={!questionBusy()}
      onflags={validUser ? openFlagList : null}
      onmods={modList ? () => (modsOpen = true) : null}
      onclose={closeOverlay}
      onskip={() => skip(false)}
      onskipall={() => skip(true)}
      onundo={undo}
      onreplace={replace}
      onlevel={jumpLevel}
      onsettings={changeSettings}
      ongoto={goTo}
      onrestart={restart}
      onbudget={setBudget}
    />
  {/if}
  {#if overlayOpen && flagListOpen && validUser}
    <FlagList bind:flags onclose={() => (flagListOpen = false)} />
  {/if}
  {#if modsOpen}
    <Mods onclose={closeMods} />
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
  /* Peek (plan 113): the corner buttons fade with the Question screen's panels. */
  .game:has(:global(.question-screen.peeking)) :global(:is(.flag-button, .menu-button, .error-box)) {
    opacity: 0;
    pointer-events: none; /* not visibility: hidden, which drops DOM focus */
    transition: opacity 0.15s;
  }
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
  .tray-label {
    margin: 0 0 calc(0.5 * var(--u));
    font-family: var(--font-display);
    font-size: calc(1 * var(--u));
    font-weight: 700;
    color: var(--slate-200);
    text-align: center;
  }
  .center {
    position: absolute;
    inset: 0;
    display: grid;
    place-items: center;
  }
</style>
