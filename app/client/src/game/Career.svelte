<script lang="ts">
  // The badge page (plan 197, plans/04-ui-tv-display.md "Career"): one player's 39 career badges, earned in colour
  // with their date, open ones dimmed; the focused badge's text below; the career's on/off switch. A layer, as Credits.
  // Badges not shown yet are celebrated on it (decision 591): hidden in their slots, revealed one by one, then fanfare
  // and fireworks; confirm skips. `after`: the game's Badges screen after an end screen («Seguir», no switch).
  import { onDestroy } from "svelte";
  import { type CareerView, SCORE_MILESTONES, SUBJECTS, YEAR_GROUPS } from "../engine/career.ts";
  import { careerShown, fetchCareers, setCareer } from "../lib/api.ts";
  import { badgeText } from "../lib/badge-text.ts";
  import { formatScore } from "../lib/career-text.ts";
  import { revealStep, unshown } from "../lib/celebration.ts";
  import { errorText } from "../lib/errors.ts";
  import { lang, t } from "../lib/i18n.ts";
  import { focusControl, pushScope } from "../lib/input.svelte.ts";
  import { badgeNames, displayName } from "../lib/names.svelte.ts";
  import Fireworks from "./Fireworks.svelte";
  import Icon from "./Icon.svelte";
  import Prompt from "./Prompt.svelte";
  import RankBar from "./RankBar.svelte";
  import { sfx } from "./sound.svelte.ts";
  import { FADE_MS, reducedMotion } from "./timing.ts";

  let { name, onclose, after = false, busy: screenBusy = false }: { name: string; onclose: () => void; after?: boolean; busy?: boolean } = $props();

  /** Icons from the Steam art (decision 199), by badge id. */
  const icons = import.meta.glob<string>("../../../desktop/achievements/CAREER_*.svg", { eager: true, query: "?url", import: "default" });
  const icon = (id: string) => icons[`../../../desktop/achievements/${id}.svg`];

  const GRADES = ["ELEMENTARY", "MIDDLE", "HIGH"] as const;
  const up = (s: string) => s.toUpperCase();
  const groups: { title: () => string; rows: string[][] }[] = [
    { title: () => t("career.page.subjects"), rows: SUBJECTS.map((s) => GRADES.map((g) => `CAREER_${up(s)}_${g}`)) },
    { title: () => t("career.page.diplomas"), rows: [GRADES.map((g) => `CAREER_DIPLOMA_${g}`)] },
    { title: () => t("career.grade.college"), rows: [["CAREER_COLLEGE"]] },
    { title: () => t("career.page.years"), rows: [YEAR_GROUPS.map((g) => `CAREER_YEAR_${up(g)}`)] },
    { title: () => t("career.points"), rows: [SCORE_MILESTONES.slice(0, 5), SCORE_MILESTONES.slice(5)].map((r) => r.map((n) => `CAREER_SCORE_${n}`)) },
  ];
  const total = groups.reduce((n, g) => n + g.rows.reduce((m, r) => m + r.length, 0), 0);

  let view = $state<CareerView | null>(null);
  let error = $state<string | null>(null);
  let busy = $state(false);
  let focused = $state<string | null>(null);
  let panel = $state<HTMLDivElement>();
  let backButton = $state<HTMLButtonElement>();

  const load = (all: Record<string, CareerView>) => (view = all[name] ?? null);
  fetchCareers().then((all) => (load(all), celebrate()), (e: unknown) => (error = errorText(e)));

  // The celebration -------------------------------------------------------------------------
  /** Badges being celebrated, in live order; `revealed` of them out of hiding. */
  let fresh = $state<string[]>([]);
  let revealed = $state(0);
  /** Fanfare and fireworks played: the reveal is over. */
  let done = $state(false);
  let closing = false;
  const reduced = reducedMotion();
  const revealing = $derived(fresh.length > 0 && !done);
  const hidden = $derived(new Set(fresh.slice(revealed)));
  const landed = $derived(new Set(fresh.slice(0, revealed)));
  let timer: ReturnType<typeof setTimeout> | undefined;
  onDestroy(() => clearTimeout(timer));

  /** Gallery (`?gallery`): `window.__galleryReveal = n` freezes the reveal after n badges. */
  const freezeAt = () => (window as { __galleryReveal?: number }).__galleryReveal;

  /** Celebrate what isn't shown yet (page open, career turned on, after a game). */
  function celebrate() {
    clearTimeout(timer);
    fresh = unshown(view ?? undefined);
    revealed = 0;
    done = false;
    if (!fresh.length) return;
    const step = revealStep(fresh.length);
    const next = () => {
      if (revealed === freezeAt()) return;
      revealed++;
      focused = fresh[revealed - 1];
      sfx("stamp");
      if (revealed < fresh.length) timer = setTimeout(next, step);
      else timer = setTimeout(finish, step);
    };
    timer = setTimeout(next, FADE_MS + 200);
  }

  function finish() {
    clearTimeout(timer);
    if (done) return;
    revealed = fresh.length;
    focused = fresh.at(-1) ?? focused;
    done = true;
    sfx("fanfare");
  }

  /** Confirm: skip the reveal to its end, else leave; shown either way once the page closes. */
  function confirm() {
    if (revealing) finish();
    else close();
  }

  async function close() {
    if (closing) return;
    closing = true;
    clearTimeout(timer);
    if (fresh.length) await careerShown(name, fresh).then(load, (e: unknown) => console.error("career:shown", e));
    onclose();
  }

  const held = $derived(new Map((view?.badges ?? []).map((b) => [b.name, b.on])));
  const names = $derived(view ? badgeNames() : { subjects: {}, age_groups: {} });
  const text = (id: string) => badgeText(id, lang, names);
  const date = (iso: string) => new Intl.DateTimeFormat(lang, { dateStyle: "medium" }).format(new Date(`${iso.slice(0, 10)}T12:00:00`));
  const rowTitle = (id: string) => displayName("subject", SUBJECTS.find((s) => id.startsWith(`CAREER_${up(s)}_`)) ?? "");

  async function toggle() {
    if (!view || busy) return;
    busy = true;
    try {
      load(await setCareer(name, !view.off));
      error = null;
      celebrate(); // on again: what wasn't shown (decision 515); off: nothing
    } catch (e) {
      error = errorText(e);
    } finally {
      busy = false;
    }
  }

  $effect(() => {
    const pop = pushScope({
      name: "career",
      // after a game: a screen every seat drives, as Victory; Esc opens the game's menu below
      modal: !after,
      whileBusy: !after,
      shared: after,
      root: () => panel,
      pressable: () => !revealing,
      handle: (a) => {
        if (a.type === "confirm" && (after || revealing)) confirm();
        else if (a.type === "back" || (a.type === "menu" && !after)) close();
        else return false;
        return true;
      },
    });
    focusControl(backButton);
    return pop;
  });
</script>

<div class="career" class:after class:done class:reduced bind:this={panel} role="dialog" aria-label={t("screen.player.badges", { name })}>
  <header>
    {#if after}
      <button class="candy" class:breathe={!revealing} bind:this={backButton} onclick={confirm} disabled={screenBusy} data-focus-default data-focus-id="next">{t("action.next")} <Prompt action="confirm" /></button>
    {:else}
      <button class="candy" bind:this={backButton} onclick={close} data-focus-default><Icon name="back" /> {t("action.back")} <Prompt action="menu" pad="back" /></button>
    {/if}
    <div class="who">
      <h2>{t("career.page.title", { name })}</h2>
      {#if view && !view.off}<p class="count">{t("career.page.earned", { n: held.size - hidden.size, total })}</p>{/if}
    </div>
    {#if fresh.length && revealed}<p class="new" class:done>{t("career.new", { n: fresh.length })}</p>{/if}
    <div class="slot" data-slot="progress">
      {#if view && !view.off}
        <p class="score"><span>{t("career.points")}</span> <b>{formatScore(view.score, lang)}</b></p>
        {#if view.rank !== null}<RankBar to={view.rank} still />{/if}
      {/if}
    </div>
    {#if view && !after}
      <button class="secondary switch" onclick={toggle} disabled={busy} aria-pressed={!view.off}>
        <Icon name="seal" /> {view.off ? t("career.page.turnOn") : t("career.page.turnOff")}
      </button>
    {/if}
  </header>

  {#if error}<p class="error">{error}</p>{/if}

  {#if view?.off}
    <p class="off"><b>{t("career.page.off")}</b><br />{t("career.page.offText")}</p>
  {:else if view}
    <div class="groups">
      {#each groups as g (g.title())}
        <section>
          <h3>{g.title()}</h3>
          {#each g.rows as row (row[0])}
            <div class="row">
              {#if g === groups[0]}<span class="subject">{rowTitle(row[0])}</span>{/if}
              {#each row as id (id)}
                {@const got = held.get(id)}
                <button class="badge" class:open={!got} class:hidden={hidden.has(id)} class:landed={landed.has(id)} onfocus={() => (focused = id)} onmouseenter={() => (focused = id)} aria-label={`${text(id).name}${got ? `, ${date(got)}` : ""}`}>
                  <img src={icon(id)} alt="" draggable="false" />
                  {#if got}<small>{date(got)}</small>{/if}
                  {#if landed.has(id)}<span class="ring" aria-hidden="true"></span>{/if}
                </button>
              {/each}
            </div>
          {/each}
        </section>
      {/each}
    </div>
    <footer aria-live="polite">
      {#if focused}
        {@const tx = text(focused)}
        {@const got = held.get(focused)}
        <b>{tx.name}</b>
        <span>{tx.description}</span>
        <em>{got ? t("career.page.got", { date: date(got) }) : t("career.page.locked")}</em>
      {/if}
    </footer>
  {/if}
  {#if done}<Fireworks />{/if}
</div>

<style>
  .career {
    position: fixed;
    inset: 0;
    z-index: 45;
    display: flex;
    flex-direction: column;
    gap: calc(0.8 * var(--u));
    padding: var(--safe-y) var(--safe-x);
    background: var(--glass-strong);
    backdrop-filter: blur(calc(0.6 * var(--u))) saturate(1.2);
  }
  header {
    display: flex;
    align-items: center;
    gap: calc(2 * var(--u));
  }
  .who {
    flex: 1;
  }
  h2 {
    margin: 0;
    font-family: var(--font-display);
    font-size: calc(2.6 * var(--u));
    font-weight: 800;
  }
  .count {
    margin: 0;
    color: var(--slate-200);
    font-size: calc(1.3 * var(--u));
    font-variant-numeric: tabular-nums;
  }
  .slot {
    display: flex;
    align-items: center;
    gap: calc(1.5 * var(--u));
  }
  .slot:empty {
    display: none;
  }
  .score {
    margin: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    font-family: var(--font-display);
    font-size: calc(1.2 * var(--u));
    color: var(--slate-200);
  }
  .score b {
    font-size: calc(2.6 * var(--u));
    font-variant-numeric: tabular-nums;
    color: var(--amber);
  }
  .groups {
    flex: 1;
    min-height: 0;
    overflow-y: auto;
    display: grid;
    grid-template-columns: auto 1fr;
    grid-auto-flow: column;
    grid-template-rows: repeat(4, auto);
    align-content: start;
    gap: calc(0.4 * var(--u)) calc(4 * var(--u));
    text-align: left;
  }
  .groups > section:first-child {
    grid-row: 1 / span 4;
  }
  section {
    display: flex;
    flex-direction: column;
    gap: calc(0.4 * var(--u));
  }
  h3 {
    margin: 0;
    font-family: var(--font-display);
    font-size: calc(1.3 * var(--u));
    font-weight: 700;
    color: var(--slate-400);
  }
  .row {
    display: flex;
    align-items: center;
    gap: calc(0.8 * var(--u));
  }
  .subject {
    width: calc(15 * var(--u));
    font-size: calc(1.2 * var(--u));
    color: var(--slate-200);
  }
  .badge {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: calc(0.1 * var(--u));
    padding: calc(0.2 * var(--u));
    border: 1px solid transparent;
    border-radius: calc(0.8 * var(--u));
    background: none;
    color: var(--slate-200);
    transition: transform 0.2s var(--spring);
  }
  .badge img {
    width: calc(3.8 * var(--u));
    height: calc(3.8 * var(--u));
    border-radius: calc(0.8 * var(--u));
  }
  .badge small {
    font-size: calc(0.8 * var(--u));
    font-variant-numeric: tabular-nums;
  }
  /* Open: the look of render.sh's unachieved PNG. */
  .badge.open img {
    filter: grayscale(1) brightness(0.55);
    opacity: 0.7;
  }
  /* Celebration: an empty slot, then the stamp (reduced motion: a fade, decision 591). */
  .badge {
    position: relative;
  }
  .badge.hidden img,
  .badge.hidden small {
    opacity: 0;
  }
  .badge.hidden::after {
    content: "";
    position: absolute;
    inset: calc(0.2 * var(--u)) calc(0.2 * var(--u)) auto;
    height: calc(3.8 * var(--u));
    border: 2px dashed var(--slate-600);
    border-radius: calc(0.8 * var(--u));
  }
  .badge.landed img {
    animation: stamp 0.45s var(--spring) backwards;
  }
  .badge .ring {
    position: absolute;
    inset: calc(0.2 * var(--u)) calc(0.2 * var(--u)) auto;
    height: calc(3.8 * var(--u));
    border-radius: calc(0.8 * var(--u));
    box-shadow: 0 0 0 2px var(--amber), 0 0 calc(1.2 * var(--u)) var(--amber);
    pointer-events: none;
  }
  .reduced .badge.landed img {
    animation: none;
    transition: opacity 0.3s ease;
  }
  @keyframes stamp {
    0% {
      transform: scale(2.6) rotate(-14deg);
      opacity: 0;
    }
    60% {
      transform: scale(0.92) rotate(2deg);
      opacity: 1;
    }
  }
  .new {
    margin: 0;
    font-family: var(--font-display);
    font-size: calc(2.4 * var(--u));
    font-weight: 800;
    color: var(--amber);
    animation: arrive 0.6s var(--spring) backwards;
  }
  .after {
    z-index: 20; /* a screen: under the overlay and the corner buttons */
  }
  .badge:hover,
  .badge:focus-visible,
  .badge:global([data-nav]) {
    border-color: var(--sky);
    transform: translateY(calc(-0.2 * var(--u)));
  }
  footer {
    display: flex;
    flex-direction: column;
    min-height: calc(6 * var(--u));
    padding: calc(0.8 * var(--u)) calc(1.2 * var(--u));
    border: 1px solid var(--slate-600);
    border-radius: calc(1 * var(--u));
    background: var(--night-700);
    font-size: calc(1.3 * var(--u));
  }
  footer b {
    font-family: var(--font-display);
    font-size: calc(1.7 * var(--u));
  }
  footer em {
    color: var(--slate-400);
    font-style: normal;
  }
  .off {
    margin: auto;
    max-width: calc(48 * var(--u));
    text-align: center;
    font-size: calc(1.5 * var(--u));
    color: var(--slate-200);
  }
  .error {
    margin: 0;
    color: var(--coral);
    font-size: calc(1.1 * var(--u));
  }
</style>
