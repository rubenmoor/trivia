<script lang="ts">
  // «¡Correcto!»: fireworks, the answer and its fun fact; next the Level screen. In a session the answerer's tag.
  import { t } from "../../lib/i18n.ts";
  import type { SessionView } from "../../lib/seats.ts";
  import type { Game } from "../../lib/types.ts";
  import AnswerPanel from "../AnswerPanel.svelte";
  import Fireworks from "../Fireworks.svelte";
  import Prompt from "../Prompt.svelte";
  import SeatTag from "../SeatTag.svelte";

  let {
    last,
    busy,
    onnext,
    session = null,
  }: { last: NonNullable<Game["last"]>; busy: boolean; onnext: () => void; session?: SessionView | null } = $props();
</script>

<section class="screen result">
  <Fireworks />
  <h1 class="title good">{t("screen.result.correct")}</h1>
  {#if session && last.seat !== undefined}<SeatTag {session} seat={last.seat} />{/if}
  <AnswerPanel {last} />
  <button class="secondary hint" onclick={onnext} disabled={busy} data-focus-default>{t("action.next")} <Prompt action="confirm" /></button>
</section>

<style>
  .title {
    animation: arrive 0.6s var(--spring) backwards;
  }
  .good {
    color: var(--mint);
  }
  .hint {
    margin-top: calc(1.5 * var(--u));
  }
</style>
