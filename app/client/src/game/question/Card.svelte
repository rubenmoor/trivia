<script lang="ts">
  // The question card (04-ui-tv-display.md): topic after Cambiazo, the question, replay; below it Soplo's notes
  // (09-jokers.md) and the missing-media line.
  import { isOurs } from "../../engine/pool.ts";
  import { t } from "../../lib/i18n.ts";
  import { displayName, questionLocale } from "../../lib/names.svelte.ts";
  import type { Game, JokerEvent } from "../../lib/types.ts";
  import Icon from "../Icon.svelte";
  import Prompt from "../Prompt.svelte";
  import { cardFlip, crossfade } from "../swap.ts";

  let {
    question,
    swappedBy,
    mediaFailed,
    sweeping,
    replayOff,
    onreplay,
  }: {
    question: NonNullable<Game["question"]>;
    swappedBy: JokerEvent | null;
    mediaFailed: boolean;
    /** «Paso»: swept off to the side (JK-6). */
    sweeping: boolean;
    /** A joker dialog or mode is up: no replay prompt. */
    replayOff: boolean;
    onreplay: () => void;
  } = $props();

  const media = $derived(question.media);
  /** Long questions shrink one step instead of growing to three lines (10, "Scale"). */
  const long = $derived(question.question.length > 110);
</script>

<header class="card glass-strong" class:long class:sweeping in:cardFlip|global={{ side: "in" }} out:cardFlip|global={{ side: "out" }}>
  {#if question.swapped_to}
    <p class="topic label" class:fresh={swappedBy?.joker === "category"}>{t("screen.question.topic", { name: displayName("subcategory", question.swapped_to) })}</p>
  {/if}
  <h1 lang={questionLocale()}>{question.question}</h1>
  {#if media.type !== "image"}
    <button class="replay" onclick={onreplay}>
      <Icon name={media.type === "audio" ? "speaker" : "film"} /> {t("screen.question.replay")} <Prompt action="replay" off={replayOff} />
    </button>
  {/if}
</header>

<div class="middle" class:sweeping out:crossfade|global>
  {#if question.hints.length}
    <div class="notes" lang={questionLocale()}>
      {#each question.hints as hint, i (i)}
        <p class="note" style:--tilt="{[-2.5, 1.8, -1.2][i]}deg" class:strong={i === 2}>
          <span class="note-label">{t("screen.question.hint", { n: i + 1 })}</span>{hint}
        </p>
      {/each}
    </div>
  {/if}
  {#if mediaFailed || (!media.file_url && media.type !== "audio" && isOurs(question.id))}
    <p class="media-missing">{t("screen.question.mediaMissing")}</p>
  {/if}
</div>

<style>
  .card {
    max-width: 70%;
    padding: calc(1.3 * var(--u)) calc(2.4 * var(--u));
    text-align: center;
    animation: rise 0.5s var(--spring) backwards;
  }
  h1 {
    margin: 0;
    font-size: calc(2.4 * var(--u));
    font-weight: 800;
    line-height: 1.25;
    text-wrap: balance;
  }
  .long h1 {
    font-size: calc(2.1 * var(--u));
  }
  .replay {
    display: inline-flex;
    align-items: center;
    gap: calc(0.5 * var(--u));
    margin-top: calc(0.6 * var(--u));
    padding: calc(0.2 * var(--u)) calc(0.8 * var(--u));
    border: 1px solid var(--glass-line);
    border-radius: calc(0.8 * var(--u));
    background: none;
    font-size: calc(1.1 * var(--u));
    color: var(--slate-200);
  }
  /* «Paso»: everything on the question is swept off to the side (JK-6); the answers in screens/Question.svelte. */
  .sweeping {
    transition:
      transform var(--sweep) cubic-bezier(0.6, 0, 0.9, 0.5),
      opacity var(--sweep);
    transform: translateX(-120vw) rotate(-8deg);
    opacity: 0;
  }
  .middle {
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: center;
    gap: calc(0.8 * var(--u));
  }
  .topic {
    margin: 0 0 calc(0.3 * var(--u));
    color: var(--sky);
  }
  .topic.fresh {
    animation: topic-pop 0.7s 0.65s var(--spring) backwards;
  }
  @keyframes topic-pop {
    from {
      opacity: 0;
      transform: scale(2.2);
    }
  }
  .notes {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: calc(1 * var(--u));
    max-width: 70vw;
  }
  .note {
    margin: 0;
    max-width: calc(26 * var(--u));
    padding: calc(0.7 * var(--u)) calc(1 * var(--u));
    border-radius: calc(0.4 * var(--u));
    background: var(--cream);
    color: var(--ink);
    font-size: calc(1.3 * var(--u));
    font-weight: 700;
    line-height: 1.25;
    box-shadow: 0 calc(0.5 * var(--u)) calc(1 * var(--u)) rgba(0, 0, 0, 0.4);
    transform: rotate(var(--tilt));
    animation: note-in 0.5s var(--spring) backwards;
  }
  .note.strong {
    background: #ffe7a8;
  }
  .note-label {
    display: block;
    font-family: var(--font-display);
    font-size: calc(0.9 * var(--u));
    color: var(--amber-deep);
    text-transform: uppercase;
    letter-spacing: 0.08em;
  }
  .media-missing {
    margin: 0;
    padding: calc(0.2 * var(--u)) calc(0.6 * var(--u));
    border: calc(0.15 * var(--u)) dashed var(--pink);
    border-radius: calc(0.6 * var(--u));
    color: #ffb8ec;
    background: rgba(60, 10, 50, 0.55);
    font-size: var(--u);
  }

  @keyframes note-in {
    from {
      opacity: 0;
      transform: translateY(calc(-2 * var(--u))) rotate(-10deg) scale(0.7);
    }
  }
</style>
