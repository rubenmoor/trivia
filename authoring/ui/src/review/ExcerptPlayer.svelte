<script lang="ts">
  // Plays an excerpt's window start→end like game/question/Media.svelte (decision 644): same playWindow,
  // polled stop, replay from the start, the game's media volume.
  import { playWindow } from "$app/engine/pool.ts";
  import { mediaVolume } from "$app/game/sound.svelte.ts";
  import type { Excerpt } from "$app/lib/types.ts";

  let { src, type, excerpt }: { src: string; type: "audio" | "video"; excerpt: Excerpt } = $props();

  let player = $state<HTMLMediaElement>();
  let playing = $state(false);
  let watch: ReturnType<typeof setInterval> | undefined;

  function stop() {
    clearInterval(watch);
    player?.pause();
    playing = false;
  }

  function play() {
    if (!player) return;
    stop();
    const w = playWindow(type, excerpt, player.duration) ?? { start: 0, end: player.duration };
    player.volume = mediaVolume();
    player.currentTime = w.start;
    watch = setInterval(() => {
      if (player && player.currentTime >= w.end) stop();
    }, 40);
    playing = true;
    player.play().catch(stop);
  }

  $effect(() => () => clearInterval(watch));
</script>

{#if type === "video"}
  <!-- svelte-ignore a11y_media_has_caption -->
  <video bind:this={player} {src} preload="auto" onended={stop}></video>
{:else}
  <audio bind:this={player} {src} preload="auto" onended={stop}></audio>
{/if}
<button class="play" onclick={() => (playing ? stop() : play())}>
  {playing ? "■ stop" : "▶ play the excerpt"} ({excerpt.start}–{excerpt.end} s)
</button>

<style>
  video {
    display: block;
    width: 100%;
    border-radius: 8px;
  }
  .play {
    margin-top: 0.4rem;
  }
</style>
