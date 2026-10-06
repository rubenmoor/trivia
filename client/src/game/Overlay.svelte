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
    background: rgba(0, 0, 0, 0.7);
  }
  .menu {
    display: flex;
    flex-direction: column;
    gap: 1.2vh;
    min-width: 34vw;
    padding: 4vh 3vw;
    border-radius: 1.5vw;
    background: var(--panel);
  }
  h2 {
    margin: 0 0 1vh;
    text-align: center;
    font-size: 2.6vw;
  }
  button {
    font: inherit;
    font-size: 1.8vw;
    padding: 1.4vh 2vw;
    border: 0.25vw solid transparent;
    border-radius: 0.8vw;
    background: #2f3240;
    color: var(--text);
    cursor: pointer;
    text-align: left;
  }
  .debug {
    margin: 1vh 0 0;
    text-align: center;
    font-size: 1vw;
    color: var(--muted);
  }
  .debug code {
    color: var(--text);
    user-select: all;
  }
  button.selected {
    border-color: var(--accent);
  }
  button:disabled {
    opacity: 0.35;
    cursor: default;
  }
</style>
