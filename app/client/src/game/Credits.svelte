<script module lang="ts">
  import type { Credits } from "../lib/types.ts";

  /** Loaded on first open, kept for the session; a failure tries again next time. */
  let cached: Promise<Credits> | null = null;

  function load(): Promise<Credits> {
    cached ??= fetch("credits.json").then((r) => (r.ok ? (r.json() as Promise<Credits>) : Promise.reject(new Error(String(r.status)))));
    cached.catch(() => (cached = null));
    return cached;
  }
</script>

<script lang="ts">
  // Credits (PUB-5, plan 47): credits.json from the build, over the overlay. Read-only, no focusable
  // rows: ↑/↓ scroll ~70 %, ←/→ jump between sections, Esc/⌫ go back.
  import { fetchModCredits } from "../lib/api.ts";
  import { buildInfo } from "../lib/build.ts";
  import { t } from "../lib/i18n.ts";
  import { focusControl, pushScope, type Action } from "../lib/input.svelte.ts";
  import Icon from "./Icon.svelte";
  import Prompt from "./Prompt.svelte";

  let { onclose }: { onclose: () => void } = $props();

  const build = buildInfo();
  let credits = $state<Credits | null>(null);
  let failed = $state(false);
  let scroller = $state<HTMLDivElement>();
  let panel = $state<HTMLDivElement>();
  let backButton = $state<HTMLButtonElement>();

  load().then(
    (c) => (credits = c),
    () => (failed = true),
  );
  /** Mod bundles' media (decision 129), after ours. */
  const modCredits = fetchModCredits().catch(() => []);

  function jump(step: 1 | -1) {
    const box = scroller;
    if (!box) return;
    const tops = [...box.querySelectorAll<HTMLElement>("section")].map((s) => s.offsetTop);
    const at = box.scrollTop + 1;
    const target = step > 0 ? tops.find((top) => top > at) : tops.filter((top) => top < at - 1).at(-1);
    box.scrollTo({ top: target ?? (step > 0 ? box.scrollHeight : 0), behavior: "smooth" });
  }

  function handle(a: Action): boolean {
    if (a.type === "back" || a.type === "menu") onclose();
    else if (a.type === "navigate" && (a.dir === "up" || a.dir === "down"))
      scroller?.scrollBy({ top: (a.dir === "down" ? 0.7 : -0.7) * scroller.clientHeight, behavior: "smooth" });
    else if (a.type === "navigate") jump(a.dir === "right" ? 1 : -1);
    else return false;
    return true;
  }

  $effect(() => {
    const pop = pushScope({ name: "credits", modal: true, whileBusy: true, root: () => panel, handle });
    focusControl(backButton);
    return pop;
  });
</script>

{#snippet row(title: string, by: string, licence: string, note: string | null, url: string | null)}
  <li>
    <p class="line"><b>{title}</b><span>{by}</span><span class="licence">{licence}</span><span class="note">{note ?? ""}</span></p>
    {#if url}<p class="url">{url}</p>{/if}
  </li>
{/snippet}

<div class="credits" bind:this={panel}>
  <header>
    <h2>{t("credits.title")}</h2>
    <p class="build">{[t("credits.version", { version: build.version }), build.pool && t("credits.pool", { pool: build.pool })].filter(Boolean).join(" · ")}</p>
    <p class="keys">
      {t("credits.scroll")} <Prompt action={{ type: "navigate", dir: "up" }} /> <Prompt action={{ type: "navigate", dir: "down" }} />
      · {t("credits.jump")} <Prompt action={{ type: "navigate", dir: "left" }} /> <Prompt action={{ type: "navigate", dir: "right" }} />
    </p>
    <button class="candy" bind:this={backButton} onclick={onclose} data-focus-default><Icon name="back" /> {t("action.back")} <Prompt action="menu" pad="back" /></button>
  </header>
  <div class="scroller" bind:this={scroller}>
    {#if failed}
      <p class="hint">{t("credits.failed")}</p>
    {:else if !credits}
      <p class="hint">{t("credits.loading")}</p>
    {:else}
      {#if credits.game.length}
        <section>
          <h3>{t("credits.game")} <small>{credits.game.length}</small></h3>
          <ul>
            {#each credits.game as g (g.file)}{@render row(g.file, g.title, "", null, null)}{/each}
          </ul>
        </section>
      {/if}
      <section>
        <h3>{t("credits.media")} <small>{credits.media.length}</small></h3>
        <ul>
          {#each credits.media as m, i (i)}
            {@render row(m.title, m.author ?? t("credits.unknownAuthor"), m.license, [t(`credits.${m.kind}`), m.provider].filter(Boolean).join(" · "), m.source_url)}
          {/each}
        </ul>
      </section>
      <section>
        <h3>{t("credits.sounds")} <small>{credits.sounds.entries.length}</small></h3>
        <ul>
          {#each credits.sounds.entries as s (s.file)}
            {@render row(s.used_for, s.author, s.license, s.source, s.source_url)}
          {/each}
        </ul>
        <p class="hint">{credits.sounds.note}</p>
      </section>
      <section>
        <h3>{t("credits.fonts")} <small>{credits.fonts.length}</small></h3>
        <ul>
          {#each credits.fonts as f (f.name)}{@render row(f.name, "", f.license, null, f.license_file)}{/each}
        </ul>
      </section>
      {#if credits.glyphs}
        <section>
          <h3>{t("credits.glyphs")}</h3>
          <p class="hint">{t("credits.glyphsText")}</p>
        </section>
      {/if}
      {#if credits.achievements}
        <section>
          <h3>{t("credits.achievements")}</h3>
          <p class="hint">{t("credits.glyphsText")}</p>
        </section>
      {/if}
      <section>
        <h3>{t("credits.libraries")} <small>{credits.libraries.length}</small></h3>
        <ul>
          {#each credits.libraries as l (l.name)}{@render row(`${l.name} ${l.version}`, "", l.license, null, l.url)}{/each}
        </ul>
      </section>
      {#await modCredits then mods}
        {#each mods as m (m.bundle)}
          <section>
            <h3>{t("credits.playerMade", { mod: m.mod })} · {m.name} <small>{m.items.length}</small></h3>
            <ul>
              {#each m.items as c, i (i)}{@render row(c.credit ?? t("credits.unknownAuthor"), "", "", null, c.url)}{/each}
            </ul>
          </section>
        {/each}
      {/await}
    {/if}
  </div>
</div>

<style>
  .credits {
    position: fixed;
    inset: 0;
    z-index: 45;
    display: flex;
    flex-direction: column;
    gap: calc(1.2 * var(--u));
    padding: var(--safe-y) var(--safe-x);
    background: var(--glass-strong);
    backdrop-filter: blur(calc(0.6 * var(--u))) saturate(1.2);
  }
  header {
    display: flex;
    align-items: center;
    gap: calc(2 * var(--u));
  }
  h2 {
    margin: 0;
    font-family: var(--font-display);
    font-size: calc(2.6 * var(--u));
    font-weight: 800;
  }
  .build {
    font-size: calc(1.1 * var(--u));
    color: var(--slate-400);
    font-variant-numeric: tabular-nums;
  }
  .keys {
    flex: 1;
    margin: 0;
    font-size: calc(1.1 * var(--u));
    color: var(--slate-400);
  }
  .scroller {
    position: relative;
    flex: 1;
    overflow-y: auto;
    padding-right: calc(1 * var(--u));
  }
  section {
    margin-bottom: calc(2 * var(--u));
  }
  h3 {
    position: sticky;
    top: 0;
    z-index: 1;
    margin: 0 0 calc(0.6 * var(--u));
    padding: calc(0.4 * var(--u)) 0;
    background: var(--night-700);
    font-family: var(--font-display);
    font-size: calc(1.6 * var(--u));
    font-weight: 700;
  }
  h3 small {
    font-size: calc(1.1 * var(--u));
    color: var(--slate-400);
  }
  ul {
    margin: 0;
    padding: 0;
    list-style: none;
  }
  li {
    padding: calc(0.35 * var(--u)) 0;
    border-bottom: 1px solid var(--glass-line);
    content-visibility: auto;
    contain-intrinsic-size: auto calc(3.2 * var(--u));
  }
  p {
    margin: 0;
  }
  .line {
    display: grid;
    grid-template-columns: 2fr 1.4fr 1fr 1fr;
    gap: calc(1 * var(--u));
    font-size: calc(1.15 * var(--u));
  }
  .line > * {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
  .licence {
    color: var(--amber);
  }
  .note {
    color: var(--slate-400);
  }
  .url {
    overflow: hidden;
    font-size: calc(0.9 * var(--u));
    color: var(--slate-400);
    text-overflow: ellipsis;
    white-space: nowrap;
  }
  .hint {
    font-size: calc(1.15 * var(--u));
    color: var(--slate-200);
  }
</style>
