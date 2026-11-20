<script lang="ts">
  // Authoring pages (never shipped, D-35): / the start page (RV-14), /review the review tool
  // (plans/08-review-tool.md), /stats/… the statistics (QP-13), /comodines the printable joker cards (JK-11),
  // /gallery the screen gallery (plan 100), /sounds the audition candidates (plan 220),
  // /review?fit=<bundle> the fit pass's verdicts and flips (plan 230).
  import Fit from "./fit/Fit.svelte";
  import Gallery from "./gallery/Gallery.svelte";
  import Home from "./home/Home.svelte";
  import JokerCards from "./print/JokerCards.svelte";
  import Sounds from "./sounds/Sounds.svelte";
  import Review from "./review/Review.svelte";
  import Stats from "./stats/Stats.svelte";

  const path = location.pathname;
</script>

{#if path === "/"}
  <Home />
{:else if path.startsWith("/stats")}
  <Stats />
{:else if path.startsWith("/gallery")}
  <Gallery />
{:else if path === "/sounds"}
  <Sounds />
{:else if path.startsWith("/comodines")}
  <JokerCards />
{:else if path === "/review" && new URLSearchParams(location.search).has("fit")}
  <Fit />
{:else}
  <Review />
{/if}
