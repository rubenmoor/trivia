<script module lang="ts">
  import { mods as bridge, type ModEntry, type ModList } from "../../lib/desktop.ts";

  /** Ids in this run's overlay, top first: from the first list (Game.svelte at mount), before any change. */
  let runOrder: string[] | null = null;

  /** `mods:list`; null outside the shell. */
  export async function fetchModList(): Promise<ModList | null> {
    if (!bridge) return null;
    const list = await bridge.list();
    runOrder ??= byPosition(list.mods.filter((m) => m.active)).map((m) => m.id ?? "");
    return list;
  }

  const byPosition = (mods: ModEntry[]) => [...mods].sort((a, b) => (a.position ?? 0) - (b.position ?? 0));

  /** In the load order with move controls: everything but invalid and pending rows. */
  export const movable = (m: ModEntry) => m.id !== null && m.position !== null && m.state !== "invalid";

  /** Start screen: mods held off until the notice is accepted. */
  export const heldOff = (list: ModList) => (list.notice ? 0 : list.mods.filter((m) => movable(m) && !m.on).length);
</script>

<script lang="ts">
  // Mods screen (plan 118): load order, on/off, state and warnings per mod; changes go to mods.json at
  // once and apply on restart. ↑/↓ rows, ←/→ to ▲▼, LB/RB move the focused row, Esc/⌫/B back.
  import { tick } from "svelte";
  import { flush } from "../../lib/engine.ts";
  import { endonym, has, t, type Params } from "../../lib/i18n.ts";
  import { focusControl, lastDevice, pushScope, type Action } from "../../lib/input.svelte.ts";
  import { modErrors } from "../../lib/mods.ts";
  import ModsNotice from "../ModsNotice.svelte";
  import Icon from "../Icon.svelte";
  import Prompt from "../Prompt.svelte";

  let { onclose }: { onclose: (list: ModList | null) => void } = $props();

  let list = $state<ModList | null>(null);
  let failed = $state(false);
  let busy = $state(false);
  /** Key of the row whose detail shows. */
  let focused = $state<string | null>(null);
  /** Waits for the notice: runs after «Allow mods». */
  let pending = $state<(() => Promise<void>) | null>(null);
  let panel = $state<HTMLDivElement>();

  const rows = $derived(list ? [...byPosition(list.mods.filter(movable)), ...list.mods.filter((m) => !movable(m))] : []);
  const order = $derived(rows.filter(movable));
  /** Unique per row: a `duplicate_id` row shares its id with the primary. */
  const keyOf = (m: ModEntry) => `${m.source}:${m.publishedFileId ?? m.dir ?? m.id ?? "?"}`;
  const detail = $derived(rows.find((m) => keyOf(m) === focused) ?? null);
  /** Next run's overlay differs from this one's. */
  const dirty = $derived(list !== null && order.filter((m) => m.state === "loaded").map((m) => m.id).join() !== (runOrder ?? []).join());
  const anyOn = $derived(order.some((m) => m.on));

  /** The text of `<prefix>.<code>`; an unknown code shows as itself. */
  function code(prefix: string, c: string, params?: Params): string {
    const key = `${prefix}.${c}`;
    return has(key) ? t(key, params) : c;
  }

  function stateText(m: ModEntry): string {
    if (m.state === "invalid") return t("mods.state.invalid", { reason: m.error ? code("mods.error", m.error.code, { field: m.error.field ?? "" }) : "" });
    if (m.state === "loaded" && !m.active) return t("mods.state.onNext");
    if (m.state === "off" && m.active) return t("mods.state.offNext");
    return code("mods.state", m.state);
  }

  function warnings(m: ModEntry): string[] {
    const page = m.active ? modErrors().filter((e) => e.id === m.id).map((e) => e.code) : [];
    return [...new Set([...m.warnings, ...page])].map((w) => code("mods.warning", w, { version: m.game ?? "" }));
  }

  function nameOf(m: ModEntry): string {
    return m.name ?? m.id ?? m.dir ?? `#${m.publishedFileId ?? ""}`;
  }

  /** The control with `data-focus-id` = `id` gets focus again after the list re-renders; Back if it's gone. */
  async function refocus(id: string | null) {
    await tick();
    const find = (sel: string) => panel?.querySelector<HTMLElement>(`${sel}:not(:disabled)`);
    const el = (id && find(`[data-focus-id="${CSS.escape(id)}"]`)) || find("[data-focus-default]"); // a control that went disabled: Back
    if (el && document.activeElement !== el) focusControl(el);
  }

  async function update(run: () => Promise<ModList>) {
    if (busy) return;
    const at = document.activeElement instanceof HTMLElement ? (document.activeElement.dataset.focusId ?? null) : null;
    busy = true;
    try {
      list = await run();
      failed = false;
    } catch (e) {
      console.error("mods:", e);
      failed = true;
    } finally {
      busy = false;
    }
    await refocus(at);
  }

  const save = (next: ModEntry[]) => update(() => bridge!.set(next.map((m) => ({ id: m.id!, on: m.on }))));

  /** Runs `action` now, or after the notice when it would turn a mod on first. */
  function guarded(on: boolean, action: () => Promise<void>) {
    if (on && list && !list.notice) pending = action;
    else void action();
  }

  async function allow() {
    const action = pending;
    pending = null;
    await update(() => bridge!.notice());
    if (list?.notice) await action?.();
  }

  function toggle(m: ModEntry) {
    if (!movable(m) || busy) return;
    const on = !m.on;
    guarded(on, () => save(order.map((x) => (x.id === m.id ? { ...x, on } : x)))); // `order` may be newer by then
  }

  function move(m: ModEntry, by: 1 | -1) {
    const i = order.indexOf(m);
    const j = i + by;
    if (i < 0 || j < 0 || j >= order.length || busy) return;
    const next = [...order];
    [next[i], next[j]] = [next[j], next[i]];
    void save(next);
  }

  const allOff = () => save(order.map((m) => ({ ...m, on: false })));
  const refresh = () => update(() => bridge!.list());

  async function restart() {
    if (!dirty || busy) return;
    busy = true;
    try {
      await flush();
      await bridge!.restart();
    } catch (e) {
      console.error("mods:restart", e);
      busy = false;
    }
  }

  function handle(a: Action): boolean {
    if (pending) return false;
    if (a.type === "back" || a.type === "menu") onclose(list);
    else if (a.type === "joker-focus") {
      const m = order.find((x) => keyOf(x) === focused);
      if (m) move(m, a.step);
    } else return false;
    return true;
  }

  $effect(() => pushScope({ name: "mods", modal: true, whileBusy: true, root: () => panel, handle }));

  fetchModList().then(
    async (l) => {
      list = l;
      await tick();
      const start = l?.safeStart?.reason === "crashed" ? "all-off" : rows[0] ? `row:${keyOf(rows[0])}` : "back";
      await refocus(start);
    },
    (e) => {
      console.error("mods:list", e);
      failed = true;
    },
  );

  function names(ids: string[]): string {
    return ids.map((id) => list?.mods.find((m) => m.id === id)?.name ?? id).join(", ");
  }
</script>

<div class="mods" bind:this={panel}>
  <header>
    <h2>{t("mods.title")}</h2>
    <p class="keys">
      {#if lastDevice.current === "gamepad"}
        {t("mods.move")} <Prompt action={{ type: "joker-focus", step: -1 }} /> <Prompt action={{ type: "joker-focus", step: 1 }} />
      {:else}
        {t("mods.order")}
      {/if}
    </p>
    <button class="secondary" onclick={refresh} disabled={!list} data-focus-id="refresh"><Icon name="refresh" /> {t("mods.refresh")}</button>
    <button class="secondary" onclick={allOff} disabled={!anyOn} data-focus-id="all-off"><Icon name="power" /> {t("mods.allOff")}</button>
    <button class="candy" onclick={() => guarded(anyOn, restart)} disabled={!dirty} data-focus-id="restart"><Icon name="rocket" /> {t("mods.restart")}</button>
    <button class="secondary" onclick={() => onclose(list)} data-focus-id="back" data-focus-default><Icon name="back" /> {t("action.back")} <Prompt action="menu" pad="back" /></button>
  </header>

  {#if list?.safeStart?.reason === "crashed"}
    <p class="line warn">{list.safeStart.mods.length ? t("mods.crashed", { mods: names(list.safeStart.mods) }) : t("mods.crashedUnknown")}</p>
  {:else if list?.safeStart?.reason === "flag"}
    <p class="line">{t("mods.flag")}</p>
  {/if}
  {#if list && !list.validUser}<p class="line">{t("mods.noUser")}</p>{/if}
  {#if failed}<p class="line warn">{t("mods.failed")}</p>{/if}

  {#if !list}
    <p class="line">{failed ? "" : t("mods.loading")}</p>
  {:else if !rows.length}
    <p class="line">{t("mods.empty")}</p>
  {:else}
    <div class="body">
      <ol class="list">
        {#each rows as m (keyOf(m))}
          {@const key = keyOf(m)}
          {@const can = movable(m)}
          {@const i = order.indexOf(m)}
          <li class:on={m.on} class:focused={focused === key} onfocusin={() => (focused = key)}>
            <button
              class="row"
              class:inert={!can}
              aria-disabled={!can}
              aria-pressed={can ? m.on : undefined}
              aria-label={can ? `${nameOf(m)}: ${t(m.on ? "mods.turnOff" : "mods.turnOn")}` : undefined}
              data-focus-id="row:{key}"
              onclick={() => toggle(m)}
            >
              <span class="switch" aria-hidden="true"><span></span></span>
              <span class="main">
                <span class="head">
                  <Icon name="puzzle" />
                  <b>{nameOf(m)}</b>
                  {#if m.version}<span class="version">{m.version}</span>{/if}
                  {#each m.kind as k (k)}<span class="badge">{code("mods.kind", k)}</span>{/each}
                </span>
                <span class="meta">
                  {m.source === "local" ? t("mods.local") : t("mods.workshop", { id: m.publishedFileId ?? "" })} ·
                  {m.languages.length ? m.languages.map((l) => endonym(l)).join(", ") : t("mods.allLanguages")}
                </span>
                <span class="state" class:bad={m.state === "invalid"}>{stateText(m)}</span>
                {#each warnings(m) as w (w)}<span class="warning">{w}</span>{/each}
              </span>
              {#if focused === key && can}<Prompt action="confirm" />{/if}
            </button>
            {#if can}
              <button class="step" aria-label={t("mods.up")} aria-disabled={i === 0} data-focus-id="up:{key}" onclick={() => move(m, -1)}>▲</button>
              <button class="step" aria-label={t("mods.down")} aria-disabled={i === order.length - 1} data-focus-id="down:{key}" onclick={() => move(m, 1)}>▼</button>
            {/if}
          </li>
        {/each}
      </ol>
      <aside class="detail">
        {#if detail}
          <h3>{nameOf(detail)}</h3>
          {#if detail.description}<p>{detail.description}</p>{/if}
          {#if detail.source === "local" && detail.dir}<p class="folder">{t("mods.folder", { dir: detail.dir })}</p>{/if}
        {/if}
      </aside>
    </div>
  {/if}
</div>

{#if pending}
  <ModsNotice onallow={allow} oncancel={() => (pending = null)} />
{/if}

<style>
  .mods {
    position: fixed;
    inset: 0;
    z-index: 45;
    display: flex;
    flex-direction: column;
    gap: calc(1 * var(--u));
    padding: var(--safe-y) var(--safe-x);
    background: var(--glass-strong);
    backdrop-filter: blur(calc(0.6 * var(--u))) saturate(1.2);
  }
  header {
    display: flex;
    align-items: center;
    gap: calc(1.2 * var(--u));
  }
  h2 {
    margin: 0;
    font-family: var(--font-display);
    font-size: calc(2.6 * var(--u));
    font-weight: 800;
  }
  .keys {
    flex: 1;
    margin: 0;
    font-size: calc(1.1 * var(--u));
    color: var(--slate-400);
  }
  .line {
    margin: 0;
    font-size: calc(1.25 * var(--u));
    color: var(--slate-200);
  }
  .warn {
    color: var(--amber);
  }
  .body {
    display: grid;
    grid-template-columns: 2fr 1fr;
    gap: calc(2 * var(--u));
    flex: 1;
    min-height: 0;
  }
  .list {
    margin: 0;
    padding: 0 calc(1 * var(--u)) 0 0;
    overflow-y: auto;
    list-style: none;
    scrollbar-width: thin;
    scrollbar-color: var(--slate-600) transparent;
  }
  li {
    display: grid;
    grid-template-columns: 1fr calc(3 * var(--u)) calc(3 * var(--u));
    gap: calc(0.6 * var(--u));
    align-items: center;
    margin: calc(0.5 * var(--u)) calc(0.3 * var(--u));
  }
  .row {
    grid-column: 1;
    display: flex;
    align-items: center;
    gap: calc(1.2 * var(--u));
    min-width: 0;
    padding: calc(0.7 * var(--u)) calc(1.2 * var(--u));
    border: calc(0.18 * var(--u)) solid transparent;
    border-radius: calc(0.8 * var(--u));
    background: rgba(43, 54, 80, 0.6);
    text-align: left;
  }
  li.focused .row {
    border-color: var(--slate-400);
  }
  .row.inert {
    opacity: 0.75;
  }
  .switch {
    flex: none;
    width: calc(3.2 * var(--u));
    height: calc(1.8 * var(--u));
    padding: calc(0.2 * var(--u));
    border-radius: calc(1 * var(--u));
    background: var(--slate-600);
  }
  .switch span {
    display: block;
    width: calc(1.4 * var(--u));
    height: calc(1.4 * var(--u));
    border-radius: 50%;
    background: var(--slate-400);
    transition: transform 0.15s;
  }
  li.on .switch {
    background: var(--amber);
  }
  li.on .switch span {
    background: var(--paper);
    transform: translateX(calc(1.4 * var(--u)));
  }
  .main {
    display: flex;
    flex: 1;
    flex-direction: column;
    gap: calc(0.2 * var(--u));
    min-width: 0;
  }
  .head {
    display: flex;
    flex-wrap: wrap;
    gap: calc(0.6 * var(--u));
    align-items: baseline;
    font-size: calc(1.4 * var(--u));
  }
  .head b {
    overflow: hidden;
    max-width: 100%;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
  .version {
    font-size: calc(1.05 * var(--u));
    color: var(--slate-400);
  }
  .badge {
    padding: 0 calc(0.5 * var(--u));
    border-radius: calc(0.4 * var(--u));
    background: var(--slate-600);
    font-size: calc(0.95 * var(--u));
    font-weight: 700;
  }
  .meta,
  .state {
    font-size: calc(1.05 * var(--u));
    font-weight: 500;
    color: var(--slate-200);
  }
  .state.bad,
  .warning {
    font-size: calc(1.05 * var(--u));
    font-weight: 500;
    color: var(--amber);
  }
  .step {
    width: calc(3 * var(--u));
    height: calc(3 * var(--u));
    padding: 0;
    border: calc(0.18 * var(--u)) solid transparent;
    border-radius: calc(0.6 * var(--u));
    background: var(--slate-600);
    font-size: calc(1.2 * var(--u));
  }
  .step[aria-disabled="true"] {
    opacity: 0.35;
  }
  .detail {
    overflow-y: auto;
    font-size: calc(1.2 * var(--u));
    line-height: 1.4;
    color: var(--slate-200);
    overflow-wrap: anywhere;
  }
  .detail h3 {
    margin: 0 0 calc(0.6 * var(--u));
    font-family: var(--font-display);
    font-size: calc(1.6 * var(--u));
    color: var(--paper);
  }
  .detail p {
    margin: 0 0 calc(0.6 * var(--u));
  }
  .folder {
    font-family: monospace;
    color: var(--slate-400);
  }
</style>
