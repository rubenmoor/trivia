<script lang="ts" module>
  // The game's icons (plans/10-visual-design.md, VD-8): small inline SVGs in one rounded style,
  // drawn in currentColor. No emoji on the TV: they look different on every system.
  export type IconName = "lock" | "unlock" | "replay" | "speaker" | "film" | "check" | "cross" | "crown" | "star" | "trash";
</script>

<script lang="ts">
  let { name, size = "1em" }: { name: IconName; size?: string } = $props();
</script>

<svg
  class="icon"
  viewBox="0 0 24 24"
  width={size}
  height={size}
  fill="none"
  stroke="currentColor"
  stroke-width="2.4"
  stroke-linecap="round"
  stroke-linejoin="round"
  aria-hidden="true"
>
  {#if name === "lock"}
    <rect x="4.5" y="10.5" width="15" height="10.5" rx="2.5" fill="currentColor" fill-opacity="0.25" />
    <path d="M8 10.5V7.5a4 4 0 0 1 8 0v3" />
    <path d="M12 14.5v2.5" />
  {:else if name === "unlock"}
    <rect x="4.5" y="10.5" width="15" height="10.5" rx="2.5" fill="currentColor" fill-opacity="0.25" />
    <path d="M8 10.5V7.5a4 4 0 0 1 7.6-1.7" />
    <path d="M12 14.5v2.5" />
  {:else if name === "replay"}
    <path d="M4.5 12a7.5 7.5 0 1 0 2.2-5.3" />
    <path d="M4 4v4.5h4.5" />
  {:else if name === "speaker"}
    <path d="M4 9.5h3.5L12 5.5v13l-4.5-4H4z" fill="currentColor" fill-opacity="0.25" />
    <path d="M15.5 9a4 4 0 0 1 0 6" />
    <path d="M18 6.5a7.5 7.5 0 0 1 0 11" />
  {:else if name === "film"}
    <rect x="3.5" y="5.5" width="17" height="13" rx="2.5" fill="currentColor" fill-opacity="0.25" />
    <path d="M10 9.5v5l4.5-2.5z" fill="currentColor" />
  {:else if name === "check"}
    <path d="M5 12.5l4.5 4.5L19 7.5" stroke-width="3.2" />
  {:else if name === "cross"}
    <path d="M6.5 6.5l11 11M17.5 6.5l-11 11" stroke-width="3.2" />
  {:else if name === "crown"}
    <path d="M3.5 8l4.5 4 4-6.5 4 6.5 4.5-4-1.8 10.5H5.3z" fill="currentColor" fill-opacity="0.35" />
    <path d="M6 21h12" />
  {:else if name === "trash"}
    <path d="M4.5 7h15" />
    <path d="M9.5 7V5a1.5 1.5 0 0 1 1.5-1.5h2A1.5 1.5 0 0 1 14.5 5v2" />
    <path d="M6.5 7l1 12.5a1.5 1.5 0 0 0 1.5 1.4h6a1.5 1.5 0 0 0 1.5-1.4l1-12.5" fill="currentColor" fill-opacity="0.25" />
    <path d="M10.5 11v6M13.5 11v6" />
  {:else if name === "star"}
    <path
      d="M12 3.5l2.6 5.4 5.9.8-4.3 4.1 1 5.8L12 16.8l-5.2 2.8 1-5.8-4.3-4.1 5.9-.8z"
      fill="currentColor"
      fill-opacity="0.35"
    />
  {/if}
</svg>

<style>
  .icon {
    display: inline-block;
    flex: none;
    vertical-align: -0.15em;
  }
</style>
