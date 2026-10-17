<script lang="ts">
  // The Mode screens (plans/04-ui-tv-display.md, "Mode"; MD-7, decision 314), between Player and the age screen: first
  // «Solo o en grupo» or «Multijugador», then the mode itself: standard or gamemaster mode, or the multiplayer modes in
  // two groups (collaborative: rr-coop; competitive: rr-competitive, timed), one pick. Only the built modes show (dev mode
  // shows the unbuilt ones marked, decision 293); with no multiplayer mode to show, the first step is skipped.
  // Preset: `?mode=`, else the player's newest game's mode. «Seguir» goes on, Back goes a step back.
  import { onMount, untrack } from "svelte";
  import { BUILT_MODES, fetchPlayerMode } from "../../lib/api.ts";
  import { devMode } from "../../lib/desktop.ts";
  import { t } from "../../lib/i18n.ts";
  import type { TextKey } from "../../locales/es.ts";
  import { pushScope, type Keys } from "../../lib/input.svelte.ts";
  import type { GameMode } from "../../lib/types.ts";
  import { isSession } from "../choiceDraft.ts";
  import Icon, { type IconName } from "../Icon.svelte";
  import Prompt from "../Prompt.svelte";

  let {
    player,
    busy,
    mode,
    onnext,
    onback,
  }: {
    player: string;
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

  type Stage = "kind" | "single" | "multi";
  const start = untrack(() => mode);
  let pick = $state<GameMode>(start ?? "gamemaster");
  const startKind = start && isSession(start) && MULTI.length ? "multi" : "single";
  let kind = $state<"single" | "multi">(startKind);
  // coming back from a later screen: the mode step the pick was made on
  let stage = $state<Stage>(start ? startKind : KINDS.length > 1 ? "kind" : "single");
  let section = $state<HTMLElement>();

  onMount(async () => {
    if (start) return;
    const launch = new URLSearchParams(location.search).get("mode") as GameMode | null;
    const last = launch ?? (await fetchPlayerMode(player).catch(() => null));
    if (!last || ![...SINGLE, ...MULTI].some((m) => m.id === last)) return;
    pick = last;
    kind = isSession(last) ? "multi" : "single";
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

  // A tile's letter picks it; Enter goes on (on a tile: picks), Backspace back; Esc falls through to the overlay.
  $effect(() =>
    pushScope({
      name: "mode",
      root: () => section,
      get keys() {
        return keys;
      },
      handle: (a) => {
        if (a.type === "letter") {
          const hit = (stage === "kind" ? KINDS : list).find((m) => m.key === a.key);
          if (!hit) return false;
          if (stage === "kind") kind = hit.id as "single" | "multi";
          else pick = hit.id as GameMode;
        } else if (a.type === "confirm") next();
        else if (a.type === "back") back();
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
        {@render card(`kind-${k.id}`, k.name, k.about, k.key, k.icon, k.id === kind, i, () => (kind = k.id as "single" | "multi"))}
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
              {@render card(`mode-${m.id}`, m.name, m.about, m.key, m.icon, m.id === chosen, gi * 2 + i, () => (pick = m.id), unbuilt(m))}
            {/each}
          </div>
        </div>
      {/each}
    </div>
  {/if}

  <div class="pick-row actions" data-line>
    <button class="secondary" onclick={back} disabled={busy} data-focus-id="back"><Icon name="back" /> {t("action.back")} <Prompt action="back" /></button>
    <button class="candy" onclick={next} disabled={busy} data-focus-default data-focus-id="next"><Icon name="next" /> {t("action.next")} <Prompt action="confirm" /></button>
  </div>
</section>

{#snippet card(id: string, name: string, about: string, key: string, icon: IconName, on: boolean, i: number, pickIt: () => void, ships?: string)}
  <button
    class="pick-tile card glass"
    class:on
    style:--i={i + 1}
    role="radio"
    aria-checked={on}
    onclick={pickIt}
    disabled={busy}
    data-focus-id={id}
  >
    <Prompt action={{ type: "letter", key }} hold />
    <span class="pick-name"><Icon name={icon} /> {name}</span>
    <span class="label">{about}</span>
    {#if ships}<span class="label warn">{`PLACEHOLDER(${ships})`}</span>{/if}
  </button>
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
  .card {
    min-width: calc(24 * var(--u));
    max-width: calc(30 * var(--u));
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
