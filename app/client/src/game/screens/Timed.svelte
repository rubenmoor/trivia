<script lang="ts">
  // Competitive (timed) (plan 164): one question for every seat, the 30 s clock and hints, claims, the claimer's 6 s,
  // one press answers (decision 295), the reveal; the next question of the round flips in here. The engine decides
  // every outcome; this screen only counts down and asks (`show`, `claim`, `answer`, `expire`).
  import { onDestroy, onMount, untrack } from "svelte";
  import { CLAIM_MS, HINT_MS, LIVES, QUESTION_MS } from "../../engine/choice.ts";
  import { fetchGame, gameAction } from "../../lib/api.ts";
  import { errorText } from "../../lib/errors.ts";
  import { claimLabel, seatDevice } from "../../lib/gamepad.svelte.ts";
  import { GameError } from "../../lib/http.ts";
  import { t } from "../../lib/i18n.ts";
  import { pushScope, type Action } from "../../lib/input.svelte.ts";
  import type { SessionView } from "../../lib/seats.ts";
  import { claimInput, seating } from "../../lib/seats.svelte.ts";
  import type { Game } from "../../lib/types.ts";
  import Glyph from "../Glyph.svelte";
  import Hearts from "../Hearts.svelte";
  import Icon from "../Icon.svelte";
  import Answers from "../question/Answers.svelte";
  import Card from "../question/Card.svelte";
  import { PAD_PICKS, questionKeys } from "../question/keys.ts";
  import Media from "../question/Media.svelte";
  import type { AnswerView } from "../question/reveal.ts";
  import SeatTag from "../SeatTag.svelte";
  import { music, sfx } from "../sound.svelte.ts";
  import { cardFlip, swap } from "../swap.ts";
  import { FLIP_MS, PRELOAD_MAX_MS, TIMED_RESULT_MS, TIMED_REVEAL_MS, sleep } from "../timing.ts";

  type Question = NonNullable<Game["question"]>;

  let {
    game,
    levels,
    paused = false,
    shown = true,
    onupdate,
    onround,
    onend,
  }: {
    /** A running timed session. */
    game: Game;
    levels: number;
    /** The Esc menu is open: the media waits. */
    paused?: boolean;
    /** The fade-in is over: the question may start its clock. */
    shown?: boolean;
    /** Every new game from this screen's actions. */
    onupdate: (game: Game) => void;
    /** The round ended (the game is the next round's); `before`: the seats before its last question, for the hearts lost. */
    onround: (game: Game, before: SessionView) => void;
    onend: (game: Game) => void;
  } = $props();

  /** An ended question during its reveal: it, the seats before it and its result stay on screen. */
  let held = $state<{ question: Question; session: SessionView; last: NonNullable<Game["last"]> } | null>(null);
  let revealed = $state(false);
  /** The claimer's pick, locked at once. */
  let locked = $state<number | null>(null);
  /** An action is out; the next waits. */
  let pending = $state(false);
  /** The next question flips in; its clock starts after. */
  let flipping = $state(false);
  let leaving = false;
  let error = $state<string | null>(null);
  let mediaFailed = $state(false);
  let mediaEl = $state<ReturnType<typeof Media>>();
  let screenEl = $state<HTMLDivElement>();
  let tiles = $state<HTMLButtonElement[]>([]);
  const timedOf = (g: Game) => g.session!.timed!;
  const roundOf = (g: Game) => `${timedOf(g).round}/${timedOf(g).repeat}`;
  // svelte-ignore state_referenced_locally
  const round = roundOf(game);
  /** The question this screen shows (not reset while paused hides it). */
  // svelte-ignore state_referenced_locally
  let current = $state<Question | null>(game.question);

  const session = $derived(held?.session ?? game.session!);
  const timed = $derived(session.timed!);
  const claim = $derived(held ? null : timedOf(game).claim);
  const question = $derived(held?.question ?? game.question);
  const view: AnswerView = $derived({ struck: [], locked, snipe: false, target: null, hit: null, revealed, result: held?.last ?? null });

  /** Resolves once the media is ready (Game.svelte waits before the fade-in). */
  export function ready() {
    return mediaEl?.ready() ?? Promise.resolve();
  }

  // Clocks: display only, from the view's deadlines.
  let now = $state(Date.now());
  /** The question bar where the last claim stopped it. */
  let frozen = $state(1);
  let frame = 0;
  onMount(() => {
    const step = () => {
      now = Date.now();
      frame = requestAnimationFrame(step);
    };
    step();
  });
  const left = (deadline: number, span: number) => Math.min(1, Math.max(0, (deadline - now) / span));
  const bar = $derived.by(() => {
    const d = held ? null : timedOf(game).deadline;
    return d === null ? frozen : left(d, QUESTION_MS);
  });
  $effect(() => {
    if (!held && timedOf(game).deadline !== null) frozen = bar;
  });
  const claimLeft = $derived(claim ? left(claim.deadline, CLAIM_MS) : 0);
  const claimSeconds = $derived(claim ? Math.max(0, Math.ceil((claim.deadline - now) / 1000)) : 0);

  let timers: ReturnType<typeof setTimeout>[] = [];
  const later = (fn: () => void, ms: number) => void timers.push(setTimeout(fn, Math.max(0, ms)));
  onDestroy(() => {
    leaving = true;
    cancelAnimationFrame(frame);
    timers.forEach(clearTimeout);
    swap.active = false;
  });

  /** A game from an action or a re-read: an ended question goes to its reveal, anything else up to Game.svelte. */
  function take(next: Game | null) {
    if (!next || next.id !== game.id || leaving) return;
    if (!held && current && next.last?.question_id === current.id) void reveal(next, game.session!);
    else onupdate(next);
  }

  /** The silent refusals (decision 282, plan 164): the new view wins. */
  const SILENT = new Set(["claim_taken", "paused", "not_shown", "claim_first", "not_your_claim"]);

  async function call(action: "show" | "claim" | "answer", body = {}) {
    pending = true;
    try {
      take(await gameAction(action, body));
      error = null;
    } catch (e) {
      if (e instanceof GameError && SILENT.has(e.code)) take((await fetchGame().catch(() => ({ game: null }))).game);
      else error = errorText(e);
      return false;
    } finally {
      pending = false;
    }
    return true;
  }

  /** The question is on screen: its media ready, then its 30 s run (decision 296). */
  async function present() {
    pending = true;
    await Promise.race([mediaEl?.ready() ?? Promise.resolve(), sleep(PRELOAD_MAX_MS)]);
    await call("show");
  }

  // Follow the game: the end, the next round, a question to show.
  $effect(() => {
    const g = game;
    if (held || pending || flipping || !shown || leaving) return;
    untrack(() => {
      if (current && g.last?.question_id === current.id) return void reveal(g, g.session!); // settled by a pause
      if (g.result !== null) return void ((leaving = true), onend(g));
      if (roundOf(g) !== round) return void ((leaving = true), onround(g, g.session!));
      const t = timedOf(g);
      if (!t.shown && !t.paused && g.phase === "question") void present();
    });
  });

  // The question's own fields (hints) as they grow; a new one once the old is gone.
  $effect(() => {
    const q = game.question;
    if (q && !held && (current === null || q.id === current.id)) current = q;
  });

  // Hints (D-27 as notes): re-read at each 8 s mark; the engine decides what shows.
  $effect(() => {
    const d = timedOf(game).deadline;
    if (d === null || held) return;
    const start = d - QUESTION_MS;
    const at = start + (Math.floor((Date.now() - start) / HINT_MS) + 1) * HINT_MS;
    if (at >= d) return;
    const id = setTimeout(reread, at - Date.now() + 50);
    return () => clearTimeout(id);
  });
  async function reread() {
    if (pending || held) return;
    take((await fetchGame().catch(() => ({ game: null }))).game);
  }
  let hintsOf: [string, number] | null = null;
  $effect(() => {
    const q = game.question;
    if (!q) return;
    if (hintsOf?.[0] === q.id && q.hints.length > hintsOf[1]) sfx("rustle");
    hintsOf = [q.id, q.hints.length];
  });

  // A deadline passed: ask the engine; `not_expired` re-arms with its ms left.
  $effect(() => {
    const t = timedOf(game);
    const at = t.claim?.deadline ?? t.deadline;
    if (at === null || held) return;
    const id = setTimeout(expire, at - Date.now() + 30);
    return () => clearTimeout(id);
  });
  async function expire() {
    if (held || leaving) return;
    if (pending) return void later(expire, 200);
    pending = true;
    try {
      take(await gameAction("expire"));
    } catch (e) {
      if (e instanceof GameError && e.code === "not_expired") later(expire, Number(e.params.ms ?? 0) + 30);
      else if (!(e instanceof GameError && e.code === "paused")) error = errorText(e);
    } finally {
      pending = false;
    }
  }

  function claimIt() {
    const t = timedOf(game);
    if (held || pending || t.claim || !t.shown || t.paused) return;
    sfx("pop"); // PLACEHOLDER(1451): the claim sting
    void call("claim");
  }

  /** The claimer's first pick is the answer (decision 295). */
  function tap(i: number) {
    if (!claim || held || pending || locked !== null || i >= (question?.answers.length ?? 0)) return;
    locked = i;
    sfx("padlock-close");
    void call("answer", { index: i }).then((ok) => {
      if (!ok && !held) locked = null;
    });
  }

  /** An ended question: the reveal beat after a pick, the result, then the next question, round or end. */
  async function reveal(next: Game, before: SessionView) {
    const last = next.last!;
    held = { question: current!, session: before, last };
    onupdate(next);
    mediaEl?.pause();
    if (last.chosen !== null) await sleep(TIMED_REVEAL_MS);
    if (leaving) return;
    revealed = true;
    sfx(last.correct ? "fanfare" : "whistle-down");
    await sleep(TIMED_RESULT_MS);
    if (leaving) return;
    const g = game;
    if (g.result !== null) return void ((leaving = true), onend(g));
    if (roundOf(g) !== round) return void ((leaving = true), onround(g, before));
    // The next question of the round flips in (JK-7's flip); its clock starts after.
    swap.active = true;
    flipping = true;
    current = g.question;
    frozen = 1;
    held = null;
    revealed = false;
    locked = null;
    mediaFailed = false;
    await sleep(FLIP_MS * 2 + 100);
    swap.active = false;
    flipping = false;
  }

  function replay() {
    if (mediaEl?.replay() && !held) music(null);
  }

  // Input: claim (bumpers, Space, picked keys; decision 290), A–D/1–4 and face buttons for the claimer; the seat
  // filter (plan 161) lets only seats that may act through.
  const KEYS = questionKeys();
  $effect(() => {
    const claims = claimInput();
    return pushScope({
      name: "timed",
      keys: { ...KEYS, ...claims.keys },
      pad: () => ({ ...PAD_PICKS, ...claims.pad }),
      root: () => screenEl,
      pressable: () => false,
      handle: (a: Action) => {
        if (a.type === "claim") claimIt();
        else if (a.type === "pick") tap(a.n - 1);
        else if (a.type === "replay") replay();
        else return a.type === "confirm" || a.type === "joker" || a.type === "peek";
        return true;
      },
    });
  });

  const name = (i: number) => session.seats[i]?.player ?? String(i + 1);
  /** The result line of the reveal. */
  const outcome = $derived.by(() => {
    if (!held || !revealed) return null;
    const { last } = held;
    if (last.seat === undefined) return { text: t("screen.timed.timeUp"), good: false };
    return last.correct
      ? { text: t("screen.timed.correct", { name: name(last.seat) }), good: true }
      : { text: t("screen.result.out", { name: name(last.seat) }), good: false };
  });
  /** The seat that answered, once revealed: ✓ or out on the strip. */
  const answered = $derived(held && revealed && held.last.seat !== undefined ? held.last : null);
</script>

<div class="timed-screen" bind:this={screenEl}>
  <div class="top">
    <p class="round-line">{t("screen.timed.round", { n: timed.round, of: levels })}</p>
    <p class="label">{t("screen.timed.question", { n: timed.question_in_round, of: timed.round_size })}</p>
    <span class="label placeholder">{"PLACEHOLDER(1453)"}</span>
  </div>
  <div class="clock" aria-hidden="true"><span class="fill" class:low={bar < 1 / 3} style:--left={bar}></span></div>

  {#if question}
    {#key question.id}
      <Card {question} swappedBy={null} {mediaFailed} sweeping={false} replayOff={!!held} onreplay={replay} />
      <footer in:cardFlip|global={{ side: "in" }} out:cardFlip|global={{ side: "out" }}>
        <Answers
          answers={question.answers}
          {view}
          disabled={!claim || !!held || locked !== null}
          pickable={!!claim && locked === null}
          device={claim ? seatDevice(claim.seat) : null}
          shattering={null}
          bind:tiles
          onpick={tap}
          onhover={() => {}}
        />
        {#if error}<p class="error-box">{error}</p>{/if}
      </footer>
      <Media bind:this={mediaEl} bind:failed={mediaFailed} {question} shown={shown && !flipping} {paused} dark={!!held && !revealed} onended={() => !held && music("question")} />
    {/key}
  {:else}
    <div></div>
    <div></div>
    <footer></footer>
  {/if}

  {#if claim}
    <div class="banner glass-strong">
      <svg class="ring" viewBox="0 0 40 40" aria-hidden="true">
        <circle cx="20" cy="20" r="17" class="track" />
        <circle cx="20" cy="20" r="17" class="arc" style:--left={claimLeft} />
        <text x="20" y="20">{claimSeconds}</text>
      </svg>
      <div class="banner-text">
        <p class="claimed">{t("screen.timed.claimed", { name: name(claim.seat) })}</p>
        <SeatTag {session} seat={claim.seat} />
      </div>
    </div>
  {:else if outcome}
    <div class="banner glass-strong result" class:good={outcome.good}>
      <p class="claimed">{outcome.text}</p>
      {#if held?.last.seat !== undefined}<SeatTag {session} seat={held.last.seat} />{/if}
    </div>
  {/if}

  {#if timedOf(game).paused}
    <div class="veil" role="status"><p>{t("screen.timed.paused")}</p></div>
  {/if}

  <div class="strip">
    {#each session.seats as s, i (i)}
      {@const out = s.status !== "playing" || (answered?.seat === i && !answered.correct)}
      {@const ok = s.correct_this_round || (answered?.seat === i && answered.correct)}
      {@const label = claimLabel(i)}
      <div class="seat glass-light" class:out class:dim={claim !== null && claim.seat !== i}>
        <SeatTag {session} seat={i} small />
        <Hearts lives={s.lives ?? LIVES} {out} small />
        {#if ok}
          <span class="ok"><Icon name="check" /></span>
        {:else if !out && label}
          {#if seating.binding[i] === "kbm"}
            <button class="claim" data-claim tabindex="-1" onclick={claimIt} disabled={!!claim || !!held}>
              <kbd>{"text" in label ? label.text : ""}</kbd> {t("screen.timed.claim")}
            </button>
          {:else if "buttons" in label}
            <span class="chip">{#each label.buttons as b (b)}<Glyph button={b} set={label.style} size="1.5em" />{/each}</span>
          {/if}<!-- a key seat's key: on its tag -->
        {/if}
      </div>
    {/each}
  </div>
</div>

<style>
  .timed-screen {
    position: absolute;
    inset: 0;
    display: grid;
    grid-template-rows: auto auto auto 1fr auto auto;
    justify-items: center;
    padding: var(--safe-y) var(--safe-x) calc(var(--safe-y) * 0.6);
    gap: calc(1 * var(--u));
  }
  .top {
    justify-self: start;
    display: flex;
    align-items: baseline;
    gap: calc(1.2 * var(--u));
  }
  .top p {
    margin: 0;
  }
  .round-line {
    font-family: var(--font-display);
    font-size: calc(1.8 * var(--u));
    font-weight: 800;
    color: var(--amber);
  }
  .placeholder {
    color: var(--amber);
  }
  .clock {
    width: 100%;
    height: calc(0.8 * var(--u));
    border-radius: calc(0.4 * var(--u));
    background: var(--glass);
    overflow: hidden;
  }
  .fill {
    display: block;
    height: 100%;
    width: calc(var(--left) * 100%);
    background: var(--amber);
    border-radius: inherit;
  }
  .fill.low {
    background: var(--coral);
  }
  footer {
    width: 70%;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: calc(0.8 * var(--u));
  }
  .banner {
    position: absolute;
    top: 28%;
    right: var(--safe-x);
    z-index: 2;
    display: flex;
    align-items: center;
    gap: calc(1.2 * var(--u));
    padding: calc(0.8 * var(--u)) calc(1.6 * var(--u));
    animation: arrive 0.35s var(--spring) backwards;
  }
  .veil {
    position: absolute;
    inset: 0;
    z-index: 3;
    display: grid;
    place-items: center;
    background: rgba(10, 12, 20, 0.94);
  }
  .veil p {
    margin: 0;
    font-family: var(--font-display);
    font-size: calc(6 * var(--u));
    font-weight: 800;
    color: var(--amber);
  }
  .banner-text {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    gap: calc(0.4 * var(--u));
  }
  .banner.result {
    flex-direction: column;
    border-color: var(--coral);
  }
  .banner.result.good {
    border-color: var(--mint);
  }
  .claimed {
    margin: 0;
    font-family: var(--font-display);
    font-size: calc(2.6 * var(--u));
    font-weight: 800;
  }
  .ring {
    width: calc(5.5 * var(--u));
    height: calc(5.5 * var(--u));
  }
  .ring circle {
    fill: none;
    stroke-width: 4;
  }
  .ring .track {
    stroke: var(--slate-600);
  }
  .ring .arc {
    stroke: var(--amber);
    stroke-dasharray: 106.8;
    stroke-dashoffset: calc((1 - var(--left)) * 106.8);
    transform: rotate(-90deg);
    transform-origin: center;
  }
  .ring text {
    fill: var(--paper);
    font-family: var(--font-display);
    font-size: 16px;
    font-weight: 800;
    text-anchor: middle;
    dominant-baseline: central;
  }
  .strip {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: calc(0.6 * var(--u)) calc(0.8 * var(--u));
    max-width: 100%;
  }
  .seat {
    display: flex;
    align-items: center;
    gap: calc(0.6 * var(--u));
    padding: calc(0.3 * var(--u)) calc(0.7 * var(--u));
    border-radius: calc(0.9 * var(--u));
    transition: opacity 0.3s, filter 0.3s;
  }
  .seat.dim {
    opacity: 0.4;
  }
  .seat.out {
    opacity: 0.45;
    filter: grayscale(1);
  }
  .ok {
    display: inline-flex;
    color: var(--mint);
    font-size: calc(1.4 * var(--u));
  }
  .chip {
    display: inline-flex;
    color: var(--slate-200);
    font-size: calc(1 * var(--u));
  }
  .claim {
    display: inline-flex;
    align-items: center;
    gap: calc(0.4 * var(--u));
    padding: calc(0.15 * var(--u)) calc(0.6 * var(--u));
    border: 1px solid var(--slate-400);
    border-radius: calc(0.6 * var(--u));
    background: none;
    font-size: calc(1 * var(--u));
    color: var(--paper);
  }
</style>
