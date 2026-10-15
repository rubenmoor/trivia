<script lang="ts">
  // Start (04, "Start"): wordmark, resume or new game, the save notice (plan 55), the Mods button
  // in the shell (plan 118), the language button top right (plan 126).
  import type { takeSaveNotice } from "../../lib/engine.ts";
  import { endonym, lang, t } from "../../lib/i18n.ts";
  import type { Game } from "../../lib/types.ts";
  import EffectsDemo from "../EffectsDemo.svelte";
  import Fireworks from "../Fireworks.svelte";
  import Flags from "../Flags.svelte";
  import Icon from "../Icon.svelte";
  import Prompt from "../Prompt.svelte";

  let {
    game,
    running,
    levels,
    notice,
    busy,
    mods = null,
    onresume,
    onnew,
    ondismiss,
    onmods,
    onlanguage,
  }: {
    game: Game | null;
    running: boolean;
    levels: number;
    notice: ReturnType<typeof takeSaveNotice>;
    busy: boolean;
    /** Null outside the shell: no Mods button. */
    mods?: { loaded: number; held: number } | null;
    onresume: () => void;
    onnew: () => void;
    ondismiss: () => void;
    onmods?: () => void;
    onlanguage: () => void;
  } = $props();

  /** /?fuegos=<variant> or ?fuegos=finale plays fireworks over the Start screen (preview, UI-9). */
  const preview = new URLSearchParams(location.search).get("fuegos");
  /** /?efectos lists every effect, recorded and synthesized (audition aid, UI-10). */
  const effectsDemo = new URLSearchParams(location.search).has("efectos");
</script>

{#if preview}<Fireworks mode={preview === "finale" ? "finale" : "single"} variant={preview} />{/if}
{#if effectsDemo}<EffectsDemo />{/if}
<section class="start">
  {#if !notice}
    <button class="language glass" onclick={onlanguage} disabled={busy} data-focus-id="language" aria-label={t("screen.start.language", { name: endonym(lang) })}>
      <Flags tag={lang} size="1.1em" />
      {endonym(lang)}
      <Prompt action="language" />
    </button>
  {/if}
  <h1 class="wordmark"><span class="bang">{t("screen.start.open")}</span>{t("screen.start.name")}<span class="bang">{t("screen.start.close")}</span></h1>
  <p class="subtitle">{t("screen.start.subtitle", { n: levels })}</p>
  <div class="buttons">
    {#if notice}
      <div class="notice glass">
        <p>{notice.kind === "unsaved" ? t("save.unsaved") : t(notice.kind === "newer" ? "save.newer" : "save.corrupt", { path: notice.path })}</p>
        <button class="candy" onclick={ondismiss} data-focus-default data-focus-id="notice"><Icon name="next" /> {t("action.next")} <Prompt action="confirm" /></button>
      </div>
    {:else if running}
      <button class="candy breathe" onclick={onresume} disabled={busy} data-focus-default data-focus-id="main">
        <Icon name="play" />
        {game?.player
          ? t("screen.start.resumePlayer", { name: game.player, level: game.level })
          : t("screen.start.resume", { level: game?.level ?? 0 })}
        <Prompt action="confirm" />
      </button>
      <button class="secondary" onclick={onnew} disabled={busy} data-focus-id="new"><Icon name="sparkle" /> {t("screen.start.new")} <Prompt action="new" /></button>
    {:else}
      <button class="candy breathe" onclick={onnew} disabled={busy} data-focus-default data-focus-id="main"><Icon name="rocket" /> {t("screen.start.play")} <Prompt action="confirm" /></button>
    {/if}
    {#if mods && !notice}
      <button class="secondary" onclick={onmods} disabled={busy} data-focus-id="mods">
        <Icon name="puzzle" /> {t("mods.open")}{#if mods.loaded}<span class="count">{mods.loaded}</span>{/if}
      </button>
    {/if}
  </div>
  {#if mods?.held && !notice}<p class="held">{t("mods.held", { n: mods.held })}</p>{/if}</section>

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
  .language {
    position: absolute;
    top: calc(var(--safe-y) * 0.5 + 4 * var(--u)); /* under the ☰ menu button, clear of the error line */
    right: calc(var(--safe-x) * 0.5);
    display: flex;
    align-items: center;
    gap: calc(0.6 * var(--u));
    padding: calc(0.5 * var(--u)) calc(1 * var(--u));
    font-size: calc(1.3 * var(--u));
    font-weight: 700;
    color: var(--slate-200);
  }
  .count {
    margin-left: calc(0.6 * var(--u));
    padding: 0 calc(0.6 * var(--u));
    border-radius: calc(0.6 * var(--u));
    background: var(--slate-600);
  }
  .held {
    font-size: calc(1.2 * var(--u));
    color: var(--amber);
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
