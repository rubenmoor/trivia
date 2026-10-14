<script lang="ts">
  // The authoring pages' nav bar (RV-16): start page, review tool, stats, screen gallery, joker cards.
  let { current }: { current: "start" | "review" | "stats" | "gallery" } = $props();
</script>

<nav>
  <a href="/" class:current={current === "start"}>Start</a>
  <a href="/review" class:current={current === "review"}>Review</a>
  <a href="/stats/categories" class:current={current === "stats"}>Stats</a>
  <a href="/gallery" class:current={current === "gallery"}>Gallery</a>
  <a href="/comodines">Joker cards</a>
</nav>

<style>
  nav {
    display: flex;
    flex-wrap: wrap;
    gap: 0.25rem 1.25rem;
    margin-bottom: 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid var(--line);
    font-size: 0.9rem;
  }
  a {
    color: var(--muted);
    text-decoration: none;
  }
  a:hover,
  a.current {
    color: var(--text);
  }
  a.current {
    font-weight: 600;
  }
</style>
