<script lang="ts">
  // Histogram: questions per difficulty over the whole shared scale 1–15 (D-38), with the window
  // the game plays today (young teens, until AG-7) shaded (RV-18).
  import type { AgeGroups, Question } from "../lib/types";
  import "./chart.css";

  let {
    questions,
    ageGroups,
    compact = false,
  }: { questions: Question[]; ageGroups: AgeGroups; compact?: boolean } = $props();

  /** The group the game plays until players can choose one (AG-7). */
  const PLAYED_GROUP = "young_teens";

  const LEVELS = $derived(
    Array.from({ length: ageGroups.scale[1] - ageGroups.scale[0] + 1 }, (_, i) => ageGroups.scale[0] + i),
  );
  const played = $derived(ageGroups.groups.find((g) => g.id === PLAYED_GROUP));
  /** Shaded band for the played window, in % of the plot width. */
  const band = $derived.by(() => {
    if (!played) return null;
    const [lo, hi] = played.window;
    const n = LEVELS.length;
    return { left: ((lo - LEVELS[0]) / n) * 100, width: ((hi - lo + 1) / n) * 100 };
  });

  const counts = $derived(LEVELS.map((l) => questions.filter((q) => q.difficulty === l).length));
  const total = $derived(counts.reduce((a, b) => a + b, 0));
  const mean = $derived(total ? questions.reduce((n, q) => n + q.difficulty, 0) / total : 0);

  /** Clean axis: a step of 1, 2 or 5 × 10ⁿ, about five gridlines. */
  const axis = $derived.by(() => {
    const top = Math.max(1, ...counts);
    const raw = top / 5;
    const mag = 10 ** Math.floor(Math.log10(raw));
    const step = Math.max(1, [1, 2, 5, 10].map((m) => m * mag).find((s) => s >= raw) ?? 10 * mag);
    const max = Math.ceil(top / step) * step;
    const ticks: number[] = [];
    for (let t = 0; t <= max; t += step) ticks.push(t);
    return { max, ticks };
  });

  let hover = $state<{ level: number; x: number; y: number } | null>(null);

  function move(level: number, e: PointerEvent) {
    hover = { level, x: Math.min(e.clientX + 16, window.innerWidth - 240), y: Math.max(8, e.clientY - 60) };
  }
  const pct = (n: number) => (total ? Math.round((n / total) * 100) : 0);
</script>

<section class="chart-panel" class:compact>
  <h2>Questions per difficulty</h2>
  <p class="sub">
    {total} questions · average difficulty {mean.toFixed(1)} · {LEVELS[0]} = easiest, {LEVELS[LEVELS.length - 1]} = hardest
    {#if played}· shaded: {played.window[0]}–{played.window[1]}, the window the game plays ({played.name}){/if}
  </p>

  <div class="plot" style:--n={LEVELS.length}>
    {#if band}
      <div class="band" style:left="{band.left}%" style:width="{band.width}%" aria-hidden="true"></div>
    {/if}
    <div class="grid" aria-hidden="true">
      {#each axis.ticks as t}
        <div class="tick" style:bottom="{(t / axis.max) * 100}%"><span>{t}</span></div>
      {/each}
    </div>
    <div class="columns">
      {#each LEVELS as level, i}
        <div
          class="slot"
          role="img"
          aria-label="Difficulty {level}: {counts[i]} questions"
          onpointermove={(e) => move(level, e)}
          onpointerleave={() => (hover = null)}
          class:dim={hover && hover.level !== level}
        >
          <div class="stack" style:height="{(counts[i] / axis.max) * 100}%">
            <span class="value">{counts[i]}</span>
            {#if counts[i] > 0}<div class="column"></div>{/if}
          </div>
        </div>
      {/each}
    </div>
  </div>
  <div class="xlabels" aria-hidden="true" style:--n={LEVELS.length}>
    {#each LEVELS as level}<span>{level}</span>{/each}
  </div>
  <p class="xtitle">Difficulty</p>

  {#if !compact}<details class="table-view">
    <summary>Table</summary>
    <table>
      <thead><tr><th>Difficulty</th><th class="num">Questions</th><th class="num">Share</th></tr></thead>
      <tbody>
        {#each LEVELS as level, i}
          <tr><td>{level}</td><td class="num">{counts[i]}</td><td class="num">{pct(counts[i])} %</td></tr>
        {/each}
      </tbody>
    </table>
  </details>{/if}
</section>

{#if hover}
  {@const n = counts[LEVELS.indexOf(hover.level)]}
  <div class="tooltip" style:left="{hover.x}px" style:top="{hover.y}px">
    <strong>Difficulty {hover.level}</strong>
    <div>{n} question{n === 1 ? "" : "s"} · {pct(n)} %</div>
  </div>
{/if}

<style>
  .plot {
    position: relative;
    height: 280px;
    margin-left: 2.25rem;
    /* Room for the value label above the tallest column. */
    margin-top: 1.5rem;
  }
  .grid {
    position: absolute;
    inset: 0;
  }
  .band {
    position: absolute;
    top: -1.5rem;
    bottom: 0;
    background: rgb(255 255 255 / 0.04);
    border-radius: 6px 6px 0 0;
  }
  .tick {
    position: absolute;
    left: 0;
    right: 0;
    border-top: 1px solid #33363f;
  }
  .tick span {
    position: absolute;
    right: calc(100% + 0.5rem);
    transform: translateY(-50%);
    font-size: 0.8rem;
    color: var(--muted);
    font-variant-numeric: tabular-nums;
  }
  .columns {
    position: absolute;
    inset: 0;
    display: grid;
    grid-template-columns: repeat(var(--n), 1fr);
  }
  .slot {
    /* The whole slot is the hover target, not just the column. */
    display: flex;
    align-items: flex-end;
    justify-content: center;
    height: 100%;
    transition: opacity 0.12s;
  }
  .slot.dim {
    opacity: 0.45;
  }
  .stack {
    position: relative;
    display: flex;
    justify-content: center;
    width: 24px;
  }
  .column {
    width: 24px;
    height: 100%;
    background: var(--bar);
    border-radius: 4px 4px 0 0;
  }
  .value {
    position: absolute;
    bottom: calc(100% + 4px);
    font-size: 0.85rem;
    font-variant-numeric: tabular-nums;
    color: var(--muted);
  }
  .slot:hover .value {
    color: var(--text);
  }
  .xlabels {
    display: grid;
    grid-template-columns: repeat(var(--n), 1fr);
    margin-left: 2.25rem;
    margin-top: 0.4rem;
    text-align: center;
    font-size: 0.85rem;
    color: var(--muted);
  }
  .compact .plot {
    height: 150px;
  }
  .compact .stack,
  .compact .column {
    width: 16px;
  }
  .xtitle {
    margin: 0.2rem 0 0 2.25rem;
    text-align: center;
    font-size: 0.85rem;
    color: var(--muted);
  }
</style>
