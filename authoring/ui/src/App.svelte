<script lang="ts">
  // Authoring pages (never shipped, D-35): / the start page (RV-14), /review the review tool
  // (plans/08-review-tool.md), /stats/… the statistics (QP-13), /comodines the printable joker cards (JK-11).
  import Home from "./home/Home.svelte";
  import JokerCards from "./print/JokerCards.svelte";
  import Review from "./review/Review.svelte";
  import Stats from "./stats/Stats.svelte";

  const path = location.pathname;
  // Old links to the review tool were plain "/?batch=…" (before the start page): keep them working.
  const oldReviewLink = path === "/" && ["batch", "bundle", "id"].some((k) => new URLSearchParams(location.search).has(k));
  if (oldReviewLink) location.replace(`/review${location.search}`);
</script>

{#if oldReviewLink}
  <!-- redirecting -->
{:else if path === "/"}
  <Home />
{:else if path.startsWith("/stats")}
  <Stats />
{:else if path.startsWith("/comodines")}
  <JokerCards />
{:else}
  <Review />
{/if}
