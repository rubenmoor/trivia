<script lang="ts">
  // Start's skyline (plan 150): Commons cut-outs from public/horizon/ (CREDITS.md), the same in every language.
  // Height share of the band, ordered so no region or silhouette type clusters.
  const ITEMS: { file: string; share: number }[] = [
    { file: "castle", share: 0.8 },
    { file: "toucan", share: 0.6 },
    { file: "lighthouse", share: 1 },
    { file: "drum", share: 0.55 },
    { file: "royal-palace", share: 0.75 },
    { file: "cactus", share: 0.7 },
    { file: "eiffel-tower", share: 1 },
    { file: "penguin", share: 0.6 },
    { file: "toy-train", share: 0.55 },
    { file: "volcano", share: 0.85 },
    { file: "ukulele", share: 0.8 },
    { file: "red-panda", share: 0.6 },
    { file: "airplane", share: 0.7 },
    { file: "teapot", share: 0.55 },
    { file: "orca", share: 0.65 },
    { file: "banjo", share: 0.8 },
  ];
</script>

<div class="horizon" aria-hidden="true">
  {#each ITEMS as item, i (item.file)}
    <img
      src="/horizon/{item.file}.webp"
      alt=""
      draggable="false"
      style="--share: {item.share}; --delay: {-((i * 1.7) % 7).toFixed(1)}s; --dur: {6 + (i % 4)}s"
    />
  {/each}
</div>

<style>
  .horizon {
    position: absolute;
    inset: auto 0 0;
    height: 33.3vh;
    display: flex;
    align-items: flex-end;
    justify-content: center;
    overflow: hidden;
    pointer-events: none;
    background: radial-gradient(ellipse 70% 60% at 50% 110%, color-mix(in srgb, var(--amber) 28%, transparent), color-mix(in srgb, var(--coral) 10%, transparent) 55%, transparent 80%),
      linear-gradient(to top, color-mix(in srgb, var(--sky) 14%, transparent), transparent 40%);
    mask-image: linear-gradient(to bottom, transparent, var(--night-800) 35%);
    filter: saturate(0.85);
  }
  img {
    flex: none;
    height: calc(var(--share) * 100%);
    width: auto;
    margin-inline: calc(-1.6 * var(--u));
    user-select: none;
    animation: sway var(--dur) ease-in-out var(--delay) infinite;
  }
  @keyframes sway {
    50% {
      transform: translateY(calc(-0.4 * var(--u)));
    }
  }
</style>
