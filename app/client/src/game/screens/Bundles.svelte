<script lang="ts">
  // The Bundles screen (plans/04-ui-tv-display.md, "Bundles"; plan 151, decisions 158, 260): «¿Qué preguntas
  // juega …?», between Player and Choice in every mode. The shared BundleSelector, two columns; exactly one base
  // bundle (D-85). Preset: the player's newest game's bundles, else the locale's first base bundle (decision 33).
  import { onMount } from "svelte";
  import { fetchChoice, fetchChoiceOptions, type ChoiceOptions } from "../../lib/api.ts";
  import { playerRegion } from "../../lib/desktop.ts";
  import { errorText } from "../../lib/errors.ts";
  import { t } from "../../lib/i18n.ts";
  import { pushScope, type Keys } from "../../lib/input.svelte.ts";
  import BundleSelector, { bundleKeys, orderBundles, toggled, type Bundle } from "../BundleSelector.svelte";
  import Icon from "../Icon.svelte";
  import Prompt from "../Prompt.svelte";

  let {
    player,
    busy,
    picked,
    onpick,
    onnext,
    onback,
  }: {
    player: string;
    busy: boolean;
    /** The pick kept in Game.svelte; null: not made yet, the preset applies. */
    picked: string[] | null;
    onpick: (ids: string[]) => void;
    onnext: () => void;
    onback: () => void;
  } = $props();

  let options = $state<ChoiceOptions | null>(null);
  let error = $state<string | null>(null);
  let section = $state<HTMLElement>();

  onMount(async () => {
    try {
      const [opts, preset] = await Promise.all([fetchChoiceOptions(), picked ? null : fetchChoice({ player })]);
      options = opts;
      if (preset) onpick(preset.choice.bundles);
    } catch (e) {
      error = errorText(e);
    }
  });

  const selected = $derived(picked ?? []);
  const ready = $derived(!!options && options.bundles.filter((b) => b.base && selected.includes(b.id)).length === 1);

  function pick(ids: string[]) {
    if (!busy) onpick(ids);
  }

  function next() {
    if (ready && !busy) onnext();
  }

  const shown = $derived(orderBundles(options?.bundles ?? [], playerRegion));
  const letters = $derived(bundleKeys(shown.map((b) => b.name), [t("flag.key")]));
  const keyOf = (b: Bundle) => letters[shown.indexOf(b)] ?? "";
  const keys = $derived<Keys>(Object.fromEntries(letters.filter(Boolean).map((key) => [key, { type: "letter", key }])));

  // A bundle's letter toggles it and scrolls it into view (focus stays, Enter still continues); arrows move between tiles and buttons, Enter/A presses the focused one;
  // Backspace/B goes back; Esc falls through to the overlay.
  $effect(() =>
    pushScope({
      name: "bundles",
      root: () => section,
      get keys() {
        return keys;
      },
      handle: (a) => {
        const b = a.type === "letter" ? options?.bundles.find((x) => keyOf(x) === a.key) : undefined;
        if (b && options) {
          pick(toggled(options.bundles, selected, b));
          section?.querySelector(`[data-focus-id="bundle-${b.id}"]`)?.scrollIntoView({ block: "nearest" });
        }
        else if (a.type === "confirm") next();
        else if (a.type === "back") onback();
        else return false;
        return true;
      },
    }),
  );
</script>

<section class="bundles-screen" bind:this={section}>
  <h1 class="title">{t("bundles.titleOpen")}<span class="name">{player}</span>{t("bundles.titleClose")}</h1>

  {#if options}
    <BundleSelector bundles={options.bundles} {selected} {busy} {keyOf} large onchange={pick} />

    <div class="actions">
      <button class="secondary" onclick={onback} disabled={busy} data-focus-id="back"><Icon name="back" /> {t("action.back")} <Prompt action="back" /></button>
      <button class="candy" onclick={next} disabled={busy || !ready} data-focus-default data-focus-id="next"><Icon name="next" /> {t("action.next")} <Prompt action="confirm" off={!ready} /></button>
    </div>
  {/if}

  {#if error}<p class="error">{error}</p>{/if}
</section>

<style>
  .bundles-screen {
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
    flex: none;
    animation: arrive 0.6s var(--spring) backwards;
  }
  .name {
    color: var(--amber);
  }
  .actions {
    flex: none;
    display: flex;
    gap: calc(1.2 * var(--u));
    align-items: center;
    margin-top: calc(1 * var(--u));
    animation: arrive 0.5s 0.4s var(--spring) backwards;
  }
  .error {
    margin: 0;
    color: var(--coral);
    font-size: calc(1.1 * var(--u));
  }
</style>
