<script lang="ts">
  // The Bundles screen (plans/04-ui-tv-display.md, "Bundles"; plan 151, decisions 158, 264): «¿Qué preguntas
  // juega …?», after Choice in every mode; «¡A jugar!» starts the game. The shared BundleSelector, base column and flowing tiles; any
  // combination, base bundles toggle too. Preset: the player's newest game's bundles, else the locale's first base bundle (decision 33).
  // The supply of the whole choice (Choice's picks + bundles) is checked on every toggle: report and disabled start
  // when short (decisions 206, 268); the running-out notice (plan 65, decision 31) comes before level 1.
  import { onMount } from "svelte";
  import { fetchChoice, fetchChoiceOptions, fetchOutlook, type ChoiceBody, type ChoiceOptions, type Outlook } from "../../lib/api.ts";
  import { playerRegion } from "../../lib/desktop.ts";
  import { GameError } from "../../lib/http.ts";
  import { errorText } from "../../lib/errors.ts";
  import { t } from "../../lib/i18n.ts";
  import { pushScope, type Keys } from "../../lib/input.svelte.ts";
  import BundleSelector, { bundleKeys, orderBundles, toggled, type Bundle } from "../BundleSelector.svelte";
  import type { GameMode, Supply } from "../../lib/types.ts";
  import { bodyOf, choiceOf, type ChoiceDraft } from "../choiceDraft.ts";
  import Icon from "../Icon.svelte";
  import Prompt from "../Prompt.svelte";
  import SupplyNotice, { worthShowing } from "../SupplyNotice.svelte";
  import SupplyReport from "../SupplyReport.svelte";

  let {
    player,
    draft,
    busy,
    greeting,
    refused,
    picked,
    onpick,
    onstart,
    onback,
  }: {
    player: string;
    /** Choice's picks. */
    draft: ChoiceDraft;
    busy: boolean;
    /** The name while «¡Hola, …!» plays into the transition, else null. */
    greeting: string | null;
    /** Why the last `new` was refused (supply, `no_questions`, `bundle_not_offered`), or null. */
    refused: GameError | null;
    /** The pick kept in Game.svelte; null: not made yet, the preset applies. */
    picked: string[] | null;
    onpick: (ids: string[]) => void;
    /** `runningOut`: the bundles the supply notice showed (plan 65). */
    onstart: (choice: ChoiceBody & { mode: GameMode }, runningOut: string[]) => void;
    onback: () => void;
  } = $props();

  let options = $state<ChoiceOptions | null>(null);
  let error = $state<string | null>(null);
  let section = $state<HTMLElement>();
  /** The supply of the current choice; null while unknown or refused. */
  let supply = $state<Supply | null>(null);
  /** Why the engine refuses the current choice (the selection has no question, `no_questions`). */
  let reason = $state<string | null>(null);
  /** The choice changed since `refused` came. */
  let stale = $state(false);
  /** The supply notice before level 1 (decision 31), or null; `checking` while it's computed. */
  let notice = $state<{ outlook: Outlook; choice: ChoiceBody & { mode: GameMode } } | null>(null);
  let checking = false;
  let seq = 0;

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
  // No question for the choice (nothing selected, or the bundles hold none for the group and levels): start off.
  const empty = $derived(!!supply && supply.levels.every((l) => l.candidates === 0));
  const ready = $derived(!!options && !!picked && !!supply?.ok && !reason);
  const shownRefusal = $derived(refused && !stale ? refused : null);

  $effect(() => {
    void refused;
    stale = false;
  });

  // Supply of the full choice, recomputed on every toggle (in-client engine).
  $effect(() => {
    if (!options || !picked) return;
    const ids = [...picked];
    const n = ++seq;
    fetchChoice({ ...bodyOf(draft, ids), jokers: undefined }).then(
      (c) => {
        if (n === seq) ({ supply, reason } = { supply: c.supply, reason: null });
      },
      (e) => {
        if (n === seq) ({ supply, reason } = { supply: null, reason: errorText(e) });
      },
    );
  });

  function pick(ids: string[]) {
    if (busy) return;
    stale = true;
    onpick(ids);
  }

  /** «¡A jugar!»: the supply notice first if it has something to say (plan 65), else the game. */
  async function start() {
    if (!ready || busy || checking) return;
    const choice = choiceOf(draft, selected);
    checking = true;
    const outlook = await fetchOutlook(choice).catch(() => null); // informational: never blocks a game
    checking = false;
    if (outlook && worthShowing(outlook)) notice = { outlook, choice };
    else onstart(choice, []);
  }

  function play() {
    if (!notice) return;
    const { outlook, choice } = notice;
    notice = null;
    onstart(choice, outlook.runningOut);
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
        else if (a.type === "confirm") start();
        else if (a.type === "back") onback();
        else return false;
        return true;
      },
    }),
  );
</script>

<section class="bundles-screen" class:reporting={!!supply && !supply.ok} bind:this={section}>
  {#if greeting}
    <h1 class="title hello">{t("screen.player.helloOpen")}<span class="name">{greeting}</span>{t("screen.player.helloClose")}</h1>
  {:else}
    <h1 class="title">{t("bundles.titleOpen")}<span class="name">{player}</span>{t("bundles.titleClose")}</h1>

    {#if options}
      <BundleSelector bundles={options.bundles} {selected} {busy} {keyOf} large onchange={pick} />

      <div class="actions">
        <button class="secondary" onclick={onback} disabled={busy} data-focus-id="back"><Icon name="back" /> {t("action.back")} <Prompt action="back" /></button>
        <button class="candy" onclick={start} disabled={busy || !ready} data-focus-default data-focus-id="start"><Icon name="rocket" /> {t("choice.start")} <Prompt action="confirm" off={!ready} /></button>
      </div>

      {#if shownRefusal?.supply}
        <SupplyReport supply={shownRefusal.supply} />
      {:else if shownRefusal}
        <p class="error">{errorText(shownRefusal)}</p>
      {:else if empty}
        <p class="error">{t("bundles.noQuestions")}</p>
      {:else if reason}
        <p class="error">{reason}</p>
      {:else if supply}
        <SupplyReport {supply} />
      {/if}
    {/if}

    {#if error}<p class="error">{error}</p>{/if}
  {/if}
</section>

{#if notice}
  <SupplyNotice outlook={notice.outlook} onplay={play} onback={() => (notice = null)} />
{/if}

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
  .bundles-screen.reporting {
    gap: calc(1 * var(--u));
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
  .hello {
    font-size: calc(7 * var(--u));
    animation: hello 0.8s var(--spring) backwards;
  }
  @keyframes hello {
    from {
      opacity: 0;
      transform: scale(0.5) rotate(-4deg);
    }
  }
  .error {
    margin: 0;
    color: var(--coral);
    font-size: calc(1.1 * var(--u));
  }
</style>
