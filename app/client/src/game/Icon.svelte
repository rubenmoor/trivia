<script lang="ts" module>
  // The game's icons (plans/10-visual-design.md, VD-8): small inline SVGs in one rounded style,
  // drawn in currentColor. No emoji on the TV: they look different on every system.
  export type IconName = "lock" | "unlock" | "speaker" | "film" | "check" | "cross" | "crown" | "trash"
    | "flag" | "idea" | "broom" | "wand" | "point" | "trick-shot" | "crosshair" | "puzzle"
    | "rocket" | "play" | "sparkle" | "next" | "back" | "person" | "person-plus" | "pencil" | "family" | "mic"
    | "balloon" | "skateboard" | "headphones" | "mug" | "sliders" | "book" | "pin" | "refresh" | "power" | "globe" | "exit" | "seal"
    | "gamepad" | "keyboard" | "heart";
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
  {:else if name === "idea"}
    <path d="M10 21h4" />
    <path d="M12 6a5 5 0 0 0-3 9c.6.5 1 1.1 1 1.9V18h4v-1.1c0-.8.4-1.4 1-1.9a5 5 0 0 0-3-9z" fill="currentColor" fill-opacity="0.25" />
    <path d="M10 10a2.4 2.4 0 0 1 1.6-1.8" />
    <path d="M12 1.5v1.3M2.5 11h1.5M20 11h1.5M5 4l1 1M19 4l-1 1" />
  {:else if name === "broom"}
    <g transform="rotate(35 12 12)">
      <path d="M12 1v7" />
      <rect x="9" y="8" width="6" height="3.5" rx="1" fill="currentColor" fill-opacity="0.25" />
      <path d="M9.5 11.5h5c1.5 2.5 3 5.5 3.5 9H6c.5-3.5 2-6.5 3.5-9z" fill="currentColor" fill-opacity="0.25" />
      <path d="M12 15v5.5" />
    </g>
    <path d="M15 21.5c2.5.4 4.6-.1 6.5-1.6M17.5 17.3c1.5 0 2.9-.6 4-1.7" />
  {:else if name === "wand"}
    <path d="M3.5 20.5l8.5-8.5" />
    <path d="M16 2.8l1.3 3.4 3.65.2-2.85 2.3.95 3.5L16 10.2l-3.05 2-.95-3.5-2.85-2.3 3.65-.2z" fill="currentColor" fill-opacity="0.25" />
    <path d="M5.5 4.5v3M4 6h3M20 16v3M18.5 17.5h3" />
  {:else if name === "point"}
    <rect x="16" y="1.5" width="6" height="8" rx="1.5" fill="currentColor" fill-opacity="0.25" transform="rotate(15 19 5.5)" />
    <path d="M5 22v-2.5L3 16a1.4 1.4 0 0 1 2.3-1.6L7 16.5V11a1.5 1.5 0 0 1 3 0v3.5a1.4 1.4 0 0 1 2.8 0 1.4 1.4 0 0 1 2.8.5v4L14.5 22" fill="currentColor" fill-opacity="0.25" transform="rotate(22 9 21)" />
  {:else if name === "trick-shot"}
    <circle cx="14.5" cy="9.5" r="6.5" />
    <path d="M14.5 1v2M14.5 16v2M23 9.5h-2" />
    <path d="M3 3C1.5 17 9 20 14.5 9.5" />
    <path d="M11.9 10.6l2.6-1.1.6 2.7" />
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
  {:else if name === "exit"}
    <path d="M13.5 3.5H6a1.5 1.5 0 0 0-1.5 1.5v14A1.5 1.5 0 0 0 6 20.5h7.5z" fill="currentColor" fill-opacity="0.25" />
    <circle cx="10.5" cy="12" r="0.6" fill="currentColor" />
    <path d="M13 12h8M18 8.5l3.5 3.5-3.5 3.5" />
  {:else if name === "seal"}
    <path d="M12 2.5l2.3 1.7 2.8-.2.9 2.7 2.3 1.6-.9 2.7.9 2.7-2.3 1.6-.9 2.7-2.8-.2-2.3 1.7-2.3-1.7-2.8.2-.9-2.7L4.6 14.7l.9-2.7-.9-2.7 2.3-1.6.9-2.7 2.8.2z" fill="currentColor" fill-opacity="0.25" />
    <path d="M8.5 12.2l2.4 2.4 4.6-4.8" />
  {:else if name === "gamepad"}
    <path d="M7.5 7h9a4.5 4.5 0 0 1 4.4 3.6l.9 4.7a2.6 2.6 0 0 1-4.5 2.2L15.5 15.5h-7l-1.8 2a2.6 2.6 0 0 1-4.5-2.2l.9-4.7A4.5 4.5 0 0 1 7.5 7z" fill="currentColor" fill-opacity="0.25" />
    <path d="M8 9.5v3.5M6.25 11.25h3.5" />
    <circle cx="16" cy="10.5" r="0.6" fill="currentColor" />
    <circle cx="17.5" cy="12.5" r="0.6" fill="currentColor" />
  {:else if name === "keyboard"}
    <rect x="2.5" y="6" width="19" height="12" rx="2.5" fill="currentColor" fill-opacity="0.25" />
    <path d="M6 9.5h.01M9.3 9.5h.01M12.6 9.5h.01M15.9 9.5h.01M18 9.5h.01M7 12.5h.01M10.5 12.5h.01M14 12.5h.01M17 12.5h.01M8 15h8" />
  {:else if name === "heart"}
    <path d="M12 20.5s-8-4.9-8-10.6A4.4 4.4 0 0 1 12 7.3a4.4 4.4 0 0 1 8 2.6c0 5.7-8 10.6-8 10.6z" fill="currentColor" fill-opacity="var(--heart-fill, 0.85)" />
  {/if}
</svg>

<style>
  .icon {
    display: inline-block;
    flex: none;
    vertical-align: -0.15em;
  }
</style>
