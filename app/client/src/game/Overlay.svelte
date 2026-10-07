<script lang="ts">
  // Admin overlay on Esc (04-ui-tv-display.md, UI-13). The family sees it, so it never shows
  // the correct answer. ↑/↓ choose, Enter runs, ←/→ change a volume or a joker budget, Esc closes.
  // Left column: game actions; right column: sound, and the running game's joker budget (MD-4).
  import type { JokerBudget, JokerName } from "../lib/types";
  import { TOKENS } from "./JokerTray.svelte";
  import { setVolumes, sound, type Volumes } from "./sound.svelte";

  type Item = {
    label: string;
    enabled: boolean;
    run: () => void;
    right?: boolean;
    confirm?: boolean;
    volume?: Channel;
    joker?: JokerName;
    preset?: boolean;
  };
  type Channel = "music" | "effects" | "media";

  const CHANNELS: { key: Channel; label: string }[] = [
    { key: "music", label: "Música" },
    { key: "effects", label: "Efectos" },
    { key: "media", label: "Audio y video de las preguntas" },
  ];
  const STEP = 0.1;
  /** «Como las cartas»: the printed card set (JK-11); the same as `CARDS` in app/server/game.py. */
  const CARDS: JokerBudget = { hint: 4, skip: 2, easier: 2, category: 2, snipe: 2 };
  /** Budget steps for ←/→: 0 to 9 uses, then unlimited (null). */
  const MAX_USES = 9;

  // The review tool and stats pages run on the authoring server (D-35). A build made with
  // VITE_AUTHORING_URL="" (the packaged game) has no authoring server and hides the links.
  const env = import.meta.env.VITE_AUTHORING_URL;
  const authoring = env ?? `${location.protocol}//${location.hostname}:8001`;

  function change(key: Channel, by: number) {
    const v = Math.round(Math.min(1, Math.max(0, sound.volumes[key] + by)) * 10) / 10;
    setVolumes({ [key]: v } as Partial<Volumes>);
  }

  let {
    questionId,
    questionLabel,
    canSkip,
    canUndo,
    canRestart,
    budget,
    left,
    onclose,
    onskip,
    onskipall,
    onundo,
    onrestart,
    onbudget,
  }: {
    /** For debugging (04, "Admin overlay"): the question on screen, or the last one answered. */
    questionId: string | null;
    questionLabel: string;
    canSkip: boolean;
    canUndo: boolean;
    canRestart: boolean;
    /** The running game's joker budget (MD-4), or null without a running game. */
    budget: JokerBudget | null;
    /** Uses left in the running game. */
    left: JokerBudget | null;
    onclose: () => void;
    onskip: () => void;
    /** «Saltar y quemar para todos»: a broken or wrong question, burned for every player (D-28). */
    onskipall: () => void;
    onundo: () => void;
    onrestart: () => void;
    onbudget: (budget: Partial<JokerBudget>) => void;
  } = $props();

  function fullscreen() {
    if (document.fullscreenElement) document.exitFullscreen();
    else document.documentElement.requestFullscreen().catch(() => {});
    onclose();
  }

  /** The budget as last changed here, until the server's answer arrives: fast clicks build on it. */
  let pending = $state<JokerBudget | null>(null);
  $effect(() => {
    void budget;
    pending = null;
  });
  const current = $derived(budget && (pending ?? budget));

  function setBudget(change: Partial<JokerBudget>) {
    if (!current) return;
    pending = { ...current, ...change };
    onbudget(change);
  }

  const unlimited = $derived(!!current && TOKENS.every((t) => current![t.name] === null));
  const cards = $derived(!!current && TOKENS.every((t) => current![t.name] === CARDS[t.name]));
  const presetLabel = $derived(unlimited ? "Sin límite" : cards ? "Como las cartas" : "A medida");

  /** Sin límite ↔ Como las cartas; a custom budget goes back to unlimited. */
  function cyclePreset() {
    setBudget(unlimited ? CARDS : Object.fromEntries(TOKENS.map((t) => [t.name, null])));
  }

  function stepJoker(name: JokerName, by: number) {
    const now = current?.[name];
    const index = Math.min(MAX_USES + 1, Math.max(0, (now ?? MAX_USES + 1) + by));
    const next = index > MAX_USES ? null : index;
    if (next !== now) setBudget({ [name]: next });
  }

  const items = $derived<Item[]>([
    { label: "Continuar", enabled: true, run: onclose },
    { label: "Saltar pregunta", enabled: canSkip, run: onskip },
    { label: "Saltar y quemar para todos", enabled: canSkip, run: onskipall, confirm: true },
    { label: "Deshacer última respuesta", enabled: canUndo, run: onundo },
    { label: "Pantalla completa", enabled: true, run: fullscreen },
    { label: "Volver al inicio (termina la partida)", enabled: canRestart, run: onrestart, confirm: true },
    ...CHANNELS.map((c) => ({ label: c.label, enabled: true, run: () => {}, volume: c.key, right: true })),
    {
      label: sound.volumes.muted ? "Sonido: apagado" : "Sonido: encendido",
      enabled: true,
      run: () => setVolumes({ muted: !sound.volumes.muted }),
      right: true,
    },
    ...(budget
      ? [
          { label: "Comodines", enabled: true, run: cyclePreset, preset: true, right: true },
          ...TOKENS.map((t) => ({ label: t.label, enabled: true, run: () => {}, joker: t.name, right: true })),
        ]
      : []),
  ]);

  let selected = $state(0);
  /** Index of an item that asked "¿Seguro?" and waits for a second Enter. */
  let confirming = $state<number | null>(null);

  function activate(i: number) {
    const item = items[i];
    if (!item.enabled) return;
    if (item.confirm && confirming !== i) {
      confirming = i;
      return;
    }
    item.run();
  }

  export function key(e: KeyboardEvent) {
    const item = items[selected];
    const by = e.key === "ArrowRight" ? 1 : e.key === "ArrowLeft" ? -1 : 0;
    if (e.key === "ArrowDown" || e.key === "ArrowUp") {
      const step = e.key === "ArrowDown" ? 1 : -1;
      do selected = (selected + step + items.length) % items.length;
      while (!items[selected].enabled);
      confirming = null;
    } else if (by && item.volume) change(item.volume, by * STEP);
    else if (by && item.joker) stepJoker(item.joker, by);
    else if (by && item.preset) cyclePreset();
    else if (e.key === "Enter" || e.key === " ") activate(selected);
    else if (e.key === "Escape") onclose();
    else return;
    e.preventDefault();
  }
</script>

{#snippet row(item: Item, i: number)}
  {#if item.volume}
    {@const key = item.volume}
    <label class="row volume" class:selected={i === selected} onmouseenter={() => (selected = i)}>
      <span>{item.label}</span>
      <input
        type="range"
        min="0"
        max="1"
        step={STEP}
        value={sound.volumes[key]}
        oninput={(e) => setVolumes({ [key]: Number(e.currentTarget.value) } as Partial<Volumes>)}
        tabindex="-1"
      />
      <span class="value">{Math.round(sound.volumes[key] * 100)} %</span>
    </label>
  {:else if item.joker}
    {@const name = item.joker}
    <div class="row joker" class:selected={i === selected} role="group" onmouseenter={() => (selected = i)}>
      <span>{item.label}</span>
      <button class="step" onclick={() => stepJoker(name, -1)} tabindex="-1" aria-label="menos">−</button>
      <span class="value">{current?.[name] ?? "∞"}</span>
      <button class="step" onclick={() => stepJoker(name, 1)} tabindex="-1" aria-label="más">+</button>
      <span class="left">{left?.[name] != null ? `quedan ${left[name]}` : ""}</span>
    </div>
  {:else}
    <button
      class:selected={i === selected}
      disabled={!item.enabled}
      onclick={() => activate(i)}
      onmouseenter={() => item.enabled && (selected = i)}
    >
      {#if item.preset}
        Comodines: <b>{presetLabel}</b>
      {:else}
        {confirming === i ? "¿Seguro? Pulsa otra vez" : item.label}
      {/if}
    </button>
  {/if}
{/snippet}

<div class="overlay">
  <div class="menu">
    <h2>Pausa</h2>
    <div class="columns">
      <div class="column">
        {#each items as item, i (item.joker ?? item.volume ?? item.label)}
          {#if !item.right}{@render row(item, i)}{/if}
        {/each}
      </div>
      <div class="column">
        <h3>Sonido</h3>
        {#each items as item, i (item.joker ?? item.volume ?? item.label)}
          {#if item.right && !item.preset && !item.joker}{@render row(item, i)}{/if}
        {/each}
        {#if budget}
          <h3>Comodines de esta partida</h3>
          {#each items as item, i (item.joker ?? item.volume ?? item.label)}
            {#if item.preset || item.joker}{@render row(item, i)}{/if}
          {/each}
        {/if}
      </div>
    </div>
    <p class="debug">Volumen y comodines: <kbd>←</kbd> <kbd>→</kbd></p>
    {#if questionId}
      <p class="debug">
        {questionLabel}:
        {#if authoring}
          <a href="{authoring}/review/{encodeURIComponent(questionId)}" target="_blank" tabindex="-1"><code>{questionId}</code></a>
        {:else}
          <code>{questionId}</code>
        {/if}
      </p>
    {/if}
    {#if authoring}
      <p class="debug">
        Estadísticas:
        <a href="{authoring}/stats/categories" target="_blank" tabindex="-1">categorías</a> ·
        <a href="{authoring}/stats/difficulty" target="_blank" tabindex="-1">dificultad</a>
      </p>
    {/if}
  </div>
</div>

<style>
  .overlay {
    position: fixed;
    inset: 0;
    z-index: 40;
    display: grid;
    place-items: center;
    background: rgba(5, 8, 16, 0.72);
  }
  .menu {
    display: flex;
    flex-direction: column;
    gap: calc(0.7 * var(--u));
    padding: calc(2.4 * var(--u)) calc(2.4 * var(--u));
    border: 1px solid var(--slate-600);
    border-radius: calc(1.6 * var(--u));
    background: var(--night-700);
    box-shadow: 0 calc(1.5 * var(--u)) calc(4 * var(--u)) rgba(0, 0, 0, 0.6);
  }
  h2 {
    margin: 0 0 calc(0.6 * var(--u));
    text-align: center;
    font-family: var(--font-display);
    font-size: calc(2.6 * var(--u));
    font-weight: 800;
  }
  h3 {
    margin: calc(0.4 * var(--u)) 0 0;
    font-family: var(--font-display);
    font-size: calc(1.2 * var(--u));
    font-weight: 700;
    color: var(--slate-400);
  }
  .columns {
    display: grid;
    grid-template-columns: calc(36 * var(--u)) calc(40 * var(--u));
    gap: calc(2.4 * var(--u));
    align-items: start;
  }
  .column {
    display: flex;
    flex-direction: column;
    gap: calc(0.7 * var(--u));
  }
  button {
    padding: calc(0.7 * var(--u)) calc(1.4 * var(--u));
    border: calc(0.18 * var(--u)) solid transparent;
    border-radius: calc(0.8 * var(--u));
    background: var(--slate-600);
    font-size: calc(1.5 * var(--u));
    font-weight: 700;
    text-align: left;
  }
  .debug {
    margin: calc(0.6 * var(--u)) 0 0;
    text-align: center;
    font-size: calc(0.9 * var(--u));
    color: var(--slate-400);
  }
  .debug code {
    color: var(--slate-200);
    user-select: all;
  }
  .debug a {
    color: var(--slate-200);
  }
  button.selected,
  .row.selected {
    border-color: var(--amber);
  }
  .row {
    display: grid;
    align-items: center;
    gap: calc(1 * var(--u));
    padding: calc(0.45 * var(--u)) calc(1.4 * var(--u));
    border: calc(0.18 * var(--u)) solid transparent;
    border-radius: calc(0.8 * var(--u));
    background: rgba(43, 54, 80, 0.5);
    font-size: calc(1.2 * var(--u));
    font-weight: 700;
  }
  .volume {
    grid-template-columns: 1fr calc(12 * var(--u)) calc(4.5 * var(--u));
  }
  .joker {
    grid-template-columns: 1fr calc(2.4 * var(--u)) calc(2.4 * var(--u)) calc(2.4 * var(--u)) calc(7 * var(--u));
  }
  .volume input {
    accent-color: var(--amber);
    width: 100%;
  }
  .value {
    text-align: right;
    color: var(--slate-200);
    font-variant-numeric: tabular-nums;
  }
  .joker .value {
    text-align: center;
    color: var(--amber);
  }
  .step {
    display: grid;
    place-items: center;
    height: calc(2.2 * var(--u));
    padding: 0;
    font-size: calc(1.4 * var(--u));
    text-align: center;
  }
  .left {
    color: var(--slate-400);
    font-weight: 600;
    text-align: right;
  }
  button:disabled {
    opacity: 0.35;
  }
</style>
