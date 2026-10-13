<script lang="ts">
  // Start (04, "Start"): wordmark, resume or new game, the save notice (plan 55), the supply report (GF-5).
  import type { takeSaveNotice } from "../../lib/engine.ts";
  import { t } from "../../lib/i18n.ts";
  import type { Game, Supply } from "../../lib/types.ts";
  import EffectsDemo from "../EffectsDemo.svelte";
  import Fireworks from "../Fireworks.svelte";
  import Prompt from "../Prompt.svelte";
  import SupplyReport from "../SupplyReport.svelte";

  let {
    game,
    running,
    levels,
    supply,
    notice,
    busy,
    onresume,
    onnew,
    ondismiss,
  }: {
    game: Game | null;
    running: boolean;
    levels: number;
    supply: Supply | null;
    notice: ReturnType<typeof takeSaveNotice>;
    busy: boolean;
    onresume: () => void;
    onnew: () => void;
    ondismiss: () => void;
  } = $props();

  /** /?fuegos=<variant> or ?fuegos=finale plays fireworks over the Start screen (preview, UI-9). */
  const preview = new URLSearchParams(location.search).get("fuegos");
  /** /?efectos lists every effect, recorded and synthesized (audition aid, UI-10). */
  const effectsDemo = new URLSearchParams(location.search).has("efectos");
</script>

{#if preview}<Fireworks mode={preview === "finale" ? "finale" : "single"} variant={preview} />{/if}
{#if effectsDemo}<EffectsDemo />{/if}
<section class="start">
  <h1 class="wordmark"><span class="bang">{t("screen.start.open")}</span>{t("screen.start.name")}<span class="bang">{t("screen.start.close")}</span></h1>
  <p class="subtitle">{t("screen.start.subtitle", { n: levels })}</p>
  <div class="buttons">
    {#if notice}
      <div class="notice glass">
        <p>{t(notice.kind === "newer" ? "save.newer" : "save.corrupt", { path: notice.path })}</p>
        <button class="candy" onclick={ondismiss} data-focus-default data-focus-id="notice">{t("action.next")} <Prompt action="confirm" /></button>
      </div>
    {:else if running}
      <button class="candy breathe" onclick={onresume} disabled={busy} data-focus-default data-focus-id="main">
        {game?.player
          ? t("screen.start.resumePlayer", { name: game.player, level: game.level })
          : t("screen.start.resume", { level: game?.level ?? 0 })}
        <Prompt action="confirm" />
      </button>
      <button class="secondary" onclick={onnew} disabled={busy} data-focus-id="new">{t("screen.start.new")} <Prompt action="new" /></button>
    {:else}
      <button class="candy breathe" onclick={onnew} disabled={busy} data-focus-default data-focus-id="main">{t("screen.start.play")} <Prompt action="confirm" /></button>
    {/if}
  </div>
  {#if supply}<SupplyReport {supply} />{/if}
</section>

<style>
  section {
    position: absolute;
    inset: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: calc(1.4 * var(--u));
    padding: var(--safe-y) var(--safe-x);
    text-align: center;
  }
  p {
    margin: 0;
  }
  .wordmark {
    margin: 0;
    font-family: var(--font-display);
    font-size: calc(11 * var(--u));
    font-weight: 800;
    line-height: 1;
    color: var(--paper);
    text-shadow:
      0 calc(0.4 * var(--u)) 0 var(--slate-600),
      0 calc(0.8 * var(--u)) calc(2.5 * var(--u)) rgba(0, 0, 0, 0.5);
    animation: arrive 0.9s var(--spring) backwards;
  }
  .bang {
    display: inline-block;
    color: var(--amber);
    animation: bob 3s ease-in-out infinite;
  }
  .bang:last-child {
    animation-delay: -1.5s;
  }
  .subtitle {
    font-size: calc(1.6 * var(--u));
    color: var(--slate-200);
  }
  .buttons {
    display: flex;
    align-items: center;
    gap: calc(1.6 * var(--u));
    margin-top: calc(2 * var(--u));
  }
  .notice {
    max-width: calc(48 * var(--u));
    padding: calc(1 * var(--u)) calc(1.6 * var(--u));
    font-size: calc(1.1 * var(--u));
    color: var(--amber);
    overflow-wrap: anywhere;
  }
  @keyframes bob {
    50% {
      transform: translateY(calc(-0.6 * var(--u))) rotate(-6deg);
    }
  }
</style>
