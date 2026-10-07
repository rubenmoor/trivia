<script lang="ts">
  // Review tool (plans/08-review-tool.md): one question per screen, single-key decisions.
  import { onMount, tick } from "svelte";
  import { fetchQuestions, pickMedia, saveReview, searchMedia, setDifficulty } from "../lib/api";
  import type { Decision, Question, Review, Slot } from "../lib/types";
  import MediaPanel from "./MediaPanel.svelte";
  import RevisionPanel from "./RevisionPanel.svelte";

  // URL: ?batch=pilot&id=q-0123. The id follows the current question, so a reload
  // (or a bookmark) comes back to it. Decisions themselves live in data/questions.json.
  const params = new URLSearchParams(location.search);
  const batch = params.get("batch");
  // /review/q-0123: just that one question (linked from the game's admin overlay).
  const singleId = decodeURIComponent(location.pathname.match(/^\/review\/([^/]+)/)?.[1] ?? "") || null;
  const startId = singleId ?? params.get("id");
  // ?debug=keys shows what the browser reports for each key press (for layout problems).
  const debugKeys = params.get("debug") === "keys";
  let lastKey = $state("");

  let questions = $state<Question[]>([]);
  let index = $state(0);
  let loading = $state(true);
  let error = $state<string | null>(null);
  let finished = $state(false);
  let showScores = $state(false);
  let feedbackOpen = $state(false);
  let feedbackText = $state("");
  let feedbackBox = $state<HTMLTextAreaElement>();
  let searchOpen = $state(false);
  let searchText = $state("");
  let searchBox = $state<HTMLInputElement>();
  let mediaWorking = $state(false);
  /** Media downloads that run in the background after an approval. */
  let downloads = $state(0);
  /** Which slot's alternatives are shown; digits and "m" act on it. */
  let openSlot = $state<Slot | null>(null);
  /** After "d": the next digit sets the difficulty. */
  let difficultyPending = $state(false);
  let toast = $state<string | null>(null);
  let busy = false;
  let toastTimer: ReturnType<typeof setTimeout> | undefined;
  /** Failed API calls stay visible until dismissed (also from background downloads). */
  let errors = $state<{ id: number; time: string; what: string; message: string }[]>([]);
  let errorSeq = 0;

  function reportError(what: string, e: unknown) {
    const message = e instanceof Error ? e.message : String(e);
    const time = new Date().toLocaleTimeString();
    errors = [...errors, { id: ++errorSeq, time, what, message }];
  }
  const undoStack: { id: string; previous: Review | null }[] = [];

  const current = $derived(questions[index]);
  const counts = $derived({
    approved: questions.filter((q) => q.status === "approved").length,
    rejected: questions.filter((q) => q.status === "rejected").length,
    needs_work: questions.filter((q) => q.status === "needs_work").length,
    draft: questions.filter((q) => q.status === "draft").length,
  });

  const LABELS: Record<Decision, string> = {
    approved: "✓ approved",
    rejected: "✗ rejected",
    needs_work: "✎ feedback saved",
  };

  onMount(async () => {
    try {
      questions = await fetchQuestions(batch);
      if (singleId) questions = questions.filter((q) => q.id === singleId);
      const fromUrl = questions.findIndex((q) => q.id === startId);
      const firstOpen = questions.findIndex((q) => q.status === "draft");
      finished = !singleId && questions.length > 0 && fromUrl === -1 && firstOpen === -1;
      index = fromUrl !== -1 ? fromUrl : Math.max(firstOpen, 0);
    } catch (e) {
      error = e instanceof Error ? e.message : String(e);
    } finally {
      loading = false;
    }
  });

  // Warm the browser cache with the next question's suggested previews.
  $effect(() => {
    const next = questions[(index + 1) % Math.max(questions.length, 1)];
    for (const c of [next?.media_candidates?.[0], next?.background_candidates?.[0]]) {
      if (c?.type === "image" && c.preview_url) new Image().src = c.preview_url;
    }
  });

  $effect(() => {
    if (singleId) return;
    const id = !loading && !finished ? questions[index]?.id : null;
    const url = new URL(location.href);
    if (id) url.searchParams.set("id", id);
    else url.searchParams.delete("id");
    if (url.href !== location.href) history.replaceState(null, "", url);
  });

  function flash(message: string) {
    toast = message;
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => (toast = null), 1200);
  }

  /** Next undecided question after `from`, wrapping around; -1 if none is left. */
  function nextOpen(from: number): number {
    for (let step = 1; step <= questions.length; step++) {
      const i = (from + step) % questions.length;
      if (questions[i].status === "draft") return i;
    }
    return -1;
  }

  async function store(i: number, review: Parameters<typeof saveReview>[1]) {
    const updated = await saveReview(questions[i].id, review);
    questions[i] = updated;
  }

  /** Slots where approving should pick the suggestion (candidate 1) first. */
  function slotsNeedingSuggestion(q: Question): Slot[] {
    const out: Slot[] = [];
    if (!q.media.file_url && (q.media_candidates?.length ?? 0) > 0) out.push("media");
    if (q.background && !q.background.file_url && (q.background_candidates?.length ?? 0) > 0) out.push("background");
    return out;
  }

  function candidatesOf(q: Question, slot: Slot) {
    return (slot === "media" ? q.media_candidates : q.background_candidates) ?? [];
  }

  function toggle(slot: Slot) {
    if (slot === "background" && !current?.background) return;
    openSlot = openSlot === slot ? null : slot;
  }

  /** Download the suggestions of an approved question without blocking the review. */
  async function pickSuggestionsInBackground(id: string, slots: Slot[]) {
    for (const slot of slots) {
      downloads++;
      try {
        const updated = await pickMedia(id, 0, slot);
        const j = questions.findIndex((q) => q.id === id);
        if (j !== -1) questions[j] = { ...updated, review: questions[j].review, status: questions[j].status };
      } catch (e) {
        reportError(`downloading ${slot === "media" ? "media" : "background"} for ${id}`, e);
      } finally {
        downloads--;
      }
    }
  }

  async function decide(decision: Decision, feedback: string | null = null) {
    if (busy || mediaWorking || !current) return;
    busy = true;
    const i = index;
    let pushed = false;
    try {
      const suggestions = decision === "approved" ? slotsNeedingSuggestion(questions[i]) : [];
      undoStack.push({ id: questions[i].id, previous: questions[i].review });
      pushed = true;
      await store(i, { decision, feedback });
      flash(LABELS[decision]);
      if (suggestions.length) pickSuggestionsInBackground(questions[i].id, suggestions);
      const next = singleId ? i : nextOpen(i);
      openSlot = null;
      if (next === -1) finished = true;
      else index = next;
    } catch (e) {
      if (pushed) undoStack.pop();
      reportError(`saving “${decision.replace("_", " ")}” for ${questions[i]?.id}`, e);
    } finally {
      busy = false;
    }
  }

  async function undo() {
    const last = undoStack.pop();
    if (!last || busy) return;
    busy = true;
    try {
      const i = questions.findIndex((q) => q.id === last.id);
      await store(i, last.previous);
      index = i;
      finished = false;
      flash("↶ undone");
    } catch (e) {
      reportError(`undo for ${last.id}`, e);
    } finally {
      busy = false;
    }
  }

  async function openFeedback() {
    feedbackText = current?.review?.feedback ?? "";
    feedbackOpen = true;
    await tick();
    feedbackBox?.focus();
  }

  function submitFeedback() {
    const text = feedbackText.trim();
    if (!text) return flash("Feedback is empty");
    feedbackOpen = false;
    decide("needs_work", text);
  }

  async function mediaAction(label: string, what: string, run: () => Promise<Question>) {
    if (mediaWorking || !current) return;
    const i = index;
    mediaWorking = true;
    try {
      questions[i] = await run();
      flash(label);
    } catch (e) {
      reportError(`${what} for ${questions[i]?.id}`, e);
    } finally {
      mediaWorking = false;
    }
  }

  function pick(slot: Slot, n: number) {
    if (!current || n >= candidatesOf(current, slot).length) return;
    const id = current.id;
    // The alternatives stay open, so the picked one is visibly marked; c/b/Esc closes them.
    const what = slot === "media" ? "media" : "background";
    mediaAction(`🖼 ${what} ${n + 1} picked`, `picking ${what} ${n + 1}`, () => pickMedia(id, n, slot));
  }

  /** "m" searches the slot whose alternatives are open; the media slot otherwise. */
  const searchSlot = $derived<Slot>(openSlot ?? "media");

  async function openSearch() {
    searchText = (searchSlot === "background" ? current?.background?.query : current?.media.query) ?? "";
    searchOpen = true;
    await tick();
    searchBox?.select();
  }

  function submitSearch() {
    const id = current?.id;
    const query = searchText.trim();
    if (!id || !query) return;
    const slot = searchSlot;
    searchOpen = false;
    openSlot = slot;
    mediaAction("🔍 new candidates", `searching Commons for “${query}”`, () => searchMedia(id, query, slot));
  }

  /** 1–8 as they are; 0 → 1 and 9 → 10, so every level is one key. */
  function digitToDifficulty(digit: number) {
    return digit === 0 ? 1 : digit === 9 ? 10 : digit;
  }

  async function changeDifficulty(difficulty: number) {
    if (!current) return;
    const i = index;
    try {
      const updated = await setDifficulty(questions[i].id, difficulty);
      questions[i] = { ...questions[i], difficulty: updated.difficulty, difficulty_original: updated.difficulty_original };
      flash(`difficulty ${difficulty}/10`);
    } catch (e) {
      reportError(`setting difficulty for ${questions[i]?.id}`, e);
    }
  }

  function move(delta: number) {
    if (!questions.length) return;
    finished = false;
    openSlot = null;
    difficultyPending = false;
    index = (index + delta + questions.length) % questions.length;
  }

  function onKey(event: KeyboardEvent) {
    if (debugKeys) {
      const mods = ["ctrlKey", "altKey", "metaKey", "shiftKey"].filter((m) => event[m as keyof KeyboardEvent]);
      lastKey = `key=${JSON.stringify(event.key)} code=${JSON.stringify(event.code)} keyCode=${event.keyCode} mods=[${mods.join(",")}] target=${(event.target as HTMLElement)?.tagName}`;
    }
    if (event.ctrlKey || event.metaKey || event.altKey) return;
    if (searchOpen) {
      if (event.key === "Enter") {
        event.preventDefault();
        submitSearch();
      } else if (event.key === "Escape") {
        searchOpen = false;
      }
      return;
    }
    if (feedbackOpen) {
      if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        submitFeedback();
      } else if (event.key === "Escape") {
        feedbackOpen = false;
      }
      return;
    }
    // event.code is the physical key, so this works on every keyboard layout
    // (e.g. AZERTY, where the top row gives "&é\"'(-" without Shift).
    const anyDigit = /^(?:Digit|Numpad)([0-9])$/.exec(event.code)?.[1] ?? (/^[0-9]$/.test(event.key) ? event.key : null);
    if (difficultyPending) {
      event.preventDefault();
      difficultyPending = false;
      if (anyDigit !== null) changeDifficulty(digitToDifficulty(Number(anyDigit)));
      else flash("difficulty unchanged");
      return;
    }
    const digit = anyDigit !== null && /[1-6]/.test(anyDigit) ? anyDigit : null;
    if (digit) {
      event.preventDefault();
      if (!openSlot) return flash(`Press c first to show the alternatives`);
      return pick(openSlot, Number(digit) - 1);
    }
    if (openSlot && event.key === "Escape") {
      openSlot = null;
      return;
    }
    const actions: Record<string, () => void> = {
      a: () => decide("approved"),
      r: () => decide("rejected"),
      f: openFeedback,
      m: openSearch,
      d: () => {
        difficultyPending = true;
        flash("difficulty: press 0–9 (0 = 1, 9 = 10)");
      },
      c: () => toggle("media"),
      b: () => toggle("background"),
      s: () => (showScores = !showScores),
      u: undo,
      ArrowRight: () => move(1),
      ArrowLeft: () => move(-1),
    };
    const action = actions[event.key];
    if (action) {
      event.preventDefault(); // keeps "f" and "m" out of the text boxes
      action();
    }
  }

  const options = $derived(current ? [current.answer, ...current.wrong_answers] : []);
</script>

<svelte:window onkeydown={onKey} />

<main>
  {#if loading}
    <p class="center">Loading…</p>
  {:else if error}
    <p class="center error">{error}</p>
  {:else if questions.length === 0}
    <p class="center">
      {singleId ? `No question “${singleId}”` : `No questions${batch ? ` in batch “${batch}”` : ""}`}.
    </p>
  {:else if finished}
    <section class="summary">
      <h1>Batch done{batch ? `: ${batch}` : ""}</h1>
      <ul>
        <li><b>{counts.approved}</b> approved</li>
        <li><b>{counts.needs_work}</b> need work</li>
        <li><b>{counts.rejected}</b> rejected</li>
      </ul>
      <p>
        Kept: <b>{Math.round(((counts.approved + counts.needs_work) / questions.length) * 100)} %</b>
        ({counts.approved + counts.needs_work} of {questions.length}, counting “needs work” as kept)
      </p>
      <p class="muted">← / → to look at questions again · u to undo the last decision</p>
    </section>
  {:else if current}
    <header>
      {#if singleId}
        <span class="progress">Single question</span>
      {:else}
        <span class="progress">{index + 1} / {questions.length}</span>
      {/if}
      {#if downloads}<span class="downloads">⬇ downloading media… ({downloads})</span>{/if}
      {#if !singleId}
        <span class="counts">
          ✓ {counts.approved} · ✎ {counts.needs_work} · ✗ {counts.rejected} · open {counts.draft}
        </span>
      {/if}
      <span class="meta">
        {current.id} · {current.subcategory} ·
        <span class:pending={difficultyPending}>difficulty {current.difficulty}/10</span>
        {#if current.difficulty_original != null && current.difficulty_original !== current.difficulty}
          (was {current.difficulty_original})
        {/if}
        {#if current.style}· {current.style.split(":")[0]}{/if}
      </span>
      <a class="stats" href="/stats/categories">Stats →</a>
    </header>

    {#if current.review}
      <div class="previous {current.status}">
        Already reviewed: <b>{current.status.replace("_", " ")}</b> ({current.review.reviewed_on})
        {#if current.review.feedback}: “{current.review.feedback}”{/if}
      </div>
    {/if}

    {#if current.revision}<RevisionPanel question={current} />{/if}

    <article>
      <p class="description">{current.description}</p>
      <h1 class="question">{current.question}</h1>

      <ol class="options">
        {#each options as option, i}
          <li class:correct={i === 0}>{option}</li>
        {/each}
      </ol>

      <MediaPanel
        title={`Media · ${current.media.type} · ${current.media.role}`}
        slot={current.media}
        decorative={current.media.role === "decorative"}
        candidates={current.media_candidates ?? null}
        showCandidates={openSlot === "media"}
        toggleKey="c"
        working={mediaWorking && searchSlot === "media"}
      />
      {#if current.background}
        <MediaPanel
          title="Background image (shown while the sound plays)"
          slot={{ type: "image", ...current.background }}
          decorative={true}
          candidates={current.background_candidates ?? null}
          showCandidates={openSlot === "background"}
          toggleKey="b"
          working={mediaWorking && searchSlot === "background"}
        />
      {/if}

      <div class="columns">
        <section>
          <h2>Hints</h2>
          <ol>
            {#each current.hints as hint}<li>{hint}</li>{/each}
          </ol>
          <h2>Fun fact</h2>
          <p>{current.fun_fact}</p>
        </section>

        <section>
          <h2>Fact check</h2>
          <p>
            {#if current.fact_checked}✓ confirmed by web search
            {:else if current.fact_checked === false}not confirmed
            {:else}not part of the pipeline{/if}
          </p>

          {#if current.quality}
            <h2>Rater scores {showScores ? "" : "(hidden, s to show)"}</h2>
            {#if showScores}
              <p class="scores">
                correct {current.quality.correct} · unambiguous {current.quality.unambiguous} ·
                distractors {current.quality.distractors} · age {current.quality.age_fit} ·
                fun {current.quality.fun} · description {current.quality.description} ·
                estimated difficulty {current.quality.difficulty_estimate}/10
              </p>
              <p class="muted">{current.quality.notes}</p>
            {/if}
          {/if}
        </section>
      </div>
    </article>

    {#if searchOpen}
      <!-- svelte-ignore a11y_click_events_have_key_events, a11y_no_static_element_interactions -->
      <div class="backdrop" onclick={() => (searchOpen = false)}>
        <div class="modal" role="dialog" tabindex="-1" aria-modal="true" aria-labelledby="search-title" onclick={(e) => e.stopPropagation()}>
          <h2 id="search-title">
            New search term · {searchSlot === "background" ? "background image" : `media (${current.media.type})`}
          </h2>
          <p class="muted">{current.question}</p>
          <input
            bind:this={searchBox}
            bind:value={searchText}
            placeholder="Search term for Wikimedia Commons (English works best)"
          />
          <p class="muted">Enter: search · Esc: cancel · 2–4 concrete words work best</p>
        </div>
      </div>
    {/if}

    {#if feedbackOpen}
      <!-- svelte-ignore a11y_click_events_have_key_events, a11y_no_static_element_interactions -->
      <div class="backdrop" onclick={() => (feedbackOpen = false)}>
        <div class="modal feedback" role="dialog" tabindex="-1" aria-modal="true" aria-labelledby="feedback-title" onclick={(e) => e.stopPropagation()}>
          <h2 id="feedback-title">Feedback · {current.id} needs work</h2>
          <p class="muted">{current.question}</p>
          <textarea
            bind:this={feedbackBox}
            bind:value={feedbackText}
            rows="4"
            placeholder="What should change? (e.g. too difficult, bad image, a wrong answer is also right…)"
          ></textarea>
          <p class="muted">Enter: save and next · Shift+Enter: new line · Esc: cancel</p>
        </div>
      </div>
    {/if}

    <footer>
      <button class="approve" onclick={() => decide("approved")}><kbd>a</kbd> approve</button>
      <button class="feedback-btn" onclick={openFeedback}><kbd>f</kbd> feedback</button>
      <button class="reject" onclick={() => decide("rejected")}><kbd>r</kbd> reject</button>
      <button onclick={() => { difficultyPending = true; flash("difficulty: press 0–9 (0 = 1, 9 = 10)"); }}><kbd>d</kbd> difficulty</button>
      <button onclick={openSearch}><kbd>m</kbd> media search</button>
      <button onclick={() => toggle("media")}><kbd>c</kbd> {openSlot === "media" ? "hide" : "show"} alternatives</button>
      {#if current.background}
        <button onclick={() => toggle("background")}><kbd>b</kbd> {openSlot === "background" ? "hide" : "show"} backgrounds</button>
      {/if}
      <span class="divider"></span>
      <button onclick={() => move(-1)}><kbd>←</kbd></button>
      <button onclick={() => move(1)}><kbd>→</kbd></button>
      <button onclick={undo}><kbd>u</kbd> undo</button>
      <button onclick={() => (showScores = !showScores)}><kbd>s</kbd> scores</button>
    </footer>
  {/if}

  {#if toast}<div class="toast">{toast}</div>{/if}
  {#if errors.length}
    <div class="errors" role="alert">
      {#each errors as err (err.id)}
        <div class="error-item">
          <div>
            <b>Error</b> {err.what} <span class="muted">({err.time})</span><br />
            {err.message}
          </div>
          <button aria-label="dismiss" onclick={() => (errors = errors.filter((x) => x.id !== err.id))}>✕</button>
        </div>
      {/each}
      {#if errors.length > 1}
        <button class="clear" onclick={() => (errors = [])}>dismiss all</button>
      {/if}
    </div>
  {/if}
  {#if debugKeys}<div class="debug">{lastKey || "press a key"}</div>{/if}
</main>

<style>
  main {
    max-width: 1200px;
    margin: 0 auto;
    padding: 1.5rem 2rem 9rem;
  }
  header {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 0.5rem 1.5rem;
    font-size: 0.95rem;
    color: var(--muted);
  }
  .pending {
    color: var(--accent);
    font-weight: 700;
  }
  .downloads {
    color: var(--accent);
  }
  .progress {
    color: var(--text);
    font-weight: 700;
  }
  .meta {
    margin-left: auto;
  }
  .stats {
    color: var(--muted);
  }
  .previous {
    margin-top: 1rem;
    padding: 0.5rem 0.8rem;
    border-radius: 8px;
    background: var(--panel);
    border-left: 4px solid var(--muted);
  }
  .previous.approved { border-color: var(--good); }
  .previous.rejected { border-color: var(--bad); }
  .previous.needs_work { border-color: var(--warn); }
  .description {
    margin: 2rem 0 0.5rem;
    font-style: italic;
    font-size: 1.3rem;
    color: var(--accent);
  }
  .question {
    margin: 0 0 1.5rem;
    font-size: 2.1rem;
    line-height: 1.25;
  }
  .options {
    display: grid;
    grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
    gap: 0.8rem;
    padding: 0;
    list-style: none;
  }
  .options li {
    padding: 0.9rem 1.1rem;
    border-radius: 10px;
    background: var(--panel);
    font-size: 1.3rem;
  }
  .options li.correct {
    background: var(--good-bg);
    outline: 2px solid var(--good);
  }
  .columns {
    display: grid;
    grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
    gap: 2rem;
    margin-top: 1.5rem;
  }
  h2 {
    margin: 1.2rem 0 0.4rem;
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--muted);
  }
  .scores {
    font-variant-numeric: tabular-nums;
  }
  .muted {
    color: var(--muted);
  }
  .modal.feedback {
    border-color: var(--warn);
  }
  .feedback textarea {
    width: 100%;
    padding: 0.8rem;
    font: inherit;
    font-size: 1.1rem;
    color: var(--text);
    background: var(--panel);
    border: 2px solid var(--warn);
    border-radius: 8px;
  }
  .backdrop {
    position: fixed;
    inset: 0;
    z-index: 10;
    display: grid;
    place-items: center;
    padding: 1rem;
    background: rgb(0 0 0 / 0.6);
  }
  .modal {
    width: min(640px, 100%);
    padding: 1.5rem;
    border-radius: 12px;
    background: var(--bg);
    border: 1px solid var(--accent);
    box-shadow: 0 20px 60px rgb(0 0 0 / 0.5);
  }
  .modal h2 {
    margin-top: 0;
  }
  .modal input {
    width: 100%;
    padding: 0.8rem;
    font: inherit;
    font-size: 1.2rem;
    color: var(--text);
    background: var(--panel);
    border: 2px solid var(--accent);
    border-radius: 8px;
  }
  footer {
    position: fixed;
    left: 0;
    right: 0;
    bottom: 0;
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 0.6rem;
    padding: 0.8rem 2rem;
    background: var(--bg);
    border-top: 1px solid var(--panel);
  }
  .divider {
    width: 1px;
    margin: 0 0.6rem;
    background: var(--panel);
  }
  button {
    padding: 0.5rem 0.9rem;
    font: inherit;
    color: var(--text);
    background: var(--panel);
    border: 1px solid transparent;
    border-radius: 8px;
    cursor: pointer;
  }
  button.approve { border-color: var(--good); }
  button.reject { border-color: var(--bad); }
  button.feedback-btn { border-color: var(--warn); }
  kbd {
    padding: 0 0.35rem;
    margin-right: 0.3rem;
    font-family: inherit;
    font-weight: 700;
    border: 1px solid var(--muted);
    border-radius: 4px;
  }
  .debug {
    position: fixed;
    top: 0.5rem;
    right: 0.5rem;
    padding: 0.3rem 0.6rem;
    font-family: monospace;
    font-size: 0.85rem;
    background: var(--panel);
    border: 1px solid var(--accent);
    border-radius: 6px;
  }
  .errors {
    position: fixed;
    top: 1rem;
    right: 1rem;
    z-index: 20;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    width: min(420px, calc(100% - 2rem));
  }
  .error-item {
    display: flex;
    gap: 0.6rem;
    align-items: flex-start;
    justify-content: space-between;
    padding: 0.7rem 0.9rem;
    border-radius: 8px;
    background: #3a1d22;
    border: 1px solid var(--bad);
    box-shadow: 0 8px 30px rgb(0 0 0 / 0.4);
  }
  .error-item button,
  .errors .clear {
    padding: 0.1rem 0.5rem;
  }
  .errors .clear {
    align-self: flex-end;
  }
  .toast {
    position: fixed;
    top: 1.5rem;
    left: 50%;
    transform: translateX(-50%);
    padding: 0.6rem 1.2rem;
    border-radius: 8px;
    background: var(--accent);
    color: var(--bg);
    font-weight: 700;
  }
  .summary ul {
    font-size: 1.4rem;
  }
  .center {
    margin-top: 30vh;
    text-align: center;
  }
  .error {
    color: var(--bad);
  }
</style>
