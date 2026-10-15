<script lang="ts" module>
  export const LETTERS = ["A", "B", "C", "D"];
</script>

<script lang="ts">
  // The four answer tiles (04-ui-tv-display.md): lock, reveal, pad glyphs; Francotirador's target and shatter (09-jokers.md).
  import { questionLocale } from "../../lib/names.svelte.ts";
  import Icon from "../Icon.svelte";
  import Prompt from "../Prompt.svelte";
  import { answerBadge, answerClass, type AnswerView } from "./reveal.ts";

  let {
    answers,
    view,
    disabled,
    shattering,
    tiles = $bindable(),
    onpick,
    onhover,
  }: {
    answers: string[];
    view: AnswerView;
    /** Every tile, e.g. once the final answer is out. */
    disabled: boolean;
    /** The tile Francotirador is shattering. */
    shattering: number | null;
    /** The tile elements, for the input scope and the scope's hole. */
    tiles: HTMLButtonElement[];
    onpick: (i: number) => void;
    onhover: (i: number) => void;
  } = $props();
</script>

<div class="answers" lang={questionLocale()}>
  {#each answers as answer, i (i)}
    {@const badge = answerBadge(i, view)}
    <button
      class="answer glass {answerClass(i, view)}"
      onclick={() => onpick(i)}
      onmouseenter={() => onhover(i)}
      disabled={disabled || view.struck.includes(i)}
      class:shatter={shattering === i}
      bind:this={tiles[i]}
      data-focus-default
    >
      {#if shattering === i}
        <span class="shards" aria-hidden="true">
          {#each Array.from({ length: 10 }, (_, s) => s) as s (s)}
            <i style:--x="{(s % 5) * 20 + 10}%" style:--y="{s < 5 ? 25 : 75}%" style:--r="{(s * 67) % 360}deg" style:--d="{s * 0.02}s"></i>
          {/each}
        </span>
      {/if}
      <span class="letter">{LETTERS[i]}{#if !view.struck.includes(i)}<span class="pad-glyph"><Prompt action={{ type: "pick", n: i + 1 }} padOnly /></span>{/if}</span>
      <span class="text">{answer}</span>
      {#if badge}<span class="badge"><Icon name={badge} /></span>{/if}
    </button>
  {/each}
</div>

<style>
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
    position: relative;
    transition:
      transform 0.2s var(--spring),
      opacity 0.3s,
      filter 0.3s,
      border-color 0.2s,
      box-shadow 0.2s,
      background 0.3s;
    animation: rise 0.5s var(--spring) backwards;
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
  .answer:focus-visible,
  .answer:global([data-nav]) {
    border-color: var(--sky);
    transform: translateY(calc(-0.3 * var(--u)));
  }
  .letter {
    position: relative;
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
  .pad-glyph {
    position: absolute;
    left: calc(-0.5 * var(--u));
    bottom: calc(-0.9 * var(--u));
    border-radius: 50%;
    background: var(--night-900);
    color: var(--paper);
    font-size: calc(1.3 * var(--u));
    line-height: 0;
  }
  .pad-glyph :global(kbd) {
    font-size: inherit;
    opacity: 1;
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
  .answer.shatter {
    z-index: 7;
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
</style>
