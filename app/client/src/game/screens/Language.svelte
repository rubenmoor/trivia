<script lang="ts">
  // The first-start language screen (plan 68, I18N-2): a fresh save picks its UI language once, the
  // guess preselected; the questions follow it (plan 126). Later: Start's language button, with `onback`.
  import { onMount, tick } from "svelte";
  import { fetchLanguage, setLanguage } from "../../lib/api.ts";
  import { errorText } from "../../lib/errors.ts";
  import { endonym, lang, t } from "../../lib/i18n.ts";
  import { focusControl, pushScope } from "../../lib/input.svelte.ts";
  import Prompt from "../Prompt.svelte";

  let { onpicked, onback }: { onpicked: () => void; onback?: () => void } = $props();

  let options = $state<string[]>([]);
  /** The focused option; confirm picks it. */
  let current = $state<string | null>(null);
  let saving = $state(false);
  let error = $state<string | null>(null);
  let section = $state<HTMLElement>();
  const buttons: Record<string, HTMLButtonElement> = {};

  onMount(async () => {
    try {
      const l = await fetchLanguage();
      options = l.options;
      current = l.language;
      await tick();
      focusControl(buttons[l.language]);
    } catch (e) {
      error = errorText(e);
    }
  });

  /** A language other than the boot one reloads (it's a boot constant). */
  async function choose(ui: string) {
    if (saving) return;
    saving = true;
    try {
      await setLanguage(ui);
      if (ui !== lang) location.reload();
      else onpicked();
    } catch (e) {
      error = errorText(e);
      saving = false;
    }
  }

  $effect(() =>
    pushScope({
      name: "language",
      root: () => section,
      handle: (a) => {
        if (a.type === "confirm" && current) choose(current);
        else if (a.type === "pick" && a.n <= options.length) choose(options[a.n - 1]);
        else if (a.type === "back" && onback && !saving) onback();
        else return a.type === "menu"; // no Esc menu here: nothing to configure yet
        return true;
      },
    }),
  );
</script>

<section class="language" bind:this={section}>
  <h1 class="title">{t("language.choose")}</h1>
  <div class="options">
    {#each options as tag, i (tag)}
      <button
        class="option glass"
        class:current={tag === current}
        bind:this={buttons[tag]}
        onclick={() => choose(tag)}
        onfocus={() => (current = tag)}
        disabled={saving}
        data-focus-default={tag === current || undefined}
        style:--i={i}
      >
        {endonym(tag)}
      </button>
    {/each}
  </div>
  {#if options.length}<p class="label">{t("language.confirm")} <Prompt action="confirm" /></p>{/if}
  {#if onback}<button class="secondary" onclick={onback} disabled={saving}>{t("action.back")} <Prompt action="back" /></button>{/if}
  {#if error}<p class="error">{error}</p>{/if}
</section>

<style>
  .language {
    position: absolute;
    inset: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: calc(2 * var(--u));
    padding: var(--safe-y) var(--safe-x);
    text-align: center;
  }
  .title {
    animation: arrive 0.6s var(--spring) backwards;
  }
  .options {
    display: flex;
    flex-direction: column;
    gap: calc(1 * var(--u));
    min-width: calc(28 * var(--u));
  }
  .option {
    padding: calc(1 * var(--u)) calc(2 * var(--u));
    border-color: var(--slate-600);
    font-family: var(--font-display);
    font-size: calc(2.2 * var(--u));
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
  .error {
    margin: 0;
    color: var(--coral);
    font-size: calc(1.1 * var(--u));
  }
</style>
