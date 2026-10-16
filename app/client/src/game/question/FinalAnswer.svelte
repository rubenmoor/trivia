<script lang="ts">
  // «Respuesta final» (04-ui-tv-display.md): the padlock shakes, opens and slides away (UI-12), then the button.
  // Answers off (D-105): the padlock is the button and reveals.
  import { t } from "../../lib/i18n.ts";
  import Icon from "../Icon.svelte";
  import Prompt from "../Prompt.svelte";

  let {
    locked,
    ready,
    submitted,
    revealed,
    error,
    answersOff = false,
    onsubmit,
    onreveal,
  }: {
    /** An answer is locked in. */
    locked: boolean;
    /** The padlock has moved away: the button shows. */
    ready: boolean;
    submitted: boolean;
    revealed: boolean;
    error: string | null;
    /** «Select answer to advance» is off (D-105). */
    answersOff?: boolean;
    onsubmit: () => void;
    onreveal: () => void;
  } = $props();
</script>

<div class="final">
  {#if error}
    <p class="error">{t("screen.question.sendFailed", { error })}</p>
  {:else if submitted}
    {#if !revealed}
      <div class="suspense">
        <span class="ring" aria-hidden="true"></span><span class="ring late" aria-hidden="true"></span>
        <p class="waiting">{t("screen.question.finalWaiting")}</p>
      </div>
    {/if}
  {:else if answersOff}
    <button class="reveal-button" onclick={onreveal} data-focus-default>
      <span class="padlock clickable" aria-hidden="true"><Icon name="lock" size="100%" /></span>
      <span class="label">{t("screen.question.reveal")}</span>
      <Prompt action="confirm" />
    </button>
  {:else}
    <button class="candy final-button" class:ready onclick={onsubmit} disabled={!ready} tabindex={ready ? 0 : -1}>
      <Icon name="seal" /> {t("screen.question.final")} <Prompt action="submit" />
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
  .reveal-button {
    display: inline-flex;
    align-items: center;
    gap: calc(0.8 * var(--u));
    padding: calc(0.3 * var(--u)) calc(1.2 * var(--u));
    border: none;
    border-radius: calc(1 * var(--u));
    background: none;
    text-shadow: var(--text-shadow);
  }
  .padlock.clickable {
    transition: transform 0.2s var(--spring), color 0.2s;
  }
  .reveal-button:hover .padlock,
  .reveal-button:focus-visible .padlock,
  .reveal-button:global([data-nav]) .padlock {
    color: var(--amber);
    transform: scale(1.08);
  }
  .prompt {
    position: absolute;
    left: calc(50% + 3.5 * var(--u));
    margin: 0;
    white-space: nowrap;
    text-shadow: var(--text-shadow);
  }
  /* Drumroll: halos beat outwards, the text trembles and grows until the reveal. */
  .suspense {
    position: relative;
    display: grid;
    place-items: center;
    animation: build 10s ease-in forwards;
  }
  .suspense > * {
    grid-area: 1 / 1;
  }
  .ring {
    width: calc(100% + 2 * var(--u));
    height: calc(100% + 0.6 * var(--u));
    border-radius: 50%;
    border: calc(0.25 * var(--u)) solid var(--amber);
    opacity: 0;
    animation: beat 1.6s ease-out infinite;
    pointer-events: none;
  }
  .ring.late {
    animation-delay: 0.8s;
  }
  .waiting {
    margin: 0;
    font-family: var(--font-display);
    font-size: calc(2.4 * var(--u));
    font-weight: 800;
    background: linear-gradient(100deg, var(--amber) 40%, var(--cream) 50%, var(--amber) 60%) 0 0 / 300% 100%;
    background-clip: text;
    color: transparent;
    filter: drop-shadow(0 0 calc(0.6 * var(--u)) rgba(255, 184, 28, 0.55));
    animation:
      shimmer 1.8s linear infinite,
      roll 0.12s linear infinite;
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
  @keyframes build {
    from {
      transform: scale(0.85);
    }
    to {
      transform: scale(1.15);
    }
  }
  @keyframes beat {
    from {
      opacity: 0.7;
      transform: none;
    }
    to {
      opacity: 0;
      transform: scale(1.25, 1.9);
    }
  }
  @keyframes shimmer {
    from {
      background-position: 100% 0;
    }
    to {
      background-position: 0 0;
    }
  }
  @keyframes roll {
    25% {
      translate: calc(0.04 * var(--u)) calc(-0.03 * var(--u));
    }
    50% {
      translate: calc(-0.03 * var(--u)) calc(0.04 * var(--u));
    }
    75% {
      translate: calc(0.03 * var(--u)) calc(0.03 * var(--u));
    }
  }
</style>
