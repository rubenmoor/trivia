<script lang="ts">
  // The Mode screens (plans/04-ui-tv-display.md, "Mode"; MD-7, decision 314), right after Start (decision 747): first
  // «Solo o en grupo» or «Multijugador», then the mode itself: standard or gamemaster mode, or the multiplayer modes in
  // two groups (collaborative: rr-coop; competitive: rr-competitive, timed), one pick. Only the built modes show (dev mode
  // shows the unbuilt ones marked, decision 293); with no multiplayer mode to show, the first step is skipped.
  // Preset (modePreset.ts, task 2114): the pick kept for Back, else `?mode=`, else the last mode played (the save's newest
  // game's, if shown), else the standard mode; with the kind step, that mode's kind. «Seguir» (Enter/A anywhere) goes
  // on, Space/X picks the ring's tile, a tile's letter picks it and moves the ring, Back goes a step back.
  import { onMount, untrack } from "svelte";
  import { BUILT_MODES, fetchLastMode } from "../../lib/api.ts";
  import { devMode } from "../../lib/desktop.ts";
  import { show } from "../../lib/focus.ts";
  import { t } from "../../lib/i18n.ts";
  import type { TextKey } from "../../locales/es.ts";
  import { pushScope, type Keys } from "../../lib/input.svelte.ts";
  import type { GameMode } from "../../lib/types.ts";
  import { modePreset, type Kind, type Stage } from "../modePreset.ts";
  import Icon, { type IconName } from "../Icon.svelte";
  import OptionButton from "../OptionButton.svelte";
  import Prompt from "../Prompt.svelte";

  let {
    busy,
    mode,
    onnext,
    onback,
  }: {
    busy: boolean;
    /** The pick kept in Game.svelte from an earlier visit (Back from a later screen), else null: the preset applies. */
    mode: GameMode | null;
    onnext: (mode: GameMode) => void;
    onback: () => void;
  } = $props();

  interface Tile {
    id: GameMode;
    name: string;
    about: string;
    key: string;
    icon: IconName;
    /** The task that ships an unbuilt mode, which dev mode shows marked (decision 293). */
    ships?: string;
  }
  /** A tile from catalog keys. */
  const tile = (id: GameMode, name: TextKey, about: TextKey, key: TextKey, icon: IconName, ships?: string): Tile =>
    ({ id, name: t(name), about: t(about), key: t(key).toLowerCase(), icon, ships });
  const unbuilt = (m: Tile) => (m.ships && !BUILT_MODES.includes(m.id) ? m.ships : undefined);
  const shown = (m: Tile) => !m.ships || BUILT_MODES.includes(m.id) || devMode;

  const SINGLE = [
    tile("solo", "mode.standard", "mode.soloAbout", "mode.soloKey", "family"),
    tile("gamemaster", "mode.gamemaster", "mode.gamemasterAbout", "mode.gamemasterKey", "mic"),
  ];
  const GROUPS = [
    { name: t("mode.collab"), tiles: [tile("rr-coop", "mode.rrCoop", "mode.rrCoopAbout", "mode.rrCoopKey", "puzzle", "1465")].filter(shown) },
    {
      name: t("mode.versus"),
      tiles: [
        tile("rr-competitive", "mode.rrCompetitive", "mode.rrCompetitiveAbout", "mode.rrCompetitiveKey", "crown", "1466"),
        tile("timed", "mode.timed", "mode.timedAbout", "mode.timedKey", "rocket", "1467"),
      ].filter(shown),
    },
  ].filter((g) => g.tiles.length);
  const MULTI = GROUPS.flatMap((g) => g.tiles);

  const KINDS = [
    { id: "single", name: t("mode.solo"), about: t("mode.soloKind"), key: t("mode.soloKey").toLowerCase(), icon: "family" as IconName },
    { id: "multi", name: t("mode.multi"), about: t("mode.multiAbout"), key: t("mode.multiKey").toLowerCase(), icon: "gamepad" as IconName },
  ].filter((k) => k.id === "single" || MULTI.length);

  const SHOWN = [...SINGLE, ...MULTI].map((m) => m.id);
  const kept = untrack(() => mode);
  const preset = (last: GameMode | null) => modePreset(kept, last, SHOWN, KINDS.length);
  let pick = $state<GameMode>(preset(null).pick);
  let kind = $state<Kind>(preset(null).kind);
  let stage = $state<Stage>(preset(null).stage);
  let section = $state<HTMLElement>();
  let nextButton = $state<HTMLButtonElement>();

  onMount(async () => {
    if (kept) return;
    const launch = new URLSearchParams(location.search).get("mode") as GameMode | null;
    ({ pick, kind } = preset(launch ?? (await fetchLastMode().catch(() => null))));
  });

  const list = $derived(stage === "single" ? SINGLE : MULTI);
  /** A pick of the other kind (the preset) gives way to the stage's first tile. */
  const chosen = $derived(list.some((m) => m.id === pick) ? pick : list[0].id);

  function next() {
    if (busy) return;
    if (stage === "kind") stage = kind;
    else onnext(chosen);
  }

  function back() {
    if (stage !== "kind" && KINDS.length > 1) stage = "kind";
    else onback();
  }

  const keys = $derived<Keys>(
    Object.fromEntries((stage === "kind" ? KINDS : list).map((m) => [m.key, { type: "letter", key: m.key }])),
  );

  // A tile's letter picks it and takes the ring; Enter/A is «Seguir» (primary), Space/X the ring's tile, Backspace back;
  // Esc falls through to the overlay.
  $effect(() =>
    pushScope({
      name: "mode",
      root: () => section,
      primary: () => nextButton,
      get keys() {
        return keys;
      },
      handle: (a) => {
        if (a.type === "letter") {
          const hit = (stage === "kind" ? KINDS : list).find((m) => m.key === a.key);
          if (!hit) return false;
          if (stage === "kind") kind = hit.id as Kind;
          else pick = hit.id as GameMode;
          if (section) show(section.querySelector<HTMLElement>(`[data-focus-id="${stage === "kind" ? "kind" : "mode"}-${hit.id}"]`), "mode", section);
        } else if (a.type === "back") back();
        else return false;
        return true;
      },
    }),
  );
</script>

<section class="mode-screen" bind:this={section}>
  <h1 class="title">{t(stage === "kind" ? "mode.kindTitle" : "mode.title")}</h1>

  {#if stage === "kind"}
    <div class="pick-row" role="radiogroup" data-line>
      {#each KINDS as k, i (k.id)}
        {@render card(`kind-${k.id}`, k.name, k.about, k.key, k.icon, k.id === kind, i, () => (kind = k.id as Kind))}
      {/each}
    </div>
  {:else if stage === "single"}
    <div class="pick-row" role="radiogroup" data-line>
      {#each SINGLE as m, i (m.id)}
        {@render card(`mode-${m.id}`, m.name, m.about, m.key, m.icon, m.id === chosen, i, () => (pick = m.id), unbuilt(m))}
      {/each}
    </div>
  {:else}
    <div class="groups" role="radiogroup">
      {#each GROUPS as g, gi (g.name)}
        <div class="group glass-light">
          <p class="label pick-heading">{g.name}</p>
          <div class="pick-row" data-line>
            {#each g.tiles as m, i (m.id)}
              {@render card(`mode-${m.id}`, m.name, m.about, m.key, m.icon, m.id === chosen, gi * 2 + i, () => (pick = m.id), unbuilt(m), true)}
            {/each}
          </div>
        </div>
      {/each}
    </div>
  {/if}

  <div class="pick-row actions" data-line>
    <button class="secondary" onclick={back} disabled={busy} data-focus-id="back"><Icon name="back" /> {t("action.back")} <Prompt action="back" /></button>
    <button class="candy" bind:this={nextButton} onclick={next} disabled={busy} data-focus-default data-focus-id="next"><Icon name="next" /> {t("action.next")} <Prompt action="confirm" /></button>
  </div>
</section>

{#snippet card(id: string, name: string, about: string, key: string, glyph: IconName, on: boolean, i: number, pickIt: () => void, ships?: string, local = false)}
  <OptionButton
    class="card"
    {on}
    style="--i:{i + 1}"
    role="radio"
    aria-checked={on}
    onclick={pickIt}
    disabled={busy}
    data-focus-id={id}
    caption={name}
  >
    {#snippet icon()}<Icon name={glyph} />{/snippet}
    {#snippet chip()}<Prompt action={{ type: "letter", key }} hold />{/snippet}
    {#if local}<span class="label local">{t("mode.local")}</span>{/if}
    <span class="label">{about}</span>
    {#if ships}<span class="label warn">{`PLACEHOLDER(${ships})`}</span>{/if}
  </OptionButton>
{/snippet}

<style>
  .mode-screen {
    position: absolute;
    inset: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: calc(1.6 * var(--u));
    padding: var(--safe-y) var(--safe-x);
    text-align: center;
  }
  .title {
    animation: arrive 0.6s var(--spring) backwards;
  }
  .groups {
    display: flex;
    gap: calc(2.4 * var(--u));
    align-items: stretch;
  }
  .group {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: calc(0.8 * var(--u));
    padding: calc(1 * var(--u)) calc(1.6 * var(--u)) calc(1.6 * var(--u));
    border: 1px dashed var(--slate-600);
    border-radius: calc(1.4 * var(--u));
  }
  .group .pick-heading {
    margin: 0;
  }
  .group .pick-row {
    align-items: stretch;
  }
  :global(.card) {
    min-width: calc(24 * var(--u));
    max-width: calc(30 * var(--u));
  }
  .local {
    color: var(--sky);
  }
  .warn {
    color: var(--amber);
  }
  .actions {
    margin-top: calc(1 * var(--u));
    align-items: center;
    animation: arrive 0.5s 0.5s var(--spring) backwards;
  }
</style>
