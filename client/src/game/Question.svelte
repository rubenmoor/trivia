<script lang="ts">
  // The Question screen (04-ui-tv-display.md): media, question, 4 answers, the lock-in
  // mechanic, the final answer, the level-dependent wait and the reveal. Jokers (09-jokers.md):
  // the tray, arming, Paso's choice, Cambiazo's picker, Francotirador's aiming, Soplo's notes.
  import { onMount } from "svelte";
  import { gameAction } from "../lib/api";
  import type { Game, JokerEvent, JokerName, Jokers } from "../lib/types";
  import CategoryPicker from "./CategoryPicker.svelte";
  import DifficultyDial from "./DifficultyDial.svelte";
  import Hud from "./Hud.svelte";
  import Icon from "./Icon.svelte";
  import JokerFlight from "./JokerFlight.svelte";
  import JokerTray, { TOKENS } from "./JokerTray.svelte";
  import Placeholder from "./Placeholder.svelte";
  import Shredder from "./Shredder.svelte";
  import { duck, mediaVolume, music, sfx } from "./sound.svelte";
  import { cardFlip, crossfade } from "./swap";
  import {
    AFTER_REVEAL_MS,
    ARM_MS,
    PADLOCK_MS,
    REVEAL_WAIT_S,
    SHATTER_MS,
    SNIPE_BEAT_MS,
    SNIPE_HIT_MS,
    SWEEP_MS,
    sleep,
  } from "./timing";

  export type JokerPlay = { joker: JokerName; purge?: boolean; subcategory?: string; index?: number };

  let {
    question,
    level,
    playerName,
    paused,
    jokers,
    swappedBy = null,
    play,
    onplayed,
    onanswered,
  }: {
    question: NonNullable<Game["question"]>;
    level: number;
    /** For the HUD (D-28). */
    playerName: string | null;
    /** The admin overlay is open: the wait before the reveal stops. */
    paused: boolean;
    /** Joker availability from the server, or null. */
    jokers: Jokers | null;
    /** The joker that just swapped this question in (Bájale, Cambiazo), for the dial and the label. */
    swappedBy?: JokerEvent | null;
    /** Sends a joker to the server (Game.svelte shows errors); null if it was refused. */
    play: (body: JokerPlay) => Promise<{ game: Game; event: JokerEvent } | null>;
    /** The joker is done on screen: Game.svelte takes the new game (and changes screen if needed). */
    onplayed: (game: Game, event: JokerEvent) => void;
    onanswered: (game: Game | null) => void;
  } = $props();

  const LETTERS = ["A", "B", "C", "D"];

  /** The answer locked in, or null. */
  let locked = $state<number | null>(null);
  /** «Respuesta final» is visible (the padlock has moved away). */
  let ready = $state(false);
  let submitted = $state(false);
  let result = $state<Game["last"]>(null);
  let revealed = $state(false);
  let error = $state<string | null>(null);
  let mediaFailed = $state(false);
  let player = $state<HTMLMediaElement>();
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
  /** The scope's hole, over the target answer. */
  let hole = $state<{ x: number; y: number; w: number; h: number } | null>(null);
  $effect(() => {
    const i = shot ?? (mode === "snipe" ? target : null);
    const el = i === null ? null : tiles[i];
    if (!el) return void (hole = null);
    const r = el.getBoundingClientRect();
    hole = { x: r.left + r.width / 2, y: r.top + r.height / 2, w: r.width, h: r.height };
  });
  let picker = $state<ReturnType<typeof CategoryPicker>>();

  const media = $derived(question.media);
  const src = (url: string | null) => (url ? `/media?url=${encodeURIComponent(url)}` : null);
  /** The full-bleed picture: the image itself, or an audio question's background (D-14). */
  const picture = $derived(media.type === "image" ? src(media.file_url) : src(question.background?.file_url ?? null));
  const decorative = $derived(media.type === "audio" || media.role === "decorative");
  const credits = $derived(
    [media.credit, media.type === "audio" ? question.background?.credit : null].filter(Boolean).join(" · "),
  );

  /** True while the final answer is out: nothing may change the question (the overlay checks it). */
  export function busy() {
    return submitted;
  }

  onMount(() => {
    if (media.type !== "image" && media.file_url) music(null); // the music is off while question media plays
    return () => {
      clearTimeout(padlockTimer);
      clearTimeout(armTimer);
    };
  });

  // The question's own audio/video follows the media volume from the admin overlay (UI-13).
  $effect(() => {
    if (player) player.volume = mediaVolume();
  });

  function mediaEnded() {
    if (!submitted) music("question");
  }

  function tap(i: number) {
    if (submitted || jokerBusy || question.struck.includes(i)) return;
    if (mode === "snipe") return aim(i);
    if (mode) return;
    disarm();
    if (locked !== null) return unlock();
    locked = i;
    sfx("candado: clunk");
    // The big padlock shakes for a suspense beat, opens and slides away (UI-12, CSS below).
    padlockTimer = setTimeout(() => {
      ready = true;
      sfx("candado se abre");
    }, PADLOCK_MS);
  }

  function unlock() {
    if (submitted || locked === null) return;
    clearTimeout(padlockTimer);
    locked = null;
    ready = false;
    sfx("candado se cierra");
  }

  /** Waits ms, but the clock stops while the overlay is open. */
  async function wait(ms: number) {
    for (let left = ms; left > 0; ) {
      await sleep(100);
      if (!paused) left -= 100;
    }
  }

  async function submit() {
    if (!ready || submitted || locked === null) return;
    submitted = true;
    error = null;
    player?.pause();
    music("submitted");
    sfx("golpe: respuesta final");
    try {
      const [game] = await Promise.all([gameAction("answer", { index: locked }), wait(REVEAL_WAIT_S[level - 1] * 1000)]);
      result = game?.last ?? null;
      revealed = true;
      music(null);
      sfx(result?.correct ? "fanfarria" : "trombón triste");
      await wait(AFTER_REVEAL_MS);
      onanswered(game);
    } catch (e) {
      submitted = false;
      music("question");
      error = e instanceof Error ? e.message : String(e);
    }
  }

  function replay() {
    if (!player) return;
    player.currentTime = 0;
    if (!submitted) music(null);
    player.play().catch(() => {});
  }

  // Jokers (09-jokers.md) ------------------------------------------------------------------------

  /** True while a joker dialog, mode or armed token waits: it gets every key, Esc included. */
  export function dialogOpen() {
    return mode !== null || armed !== null;
  }

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
      sfx(name === "snipe" ? "mira: latido" : "comodín: abrir");
      return;
    }
    if (armed === name) return fire({ joker: name });
    disarm();
    armed = name;
    sfx("comodín: preparado");
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
    sfx(`comodín: ${TOKENS.find((t) => t.name === body.joker)?.label}`);
    if (body.joker === "snipe") shot = body.index ?? null;
    const [res] = await Promise.all([play(body), fly(body.joker)]);
    flight = null;
    popping = body.joker;
    setTimeout(() => (popping = null), 500);
    if (!res) {
      jokerBusy = false;
      shot = null;
      duck(false);
      return;
    }
    if (res.event.joker === "snipe") {
      // The scope tightens on the target, a beat of silence, then the cork pops (09, "Francotirador").
      sfx("silencio…");
      await wait(SNIPE_BEAT_MS(level));
      sfx("¡pop! disparo de corcho");
      if (res.event.outcome === "hit") {
        hit = res.event.correct_index;
        shot = null;
        sfx("¡Ups!");
        await wait(SNIPE_HIT_MS);
      } else {
        shattering = res.event.index;
        shot = null;
        sfx("vidrio roto");
        await sleep(SHATTER_MS);
        shattering = null;
      }
    } else if (res.event.joker === "skip") {
      const purged = res.event.purged;
      if (purged) await new Promise<void>((done) => (shredding = { name: purged, done }));
      shredding = null;
      sweeping = true;
      sfx("escoba: fuuush");
      await sleep(SWEEP_MS);
    }
    jokerBusy = false;
    target = null;
    duck(false);
    onplayed(res.game, res.event);
  }

  function aim(i: number) {
    if (question.struck.includes(i)) return;
    if (target === i) return fire({ joker: "snipe", index: i });
    target = i;
    sfx("mira: tic");
  }

  /** Arrow keys move the crosshair over the answers that are left (2×2 grid). */
  function moveTarget(key: string) {
    const step = { ArrowRight: 1, ArrowLeft: -1, ArrowDown: 2, ArrowUp: -2 }[key] ?? 0;
    for (let i = (target ?? 0) + step; i >= 0 && i < question.answers.length; i += step) {
      if (!question.struck.includes(i)) return void (target = i);
    }
  }

  const JOKER_KEYS: Record<string, JokerName> = Object.fromEntries(TOKENS.map((t) => [t.key.toLowerCase(), t.name]));

  export function key(e: KeyboardEvent) {
    const k = e.key.toLowerCase();
    const i = "abcd".indexOf(k) >= 0 ? "abcd".indexOf(k) : "1234".indexOf(k);
    const cancel = e.key === "Escape" || e.key === "Backspace";
    if (mode === "category") return picker?.key(e);
    if (mode === "skip") {
      if (cancel) mode = null;
      else if (e.key === "1") fire({ joker: "skip" });
      else if (e.key === "2" && jokers?.skip.purge.available) fire({ joker: "skip", purge: true });
      else return;
    } else if (mode === "snipe") {
      if (cancel) mode = target = null;
      else if (k.length === 1 && i >= 0 && !question.struck.includes(i)) target = i; // keys only aim; Enter shoots
      else if (e.key.startsWith("Arrow")) moveTarget(e.key);
      else if ((e.key === "Enter" || e.key === " ") && target !== null) fire({ joker: "snipe", index: target });
      else return;
    } else if (armed && cancel) disarm();
    else if (armed && (e.key === "Enter" || e.key === " ")) fire({ joker: armed });
    else if (k in JOKER_KEYS) press(JOKER_KEYS[k]);
    else if (k.length === 1 && i >= 0) tap(i);
    else if (e.key === "Backspace") unlock();
    else if (e.key === "Enter" || e.key === " ") submit();
    else if (k === "r") replay();
    else return;
    e.preventDefault();
  }

  /** Long questions shrink one step instead of growing to three lines (10, "Scale"). */
  const long = $derived(question.question.length > 110);

  function answerClass(i: number) {
    if (hit !== null) return i === hit ? "right" : "dim";
    if (question.struck.includes(i)) return "struck";
    if (mode === "snipe") return i === target ? "target" : "";
    if (revealed && result) {
      if (i === result.correct_index) return "right";
      if (i === result.chosen) return "wrong";
      return "dim";
    }
    if (locked === null) return "";
    return i === locked ? "locked" : "dim";
  }
</script>

<div class="question-screen" class:dark={submitted && !revealed} class:sweeping>
  <div class="backdrop" in:crossfade|global out:crossfade|global>
    {#if media.type === "video" && media.file_url}
      <!-- svelte-ignore a11y_media_has_caption -->
      <video bind:this={player} src={src(media.file_url)} autoplay onended={mediaEnded} onerror={() => (mediaFailed = true)}></video>
    {:else if picture && !mediaFailed}
      <img src={picture} alt="" class:blurred={decorative} onerror={() => (mediaFailed = true)} />
    {/if}
    {#if decorative && !mediaFailed}<div class="mark">?</div>{/if}
  </div>
  {#if media.type === "audio" && media.file_url}
    <audio bind:this={player} src={src(media.file_url)} autoplay onended={mediaEnded} onerror={() => (mediaFailed = true)}></audio>
  {/if}

  <div class="top">
    <Hud {level} player={playerName} />
  </div>

  {#if swappedBy?.joker === "easier"}
    <div class="dial-spot"><DifficultyDial from={swappedBy.from} to={swappedBy.to} /></div>
  {/if}

  <header class="card glass-strong" class:long in:cardFlip|global={{ side: "in" }} out:cardFlip|global={{ side: "out" }}>
    {#if question.swapped_to}
      <p class="topic label" class:fresh={swappedBy?.joker === "category"}>Tema: {question.swapped_to}</p>
    {/if}
    <h1>{question.question}</h1>
    {#if media.type !== "image"}
      <button class="replay" onclick={replay}>
        <Icon name={media.type === "audio" ? "speaker" : "film"} /> repetir <kbd>R</kbd>
      </button>
    {/if}
  </header>

  <div class="middle" out:crossfade|global>
    {#if question.hints.length}
      <div class="notes">
        {#each question.hints as hint, i (i)}
          <p class="note" style:--tilt="{[-2.5, 1.8, -1.2][i]}deg" class:strong={i === 2}>
            <span class="note-label">Soplo {i + 1}</span>{hint}
          </p>
        {/each}
      </div>
    {/if}
    {#if mediaFailed || (!media.file_url && media.type !== "audio")}
      <Placeholder task="IMG" label="medio no disponible (¿falta `python3 tools/media.py sync`?)" chip />
    {/if}
  </div>

  <aside class="tray">
    <JokerTray
      jokers={submitted ? null : jokers}
      hintsLeft={3 - question.hints.length}
      {armed}
      away={flight?.name ?? null}
      {popping}
      onpress={press}
    />
  </aside>
  {#if flight}
    {@const f = flight}
    <JokerFlight from={f.from} icon={TOKENS.find((t) => t.name === f.name)!.icon} ondone={f.done} />
  {/if}

  {#if mode === "skip" && jokers}
    <div class="backdrop-dim">
      <div class="dialog glass-strong">
        <h2>Paso</h2>
        <button class="candy" onclick={() => fire({ joker: "skip" })}>Paso <kbd>1</kbd></button>
        <button
          class="secondary purge"
          onclick={() => fire({ joker: "skip", purge: true })}
          disabled={!jokers.skip.purge.available}
        >
          Paso, y fuera el tema «{jokers.skip.purge.subcategory}» <kbd>2</kbd>
          {#if jokers.skip.purge.reason}<span class="reason">{jokers.skip.purge.reason}</span>{/if}
        </button>
        <button class="secondary" onclick={() => (mode = null)}>Cancelar <kbd>Esc</kbd></button>
      </div>
    </div>
  {/if}
  {#if shredding}<Shredder name={shredding.name} ondone={shredding.done} />{/if}
  {#if mode === "category" && jokers}
    <CategoryPicker
      bind:this={picker}
      categories={jokers.category.categories}
      onpick={(subcategory) => fire({ joker: "category", subcategory })}
      oncancel={() => (mode = null)}
    />
  {/if}
  {#if hole}
    <div
      class="scope"
      class:tight={shot !== null}
      style:left="{hole.x}px"
      style:top="{hole.y}px"
      style:width="{hole.w + 40}px"
      style:height="{hole.h + 40}px"
      aria-hidden="true"
    >
      <span class="reticle"><Icon name="crosshair" size="100%" /></span>
    </div>
  {/if}
  {#if mode === "snipe"}
    <p class="aim-hint glass-strong">
      <Icon name="crosshair" /> Elijan la respuesta que creen que es <b>falsa</b> · <kbd>Enter</kbd> dispara ·
      <kbd>Esc</kbd> cancela
    </p>
  {/if}
  {#if hit !== null}
    <p class="aim-hint hit glass-strong">¡Le dieron a la correcta! Este nivel se repite.</p>
  {/if}

  <footer in:cardFlip|global={{ side: "in" }} out:cardFlip|global={{ side: "out" }}>
    <div class="answers">
      {#each question.answers as answer, i (i)}
        <button
          class="answer glass {answerClass(i)}"
          onclick={() => tap(i)}
          onmouseenter={() => mode === "snipe" && !question.struck.includes(i) && (target = i)}
          disabled={submitted || question.struck.includes(i) || hit !== null}
          class:shatter={shattering === i}
          bind:this={tiles[i]}
        >
          {#if shattering === i}
            <span class="shards" aria-hidden="true">
              {#each Array.from({ length: 10 }, (_, s) => s) as s (s)}
                <i style:--x="{(s % 5) * 20 + 10}%" style:--y="{s < 5 ? 25 : 75}%" style:--r="{(s * 67) % 360}deg" style:--d="{s * 0.02}s"></i>
              {/each}
            </span>
          {/if}
          <span class="letter">{LETTERS[i]}</span>
          <span class="text">{answer}</span>
          {#if hit === i}
            <span class="badge"><Icon name="check" /></span>
          {:else if question.struck.includes(i)}
            <span class="badge"><Icon name="cross" /></span>

          {:else if revealed && result && i === result.correct_index}
            <span class="badge"><Icon name="check" /></span>
          {:else if revealed && result && i === result.chosen}
            <span class="badge"><Icon name="cross" /></span>
          {:else if locked === i}
            <span class="badge"><Icon name="lock" /></span>
          {/if}
        </button>
      {/each}
    </div>

    <div class="final">
      {#if error}
        <p class="error">No se pudo enviar la respuesta: {error}</p>
      {:else if submitted}
        {#if !revealed}<p class="waiting">Respuesta final…</p>{/if}
      {:else}
        <button class="candy final-button" class:ready onclick={submit} disabled={!ready} tabindex={ready ? 0 : -1}>
          Respuesta final <kbd>Enter</kbd>
        </button>
        <div class="padlock" class:shaking={locked !== null && !ready} class:open={ready} aria-hidden="true">
          <Icon name={ready ? "unlock" : "lock"} size="100%" />
        </div>
        {#if locked === null}<p class="prompt label">Elijan una respuesta</p>{/if}
      {/if}
    </div>
  </footer>

  {#if credits}<p class="credit glass-light">{credits}</p>{/if}
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
  .backdrop {
    position: absolute;
    inset: 0;
    z-index: -1;
    background: var(--night-900);
  }
  .backdrop img,
  .backdrop video {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: filter 0.6s;
  }
  .backdrop img.blurred {
    filter: blur(calc(1.4 * var(--u))) brightness(0.6);
    transform: scale(1.06);
  }
  .dark .backdrop img,
  .dark .backdrop video {
    filter: brightness(0.4) saturate(0.3);
  }
  .dark .backdrop img.blurred {
    filter: blur(calc(1.4 * var(--u))) brightness(0.3) saturate(0.3);
  }
  .mark {
    position: absolute;
    inset: 0;
    display: grid;
    place-items: center;
    font-family: var(--font-display);
    font-size: calc(30 * var(--u));
    font-weight: 800;
    color: var(--paper);
    opacity: 0.12;
  }

  .top {
    justify-self: start;
  }
  .card {
    max-width: 70%;
    padding: calc(1.3 * var(--u)) calc(2.4 * var(--u));
    text-align: center;
    animation: arrive 0.5s var(--spring) backwards;
  }
  h1 {
    margin: 0;
    font-size: calc(2.4 * var(--u));
    font-weight: 800;
    line-height: 1.25;
    text-wrap: balance;
  }
  .long h1 {
    font-size: calc(2.1 * var(--u));
  }
  .replay {
    display: inline-flex;
    align-items: center;
    gap: calc(0.5 * var(--u));
    margin-top: calc(0.6 * var(--u));
    padding: calc(0.2 * var(--u)) calc(0.8 * var(--u));
    border: 1px solid var(--glass-line);
    border-radius: calc(0.8 * var(--u));
    background: none;
    font-size: calc(1.1 * var(--u));
    color: var(--slate-200);
  }
  /* «Paso»: everything on the question is swept off to the side (JK-6). */
  .sweeping .card,
  .sweeping .middle,
  .sweeping footer {
    transition:
      transform var(--sweep, 0.55s) cubic-bezier(0.6, 0, 0.9, 0.5),
      opacity var(--sweep, 0.55s);
    transform: translateX(-120vw) rotate(-8deg);
    opacity: 0;
  }
  .sweeping footer {
    transition-delay: 0.08s;
  }
  .middle {
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: center;
    gap: calc(0.8 * var(--u));
  }
  .topic {
    margin: 0 0 calc(0.3 * var(--u));
    color: var(--sky);
  }
  .topic.fresh {
    animation: topic-pop 0.7s 0.65s var(--spring) backwards;
  }
  @keyframes topic-pop {
    from {
      opacity: 0;
      transform: scale(2.2);
    }
  }
  .dial-spot {
    position: absolute;
    top: var(--safe-y);
    right: var(--safe-x);
    z-index: 2;
  }
  .notes {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: calc(1 * var(--u));
    max-width: 70vw;
  }
  .note {
    margin: 0;
    max-width: calc(26 * var(--u));
    padding: calc(0.7 * var(--u)) calc(1 * var(--u));
    border-radius: calc(0.4 * var(--u));
    background: var(--cream);
    color: var(--ink);
    font-size: calc(1.3 * var(--u));
    font-weight: 700;
    line-height: 1.25;
    box-shadow: 0 calc(0.5 * var(--u)) calc(1 * var(--u)) rgba(0, 0, 0, 0.4);
    transform: rotate(var(--tilt));
    animation: note-in 0.5s var(--spring) backwards;
  }
  .note.strong {
    background: #ffe7a8;
  }
  .note-label {
    display: block;
    font-family: var(--font-display);
    font-size: calc(0.9 * var(--u));
    color: var(--amber-deep);
    text-transform: uppercase;
    letter-spacing: 0.08em;
  }
  .backdrop-dim {
    position: absolute;
    inset: 0;
    z-index: 5;
    display: grid;
    place-items: center;
    background: rgba(5, 8, 16, 0.55);
  }
  .dialog {
    display: flex;
    flex-direction: column;
    align-items: stretch;
    gap: calc(0.9 * var(--u));
    min-width: calc(36 * var(--u));
    padding: calc(1.8 * var(--u)) calc(2.2 * var(--u));
    text-align: center;
    animation: arrive 0.35s var(--spring) backwards;
  }
  .dialog h2 {
    margin: 0;
    font-family: var(--font-display);
    font-size: calc(2.6 * var(--u));
  }
  .dialog .candy,
  .dialog .secondary {
    justify-content: center;
  }
  .purge {
    flex-direction: column;
  }
  .reason {
    font-family: var(--font-text);
    font-size: calc(1.1 * var(--u));
    color: var(--slate-200);
  }
  .aim-hint {
    position: absolute;
    z-index: 7;
    left: 50%;
    top: 45%;
    transform: translateX(-50%);
    margin: 0;
    padding: calc(0.6 * var(--u)) calc(1.4 * var(--u));
    font-family: var(--font-display);
    font-size: calc(1.4 * var(--u));
    font-weight: 700;
    white-space: nowrap;
  }
  .aim-hint.hit {
    color: var(--mint);
    font-size: calc(2 * var(--u));
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
  .answers {
    width: 100%;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: calc(1 * var(--u)) calc(1.2 * var(--u));
  }
  .answer {
    display: flex;
    align-items: center;
    gap: calc(1 * var(--u));
    padding: calc(0.9 * var(--u)) calc(1.2 * var(--u));
    border-color: var(--slate-600);
    font-size: calc(1.9 * var(--u));
    font-weight: 700;
    text-align: left;
    transition:
      transform 0.2s var(--spring),
      opacity 0.3s,
      filter 0.3s,
      border-color 0.2s,
      box-shadow 0.2s,
      background 0.3s;
    animation: arrive 0.5s var(--spring) backwards;
  }
  .answer:nth-child(2) {
    animation-delay: 0.06s;
  }
  .answer:nth-child(3) {
    animation-delay: 0.12s;
  }
  .answer:nth-child(4) {
    animation-delay: 0.18s;
  }
  .answer:hover:not(:disabled),
  .answer:focus-visible {
    border-color: var(--sky);
    transform: translateY(calc(-0.3 * var(--u)));
  }
  .letter {
    flex: none;
    display: grid;
    place-items: center;
    width: calc(2.6 * var(--u));
    height: calc(2.6 * var(--u));
    border-radius: 50%;
    background: var(--night-900);
    color: var(--amber);
    font-family: var(--font-display);
    font-size: calc(1.5 * var(--u));
    font-weight: 800;
    text-shadow: none;
  }
  .text {
    flex: 1;
  }
  .badge {
    flex: none;
    display: grid;
    place-items: center;
    font-size: calc(1.8 * var(--u));
  }
  .answer.locked {
    border: calc(0.25 * var(--u)) solid var(--amber);
    box-shadow: 0 0 calc(1.6 * var(--u)) rgba(255, 184, 28, 0.45);
    transform: scale(1.02);
  }
  .answer.locked .badge {
    color: var(--amber);
    animation: clunk 0.35s var(--spring);
  }
  .answer.dim {
    opacity: 0.45;
    filter: saturate(0.4);
  }
  .answer.struck {
    opacity: 0.35;
    filter: grayscale(1);
    text-decoration: line-through;
    text-decoration-color: var(--coral);
    text-decoration-thickness: calc(0.2 * var(--u));
  }
  .answer.struck .badge {
    color: var(--coral);
  }
  .scope {
    position: fixed;
    z-index: 6;
    border-radius: 50%;
    transform: translate(-50%, -50%);
    box-shadow: 0 0 0 200vmax rgba(5, 8, 16, 0.62);
    pointer-events: none;
    transition:
      left 0.25s var(--spring),
      top 0.25s var(--spring),
      width 0.25s,
      height 0.25s,
      box-shadow 0.4s;
    animation: scope-in 0.35s ease-out;
  }
  .scope.tight {
    width: calc(var(--u) * 26) !important;
    box-shadow: 0 0 0 200vmax rgba(5, 8, 16, 0.85);
  }
  .reticle {
    position: absolute;
    left: 50%;
    top: 50%;
    width: calc(7 * var(--u));
    height: calc(7 * var(--u));
    transform: translate(-50%, -50%);
    color: var(--coral);
    filter: drop-shadow(0 0 calc(0.5 * var(--u)) rgba(255, 84, 112, 0.8));
    animation: spin 3s linear infinite;
  }
  .tight .reticle {
    animation: spin 0.8s linear infinite;
  }
  @keyframes scope-in {
    from {
      box-shadow: 0 0 0 200vmax rgba(5, 8, 16, 0);
    }
  }
  .answer {
    position: relative;
  }
  .answer.shatter {
    z-index: 7;
  }
  .answer.shatter {
    background: var(--coral);
    animation: shake 0.3s ease-in-out 2;
  }
  .shards {
    position: absolute;
    inset: 0;
    pointer-events: none;
  }
  .shards i {
    position: absolute;
    left: var(--x);
    top: var(--y);
    width: calc(3.2 * var(--u));
    height: calc(2.6 * var(--u));
    background: linear-gradient(135deg, rgba(238, 241, 246, 0.85), rgba(255, 84, 112, 0.6));
    clip-path: polygon(0 0, 100% 30%, 40% 100%);
    animation: shard 0.8s var(--d) cubic-bezier(0.3, 0, 0.8, 0.6) forwards;
  }
  @keyframes shard {
    from {
      transform: translate(-50%, -50%) rotate(var(--r));
    }
    to {
      transform: translate(calc(-50% + (var(--x) - 50%) * 3), 40vh) rotate(calc(var(--r) + 220deg));
      opacity: 0;
    }
  }
  .answer.target {
    border: calc(0.25 * var(--u)) solid var(--coral);
    box-shadow: 0 0 calc(1.6 * var(--u)) rgba(255, 84, 112, 0.45);
  }
  .crosshair {
    color: var(--coral);
    animation: spin 2.5s linear infinite;
  }
  @keyframes spin {
    to {
      transform: rotate(360deg);
    }
  }
  @keyframes note-in {
    from {
      opacity: 0;
      transform: translateY(calc(-2 * var(--u))) rotate(-10deg) scale(0.7);
    }
  }
  .answer.right {
    border-color: var(--mint);
    background: var(--mint);
    color: var(--night-900);
    text-shadow: none;
    animation: pop 0.6s var(--spring);
  }
  .answer.wrong {
    border-color: var(--coral);
    background: var(--coral);
    color: var(--night-900);
    text-shadow: none;
    animation: shake 0.45s ease-in-out 3;
  }
  .answer.right .letter,
  .answer.wrong .letter {
    background: rgba(11, 17, 32, 0.85);
  }

  .final {
    position: relative;
    min-height: calc(5.5 * var(--u));
    display: grid;
    place-items: center;
  }
  .final > * {
    grid-area: 1 / 1;
  }
  .final-button {
    opacity: 0;
    transform: scale(0.85);
    transition:
      opacity 0.3s,
      transform 0.4s var(--spring);
  }
  .final-button.ready {
    opacity: 1;
    transform: none;
  }
  .padlock {
    width: calc(5 * var(--u));
    height: calc(5 * var(--u));
    color: var(--slate-200);
    filter: drop-shadow(0 calc(0.3 * var(--u)) calc(0.6 * var(--u)) rgba(0, 0, 0, 0.6));
    transition:
      transform 0.6s var(--spring),
      opacity 0.5s,
      color 0.2s;
    pointer-events: none;
  }
  .padlock.shaking {
    color: var(--amber);
    animation: jiggle 0.8s ease-in-out;
  }
  .padlock.open {
    color: var(--amber);
    opacity: 0;
    transform: translate(calc(14 * var(--u)), calc(1 * var(--u))) rotate(35deg) scale(0.7);
  }
  .prompt {
    position: absolute;
    left: calc(50% + 3.5 * var(--u));
    margin: 0;
    white-space: nowrap;
    text-shadow: var(--text-shadow);
  }
  .waiting {
    margin: 0;
    font-family: var(--font-display);
    font-size: calc(2 * var(--u));
    font-weight: 700;
    color: var(--amber);
    text-shadow: var(--text-shadow);
    animation: pulse 1.2s ease-in-out infinite;
  }
  .error {
    margin: 0;
    color: var(--coral);
    font-size: calc(1.1 * var(--u));
  }
  .credit {
    position: absolute;
    right: var(--safe-x);
    bottom: calc(var(--safe-y) * 0.3);
    margin: 0;
    padding: calc(0.15 * var(--u)) calc(0.7 * var(--u));
    border-radius: calc(0.6 * var(--u));
    font-size: calc(0.8 * var(--u));
    color: var(--slate-200);
  }

  @keyframes arrive {
    from {
      opacity: 0;
      transform: translateY(calc(1.5 * var(--u))) scale(0.96);
    }
  }
  @keyframes pop {
    40% {
      transform: scale(1.06);
    }
  }
  @keyframes shake {
    25% {
      transform: translateX(calc(-0.5 * var(--u)));
    }
    75% {
      transform: translateX(calc(0.5 * var(--u)));
    }
  }
  @keyframes clunk {
    from {
      transform: translateY(-60%) scale(1.4);
    }
  }
  @keyframes jiggle {
    15%,
    45%,
    75% {
      transform: rotate(-9deg);
    }
    30%,
    60%,
    90% {
      transform: rotate(9deg);
    }
  }
  @keyframes pulse {
    50% {
      opacity: 0.45;
    }
  }
</style>
