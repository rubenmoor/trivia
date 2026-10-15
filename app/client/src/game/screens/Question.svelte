<script lang="ts">
  // The Question screen (04-ui-tv-display.md): media, question, 4 answers, the lock-in
  // mechanic, the final answer, the level-dependent wait and the reveal. Jokers (09-jokers.md):
  // the tray, arming, Paso's choice, Cambiazo's picker, Francotirador's aiming, Soplo's notes.
  // Controller: the state, timers and input scopes; the pieces in game/question/.
  import { onMount } from "svelte";
  import { gameAction } from "../../lib/api.ts";
  import { errorText } from "../../lib/errors.ts";
  import { t } from "../../lib/i18n.ts";
  import { displayName, questionLocale } from "../../lib/names.svelte.ts";
  import { focusControl, pushScope, type Action, type Dir, type Intent, type Keys } from "../../lib/input.svelte.ts";
  import type { Game, JokerBudget, JokerEvent, JokerName, Jokers } from "../../lib/types.ts";
  import CategoryPicker from "../CategoryPicker.svelte";
  import DifficultyDial from "../DifficultyDial.svelte";
  import Hud from "../Hud.svelte";
  import JokerFlight from "../JokerFlight.svelte";
  import JokerTray from "../JokerTray.svelte";
  import Prompt from "../Prompt.svelte";
  import { TOKENS } from "../jokers.ts";
  import { DEFAULT_LEVELS, onTwelve } from "../levels.ts";
  import Answers, { LETTERS } from "../question/Answers.svelte";
  import Card from "../question/Card.svelte";
  import FinalAnswer from "../question/FinalAnswer.svelte";
  import Media from "../question/Media.svelte";
  import Scope from "../question/Scope.svelte";
  import SkipDialog from "../question/SkipDialog.svelte";
  import type { AnswerView } from "../question/reveal.ts";
  import Shredder from "../Shredder.svelte";
  import { duck, music, sfx, sound } from "../sound.svelte.ts";
  import { cardFlip } from "../swap.ts";
  import {
    AFTER_REVEAL_MS,
    ARM_MS,
    PADLOCK_MS,
    POP_BACK_MS,
    REVEAL_WAIT_S,
    SHATTER_MS,
    SNIPE_BEAT_MS,
    SNIPE_HIT_MS,
    SWEEP_MS,
    sleep,
  } from "../timing.ts";

  export type JokerPlay = { joker: JokerName; purge?: boolean; subcategory?: string; index?: number };

  let {
    question,
    level,
    levels = DEFAULT_LEVELS,
    playerName,
    paused,
    shown = true,
    jokers,
    jokersLeft = null,
    swappedBy = null,
    play,
    onplayed,
    onanswered,
  }: {
    question: NonNullable<Game["question"]>;
    level: number;
    /** The game's levels (D-88). */
    levels?: number;
    /** For the HUD (D-28). */
    playerName: string | null;
    /** The admin overlay is open: the wait before the reveal stops. */
    paused: boolean;
    /** False while the screen sits behind the black of a transition: the media waits to start (UI-7). */
    shown?: boolean;
    /** Joker availability from the engine, or null. */
    jokers: Jokers | null;
    /** Uses left per joker for the tray's badges, null = unlimited (MD-3). */
    jokersLeft?: JokerBudget | null;
    /** The joker that just swapped this question in (Bájale, Cambiazo), for the dial and the label. */
    swappedBy?: JokerEvent | null;
    /** Sends a joker to the engine (Game.svelte shows errors); null if it was refused. */
    play: (body: JokerPlay) => Promise<{ game: Game; event: JokerEvent } | null>;
    /** The joker is done on screen: Game.svelte takes the new game (and changes screen if needed). */
    onplayed: (game: Game, event: JokerEvent) => void;
    onanswered: (game: Game | null) => void;
  } = $props();

  /** The answer locked in, or null. */
  let locked = $state<number | null>(null);
  /** «Respuesta final» is visible (the padlock has moved away). */
  let finalReady = $state(false);
  let submitted = $state(false);
  let result = $state<Game["last"]>(null);
  let revealed = $state(false);
  let error = $state<string | null>(null);
  let mediaFailed = $state(false);
  let mediaEl = $state<ReturnType<typeof Media>>();

  let padlockTimer: ReturnType<typeof setTimeout> | undefined;

  /** The joker token lifted by a first tap (Soplo, Bájale), waiting for the second. */
  let armed = $state<JokerName | null>(null);
  let armTimer: ReturnType<typeof setTimeout> | undefined;
  /** The joker dialog or mode on screen. */
  let mode = $state<null | "skip" | "category" | "snipe">(null);
  /** Francotirador's target, and the shot that hit the correct answer. */
  let target = $state<number | null>(null);
  let hit = $state<number | null>(null);
  let jokerBusy = $state(false);
  /** The token flying to the centre (JK-5), and the slot a fresh one pops back into. */
  let flight = $state<{ name: JokerName; from: DOMRect; done: () => void } | null>(null);
  let popping = $state<JokerName | null>(null);
  /** «Paso» (JK-6): the purged subcategory in the shredder, then the question swept off. */
  let shredding = $state<{ name: string; done: () => void } | null>(null);
  let sweeping = $state(false);
  /** Francotirador (JK-8): the answer being shot at (the scope stays on it), and the one shattering. */
  let shot = $state<number | null>(null);
  let shattering = $state<number | null>(null);
  let tiles = $state<HTMLButtonElement[]>([]);
  let screenEl = $state<HTMLDivElement>();
  /** The peek is held (plan 113): only the picture shows. */
  let peeking = $state(false);
  const canPeek = $derived(
    question.media.type === "image" && question.media.role !== "decorative" && !!question.media.file_url && !mediaFailed && mode === null,
  );

  /** Resolves once the media is ready to show (or failed); Game.svelte waits for it before the fade-in. */
  export function ready() {
    return mediaEl?.ready() ?? Promise.resolve();
  }

  /** True while the final answer or a joker is out: nothing may change the question (the overlay checks it). */
  export function busy() {
    return submitted || jokerBusy;
  }

  onMount(() => () => {
    clearTimeout(padlockTimer);
    clearTimeout(armTimer);
  });

  function mediaEnded() {
    if (!submitted) music(locked !== null ? "submitted" : "question");
  }

  /** The music follows the lock (developer feedback): locked in = the intense loop, unlocked =
   * back to the question loop. While the question's own media plays, the music stays off. */
  function lockMusic() {
    if (sound.music === "question" || sound.music === "submitted") music(locked !== null ? "submitted" : "question");
  }

  function tap(i: number) {
    if (submitted || jokerBusy || question.struck.includes(i)) return;
    if (mode === "snipe") return aim(i);
    if (mode) return;
    disarm();
    if (locked !== null) return unlock();
    locked = i;
    sfx("padlock-close");
    lockMusic();
    // The big padlock shakes for a suspense beat, opens and slides away (UI-12, question/FinalAnswer.svelte).
    padlockTimer = setTimeout(() => {
      finalReady = true;
      sfx("padlock-open");
    }, PADLOCK_MS);
  }

  function unlock() {
    if (submitted || locked === null) return;
    clearTimeout(padlockTimer);
    locked = null;
    finalReady = false;
    sfx("padlock-close");
    lockMusic();
  }

  /** Waits ms, but the clock stops while the overlay is open. */
  async function wait(ms: number) {
    for (let left = ms; left > 0; ) {
      await sleep(100);
      if (!paused) left -= 100;
    }
  }

  async function submit() {
    if (!finalReady || submitted || locked === null) return;
    submitted = true;
    error = null;
    mediaEl?.pause();
    music("roll"); // the drum roll until the reveal (developer feedback)
    sfx("boom");
    try {
      const [game] = await Promise.all([gameAction("answer", { index: locked }), wait(REVEAL_WAIT_S[onTwelve(level, levels) - 1] * 1000)]);
      result = game?.last ?? null;
      revealed = true;
      music(null);
      sfx(result?.correct ? "fanfare" : "sad-trombone");
      await wait(AFTER_REVEAL_MS);
      onanswered(game);
    } catch (e) {
      submitted = false;
      music(locked !== null ? "submitted" : "question");
      error = errorText(e);
    }
  }

  function replay() {
    if (mediaEl?.replay() && !submitted) music(null);
  }

  // Jokers (09-jokers.md) ------------------------------------------------------------------------

  function disarm() {
    clearTimeout(armTimer);
    armed = null;
  }

  /** A tap on a token (or its key): Soplo and Bájale arm first; the others open their dialog. */
  function press(name: JokerName) {
    if (submitted || jokerBusy || mode || !jokers?.[name].available) return;
    if (locked !== null) unlock(); // a joker unlocks a locked answer first (09, "Common")
    if (name === "skip" || name === "category" || name === "snipe") {
      disarm();
      mode = name;
      target = name === "snipe" ? question.answers.findIndex((_, i) => !question.struck.includes(i)) : null;
      sfx(name === "snipe" ? "heartbeat" : "joker-open");
      return;
    }
    if (armed === name) return void fire({ joker: name });
    disarm();
    armed = name;
    sfx("joker-armed");
    armTimer = setTimeout(() => (armed = null), ARM_MS);
  }

  /** The common play animation (JK-5): resolves once the token has burst in the centre. */
  function fly(name: JokerName) {
    const token = document.querySelector(`.token[data-joker="${name}"]`);
    if (!token) return Promise.resolve();
    return new Promise<void>((done) => (flight = { name, from: token.getBoundingClientRect(), done }));
  }

  async function fire(body: JokerPlay) {
    disarm();
    mode = null;
    jokerBusy = true; // input stays locked until the joker's effect is over
    duck(true);
    sfx("joker-activate");
    if (body.joker === "snipe") shot = body.index ?? null;
    const [res] = await Promise.all([play(body), fly(body.joker)]);
    flight = null;
    popping = body.joker;
    sfx("token-back");
    setTimeout(() => (popping = null), POP_BACK_MS);
    if (!res) {
      jokerBusy = false;
      shot = null;
      duck(false);
      return;
    }
    if (res.event.joker === "snipe") {
      // The scope tightens on the target, a beat of silence, then the cork pops (09, "Francotirador").
      sfx("silence");
      await wait(SNIPE_BEAT_MS(onTwelve(level, levels)));
      sfx("cork-pop");
      if (res.event.outcome === "hit") {
        hit = res.event.correct_index;
        shot = null;
        sfx("sad-trombone");
        await wait(SNIPE_HIT_MS);
      } else {
        shattering = res.event.index;
        shot = null;
        sfx("glass-break");
        await sleep(SHATTER_MS);
        shattering = null;
      }
    } else if (res.event.joker === "skip") {
      const purged = res.event.purged;
      if (purged) await new Promise<void>((done) => (shredding = { name: purged, done }));
      shredding = null;
      sweeping = true;
      sfx("swoosh");
      await sleep(SWEEP_MS);
    }
    jokerBusy = false;
    target = null;
    duck(false);
    if (res.event.joker === "hint") sfx("rustle"); // the new note slides in
    onplayed(res.game, res.event);
  }

  function aim(i: number) {
    if (question.struck.includes(i)) return;
    if (target === i) return void fire({ joker: "snipe", index: i });
    target = i;
    sfx("tick");
  }

  /** Arrow keys move the crosshair over the answers that are left (2×2 grid). */
  function moveTarget(dir: Dir) {
    const step = { right: 1, left: -1, down: 2, up: -2 }[dir];
    for (let i = (target ?? 0) + step; i >= 0 && i < question.answers.length; i += step) {
      if (!question.struck.includes(i)) return void (target = i);
    }
  }

  // Input (lib/input.svelte.ts): A–D/1–4 pick, joker letters, R replay; dialogs and aiming are modal.
  const REPLAY_KEY = t("screen.question.replayKey");
  const KEYS: Keys = {
    ...Object.fromEntries(TOKENS.map((t) => [t.key.toLowerCase(), { type: "joker", name: t.name }])),
    ...Object.fromEntries(LETTERS.map((l, i) => [l.toLowerCase(), { type: "pick", n: i + 1 }])),
    [REPLAY_KEY.toLowerCase()]: { type: "replay" },
    [t("screen.question.peekKey").toLowerCase()]: { type: "peek", down: true },
  };
  // Pad (decision 9): Y/B/X/A pick by position, RT submits, LT unlocks; on a token A/B are confirm/back.
  const PAD_PICKS: Record<number, Intent> = Object.fromEntries([3, 1, 2, 0].map((b, i) => [b, { type: "pick", n: i + 1 }]));
  const PAD_FINAL: Record<number, Intent> = { 6: { type: "back" }, 7: { type: "submit" }, 11: { type: "peek", down: true } };
  const PAD_TOKEN: Record<number, Intent> = { 0: { type: "confirm" }, 1: { type: "back" } };
  function padMap(): Record<number, Intent> {
    const f = document.activeElement;
    const other = f instanceof HTMLElement && f.hasAttribute("data-nav") && !tiles.includes(f as HTMLButtonElement);
    return { ...PAD_PICKS, ...(other ? PAD_TOKEN : {}), ...PAD_FINAL };
  }

  /** LB/RB: focus the previous/next playable token, wrapping. */
  function focusToken(step: 1 | -1) {
    const list = [...(screenEl?.querySelectorAll<HTMLButtonElement>(".tray .token:not(:disabled)") ?? [])];
    if (!list.length) return;
    const at = list.indexOf(document.activeElement as HTMLButtonElement);
    focusControl(list[at < 0 ? (step > 0 ? 0 : list.length - 1) : (at + step + list.length) % list.length]);
  }
  const answer = (a: Action) => (a.type === "pick" && a.n <= question.answers.length ? a.n - 1 : null);

  $effect(() =>
    pushScope({
      name: "question",
      keys: KEYS,
      pad: padMap,
      root: () => screenEl,
      pressable: (el) => locked === null || el !== tiles[locked],
      handle: (a) => {
        const i = answer(a);
        if (a.type === "joker") press(a.name);
        else if (i !== null) tap(i);
        else if (a.type === "back") unlock();
        else if (a.type === "confirm" || a.type === "submit") submit();
        else if (a.type === "joker-focus") focusToken(a.step);
        else if (a.type === "replay") replay();
        else if (a.type === "peek") peeking = a.down;
        else return false;
        return true;
      },
    }),
  );

  $effect(() => {
    const name = armed;
    if (!name) return;
    return pushScope({
      name: "question-armed",
      handle: (a) => {
        if (a.type === "back" || a.type === "menu") disarm();
        else if (a.type === "confirm") fire({ joker: name });
        else return false;
        return true;
      },
    });
  });

  // Francotirador: keys and arrows only aim; Enter shoots.
  $effect(() => {
    if (mode !== "snipe") return;
    return pushScope({
      name: "question-snipe",
      modal: true,
      handle: (a) => {
        const i = answer(a);
        if (a.type === "back" || a.type === "menu") mode = target = null;
        else if (i !== null && !question.struck.includes(i)) target = i;
        else if (a.type === "navigate") moveTarget(a.dir);
        else if (a.type === "confirm" && target !== null) fire({ joker: "snipe", index: target });
        else return false;
        return true;
      },
    });
  });

  const view: AnswerView = $derived({ struck: question.struck, locked, snipe: mode === "snipe", target, hit, revealed, result });
  /** The tile under Francotirador's scope. */
  const scoped = $derived(tiles[shot ?? (mode === "snipe" ? (target ?? -1) : -1)] ?? null);
</script>

<!-- svelte-ignore a11y_no_static_element_interactions -->
<div
  class="question-screen"
  bind:this={screenEl}
  class:sweeping
  class:peeking={peeking && canPeek}
  style:--sweep="{SWEEP_MS}ms"
  onpointerdown={(e) => e.target === screenEl && e.button === 0 && (peeking = true)}
  onpointerup={() => (peeking = false)}
  onpointercancel={() => (peeking = false)}
  onpointerleave={() => (peeking = false)}
>
  <div class="top">
    <Hud {level} {levels} player={playerName} />
    {#if canPeek}<span class="peek glass"><Prompt action={{ type: "peek", down: true }} /> {t("screen.question.peek")}</span>{/if}
  </div>

  {#if swappedBy?.joker === "easier"}
    <div class="dial-spot"><DifficultyDial from={swappedBy.from} to={swappedBy.to} /></div>
  {/if}

  <Card {question} {swappedBy} {mediaFailed} {sweeping} replayOff={mode !== null} onreplay={replay} />

  <aside class="tray">
    <JokerTray
      jokers={submitted ? null : jokers}
      left={jokersLeft}
      hintsLeft={3 - question.hints.length}
      {armed}
      away={flight?.name ?? null}
      {popping}
      covered={mode !== null}
      onpress={press}
    />
  </aside>
  {#if flight}
    {@const f = flight}
    <JokerFlight from={f.from} icon={TOKENS.find((t) => t.name === f.name)!.icon} ondone={f.done} />
  {/if}

  {#if mode === "skip" && jokers}
    <SkipDialog purge={jokers.skip.purge} onpick={(purge) => fire(purge ? { joker: "skip", purge } : { joker: "skip" })} oncancel={() => (mode = null)} />
  {/if}
  {#if shredding}<Shredder name={displayName("subcategory", shredding.name)} lang={questionLocale()} ondone={shredding.done} />{/if}
  {#if mode === "category" && jokers}
    <CategoryPicker
      categories={jokers.category.categories}
      onpick={(subcategory) => fire({ joker: "category", subcategory })}
      oncancel={() => (mode = null)}
    />
  {/if}
  <Scope tile={scoped} tight={shot !== null} aiming={mode === "snipe"} hit={hit !== null} oncancel={() => (mode = target = null)} />

  <footer in:cardFlip|global={{ side: "in" }} out:cardFlip|global={{ side: "out" }}>
    <Answers
      answers={question.answers}
      {view}
      disabled={submitted || hit !== null}
      {shattering}
      bind:tiles
      onpick={tap}
      onhover={(i) => mode === "snipe" && !question.struck.includes(i) && (target = i)}
    />
    <FinalAnswer locked={locked !== null} ready={finalReady} {submitted} {revealed} {error} onsubmit={submit} />
  </footer>

  <Media bind:this={mediaEl} bind:failed={mediaFailed} {question} {shown} {paused} dark={submitted && !revealed} onended={mediaEnded} />
</div>

<style>
  .question-screen {
    position: absolute;
    inset: 0;
    display: grid;
    grid-template-rows: auto auto 1fr auto;
    justify-items: center;
    padding: var(--safe-y) var(--safe-x) calc(var(--safe-y) * 0.6);
    gap: calc(1.2 * var(--u));
  }
  .top {
    justify-self: start;
    display: flex;
    align-items: center;
    gap: calc(0.8 * var(--u));
  }
  .peek {
    display: flex;
    align-items: center;
    gap: calc(0.4 * var(--u));
    padding: calc(0.35 * var(--u)) calc(1 * var(--u));
    border-radius: calc(0.9 * var(--u));
    font-size: calc(1 * var(--u));
    color: var(--slate-200);
  }
  /* Peek (plan 113): every panel fades out, the picture stays, unfiltered; release restores at once. */
  .peeking > :global(:not(.backdrop)) {
    opacity: 0;
    pointer-events: none; /* not visibility: hidden, which drops DOM focus */
    transition: opacity 0.15s;
  }
  .question-screen.peeking > :global(.backdrop) :global(img) {
    filter: none;
  }
  .dial-spot {
    position: absolute;
    top: var(--safe-y);
    right: var(--safe-x);
    z-index: 2;
  }
  .tray {
    position: absolute;
    left: var(--safe-x);
    top: 50%;
    transform: translateY(-50%);
  }
  footer {
    width: 70%;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: calc(1.2 * var(--u));
  }
  /* «Paso»: the answers are swept off after the card (JK-6, question/Card.svelte). */
  .sweeping footer {
    transition:
      transform var(--sweep) cubic-bezier(0.6, 0, 0.9, 0.5),
      opacity var(--sweep);
    transition-delay: 0.08s;
    transform: translateX(-120vw) rotate(-8deg);
    opacity: 0;
  }
</style>
