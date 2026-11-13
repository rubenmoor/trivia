<script lang="ts">
  // The badge page (plan 197, plans/04-ui-tv-display.md "Career"): one player's 39 career badges, earned in colour
  // with their date, open ones dimmed; the focused badge's text below; the career's on/off switch. A layer, as Credits.
  import { type CareerView, SCORE_MILESTONES, SUBJECTS, YEAR_GROUPS } from "../engine/career.ts";
  import { fetchCareers, setCareer } from "../lib/api.ts";
  import { badgeText } from "../lib/badge-text.ts";
  import { errorText } from "../lib/errors.ts";
  import { lang, t } from "../lib/i18n.ts";
  import { focusControl, pushScope } from "../lib/input.svelte.ts";
  import { badgeNames, displayName } from "../lib/names.svelte.ts";
  import Icon from "./Icon.svelte";
  import Prompt from "./Prompt.svelte";

  let { name, onclose }: { name: string; onclose: () => void } = $props();

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
  fetchCareers().then(load, (e: unknown) => (error = errorText(e)));

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
    } catch (e) {
      error = errorText(e);
    } finally {
      busy = false;
    }
  }

  $effect(() => {
    const pop = pushScope({ name: "career", modal: true, whileBusy: true, root: () => panel, handle: (a) => (a.type === "back" || a.type === "menu" ? (onclose(), true) : false) });
    focusControl(backButton);
    return pop;
  });
</script>

<div class="career" bind:this={panel} role="dialog" aria-label={t("screen.player.badges", { name })}>
  <header>
    <button class="candy" bind:this={backButton} onclick={onclose} data-focus-default><Icon name="back" /> {t("action.back")} <Prompt action="menu" pad="back" /></button>
    <div class="who">
      <h2>{t("career.page.title", { name })}</h2>
      {#if view && !view.off}<p class="count">{t("career.page.earned", { n: held.size, total })}</p>{/if}
    </div>
    <!-- part 6: score, rank and progress bars -->
    <div class="slot" data-slot="progress"></div>
    {#if view}
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
                <button class="badge" class:open={!got} onfocus={() => (focused = id)} onmouseenter={() => (focused = id)} aria-label={`${text(id).name}${got ? `, ${date(got)}` : ""}`}>
                  <img src={icon(id)} alt="" draggable="false" />
                  {#if got}<small>{date(got)}</small>{/if}
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
  .slot:empty {
    display: none;
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
