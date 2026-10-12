<script lang="ts">
  // «Preguntas reportadas» (MD-6): the local report list, newest first, over the overlay. Offline;
  // «Copiar» puts plain text on the clipboard, else shows it selectable. ↑/↓ move, Esc/⌫ go back.
  import { t } from "../lib/i18n";
  import { focusControl, pushScope } from "../lib/input.svelte";
  import type { Report } from "../lib/types";
  import Prompt from "./Prompt.svelte";

  let { reports, onclose }: { reports: Report[]; onclose: () => void } = $props();

  let panel = $state<HTMLDivElement>();
  let backButton = $state<HTMLButtonElement>();
  let copied = $state(false);
  let failed = $state(false);

  const when = (iso: string) => iso.slice(0, 16).replace("T", " ");
  const answerOf = (r: Report) => r.answer ?? t("report.hidden");

  const text = $derived(
    reports
      .map((r) =>
        [
          `${when(r.reported_on)} · ${r.question_id}`,
          `${t("report.question")}: ${r.question ?? "—"}`,
          `${t("report.answer")}: ${answerOf(r)}`,
          `${t("report.player")}: ${r.player ?? "—"} · ${t("report.level", { n: r.level })}`,
          ...(r.note ? [r.note] : []),
        ].join("\n"),
      )
      .join("\n\n"),
  );

  async function copy() {
    try {
      await navigator.clipboard.writeText(text); // undefined outside a secure context (TV over the LAN)
      copied = true;
      failed = false;
    } catch {
      failed = true;
    }
  }

  $effect(() => {
    const pop = pushScope({
      name: "reports",
      modal: true,
      whileBusy: true,
      root: () => panel,
      handle: (a) => (a.type === "back" || a.type === "menu") && (onclose(), true),
    });
    focusControl(backButton);
    return pop;
  });
</script>

<div class="reports" bind:this={panel}>
  <header>
    <h2>{t("report.list")}</h2>
    <div class="buttons">
      {#if reports.length}
        <button class="secondary" onclick={copy}>{copied ? t("report.copied") : t("report.copy")}</button>
      {/if}
      <button class="candy" bind:this={backButton} onclick={onclose} data-focus-default>{t("action.back")} <Prompt action="menu" pad="back" /></button>
    </div>
  </header>
  {#if failed}
    <p class="hint">{t("report.copyFailed")}</p>
    <pre>{text}</pre>
  {:else if reports.length}
    <ol>
      {#each reports as r (`${r.game_id}:${r.question_id}`)}
        <!-- svelte-ignore a11y_no_noninteractive_tabindex -->
        <li tabindex="0" data-focusable>
          <p class="meta">{when(r.reported_on)} · <code>{r.question_id}</code> · {r.player ?? "—"} · {t("report.level", { n: r.level })}</p>
          <p class="question">{r.question ?? "—"}</p>
          <p class="answer">{t("report.answer")}: <b>{answerOf(r)}</b></p>
          {#if r.note}<p class="meta">{r.note}</p>{/if}
        </li>
      {/each}
    </ol>
  {:else}
    <p class="hint">{t("report.empty")}</p>
  {/if}
</div>

<style>
  .reports {
    position: fixed;
    inset: 0;
    z-index: 45;
    display: flex;
    flex-direction: column;
    gap: calc(1.2 * var(--u));
    padding: var(--safe-y) var(--safe-x);
    background: var(--night-700);
  }
  header {
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
  h2 {
    margin: 0;
    font-family: var(--font-display);
    font-size: calc(2.6 * var(--u));
    font-weight: 800;
  }
  .buttons {
    display: flex;
    gap: calc(1 * var(--u));
  }
  ol {
    display: flex;
    flex-direction: column;
    gap: calc(0.8 * var(--u));
    margin: 0;
    padding: 0;
    overflow-y: auto;
    list-style: none;
  }
  li {
    padding: calc(0.8 * var(--u)) calc(1.4 * var(--u));
    border: calc(0.18 * var(--u)) solid transparent;
    border-radius: calc(0.8 * var(--u));
    background: rgba(43, 54, 80, 0.5);
    outline: none;
  }
  li:focus,
  li:global([data-nav]) {
    border-color: var(--amber);
  }
  p {
    margin: 0;
  }
  .meta {
    font-size: calc(1 * var(--u));
    color: var(--slate-400);
  }
  .meta code {
    color: var(--slate-200);
    user-select: all;
  }
  .question {
    font-size: calc(1.4 * var(--u));
    font-weight: 700;
  }
  .answer {
    font-size: calc(1.2 * var(--u));
    color: var(--slate-200);
  }
  .hint {
    color: var(--slate-400);
  }
  pre {
    overflow: auto;
    margin: 0;
    padding: calc(1 * var(--u));
    border-radius: calc(0.8 * var(--u));
    background: rgba(5, 8, 16, 0.6);
    font-size: calc(1 * var(--u));
    white-space: pre-wrap;
    user-select: all;
  }
</style>
