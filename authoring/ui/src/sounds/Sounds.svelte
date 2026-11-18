<script lang="ts">
  // Audition candidates (plan 220): work/sound-brief/manifest.json, one section per effects direction and music mood,
  // grouped by round. What is installed in the game is /?efectos, not this page.
  import { onMount } from "svelte";
  import { messageOf } from "$app/lib/http.ts";
  import { fetchSounds } from "../lib/api.ts";
  import Nav from "../lib/Nav.svelte";
  import type { SoundCandidate } from "../lib/types.ts";

  let entries = $state<SoundCandidate[] | null>(null);
  let loaded = $state(false);
  let error = $state<string | null>(null);

  onMount(async () => {
    try {
      entries = await fetchSounds();
    } catch (e) {
      error = messageOf(e);
    }
    loaded = true;
  });

  const url = (file: string) => `/sounds/${file.split("/").map(encodeURIComponent).join("/")}`;
  const num = (n: number | undefined, unit: string, digits = 1) => (typeof n === "number" ? `${n.toFixed(digits)} ${unit}` : "-");

  // [heading, entries by round]; effects first, then music, in manifest order.
  const sections = $derived.by(() => {
    const out = new Map<string, Map<number, SoundCandidate[]>>();
    for (const e of entries ?? []) {
      const head = `${e.group === "music" ? "Music" : "Effects"}: ${(e.group === "music" ? e.mood : e.direction) ?? "?"}`;
      const rounds = out.get(head) ?? new Map<number, SoundCandidate[]>();
      rounds.set(e.round, [...(rounds.get(e.round) ?? []), e]);
      out.set(head, rounds);
    }
    return [...out].sort(([a], [b]) => a.localeCompare(b)).map(([head, rounds]) => ({ head, rounds: [...rounds].sort(([a], [b]) => a - b) }));
  });

  let playing: HTMLAudioElement | null = null;

  // One file at a time.
  function onPlay(e: Event) {
    const a = e.currentTarget as HTMLAudioElement;
    if (playing && playing !== a) playing.pause();
    playing = a;
  }
</script>

<Nav current="sounds" />
<main>
  <h1>Sounds</h1>
  <p class="muted small">Audition candidates for the sound rework (<code>work/sound-brief/</code>). Installed sounds: <a href="http://localhost:8000/?efectos">/?efectos</a> on the game.</p>
  {#if !loaded}
    <p class="muted">Loading…</p>
  {:else if error}
    <p class="error">{error}</p>
  {:else if !entries?.length}
    <p class="muted">No candidates yet.</p>
  {:else}
    {#each sections as s (s.head)}
      <section>
        <h2>{s.head}</h2>
        {#each s.rounds as [round, items] (round)}
          <h3>Round {round}</h3>
          <table>
            <thead>
              <tr><th>Play</th><th>Stands for</th><th>Length</th><th>LUFS</th><th>True peak</th><th>Centroid</th><th>BPM</th><th>Author, licence</th><th>Source</th></tr>
            </thead>
            <tbody>
              {#each items as it (it.file)}
                <tr>
                  <td><audio controls preload="none" src={url(it.file)} onplay={onPlay}></audio></td>
                  <td><b>{it.stands_for}</b><br /><span class="muted small">{it.file}</span>{#if it.full_length_s}<br /><span class="muted small">full track {it.full_length_s} s, excerpt from {it.excerpt_start_s} s</span>{/if}{#if it.tension_note}<br /><span class="small">Tension: {it.tension_note}</span>{/if}</td>
                  <td>{num(it.length_s, "s")}</td>
                  <td>{num(it.lufs, "")}</td>
                  <td>{num(it.true_peak_db, "dB")}</td>
                  <td>{num(it.centroid_hz, "Hz", 0)}</td>
                  <td>{typeof it.bpm === "number" ? it.bpm : "-"}</td>
                  <td>{it.author}, {it.licence}</td>
                  <td><a href={it.source} target="_blank" rel="noreferrer">page</a></td>
                </tr>
              {/each}
            </tbody>
          </table>
        {/each}
      </section>
    {/each}
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
    margin: 1rem 0 0.5rem;
    font-size: 1rem;
  }
  .small {
    font-size: 0.85rem;
  }
  .error {
    color: var(--bad);
  }
  table {
    border-collapse: collapse;
    width: 100%;
  }
  th,
  td {
    padding: 0.3rem 0.5rem;
    text-align: left;
    vertical-align: middle;
    border-bottom: 1px solid var(--border, #ddd);
  }
  audio {
    height: 2rem;
    width: 14rem;
  }
</style>
