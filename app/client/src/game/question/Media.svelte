<script lang="ts">
  // The question's media (04-ui-tv-display.md): backdrop picture or video, the audio, the decorative mark, the credit.
  // Ready once loaded (UI-7); starts with the fade-in, not behind the black or while the overlay is open.
  import { onMount } from "svelte";
  import type { Game } from "../../lib/types.ts";
  import { mediaVolume, music } from "../sound.svelte.ts";
  import Stage from "../Stage.svelte";
  import { crossfade } from "../swap.ts";

  let {
    question,
    shown,
    paused,
    dark,
    failed = $bindable(false),
    onended,
  }: {
    question: NonNullable<Game["question"]>;
    /** False while the screen sits behind the black of a transition. */
    shown: boolean;
    paused: boolean;
    /** The final answer is out: the backdrop darkens until the reveal. */
    dark: boolean;
    /** The media is missing or broken. */
    failed?: boolean;
    /** The audio/video ended, or failed to play. */
    onended: () => void;
  } = $props();

  /** A sharp image's native size in CSS px at this screen's pixel density (D-51). */
  let native = $state<{ w: number; h: number } | null>(null);
  function measure(e: Event) {
    const img = e.currentTarget as HTMLImageElement;
    native = { w: img.naturalWidth / devicePixelRatio, h: img.naturalHeight / devicePixelRatio };
  }
  let player = $state<HTMLMediaElement>();
  let started = false;

  const media = $derived(question.media);
  /** Ours from the media cache; a mod's under /data/ (decision 128). */
  const src = (url: string | null) => (url ? (url.startsWith("/data/") ? url : `/media?url=${encodeURIComponent(url)}`) : null);
  /** The picture: the image itself, or an audio question's background (D-14). */
  const picture = $derived(media.type === "image" ? src(media.file_url) : src(question.background?.file_url ?? null));
  const decorative = $derived(media.type === "audio" || media.role === "decorative");
  const credits = $derived(
    [media.credit, media.type === "audio" ? question.background?.credit : null].filter(Boolean).join(" · "),
  );

  // UI-7: ready once the picture and the audio/video have loaded; any failure ends the wait.
  const waiting = new Set<"picture" | "player">();
  // svelte-ignore state_referenced_locally
  if (picture && media.type !== "video") waiting.add("picture");
  // svelte-ignore state_referenced_locally
  if (media.type !== "image" && media.file_url) waiting.add("player");
  let settleAll: () => void;
  const settled = new Promise<void>((resolve) => (settleAll = resolve));
  function settle(what: "picture" | "player") {
    waiting.delete(what);
    if (!waiting.size) settleAll();
  }
  if (!waiting.size) settleAll!();
  function fail() {
    failed = true;
    settleAll();
  }
  /** Resolves once the media is ready to show (or failed). */
  export function ready() {
    return settled;
  }

  $effect(() => {
    if (!shown || paused || !player || started) return;
    started = true;
    player.play().catch(() => {});
  });

  onMount(() => {
    if (media.type !== "image" && media.file_url) music(null); // the music is off while question media plays
  });

  // The question's own audio/video follows the media volume from the admin overlay (UI-13).
  $effect(() => {
    if (player) player.volume = mediaVolume();
  });

  /** A missing audio/video: the music comes back as if it had ended. */
  function playerFailed() {
    fail();
    onended();
  }

  /** From the start; false if there is nothing to replay. */
  export function replay() {
    if (!player || failed) return false;
    player.currentTime = 0;
    player.play().catch(() => {});
    return true;
  }

  export function pause() {
    player?.pause();
  }
</script>

<div class="backdrop" class:dark in:crossfade|global out:crossfade|global>
  {#if media.type === "video" && media.file_url}
    <!-- svelte-ignore a11y_media_has_caption -->
    <video
      bind:this={player}
      src={src(media.file_url)}
      preload="auto"
      oncanplaythrough={() => settle("player")}
      onended={onended}
      onerror={playerFailed}
    ></video>
  {:else if picture && !failed && decorative}
    <img src={picture} alt="" class="blurred" onload={() => settle("picture")} onerror={fail} />
  {:else if picture && !failed}
    <Stage />
    <img
      src={picture}
      alt=""
      class="fit"
      class:ready={native}
      style:--w={native?.w}
      style:--ratio={native ? native.w / native.h : 1}
      onload={(e) => (measure(e), settle("picture"))}
      onerror={fail}
    />
  {/if}
  {#if decorative && !failed}<div class="mark">?</div>{/if}
</div>
{#if media.type === "audio" && media.file_url}
  <audio
    bind:this={player}
    src={src(media.file_url)}
    preload="auto"
    oncanplaythrough={() => settle("player")}
    onended={onended}
    onerror={playerFailed}
  ></audio>
{/if}
{#if credits}<p class="credit glass-light">{credits}</p>{/if}

<style>
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
  /* D-51: native size, down to fit, never up; rounded fade into the stage. */
  .backdrop {
    container-type: size;
  }
  .backdrop img.fit {
    --fade: min(calc(4.5 * var(--u)), 20%);
    --ramp:
      transparent, rgba(0, 0, 0, 0.12) calc(0.25 * var(--fade)), rgba(0, 0, 0, 0.5) calc(0.5 * var(--fade)),
      rgba(0, 0, 0, 0.88) calc(0.75 * var(--fade)), #000 var(--fade), #000 calc(100% - var(--fade)),
      rgba(0, 0, 0, 0.88) calc(100% - 0.75 * var(--fade)), rgba(0, 0, 0, 0.5) calc(100% - 0.5 * var(--fade)),
      rgba(0, 0, 0, 0.12) calc(100% - 0.25 * var(--fade)), transparent;
    position: absolute;
    inset: 0;
    margin: auto;
    width: min(calc(var(--w) * 1px), 100cqw, calc(100cqh * var(--ratio)));
    height: auto;
    opacity: 0;
    transition:
      filter 0.6s,
      opacity 0.3s;
    mask-image: linear-gradient(to right, var(--ramp)), linear-gradient(to bottom, var(--ramp));
    mask-composite: intersect;
  }
  .backdrop img.fit.ready {
    opacity: 1;
  }
  .backdrop img.blurred {
    filter: blur(calc(1.4 * var(--u))) brightness(0.6);
    transform: scale(1.06);
  }
  .dark img,
  .dark video {
    filter: brightness(0.4) saturate(0.3);
  }
  .dark img.blurred {
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
  .credit {
    position: absolute;
    right: var(--safe-x);
    bottom: calc(var(--safe-y) * 0.3);
    margin: 0;
    padding: calc(0.15 * var(--u)) calc(0.7 * var(--u));
    border-radius: calc(0.6 * var(--u));
    font-size: calc(0.9 * var(--u));
    color: var(--slate-200);
  }
</style>
