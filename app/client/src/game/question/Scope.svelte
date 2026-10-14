<script lang="ts">
  // «Francotirador» (plans/09-jokers.md, JK-8): the scope's hole over the target answer, the aim and hit lines.
  // Markup only: aiming keys stay in screens/Question.svelte's input scope.
  import { t } from "../../lib/i18n.ts";
  import Icon from "../Icon.svelte";
  import Prompt from "../Prompt.svelte";

  let {
    tile,
    tight,
    aiming,
    hit,
    oncancel,
  }: {
    /** The answer tile under the scope, or null. */
    tile: HTMLElement | null;
    /** The shot is out: the scope tightens. */
    tight: boolean;
    aiming: boolean;
    hit: boolean;
    oncancel: () => void;
  } = $props();

  let hole = $state<{ x: number; y: number; w: number; h: number } | null>(null);
  $effect(() => {
    if (!tile) return void (hole = null);
    const r = tile.getBoundingClientRect();
    hole = { x: r.left + r.width / 2, y: r.top + r.height / 2, w: r.width, h: r.height };
  });
</script>

{#if hole}
  <div
    class="scope"
    class:tight
    style:left="{hole.x}px"
    style:top="{hole.y}px"
    style:width="{hole.w + 40}px"
    style:height="{hole.h + 40}px"
    aria-hidden="true"
  >
    <span class="reticle"><Icon name="crosshair" size="100%" /></span>
  </div>
{/if}
{#if aiming}
  <p class="aim-hint glass-strong">
    <Icon name="crosshair" /> {t("joker.snipe.aim")} <b>{t("joker.snipe.false")}</b> · <Prompt action="confirm" /> {t("joker.snipe.shoot")}
    <button class="secondary cancel" onclick={oncancel}>{t("action.cancel")} <Prompt action="menu" pad="back" /></button>
  </p>
{/if}
{#if hit}
  <p class="aim-hint hit glass-strong">{t("joker.snipe.hit")}</p>
{/if}

<style>
  .aim-hint {
    position: absolute;
    z-index: 7;
    left: 50%;
    top: 45%;
    transform: translateX(-50%);
    margin: 0;
    padding: calc(0.6 * var(--u)) calc(1.4 * var(--u));
    font-family: var(--font-display);
    font-size: calc(1.4 * var(--u));
    font-weight: 700;
    white-space: nowrap;
  }
  .aim-hint .cancel {
    margin-left: calc(0.8 * var(--u));
    padding: calc(0.3 * var(--u)) calc(1 * var(--u));
    font-size: calc(1.2 * var(--u));
  }
  .aim-hint.hit {
    color: var(--mint);
    font-size: calc(2 * var(--u));
  }
  .scope {
    position: fixed;
    z-index: 6;
    border-radius: 50%;
    transform: translate(-50%, -50%);
    box-shadow: 0 0 0 200vmax rgba(5, 8, 16, 0.62);
    pointer-events: none;
    transition:
      left 0.25s var(--spring),
      top 0.25s var(--spring),
      width 0.25s,
      height 0.25s,
      box-shadow 0.4s;
    animation: scope-in 0.35s ease-out;
  }
  .scope.tight {
    width: calc(var(--u) * 26) !important;
    box-shadow: 0 0 0 200vmax rgba(5, 8, 16, 0.85);
  }
  .reticle {
    position: absolute;
    left: 50%;
    top: 50%;
    width: calc(7 * var(--u));
    height: calc(7 * var(--u));
    transform: translate(-50%, -50%);
    color: var(--coral);
    filter: drop-shadow(0 0 calc(0.5 * var(--u)) rgba(255, 84, 112, 0.8));
    animation: spin 3s linear infinite;
  }
  .tight .reticle {
    animation: spin 0.8s linear infinite;
  }
  @keyframes scope-in {
    from {
      box-shadow: 0 0 0 200vmax rgba(5, 8, 16, 0);
    }
  }
  @keyframes spin {
    to {
      transform: rotate(360deg);
    }
  }
</style>
