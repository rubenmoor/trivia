<script module lang="ts">
  /** One key per bundle (plan 29): the first letter of its name, accents stripped, not taken by an
   * earlier bundle nor in `reserved`, else the name's next letter; "" if none is left. */
  export function bundleKeys(names: string[], reserved: string[]): string[] {
    const taken = new Set(reserved.map((k) => k.toLowerCase()));
    return names.map((name) => {
      const letters = [...name.normalize("NFD").replace(/\p{M}/gu, "").toLowerCase()].filter((c) => /\p{L}/u.test(c));
      const key = letters.find((c) => !taken.has(c)) ?? "";
      if (key) taken.add(key);
      return key;
    });
  }
</script>

<script lang="ts">
  // The Choice screen (plans/04-ui-tv-display.md, "Choice"; plan 29, AG-7, BN-6): «¿Cómo juega …?»,
  // between Player and Level. Age group (1–4), exactly one base bundle and the other bundles (letter
  // keys) of the new game's language; preset: the player's newest game, else the defaults.
  import { onMount } from "svelte";
  import { DEFAULT_AGE_GROUP, fetchChoice, fetchChoiceOptions, GameError, type ChoiceOptions } from "../lib/api";
  import { errorText } from "../lib/errors";
  import { t } from "../lib/i18n";
  import { pushScope, type Keys } from "../lib/input.svelte";
  import type { Supply } from "../lib/types";
  import Prompt from "./Prompt.svelte";
  import SupplyReport from "./SupplyReport.svelte";

  type Bundle = ChoiceOptions["bundles"][number];

  let {
    player,
    busy,
    greeting,
    refused,
    onstart,
    onback,
  }: {
    player: string;
    busy: boolean;
    /** The name while «¡Hola, …!» plays into the transition, else null. */
    greeting: string | null;
    /** Why the last `new` was refused (supply, `base_bundle_count`, `bundle_not_offered`), or null. */
    refused: GameError | null;
    onstart: (choice: { age_group: string; bundles: string[] }) => void;
    onback: () => void;
  } = $props();

  let options = $state<ChoiceOptions | null>(null);
  let group = $state(DEFAULT_AGE_GROUP);
  let bundles = $state<string[]>([]);
  /** The supply of the current choice; null while unknown or refused. */
  let supply = $state<Supply | null>(null);
  /** Why the engine refuses the current choice (zero or two base bundles). */
  let reason = $state<string | null>(null);
  /** Groups that can't fill a game with the current bundles. */
  let short = $state<Record<string, boolean>>({});
  let error = $state<string | null>(null);
  /** The choice changed since `refused` came. */
  let stale = $state(false);
  let section = $state<HTMLElement>();
  let seq = 0;

  onMount(async () => {
    try {
      const [opts, preset] = await Promise.all([fetchChoiceOptions(), fetchChoice({ player })]);
      options = opts;
      group = preset.choice.age_group ?? DEFAULT_AGE_GROUP;
      bundles = preset.choice.bundles;
      await check();
    } catch (e) {
      error = errorText(e);
    }
  });

  $effect(() => {
    void refused;
    stale = false;
  });

  /** Supply of the current choice and of each group with the current bundles (in-client engine). */
  async function check() {
    if (!options) return;
    const n = ++seq;
    const wanted = [...bundles];
    const [mine, ...each] = await Promise.allSettled([
      fetchChoice({ age_group: group, bundles: wanted }),
      ...options.groups.map((g) => fetchChoice({ age_group: g.id, bundles: wanted })),
    ]);
    if (n !== seq) return;
    supply = mine.status === "fulfilled" ? mine.value.supply : null;
    reason = mine.status === "rejected" ? errorText(mine.reason) : null;
    short = Object.fromEntries(options.groups.map((g, i) => [g.id, each[i].status === "fulfilled" && !each[i].value.supply.ok]));
  }

  function changed() {
    stale = true;
    check();
  }

  function pickGroup(id: string) {
    if (busy) return;
    group = id;
    changed();
  }

  /** A base bundle replaces the other base bundle; another bundle toggles. */
  function toggle(b: Bundle) {
    if (busy || !options) return;
    const on = (x: Bundle) => (b.base && x.base ? x.id === b.id : x.id === b.id ? !bundles.includes(x.id) : bundles.includes(x.id));
    bundles = options.bundles.filter(on).map((x) => x.id);
    changed();
  }

  const ready = $derived(!!options && !!supply?.ok && !reason);
  const shownRefusal = $derived(refused && !stale ? refused : null);

  function start() {
    if (ready && !busy) onstart({ age_group: group, bundles: [...bundles] });
  }

  const base = $derived(options?.bundles.filter((b) => b.base) ?? []);
  const others = $derived(options?.bundles.filter((b) => !b.base) ?? []);
  const RESERVED = [t("flag.key"), t("screen.start.newKey"), t("screen.question.replayKey"), t("joker.hint.key")];
  const letters = $derived(bundleKeys(options?.bundles.map((b) => b.name) ?? [], RESERVED));
  const keyOf = (b: Bundle) => letters[options?.bundles.indexOf(b) ?? -1] ?? "";
  const keys = $derived<Keys>(Object.fromEntries(letters.filter(Boolean).map((k) => [k, { type: "letter", key: k }])));

  function ages([lo, hi]: readonly [number, number | null]) {
    return hi === null ? t("choice.agesFrom", { lo }) : t("choice.ages", { lo, hi });
  }

  // 1–4 pick a group, a bundle's letter selects or toggles it, Enter starts, Backspace goes back; Esc falls through to the overlay.
  $effect(() =>
    pushScope({
      name: "choice",
      root: () => section,
      get keys() {
        return keys;
      },
      handle: (a) => {
        if (a.type === "pick" && options && a.n <= options.groups.length) pickGroup(options.groups[a.n - 1].id);
        else if (a.type === "letter" && options?.bundles.some((b) => keyOf(b) === a.key))
          toggle(options.bundles.find((b) => keyOf(b) === a.key)!);
        else if (a.type === "confirm") start();
        else if (a.type === "back") onback();
        else return false;
        return true;
      },
    }),
  );
</script>

<section class="choice" bind:this={section}>
  {#if greeting}
    <h1 class="title hello">{t("screen.player.helloOpen")}<span class="name">{greeting}</span>{t("screen.player.helloClose")}</h1>
  {:else}
    <h1 class="title">{t("choice.titleOpen")}<span class="name">{player}</span>{t("choice.titleClose")}</h1>

    {#if options}
      <p class="label heading" style:--i={0}>{t("choice.groups")}</p>
      <div class="row" role="radiogroup">
        {#each options.groups as g, i (g.id)}
          <button
            class="tile glass"
            class:on={g.id === group}
            class:short={short[g.id]}
            style:--i={i + 1}
            role="radio"
            aria-checked={g.id === group}
            onclick={() => pickGroup(g.id)}
            disabled={busy}
            data-focus-id="group-{g.id}"
          >
            <Prompt action={{ type: "pick", n: i + 1 }} hold />
            <span class="name-text">{g.name}</span>
            <span class="label">{ages(g.ages)}</span>
            {#if short[g.id]}<span class="label warn">{t("choice.short")}</span>{/if}
          </button>
        {/each}
      </div>

      <p class="label heading" style:--i={5}>{t("choice.bundles")}</p>
      <div class="row" role="radiogroup">
        {#each base as b, i (b.id)}
          {@render bundle(b, "radio", 6 + i)}
        {/each}
      </div>
      {#if others.length}
        <div class="row">
          {#each others as b, i (b.id)}
            {@render bundle(b, "switch", 6 + base.length + i)}
          {/each}
        </div>
      {/if}

      <div class="row actions">
        <button class="secondary" onclick={onback} disabled={busy} data-focus-id="back">{t("action.back")} <Prompt action="back" /></button>
        <button class="candy" onclick={start} disabled={busy || !ready} data-focus-default data-focus-id="start">{t("choice.start")} <Prompt action="confirm" off={!ready} /></button>
      </div>

      {#if shownRefusal?.supply}
        <SupplyReport supply={shownRefusal.supply} />
      {:else if shownRefusal}
        <p class="error">{errorText(shownRefusal)}</p>
      {:else if reason}
        <p class="error">{reason}</p>
      {:else if supply}
        <SupplyReport {supply} />
      {/if}
    {/if}

    {#if error}<p class="error">{error}</p>{/if}
  {/if}
</section>

{#snippet bundle(b: Bundle, role: "radio" | "switch", i: number)}
  {@const on = bundles.includes(b.id)}
  {@const key = keyOf(b)}
  <button
    class="tile bundle glass"
    class:on
    style:--i={i}
    {role}
    aria-checked={on}
    onclick={() => toggle(b)}
    disabled={busy}
    data-focus-id="bundle-{b.id}"
  >
    {#if key}<Prompt action={{ type: "letter", key }} hold />{/if}
    <span class="name-text">{b.name}</span>
    {#if role === "switch"}<span class="switch label">{t(on ? "choice.on" : "choice.off")}</span>{/if}
    <span class="label description">{b.description}</span>
  </button>
{/snippet}

<style>
  .choice {
    position: absolute;
    inset: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: calc(1.2 * var(--u));
    padding: var(--safe-y) var(--safe-x);
    text-align: center;
  }
  .title {
    animation: arrive 0.6s var(--spring) backwards;
  }
  .name {
    color: var(--amber);
  }
  .heading {
    margin: calc(0.6 * var(--u)) 0 0;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    animation: arrive 0.5s calc(0.15s + var(--i) * 0.05s) var(--spring) backwards;
  }
  .row {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: calc(1.2 * var(--u));
    max-width: calc(110 * var(--u));
  }
  .tile {
    display: grid;
    grid-template-columns: auto 1fr;
    column-gap: calc(1 * var(--u));
    align-items: center;
    min-width: calc(20 * var(--u));
    padding: calc(1 * var(--u)) calc(1.6 * var(--u));
    border-color: var(--slate-600);
    text-align: left;
    transition:
      transform 0.2s var(--spring),
      border-color 0.2s,
      opacity 0.2s;
    animation: arrive 0.5s calc(0.15s + var(--i) * 0.05s) var(--spring) backwards;
  }
  .tile > :global(kbd) {
    grid-row: span 3;
  }
  .tile > :not(:global(kbd)) {
    grid-column: 2;
  }
  .tile:hover:not(:disabled) {
    transform: translateY(calc(-0.3 * var(--u)));
  }
  .tile.on {
    border-color: var(--sky);
    background: rgba(76, 201, 240, 0.16);
    transform: translateY(calc(-0.3 * var(--u)));
  }
  .tile.short:not(.on) {
    opacity: 0.55;
  }
  .bundle {
    max-width: calc(34 * var(--u));
  }
  .bundle:not(.on) .name-text {
    color: var(--slate-400);
  }
  .name-text {
    font-family: var(--font-display);
    font-size: calc(2 * var(--u));
    font-weight: 800;
    line-height: 1.1;
  }
  .switch {
    color: var(--sky);
  }
  .bundle:not(.on) .switch {
    color: var(--slate-400);
  }
  .warn {
    color: var(--amber);
  }
  .actions {
    margin-top: calc(1 * var(--u));
    align-items: center;
    animation: arrive 0.5s 0.5s var(--spring) backwards;
  }
  .error {
    margin: 0;
    color: var(--coral);
    font-size: calc(1.1 * var(--u));
  }
  .hello {
    font-size: calc(7 * var(--u));
    animation: hello 0.8s var(--spring) backwards;
  }
  @keyframes arrive {
    from {
      opacity: 0;
      transform: translateY(calc(2 * var(--u))) scale(0.94);
    }
  }
  @keyframes hello {
    from {
      opacity: 0;
      transform: scale(0.5) rotate(-4deg);
    }
  }
</style>
