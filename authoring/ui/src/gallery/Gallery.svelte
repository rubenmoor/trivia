<script lang="ts">
  // Screen gallery (plan 100): trivia-gallery's shots per UI language with each text's catalog key;
  // the developer flags strings with a note for the next fix pass (authoring/data/ui-flags.json).
  import { onMount } from "svelte";
  import { messageOf } from "$app/lib/http.ts";
  import { changeUiFlag, fetchGallery } from "../lib/api.ts";
  import Nav from "../lib/Nav.svelte";
  import type { GalleryItem, GalleryManifest, UiFlag } from "../lib/types.ts";

  // Viewport of a locale entry: `es@1280x800`, else 1920 × 1080.
  const sizeOf = (l: string): [number, number] => {
    const m = /@(\d+)x(\d+)$/.exec(l);
    return m ? [Number(m[1]), Number(m[2])] : [1920, 1080];
  };

  let manifest = $state<GalleryManifest | null>(null);
  let flags = $state<UiFlag[]>([]);
  let loaded = $state(false);
  let error = $state<string | null>(null);
  let showFixed = $state(false);

  const params = new URLSearchParams(location.search);
  const set = params.get("set");
  let locale = $state(params.get("locale") ?? "");
  const [W, H] = $derived(sizeOf(locale));
  let shot = $state(params.get("shot") ?? "");
  let selected = $state<GalleryItem | null>(null);
  let key = $state<string | null>(null);
  let note = $state("");
  let editing = $state<number | null>(null);
  let editNote = $state("");

  onMount(async () => {
    try {
      ({ manifest, flags } = await fetchGallery(set));
      const locales = Object.keys(manifest?.locales ?? {});
      if (!locales.includes(locale)) locale = locales[0] ?? "";
      if (!shots.includes(shot)) shot = shots[0] ?? "";
    } catch (e) {
      error = messageOf(e);
    }
    loaded = true;
  });

  const shots = $derived(Object.keys(manifest?.locales[locale] ?? {}));
  const current = $derived(manifest?.locales[locale]?.[shot] ?? null);
  // Biggest first, so smaller boxes on top stay clickable.
  const boxes = $derived((current?.items ?? []).filter((it) => !it.attr).sort((a, b) => b.box[2] * b.box[3] - a.box[2] * a.box[3]));
  // A review set: only its shots' flags.
  const inSet = (f: UiFlag) => !manifest?.shots || manifest.shots.includes(f.shot);
  const visible = $derived(flags.filter((f) => f.locale === locale && inSet(f) && (showFixed || !f.fixed_on)));
  const openCount = (l: string, s?: string) =>
    flags.filter((f) => f.locale === l && inSet(f) && !f.fixed_on && (!s || f.shot === s)).length;
  const link = (l: string, s: string) => `/gallery?${new URLSearchParams({ ...(set ? { set } : {}), locale: l, shot: s })}`;
  const flagsOf = (it: GalleryItem) => visible.filter((f) => f.shot === shot && f.text === it.text);

  function go(l: string, s: string) {
    locale = l;
    shot = manifest?.locales[l]?.[s] ? s : (Object.keys(manifest?.locales[l] ?? {})[0] ?? "");
    selected = null;
    history.replaceState(null, "", link(locale, shot));
  }

  function move(delta: number) {
    if (!shots.length) return;
    go(locale, shots[(shots.indexOf(shot) + delta + shots.length) % shots.length]);
    requestAnimationFrame(() => document.querySelector(".shots a.on")?.scrollIntoView({ block: "nearest" }));
  }

  const steps: Record<string, number> = { ArrowDown: 1, ArrowRight: 1, ArrowUp: -1, ArrowLeft: -1 };

  function onKey(e: KeyboardEvent) {
    const delta = steps[e.key];
    if (!delta || e.ctrlKey || e.metaKey || e.altKey || (e.target as Element).closest?.("input, textarea, select")) return;
    e.preventDefault();
    move(delta);
  }

  function pick(it: GalleryItem) {
    selected = it;
    key = it.keys?.[0] ?? null;
    note = "";
  }

  async function save(body: Parameters<typeof changeUiFlag>[0]) {
    try {
      flags = await changeUiFlag(body);
      error = null;
      return true;
    } catch (e) {
      error = messageOf(e);
      return false;
    }
  }

  async function add(e: SubmitEvent) {
    e.preventDefault();
    if (selected && (await save({ flag: { locale, key, text: selected.text, shot, note } }))) note = "";
  }

  async function saveEdit(id: number) {
    if (await save({ id, note: editNote })) editing = null;
  }

  const kind = (it: GalleryItem) =>
    it.attr ? it.attr : it.keys ? (it.unmatched ? "partly keyed" : "") : it.glyph ? "glyph" : it.data ? "content" : "no key";
  const style = (b: GalleryItem["box"]) =>
    `left:${(b[0] / W) * 100}%;top:${(b[1] / H) * 100}%;width:${(b[2] / W) * 100}%;height:${(b[3] / H) * 100}%`;
</script>

<svelte:window onkeydown={onKey} />

<svelte:head><title>Screen gallery · Trivia authoring</title></svelte:head>

<main>
  <Nav current="gallery" />
  <h1>Screen gallery</h1>

  {#if error}<p class="error">{error}</p>{/if}
  {#if !loaded}
    <p class="muted">Loading…</p>
  {:else if set && !manifest}
    <!-- a missing set: the error above, not the full gallery -->
  {:else if !manifest}
    <p>No gallery yet: run <code>trivia-gallery</code> (every screen in every UI language, ~15 min), then reload.</p>
  {:else}
    {#if manifest.name}
      <h2>Review set {manifest.name}</h2>
      {#if manifest.note}<p>{manifest.note}</p>{/if}
      <p class="muted small">{manifest.shots?.length} shots × {Object.keys(manifest.locales).length} entries. <a href="/gallery">Full gallery</a></p>
    {/if}
    <p class="muted small">
      Run {manifest.run.replace("T", " ")} at {manifest.commit}. Click a text to see its catalog key and flag it; a fix pass
      reads the flags. Arrow keys step through the shots. Re-run <code>trivia-gallery</code> for fresh shots.
    </p>
    <div class="locales">
      {#each Object.keys(manifest.locales) as l (l)}
        <button class:on={l === locale} onclick={() => go(l, shot)}>{l}{#if openCount(l)} <b>{openCount(l)}</b>{/if}</button>
      {/each}
      <label class="small"><input type="checkbox" bind:checked={showFixed} /> show fixed flags</label>
    </div>

    <div class="layout">
      <ul class="shots">
        {#each shots as s (s)}
          <li>
            <a href={link(locale, s)} class:on={s === shot}
              onclick={(e) => { e.preventDefault(); go(locale, s); }}
              >{s}{#if openCount(locale, s)} <b>{openCount(locale, s)}</b>{/if}</a
            >
          </li>
        {/each}
      </ul>

      {#if current}
        <section class="view">
          <div class="shot">
            <img src="/gallery/{current.file}" alt={shot} />
            {#each boxes as it, i (i)}
              <button
                class="box"
                class:keyed={it.keys}
                class:loose={!it.keys && !it.data && !it.glyph}
                class:flagged={flagsOf(it).length}
                class:sel={selected === it}
                style={style(it.box)}
                title="{it.keys?.join(', ') ?? kind(it)}: {it.text}"
                onclick={() => pick(it)}
                aria-label={it.text}
              ></button>
            {/each}
          </div>

          <div class="below">
            <div class="panel">
              {#if selected}
                <p class="text">«{selected.text}»</p>
                <p class="small">
                  {#if selected.keys}<code>{selected.keys.join(" · ")}</code>{/if}
                  {#if kind(selected)}<span class="muted">{kind(selected)}</span>{/if}
                  {#if selected.unmatched}<span class="warn">without key: «{selected.unmatched}»</span>{/if}
                </p>
                <form onsubmit={add}>
                  {#if (selected.keys?.length ?? 0) > 1}
                    <select bind:value={key}>
                      {#each selected.keys ?? [] as k (k)}<option value={k}>{k}</option>{/each}
                    </select>
                  {/if}
                  <input bind:value={note} placeholder="What's wrong? (note for the fix pass)" />
                  <button class="primary" disabled={!note.trim()}>Flag</button>
                </form>
              {:else}
                <p class="muted small">Click a box on the shot. Green: catalog key; red: text without a key; grey: content, glyphs.</p>
              {/if}
            </div>

            {#if current.items.some((it) => it.attr)}
              <div class="panel">
                <h3>Not visible (aria-label, title, placeholder)</h3>
                <ul class="plain">
                  {#each current.items.filter((it) => it.attr) as it, i (i)}
                    <li><button class="link" class:sel={selected === it} onclick={() => pick(it)}>«{it.text}»</button>
                      <span class="muted small">{it.attr} · {it.keys?.join(", ") ?? "no key"}</span></li>
                  {/each}
                </ul>
              </div>
            {/if}

            {#if current.unmatched.length}
              <div class="panel">
                <h3 class="warn">Text without a catalog key</h3>
                <ul class="plain">{#each current.unmatched as u (u)}<li>«{u}»</li>{/each}</ul>
              </div>
            {/if}
          </div>
        </section>
      {/if}
    </div>

    <section class="panel">
      <h2>{showFixed ? "Flags" : "Open flags"} in {locale} ({visible.length})</h2>
      {#if visible.length}
        <table>
          <tbody>
            {#each visible as f (f.id)}
              <tr class:fixed={f.fixed_on}>
                <td><a href={link(locale, f.shot)}
                    onclick={(e) => { e.preventDefault(); go(locale, f.shot); }}>{f.shot}</a></td>
                <td><code>{f.key ?? "no key"}</code><br /><span class="small">«{f.text}»</span></td>
                <td class="note">
                  {#if editing === f.id}
                    <form onsubmit={(e) => { e.preventDefault(); saveEdit(f.id); }}>
                      <input bind:value={editNote} />
                      <button class="primary" disabled={!editNote.trim()}>Save</button>
                      <button type="button" onclick={() => (editing = null)}>Cancel</button>
                    </form>
                  {:else}
                    {f.note}
                  {/if}
                </td>
                <td class="muted small">{f.flagged_on}{#if f.fixed_on}<br />fixed {f.fixed_on}{/if}</td>
                <td class="actions">
                  {#if editing !== f.id}
                    <button onclick={() => { editing = f.id; editNote = f.note; }}>Edit</button>
                    <button onclick={() => save({ id: f.id, remove: true })}>Remove</button>
                  {/if}
                </td>
              </tr>
            {/each}
          </tbody>
        </table>
      {:else}
        <p class="muted small">None.</p>
      {/if}
    </section>
  {/if}
</main>

<style>
  main {
    max-width: 1500px;
    margin: 0 auto;
    padding: 1.5rem 1rem 4rem;
  }
  h1 {
    margin: 0 0 0.5rem;
    font-size: 1.5rem;
  }
  h2,
  h3 {
    margin: 0 0 0.5rem;
    font-size: 1rem;
  }
  .small {
    font-size: 0.85rem;
  }
  .error {
    color: var(--bad);
  }
  .warn {
    color: var(--warn);
  }
  code {
    padding: 0.05rem 0.3rem;
    border-radius: 4px;
    background: var(--field);
    font-size: 0.85em;
  }
  a {
    color: var(--text);
  }
  b {
    color: var(--bad);
  }
  button,
  input,
  select {
    padding: 0.3rem 0.7rem;
    border: 1px solid var(--border);
    border-radius: 6px;
    background: var(--field);
    color: var(--text);
    font: inherit;
  }
  button {
    cursor: pointer;
  }
  button.on,
  button.primary {
    border-color: var(--accent);
    background: var(--accent);
    color: #1a1b22;
    font-weight: 600;
  }
  button:disabled {
    opacity: 0.4;
    cursor: default;
  }
  button.on b {
    color: #8a1c1c;
  }
  .locales {
    display: flex;
    gap: 0.5rem;
    align-items: center;
    margin: 0.75rem 0 1rem;
  }
  .locales label {
    margin-left: 1rem;
  }
  .layout {
    display: grid;
    grid-template-columns: 13rem minmax(0, 1fr);
    gap: 1rem;
    margin-bottom: 1.5rem;
  }
  .shots {
    list-style: none;
    margin: 0;
    padding: 0;
    font-size: 0.85rem;
    max-height: 80vh;
    overflow-y: auto;
  }
  .shots a {
    display: block;
    padding: 0.15rem 0.5rem;
    border-radius: 4px;
    color: var(--muted);
    text-decoration: none;
  }
  .shots a.on {
    background: var(--panel);
    color: var(--text);
  }
  .shot {
    position: relative;
    line-height: 0;
  }
  .shot img {
    width: 100%;
    border-radius: 6px;
  }
  .box {
    position: absolute;
    padding: 0;
    border: 1px solid rgb(154 156 171 / 0.35);
    border-radius: 2px;
    background: transparent;
  }
  .box.keyed {
    border-color: rgb(62 207 142 / 0.55);
  }
  .box.loose {
    border-color: var(--bad);
  }
  .box:hover {
    background: rgb(255 201 74 / 0.2);
  }
  .box.flagged {
    border: 2px solid var(--warn);
    background: rgb(255 169 77 / 0.25);
  }
  .box.sel {
    border: 2px solid var(--accent);
  }
  .below {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(20rem, 1fr));
    gap: 1rem;
    margin-top: 1rem;
  }
  .panel {
    background: var(--panel);
    border-radius: 12px;
    padding: 0.9rem 1.1rem;
  }
  section.panel {
    margin-bottom: 1.5rem;
  }
  .panel p {
    margin: 0.3rem 0;
  }
  .text {
    font-size: 1.1rem;
  }
  form {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-top: 0.5rem;
  }
  form input {
    flex: 1;
    min-width: 12rem;
  }
  .plain {
    margin: 0;
    padding-left: 1.1rem;
    font-size: 0.9rem;
  }
  .link {
    padding: 0;
    border: 0;
    background: none;
    text-align: left;
  }
  .link.sel {
    color: var(--accent);
  }
  table {
    border-collapse: collapse;
    width: 100%;
    font-size: 0.9rem;
  }
  td {
    padding: 0.4rem 0.75rem 0.4rem 0;
    border-bottom: 1px solid var(--line);
    vertical-align: top;
  }
  td.note {
    width: 45%;
  }
  td.actions {
    white-space: nowrap;
  }
  tr.fixed {
    opacity: 0.55;
  }
</style>
