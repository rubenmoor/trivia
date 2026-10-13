<script lang="ts">
  // The Select screen's cards: paper envelopes on the night table (VD-5, UI-11); the picked one tears open.
  import { t } from "../lib/i18n.ts";
  import { questionLocale } from "../lib/names.svelte.ts";

  let {
    options,
    picked,
    fresh,
    busy,
    seed,
    onpick,
  }: {
    options: { description: string }[];
    picked: number | null;
    fresh: Set<number>;
    busy: boolean;
    /** Game id and level: the tilts stay put on a re-render. */
    seed: { id: number; level: number };
    onpick: (i: number) => void;
  } = $props();

  /** Each card's tilt, within ±3° (10, "Cards"); fixed per game and level, so a re-render keeps it. */
  function tilt(i: number) {
    const s = (seed.id * 31 + seed.level * 7 + i * 13) % 13;
    return (s / 12) * 6 - 3;
  }
</script>

<div class="cards" style:--n={options.length}>
  {#each options as option, i (i)}
    <button
      class="card"
      class:chosen={picked === i}
      class:gone={picked !== null && picked !== i}
      class:fresh={fresh.has(i)}
      style:--tilt="{tilt(i)}deg"
      style:--deal-delay="{i * 0.12}s"
      onclick={() => picked === null && onpick(i)}
      disabled={busy}
      data-focus-default
    >
      <span class="flap"></span>
      <span class="seal">{i + 1}</span>
      {#if picked === i}
        <span class="tear"></span>
        <span class="letter-slot"><span class="letter">?</span></span>
      {/if}
      {#if fresh.has(i)}<span class="new-badge">{t("screen.select.fresh")}</span>{/if}
      <span class="description" lang={questionLocale()}>{option.description}</span>
    </button>
  {/each}
</div>

<style>
  .cards {
    display: grid;
    grid-template-columns: repeat(var(--n), minmax(0, calc(23.5 * var(--u))));
    justify-content: center;
    gap: calc(2 * var(--u));
    width: 100%;
    max-width: calc(100 * var(--u));
    margin: calc(2 * var(--u)) 0;
  }
  .card {
    /* The torn edge of the flap, shared by the flap and what it leaves behind */
    --ragged: polygon(
      0 0, 100% 0, 100% 88%, 94% 100%, 88% 86%, 81% 98%, 75% 84%, 68% 97%, 62% 87%, 55% 100%, 49% 85%,
      43% 96%, 37% 84%, 30% 99%, 24% 86%, 18% 97%, 11% 85%, 5% 98%, 0 88%
    );
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: calc(1.2 * var(--u));
    min-height: calc(26 * var(--u));
    padding: calc(5 * var(--u)) calc(1.4 * var(--u)) calc(2 * var(--u));
    border: none;
    border-radius: calc(0.8 * var(--u));
    background: var(--cream);
    color: var(--ink);
    font-size: calc(1.6 * var(--u));
    font-weight: 700;
    line-height: 1.3;
    box-shadow:
      0 calc(0.4 * var(--u)) 0 var(--cream-edge),
      0 calc(1.2 * var(--u)) calc(2.4 * var(--u)) rgba(0, 0, 0, 0.45);
    transform: rotate(var(--tilt));
    transition:
      transform 0.3s var(--spring),
      opacity 0.3s;
    animation: deal 0.6s var(--deal-delay) var(--spring) backwards;
  }
  /* The envelope flap, on a strip of paper with a ragged lower edge that tears off when picked */
  .flap {
    position: absolute;
    inset: 0 0 auto;
    height: calc(6.6 * var(--u));
    background: var(--cream);
    border-radius: calc(0.8 * var(--u)) calc(0.8 * var(--u)) 0 0;
    clip-path: var(--ragged);
    z-index: 1;
  }
  .flap::before {
    content: "";
    position: absolute;
    inset: 0 0 auto;
    height: calc(6 * var(--u));
    background: linear-gradient(to bottom, #e8dcc0, #efe4cb);
    clip-path: polygon(0 0, 100% 0, 50% 100%);
  }
  /* What the torn flap leaves behind: the shadowed inside of the envelope, with the same ragged edge */
  .tear {
    position: absolute;
    inset: 0 0 auto;
    height: calc(6.6 * var(--u));
    background: linear-gradient(to bottom, #6b5d45, #b9ab8a 70%, var(--cream-edge));
    clip-path: var(--ragged);
    animation: tear-show 0.15s 0.3s backwards;
  }
  /* The letter slides up out of the open envelope; the slot hides it below the card's top edge. */
  .letter-slot {
    position: absolute;
    left: 14%;
    right: 14%;
    bottom: calc(100% - 3 * var(--u));
    height: calc(11 * var(--u));
    overflow: hidden;
  }
  .letter {
    position: absolute;
    inset: 0;
    display: grid;
    place-items: center;
    border-radius: calc(0.4 * var(--u)) calc(0.4 * var(--u)) 0 0;
    background: repeating-linear-gradient(to bottom, #fffaf0 0 calc(1.6 * var(--u)), #e6dcc6 0 calc(1.7 * var(--u)));
    color: var(--seal);
    font-family: var(--font-display);
    font-size: calc(5 * var(--u));
    font-weight: 800;
    box-shadow: 0 0 calc(1 * var(--u)) rgba(0, 0, 0, 0.3);
    transform: translateY(100%);
    animation: letter-up 0.4s 0.58s var(--spring) forwards;
  }
  .seal {
    position: absolute;
    z-index: 2;
    top: calc(3.6 * var(--u));
    left: 50%;
    translate: -50% 0;
    display: grid;
    place-items: center;
    width: calc(4.4 * var(--u));
    height: calc(4.4 * var(--u));
    border-radius: 50%;
    background: radial-gradient(circle at 35% 30%, #e0584a, var(--seal) 60%, #8e2a20);
    color: var(--amber);
    font-family: var(--font-display);
    font-size: calc(2.2 * var(--u));
    font-weight: 800;
    box-shadow: 0 calc(0.2 * var(--u)) calc(0.4 * var(--u)) rgba(0, 0, 0, 0.35);
  }
  .description {
    margin-top: calc(2.4 * var(--u));
  }
  .card.fresh {
    box-shadow:
      0 calc(0.4 * var(--u)) 0 var(--cream-edge),
      0 0 calc(2.4 * var(--u)) rgba(76, 201, 240, 0.7);
    animation-delay: calc(var(--deal-delay) + 0.5s);
  }
  .new-badge {
    position: absolute;
    top: calc(-1 * var(--u));
    right: calc(-1 * var(--u));
    padding: calc(0.2 * var(--u)) calc(0.8 * var(--u));
    border-radius: calc(0.8 * var(--u));
    background: var(--sky);
    color: var(--night-900);
    font-family: var(--font-display);
    font-size: calc(1.3 * var(--u));
    font-weight: 800;
    transform: rotate(8deg);
    box-shadow: 0 calc(0.2 * var(--u)) calc(0.6 * var(--u)) rgba(0, 0, 0, 0.4);
  }
  .card:hover:not(:disabled),
  .card:focus-visible,
  .card:global([data-nav]) {
    transform: translateY(calc(-1.2 * var(--u))) rotate(0deg) scale(1.03);
    outline: calc(0.25 * var(--u)) solid var(--sky);
  }
  .card.chosen {
    z-index: 1;
    animation: chosen 0.5s var(--spring) forwards;
  }
  /* Tear-open (UI-11, TEAR_MS): the seal cracks off, then the flap rips away to the upper right. */
  .card.chosen .seal {
    animation: seal-crack 0.4s 0.1s ease-in forwards;
  }
  .card.chosen .flap {
    transform-origin: 0 100%;
    animation: flap-off 0.45s 0.3s ease-in forwards;
  }
  .card.gone {
    animation: gone 0.4s ease-in forwards;
  }
  @keyframes deal {
    from {
      opacity: 0;
      transform: translateY(-60vh) rotate(calc(var(--tilt) * -6));
    }
  }
  @keyframes chosen {
    40% {
      transform: rotate(0deg) scale(1.12);
    }
    to {
      transform: rotate(0deg) scale(1.06);
      box-shadow: 0 0 calc(3 * var(--u)) var(--amber);
    }
  }
  @keyframes seal-crack {
    30% {
      transform: scale(1.25) rotate(-12deg);
    }
    to {
      opacity: 0;
      transform: translate(calc(-6 * var(--u)), calc(-10 * var(--u))) scale(0.9) rotate(-70deg);
    }
  }
  @keyframes flap-off {
    20% {
      transform: rotate(-4deg);
    }
    to {
      opacity: 0;
      transform: translate(calc(14 * var(--u)), calc(-16 * var(--u))) rotate(28deg);
    }
  }
  @keyframes tear-show {
    from {
      opacity: 0;
    }
  }
  @keyframes letter-up {
    to {
      transform: translateY(30%);
    }
  }
  @keyframes gone {
    to {
      opacity: 0;
      transform: translateY(40vh) rotate(calc(var(--tilt) * 4));
    }
  }
</style>
