<script lang="ts">
  // The Question screen (04-ui-tv-display.md): media, question, 4 answers, the lock-in
  // mechanic, the final answer, the level-dependent wait and the reveal.
  import { onMount } from "svelte";
  import { gameAction } from "../lib/api";
  import type { Game } from "../lib/types";
  import Placeholder from "./Placeholder.svelte";
  import { music, sfx } from "./sound.svelte";
  import { AFTER_REVEAL_MS, PADLOCK_MS, REVEAL_WAIT_S, sleep } from "./timing";

  let {
    question,
    level,
    paused,
    onanswered,
  }: {
    question: NonNullable<Game["question"]>;
    level: number;
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
    // PLACEHOLDER(UI-12): the padlock just waits, then the button appears; no animation.
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

  <header>
    <h1>{question.question}</h1>
    {#if media.type !== "image"}
      <p class="replay">{media.type === "audio" ? "🔊" : "🎬"} <kbd>R</kbd> repetir</p>
    {/if}
  </header>

  <div class="middle">
    {#if mediaFailed || (!media.file_url && media.type !== "audio")}
      <Placeholder task="IMG" label="medio no disponible (¿falta `python3 tools/media.py sync`?)" chip />
    {/if}
    <!-- PLACEHOLDER(JK-4, JK-6): hints only come through the «Pista» joker (D-26); tray and notes go here. -->
    <Placeholder task="JK-4 · JK-6" label="comodines y notas de «Pista»" chip />
  </div>

  <footer>
    <div class="answers">
      {#each question.answers as answer, i (i)}
        <button class="answer {answerClass(i)}" onclick={() => tap(i)} disabled={submitted}>
          <span class="letter">{LETTERS[i]}</span>
          <span>{answer}</span>
          {#if locked === i && !revealed}<span class="lock-icon">🔒</span>{/if}
        </button>
      {/each}
    </div>

    <div class="final">
      {#if error}
        <p class="error">No se pudo enviar la respuesta: {error}</p>
      {/if}
      {#if submitted}
        {#if !revealed}<p class="waiting">Respuesta final…</p>{/if}
      {:else if ready}
        <button class="final-button" onclick={submit}>Respuesta final <kbd>Enter</kbd></button>
      {:else}
        <Placeholder task="UI-12" label={locked === null ? "🔒 candado (elige una respuesta)" : "🔒 el candado se abre…"} chip />
      {/if}
    </div>
  </footer>

  {#if credits}<p class="credit">{credits}</p>{/if}
</div>

<style>
  .question-screen {
    position: absolute;
    inset: 0;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }
  .backdrop {
    position: absolute;
    inset: 0;
    z-index: -1;
    background: #000;
  }
  .backdrop img,
  .backdrop video {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: filter 0.6s;
  }
  .backdrop img.blurred {
    filter: blur(1.2vw) brightness(0.6);
    transform: scale(1.06);
  }
  .dark .backdrop img,
  .dark .backdrop video {
    filter: brightness(0.35);
  }
  .mark {
    position: absolute;
    inset: 0;
    display: grid;
    place-items: center;
    font-size: 40vh;
    font-weight: 800;
    color: rgba(255, 255, 255, 0.18);
  }
  header {
    padding: 3vh 5vw 5vh;
    background: linear-gradient(rgba(0, 0, 0, 0.85), rgba(0, 0, 0, 0.6) 70%, transparent);
    text-align: center;
  }
  h1 {
    margin: 0;
    font-size: 3.4vw;
    line-height: 1.2;
  }
  .replay {
    margin: 1vh 0 0;
    font-size: 1.4vw;
    color: var(--muted);
  }
  .middle {
    display: flex;
    justify-content: center;
    gap: 1rem;
  }
  footer {
    padding: 4vh 5vw 3vh;
    background: linear-gradient(transparent, rgba(0, 0, 0, 0.75) 25%);
  }
  .answers {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 2vh 2vw;
  }
  .answer {
    display: flex;
    align-items: center;
    gap: 1.2vw;
    padding: 2.2vh 2vw;
    font: inherit;
    font-size: 2.4vw;
    text-align: left;
    color: var(--text);
    background: rgba(35, 37, 47, 0.92);
    border: 0.3vw solid rgba(255, 255, 255, 0.15);
    border-radius: 1vw;
    cursor: pointer;
    transition: opacity 0.3s, border-color 0.3s, background 0.3s;
  }
  .answer:disabled {
    cursor: default;
  }
  .letter {
    font-weight: 800;
    color: var(--accent);
  }
  .lock-icon {
    margin-left: auto;
  }
  .answer.locked {
    border-color: var(--accent);
    background: rgba(80, 64, 20, 0.95);
  }
  .answer.dim {
    opacity: 0.45;
  }
  .answer.right {
    border-color: var(--good);
    background: var(--good-bg);
    animation: flash 0.5s 3;
  }
  .answer.wrong {
    border-color: var(--bad);
    background: #4a1f24;
    animation: flash 0.5s 3;
  }
  @keyframes flash {
    50% {
      opacity: 0.5;
    }
  }
  .final {
    min-height: 9vh;
    margin-top: 2.5vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
  }
  .final-button {
    font: inherit;
    font-size: 2.6vw;
    font-weight: 800;
    padding: 1.5vh 4vw;
    border: none;
    border-radius: 1vw;
    background: var(--accent);
    color: #1a1a1a;
    cursor: pointer;
  }
  .final-button kbd {
    font-size: 1.2vw;
    opacity: 0.6;
  }
  .waiting {
    margin: 0;
    font-size: 2.4vw;
    animation: flash 1s infinite;
  }
  .error {
    color: var(--bad);
    font-size: 1.4vw;
  }
  .credit {
    position: absolute;
    right: 1vw;
    bottom: 0.5vh;
    margin: 0;
    font-size: 0.8vw;
    color: rgba(255, 255, 255, 0.45);
  }
</style>
