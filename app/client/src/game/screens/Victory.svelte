<script lang="ts">
  // «¡Ganaron!»: the full tower with its crown, the finale fireworks, the last answer. rr-coop: every player on top.
  import { t } from "../../lib/i18n.ts";
  import type { Game } from "../../lib/types.ts";
  import AnswerPanel from "../AnswerPanel.svelte";
  import Fireworks from "../Fireworks.svelte";
  import Prompt from "../Prompt.svelte";
  import Tower from "../Tower.svelte";
  import { seatNames } from "../seats.ts";

  let { game, levels, busy, onhome }: { game: Game; levels: number; busy: boolean; onhome: () => void } = $props();

  /** Names on the team line before «y n más»: one line at Deck size. */
  const TEAM_NAMES = 4;
</script>

<Fireworks mode="finale" />
<section class="screen result victory">
  <Tower filled={levels} {levels} drop />
  <div class="stack">
    <h1 class="title big gold">{t("screen.victory.title")}</h1>
    {#if game.session?.mode === "rr-coop"}<p class="milestone">{t("screen.victory.team", { names: seatNames(game.session, TEAM_NAMES) })}</p>
    {:else if game.player}<p class="milestone">{t("screen.victory.top", { name: game.player })}</p>{/if}
    {#if game.last}<AnswerPanel last={game.last} />{/if}

    <button class="candy breathe" onclick={onhome} disabled={busy} data-focus-default>{t("action.home")} <Prompt action="confirm" /></button>
  </div>
</section>

<style>
  p {
    margin: 0;
  }
  .title.big {
    font-size: calc(7 * var(--u));
  }
  .title {
    animation: arrive 0.6s var(--spring) backwards;
  }
  .gold {
    color: var(--amber);
  }
  .milestone {
    font-family: var(--font-display);
    font-size: calc(2 * var(--u));
    font-weight: 700;
    color: var(--sky);
    animation: arrive 0.7s 0.9s var(--spring) backwards;
  }
  .stack {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: calc(1.4 * var(--u));
  }
  .victory {
    flex-direction: row;
    justify-content: space-evenly;
  }
</style>
