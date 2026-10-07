<script lang="ts">
  // Admin overlay on Esc (04-ui-tv-display.md, UI-13). The family sees it, so it never shows
  // the correct answer. ↑/↓ choose, Enter runs, ←/→ change a volume, Esc closes.
  import { setVolumes, sound, type Volumes } from "./sound.svelte";

  type Item = { label: string; enabled: boolean; run: () => void; confirm?: boolean; volume?: Channel };
  type Channel = "music" | "effects" | "media";

  const CHANNELS: { key: Channel; label: string }[] = [
    { key: "music", label: "Música" },
    { key: "effects", label: "Efectos" },
    { key: "media", label: "Audio y video de las preguntas" },
  ];
  const STEP = 0.1;

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
    onclose,
    onskip,
    onskipall,
    onundo,
    onrestart,
  }: {
    /** For debugging (04, "Admin overlay"): the question on screen, or the last one answered. */
    questionId: string | null;
    questionLabel: string;
    canSkip: boolean;
    canUndo: boolean;
    canRestart: boolean;
    onclose: () => void;
    onskip: () => void;
    /** «Saltar y quemar para todos»: a broken or wrong question, burned for every player (D-28). */
    onskipall: () => void;
    onundo: () => void;
    onrestart: () => void;
  } = $props();

  function fullscreen() {
    if (document.fullscreenElement) document.exitFullscreen();
    else document.documentElement.requestFullscreen().catch(() => {});
    onclose();
  }

  const items = $derived<Item[]>([
    { label: "Continuar", enabled: true, run: onclose },
    { label: "Saltar pregunta", enabled: canSkip, run: onskip },
    { label: "Saltar y quemar para todos", enabled: canSkip, run: onskipall, confirm: true },
    { label: "Deshacer última respuesta", enabled: canUndo, run: onundo },
    { label: "Pantalla completa", enabled: true, run: fullscreen },
    { label: "Volver al inicio (termina la partida)", enabled: canRestart, run: onrestart, confirm: true },
    ...CHANNELS.map((c) => ({ label: c.label, enabled: true, run: () => {}, volume: c.key })),
    {
      label: sound.volumes.muted ? "Sonido: apagado" : "Sonido: encendido",
      enabled: true,
      run: () => setVolumes({ muted: !sound.volumes.muted }),
    },
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
    if (e.key === "ArrowDown" || e.key === "ArrowUp") {
      const step = e.key === "ArrowDown" ? 1 : -1;
      do selected = (selected + step + items.length) % items.length;
      while (!items[selected].enabled);
      confirming = null;
    } else if ((e.key === "ArrowLeft" || e.key === "ArrowRight") && items[selected].volume) {
      change(items[selected].volume!, e.key === "ArrowRight" ? STEP : -STEP);
    } else if (e.key === "Enter" || e.key === " ") activate(selected);
    else if (e.key === "Escape") onclose();
    else return;
    e.preventDefault();
  }
</script>

<div class="overlay">
  <div class="menu">
    <h2>Pausa</h2>
    {#each items as item, i (item.volume ?? item.label)}
      {#if item.volume}
        {@const key = item.volume}
        <label class="volume" class:selected={i === selected} onmouseenter={() => (selected = i)}>
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
          <span class="pct">{Math.round(sound.volumes[key] * 100)} %</span>
        </label>
      {:else}
        <button
          class:selected={i === selected}
          disabled={!item.enabled}
          onclick={() => activate(i)}
          onmouseenter={() => item.enabled && (selected = i)}
        >
          {confirming === i ? "¿Seguro? Pulsa otra vez" : item.label}
        </button>
      {/if}
    {/each}
    <p class="debug">Volumen: <kbd>←</kbd> <kbd>→</kbd></p>
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
    min-width: calc(40 * var(--u));
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
  .volume.selected {
    border-color: var(--amber);
  }
  .volume {
    display: grid;
    grid-template-columns: 1fr calc(14 * var(--u)) calc(4.5 * var(--u));
    align-items: center;
    gap: calc(1 * var(--u));
    padding: calc(0.45 * var(--u)) calc(1.4 * var(--u));
    border: calc(0.18 * var(--u)) solid transparent;
    border-radius: calc(0.8 * var(--u));
    background: rgba(43, 54, 80, 0.5);
    font-size: calc(1.2 * var(--u));
    font-weight: 700;
  }
  .volume:first-of-type {
    margin-top: calc(0.8 * var(--u));
  }
  .volume input {
    accent-color: var(--amber);
    width: 100%;
  }
  .pct {
    text-align: right;
    color: var(--slate-200);
    font-variant-numeric: tabular-nums;
  }
  button:disabled {
    opacity: 0.35;
  }
</style>
