<script lang="ts">
  // /?efectos: every effect, recorded and synthesized, to compare on the TV (dev aid, UI-10).
  import { effects, music, sfx, sound, unlock, type Cue, type Track } from "./sound.svelte.ts";

  const list = effects();
  const loops: Track[] = ["normal", "question", "submitted", "timed"];
  let synth = $state(false);

  function play(cue: Cue, synthesized: boolean) {
    unlock();
    sfx(cue, 5, { synth: synthesized });
  }

  /** The loops keep looping, so the seam can be heard. */
  function loop(track: Track | null, s = synth) {
    unlock();
    synth = s;
    music(track, { synth });
  }
</script>

<aside class="efectos">
  <table>
    <tbody>
      {#each loops as track (track)}
        <tr class:on={sound.music === track}>
          <td>música {track}</td>
          <td><button onclick={() => loop(track, false)}>grabado</button></td>
          <td><button onclick={() => loop(track, true)}>sintetizado</button></td>
        </tr>
      {/each}
      <tr>
        <td>{synth ? "sintetizado" : "grabado"}</td>
        <td><button onclick={() => loop(sound.music === "question" ? "submitted" : "question")}>corte</button></td>
        <td><button onclick={() => loop(null)}>parar</button></td>
      </tr>
      {#each list as { cue, file } (cue)}
        <tr>
          <td>{cue}</td>
          <td><button onclick={() => play(cue, false)} disabled={!file} title={file}>grabado</button></td>
          <td><button onclick={() => play(cue, true)}>sintetizado</button></td>
        </tr>
      {/each}
    </tbody>
  </table>
</aside>

<style>
  .efectos {
    position: fixed;
    top: 1rem;
    left: 1rem;
    z-index: 10;
    max-height: calc(100vh - 2rem);
    overflow-y: auto;
    padding: 0.5rem;
    background: rgb(0 0 0 / 0.75);
    color: white;
    font: 0.9rem/1.2 sans-serif;
  }
  td {
    padding: 0.1rem 0.4rem;
  }
  .on {
    color: gold;
  }
</style>
