<script lang="ts" module>
  // Pad button glyphs (plans/14-input.md, IN-5): drawn for the game in Icon.svelte's style (VD-8),
  // no console makers' art. Standard button index + glyph set → one 24×24 SVG.
  import type { PadStyle } from "../lib/gamepad.ts";

  type Shape = "a" | "b" | "x" | "y" | "cross" | "circle" | "square" | "triangle" | "bumper" | "trigger" | "view" | "menu"
    | "create" | "options" | "up" | "down" | "left" | "right";

  const DPAD: Record<number, Shape> = { 12: "up", 13: "down", 14: "left", 15: "right" };
  const SETS: Record<PadStyle, Record<number, [Shape, string?]>> = {
    xbox: { 0: ["a"], 1: ["b"], 2: ["x"], 3: ["y"], 4: ["bumper", "LB"], 5: ["bumper", "RB"], 6: ["trigger", "LT"],
      7: ["trigger", "RT"], 8: ["view"], 9: ["menu"] },
    playstation: { 0: ["cross"], 1: ["circle"], 2: ["square"], 3: ["triangle"], 4: ["bumper", "L1"], 5: ["bumper", "R1"],
      6: ["trigger", "L2"], 7: ["trigger", "R2"], 8: ["create"], 9: ["options"] },
  };
  const ARMS: Record<string, string> = {
    up: "M9 3.5h6V9H9z",
    down: "M9 15h6v5.5H9z",
    left: "M3.5 9H9v6H3.5z",
    right: "M15 9h5.5v6H15z",
  };
</script>

<script lang="ts">
  let { button, set, size = "1em" }: { button: number; set: PadStyle; size?: string } = $props();
  const glyph: [Shape, string?] | undefined = $derived(DPAD[button] ? [DPAD[button]] : SETS[set][button]);
  const shape = $derived(glyph?.[0]);
  const label = $derived(glyph?.[1] ?? "");
</script>

{#if shape}
  <svg
    class="glyph"
    viewBox="0 0 24 24"
    width={size}
    height={size}
    fill="none"
    stroke="currentColor"
    stroke-width="2.2"
    stroke-linecap="round"
    stroke-linejoin="round"
    aria-hidden="true"
  >
    {#if shape === "bumper"}
      <rect x="1.5" y="5.5" width="21" height="13" rx="5" fill="currentColor" fill-opacity="0.25" />
    {:else if shape === "trigger"}
      <path d="M2.5 19.5V11a6.5 6.5 0 0 1 6.5-6.5h6a6.5 6.5 0 0 1 6.5 6.5v8.5z" fill="currentColor" fill-opacity="0.25" />
    {:else if shape === "create" || shape === "options"}
      <rect x="6.5" y="2.5" width="11" height="19" rx="5.5" fill="currentColor" fill-opacity="0.25" />
    {:else if shape in ARMS}
      <path d="M9 3.5h6V9h5.5v6H15v5.5H9V15H3.5V9H9z" fill="currentColor" fill-opacity="0.2" stroke-width="1.8" />
      <path d={ARMS[shape]} fill="currentColor" stroke-width="1.8" />
    {:else}
      <circle cx="12" cy="12" r="9.8" fill="currentColor" fill-opacity="0.25" />
    {/if}

    {#if label}
      <text x="12" y="16.6" text-anchor="middle" font-size="13.5" letter-spacing="-0.4" fill="currentColor" stroke="none">{label}</text>
    {:else if shape === "a"}
      <path d="M8.5 17l3.5-10 3.5 10M9.8 13.5h4.4" />
    {:else if shape === "b"}
      <path d="M9.2 7h3.4a2.5 2.5 0 0 1 0 5H9.2zM9.2 12h3.9a2.5 2.5 0 0 1 0 5H9.2z" />
    {:else if shape === "x"}
      <path d="M8.8 7.5l6.4 9M15.2 7.5l-6.4 9" />
    {:else if shape === "y"}
      <path d="M8.5 7l3.5 5 3.5-5M12 12v5" />
    {:else if shape === "cross"}
      <path d="M8.5 8.5l7 7M15.5 8.5l-7 7" />
    {:else if shape === "circle"}
      <circle cx="12" cy="12" r="4" />
    {:else if shape === "square"}
      <rect x="8" y="8" width="8" height="8" rx="1" />
    {:else if shape === "triangle"}
      <path d="M12 7.5l4.6 8H7.4z" />
    {:else if shape === "view"}
      <rect x="6.5" y="7.5" width="7" height="6" rx="1.5" stroke-width="1.6" />
      <rect x="10.5" y="10.5" width="7" height="6" rx="1.5" fill="currentColor" stroke-width="1.6" />
    {:else if shape === "menu"}
      <path d="M8 8.5h8M8 12h8M8 15.5h8" stroke-width="1.8" />
    {:else if shape === "create"}
      <path d="M12 15.5V8.5M9.5 11l2.5-2.5 2.5 2.5" stroke-width="1.8" />
    {:else if shape === "options"}
      <path d="M9.5 8.5h5M9.5 12h5M9.5 15.5h5" stroke-width="1.8" />
    {/if}
  </svg>
{/if}

<style>
  .glyph {
    display: inline-block;
    flex: none;
    vertical-align: middle;
  }
  text {
    font-family: var(--font-display);
    font-weight: 800;
  }
</style>
