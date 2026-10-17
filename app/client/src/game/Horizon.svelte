<script lang="ts">
  // Start's skyline (plan 150): Commons cut-outs from public/horizon/ (CREDITS.md), the same in every language.
  // Two layers on a bowl-shaped ground: landmarks and nature behind, objects and animals in front.
  // Height share of the band; items spread evenly across the width, in an order that avoids clusters.
  const BACK: { file: string; share: number }[] = [
    { file: "castle", share: 0.75 },
    { file: "windmill", share: 0.6 },
    { file: "empire-state", share: 1 },
    { file: "chinese-house", share: 0.6 },
    { file: "lighthouse", share: 0.9 },
    { file: "colosseum", share: 0.55 },
    { file: "eiffel-tower", share: 1 },
    { file: "easter-island", share: 0.6 },
    { file: "nairobi-skyline", share: 0.7 },
    { file: "volcano", share: 0.8 },
    { file: "big-ben", share: 0.95 },
    { file: "opera-house", share: 0.55 },
    { file: "cactus", share: 0.7 },
    { file: "royal-palace", share: 0.65 },
    { file: "leaning-tower", share: 0.9 },
    { file: "acacia-tree", share: 0.6 },
  ];
  const FRONT: { file: string; share: number }[] = [
    { file: "toucan", share: 0.36 },
    { file: "taco", share: 0.3 },
    { file: "drum", share: 0.38 },
    { file: "penguin", share: 0.34 },
    { file: "violin", share: 0.42 },
    { file: "elephant", share: 0.32 },
    { file: "toy-train", share: 0.26 },
    { file: "cowboy-hat-boot", share: 0.36 },
    { file: "red-panda", share: 0.32 },
    { file: "banjo", share: 0.3 },
    { file: "turtle", share: 0.28 },
    { file: "lion", share: 0.38 },
    { file: "teapot", share: 0.32 },
    { file: "taiko", share: 0.32 },
    { file: "ukulele", share: 0.4 },
    { file: "orca", share: 0.26 },
    { file: "rocking-horse", share: 0.32 },
    { file: "balalaika", share: 0.28 },
    { file: "airplane", share: 0.26 },
  ];
  // Ground rises towards both edges: share of the band at the outermost item.
  const RISE = { back: 0.32, front: 0.16 };

  function place(items: { file: string; share: number }[], rise: number, phase: number) {
    return items.map((item, i) => {
      const x = (i + 0.5) / items.length;
      const lift = rise * (2 * x - 1) ** 2;
      return {
        file: item.file,
        x: (x * 100).toFixed(1),
        lift: lift.toFixed(3),
        share: Math.min(item.share, 1 - lift).toFixed(3),
        delay: -(((i + phase) * 1.7) % 7).toFixed(1),
        dur: 6 + ((i + phase) % 4),
      };
    });
  }
  const layers = [place(BACK, RISE.back, 0), place(FRONT, RISE.front, 2)];
</script>

<div class="horizon" aria-hidden="true">
  {#each layers as layer, l (l)}
    <div class="layer">
      {#each layer as item (item.file)}
        <img
          src="/horizon/{item.file}.webp"
          alt=""
          draggable="false"
          style="--x: {item.x}%; --lift: {item.lift}; --share: {item.share}; --delay: {item.delay}s; --dur: {item.dur}s"
        />
      {/each}
    </div>
  {/each}
</div>

<style>
  .horizon {
    position: absolute;
    inset: auto 0 0;
    --band: 33.3vh;
    height: var(--band);
    overflow: hidden;
    pointer-events: none;
    background: radial-gradient(ellipse 70% 60% at 50% 110%, color-mix(in srgb, var(--amber) 28%, transparent), color-mix(in srgb, var(--coral) 10%, transparent) 55%, transparent 80%),
      linear-gradient(to top, color-mix(in srgb, var(--sky) 14%, transparent), transparent 40%);
    mask-image: linear-gradient(to bottom, transparent, var(--night-800) 35%);
    filter: saturate(0.85);
  }
  .layer {
    position: absolute;
    inset: 0;
  }
  img {
    position: absolute;
    left: var(--x);
    bottom: calc(var(--lift) * var(--band));
    translate: -50% 0;
    height: calc(var(--share) * var(--band));
    width: auto;
    user-select: none;
    animation: sway var(--dur) ease-in-out var(--delay) infinite;
  }
  @keyframes sway {
    50% {
      transform: translateY(calc(-0.4 * var(--u)));
    }
  }
</style>
