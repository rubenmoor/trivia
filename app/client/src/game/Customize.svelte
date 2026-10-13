<script lang="ts">
  // «Personalizar partida» (MD-7): joker counts for a «Solo o en grupo» game, 0–9 or ∞ like the
  // overlay's budget (MD-4). ↑/↓ move, ←/→ or −/+ change a count, Enter/Esc/⌫ close.
  import { t } from "../lib/i18n";
  import { focusControl, pushScope } from "../lib/input.svelte";
  import type { JokerBudget, JokerName } from "../lib/types";
  import { TOKENS } from "./JokerTray.svelte";
  import Prompt from "./Prompt.svelte";

  const MAX_USES = 9;

  let {
    jokers,
    standard,
    onchange,
    onclose,
  }: { jokers: JokerBudget; standard: JokerBudget; onchange: (jokers: JokerBudget) => void; onclose: () => void } = $props();

  let dialog = $state<HTMLDivElement>();

  function step(name: JokerName, by: number) {
    const now = jokers[name];
    const index = Math.min(MAX_USES + 1, Math.max(0, (now ?? MAX_USES + 1) + by));
    const next = index > MAX_USES ? null : index;
    if (next !== now) onchange({ ...jokers, [name]: next });
  }

  const jokerOf = (el: Element | null) => (el instanceof HTMLElement ? (el.dataset.joker as JokerName | undefined) : undefined);

  $effect(() => {
    const pop = pushScope({
      name: "customize",
      modal: true,
      root: () => dialog,
      pressable: (el) => !el.dataset.joker,
      handle: (a) => {
        const name = jokerOf(document.activeElement);
        if (a.type === "navigate" && name && (a.dir === "left" || a.dir === "right")) step(name, a.dir === "right" ? 1 : -1);
        else if (a.type === "back" || a.type === "menu" || a.type === "confirm") onclose();
        else return false;
        return true;
      },
    });
    focusControl(dialog?.querySelector<HTMLElement>("[data-joker]"));
    return pop;
  });
</script>

<div class="backdrop">
  <div class="dialog" bind:this={dialog} role="dialog" aria-labelledby="customize-title">
    <h2 id="customize-title">{t("customize.title")}</h2>
    <p class="note">{t("customize.body")}</p>
    {#each TOKENS as token, i (token.name)}
      {@const name = token.name}
      <!-- svelte-ignore a11y_no_noninteractive_tabindex -->
      <div class="row" data-joker={name} data-focusable data-focus-default={i === 0 || undefined} tabindex="0" role="group">
        <span>{token.label}</span>
        <button class="step" onclick={() => step(name, -1)} tabindex="-1" aria-label={t("overlay.less")}>−</button>
        <span class="value" class:changed={jokers[name] !== standard[name]}>{jokers[name] ?? "∞"}</span>
        <button class="step" onclick={() => step(name, 1)} tabindex="-1" aria-label={t("overlay.more")}>+</button>
      </div>
    {/each}
    <div class="choices">
      <button class="secondary" onclick={() => onchange({ ...standard })}>{t("customize.reset")}</button>
      <button class="candy" onclick={onclose}>{t("customize.done")} <Prompt action="confirm" /></button>
    </div>
  </div>
</div>

<style>
  .backdrop {
    position: fixed;
    inset: 0;
    z-index: 40;
    display: grid;
    place-items: center;
    background: rgba(5, 8, 16, 0.72);
  }
  .dialog {
    display: flex;
    flex-direction: column;
    gap: calc(0.7 * var(--u));
    min-width: calc(36 * var(--u));
    padding: calc(2.4 * var(--u));
    border: 1px solid var(--slate-600);
    border-radius: calc(1.6 * var(--u));
    background: var(--night-700);
    box-shadow: 0 calc(1.5 * var(--u)) calc(4 * var(--u)) rgba(0, 0, 0, 0.6);
  }
  h2 {
    margin: 0;
    text-align: center;
    font-family: var(--font-display);
    font-size: calc(2.6 * var(--u));
    font-weight: 800;
  }
  .note {
    margin: 0 0 calc(0.4 * var(--u));
    text-align: center;
    color: var(--slate-400);
  }
  .row {
    display: grid;
    grid-template-columns: 1fr calc(2.4 * var(--u)) calc(2.4 * var(--u)) calc(2.4 * var(--u));
    align-items: center;
    gap: calc(1 * var(--u));
    padding: calc(0.45 * var(--u)) calc(1.4 * var(--u));
    border: calc(0.18 * var(--u)) solid transparent;
    border-radius: calc(0.8 * var(--u));
    background: rgba(43, 54, 80, 0.5);
    font-size: calc(1.4 * var(--u));
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
    color: var(--slate-200);
    font-variant-numeric: tabular-nums;
  }
  .value.changed {
    color: var(--amber);
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
  .choices {
    display: flex;
    justify-content: center;
    gap: calc(1 * var(--u));
    margin-top: calc(0.6 * var(--u));
  }
</style>
