<script module lang="ts">
  /** One key per bundle (plan 29): the first letter of its name (after a «Regional:»-style prefix), accents
   * stripped, not taken by an earlier bundle nor in `reserved`, else the name's next letter; "" if none is left. */
  function bundleKeys(names: string[], reserved: string[]): string[] {
    const taken = new Set(reserved.map((k) => k.toLowerCase()));
    return names.map((name) => {
      const ordered = name.includes(":") ? name.slice(name.lastIndexOf(":") + 1) + name : name;
      const letters = [...ordered.normalize("NFD").replace(/\p{M}/gu, "").toLowerCase()].filter((c) => /\p{L}/u.test(c));
      const key = letters.find((c) => !taken.has(c)) ?? "";
      if (key) taken.add(key);
      return key;
    });
  }
</script>

<script lang="ts">
  // The Choice screen (plans/04-ui-tv-display.md, "Choice"; plan 29, AG-7, BN-6): «¿Cómo juega …?»,
  // between Player and Level. Mode row (MD-7); gamemaster mode: the configure game screen (MD-11, D-88):
  // difficulty, bundles (letter keys), levels, cards, video, audio, jokers; «Solo o en grupo»: age group (1–4),
  // the language's default bundles and «Personalizar partida» (joker counts). Preset: `?mode=`, the
  // player's newest game (every field), else the defaults. ↑/↓ move between lines, ←/→ change a value.
  import { onMount } from "svelte";
  import {
    BUILT_MODES, CARDS_MAX, DEFAULT_AGE_GROUP, DIFFICULTY_MAX, fetchChoice, fetchChoiceOptions, fetchOutlook, fetchPlayerMode,
    LEVELS_MAX, STANDARD_JOKERS, type ChoiceBody, type ChoiceOptions, type Outlook,
  } from "../../lib/api.ts";
  import { GameError } from "../../lib/http.ts";
  import { errorText } from "../../lib/errors.ts";
  import { candidates, show } from "../../lib/focus.ts";
  import { t } from "../../lib/i18n.ts";
  import { pushScope, type Keys } from "../../lib/input.svelte.ts";
  import type { Difficulty, GameMode, JokerBudget, JokerName, Supply } from "../../lib/types.ts";
  import BundleSelector, { toggled, type Bundle } from "../BundleSelector.svelte";
  import Customize from "../Customize.svelte";
  import { presetOf, stepPreset, TOKENS } from "../jokers.ts";
  import { clamp, spanOf, stepDifficulty } from "../difficulty.ts";
  import { DEFAULT_LEVELS } from "../levels.ts";
  import Prompt from "../Prompt.svelte";
  import SupplyNotice, { worthShowing } from "../SupplyNotice.svelte";
  import SupplyReport from "../SupplyReport.svelte";

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
    /** `exhausted`: the subcategories the supply notice showed (plan 65). */
    onstart: (choice: ChoiceBody & { mode: GameMode }, exhausted: string[]) => void;
    onback: () => void;
  } = $props();

  let options = $state<ChoiceOptions | null>(null);
  let group = $state(DEFAULT_AGE_GROUP);
  let bundles = $state<string[]>([]);
  let mode = $state<GameMode>("gamemaster");
  /** «Solo o en grupo»'s joker counts; a difference from the standard set makes the game customized. */
  let jokers = $state<JokerBudget>({ ...STANDARD_JOKERS });
  let customizing = $state(false);
  /** Gamemaster mode's fields (D-88); `custom`: the difficulty instead of the group. */
  let custom = $state(false);
  let difficulty = $state<Difficulty>({ start: 1, end: DIFFICULTY_MAX });
  let levels = $state(DEFAULT_LEVELS);
  let cards = $state(CARDS_MAX);
  let video = $state(true);
  let audio = $state(true);
  let budget = $state<JokerBudget>({ ...STANDARD_JOKERS });
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
  /** The supply notice before level 1 (decision 31), or null; `checking` while it's computed. */
  let notice = $state<{ outlook: Outlook; choice: ChoiceBody & { mode: GameMode } } | null>(null);
  let checking = false;
  let seq = 0;

  onMount(async () => {
    try {
      const [opts, preset, last] = await Promise.all([fetchChoiceOptions(), fetchChoice({ player }), fetchPlayerMode(player)]);
      options = opts;
      const launch = new URLSearchParams(location.search).get("mode") as GameMode | null;
      mode = launch && BUILT_MODES.includes(launch) ? launch : last;
      const c = preset.choice;
      group = c.age_group ?? DEFAULT_AGE_GROUP;
      custom = c.difficulty !== null;
      difficulty = c.difficulty ?? spanOf(opts.groups, group);
      bundles = c.bundles;
      ({ levels, cards, video, audio } = c);
      budget = { ...c.jokers };
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
    const wanted = mode === "gamemaster" ? { ...config(), jokers: undefined } : { age_group: group, bundles: active() };
    const [mine, ...each] = await Promise.allSettled([
      fetchChoice(wanted),
      ...options.groups.map((g) => fetchChoice({ ...wanted, age_group: g.id, difficulty: undefined })),
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

  /** «Solo o en grupo» plays the language's default bundles (decision 38): the first base bundle plus every other one. */
  function active(): string[] {
    if (mode === "gamemaster" || !options) return [...bundles];
    const base = options.bundles.find((b) => b.base);
    return options.bundles.filter((b) => b === base || !b.base).map((b) => b.id);
  }

  function pickMode(m: GameMode) {
    if (busy || m === mode) return;
    mode = m;
    changed();
  }

  function pickGroup(id: string) {
    if (busy) return;
    group = id;
    custom = false;
    changed();
  }

  function pickBundles(ids: string[]) {
    if (busy) return;
    bundles = ids;
    changed();
  }

  /** Gamemaster mode's whole configuration, every field (D-88). */
  function config(): ChoiceBody {
    return {
      ...(custom ? { difficulty: { ...difficulty } } : { age_group: group }),
      bundles: [...bundles], levels, cards, video, audio, jokers: { ...budget },
    };
  }

  const JOKER_MAX = 99;

  /** A joker's count by one: 0–99, then ∞, wrapping both ways. */
  function stepJoker(name: JokerName, by: number) {
    const now = budget[name] ?? JOKER_MAX + 1;
    const next = (now + by + JOKER_MAX + 2) % (JOKER_MAX + 2);
    budget = { ...budget, [name]: next > JOKER_MAX ? null : next };
  }

  /** ←/→ or −/+ on a configure line (`data-step`). */
  function step(id: string, by: number) {
    if (busy || !options) return;
    const pick = stepDifficulty(options.groups, { group, custom, difficulty }, id, by);
    if (pick) ({ group, custom, difficulty } = pick);
    else if (id === "levels") levels = clamp(levels + by, 1, LEVELS_MAX);
    else if (id === "cards") cards = clamp(cards + by, 0, CARDS_MAX);
    else if (id === "video") video = !video;
    else if (id === "audio") audio = !audio;
    else if (id === "preset") return void (budget = stepPreset(budget, by));
    else if (id.startsWith("joker-")) return stepJoker(id.slice(6) as JokerName, by);
    changed();
  }

  /** ↑/↓: the previous or next line (`data-line`), its control nearest across; false outside a line. */
  function moveLine(dir: "up" | "down"): boolean {
    const el = document.activeElement;
    if (!section || !(el instanceof HTMLElement)) return false;
    const all = candidates(section);
    const inLine = (l: HTMLElement) => all.filter((c) => l.contains(c));
    const lines = [...section.querySelectorAll<HTMLElement>("[data-line]")].filter((l) => inLine(l).length);
    const at = lines.findIndex((l) => l.contains(el));
    if (at < 0) return false;
    const next = lines[at + (dir === "down" ? 1 : -1)];
    if (!next) {
      show(el);
      return true;
    }
    const x = (r: DOMRect) => r.left + r.width / 2;
    const from = x(el.getBoundingClientRect());
    const list = inLine(next);
    const near = list.reduce((m, c) => (Math.abs(x(c.getBoundingClientRect()) - from) < Math.abs(x(m.getBoundingClientRect()) - from) ? c : m));
    show(near, "choice", section);
    return true;
  }

  const ready = $derived(!!options && !!supply?.ok && !reason);
  const shownRefusal = $derived(refused && !stale ? refused : null);
  /** A supply report is shown: tighter gaps, so a long one fits at 720p (plan 46). */
  const reporting = $derived(!!shownRefusal?.supply || (!shownRefusal && !reason && supply?.ok === false));

  /** «¡A jugar!»: the supply notice first if it has something to say (plan 65), else the game. */
  async function start() {
    if (!ready || busy || checking) return;
    const choice: ChoiceBody & { mode: GameMode } = mode === "gamemaster"
      ? { mode, ...config() }
      : { mode, age_group: group, bundles: active(), ...(customized ? { jokers: { ...jokers } } : {}) };
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
    onstart(choice, outlook.exhausted);
  }

  const MODE_ROW: { id: GameMode; name: string; about: string; key: string }[] = [
    { id: "gamemaster", name: t("mode.gamemaster"), about: t("mode.gamemasterAbout"), key: t("mode.gamemasterKey").toLowerCase() },
    { id: "solo", name: t("mode.solo"), about: t("mode.soloAbout"), key: t("mode.soloKey").toLowerCase() },
  ];
  const modes = MODE_ROW.filter((m) => BUILT_MODES.includes(m.id));
  const CUSTOMIZE_KEY = t("customize.openKey").toLowerCase();
  const RESERVED = [
    t("flag.key"), t("screen.start.newKey"), t("screen.question.replayKey"), t("joker.hint.key"), CUSTOMIZE_KEY, ...modes.map((m) => m.key),
  ];
  const letters = $derived(bundleKeys(options?.bundles.map((b) => b.name) ?? [], RESERVED));
  const keyOf = (b: Bundle) => letters[options?.bundles.indexOf(b) ?? -1] ?? "";
  const letter = (key: string) => [key, { type: "letter", key }] as const;
  const keys = $derived<Keys>(
    Object.fromEntries([
      ...modes.map((m) => letter(m.key)),
      ...(mode === "gamemaster" ? letters.filter(Boolean).map(letter) : [letter(CUSTOMIZE_KEY)]),
    ]),
  );
  const customized = $derived(presetOf(jokers) !== "standard");

  function ages([lo, hi]: readonly [number, number | null]) {
    return hi === null ? t("choice.agesFrom", { lo }) : t("choice.ages", { lo, hi });
  }

  // A mode's letter picks it, 1–4 pick a group, a bundle's letter selects or toggles it (gamemaster mode), the
  // customize letter opens the dialog (solo); ↑/↓ lines, ←/→ a configure value; Enter starts (on a switch: toggles),
  // Backspace goes back; Esc falls through to the overlay.
  $effect(() =>
    pushScope({
      name: "choice",
      root: () => section,
      pressable: (el) => !(el instanceof HTMLDivElement && el.dataset.step),
      get keys() {
        return keys;
      },
      handle: (a) => {
        const stepping = document.activeElement instanceof HTMLElement ? document.activeElement.dataset.step : undefined;
        if (a.type === "navigate" && (a.dir === "up" || a.dir === "down")) return moveLine(a.dir);
        if (a.type === "navigate" && stepping) step(stepping, a.dir === "right" ? 1 : -1);
        else if (a.type === "letter" && modes.some((m) => m.key === a.key)) pickMode(modes.find((m) => m.key === a.key)!.id);
        else if (a.type === "letter" && mode !== "gamemaster" && a.key === CUSTOMIZE_KEY) customizing = !busy;
        else if (a.type === "pick" && options && a.n <= options.groups.length) pickGroup(options.groups[a.n - 1].id);
        else if (a.type === "letter" && mode === "gamemaster" && options?.bundles.some((b) => keyOf(b) === a.key))
          pickBundles(toggled(options.bundles, bundles, options.bundles.find((b) => keyOf(b) === a.key)!));
        else if (a.type === "confirm") start();
        else if (a.type === "back") onback();
        else return false;
        return true;
      },
    }),
  );
</script>

<section class="choice" class:reporting bind:this={section}>
  {#if greeting}
    <h1 class="title hello">{t("screen.player.helloOpen")}<span class="name">{greeting}</span>{t("screen.player.helloClose")}</h1>
  {:else}
    <h1 class="title">{t("choice.titleOpen")}<span class="name">{player}</span>{t("choice.titleClose")}</h1>

    {#if options}
      {#if modes.length > 1}
        <p class="label heading" style:--i={0}>{t("mode.heading")}</p>
        <div class="row" role="radiogroup" data-line>
          {#each modes as m, i (m.id)}
            <button
              class="tile mode glass"
              class:on={m.id === mode}
              style:--i={i + 1}
              role="radio"
              aria-checked={m.id === mode}
              onclick={() => pickMode(m.id)}
              disabled={busy}
              data-focus-id="mode-{m.id}"
            >
              <Prompt action={{ type: "letter", key: m.key }} hold />
              <span class="name-text">{m.name}</span>
              <span class="label">{m.about}</span>
            </button>
          {/each}
        </div>
      {/if}

      {#if mode === "gamemaster"}
        {@const g = options.groups.find((x) => x.id === group)}
        <div class="config">
          <div class="lines">
            <p class="label heading">{t("configure.game")}</p>
            {@render stepper("difficulty", t("configure.difficulty"), custom ? t("configure.custom") : (g?.name ?? group),
              custom ? "" : g ? ages(g.ages) : "", !custom && short[group])}
            {#if custom}
              {@render stepper("start", t("configure.start"), String(difficulty.start))}
              {@render stepper("end", t("configure.end"), String(difficulty.end))}
            {/if}
            {@render stepper("levels", t("configure.levels"), String(levels))}
            {@render stepper("cards", t("configure.cards"), String(cards), cards ? "" : t("configure.noCards"))}
            {@render toggle("video", t("configure.video"), video)}
            {@render toggle("audio", t("configure.audio"), audio)}
          </div>
          <div class="lines">
            <p class="label heading">{t("configure.jokers")}</p>
            {@render stepper("preset", t("configure.preset"), t(`configure.presets.${presetOf(budget)}`))}
            {#each TOKENS as token (token.name)}
              {@render stepper(`joker-${token.name}`, token.label, String(budget[token.name] ?? "∞"))}
            {/each}
          </div>
        </div>
        <p class="label heading" style:--i={5}>{t("choice.bundles")}</p>
        <BundleSelector bundles={options.bundles} selected={bundles} {busy} {keyOf} first={6} onchange={pickBundles} />
      {:else}
        <p class="label heading" style:--i={0}>{t("choice.groups")}</p>
        <div class="row" role="radiogroup" data-line>
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
        <div class="row" data-line>
          <button class="secondary customize" onclick={() => (customizing = true)} disabled={busy} data-focus-id="customize">
            {t("customize.open")} <Prompt action={{ type: "letter", key: CUSTOMIZE_KEY }} />
          </button>
          <span class="label" class:warn={customized}>{t(customized ? "customize.custom" : "customize.standard")}</span>
        </div>
      {/if}

      <div class="row actions" data-line>
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

{#if notice}
  <SupplyNotice outlook={notice.outlook} onplay={play} onback={() => (notice = null)} />
{/if}

{#if customizing}
  <Customize {jokers} onchange={(j) => (jokers = j)} onclose={() => (customizing = false)} />
{/if}

{#snippet stepper(id: string, label: string, value: string, note = "", warn = false)}
  <!-- svelte-ignore a11y_no_noninteractive_tabindex -->
  <div class="line glass" data-line data-step={id} data-focusable data-focus-id="config-{id}" tabindex="0" role="group" aria-label={label}>
    <span class="label line-name">{label}</span>
    <button class="step" onclick={() => step(id, -1)} disabled={busy} tabindex="-1" aria-label={t("overlay.less")}>−</button>
    <span class="value">{value}{#if note}<span class="label note" class:warn>{note}</span>{/if}</span>
    <button class="step" onclick={() => step(id, 1)} disabled={busy} tabindex="-1" aria-label={t("overlay.more")}>+</button>
  </div>
{/snippet}

{#snippet toggle(id: string, label: string, on: boolean)}
  <button class="line glass" class:on data-line data-step={id} data-focus-id="config-{id}" role="switch" aria-checked={on} onclick={() => step(id, 1)} disabled={busy}>
    <span class="label line-name">{label}</span>
    <span class="value switch">{t(on ? "choice.on" : "choice.off")}</span>
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
  .choice.reporting {
    gap: calc(0.8 * var(--u));
  }
  .choice.reporting :global(.bundle .description) {
    display: none;
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
  .mode {
    min-width: calc(26 * var(--u));
  }
  .row:has(.customize) {
    align-items: center;
  }
  .config {
    display: flex;
    gap: calc(2.4 * var(--u));
    align-items: flex-start;
    animation: arrive 0.5s 0.2s var(--spring) backwards;
  }
  .lines {
    display: flex;
    flex-direction: column;
    gap: calc(0.5 * var(--u));
    width: calc(36 * var(--u));
  }
  .lines .heading {
    margin: 0;
    animation: none;
  }
  .line {
    display: grid;
    grid-template-columns: 1fr calc(2.4 * var(--u)) calc(14 * var(--u)) calc(2.4 * var(--u));
    align-items: center;
    gap: calc(0.8 * var(--u));
    padding: calc(0.4 * var(--u)) calc(1.2 * var(--u));
    border-color: var(--slate-600);
    font-size: calc(1.3 * var(--u));
    font-weight: 700;
    text-align: left;
    outline: none;
  }
  .line:focus,
  .line:global([data-nav]),
  .line:hover {
    border-color: var(--amber);
  }
  button.line {
    grid-template-columns: 1fr calc(14 * var(--u)) calc(2.4 * var(--u));
  }
  button.line .value {
    grid-column: 2;
  }
  .line-name {
    color: var(--slate-200);
  }
  .value {
    display: flex;
    flex-direction: column;
    align-items: center;
    font-variant-numeric: tabular-nums;
    line-height: 1.1;
  }
  .value .note {
    font-size: calc(0.9 * var(--u));
  }
  .line.on .switch {
    color: var(--sky);
  }
  .line:not(.on) .switch {
    color: var(--slate-400);
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
  .row .customize {
    padding: calc(0.5 * var(--u)) calc(1.2 * var(--u));
    font-size: calc(1.1 * var(--u));
  }
  .name-text {
    font-family: var(--font-display);
    font-size: calc(2 * var(--u));
    font-weight: 800;
    line-height: 1.1;
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
  @keyframes hello {
    from {
      opacity: 0;
      transform: scale(0.5) rotate(-4deg);
    }
  }
</style>
