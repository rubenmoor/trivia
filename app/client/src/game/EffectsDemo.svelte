<script lang="ts">
  // /?efectos: every effect, recorded and synthesized, to compare on the TV (dev aid, UI-10).
  import { effects, sfx, unlock, type Cue } from "./sound.svelte";

  const list = effects();

  function play(cue: Cue, synth: boolean) {
    unlock();
    sfx(cue, 5, { synth });
  }
</script>

<aside class="efectos">
  <table>
    <tbody>
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
</style>
