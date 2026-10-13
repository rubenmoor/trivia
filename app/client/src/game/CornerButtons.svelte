<script lang="ts">
  // Top right over every screen: the error line (B-18), the flag (GM-5) and menu (IN-1) buttons.
  import { t } from "../lib/i18n.ts";
  import Icon from "./Icon.svelte";

  let {
    error,
    flagged,
    menu,
    onflag,
    onmenu,
  }: {
    error: string | null;
    /** null: no flag button. */
    flagged: boolean | null;
    menu: boolean;
    onflag: () => void;
    onmenu: () => void;
  } = $props();

  const FLAG_KEY = t("flag.key");
</script>

{#if error}
  <div class="error-box corner">{error}</div>
{/if}

{#if flagged !== null}
  <!-- Flag for review (GM-5): as faint as the menu button; no focus, like it. -->
  <button
    class="flag-button"
    class:on={flagged}
    onclick={onflag}
    onmousedown={(e) => e.preventDefault()}
    tabindex="-1"
    data-nofocus
    aria-label={t(flagged ? "flag.on" : "flag.off", { key: FLAG_KEY })}
    title={t(flagged ? "flag.on" : "flag.off", { key: FLAG_KEY })}
  >
    <Icon name="flag" />
  </button>
{/if}

{#if menu}
  <!-- The overlay for the mouse (IN-1); no focus, so a later Enter can't open it. -->
  <button
    class="menu-button"
    onclick={onmenu}
    onmousedown={(e) => e.preventDefault()}
    tabindex="-1"
    data-nofocus
    aria-label={t("a11y.menu")}
    title={t("a11y.menu")}
  >
    <span></span><span></span><span></span>
  </button>
{/if}

<style>
  .error-box {
    color: var(--coral);
    background: rgba(40, 10, 18, 0.9);
    border: 1px solid var(--coral);
    border-radius: calc(0.6 * var(--u));
    padding: calc(0.5 * var(--u)) calc(1 * var(--u));
    font-size: calc(1.1 * var(--u));
  }
  .menu-button {
    position: fixed;
    top: calc(var(--safe-y) * 0.5);
    right: calc(var(--safe-x) * 0.5);
    z-index: 30;
    display: flex;
    flex-direction: column;
    justify-content: center;
    gap: calc(0.35 * var(--u));
    width: calc(3.2 * var(--u));
    height: calc(3.2 * var(--u));
    padding: 0 calc(0.8 * var(--u));
    border: 1px solid transparent;
    border-radius: calc(0.8 * var(--u));
    background: transparent;
    opacity: 0.35;
    transition:
      opacity 0.2s,
      background 0.2s;
  }
  .menu-button:hover {
    opacity: 1;
    background: var(--glass-strong);
    border-color: var(--slate-400);
  }
  .menu-button span {
    height: calc(0.25 * var(--u));
    border-radius: calc(0.15 * var(--u));
    background: var(--paper);
  }
  .flag-button {
    position: fixed;
    top: calc(var(--safe-y) * 0.5);
    right: calc(var(--safe-x) * 0.5 + 3.8 * var(--u));
    z-index: 30;
    display: grid;
    place-items: center;
    width: calc(3.2 * var(--u));
    height: calc(3.2 * var(--u));
    padding: 0;
    border: 1px solid transparent;
    border-radius: calc(0.8 * var(--u));
    background: transparent;
    color: var(--paper);
    font-size: calc(1.6 * var(--u));
    opacity: 0.35;
    transition:
      opacity 0.2s,
      background 0.2s;
  }
  .flag-button:hover {
    opacity: 1;
    background: var(--glass-strong);
    border-color: var(--slate-400);
  }
  .flag-button.on {
    --flag-fill: 1;
    color: var(--amber);
    opacity: 0.7;
  }
  /* Beside the flag and menu buttons, above the question card (B-18). */
  .corner {
    position: fixed;
    top: calc(var(--safe-y) * 0.5);
    right: calc(var(--safe-x) * 0.5 + 7.6 * var(--u));
    max-width: 55vw;
    min-height: calc(3.2 * var(--u));
    display: flex;
    align-items: center;
    z-index: 35;
  }
</style>
