<script lang="ts" module>
  // National flags per language tag (plans/10-visual-design.md, VD-8) or one country (a regional bundle, plan 151):
  // own simplified drawings of the public-domain designs, fixed colours. Unknown tags and countries show the globe.
  const DRAWN = ["mx", "co", "ar", "es", "gb", "us", "de", "at", "ch", "cn", "tw", "hk", "mo"] as const;
  type Flag = (typeof DRAWN)[number];

  const SETS: Record<string, Flag[]> = {
    es: ["mx", "co", "ar"],
    "es-ES": ["es"],
    en: ["gb", "us"],
    de: ["de", "at", "ch"],
    "zh-Hans": ["cn"],
    "zh-Hant": ["hk", "mo", "tw"],
  };
</script>

<script lang="ts">
  import Icon from "./Icon.svelte";

  /** `tag`: a language tag's flags; `country`: one ISO 3166-1 alpha-2 code's flag. */
  let { tag, country, size = "1em" }: { tag?: string; country?: string; size?: string } = $props();

  const one = $derived(country?.toLowerCase() as Flag | undefined);
  const flags = $derived(country ? (one && DRAWN.includes(one) ? [one] : []) : (SETS[tag ?? ""] ?? []));
</script>

{#if flags.length}
  <span class="flags" style:--h={size} aria-hidden="true">
    {#each flags as f, i (f)}
      <span class="flag" class:square={f === "ch"} style:--r="{(i - (flags.length - 1) / 2) * 9}deg" style:z-index={i}>
        <svg viewBox={f === "ch" ? "0 0 20 20" : "0 0 30 20"} preserveAspectRatio="none">
          {#if f === "mx"}
            <rect width="10" height="20" fill="#006847" />
            <rect x="10" width="10" height="20" fill="#fff" />
            <rect x="20" width="10" height="20" fill="#ce1126" />
            <circle cx="15" cy="9.6" r="2.4" fill="#8c5a2b" />
            <path d="M12.2 10.8a2.9 2.9 0 0 0 5.6 0" fill="none" stroke="#006847" stroke-width="1" stroke-linecap="round" />
          {:else if f === "co"}
            <rect width="30" height="10" fill="#fcd116" />
            <rect y="10" width="30" height="5" fill="#003893" />
            <rect y="15" width="30" height="5" fill="#ce1126" />
          {:else if f === "ar"}
            <rect width="30" height="20" fill="#74acdf" />
            <rect y="6.67" width="30" height="6.67" fill="#fff" />
            <circle cx="15" cy="10" r="2.3" fill="#f6b40e" stroke="#85340a" stroke-width="0.5" />
          {:else if f === "es"}
            <rect width="30" height="20" fill="#aa151b" />
            <rect y="5" width="30" height="10" fill="#f1bf00" />
          {:else if f === "gb"}
            <rect width="30" height="20" fill="#012169" />
            <path d="M0 0l30 20M30 0L0 20" stroke="#fff" stroke-width="4" />
            <path d="M0 0l30 20M30 0L0 20" stroke="#c8102e" stroke-width="1.4" />
            <path d="M15 0v20M0 10h30" stroke="#fff" stroke-width="6" />
            <path d="M15 0v20M0 10h30" stroke="#c8102e" stroke-width="3.6" />
          {:else if f === "us"}
            <rect width="30" height="20" fill="#b22234" />
            <path d="M0 4.29h30M0 10h30M0 15.71h30" stroke="#fff" stroke-width="2.86" />
            <rect width="13" height="11.43" fill="#3c3b6e" />
            <g fill="#fff">
              <circle cx="3" cy="3" r="1" /><circle cx="6.5" cy="3" r="1" /><circle cx="10" cy="3" r="1" />
              <circle cx="4.75" cy="5.7" r="1" /><circle cx="8.25" cy="5.7" r="1" />
              <circle cx="3" cy="8.4" r="1" /><circle cx="6.5" cy="8.4" r="1" /><circle cx="10" cy="8.4" r="1" />
            </g>
          {:else if f === "de"}
            <rect width="30" height="6.67" fill="#000" />
            <rect y="6.67" width="30" height="6.67" fill="#dd0000" />
            <rect y="13.33" width="30" height="6.67" fill="#ffce00" />
          {:else if f === "at"}
            <rect width="30" height="20" fill="#c8102e" />
            <rect y="6.67" width="30" height="6.67" fill="#fff" />
          {:else if f === "ch"}
            <rect width="20" height="20" fill="#da291c" />
            <path d="M8.1 3.8h3.8v4.3h4.3v3.8h-4.3v4.3H8.1v-4.3H3.8V8.1h4.3z" fill="#fff" />
          {:else if f === "cn"}
            <rect width="30" height="20" fill="#de2910" />
            <path d="M0-3l.88 2.7 2.84.02-2.3 1.66.87 2.7L0 2.4l-2.29 1.68.87-2.7-2.3-1.66 2.84-.02z" fill="#ffde00" transform="translate(5 5) scale(1.4)" />
            <g fill="#ffde00">
              <circle cx="10" cy="2" r="0.7" /><circle cx="12" cy="4" r="0.7" /><circle cx="12" cy="7" r="0.7" /><circle cx="10" cy="9" r="0.7" />
            </g>
          {:else if f === "tw"}
            <rect width="30" height="20" fill="#fe0000" />
            <rect width="15" height="10" fill="#000095" />
            <circle cx="7.5" cy="5" r="3.2" fill="#fff" />
            <circle cx="7.5" cy="5" r="2.2" fill="#000095" />
            <circle cx="7.5" cy="5" r="1.8" fill="#fff" />
          {:else if f === "hk"}
            <rect width="30" height="20" fill="#de2910" />
            <g fill="#fff" transform="translate(15 10)">
              {#each [0, 72, 144, 216, 288] as a (a)}
                <ellipse cx="0" cy="-3.6" rx="1.7" ry="3" transform="rotate({a})" />
              {/each}
            </g>
          {:else if f === "mo"}
            <rect width="30" height="20" fill="#00785e" />
            <path d="M8 14.5q7-3 14 0v1.5q-7-3-14 0z" fill="#fff" />
            <ellipse cx="15" cy="12.3" rx="3.6" ry="1.6" fill="#fff" />
            <path d="M15 4l.5 1.3h1.4l-1.1.9.4 1.3-1.2-.8-1.2.8.4-1.3-1.1-.9h1.4z" fill="#fbd116" />
            <g fill="#fbd116">
              <circle cx="10.5" cy="6.3" r="0.8" /><circle cx="12" cy="4.6" r="0.8" /><circle cx="18" cy="4.6" r="0.8" /><circle cx="19.5" cy="6.3" r="0.8" />
            </g>
          {/if}
        </svg>
      </span>
    {/each}
  </span>
{:else}
  <Icon name="globe" {size} />
{/if}

<style>
  .flags {
    display: inline-flex;
    flex: none;
    align-items: center;
    padding: 0 0.1em;
  }
  .flag {
    position: relative;
    display: block;
    width: calc(var(--h) * 1.5);
    height: var(--h);
    border-radius: calc(var(--h) * 0.14);
    overflow: hidden;
    box-shadow: 0 0 0 calc(var(--h) * 0.05) rgb(15 23 42 / 0.85);
    transform: rotate(var(--r));
  }
  .flag + .flag {
    margin-left: calc(var(--h) * -0.45);
  }
  .flag.square {
    width: var(--h);
  }
  svg {
    display: block;
    width: 100%;
    height: 100%;
  }
</style>
