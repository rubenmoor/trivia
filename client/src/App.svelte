<script lang="ts">
  // Routes: /stats/… shows the statistics (QP-13); everything else is the review tool
  // (plans/08-review-tool.md). The game will get its own route.
  import Review from "./review/Review.svelte";
  import Stats from "./stats/Stats.svelte";

  const stats = location.pathname.startsWith("/stats");
</script>

{#if stats}
  <Stats />
{:else}
  <Review />
{/if}
