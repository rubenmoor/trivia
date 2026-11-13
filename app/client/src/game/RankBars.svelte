<script lang="ts">
  // The rank of every seat with a player at a finished game (plan 198, decision 593): one `RankBar` each, read after
  // mount; nothing where the game counts nothing. Never blocks anything. `names`: a session, each bar names its player.
  import { onMount } from "svelte";
  import type { RankStep } from "../engine/career.ts";
  import { fetchRankSteps } from "../lib/api.ts";
  import { buildInfo } from "../lib/build.ts";
  import RankBar from "./RankBar.svelte";

  let { names = false }: { names?: boolean } = $props();

  let steps = $state<RankStep[]>([]);

  onMount(async () => {
    if (buildInfo().demo) return;
    steps = await fetchRankSteps().catch((e: unknown) => (console.error("career:rank", e), []));
  });
</script>

{#if steps.length}
  <div class="ranks">
    {#each steps as s (s.name)}<RankBar from={s.from} to={s.to} name={names ? s.name : undefined} />{/each}
  </div>
{/if}

<style>
  .ranks {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: calc(0.6 * var(--u));
    max-width: calc(62 * var(--u));
  }
</style>
