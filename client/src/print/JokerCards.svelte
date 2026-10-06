<script lang="ts">
  // Printable joker cards (plans/09-jokers.md, JK-11): one US Letter sheet with 4 × Soplo and
  // 2 × each other joker, 12 cards of 2.5 in in a 3 × 4 grid, with dashed cut lines. White
  // cards to save ink; the token, name and key match the game's tray (JokerTray.svelte).
  import "../game/theme.css"; // the fonts (Baloo 2, Nunito)
  import Icon from "../game/Icon.svelte";
  import { TOKENS } from "../game/JokerTray.svelte";
  import type { JokerName } from "../lib/types";

  const RULES: Record<JokerName, string> = {
    hint: "Muestra una pista de la pregunta. Hasta tres por pregunta.",
    skip: "Cambia la pregunta por otra carta. Si quieren, ese tema sale del juego.",
    easier: "Cambia la pregunta por una más fácil del mismo tema.",
    category: "Ustedes eligen otro tema; la dificultad sigue parecida.",
    snipe: "Disparen a una respuesta falsa y queda tachada. Si le dan a la correcta, el nivel se repite.",
  };
  /** Per joker, its colour on paper (the tray is amber on night blue; paper needs more contrast). */
  const INK: Record<JokerName, string> = {
    hint: "#c98a00",
    skip: "#2a8fb8",
    easier: "#1f9e6e",
    category: "#7a5cc7",
    snipe: "#d6304e",
  };
  const COPIES: Record<JokerName, number> = { hint: 4, skip: 2, easier: 2, category: 2, snipe: 2 };

  const cards = TOKENS.flatMap((t) => Array.from({ length: COPIES[t.name] }, () => t));
</script>

<svelte:head><title>Comodines para imprimir</title></svelte:head>

<div class="screen-only">
  <h1>Comodines para imprimir</h1>
  <p>
    Una hoja carta: 4 × Soplo y 2 × cada otro comodín. Imprimir al <b>100 %</b> (sin «ajustar a la página»),
    luego recortar por las líneas.
  </p>
  <button onclick={() => print()}>Imprimir</button>
</div>

<main class="sheet">
  {#each cards as t, i (i)}
    <section class="card" style:--ink={INK[t.name]}>
      <div class="chip"><span class="face"><Icon name={t.icon} size="100%" /></span></div>
      <h2>{t.label}</h2>
      <p class="rule">{RULES[t.name]}</p>
      <span class="key">{t.key}</span>
    </section>
  {/each}
</main>

<style>
  @page {
    size: letter;
    margin: 0.5in;
  }
  :global(body) {
    background: #e9e6df;
    color: #2a2238;
  }
  .screen-only {
    max-width: 7.5in;
    margin: 0.4in auto 0.2in;
    font-family: "Nunito", system-ui, sans-serif;
  }
  .screen-only h1 {
    margin: 0 0 0.3em;
    font-family: "Baloo 2", system-ui, sans-serif;
  }
  .screen-only button {
    font: inherit;
    font-weight: 700;
    padding: 0.4em 1.2em;
    border: none;
    border-radius: 0.5em;
    background: #ffb81c;
    color: #0b1120;
    cursor: pointer;
  }

  /* 3 × 2.5 in by 4 × 2.5 in: exactly the printable area of a Letter sheet with 0.5 in margins. */
  .sheet {
    display: grid;
    grid-template-columns: repeat(3, 2.5in);
    grid-auto-rows: 2.5in;
    width: 7.5in;
    margin: 0 auto 0.5in;
    background: white;
    box-shadow: 0 0.1in 0.3in rgba(0, 0, 0, 0.2);
  }
  .card {
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 0.06in;
    padding: 0.18in;
    outline: 1px dashed #b9b4aa; /* cut lines; outlines of neighbours overlap into one line */
    text-align: center;
    break-inside: avoid;
  }
  .chip {
    display: grid;
    place-items: center;
    width: 0.95in;
    height: 0.95in;
    border: 0.05in dashed var(--ink);
    border-radius: 50%;
    color: var(--ink);
    box-shadow: 0 0 0 0.04in white, 0 0 0 0.065in var(--ink);
  }
  .face {
    width: 52%;
    height: 52%;
  }
  h2 {
    margin: 0.04in 0 0;
    font-family: "Baloo 2", system-ui, sans-serif;
    font-size: 19pt;
    font-weight: 800;
    line-height: 1;
    color: var(--ink);
  }
  .rule {
    margin: 0;
    font-family: "Nunito", system-ui, sans-serif;
    font-size: 8.5pt;
    font-weight: 700;
    line-height: 1.25;
  }
  .key {
    position: absolute;
    top: 0.12in;
    right: 0.12in;
    display: grid;
    place-items: center;
    width: 0.26in;
    height: 0.26in;
    border: 1.5px solid var(--ink);
    border-radius: 0.05in;
    font-family: "Baloo 2", system-ui, sans-serif;
    font-size: 10pt;
    font-weight: 800;
    color: var(--ink);
  }

  @media print {
    :global(body) {
      background: white;
    }
    .screen-only {
      display: none;
    }
    .sheet {
      margin: 0;
      box-shadow: none;
    }
    .card {
      -webkit-print-color-adjust: exact;
      print-color-adjust: exact;
    }
  }
</style>
