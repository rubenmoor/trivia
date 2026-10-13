<script lang="ts">
  // «Preguntas marcadas» (GM-5, decision 60): the flagged questions with their notes, newest first, over the overlay.
  // «Copiar» per flag or all puts report text (plan 93) on the clipboard, else shows it selectable; «Enviar» sends it
  // from the shell (one request per flag, on the click only). ↑/↓/←/→ move, Esc/⌫ go back.
  import { markReported } from "../lib/api.ts";
  import { report, type ReportResult } from "../lib/desktop.ts";
  import { t } from "../lib/i18n.ts";
  import { focusControl, pushScope } from "../lib/input.svelte.ts";
  import type { Flagged } from "../lib/types.ts";
  import Prompt from "./Prompt.svelte";
  import { consent, poolsFor, reportFields, reportText } from "./report.ts";

  let { flags = $bindable(), onclose }: { flags: Flagged[]; onclose: () => void } = $props();

  type Failed = Extract<ReportResult, { ok: false }>;

  let panel = $state<HTMLDivElement>();
  let backButton = $state<HTMLButtonElement>();
  /** "*" for all, else a question id. */
  let copied = $state<string | null>(null);
  /** The text that didn't reach the clipboard, shown selectable. */
  let fallback = $state<string | null>(null);
  let canSend = $state(false);
  /** In memory only (plan 93): a flag being sent or its last failure. */
  let sending = $state<Record<string, "sending" | Failed>>({});
  /** Flags waiting for the privacy confirm. */
  let asking = $state<Flagged[] | null>(null);
  let dialog = $state<HTMLDivElement>();
  let confirmButton = $state<HTMLButtonElement>();

  const when = (iso: string) => iso.slice(0, 16).replace("T", " ");
  const answerOf = (f: Flagged) => f.answer ?? t("flag.hidden");
  const meta = (f: Flagged) =>
    [f.player ?? "—", ...(f.level ? [t("flag.level", { n: f.level })] : []), f.locale ?? "es"].join(" · ");
  const unsent = $derived(flags.filter((f) => !f.reported_on));
  const busy = $derived(Object.values(sending).includes("sending"));

  void report?.available().then((ok) => (canSend = ok), () => {});

  async function copy(list: Flagged[], key: string) {
    const text = reportText(list, await poolsFor(list));
    try {
      await navigator.clipboard.writeText(text); // undefined outside a secure context (TV over the LAN)
      copied = key;
      fallback = null;
    } catch {
      fallback = text;
    }
  }

  function send(list: Flagged[]) {
    if (!list.length || busy) return;
    if (consent.given) void sendEach(list);
    else asking = list;
  }

  function confirmSend() {
    const list = asking ?? [];
    consent.given = true;
    asking = null;
    void sendEach(list);
  }

  /** One request per flag, stops at the first failure. */
  async function sendEach(list: Flagged[]) {
    if (!report) return;
    const pools = await poolsFor(list);
    for (const f of list) {
      const id = f.question_id;
      sending[id] = "sending";
      const r = await report.send(reportFields(f, pools)).catch((): Failed => ({ ok: false, status: 0, error: "unavailable" }));
      if (!r.ok) {
        sending[id] = r;
        return;
      }
      flags = await markReported(id).catch(() => flags);
      delete sending[id];
    }
  }

  function reason(r: Failed): string {
    if (r.status === 0 && (r.error === "no_connection" || r.error === "timeout")) return t("flag.sendOffline");
    if (r.status === 429) return t("flag.sendTomorrow");
    if (r.status === 503) return t("flag.sendClosed");
    return t("flag.sendFailed");
  }

  $effect(() => {
    const pop = pushScope({
      name: "flags",
      modal: true,
      whileBusy: true,
      root: () => panel,
      handle: (a) => (a.type === "back" || a.type === "menu") && (onclose(), true),
    });
    focusControl(backButton);
    return pop;
  });

  $effect(() => {
    if (!asking) return;
    const pop = pushScope({
      name: "flags-send",
      modal: true,
      whileBusy: true,
      root: () => dialog,
      handle: (a) => (a.type === "back" || a.type === "menu") && ((asking = null), true),
    });
    focusControl(confirmButton);
    return pop;
  });
</script>

<div class="flags" bind:this={panel}>
  <header>
    <h2>{t("flag.list")}</h2>
    <div class="buttons">
      {#if flags.length}
        <button class="secondary" onclick={() => copy(flags, "*")}>{copied === "*" ? t("flag.copied") : t("flag.copyAll")}</button>
      {/if}
      {#if canSend && unsent.length}
        <button class="secondary" onclick={() => send(unsent)} disabled={busy}>{t("flag.sendAll")}</button>
      {/if}
      <button class="candy" bind:this={backButton} onclick={onclose} data-focus-default>{t("action.back")} <Prompt action="menu" pad="back" /></button>
    </div>
  </header>
  {#if fallback !== null}
    <p class="hint">{t("flag.copyFailed")}</p>
    <pre>{fallback}</pre>
  {/if}
  {#if flags.length}
    <ol>
      {#each flags as f (f.question_id)}
        {@const st = sending[f.question_id]}
        <li>
          <p class="meta">{when(f.flagged_on)} · <code>{f.question_id}</code> · {meta(f)}</p>
          <p class="question">{f.question ?? "—"}</p>
          <p class="answer">{t("flag.answer")}: <b>{answerOf(f)}</b></p>
          {#if f.note}<p class="note">{t("flag.note")}: {f.note}</p>{/if}
          <div class="actions">
            <button class="secondary small" onclick={() => copy([f], f.question_id)}>
              {copied === f.question_id ? t("flag.copied") : t("flag.copy")}
            </button>
            {#if canSend}
              <button class="secondary small" onclick={() => send([f])} disabled={busy}>{t("flag.send")}</button>
            {/if}
            {#if st === "sending"}
              <span class="status">{t("flag.sending")}</span>
            {:else if st}
              <span class="status failed">{reason(st)}</span>
            {:else if f.reported_on}
              <span class="status sent">{t("flag.sent", { date: f.reported_on.slice(0, 10) })}</span>
            {/if}
          </div>
        </li>
      {/each}
    </ol>
  {:else}
    <p class="hint">{t("flag.empty")}</p>
  {/if}
  {#if asking}
    <div class="backdrop">
      <div class="dialog" bind:this={dialog} role="alertdialog" aria-labelledby="send-title">
        <h2 id="send-title">{t("flag.sendTitle")}</h2>
        <p>{t("flag.privacy1")}</p>
        <p>{t("flag.privacy2")}</p>
        <div class="buttons">
          <button class="secondary" onclick={() => (asking = null)}>{t("action.cancel")} <Prompt action="menu" pad="back" /></button>
          <button class="candy" bind:this={confirmButton} onclick={confirmSend}>{t("flag.send")} <Prompt action="confirm" /></button>
        </div>
      </div>
    </div>
  {/if}
</div>

<style>
  .flags {
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
  li:focus-within {
    border-color: var(--amber);
  }
  .actions {
    display: flex;
    align-items: center;
    gap: calc(0.8 * var(--u));
    margin-top: calc(0.4 * var(--u));
  }
  .small {
    padding: calc(0.3 * var(--u)) calc(1 * var(--u));
    font-size: calc(1 * var(--u));
  }
  .status {
    font-size: calc(1 * var(--u));
    color: var(--slate-400);
  }
  .sent {
    color: var(--mint);
  }
  .failed {
    color: var(--coral);
  }
  .backdrop {
    position: fixed;
    inset: 0;
    display: grid;
    place-items: center;
    background: var(--dim);
  }
  .dialog {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: calc(1 * var(--u));
    max-width: calc(60 * var(--u));
    padding: calc(2.4 * var(--u));
    border: 1px solid var(--slate-600);
    border-radius: calc(1.6 * var(--u));
    background: var(--night-700);
    box-shadow: 0 calc(1.5 * var(--u)) calc(4 * var(--u)) rgba(0, 0, 0, 0.6);
    text-align: center;
  }
  .dialog p {
    color: var(--slate-200);
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
  .note {
    font-size: calc(1.2 * var(--u));
    color: var(--amber);
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
