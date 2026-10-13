<script lang="ts">
  // «Dificultad y paquetes» of the gamemaster menu (MD-12, D-88): the configure screen's difficulty row and
  // the shared bundle selector for the running game; «Aplicar» sends `settings` (new table, level and history stay).
  // ↑/↓ move, ←/→ or −/+ change the difficulty, Enter on a row applies, Esc/⌫/B cancel.
  import { onMount } from "svelte";
  import { DIFFICULTY_MAX, fetchChoiceOptions, fetchGameSettings, type ChoiceOptions, type GameActionBody } from "../lib/api";
  import { errorText } from "../lib/errors";
  import { t } from "../lib/i18n";
  import { focusControl, pushScope } from "../lib/input.svelte";
  import type { Difficulty, Game } from "../lib/types";
  import BundleSelector from "./BundleSelector.svelte";
  import { spanOf, stepDifficulty } from "./difficulty";
  import Prompt from "./Prompt.svelte";

  let {
    settings,
    onapply,
    onclose,
  }: {
    settings: Game["settings"];
    /** Runs `settings`; the refusal's text, or null when applied. */
    onapply: (body: GameActionBody) => Promise<string | null>;
    onclose: () => void;
  } = $props();

  let dialog = $state<HTMLDivElement>();
  let options = $state<ChoiceOptions | null>(null);
  let group = $state<string | null>(null);
  let custom = $state(false);
  let difficulty = $state<Difficulty>({ start: 1, end: DIFFICULTY_MAX });
  let bundles = $state<string[]>([]);
  let busy = $state(false);
  let error = $state<string | null>(null);

  onMount(async () => {
    try {
      const [opts, c] = await Promise.all([fetchChoiceOptions("game"), fetchGameSettings(settings)]);
      options = opts;
      group = c.age_group ?? opts.groups[0]?.id ?? null;
      custom = c.difficulty !== null;
      difficulty = c.difficulty ?? spanOf(opts.groups, group);
      bundles = c.bundles;
    } catch (e) {
      error = errorText(e);
    }
  });

  /** As on the configure screen: ←/→ cycles the age groups, then «Custom». */
  function step(id: string, by: number) {
    if (busy || !options) return;
    error = null;
    const pick = stepDifficulty(options.groups, { group, custom, difficulty }, id, by);
    if (pick) ({ group, custom, difficulty } = pick);
  }

  async function apply() {
    if (busy || !options) return;
    busy = true;
    const body = custom ? { difficulty: { ...difficulty }, bundles: [...bundles] } : { age_group: group, bundles: [...bundles] };
    error = await onapply(body);
    busy = false;
  }

  $effect(() => {
    const pop = pushScope({
      name: "game-settings",
      modal: true,
      whileBusy: true,
      root: () => dialog,
      pressable: (el) => !el.dataset.step,
      handle: (a) => {
        const id = document.activeElement instanceof HTMLElement ? document.activeElement.dataset.step : undefined;
        if (a.type === "navigate" && id && (a.dir === "left" || a.dir === "right")) step(id, a.dir === "right" ? 1 : -1);
        else if (a.type === "confirm") apply();
        else if (a.type === "back" || a.type === "menu") {
          if (!busy) onclose();
        }
        else return false;
        return true;
      },
    });
    return pop;
  });

  $effect(() => {
    if (options) focusControl(dialog?.querySelector<HTMLElement>("[data-focus-default]"));
  });

  const g = $derived(options?.groups.find((x) => x.id === group));
</script>

<div class="backdrop">
  <div class="dialog" bind:this={dialog} role="dialog" aria-labelledby="game-settings-title">
    <h2 id="game-settings-title">{t("overlay.settings")}</h2>
    <p class="note">{t("overlay.settingsNote")}</p>
    {#if options}
      <div class="lines">
        {@render stepper("difficulty", t("configure.difficulty"), custom ? t("configure.custom") : (g?.name ?? ""), true)}
        {#if custom}
          {@render stepper("start", t("configure.start"), String(difficulty.start))}
          {@render stepper("end", t("configure.end"), String(difficulty.end))}
        {/if}
      </div>
      <BundleSelector bundles={options.bundles} selected={bundles} {busy} onchange={(ids) => ((bundles = ids), (error = null))} />
    {/if}
    {#if error}<p class="error">{error}</p>{/if}
    <div class="choices">
      <button class="secondary" onclick={onclose} disabled={busy}>{t("action.cancel")} <Prompt action="back" /></button>
      <button class="candy" onclick={apply} disabled={busy || !options}>{t("overlay.apply")} <Prompt action="confirm" /></button>
    </div>
  </div>
</div>

{#snippet stepper(id: string, label: string, value: string, first = false)}
  <!-- svelte-ignore a11y_no_noninteractive_tabindex -->
  <div class="row" data-step={id} data-focusable data-focus-default={first || undefined} tabindex="0" role="group" aria-label={label}>
    <span>{label}</span>
    <button class="step" onclick={() => step(id, -1)} disabled={busy} tabindex="-1" aria-label={t("overlay.less")}>−</button>
    <span class="value">{value}</span>
    <button class="step" onclick={() => step(id, 1)} disabled={busy} tabindex="-1" aria-label={t("overlay.more")}>+</button>
  </div>
{/snippet}

<style>
  .backdrop {
    position: fixed;
    inset: 0;
    z-index: 41;
    display: grid;
    place-items: center;
    background: var(--dim);
  }
  .dialog {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: calc(1 * var(--u));
    max-width: calc(110 * var(--u));
    max-height: calc(100vh - 2 * var(--u));
    overflow-y: auto;
    padding: calc(2.4 * var(--u));
    border: 1px solid var(--slate-600);
    border-radius: calc(1.6 * var(--u));
    background: var(--night-700);
    box-shadow: 0 calc(1.5 * var(--u)) calc(4 * var(--u)) rgba(0, 0, 0, 0.6);
  }
  h2 {
    margin: 0;
    font-family: var(--font-display);
    font-size: calc(2.6 * var(--u));
    font-weight: 800;
  }
  .note {
    margin: 0;
    color: var(--slate-400);
  }
  .lines {
    display: flex;
    flex-direction: column;
    gap: calc(0.5 * var(--u));
    width: calc(40 * var(--u));
  }
  .row {
    display: grid;
    grid-template-columns: 1fr calc(2.4 * var(--u)) calc(14 * var(--u)) calc(2.4 * var(--u));
    align-items: center;
    gap: calc(0.8 * var(--u));
    padding: calc(0.4 * var(--u)) calc(1.2 * var(--u));
    border: calc(0.18 * var(--u)) solid transparent;
    border-radius: calc(0.8 * var(--u));
    background: rgba(43, 54, 80, 0.5);
    font-size: calc(1.3 * var(--u));
    font-weight: 700;
    outline: none;
  }
  .row:focus,
  .row:global([data-nav]),
  .row:hover {
    border-color: var(--amber);
  }
  .value {
    text-align: center;
    color: var(--amber);
    font-variant-numeric: tabular-nums;
  }
  .step {
    display: grid;
    place-items: center;
    height: calc(2.2 * var(--u));
    padding: 0;
    border-radius: calc(0.8 * var(--u));
    background: var(--slate-600);
    font-size: calc(1.4 * var(--u));
    font-weight: 700;
  }
  .error {
    margin: 0;
    color: var(--coral);
    font-size: calc(1.1 * var(--u));
  }
  .choices {
    display: flex;
    justify-content: center;
    gap: calc(1 * var(--u));
  }
</style>
