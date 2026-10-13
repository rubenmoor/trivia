<script lang="ts">
  // Admin overlay on Esc (04-ui-tv-display.md, UI-13). The family sees it, so it never shows
  // the correct answer. ↑/↓ choose, Enter runs, ←/→ change a volume or a joker budget, Esc closes.
  // Left column: game actions; right column: sound, and the running game's joker budget (MD-4).
  // Under the budget, read-only: the game's group and bundles (plan 29).
  // Outside gamemaster mode no undo, skip or budget editor (D-74); «Preguntas marcadas» in every mode (decision 60).
  // Language rows (plan 68) only with ≥2 options: ←/→ pick; questions apply at once, the UI on Enter (reload).
  import { fetchGameChoice, fetchLanguage, localeSupply, setLanguage } from "../lib/api";
  import { desktop } from "../lib/desktop";
  import { flush } from "../lib/engine";
  import { endonym, t } from "../lib/i18n";
  import { pushScope, type Action } from "../lib/input.svelte";
  import Credits from "./Credits.svelte";
  import Prompt from "./Prompt.svelte";
  import type { Game, GameMode, JokerBudget, JokerName, Language, Supply } from "../lib/types";
  import { TOKENS } from "./JokerTray.svelte";
  import { setVolumes, sound, type Volumes } from "./sound.svelte";

  type Item = {
    label: string;
    enabled: boolean;
    run: () => void;
    right?: boolean;
    confirm?: boolean;
    volume?: Channel;
    joker?: JokerName;
    preset?: boolean;
    lang?: LangKind;
    /** Read-only: the running game's choice (plan 29); ↑/↓ skip it. */
    info?: boolean;
  };
  type LangKind = "ui" | "questions";
  type Channel = "music" | "effects" | "media";

  const CHANNELS: { key: Channel; label: string }[] = [
    { key: "music", label: t("overlay.music") },
    { key: "effects", label: t("overlay.effects") },
    { key: "media", label: t("overlay.media") },
  ];
  const STEP = 0.1;
  /** «Como las cartas»: the printed card set (JK-11); the same as `CARDS` in app/server/game.py. */
  const CARDS: JokerBudget = { hint: 4, skip: 2, easier: 2, category: 2, snipe: 2 };
  /** Budget steps for ←/→: 0 to 9 uses, then unlimited (null). */
  const MAX_USES = 9;

  // The review tool and stats pages run on the authoring server (D-35). A build made with
  // VITE_AUTHORING_URL="" (the packaged game) and the desktop shell have none and hide the links.
  const env = import.meta.env.VITE_AUTHORING_URL;
  const authoring = desktop ? "" : (env ?? `${location.protocol}//${location.hostname}:8001`);

  function change(key: Channel, by: number) {
    const v = Math.round(Math.min(1, Math.max(0, sound.volumes[key] + by)) * 10) / 10;
    setVolumes({ [key]: v } as Partial<Volumes>);
  }

  let {
    mode,
    questionId,
    questionLabel,
    canSkip,
    canUndo,
    canRestart,
    budget,
    left,
    settings,
    onclose,
    onskip,
    onskipall,
    onundo,
    onrestart,
    onbudget,
    onflags,
  }: {
    mode: GameMode;
    /** For debugging (04, "Admin overlay"): the question on screen, or the last one answered. */
    questionId: string | null;
    questionLabel: string;
    canSkip: boolean;
    canUndo: boolean;
    canRestart: boolean;
    /** The running game's joker budget (MD-4), or null without a running game. */
    budget: JokerBudget | null;
    /** Uses left in the running game. */
    left: JokerBudget | null;
    /** The running game's settings, for its group and bundles (plan 29), or null. */
    settings: Game["settings"] | null;
    onclose: () => void;
    onskip: () => void;
    /** «Bloquear pregunta»: a broken or wrong question, never offered again (plan 65). */
    onskipall: () => void;
    onundo: () => void;
    onrestart: () => void;
    onbudget: (budget: Partial<JokerBudget>) => void;
    /** «Preguntas marcadas» opens over the overlay. */
    onflags: () => void;
  } = $props();

  const gamemaster = $derived(mode === "gamemaster");

  /** The Credits screen (PUB-5) is open over the game; the menu hides. */
  let creditsOpen = $state(false);
  function fullscreen() {
    if (desktop) desktop.toggleFullscreen();
    else if (document.fullscreenElement) document.exitFullscreen();
    else document.documentElement.requestFullscreen().catch(() => {});
    onclose();
  }

  /** The budget as last changed here, until the server's answer arrives: fast clicks build on it. */
  let pending = $state<JokerBudget | null>(null);
  $effect(() => {
    void budget;
    pending = null;
  });
  const current = $derived(budget && (pending ?? budget));

  function setBudget(change: Partial<JokerBudget>) {
    if (!current) return;
    pending = { ...current, ...change };
    onbudget(change);
  }

  const unlimited = $derived(!!current && TOKENS.every((t) => current![t.name] === null));
  const cards = $derived(!!current && TOKENS.every((t) => current![t.name] === CARDS[t.name]));
  const presetLabel = $derived(t(unlimited ? "overlay.unlimited" : cards ? "overlay.cards" : "overlay.custom"));

  /** Sin límite ↔ Como las cartas; a custom budget goes back to unlimited. */
  function cyclePreset() {
    setBudget(unlimited ? CARDS : Object.fromEntries(TOKENS.map((t) => [t.name, null])));
  }

  function stepJoker(name: JokerName, by: number) {
    const now = current?.[name];
    const index = Math.min(MAX_USES + 1, Math.max(0, (now ?? MAX_USES + 1) + by));
    const next = index > MAX_USES ? null : index;
    if (next !== now) setBudget({ [name]: next });
  }

  /** Stored language and options; per question locale its supply (default bundles). Null until loaded. */
  let langs = $state<{ language: Language; ui: string[]; questions: string[]; supply: Record<string, Supply> } | null>(null);
  /** The option each row shows; differs from the stored one only for an unapplied UI language or a disabled locale. */
  let shown = $state<Language | null>(null);
  $effect(() => {
    (async () => {
      const l = await fetchLanguage();
      const supply = l.questions.length > 1 ? await localeSupply() : {};
      langs = { ...l, supply };
      shown = l.language;
    })().catch(() => {});
  });
  const langKinds = $derived(langs ? (["ui", "questions"] as const).filter((k) => langs![k].length > 1) : []);

  function blocked(kind: LangKind, tag: string): string | null {
    const s = kind === "questions" ? langs?.supply[tag] : undefined;
    return s && !s.ok ? t("language.short", { n: s.available }) : null;
  }

  async function stepLang(kind: LangKind, by: number) {
    if (!langs || !shown) return;
    const options = langs[kind];
    const tag = options[(options.indexOf(shown[kind]) + by + options.length) % options.length];
    shown = { ...shown, [kind]: tag };
    if (kind === "questions" && !blocked(kind, tag) && tag !== langs.language.questions)
      langs.language = await setLanguage({ ui: langs.language.ui, questions: tag });
  }

  /** The UI language is a boot constant: write the save, then reload. */
  async function applyUi() {
    if (!langs || !shown || shown.ui === langs.language.ui) return;
    await setLanguage({ ui: shown.ui, questions: langs.language.questions });
    location.reload();
  }

  /** «Adolescentes · Básico, Colombia»; null without a running game. */
  let choiceLine = $state<string | null>(null);
  $effect(() => {
    const s = settings;
    if (!s) return void (choiceLine = null);
    fetchGameChoice(s)
      .then(({ group, difficulty, bundles }) => {
        const head = difficulty ? t("choice.difficulty", { start: difficulty.start, end: difficulty.end }) : (group ?? "");
        choiceLine = t("choice.line", { group: head, bundles: bundles.join(", ") });
      })
      .catch(() => {});
  });

  /** Pending saves first (plan 55). */
  async function quit() {
    await flush();
    await desktop?.quit();
  }

  const items = $derived<Item[]>([
    { label: t("overlay.continue"), enabled: true, run: onclose },
    ...(gamemaster
      ? [
          { label: t("overlay.skip"), enabled: canSkip, run: onskip },
          { label: t("overlay.skipAll"), enabled: canSkip, run: onskipall, confirm: true },
          { label: t("overlay.undo"), enabled: canUndo, run: onundo },
        ]
      : []),
    { label: t("flag.list"), enabled: true, run: onflags },
    { label: t("overlay.fullscreen"), enabled: true, run: fullscreen },
    { label: t("credits.open"), enabled: true, run: () => (creditsOpen = true) },
    { label: t("overlay.restart"), enabled: canRestart, run: onrestart, confirm: true },
    ...(desktop ? [{ label: t("overlay.quit"), enabled: true, run: quit }] : []),
    ...CHANNELS.map((c) => ({ label: c.label, enabled: true, run: () => {}, volume: c.key, right: true })),
    {
      label: t(sound.volumes.muted ? "overlay.muted" : "overlay.unmuted"),
      enabled: true,
      run: () => setVolumes({ muted: !sound.volumes.muted }),
      right: true,
    },
    ...langKinds.map((k) => ({
      label: t(k === "ui" ? "language.ui" : "language.questions"),
      enabled: true,
      run: k === "ui" ? applyUi : () => {},
      lang: k,
      right: true,
    })),
    ...(budget && gamemaster
      ? [
          { label: t("overlay.jokers"), enabled: true, run: cyclePreset, preset: true, right: true },
          ...TOKENS.map((t) => ({ label: t.label, enabled: true, run: () => {}, joker: t.name, right: true })),
        ]
      : []),
    ...(budget && choiceLine ? [{ label: choiceLine, enabled: false, run: () => {}, info: true, right: true }] : []),
  ]);

  let selected = $state(0);
  /** Index of an item that asked "¿Seguro?" and waits for a second Enter. */
  let confirming = $state<number | null>(null);

  function activate(i: number) {
    const item = items[i];
    if (!item.enabled) return;
    if (item.confirm && confirming !== i) {
      confirming = i;
      return;
    }
    item.run();
  }

  function handle(a: Action): boolean {
    const item = items[selected];
    const by = a.type === "navigate" ? { right: 1, left: -1, up: 0, down: 0 }[a.dir] : 0;
    if (a.type === "navigate" && (a.dir === "up" || a.dir === "down")) {
      const step = a.dir === "down" ? 1 : -1;
      do selected = (selected + step + items.length) % items.length;
      while (!items[selected].enabled);
      confirming = null;
    } else if (by && item.volume) change(item.volume, by * STEP);
    else if (by && item.joker) stepJoker(item.joker, by);
    else if (by && item.preset) cyclePreset();
    else if (by && item.lang) stepLang(item.lang, by);
    else if (a.type === "confirm") activate(selected);
    else if (a.type === "menu") onclose();
    else if (a.type === "back" && a.device === "gamepad") confirming === null ? onclose() : (confirming = null); // B leaves
    else return false;
    return true;
  }

  $effect(() => pushScope({ name: "overlay", handle, modal: true, whileBusy: true }));
</script>

{#snippet row(item: Item, i: number)}
  {#if item.volume}
    {@const key = item.volume}
    <label class="row volume" class:selected={i === selected} onmouseenter={() => (selected = i)}>
      <span>{item.label}</span>
      <input
        type="range"
        min="0"
        max="1"
        step={STEP}
        value={sound.volumes[key]}
        oninput={(e) => setVolumes({ [key]: Number(e.currentTarget.value) } as Partial<Volumes>)}
        tabindex="-1"
      />
      <span class="value">{Math.round(sound.volumes[key] * 100)} %</span>
    </label>
  {:else if item.joker}
    {@const name = item.joker}
    <div class="row joker" class:selected={i === selected} role="group" onmouseenter={() => (selected = i)}>
      <span>{item.label}</span>
      <button class="step" onclick={() => stepJoker(name, -1)} tabindex="-1" aria-label={t("overlay.less")}>−</button>
      <span class="value">{current?.[name] ?? "∞"}</span>
      <button class="step" onclick={() => stepJoker(name, 1)} tabindex="-1" aria-label={t("overlay.more")}>+</button>
      <span class="left">{left?.[name] != null ? t("overlay.left", { n: left[name] }) : ""}</span>
    </div>
  {:else if item.info}
    <p class="row readonly info">{item.label}</p>
  {:else if item.lang && shown}
    {@const kind = item.lang}
    {@const tag = shown[kind]}
    {@const reason = blocked(kind, tag)}
    <div class="row lang" class:selected={i === selected} role="group" onmouseenter={() => (selected = i)}>
      <span>{item.label}</span>
      <button class="step" onclick={() => stepLang(kind, -1)} tabindex="-1" aria-label={t("language.previous")}>‹</button>
      <span class="value" class:off={reason}>{endonym(tag, kind)}</span>
      <button class="step" onclick={() => stepLang(kind, 1)} tabindex="-1" aria-label={t("language.next")}>›</button>
      {#if reason}
        <span class="note">{reason}</span>
      {:else if kind === "ui" && tag !== langs?.language.ui}
        <button class="note apply" onclick={applyUi} tabindex="-1">{t("language.apply")} <Prompt action="confirm" /></button>
      {/if}
    </div>
  {:else}
    <button
      class:selected={i === selected}
      disabled={!item.enabled}
      onclick={() => activate(i)}
      onmouseenter={() => item.enabled && (selected = i)}
    >
      {#if item.preset}
        {t("overlay.preset")} <b>{presetLabel}</b>
      {:else}
        {confirming === i ? t("overlay.confirm") : item.label}
      {/if}
    </button>
  {/if}
{/snippet}

<div class="overlay" class:clear={creditsOpen}>
  <div class="menu" class:hidden={creditsOpen}>
    <h2>{t("overlay.title")}</h2>
    <div class="columns">
      <div class="column">
        {#each items as item, i (item.joker ?? item.volume ?? item.lang ?? item.label)}
          {#if !item.right}{@render row(item, i)}{/if}
        {/each}
      </div>
      <div class="column">
        <h3>{t("overlay.sound")}</h3>
        {#each items as item, i (item.joker ?? item.volume ?? item.lang ?? item.label)}
          {#if item.right && !item.preset && !item.joker && !item.info}{@render row(item, i)}{/if}
        {/each}
        {#if budget}
          <h3>{t("overlay.budget")}</h3>
          {#if gamemaster}
            {#each items as item, i (item.joker ?? item.volume ?? item.lang ?? item.label)}
              {#if item.preset || item.joker}{@render row(item, i)}{/if}
            {/each}
          {:else}
            {#each TOKENS as token (token.name)}
              <p class="row readonly">
                <span>{token.label}</span>
                <span class="value">{left?.[token.name] ?? "∞"}</span>
              </p>
            {/each}
          {/if}
          {#each items as item, i (item.label)}
            {#if item.info}{@render row(item, i)}{/if}
          {/each}
        {/if}
      </div>
    </div>
    <p class="debug">{t(gamemaster ? "overlay.keys" : "overlay.keysVolume")} <Prompt action={{ type: "navigate", dir: "left" }} /> <Prompt action={{ type: "navigate", dir: "right" }} /></p>
    {#if questionId}
      <p class="debug">
        {questionLabel}:
        {#if authoring}
          <a href="{authoring}/review/{encodeURIComponent(questionId)}" target="_blank" tabindex="-1"><code>{questionId}</code></a>
        {:else}
          <code>{questionId}</code>
        {/if}
      </p>
    {/if}
    {#if authoring}
      <p class="debug">
        {t("overlay.stats")}
        <a href="{authoring}/stats/categories" target="_blank" tabindex="-1">{t("overlay.statsCategories")}</a> ·
        <a href="{authoring}/stats/difficulty" target="_blank" tabindex="-1">{t("overlay.statsDifficulty")}</a>
      </p>
    {/if}
  </div>
  {#if creditsOpen}
    <Credits onclose={() => (creditsOpen = false)} />
  {/if}
</div>

<style>
  .overlay {
    position: fixed;
    inset: 0;
    z-index: 40;
    display: grid;
    place-items: center;
    background: rgba(5, 8, 16, 0.72);
  }
  .overlay.clear {
    background: none;
  }
  .hidden {
    visibility: hidden;
  }
  .menu {
    display: flex;
    flex-direction: column;
    gap: calc(0.7 * var(--u));
    padding: calc(2.4 * var(--u)) calc(2.4 * var(--u));
    border: 1px solid var(--slate-600);
    border-radius: calc(1.6 * var(--u));
    background: var(--night-700);
    box-shadow: 0 calc(1.5 * var(--u)) calc(4 * var(--u)) rgba(0, 0, 0, 0.6);
  }
  h2 {
    margin: 0 0 calc(0.6 * var(--u));
    text-align: center;
    font-family: var(--font-display);
    font-size: calc(2.6 * var(--u));
    font-weight: 800;
  }
  h3 {
    margin: calc(0.4 * var(--u)) 0 0;
    font-family: var(--font-display);
    font-size: calc(1.2 * var(--u));
    font-weight: 700;
    color: var(--slate-400);
  }
  .columns {
    display: grid;
    grid-template-columns: calc(36 * var(--u)) calc(40 * var(--u));
    gap: calc(2.4 * var(--u));
    align-items: start;
  }
  .column {
    display: flex;
    flex-direction: column;
    gap: calc(0.7 * var(--u));
  }
  button {
    padding: calc(0.7 * var(--u)) calc(1.4 * var(--u));
    border: calc(0.18 * var(--u)) solid transparent;
    border-radius: calc(0.8 * var(--u));
    background: var(--slate-600);
    font-size: calc(1.5 * var(--u));
    font-weight: 700;
    text-align: left;
  }
  .debug {
    margin: calc(0.6 * var(--u)) 0 0;
    text-align: center;
    font-size: calc(0.9 * var(--u));
    color: var(--slate-400);
  }
  .debug code {
    color: var(--slate-200);
    user-select: all;
  }
  .debug a {
    color: var(--slate-200);
  }
  button.selected,
  .row.selected {
    border-color: var(--amber);
  }
  .row {
    display: grid;
    align-items: center;
    gap: calc(1 * var(--u));
    padding: calc(0.45 * var(--u)) calc(1.4 * var(--u));
    border: calc(0.18 * var(--u)) solid transparent;
    border-radius: calc(0.8 * var(--u));
    background: rgba(43, 54, 80, 0.5);
    font-size: calc(1.2 * var(--u));
    font-weight: 700;
  }
  .volume {
    grid-template-columns: 1fr calc(12 * var(--u)) calc(4.5 * var(--u));
  }
  .joker {
    grid-template-columns: 1fr calc(2.4 * var(--u)) calc(2.4 * var(--u)) calc(2.4 * var(--u)) calc(7 * var(--u));
  }
  .lang {
    grid-template-columns: 1fr calc(2.4 * var(--u)) calc(14 * var(--u)) calc(2.4 * var(--u));
  }
  .lang .value {
    text-align: center;
    color: var(--amber);
  }
  .lang .value.off {
    color: var(--slate-400);
    text-decoration: line-through;
  }
  .note {
    grid-column: 1 / -1;
    color: var(--slate-400);
    font-weight: 600;
  }
  .note.apply {
    padding: calc(0.3 * var(--u)) calc(0.8 * var(--u));
    font-size: calc(1.1 * var(--u));
    color: var(--slate-200);
  }
  .volume input {
    accent-color: var(--amber);
    width: 100%;
  }
  .value {
    text-align: right;
    color: var(--slate-200);
    font-variant-numeric: tabular-nums;
  }
  .joker .value {
    text-align: center;
    color: var(--amber);
  }
  .step {
    display: grid;
    place-items: center;
    height: calc(2.2 * var(--u));
    padding: 0;
    font-size: calc(1.4 * var(--u));
    text-align: center;
  }
  .left {
    color: var(--slate-400);
    font-weight: 600;
    text-align: right;
  }
  .readonly {
    grid-template-columns: 1fr auto;
    margin: 0;
  }
  .info {
    grid-template-columns: 1fr;
    color: var(--slate-200);
  }
  .readonly .value {
    color: var(--amber);
  }
  button:disabled {
    opacity: 0.35;
  }
</style>
