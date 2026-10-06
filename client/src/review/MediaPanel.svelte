<script lang="ts">
  // One media slot (the question's media, or the background of an audio question, D-14):
  // what is picked or suggested, plus the Commons alternatives (plans/06-images.md).
  import type { MediaCandidate } from "../lib/types";

  interface Slot {
    type: "image" | "audio" | "video";
    query: string;
    note?: string | null;
    source_url: string | null;
    file_url: string | null;
    credit: string | null;
  }

  let {
    title,
    slot,
    decorative,
    candidates,
    showCandidates,
    toggleKey,
    working,
  }: {
    title: string;
    slot: Slot;
    /** Decorative images get the blurred "?" overlay, as on the TV (D-15). */
    decorative: boolean;
    candidates: MediaCandidate[] | null;
    showCandidates: boolean;
    toggleKey: string;
    working: boolean;
  } = $props();

  /** Shown when nothing is picked yet; approving picks it. */
  const suggestion = $derived(!slot.file_url ? (candidates?.[0] ?? null) : null);

  /** Served from the local cache (D-17); a re-pick has another URL, so the browser cache can't go stale. */
  const fileUrl = $derived(slot.file_url ? `/media?url=${encodeURIComponent(slot.file_url)}` : "");

  function chosen(c: MediaCandidate) {
    return c.page_url === slot.source_url;
  }

  function size(c: MediaCandidate) {
    if (c.type === "audio") return c.duration ? `${Math.round(c.duration)} s` : "";
    return c.width ? `${c.width}×${c.height}` : "";
  }
</script>

{#snippet preview(c: MediaCandidate)}
  {#if c.type === "image"}
    <img src={c.preview_url} alt={c.title} loading="lazy" />
  {:else if c.type === "audio"}
    <audio controls preload="none" src={c.file_url}></audio>
  {:else}
    <!-- svelte-ignore a11y_media_has_caption -->
    <video controls preload="none" poster={c.preview_url ?? undefined} src={c.file_url}></video>
  {/if}
{/snippet}

<section class="media">
  <div class="chosen">
    <h2>{title}</h2>
    {#if slot.file_url}
      {#if slot.type === "image"}
        <div class="frame" class:decorative>
          <img src={fileUrl} alt={slot.query} />
          {#if decorative}<span class="mark" aria-hidden="true">?</span>{/if}
        </div>
      {:else if slot.type === "audio"}
        <audio controls src={fileUrl}></audio>
      {:else}
        <!-- svelte-ignore a11y_media_has_caption -->
        <video controls src={fileUrl}></video>
      {/if}
      {#if slot.credit}<p class="credit">{slot.credit}</p>{/if}
    {:else if suggestion}
      {#if suggestion.type === "image"}
        <div class="frame" class:decorative>
          {@render preview(suggestion)}
          {#if decorative}<span class="mark" aria-hidden="true">?</span>{/if}
        </div>
      {:else}
        {@render preview(suggestion)}
      {/if}
      <p class="credit">
        Suggestion · {[suggestion.author, suggestion.license].filter(Boolean).join(" · ")} · approving picks it
      </p>
    {:else}
      <p class="muted">Nothing picked yet.</p>
    {/if}
    <p class="muted">Search: “{slot.query}”</p>
    {#if slot.note}<p class="muted">{slot.note}</p>{/if}
    {#if working}<p class="working">Working…</p>{/if}
  </div>

  <div class="candidates">
    <h2>Alternatives from Wikimedia Commons</h2>
    {#if !showCandidates}
      <p class="muted">
        {#if candidates === null}Not fetched yet. Press <kbd>{toggleKey}</kbd>, then <kbd>m</kbd> to search.
        {:else if candidates.length === 0}Nothing found. Press <kbd>{toggleKey}</kbd>, then <kbd>m</kbd> to try another search term.
        {:else}{candidates.length} candidates · <kbd>{toggleKey}</kbd> to show alternatives{/if}
      </p>
    {:else if candidates === null}
      <p class="muted">Not fetched yet. Press <kbd>m</kbd> to search.</p>
    {:else if candidates.length === 0}
      <p class="muted">Nothing found. Press <kbd>m</kbd> to try another search term.</p>
    {:else}
      <ol>
        {#each candidates as c, i}
          <li class:picked={chosen(c)}>
            <span class="key">{i + 1}{chosen(c) ? " ✓ picked" : ""}</span>
            {@render preview(c)}
            <a class="info" href={c.page_url} target="_blank" rel="noreferrer">
              {c.type} · {size(c)} · {c.license ?? "?"}<br />{c.title.replace(/^File:/, "")}
            </a>
          </li>
        {/each}
      </ol>
      <p class="muted">Press <kbd>1</kbd>–<kbd>{candidates.length}</kbd> to pick · <kbd>m</kbd> new search term · <kbd>Esc</kbd> close</p>
    {/if}
  </div>
</section>

<style>
  .media {
    display: grid;
    grid-template-columns: minmax(0, 2fr) minmax(0, 3fr);
    gap: 2rem;
    margin-top: 1.5rem;
  }
  h2 {
    margin: 0 0 0.4rem;
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--muted);
  }
  img, video {
    display: block;
    width: 100%;
    border-radius: 8px;
  }
  audio {
    width: 100%;
  }
  /* TV look for decorative images (D-15): blurred, darkened, big "?". Hover shows it sharp. */
  .frame {
    position: relative;
    overflow: hidden;
    border-radius: 8px;
  }
  .frame.decorative img {
    filter: blur(6px) brightness(0.7);
    transform: scale(1.05); /* hides the blurred edges */
    transition: filter 0.2s;
  }
  .mark {
    position: absolute;
    inset: 0;
    display: grid;
    place-items: center;
    font-size: clamp(4rem, 12vw, 9rem);
    font-weight: 800;
    color: rgb(255 255 255 / 0.85);
    text-shadow: 0 4px 24px rgb(0 0 0 / 0.6);
    pointer-events: none;
    transition: opacity 0.2s;
  }
  .frame.decorative:hover img {
    filter: none;
    transform: none;
  }
  .frame.decorative:hover .mark {
    opacity: 0;
  }
  .credit {
    margin: 0.3rem 0 0;
    font-size: 0.8rem;
    color: var(--muted);
  }
  .muted {
    color: var(--muted);
  }
  .working {
    color: var(--accent);
  }
  ol {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 0.8rem;
    margin: 0;
    padding: 0;
    list-style: none;
  }
  li {
    position: relative;
    min-width: 0;
    padding: 0.4rem;
    border-radius: 10px;
    background: var(--panel);
    border: 2px solid transparent;
  }
  li.picked {
    border-color: var(--good);
  }
  li img, li video {
    aspect-ratio: 16 / 10;
    object-fit: cover;
  }
  .key {
    position: absolute;
    top: 0.6rem;
    left: 0.6rem;
    z-index: 1;
    padding: 0 0.45rem;
    font-weight: 700;
    border-radius: 4px;
    background: var(--bg);
    color: var(--accent);
  }
  li audio {
    margin-top: 1.8rem;
  }
  .info {
    display: block;
    margin-top: 0.3rem;
    font-size: 0.75rem;
    color: var(--muted);
    text-decoration: none;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
  kbd {
    padding: 0 0.35rem;
    font-family: inherit;
    font-weight: 700;
    border: 1px solid var(--muted);
    border-radius: 4px;
  }
</style>
