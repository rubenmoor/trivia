<script lang="ts">
  // The Choice screen, the age screen (plans/04-ui-tv-display.md, "Choice"; plan 29, AG-7, BN-6; decision 314): «¿Cómo juega …?»,
  // after the Mode screen (and the Join screen in a multiplayer mode). Gamemaster mode: the configure game screen (MD-11, D-88):
  // difficulty, levels, cards, video, audio, answers (D-105), jokers; the other modes: the age group (1–4), one per seat in rr-competitive,
  // and «Personalizar partida» (joker counts). «Seguir» goes to the Bundles screen, which holds the supply report and starts the game (decision 264).
  // Preset: the player's newest game (every field but the bundles and the mode), else the defaults; a returning draft wins. ↑/↓ move between lines, ←/→ change a value.
  import { onMount, untrack } from "svelte";
  import {
    CARDS_MAX, DEFAULT_AGE_GROUP, fetchChoice, fetchChoiceOptions, LEVELS_MAX, type ChoiceOptions,
  } from "../../lib/api.ts";
  import { errorText } from "../../lib/errors.ts";
  import { candidates, show } from "../../lib/focus.ts";
  import { t } from "../../lib/i18n.ts";
  import { pushScope, type Keys } from "../../lib/input.svelte.ts";
  import type { GameMode, JokerName } from "../../lib/types.ts";
  import Customize from "../Customize.svelte";
  import { presetOf, stepPreset, stepUses, TOKENS } from "../jokers.ts";
  import { clamp, spanOf, stepDifficulty } from "../difficulty.ts";
  import { defaultDraft, type ChoiceDraft } from "../choiceDraft.ts";
  import { seatColor, type SeatDraft } from "../seats.ts";
  import Icon, { type IconName } from "../Icon.svelte";
  import Prompt from "../Prompt.svelte";

  let {
    mode,
    player,
    busy,
    draft,
    seats,
    onseats,
    onnext,
    onback,
  }: {
    /** The Mode screen's pick. */
    mode: GameMode;
    player: string;
    busy: boolean;
    /** The picks kept in Game.svelte from an earlier visit (Back from Join or Bundles), else null: the preset applies. */
    draft: ChoiceDraft | null;
    /** The Join screen's seats (multiplayer modes); rr-competitive sets each seat's group here. */
    seats: SeatDraft[];
    onseats: (seats: SeatDraft[]) => void;
    onnext: (draft: ChoiceDraft) => void;
    onback: () => void;
  } = $props();

  const start = untrack(() => draft) ?? defaultDraft();
  let options = $state<ChoiceOptions | null>(null);
  let group = $state(start.group);
  /** «Solo o en grupo»'s joker counts; a difference from the standard set makes the game customized. */
  let jokers = $state(start.jokers);
  let customizing = $state(false);
  /** Gamemaster mode's fields (D-88); `custom`: the difficulty instead of the group. */
  let custom = $state(start.custom);
  let difficulty = $state(start.difficulty);
  let levels = $state(start.levels);
  let cards = $state(start.cards);
  let video = $state(start.video);
  let audio = $state(start.audio);
  let answers = $state(start.answers);
  let budget = $state(start.budget);
  let error = $state<string | null>(null);
  let section = $state<HTMLElement>();

  onMount(async () => {
    try {
      if (draft) {
        options = await fetchChoiceOptions();
        return;
      }
      const [opts, preset] = await Promise.all([fetchChoiceOptions(), fetchChoice({ player })]);
      options = opts;
      const c = preset.choice;
      group = c.age_group ?? DEFAULT_AGE_GROUP;
      custom = c.difficulty !== null;
      difficulty = c.difficulty ?? spanOf(opts.groups, group);
      ({ levels, cards, video, audio, answers } = c);
      budget = { ...c.jokers };
    } catch (e) {
      error = errorText(e);
    }
  });

  function pickGroup(id: string) {
    if (busy) return;
    group = id;
    custom = false;
  }

  /** A joker's count by one: 0–9, then ∞, clamped (decision 105). */
  function stepJoker(name: JokerName, by: number) {
    budget = { ...budget, [name]: stepUses(budget[name], by) };
  }

  /** rr-competitive: seat `i`'s age group by one, wrapping. */
  function stepSeat(i: number, by: number) {
    if (busy || !options) return;
    const ids = options.groups.map((g) => g.id);
    const at = Math.max(0, ids.indexOf(seats[i].group));
    onseats(seats.map((s, j) => (j === i ? { ...s, group: ids[(at + by + ids.length) % ids.length] } : s)));
  }

  /** ←/→ or −/+ on a configure line (`data-step`). */
  function step(id: string, by: number) {
    if (busy || !options) return;
    if (id.startsWith("seat-group-")) return stepSeat(Number(id.slice(11)), by);
    const pick = stepDifficulty(options.groups, { group, custom, difficulty }, id, by);
    if (pick) ({ group, custom, difficulty } = pick);
    else if (id === "levels") levels = clamp(levels + by, 1, LEVELS_MAX);
    else if (id === "cards") cards = clamp(cards + by, 0, CARDS_MAX);
    else if (id === "video") video = !video;
    else if (id === "audio") audio = !audio;
    else if (id === "answers") answers = !answers;
    else if (id === "preset") return void (budget = stepPreset(budget, by));
    else if (id.startsWith("joker-")) return stepJoker(id.slice(6) as JokerName, by);
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

  /** «Seguir»: the Join screen (a multiplayer mode) or the Bundles screen, with these picks kept. */
  function next() {
    if (busy || !options) return;
    onnext({ mode, group, jokers, custom, difficulty, levels, cards, video, audio, answers, budget });
  }

  const session = $derived(mode !== "solo" && mode !== "gamemaster");
  /** «Personalizar partida»: every mode but gamemaster and timed (no jokers). */
  const jokerMode = $derived(mode !== "gamemaster" && mode !== "timed");
  const CUSTOMIZE_KEY = t("customize.openKey").toLowerCase();
  const GROUP_ICONS: Record<string, IconName> = { kids: "balloon", young_teens: "skateboard", young_adults: "headphones", adults: "mug" };
  const keys = $derived<Keys>(jokerMode ? { [CUSTOMIZE_KEY]: { type: "letter", key: CUSTOMIZE_KEY } } : {});
  const customized = $derived(presetOf(jokers) !== "standard");
  function ages([lo, hi]: readonly [number, number | null]) {
    return hi === null ? t("choice.agesFrom", { lo }) : t("choice.ages", { lo, hi });
  }

  // 1–4 pick a group, the customize letter opens the dialog (solo); ↑/↓ lines, ←/→ a configure value; Enter starts (on a switch: toggles),
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
        else if (a.type === "letter" && jokerMode && a.key === CUSTOMIZE_KEY) customizing = !busy;
        else if (a.type === "pick" && options && a.n <= options.groups.length) pickGroup(options.groups[a.n - 1].id);
        else if (a.type === "confirm") next();
        else if (a.type === "back") onback();
        else return false;
        return true;
      },
    }),
  );
</script>

<section class="choice" bind:this={section}>
  <h1 class="title">
    {#if session}{t("choice.titleMany")}{:else}{t("choice.titleOpen")}<span class="name">{player}</span>{t("choice.titleClose")}{/if}
  </h1>

  {#if options}
    {#if mode === "gamemaster"}
      {@const g = options.groups.find((x) => x.id === group)}
      {@const span = custom ? difficulty : spanOf(options.groups, group)}
      <div class="config">
        <div class="lines">
          <p class="label pick-heading">{t("configure.game")}</p>
          {@render stepper("difficulty", t("configure.difficulty"), custom ? t("configure.custom") : (g?.name ?? group),
            custom ? "" : g ? ages(g.ages) : "")}
          {@render stepper("start", t("configure.start"), String(span.start), "", false, !custom)}
          {@render stepper("end", t("configure.end"), String(span.end), "", false, !custom)}
          {@render stepper("levels", t("configure.levels"), String(levels))}
          {@render stepper("cards", t("configure.cards"), String(cards), cards ? "" : t("configure.noCards"))}
          {@render toggle("video", t("configure.video"), video, "film")}
          {@render toggle("audio", t("configure.audio"), audio, "speaker")}
          {@render toggle("answers", t("configure.answers"), answers, "lock")}
        </div>
        <div class="lines">
          <p class="label pick-heading">{t("configure.jokers")}</p>
          {@render stepper("preset", t("configure.preset"), t(`configure.presets.${presetOf(budget)}`))}
          {#each TOKENS as token (token.name)}
            {@render stepper(`joker-${token.name}`, token.label, String(budget[token.name] ?? "∞"), "", false, false, token.icon)}
          {/each}
        </div>
      </div>
    {:else}
      <p class="label pick-heading">{t("choice.groups")}</p>
      {#if mode === "rr-competitive"}
        <div class="seat-groups" data-nav-scroll>
          {#each seats as s, i (i)}
            {@const g = options.groups.find((x) => x.id === s.group)}
            {@render stepper(`seat-group-${i}`, s.name ?? String(i + 1), g?.name ?? s.group, g ? ages(g.ages) : "", false, false, undefined, seatColor(i))}
          {/each}
        </div>
      {:else}
      <div class="pick-row" role="radiogroup" data-line>
        {#each options.groups as g, i (g.id)}
          <button
            class="pick-tile glass"
            class:on={g.id === group}
            style:--i={i + 1}
            role="radio"
            aria-checked={g.id === group}
            onclick={() => pickGroup(g.id)}
            disabled={busy}
            data-focus-id="group-{g.id}"
          >
            <Prompt action={{ type: "pick", n: i + 1 }} hold />
            <span class="pick-name">{#if GROUP_ICONS[g.id]}<Icon name={GROUP_ICONS[g.id]} />{/if} {g.name}</span>
            <span class="label">{ages(g.ages)}</span>
          </button>
        {/each}
      </div>
      {/if}
      {#if jokerMode}
      <div class="row" data-line>
        <button class="secondary customize" onclick={() => (customizing = true)} disabled={busy} data-focus-id="customize">
          <Icon name="sliders" /> {t("customize.open")} <Prompt action={{ type: "letter", key: CUSTOMIZE_KEY }} />
        </button>
        <span class="label" class:warn={customized}>{t(customized ? "customize.custom" : "customize.standard")}</span>
      </div>
      {/if}
    {/if}

    <div class="row actions" data-line>
      <button class="secondary" onclick={onback} disabled={busy} data-focus-id="back"><Icon name="back" /> {t("action.back")} <Prompt action="back" /></button>
      <button class="candy" onclick={next} disabled={busy || !options} data-focus-default data-focus-id="next"><Icon name="next" /> {t("action.next")} <Prompt action="confirm" /></button>
    </div>
  {/if}

  {#if error}<p class="error">{error}</p>{/if}
</section>

{#if customizing}
  <Customize {jokers} onchange={(j) => (jokers = j)} onclose={() => (customizing = false)} />
{/if}

<!-- `fixed`: read-only, out of the focus ring and ↑/↓ -->
{#snippet stepper(id: string, label: string, value: string, note = "", warn = false, fixed = false, icon?: IconName, color?: string)}
  <!-- svelte-ignore a11y_no_noninteractive_tabindex -->
  <div class="line glass" class:fixed data-line data-step={fixed ? undefined : id} data-focusable={!fixed || undefined}
    data-focus-id="config-{id}" tabindex={fixed ? undefined : 0} role="group" aria-label={label} style:--seat={color}>
    <span class="label line-name" class:seat={color}>{#if icon}<Icon name={icon} />{/if} {label}</span>
    <button class="step" onclick={() => step(id, -1)} disabled={busy || fixed} tabindex="-1" aria-label={t("overlay.less")}>−</button>
    <span class="value">{value}{#if note}<span class="label note" class:warn>{note}</span>{/if}</span>
    <button class="step" onclick={() => step(id, 1)} disabled={busy || fixed} tabindex="-1" aria-label={t("overlay.more")}>+</button>
  </div>
{/snippet}

{#snippet toggle(id: string, label: string, on: boolean, icon: IconName)}
  <button class="line glass" class:on data-line data-step={id} data-focus-id="config-{id}" role="switch" aria-checked={on} onclick={() => step(id, 1)} disabled={busy}>
    <span class="label line-name"><Icon name={icon} /> {label}</span>
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
  .title {
    animation: arrive 0.6s var(--spring) backwards;
  }
  .name {
    color: var(--amber);
  }
  .row {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: calc(1.2 * var(--u));
    max-width: calc(110 * var(--u));
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
  .lines .pick-heading {
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
  .line-name.seat {
    color: var(--seat);
  }
  .seat-groups {
    display: flex;
    flex-direction: column;
    gap: calc(0.5 * var(--u));
    width: calc(36 * var(--u));
    max-height: calc(36 * var(--u));
    overflow-y: auto;
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
  .line.fixed {
    border-color: var(--slate-600);
  }
  .line.fixed .value {
    color: var(--slate-400);
  }
  .line.fixed .step {
    visibility: hidden;
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
</style>
