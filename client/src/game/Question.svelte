<script lang="ts">
  // The Question screen (04-ui-tv-display.md): media, question, 4 answers, the lock-in
  // mechanic, the final answer, the level-dependent wait and the reveal.
  import { onMount } from "svelte";
  import { gameAction } from "../lib/api";
  import type { Game } from "../lib/types";
  import Hud from "./Hud.svelte";
  import Icon from "./Icon.svelte";
  import Placeholder from "./Placeholder.svelte";
  import { music, sfx } from "./sound.svelte";
  import { AFTER_REVEAL_MS, PADLOCK_MS, REVEAL_WAIT_S, sleep } from "./timing";

  let {
    question,
    level,
    playerName,
    paused,
    onanswered,
  }: {
    question: NonNullable<Game["question"]>;
    level: number;
    /** For the HUD (D-28). */
    playerName: string | null;
    /** The admin overlay is open: the wait before the reveal stops. */
    paused: boolean;
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
    return () => clearTimeout(padlockTimer);
  });

  function mediaEnded() {
    if (!submitted) music("question");
  }

  function tap(i: number) {
    if (submitted) return;
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

  export function key(e: KeyboardEvent) {
    const k = e.key.toLowerCase();
    const i = "abcd".indexOf(k) >= 0 ? "abcd".indexOf(k) : "1234".indexOf(k);
    if (k.length === 1 && i >= 0) tap(i);
    else if (e.key === "Backspace") unlock();
    else if (e.key === "Enter" || e.key === " ") submit();
    else if (k === "r") replay();
    else return;
    e.preventDefault();
  }

  /** Long questions shrink one step instead of growing to three lines (10, "Scale"). */
  const long = $derived(question.question.length > 110);

  function answerClass(i: number) {
    if (revealed && result) {
      if (i === result.correct_index) return "right";
      if (i === result.chosen) return "wrong";
      return "dim";
    }
    if (locked === null) return "";
    return i === locked ? "locked" : "dim";
  }
</script>

<div class="question-screen" class:dark={submitted && !revealed}>
  <div class="backdrop">
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

  <header class="card glass-strong" class:long>
    <h1>{question.question}</h1>
    {#if media.type !== "image"}
      <button class="replay" onclick={replay}>
        <Icon name={media.type === "audio" ? "speaker" : "film"} /> repetir <kbd>R</kbd>
      </button>
    {/if}
  </header>

  <div class="middle">
    {#if mediaFailed || (!media.file_url && media.type !== "audio")}
      <Placeholder task="IMG" label="medio no disponible (¿falta `python3 tools/media.py sync`?)" chip />
    {/if}
  </div>

  <aside class="tray">
    <!-- PLACEHOLDER(JK-4, JK-6): the joker tray runs down this strip; «Soplo» notes go under the question (D-26). -->
    <Placeholder task="JK-4 · JK-6" label="comodines" chip />
  </aside>

  <footer>
    <div class="answers">
      {#each question.answers as answer, i (i)}
        <button class="answer glass {answerClass(i)}" onclick={() => tap(i)} disabled={submitted}>
          <span class="letter">{LETTERS[i]}</span>
          <span class="text">{answer}</span>
          {#if revealed && result && i === result.correct_index}
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
  .middle {
    display: flex;
    justify-content: center;
    align-items: flex-start;
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
