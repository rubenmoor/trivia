<script lang="ts">
  // The first-start telemetry question (plan 108, decision 121): asked once per install, «No» focused;
  // skipping isn't an answer. Later changes: the Esc menu.
  import { onMount, tick } from "svelte";
  import { t } from "../../lib/i18n.ts";
  import { focusControl, pushScope } from "../../lib/input.svelte.ts";
  import { setTelemetryConsent } from "../../lib/telemetry.ts";
  import Icon from "../Icon.svelte";
  import Prompt from "../Prompt.svelte";

  let { ondone }: { ondone: () => void } = $props();

  /** On screen in this order; `pick` n is the n-th. */
  const OPTIONS = [false, true] as const;
  let current = $state(false);
  let saving = $state(false);
  let section = $state<HTMLElement>();
  const buttons: HTMLButtonElement[] = [];

  onMount(async () => {
    await tick();
    focusControl(buttons[0]);
  });

  /** A failed call stays silent: still unanswered, asked again next start. */
  async function choose(yes: boolean) {
    if (saving) return;
    saving = true;
    try {
      await setTelemetryConsent(yes);
    } catch (e) {
      console.warn("telemetry consent:", e);
    }
    ondone();
  }

  $effect(() =>
    pushScope({
      name: "consent",
      root: () => section,
      handle: (a) => {
        if (a.type === "confirm") choose(current);
        else if (a.type === "pick" && a.n <= OPTIONS.length) choose(OPTIONS[a.n - 1]);
        else if (a.type === "back") choose(false);
        else return a.type === "menu"; // no Esc menu here
        return true;
      },
    }),
  );
</script>

<section class="screen consent" bind:this={section}>
  <h1 class="title">{t("consent.title")}</h1>
  <p class="body">{t("consent.body")}</p>
  <p class="line">{t("consent.noNames")}<br />{t("consent.change")} <Prompt action="menu" /></p>
  <div class="options">
    {#each OPTIONS as yes, i (yes)}
      <button
        class="option glass"
        class:current={yes === current}
        bind:this={buttons[i]}
        onclick={() => choose(yes)}
        onfocus={() => (current = yes)}
        disabled={saving}
        data-focus-default={!yes || undefined}
        style:--i={i}
      >
        <Icon name={yes ? "check" : "cross"} /> {t(yes ? "consent.yes" : "consent.no")}
      </button>
    {/each}
  </div>
</section>

<style>
  .consent {
    gap: calc(2 * var(--u));
  }
  .title {
    animation: arrive 0.6s var(--spring) backwards;
  }
  .body,
  .line {
    margin: 0;
    max-width: calc(60 * var(--u));
    font-size: calc(1.6 * var(--u));
    line-height: 1.4;
  }
  .line {
    color: var(--slate-200);
    font-size: calc(1.3 * var(--u));
  }
  .options {
    display: flex;
    gap: calc(1.5 * var(--u));
  }
  .option {
    min-width: calc(14 * var(--u));
    padding: calc(1 * var(--u)) calc(2 * var(--u));
    border-color: var(--slate-600);
    font-family: var(--font-display);
    font-size: calc(2 * var(--u));
    font-weight: 800;
    animation: arrive 0.5s calc(0.15s + var(--i) * 0.06s) var(--spring) backwards;
    transition:
      transform 0.2s var(--spring),
      border-color 0.2s;
  }
  .option.current,
  .option:hover:not(:disabled),
  .option:focus-visible,
  .option:global([data-nav]) {
    border-color: var(--sky);
    transform: translateY(calc(-0.3 * var(--u)));
  }
</style>
