<script lang="ts" module>
  // The night stage behind every screen without media (plans/10-visual-design.md, VD-6): a radial
  // gradient, an amber spotlight from the top, faint «?» drifting upwards. Variants per screen.
  export type StageMood = "calm" | "correct" | "wrong" | "victory";

  /** Fixed positions, so the glyphs don't jump when the screen changes. */
  const GLYPHS = Array.from({ length: 18 }, (_, i) => ({
    left: (i * 37 + 11) % 100,
    size: 3 + ((i * 7) % 5) * 1.6,
    duration: 22 + ((i * 13) % 17),
    delay: -((i * 29) % 40),
    tilt: ((i * 47) % 40) - 20,
  }));
</script>

<script lang="ts">
  let { mood = "calm" }: { mood?: StageMood } = $props();
</script>

<div class="stage {mood}" aria-hidden="true">
  <div class="spotlight"></div>
  {#each GLYPHS as g, i (i)}
    <span
      class="glyph"
      style:left="{g.left}%"
      style:font-size="calc({g.size} * var(--u))"
      style:animation-duration="{g.duration}s"
      style:animation-delay="{g.delay}s"
      style:--tilt="{g.tilt}deg"
    >
      {mood === "victory" ? "★" : "?"}
    </span>
  {/each}
  <div class="rim"></div>
</div>

<style>
  .stage {
    position: absolute;
    inset: 0;
    overflow: hidden;
    background: radial-gradient(ellipse at 50% 35%, var(--night-800), var(--night-900) 75%);
    transition: filter 1.2s;
  }
  .spotlight {
    position: absolute;
    left: 50%;
    top: -10%;
    width: 70%;
    height: 120%;
    transform: translateX(-50%);
    background: radial-gradient(ellipse 50% 60% at 50% 0%, rgba(255, 184, 28, 0.16), transparent 70%);
    clip-path: polygon(38% 0, 62% 0, 100% 100%, 0 100%);
    filter: blur(calc(2 * var(--u)));
    transition:
      opacity 1.2s,
      background 1.2s;
  }
  .glyph {
    position: absolute;
    bottom: -15%;
    font-family: var(--font-display);
    font-weight: 800;
    color: var(--paper);
    opacity: 0.05;
    animation: drift linear infinite;
  }
  @keyframes drift {
    from {
      transform: translateY(0) rotate(var(--tilt));
    }
    to {
      transform: translateY(-130vh) rotate(calc(-1 * var(--tilt)));
    }
  }
  .rim {
    position: absolute;
    inset: 0;
    pointer-events: none;
    transition: box-shadow 1.2s;
  }

  .correct .spotlight {
    opacity: 1.4;
    background: radial-gradient(ellipse 50% 60% at 50% 0%, rgba(47, 227, 154, 0.2), transparent 70%);
  }
  .correct .rim {
    box-shadow: inset 0 0 calc(8 * var(--u)) rgba(47, 227, 154, 0.35);
  }
  .wrong {
    filter: grayscale(0.8) brightness(0.75);
  }
  .wrong .spotlight {
    opacity: 0.35;
  }
  .wrong .rim {
    box-shadow: inset 0 0 calc(18 * var(--u)) rgba(0, 0, 0, 0.85);
  }
  .victory .spotlight {
    background: radial-gradient(ellipse 50% 60% at 50% 0%, rgba(255, 184, 28, 0.32), transparent 70%);
  }
  .victory .glyph {
    color: var(--amber);
    opacity: 0.18;
  }
  .victory .rim {
    box-shadow: inset 0 0 calc(10 * var(--u)) rgba(255, 184, 28, 0.25);
  }
</style>
