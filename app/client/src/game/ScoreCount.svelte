<script lang="ts">
  // The answering player's career score after an answer (plan 198, decision 593): counts from old to new, a small
  // «+25» / «−1» next to it. Reads the step itself; nothing where the game doesn't count. Never blocks anything.
  import { onDestroy, onMount } from "svelte";
  import type { ScoreStep } from "../engine/career.ts";
  import { fetchScoreStep } from "../lib/api.ts";
  import { formatDelta, formatScore } from "../lib/career-text.ts";
  import { buildInfo } from "../lib/build.ts";
  import { lang, t } from "../lib/i18n.ts";
  import { reducedMotion } from "./timing.ts";

  /** The count's length. */
  const COUNT_MS = 1000;

  let step = $state<ScoreStep | null>(null);
  let shown = $state(0);
  let frame = 0;

  onMount(async () => {
    if (buildInfo().demo) return;
    const s = await fetchScoreStep().catch((e: unknown) => (console.error("career:score", e), null));
    if (!s) return;
    step = s;
    const from = s.score - s.delta;
    if (reducedMotion()) return void (shown = s.score);
    shown = from;
    const t0 = performance.now();
    const tick = (now: number) => {
      const k = Math.min(1, (now - t0) / COUNT_MS);
      shown = Math.round(from + (s.score - from) * (1 - (1 - k) ** 3));
      if (k < 1) frame = requestAnimationFrame(tick);
    };
    frame = requestAnimationFrame(tick);
  });
  onDestroy(() => cancelAnimationFrame(frame));
</script>

{#if step}
  <span class="score glass" data-score>
    <span class="label">{t("career.points")}</span>
    <span class="value">{formatScore(shown, lang)}</span>
    <span class="delta" class:gain={step.delta > 0}>{formatDelta(step.delta, lang)}</span>
  </span>
{/if}

<style>
  .score {
    display: inline-flex;
    align-items: baseline;
    gap: calc(0.7 * var(--u));
    padding: calc(0.3 * var(--u)) calc(1.1 * var(--u));
    border-radius: calc(1 * var(--u));
    font-family: var(--font-display);
    animation: arrive 0.4s var(--spring) backwards;
  }
  .label {
    font-size: calc(1.2 * var(--u));
    color: var(--slate-200);
  }
  .value {
    font-size: calc(2 * var(--u));
    font-weight: 800;
    font-variant-numeric: tabular-nums;
  }
  .delta {
    font-size: calc(1.3 * var(--u));
    font-weight: 700;
    color: var(--coral);
  }
  .delta.gain {
    color: var(--mint);
  }
</style>
