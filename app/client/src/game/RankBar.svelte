<script lang="ts">
  // A player's career rank on the 1–15 scale (plan 198): the bar moves from `from` to `to`, the number and name change
  // when a whole number is crossed (a cue on rank up); `from` null: the first rank appears. `still`: no motion, no cue.
  import { onDestroy, onMount } from "svelte";
  import { rankNumber, rankText } from "../lib/career-text.ts";
  import { lang, t } from "../lib/i18n.ts";
  import { sfx } from "./sound.svelte.ts";
  import { reducedMotion } from "./timing.ts";

  let { from = null, to, name, still = false }: { from?: number | null; to: number; name?: string; still?: boolean } = $props();

  /** After the end screen's title arrives. */
  const DELAY_MS = 800;
  const MOVE_MS = 1600;
  const TOP = 15;

  // svelte-ignore state_referenced_locally
  let value = $state(still ? to : (from ?? 0));
  // svelte-ignore state_referenced_locally
  let done = $state(still);
  const shown = $derived(done || from !== null ? rankNumber(value) : null);
  let frame = 0;
  let timer = 0;

  onMount(() => {
    if (still) return;
    const start = from ?? 0;
    const up = from === null || rankNumber(to) > rankNumber(from);
    const finish = () => {
      value = to;
      done = true;
      if (up) sfx("bing");
    };
    if (reducedMotion()) return finish();
    timer = window.setTimeout(() => {
      const t0 = performance.now();
      let last = rankNumber(start);
      const tick = (now: number) => {
        const k = Math.min(1, (now - t0) / MOVE_MS);
        value = start + (to - start) * (k < 0.5 ? 2 * k * k : 1 - (-2 * k + 2) ** 2 / 2);
        if (k >= 1) return finish();
        // a whole number crossed on the way up, before the end
        if (from !== null && rankNumber(value) > last && rankNumber(value) < rankNumber(to)) sfx("bing");
        last = rankNumber(value);
        frame = requestAnimationFrame(tick);
      };
      frame = requestAnimationFrame(tick);
    }, DELAY_MS);
  });
  onDestroy(() => (cancelAnimationFrame(frame), clearTimeout(timer)));
</script>

<div class="rank glass" class:still data-rank>
  <div class="line">
    {#if name}<span class="who">{name}</span>{/if}
    <span class="label">{t("career.rank")}</span>
    {#if shown !== null}
      {#key shown}
        <span class="now" class:pop={!still}><span class="value">{shown}</span> <span class="name">{rankText(shown, lang)}</span></span>
      {/key}
    {/if}
  </div>
  <div class="track">
    <div class="fill" style:width="{(Math.min(TOP, Math.max(0, value)) / TOP) * 100}%"></div>
    {#if from !== null && !still}<div class="was" style:left="{(Math.min(TOP, Math.max(0, from)) / TOP) * 100}%"></div>{/if}
  </div>
</div>

<style>
  .rank {
    display: flex;
    flex-direction: column;
    gap: calc(0.5 * var(--u));
    width: calc(30 * var(--u));
    padding: calc(0.6 * var(--u)) calc(1.2 * var(--u)) calc(0.8 * var(--u));
    border-radius: calc(1 * var(--u));
    font-family: var(--font-display);
  }
  .rank:not(.still) {
    animation: arrive 0.5s 0.4s var(--spring) backwards;
  }
  .line {
    display: flex;
    align-items: baseline;
    gap: calc(0.7 * var(--u));
    min-height: calc(2.6 * var(--u));
  }
  .who {
    font-size: calc(1.4 * var(--u));
    font-weight: 700;
    color: var(--paper);
  }
  .label {
    font-size: calc(1.2 * var(--u));
    color: var(--slate-200);
  }
  .now {
    white-space: nowrap;
  }
  .now.pop {
    animation: crossfade 0.4s ease backwards;
  }
  .value {
    font-size: calc(2 * var(--u));
    font-weight: 800;
    font-variant-numeric: tabular-nums;
    color: var(--amber);
  }
  .name {
    font-size: calc(1.5 * var(--u));
    font-weight: 700;
  }
  .track {
    position: relative;
    height: calc(0.8 * var(--u));
    border-radius: calc(0.4 * var(--u));
    background: repeating-linear-gradient(90deg, transparent 0 calc(100% / 15 - 1px), rgba(255, 255, 255, 0.12) 0 calc(100% / 15))
      rgba(255, 255, 255, 0.08);
  }
  .fill {
    height: 100%;
    border-radius: inherit;
    background: linear-gradient(90deg, var(--sky), var(--amber));
  }
  .was {
    position: absolute;
    top: calc(-0.3 * var(--u));
    bottom: calc(-0.3 * var(--u));
    width: 2px;
    background: var(--paper);
    opacity: 0.6;
  }
  @keyframes crossfade {
    from {
      opacity: 0;
      transform: translateY(calc(-0.4 * var(--u)));
    }
  }
</style>
