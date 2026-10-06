<script lang="ts">
  // Admin overlay on Esc (04-ui-tv-display.md, UI-13). The family sees it, so it never shows
  // the correct answer. ↑/↓ choose, Enter runs, Esc closes.
  import Placeholder from "./Placeholder.svelte";

  type Item = { label: string; enabled: boolean; run: () => void; confirm?: boolean };

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
    } else if (e.key === "Enter" || e.key === " ") activate(selected);
    else if (e.key === "Escape") onclose();
    else return;
    e.preventDefault();
  }
</script>

<div class="overlay">
  <div class="menu">
    <h2>Pausa</h2>
    {#each items as item, i (item.label)}
      <button
        class:selected={i === selected}
        disabled={!item.enabled}
        onclick={() => activate(i)}
        onmouseenter={() => item.enabled && (selected = i)}
      >
        {confirming === i ? "¿Seguro? Pulsa otra vez" : item.label}
      </button>
    {/each}
    <!-- PLACEHOLDER(UI-8): volume sliders and mute come with the audio engine. -->
    <Placeholder task="UI-8" label="volumen: música, efectos, medios, silenciar" chip />
    {#if questionId}<p class="debug">{questionLabel}: <code>{questionId}</code></p>{/if}
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
  button.selected {
    border-color: var(--amber);
  }
  button:disabled {
    opacity: 0.35;
  }
</style>
