<script lang="ts">
  // What the LLM saw of a media-first question's window (plan 204), shown once the developer has decided.
  import type { MediaAids } from "../lib/types.ts";

  let { aids }: { aids: MediaAids } = $props();
  const num = (n: number | undefined, unit: string) => (n === undefined ? "" : `${n} ${unit}`);
</script>

<h2>Media aids</h2>
<p class="muted">{[num(aids.integrated_lufs, "LUFS"), num(aids.true_peak_dbfs, "dBTP"), aids.silence_share === undefined ? "" : `${Math.round(aids.silence_share * 100)} % silent`].filter(Boolean).join(" · ")}</p>
{#if aids.speech?.text}<p>“{aids.speech.text}” <span class="muted">{aids.speech.language ?? ""}</span></p>{/if}
{#if aids.ocr?.length}<p class="muted">OCR: {aids.ocr.join(" | ")}</p>{/if}
{#each aids.pictures as src}<img {src} alt="" />{/each}
<h2>Mechanical findings</h2>
{#if aids.mechanical.length}
  <ul>
    {#each aids.mechanical as f}<li>{f.hard ? "⛔" : "·"} {f.kind}: {f.note}</li>{/each}
  </ul>
{:else}
  <p class="muted">none</p>
{/if}

<style>
  img {
    display: block;
    width: 100%;
    margin-top: 0.4rem;
    border-radius: 6px;
  }
</style>
