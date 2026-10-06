<script lang="ts">
  // PLACEHOLDER(UI-8): shows the music and effects that would be playing.
  import { sound } from "./sound.svelte";
</script>

<div class="captions">
  <span class="tag">PLACEHOLDER · UI-8 sonido</span>
  <span>♪ música: {sound.music ?? "silencio"}</span>
  {#each sound.effects as e (e.id)}
    <span class="effect">🔊 {e.name}</span>
  {/each}
</div>

<style>
  .captions {
    position: fixed;
    left: 1rem;
    bottom: 1rem;
    display: flex;
    flex-direction: column;
    gap: 0.2rem;
    padding: 0.4rem 0.7rem;
    border: 0.12rem dashed #ff7ad9;
    border-radius: 0.5rem;
    background: rgba(60, 10, 50, 0.7);
    color: #ffb8ec;
    font-size: 0.9rem;
    z-index: 30;
    pointer-events: none;
  }
  .tag {
    font-family: ui-monospace, monospace;
    font-size: 0.75rem;
    opacity: 0.85;
  }
  .effect {
    animation: pop 0.2s ease-out;
  }
  @keyframes pop {
    from {
      transform: scale(1.3);
    }
  }
</style>
