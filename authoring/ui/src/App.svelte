<script lang="ts">
  // Authoring pages (never shipped, D-35): /review the review tool (plans/08-review-tool.md),
  // /stats/… the statistics (QP-13), /comodines the printable joker cards (JK-11).
  import JokerCards from "./print/JokerCards.svelte";
  import Review from "./review/Review.svelte";
  import Stats from "./stats/Stats.svelte";

  const path = location.pathname;
</script>

{#if path.startsWith("/stats")}
  <Stats />
{:else if path.startsWith("/comodines")}
  <JokerCards />
{:else}
  <Review />
{/if}
