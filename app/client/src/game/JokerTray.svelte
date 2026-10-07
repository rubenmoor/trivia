<script lang="ts" module>
  // The joker tray (plans/09-jokers.md, "Joker tray", JK-4): five tokens down the left edge of the
  // Question screen, read-only and smaller on Level and Select. A token is either playable or
  // disabled right now, with the server's reason. Jokers are unlimited by default (D-27); with a
  // budget (13-game-modes.md, MD-3) a limited token carries a badge with the uses left.
  import type { IconName } from "./Icon.svelte";
  import type { JokerName } from "../lib/types";

  export const TOKENS: { name: JokerName; label: string; key: string; icon: IconName }[] = [
    { name: "hint", label: "Soplo", key: "S", icon: "bulb" },
    { name: "skip", label: "Paso", key: "P", icon: "door" },
    { name: "easier", label: "Bájale", key: "F", icon: "stairs" },
    { name: "category", label: "Cambiazo", key: "T", icon: "compass" },
    { name: "snipe", label: "Francotirador", key: "X", icon: "crosshair" },
  ];
</script>

<script lang="ts">
  import type { JokerBudget, Jokers } from "../lib/types";
  import Icon from "./Icon.svelte";

  let {
    jokers = null,
    left = null,
    hintsLeft = 3,
    readonly = false,
    armed = null,
    away = null,
    popping = null,
    onpress,
  }: {
    jokers?: Jokers | null;
    /** Uses left in this game; null (or a null entry) = unlimited, no badge (MD-3). */
    left?: JokerBudget | null;
    /** Soplo's pips: hints of the current question not shown yet. */
    hintsLeft?: number;
    /** Level and Select: a reminder only. */
    readonly?: boolean;
    /** The token lifted by a first tap, waiting for the second (09, "Arming"). */
    armed?: JokerName | null;
    /** The token in flight (JK-5): its slot is empty meanwhile. */
    away?: JokerName | null;
    /** A fresh token pops back into this slot (JK-5). */
    popping?: JokerName | null;
    onpress?: (name: JokerName) => void;
  } = $props();
</script>

<div class="tray" class:readonly>
  {#each TOKENS as t (t.name)}
    {@const state = jokers?.[t.name]}
    {@const off = !readonly && !state?.available}
    <div class="slot">
      <button
        class="token"
        class:off
        class:armed={armed === t.name}
        class:away={away === t.name}
        class:popping={popping === t.name}
        data-joker={t.name}
        disabled={readonly || off}
        onclick={() => onpress?.(t.name)}
        aria-label="{t.label} ({t.key})"
      >
        <span class="face"><Icon name={t.icon} size="100%" /></span>
        {#if !readonly}<span class="key">{t.key}</span>{/if}
        {#if off}<span class="lock"><Icon name="lock" size="100%" /></span>{/if}
        {#if left?.[t.name] != null}<span class="count" class:empty={left[t.name] === 0}>{left[t.name]}</span>{/if}
        {#if t.name === "hint" && !readonly}
          <span class="pips">
            {#each [0, 1, 2] as p (p)}<span class="pip" class:full={p < hintsLeft}></span>{/each}
          </span>
        {/if}
      </button>
      {#if !readonly}
        {#if armed === t.name}
          <button class="bubble arm glass-strong" onclick={() => onpress?.(t.name)}>¿Usar {t.label}? <kbd>Enter</kbd></button>
        {:else}
          <span class="bubble name glass-strong">
            {t.label}{#if off && state?.reason}<span class="reason">{state.reason}</span>{/if}
          </span>
        {/if}
      {/if}
    </div>
  {/each}
</div>

<style>
  .tray {
    --chip: calc(4.6 * var(--u));
    display: flex;
    flex-direction: column;
    gap: calc(1.1 * var(--u));
  }
  .tray.readonly {
    --chip: calc(3.2 * var(--u));
    gap: calc(0.7 * var(--u));
    opacity: 0.55;
  }
  .slot {
    position: relative;
    display: flex;
    align-items: center;
  }
  .token {
    position: relative;
    display: grid;
    place-items: center;
    width: var(--chip);
    height: var(--chip);
    padding: 0;
    border: calc(0.3 * var(--u)) dashed var(--amber);
    border-radius: 50%;
    background:
      radial-gradient(circle at 35% 30%, rgba(255, 255, 255, 0.12), transparent 60%),
      var(--night-700);
    color: var(--amber);
    box-shadow:
      0 0 0 calc(0.25 * var(--u)) var(--night-900),
      0 calc(0.35 * var(--u)) calc(0.8 * var(--u)) rgba(0, 0, 0, 0.5);
    transition:
      transform 0.2s var(--spring),
      opacity 0.2s,
      filter 0.2s;
  }
  .readonly .token {
    border-style: solid;
    border-width: calc(0.18 * var(--u));
    cursor: default;
  }
  .face {
    width: 52%;
    height: 52%;
  }
  .token:not(:disabled):hover,
  .token:focus-visible {
    transform: translateY(calc(-0.25 * var(--u))) scale(1.06);
  }
  .token.armed {
    border-color: var(--sky);
    color: var(--sky);
    transform: translateX(calc(0.8 * var(--u))) scale(1.15);
    animation: shimmer 0.9s ease-in-out infinite;
  }
  .token.away {
    opacity: 0;
    transition: none;
  }
  .token.popping {
    animation: pop-back 0.45s var(--spring);
  }
  @keyframes pop-back {
    from {
      transform: scale(0);
    }
  }
  .token.off {
    opacity: 0.4;
    filter: grayscale(0.8);
  }
  .key {
    position: absolute;
    right: calc(-0.3 * var(--u));
    bottom: calc(-0.3 * var(--u));
    display: grid;
    place-items: center;
    width: calc(1.6 * var(--u));
    height: calc(1.6 * var(--u));
    border-radius: calc(0.4 * var(--u));
    background: var(--paper);
    color: var(--night-900);
    font-family: var(--font-display);
    font-size: calc(1 * var(--u));
    font-weight: 800;
  }
  .lock {
    position: absolute;
    top: calc(-0.3 * var(--u));
    right: calc(-0.3 * var(--u));
    width: calc(1.5 * var(--u));
    height: calc(1.5 * var(--u));
    color: var(--slate-200);
  }
  .pips {
    position: absolute;
    bottom: calc(-1 * var(--u));
    display: flex;
    gap: calc(0.25 * var(--u));
  }
  .pip {
    width: calc(0.5 * var(--u));
    height: calc(0.5 * var(--u));
    border-radius: 50%;
    background: var(--slate-600);
  }
  .pip.full {
    background: var(--amber);
  }

  .bubble {
    position: absolute;
    left: calc(var(--chip) + 1.2 * var(--u));
    padding: calc(0.3 * var(--u)) calc(0.9 * var(--u));
    border-radius: calc(0.7 * var(--u));
    font-family: var(--font-display);
    font-size: calc(1.1 * var(--u));
    font-weight: 700;
    white-space: nowrap;
    pointer-events: none;
  }
  .bubble.name {
    opacity: 0;
    transform: translateX(calc(-0.5 * var(--u)));
    transition:
      opacity 0.15s,
      transform 0.15s;
  }
  .slot:hover .bubble.name,
  .slot:focus-within .bubble.name {
    opacity: 1;
    transform: none;
  }
  .reason {
    display: block;
    font-family: var(--font-text);
    font-weight: 600;
    color: var(--slate-200);
  }
  .count {
    position: absolute;
    top: calc(-0.3 * var(--u));
    left: calc(-0.3 * var(--u));
    display: grid;
    place-items: center;
    min-width: calc(1.6 * var(--u));
    height: calc(1.6 * var(--u));
    padding: 0 calc(0.3 * var(--u));
    border-radius: calc(0.8 * var(--u));
    background: var(--amber);
    color: var(--night-900);
    font-family: var(--font-display);
    font-size: calc(1 * var(--u));
    font-weight: 800;
    font-variant-numeric: tabular-nums;
  }
  .readonly .count {
    font-size: calc(0.9 * var(--u));
  }
  .count.empty {
    background: var(--slate-600);
    color: var(--slate-200);
  }
  .bubble.arm {
    left: calc(var(--chip) + 2 * var(--u));
    border: 1px solid var(--sky);
    pointer-events: auto;
    cursor: pointer;
    border-color: var(--sky);
    color: var(--sky);
  }
  @keyframes shimmer {
    50% {
      box-shadow:
        0 0 0 calc(0.25 * var(--u)) var(--night-900),
        0 0 calc(1.6 * var(--u)) var(--sky);
    }
  }
</style>
