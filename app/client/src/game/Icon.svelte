<script lang="ts" module>
  // The game's icons (plans/10-visual-design.md, VD-8): small inline SVGs in one rounded style,
  // drawn in currentColor. No emoji on the TV: they look different on every system.
  export type IconName = "lock" | "unlock" | "speaker" | "film" | "check" | "cross" | "crown" | "trash"
    | "flag" | "bulb" | "door" | "stairs" | "compass" | "crosshair" | "puzzle"
    | "rocket" | "play" | "sparkle" | "next" | "back" | "person" | "person-plus" | "pencil" | "family" | "mic"
    | "balloon" | "skateboard" | "headphones" | "mug" | "sliders" | "book" | "pin" | "refresh" | "power" | "globe";
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
  {:else if name === "flag"}
    <path d="M5.5 21V4" />
    <path d="M5.5 4.5h12l-2.5 4 2.5 4h-12" fill="currentColor" fill-opacity="var(--flag-fill, 0.25)" />
  {:else if name === "bulb"}
    <path d="M9 17.5h6M10 21h4" />
    <path d="M12 3a6 6 0 0 0-3.6 10.8c.7.6 1.1 1.3 1.1 2.2v1.5h5V16c0-.9.4-1.6 1.1-2.2A6 6 0 0 0 12 3z" fill="currentColor" fill-opacity="0.25" />
  {:else if name === "door"}
    <path d="M5 21V4.5A1.5 1.5 0 0 1 6.5 3H14v18" fill="currentColor" fill-opacity="0.25" />
    <path d="M3.5 21h17" />
    <path d="M14 12h7M18 9l3 3-3 3" />
  {:else if name === "stairs"}
    <path d="M3.5 6.5h4v4h4v4h4v4h5" />
    <path d="M14 4.5l5 5M19 5.5v4h-4" />
  {:else if name === "compass"}
    <circle cx="12" cy="12" r="8.5" fill="currentColor" fill-opacity="0.2" />
    <path d="M15.5 8.5l-2 5-5 2 2-5z" fill="currentColor" />
  {:else if name === "crosshair"}
    <circle cx="12" cy="12" r="7.5" />
    <path d="M12 2v5M12 17v5M2 12h5M17 12h5" />
    <circle cx="12" cy="12" r="1.5" fill="currentColor" />
  {:else if name === "puzzle"}
    <path d="M4 8h4a2 2 0 1 1 4 0h4v4a2 2 0 1 1 0 4v4h-4a2 2 0 1 0-4 0H4v-4a2 2 0 1 0 0-4z" fill="currentColor" fill-opacity="0.2" />
  {:else if name === "rocket"}
    <path d="M13.5 16.5l-6-6C10 5 14.5 3 20.5 3.5 21 9.5 19 14 13.5 16.5z" fill="currentColor" fill-opacity="0.25" />
    <circle cx="15.5" cy="8.5" r="1.8" />
    <path d="M8.5 11.5L4 12l2.5-4.5h4M12.5 15.5L12 20l4.5-2.5v-4" />
    <path d="M7 17l-3 3M5 14.5l-1.5 1.5M9.5 19.5L8 21" />
  {:else if name === "play"}
    <path d="M8 5.5v13a1 1 0 0 0 1.5.9l10-6.5a1 1 0 0 0 0-1.7l-10-6.5A1 1 0 0 0 8 5.5z" fill="currentColor" fill-opacity="0.25" />
  {:else if name === "sparkle"}
    <path d="M11 3c.8 4.5 2.5 6.2 7 7-4.5.8-6.2 2.5-7 7-.8-4.5-2.5-6.2-7-7 4.5-.8 6.2-2.5 7-7z" fill="currentColor" fill-opacity="0.25" />
    <path d="M19 15.5v5M16.5 18h5" />
  {:else if name === "next"}
    <path d="M4 9.5h8V5.5l8 6.5-8 6.5v-4H4z" fill="currentColor" fill-opacity="0.25" />
  {:else if name === "back"}
    <path d="M9 4.5L4 9.5l5 5" />
    <path d="M4 9.5h10a5.5 5.5 0 0 1 0 11h-3" />
  {:else if name === "person"}
    <circle cx="12" cy="8" r="3.8" fill="currentColor" fill-opacity="0.25" />
    <path d="M5 20.5a7 7 0 0 1 14 0z" fill="currentColor" fill-opacity="0.25" />
  {:else if name === "person-plus"}
    <circle cx="9.5" cy="8" r="3.8" fill="currentColor" fill-opacity="0.25" />
    <path d="M2.5 20.5a7 7 0 0 1 14 0z" fill="currentColor" fill-opacity="0.25" />
    <path d="M19.5 8v6M16.5 11h6" />
  {:else if name === "pencil"}
    <path d="M15.5 4.5l4 4L9 19l-5 1 1-5z" fill="currentColor" fill-opacity="0.25" />
    <path d="M13 7l4 4" />
  {:else if name === "family"}
    <circle cx="7" cy="6.5" r="2.5" />
    <circle cx="17" cy="6.5" r="2.5" />
    <circle cx="12" cy="13.5" r="2" />
    <path d="M3.5 19.5v-3a3.5 3.5 0 0 1 7 0v3M13.5 19.5v-3a3.5 3.5 0 0 1 7 0v3" fill="currentColor" fill-opacity="0.25" />
    <path d="M9.5 21v-2.5a2.5 2.5 0 0 1 5 0V21" fill="currentColor" fill-opacity="0.25" />
  {:else if name === "mic"}
    <rect x="9" y="3" width="6" height="11" rx="3" fill="currentColor" fill-opacity="0.25" />
    <path d="M5.5 11a6.5 6.5 0 0 0 13 0" />
    <path d="M12 17.5V21M8.5 21h7" />
  {:else if name === "balloon"}
    <path d="M12 3a6 6 0 0 0-6 6.5c0 3.5 3 6.5 6 7.5 3-1 6-4 6-7.5A6 6 0 0 0 12 3z" fill="currentColor" fill-opacity="0.25" />
    <path d="M12 17c-1.5 1.5 1 2.5-.5 4" />
    <path d="M9.3 8.5a3 3 0 0 1 2-2.5" />
  {:else if name === "skateboard"}
    <path d="M2.5 11c.5 1.5 1.5 2.5 3 2.5h13c1.5 0 2.5-1 3-2.5" fill="currentColor" fill-opacity="0.25" />
    <circle cx="7" cy="17.5" r="1.8" />
    <circle cx="17" cy="17.5" r="1.8" />
  {:else if name === "headphones"}
    <path d="M4.5 15v-3a7.5 7.5 0 0 1 15 0v3" />
    <rect x="3" y="13.5" width="4.5" height="7" rx="2" fill="currentColor" fill-opacity="0.25" />
    <rect x="16.5" y="13.5" width="4.5" height="7" rx="2" fill="currentColor" fill-opacity="0.25" />
  {:else if name === "mug"}
    <path d="M4.5 8.5h11v8a3.5 3.5 0 0 1-3.5 3.5H8a3.5 3.5 0 0 1-3.5-3.5z" fill="currentColor" fill-opacity="0.25" />
    <path d="M15.5 10.5H17a2.5 2.5 0 0 1 0 5h-1.5" />
    <path d="M8 3c-.8 1 .8 2 0 3M12 3c-.8 1 .8 2 0 3" />
  {:else if name === "sliders"}
    <path d="M4 6.5h3M11 6.5h9M4 12h9M17 12h3M4 17.5h2M10 17.5h10" />
    <circle cx="9" cy="6.5" r="2" fill="currentColor" fill-opacity="0.25" />
    <circle cx="15" cy="12" r="2" fill="currentColor" fill-opacity="0.25" />
    <circle cx="8" cy="17.5" r="2" fill="currentColor" fill-opacity="0.25" />
  {:else if name === "book"}
    <path d="M12 6.5C10 5 7 4.5 3.5 5v13c3.5-.5 6.5 0 8.5 1.5 2-1.5 5-2 8.5-1.5V5C17 4.5 14 5 12 6.5z" fill="currentColor" fill-opacity="0.25" />
    <path d="M12 6.5v13" />
  {:else if name === "pin"}
    <path d="M12 21s-6.5-6-6.5-11a6.5 6.5 0 0 1 13 0c0 5-6.5 11-6.5 11z" fill="currentColor" fill-opacity="0.25" />
    <circle cx="12" cy="10" r="2.3" />
  {:else if name === "refresh"}
    <path d="M4.5 12a7.5 7.5 0 0 1 13-5.1M19.5 12a7.5 7.5 0 0 1-13 5.1" />
    <path d="M17.5 3v3.9h-3.9M6.5 21v-3.9h3.9" />
  {:else if name === "power"}
    <circle cx="12" cy="11.8" r="7.5" fill="currentColor" fill-opacity="0.2" stroke="none" />
    <path d="M7 6.2a7.5 7.5 0 1 0 10 0" />
    <path d="M12 3v8" />
  {:else if name === "globe"}
    <circle cx="12" cy="12" r="8.5" fill="currentColor" fill-opacity="0.2" />
    <path d="M3.5 12h17M12 3.5a13 13 0 0 1 0 17M12 3.5a13 13 0 0 0 0 17" />
  {/if}
</svg>

<style>
  .icon {
    display: inline-block;
    flex: none;
    vertical-align: -0.15em;
  }
</style>
