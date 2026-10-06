<script lang="ts">
  // Routes (D-25): / is the game (plans/04-ui-tv-display.md), /review the review tool
  // (plans/08-review-tool.md), /stats/… the statistics (QP-13), /comodines the printable joker
  // cards (JK-11).
  import Game from "./game/Game.svelte";
  import JokerCards from "./print/JokerCards.svelte";
  import Review from "./review/Review.svelte";
  import Stats from "./stats/Stats.svelte";

  const path = location.pathname;
</script>

{#if path.startsWith("/stats")}
  <Stats />
{:else if path.startsWith("/review")}
  <Review />
{:else if path.startsWith("/comodines")}
  <JokerCards />
{:else}
  <Game />
{/if}
