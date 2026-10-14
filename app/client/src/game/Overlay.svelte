<script lang="ts">
  // Gamemaster menu on Esc (04-ui-tv-display.md, UI-13; MD-12, D-88). The family sees it, so it never shows
  // the correct answer. Two parts: general (every mode: actions, sound, languages) and, in gamemaster mode,
  // the cheats apart (skip, block, undo, replace, jump to level, difficulty and bundles, jokers left).
  // ↑/↓ choose, Enter runs, ←/→ change a value (else the next column), Esc closes. Outside gamemaster
  // mode no cheats (D-74), the jokers left read-only. Language rows (plan 68) only with ≥2 options.
  // Code mods' rows (plan 117) in a last column.
  import { fetchGameChoice, fetchJokersUsed, fetchLanguage, localeSupply, setLanguage, type GameActionBody } from "../lib/api.ts";
  import { desktop, devMode } from "../lib/desktop.ts";
  import { flush } from "../lib/engine.ts";
  import { endonym, t } from "../lib/i18n.ts";
  import { pushScope, type Action } from "../lib/input.svelte.ts";
  import { menuRows } from "../lib/mods.ts";
  import Credits from "./Credits.svelte";
  import GameSettings from "./GameSettings.svelte";
  import GoToDialog from "./GoToDialog.svelte";
  import { levelsOf } from "./levels.ts";
  import Prompt from "./Prompt.svelte";
  import type { Game, GameMode, JokerBudget, JokerName, Language, Supply } from "../lib/types.ts";
  import { stepUses, TOKENS } from "./jokers.ts";
  import { setVolumes, sound, type Volumes } from "./sound.svelte.ts";

  type Item = {
    label: string;
    enabled: boolean;
    run: () => void;
    /** 0 general, 1 cheats, 2 jokers, 3 mods. */
    col: 0 | 1 | 2 | 3;
    /** Mod rows: their labels may repeat. */
    key?: string;
    /** General part, under «Sonido»: volumes, mute, languages. */
    sound?: boolean;
    confirm?: boolean;
    volume?: Channel;
    joker?: JokerName;
    lang?: LangKind;
    /** «Cambiar pregunta»: ←/→ toggles seen. */
    replace?: boolean;
    /** «Saltar a nivel»: ←/→ picks the level. */
    level?: boolean;
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

  // The review tool and stats pages run on the authoring server (D-35). A build made with
  // VITE_AUTHORING_URL="" (the packaged game) and the desktop shell have none and hide the links.
  // The dev server's shim (plan 99) is no shell: links on, no quit.
  const shell = desktop?.devServer ? null : desktop;
  const env = import.meta.env.VITE_AUTHORING_URL;
  const authoring = shell ? "" : (env ?? `${location.protocol}//${location.hostname}:8001`);

  function change(key: Channel, by: number) {
    const v = Math.round(Math.min(1, Math.max(0, sound.volumes[key] + by)) * 10) / 10;
    setVolumes({ [key]: v } as Partial<Volumes>);
  }

  let {
    mode,
    game,
    running,
    questionId,
    questionLabel,
    canSkip,
    questionOn,
    canTable,
    canUndo,
    canRestart,
    canBudget,
    onclose,
    onskip,
    onskipall,
    onundo,
    onreplace,
    onlevel,
    onsettings,
    ongoto,
    onrestart,
    onbudget,
    onflags,
  }: {
    mode: GameMode;
    /** The newest game (running or finished), or null. */
    game: Game | null;
    running: boolean;
    /** For debugging (04, "Admin overlay"): the question on screen, or the last one answered. */
    questionId: string | null;
    questionLabel: string;
    /** A question on screen: skip, block, replace. */
    canSkip: boolean;
    /** A question on screen: «Ir a pregunta…» in dev mode (plan 85). */
    questionOn: boolean;
    /** A new table is possible: jump to level, difficulty and bundles. */
    canTable: boolean;
    canUndo: boolean;
    canRestart: boolean;
    /** Off while the question's answer or a joker is out: its callback would bring back the old budget. */
    canBudget: boolean;
    onclose: () => void;
    onskip: () => void;
    /** «Bloquear pregunta»: a broken or wrong question, never offered again (plan 65). */
    onskipall: () => void;
    onundo: () => void;
    onreplace: (seen: boolean) => void;
    onlevel: (level: number) => void;
    /** Difficulty and bundles; the refusal's text, or null when applied. */
    onsettings: (body: GameActionBody) => Promise<string | null>;
    /** «Ir a pregunta…»: the refusal's text, or null when it opened. */
    ongoto: (id: string) => Promise<string | null>;
    onrestart: () => void;
    onbudget: (budget: Partial<JokerBudget>) => void;
    /** «Preguntas marcadas» opens over the overlay. */
    /** Null without a valid Steam user (decision 111): no «Preguntas marcadas». */
    onflags: (() => void) | null;
  } = $props();

  const gamemaster = $derived(mode === "gamemaster");
  /** The running game's joker budget (MD-4), or null. */
  const budget = $derived(running ? (game?.settings.jokers ?? null) : null);
  const cheats = $derived(gamemaster && !!game && (running || canUndo));

  /** The Credits screen (PUB-5) is open over the game; the menu hides. */
  let creditsOpen = $state(false);
  /** «Dificultad y paquetes» is open over the menu. */
  let settingsOpen = $state(false);
  let goToOpen = $state(false);
  function fullscreen() {
    if (desktop) desktop.toggleFullscreen();
    else if (document.fullscreenElement) document.exitFullscreen();
    else document.documentElement.requestFullscreen().catch(() => {});
    onclose();
  }

  /** «Cambiar pregunta» counts the old one as seen. */
  let seen = $state(false);
  /** «Saltar a nivel»'s target, from the current level. */
  let target = $state(1);
  $effect(() => {
    target = game?.level ?? 1;
  });
  const levels = $derived(levelsOf(game));

  /** Uses so far per joker (MD-12: the rows edit uses left; limit = used + left). */
  let used = $state<Record<JokerName, number> | null>(null);
  $effect(() => {
    void budget;
    fetchJokersUsed().then((u) => (used = u)).catch(() => {});
  });

  /** The budget as last changed here, until the engine's answer arrives: fast clicks build on it. */
  let pending = $state<JokerBudget | null>(null);
  $effect(() => {
    void budget;
    pending = null;
  });
  const current = $derived(budget && (pending ?? budget));

  function setBudget(change: Partial<JokerBudget>) {
    if (!current || !canBudget) return;
    pending = { ...current, ...change };
    onbudget(change);
  }

  /** Uses left of a joker, null = unlimited. */
  function leftOf(name: JokerName): number | null {
    const limit = current?.[name];
    return limit == null ? null : Math.max(0, limit - (used?.[name] ?? 0));
  }

  /** Give back (+) or take away (−) one use; past 9 left: unlimited. */
  function stepJoker(name: JokerName, by: number) {
    if (!used) return;
    const now = leftOf(name);
    const next = stepUses(now, by);
    if (next === now) return;
    setBudget({ [name]: next === null ? null : used[name] + next });
  }

  function stepLevel(by: number) {
    target = ((target - 1 + by + levels) % levels) + 1;
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
    })().catch((e) => console.warn("language rows", e));
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
    const s = running ? game?.settings : null;
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

  /** Read once per opening; a row closes the menu, then runs. */
  const modRows: Item[] = menuRows().map((r, i) => ({
    label: r.label,
    enabled: true,
    run: () => (onclose(), r.select()),
    col: 3,
    key: `mod:${i}`,
  }));

  const items = $derived<Item[]>([
    { label: t("overlay.continue"), enabled: true, run: onclose, col: 0 },
    ...(onflags ? [{ label: t("flag.list"), enabled: true, run: onflags, col: 0 as const }] : []),
    ...(devMode && questionOn ? [{ label: t("overlay.goTo"), enabled: canSkip, run: () => (goToOpen = true), col: 0 as const }] : []),
    { label: t("overlay.fullscreen"), enabled: true, run: fullscreen, col: 0 },
    { label: t("credits.open"), enabled: true, run: () => (creditsOpen = true), col: 0 },
    { label: t("overlay.restart"), enabled: canRestart, run: onrestart, confirm: true, col: 0 },
    ...(shell ? [{ label: t("overlay.quit"), enabled: true, run: quit, col: 0 as const }] : []),
    ...CHANNELS.map((c) => ({ label: c.label, enabled: true, run: () => {}, volume: c.key, col: 0 as const, sound: true })),
    {
      label: t(sound.volumes.muted ? "overlay.muted" : "overlay.unmuted"),
      enabled: true,
      run: () => setVolumes({ muted: !sound.volumes.muted }),
      col: 0,
      sound: true,
    },
    ...langKinds.map((k) => ({
      label: t(k === "ui" ? "language.ui" : "language.questions"),
      enabled: true,
      run: k === "ui" ? applyUi : () => {},
      lang: k,
      col: 0 as const,
      sound: true,
    })),
    ...(cheats
      ? [
          { label: t("overlay.skip"), enabled: canSkip, run: onskip, col: 1 as const },
          { label: t("overlay.skipAll"), enabled: canSkip, run: onskipall, confirm: true, col: 1 as const },
          { label: t("overlay.undo"), enabled: canUndo, run: onundo, col: 1 as const },
          { label: t("overlay.replace"), enabled: canSkip, run: () => onreplace(seen), replace: true, col: 1 as const },
          { label: t("overlay.level"), enabled: canTable, run: () => onlevel(target), level: true, col: 1 as const },
          { label: t("overlay.settings"), enabled: canTable, run: () => (settingsOpen = true), col: 1 as const },
          ...(choiceLine ? [{ label: choiceLine, enabled: false, run: () => {}, info: true, col: 1 as const }] : []),
        ]
      : []),
    ...(cheats && budget
      ? [
          ...TOKENS.map((t) => ({ label: t.label, enabled: !!used && canBudget, run: () => {}, joker: t.name, col: 2 as const })),
        ]
      : []),
    ...modRows,
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

  /** ←/→ on an item without a value: the enabled item at about the same height in the next column. */
  function across(by: number): boolean {
    const here = items[selected];
    const cols = [...new Set(items.map((x) => x.col))].sort((a, b) => a - b);
    const to = cols[cols.indexOf(here.col) + by];
    if (to === undefined) return false;
    const y = (i: number) => menu?.querySelector(`[data-item="${i}"]`)?.getBoundingClientRect().top ?? 0;
    const from = y(selected);
    const list = items.flatMap((x, i) => (x.col === to && x.enabled ? [i] : []));
    if (!list.length) return false;
    selected = list.reduce((m, i) => (Math.abs(y(i) - from) < Math.abs(y(m) - from) ? i : m));
    confirming = null;
    return true;
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
    else if (by && item.lang) stepLang(item.lang, by);
    else if (by && item.replace && item.enabled) seen = !seen;
    else if (by && item.level && item.enabled) stepLevel(by);
    else if (by) across(by);
    else if (a.type === "confirm") activate(selected);
    else if (a.type === "menu") onclose();
    else if (a.type === "back" && a.device === "gamepad") {
      // B leaves
      if (confirming === null) onclose();
      else confirming = null;
    } else return false;
    return true;
  }

  $effect(() => pushScope({ name: "overlay", handle, modal: true, whileBusy: true }));

  let menu = $state<HTMLElement>();
  /** A menu taller than the screen scrolls (B-17): keep the selected row in view. */
  $effect(() => {
    if (selected === 0) menu?.scrollTo({ top: 0 });
    else menu?.querySelector(".selected")?.scrollIntoView({ block: "nearest" });
  });

  async function applySettings(body: GameActionBody): Promise<string | null> {
    const refused = await onsettings(body);
    if (refused === null) settingsOpen = false;
    return refused;
  }
</script>

{#snippet row(item: Item, i: number)}
  {#if item.volume}
    {@const key = item.volume}
    <label class="row volume" class:selected={i === selected} data-item={i} onmouseenter={() => (selected = i)}>
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
    <div class="row joker" class:selected={i === selected} data-item={i} role="group" onmouseenter={() => (selected = i)}>
      <span>{item.label}</span>
      <button class="step" onclick={() => stepJoker(name, -1)} disabled={!item.enabled} tabindex="-1" aria-label={t("overlay.less")}>−</button>
      <span class="value">{leftOf(name) ?? "∞"}</span>
      <button class="step" onclick={() => stepJoker(name, 1)} disabled={!item.enabled} tabindex="-1" aria-label={t("overlay.more")}>+</button>
      <span class="left">{used ? t("overlay.used", { n: used[name] }) : ""}</span>
    </div>
  {:else if item.level || item.replace}
    <div class="row pick" class:selected={i === selected} class:off={!item.enabled} data-item={i} role="group" onmouseenter={() => item.enabled && (selected = i)}>
      <button class="run" onclick={() => activate(i)} disabled={!item.enabled} tabindex="-1">{item.label}</button>
      <button class="step" onclick={() => (item.level ? stepLevel(-1) : (seen = !seen))} disabled={!item.enabled} tabindex="-1" aria-label={t("overlay.less")}>‹</button>
      <span class="value">{item.level ? target : t(seen ? "overlay.seen" : "overlay.unseen")}</span>
      <button class="step" onclick={() => (item.level ? stepLevel(1) : (seen = !seen))} disabled={!item.enabled} tabindex="-1" aria-label={t("overlay.more")}>›</button>
    </div>
  {:else if item.info}
    <p class="row readonly info">{item.label}</p>
  {:else if item.lang && shown}
    {@const kind = item.lang}
    {@const tag = shown[kind]}
    {@const reason = blocked(kind, tag)}
    <div class="row lang" class:selected={i === selected} data-item={i} role="group" onmouseenter={() => (selected = i)}>
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
      data-item={i}
      disabled={!item.enabled}
      onclick={() => activate(i)}
      onmouseenter={() => item.enabled && (selected = i)}
    >
      {confirming === i ? t("overlay.confirm") : item.label}
    </button>
  {/if}
{/snippet}

{#snippet column(col: number, sound = false)}
  {#each items as item, i (item.joker ?? item.volume ?? item.lang ?? item.key ?? item.label)}
    {#if item.col === col && !!item.sound === sound}{@render row(item, i)}{/if}
  {/each}
{/snippet}

<div class="overlay" class:clear={creditsOpen}>
  <div class="menu" class:hidden={creditsOpen} bind:this={menu}>
    <h2>{t("overlay.title")}</h2>
    <div class="columns">
      <div class="column">
        {@render column(0)}
        <h3>{t("overlay.sound")}</h3>
        {@render column(0, true)}
      </div>
      {#if cheats}
        <section class="cheats">
          <h3>{t("overlay.cheats")}</h3>
          <div class="cheat-columns">
            <div class="column">{@render column(1)}</div>
            {#if budget}
              <div class="column">
                <h4>{t("overlay.budget")}</h4>
                {@render column(2)}
              </div>
            {/if}
          </div>
        </section>
      {:else if budget}
        <div class="column">
          <h3>{t("overlay.budget")}</h3>
          {#each TOKENS as token (token.name)}
            <p class="row readonly">
              <span>{token.label}</span>
              <span class="value">{game?.jokers_left?.[token.name] ?? "∞"}</span>
            </p>
          {/each}
          {#if choiceLine}<p class="row readonly info">{choiceLine}</p>{/if}
        </div>
      {/if}
      {#if modRows.length}
        <div class="column">
          <h3>{t("overlay.mods")}</h3>
          {@render column(3)}
        </div>
      {/if}
    </div>
    <p class="debug">{t(cheats ? "overlay.keys" : "overlay.keysVolume")} <Prompt action={{ type: "navigate", dir: "left" }} /> <Prompt action={{ type: "navigate", dir: "right" }} /></p>
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
  {#if goToOpen}
    <GoToDialog ongo={ongoto} onclose={() => (goToOpen = false)} />
  {/if}
  {#if settingsOpen && game}
    <GameSettings settings={game.settings} onapply={applySettings} onclose={() => (settingsOpen = false)} />
  {/if}
</div>

<style>
  .overlay {
    position: fixed;
    inset: 0;
    z-index: 40;
    display: grid;
    place-items: center;
    background: var(--dim);
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
    /* Taller than the screen (B-17): scrolls; focus keeps the selected item in view. */
    max-height: calc(100vh - 2 * var(--u));
    overflow-y: auto;
    scrollbar-width: thin;
    scrollbar-color: var(--slate-600) transparent;
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
  h4 {
    margin: 0;
    font-size: calc(1.1 * var(--u));
    font-weight: 700;
    color: var(--slate-400);
  }
  .columns {
    display: flex;
    gap: calc(2 * var(--u));
    align-items: start;
  }
  .column {
    display: flex;
    flex-direction: column;
    gap: calc(0.55 * var(--u));
    width: calc(32 * var(--u));
  }
  /* The cheats, apart from the general part (D-88). */
  .cheats {
    display: flex;
    flex-direction: column;
    gap: calc(0.55 * var(--u));
    margin-top: calc(-0.6 * var(--u));
    padding: calc(0.6 * var(--u)) calc(1.2 * var(--u)) calc(1.2 * var(--u));
    border: calc(0.15 * var(--u)) dashed rgba(255, 183, 3, 0.45);
    border-radius: calc(1.2 * var(--u));
    background: rgba(255, 183, 3, 0.05);
  }
  .cheats h3 {
    margin: 0;
    color: var(--amber);
  }
  .cheat-columns {
    display: flex;
    gap: calc(1.6 * var(--u));
    align-items: start;
  }
  .cheat-columns .column:first-child {
    width: calc(30 * var(--u));
  }
  .cheat-columns .column:last-child {
    width: calc(34 * var(--u));
  }
  button {
    padding: calc(0.5 * var(--u)) calc(1.2 * var(--u));
    border: calc(0.18 * var(--u)) solid transparent;
    border-radius: calc(0.8 * var(--u));
    background: var(--slate-600);
    font-size: calc(1.35 * var(--u));
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
    gap: calc(0.8 * var(--u));
    padding: calc(0.35 * var(--u)) calc(1.2 * var(--u));
    border: calc(0.18 * var(--u)) solid transparent;
    border-radius: calc(0.8 * var(--u));
    background: rgba(43, 54, 80, 0.5);
    font-size: calc(1.2 * var(--u));
    font-weight: 700;
  }
  .volume {
    grid-template-columns: 1fr calc(10 * var(--u)) calc(4.5 * var(--u));
  }
  .joker {
    grid-template-columns: 1fr calc(2.4 * var(--u)) calc(2.4 * var(--u)) calc(2.4 * var(--u)) minmax(calc(6 * var(--u)), auto);
  }
  .pick {
    grid-template-columns: 1fr calc(2.4 * var(--u)) minmax(calc(4 * var(--u)), auto) calc(2.4 * var(--u));
    padding-left: 0;
    background: var(--slate-600);
  }
  .pick.off {
    opacity: 0.35;
  }
  .pick .run {
    border: none;
    background: none;
    font-size: calc(1.35 * var(--u));
  }
  .pick .run:disabled {
    opacity: 1;
  }
  .pick .value {
    text-align: center;
    color: var(--amber);
    white-space: nowrap;
  }
  .lang {
    grid-template-columns: 1fr calc(2.4 * var(--u)) calc(12 * var(--u)) calc(2.4 * var(--u));
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
    white-space: nowrap;
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
