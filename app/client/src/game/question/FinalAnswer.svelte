<script lang="ts">
  // «Respuesta final» (04-ui-tv-display.md): the padlock shakes, opens and slides away (UI-12), then the button.
  import { t } from "../../lib/i18n.ts";
  import Icon from "../Icon.svelte";
  import Prompt from "../Prompt.svelte";

  let {
    locked,
    ready,
    submitted,
    revealed,
    error,
    onsubmit,
  }: {
    /** An answer is locked in. */
    locked: boolean;
    /** The padlock has moved away: the button shows. */
    ready: boolean;
    submitted: boolean;
    revealed: boolean;
    error: string | null;
    onsubmit: () => void;
  } = $props();
</script>

<div class="final">
  {#if error}
    <p class="error">{t("screen.question.sendFailed", { error })}</p>
  {:else if submitted}
    {#if !revealed}<p class="waiting">{t("screen.question.finalWaiting")}</p>{/if}
  {:else}
    <button class="candy final-button" class:ready onclick={onsubmit} disabled={!ready} tabindex={ready ? 0 : -1}>
      {t("screen.question.final")} <Prompt action="submit" />
    </button>
    <div class="padlock" class:shaking={locked && !ready} class:open={ready} aria-hidden="true">
      <Icon name={ready ? "unlock" : "lock"} size="100%" />
    </div>
    {#if !locked}<p class="prompt label">{t("screen.question.prompt")}</p>{/if}
  {/if}
</div>

<style>
  .final {
    position: relative;
    min-height: calc(5.5 * var(--u));
    display: grid;
    place-items: center;
  }
  .final > * {
    grid-area: 1 / 1;
  }
  .final-button {
    opacity: 0;
    transform: scale(0.85);
    transition:
      opacity 0.3s,
      transform 0.4s var(--spring);
  }
  .final-button.ready {
    opacity: 1;
    transform: none;
  }
  .padlock {
    width: calc(5 * var(--u));
    height: calc(5 * var(--u));
    color: var(--slate-200);
    filter: drop-shadow(0 calc(0.3 * var(--u)) calc(0.6 * var(--u)) rgba(0, 0, 0, 0.6));
    transition:
      transform 0.6s var(--spring),
      opacity 0.5s,
      color 0.2s;
    pointer-events: none;
  }
  .padlock.shaking {
    color: var(--amber);
    animation: jiggle 0.8s ease-in-out;
  }
  .padlock.open {
    color: var(--amber);
    opacity: 0;
    transform: translate(calc(14 * var(--u)), calc(1 * var(--u))) rotate(35deg) scale(0.7);
  }
  .prompt {
    position: absolute;
    left: calc(50% + 3.5 * var(--u));
    margin: 0;
    white-space: nowrap;
    text-shadow: var(--text-shadow);
  }
  .waiting {
    margin: 0;
    font-family: var(--font-display);
    font-size: calc(2 * var(--u));
    font-weight: 700;
    color: var(--amber);
    text-shadow: var(--text-shadow);
    animation: pulse 1.2s ease-in-out infinite;
  }
  .error {
    margin: 0;
    color: var(--coral);
    font-size: calc(1.1 * var(--u));
  }

  @keyframes jiggle {
    15%,
    45%,
    75% {
      transform: rotate(-9deg);
    }
    30%,
    60%,
    90% {
      transform: rotate(9deg);
    }
  }
  @keyframes pulse {
    50% {
      opacity: 0.45;
    }
  }
</style>
