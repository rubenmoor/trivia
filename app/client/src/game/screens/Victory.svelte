<script lang="ts">
  // «¡Ganaron!»: the full tower with its crown, the finale fireworks, the last answer. rr-coop: every player on top;
  // rr-competitive: «¡Gana Ana!», the winner's tower big, the others' final tracks (plan 163).
  import { t } from "../../lib/i18n.ts";
  import type { Game } from "../../lib/types.ts";
  import AnswerPanel from "../AnswerPanel.svelte";
  import Fireworks from "../Fireworks.svelte";
  import Prompt from "../Prompt.svelte";
  import SeatTag from "../SeatTag.svelte";
  import Tower from "../Tower.svelte";
  import Tracks from "../Tracks.svelte";
  import { seatBlocks, seatNames } from "../seats.ts";

  let { game, levels, busy, onhome }: { game: Game; levels: number; busy: boolean; onhome: () => void } = $props();

  /** Names on the team line before «y n más»: one line at Deck size. */
  const TEAM_NAMES = 4;

  const session = $derived(game.session);
  const competitive = $derived(session?.mode === "rr-competitive");
  const winner = $derived(session?.seats.findIndex((x) => x.status === "won") ?? -1);
  /** Won as the last one standing, not at the top (decision 278). */
  const standing = $derived(game.last?.correct === false);
  const others = $derived(session?.seats.map((_, i) => i).filter((i) => i !== winner) ?? []);
</script>

<Fireworks mode="finale" />
<section class="screen result victory">
  {#if competitive && session && winner >= 0}
    <div class="stack">
      <Tower filled={seatBlocks(session, winner, levels, !standing)} {levels} drop={!standing} />
      <SeatTag {session} seat={winner} />
    </div>
  {:else}
    <Tower filled={levels} {levels} drop />
  {/if}
  <div class="stack">
    {#if competitive && session && winner >= 0}
      <h1 class="title big gold">{t("screen.victory.winner", { name: session.seats[winner].player ?? winner + 1 })}</h1>
      {#if standing}<p class="milestone">{t("screen.victory.standing")}</p>{/if}
      {#if others.length}<Tracks {session} {levels} seats={others} final />{/if}
    {:else}
      <h1 class="title big gold">{t("screen.victory.title")}</h1>
    {/if}
    {#if game.session?.mode === "rr-coop"}<p class="milestone">{t("screen.victory.team", { names: seatNames(game.session, TEAM_NAMES) })}</p>
    {:else if !competitive && game.player}<p class="milestone">{t("screen.victory.top", { name: game.player })}</p>{/if}
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
