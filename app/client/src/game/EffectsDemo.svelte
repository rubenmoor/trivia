<script lang="ts">
  // /?efectos: every effect, recorded and synthesized, to compare on the TV (dev aid, UI-10).
  import Splash from "./question/Splash.svelte";
  import { SPLASH_EXITS, type SplashExit } from "./question/splash.ts";
  import { effects, music, sfx, setSoundtrack, sound, SOUNDTRACKS, soundtrackIds, unlock, type Cue, type SoundtrackId, type Track } from "./sound.svelte.ts";

  const list = effects();
  /** The splash on show: a sample category over a sample subcategory (the names fall back to the keys). */
  let splash = $state<{ exit: SplashExit; n: number } | null>(null);
  function playSplash(exit: SplashExit) {
    unlock();
    splash = { exit, n: (splash?.n ?? 0) + 1 };
  }
  const FILE_NAME: Record<Track, string> = { normal: "normal", question: "pregunta", submitted: "enviada", timed: "timed", roll: "roll", victory: "victory" };
  const loops: Track[] = ["normal", "question", "submitted", "timed"];
  let shown = $state<SoundtrackId>(soundtrackIds[0]);

  function play(cue: Cue, synthesized: boolean) {
    unlock();
    sfx(cue, 5, { synth: synthesized });
  }

  /** The loops keep looping, so the seam can be heard. */
  function loop(track: Track | null, soundtrack = shown) {
    unlock();
    shown = soundtrack;
    music(track, { soundtrack });
  }
</script>

<aside class="efectos">
  <table>
    <tbody>
      {#each soundtrackIds as id (id)}
        <tr>
          <td class:on={sound.soundtrack === id}><button onclick={() => setSoundtrack(id)} title="elegir (se guarda)">{id}</button></td>
          {#each loops as track (track)}
            <td class:on={sound.music === track && shown === id}>
              <button onclick={() => loop(track, id)}>{"files" in SOUNDTRACKS[id] ? FILE_NAME[track] : track}</button>
            </td>
          {/each}
          <td><button onclick={() => loop(sound.music === "question" ? "submitted" : "question", id)}>corte</button></td>
        </tr>
      {/each}
      <tr>
        <td colspan="6"><button onclick={() => loop(null)}>parar</button></td>
      </tr>
      {#each SPLASH_EXITS as exit (exit.id)}
        <tr>
          <td>splash {exit.id}</td>
          <td><button onclick={() => playSplash(exit)}>jugar</button></td>
          <td>{exit.cue}</td>
        </tr>
      {/each}
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

{#if splash}
  {#key splash.n}
    <div class="splash-stage"><Splash category="Geografía" subcategory="Capitales del mundo" start exit={splash.exit} /></div>
  {/key}
{/if}

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
  .splash-stage {
    position: fixed;
    inset: 0;
    pointer-events: none;
  }
  td {
    padding: 0.1rem 0.4rem;
  }
  .on {
    color: gold;
  }
</style>
