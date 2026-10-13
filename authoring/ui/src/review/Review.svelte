<script lang="ts">
  // Review tool (plans/08-review-tool.md): one question per screen, single-key decisions.
  import { onMount } from "svelte";
  import { messageOf } from "$app/lib/http";
  import {
    fetchBundles,
    fetchNames,
    fetchQuestions,
    fetchSpotChecks,
    pickMedia,
    recordSpotCheck,
    removeSpotCheck,
    saveReview,
    searchMedia,
    setBundle,
    setDifficulty,
    setTranslatable,
  } from "../lib/api";
  import type { Bundle, Decision, Names, Question, Review, Slot, SpotCheckItem } from "../lib/types";
  import Nav from "../lib/Nav.svelte";
  import FeedbackModal from "./FeedbackModal.svelte";
  import MediaPanel from "./MediaPanel.svelte";
  import ReviewBanners, { accepts } from "./ReviewBanners.svelte";
  import ReviewHeader from "./ReviewHeader.svelte";
  import RevisionPanel from "./RevisionPanel.svelte";
  import SearchModal from "./SearchModal.svelte";
  import SourcePanel from "./SourcePanel.svelte";
  import { reviewUrl } from "./url";

  const { locale, checkGroup, sampleMode, filter, licenceMode, filterText, singleId, startId, debugKeys } = reviewUrl();
  let lastKey = $state("");

  let questions = $state<Question[]>([]);
  let bundles = $state<Bundle[]>([]);
  let names = $state<Names | null>(null);
  let index = $state(0);
  let loading = $state(true);
  let error = $state<string | null>(null);
  let finished = $state(false);
  let showScores = $state(false);
  let feedbackOpen = $state(false);
  let feedbackText = $state("");
  let searchOpen = $state(false);
  let searchText = $state("");
  let mediaWorking = $state(false);
  /** Media downloads that run in the background after an approval. */
  let downloads = $state(0);
  /** Which slot's alternatives are shown; digits and "m" act on it. */
  let openSlot = $state<Slot | null>(null);
  /** After "d": the digits typed so far; Enter sets the difficulty, Esc cancels. null = not typing. */
  let difficultyInput = $state<string | null>(null);
  /** Top of the shared difficulty scale (app/data/age-groups.json, D-38); the server checks it too. */
  const MAX_DIFFICULTY = 15;
  let toast = $state<string | null>(null);
  let busy = false;
  let toastTimer: ReturnType<typeof setTimeout> | undefined;
  /** Failed API calls stay visible until dismissed (also from background downloads). */
  let errors = $state<{ id: number; time: string; what: string; message: string }[]>([]);
  let errorSeq = 0;

  function reportError(what: string, e: unknown) {
    const message = messageOf(e);
    const time = new Date().toLocaleTimeString();
    errors = [...errors, { id: ++errorSeq, time, what, message }];
  }
  /** translatable: the step set "doesn't travel"; undo makes the source travel again first. */
  const undoStack: { id: string; previous: Review | null; spot: boolean; translatable?: boolean }[] = [];
  /** Spot checks of this batch (sample mode); a question is blind until it has one. */
  let spotItems = $state<Record<string, SpotCheckItem>>({});
  /** Problem kinds for the feedback box (qgen.py PROBLEMS). */
  let problemKinds = $state<string[]>([]);
  let feedbackProblems = $state<string[]>([]);
  /** Questions whose media was picked or searched in this session (the spot check's media_changed). */
  const mediaTouched = new Set<string>();

  /** Decided in this session: with a status filter, a question is open until it gets one (RV-22). */
  let decidedNow = $state<Set<string>>(new Set());
  /** Open until a human has reviewed it: drafts and LLM-reviewed questions (D-33). In the media queue
   *  (media=missing) a question stays open until it has picked media, whoever reviewed it; in the licence
   *  queue until no slot is still "replace" (plan 53). With a
   *  status filter the list is one pass over questions that may already have a human review. */
  const isOpen = (q: Question) =>
    sampleMode ? !spotItems[q.id]
      : filter.media === "missing" ? !q.media.file_url
      : licenceMode ? Object.values(q.licence).some((v) => v.verdict === "replace")
      : filter.status ? !decidedNow.has(q.id) : q.review?.reviewer !== "human";

  const current = $derived(questions[index]);
  /** Sample mode before the human's decision: no LLM decision, feedback, reasons or audit. */
  const blind = $derived(sampleMode && !!current && !spotItems[current.id]);
  const spot = $derived(sampleMode && current ? spotItems[current.id] : undefined);
  const agreed = $derived(Object.values(spotItems).filter((i) => accepts(i.llm) === accepts(i.human)).length);
  const counts = $derived({
    approved: questions.filter((q) => q.status === "approved").length,
    rejected: questions.filter((q) => q.status === "rejected").length,
    needs_work: questions.filter((q) => q.status === "needs_work").length,
    open: questions.filter(isOpen).length,
    llm: questions.filter((q) => q.review?.reviewer === "llm").length,
  });

  const LABELS: Record<Decision, string> = {
    approved: "✓ approved",
    rejected: "✗ rejected",
    needs_work: "✎ feedback saved",
  };

  onMount(async () => {
    try {
      const [qs, bs, spots, ns] = await Promise.all([
        fetchQuestions(filter), fetchBundles(), fetchSpotChecks(), locale ? fetchNames(locale) : null,
      ]);
      [questions, bundles, problemKinds, names] = [qs, bs, spots.problems, ns];
      if (sampleMode) spotItems = spots.checks[checkGroup!]?.items ?? {};
      if (singleId) questions = questions.filter((q) => q.id === singleId);
      const fromUrl = questions.findIndex((q) => q.id === startId);
      const firstOpen = questions.findIndex(isOpen);
      finished = !singleId && questions.length > 0 && fromUrl === -1 && firstOpen === -1;
      index = fromUrl !== -1 ? fromUrl : Math.max(firstOpen, 0);
    } catch (e) {
      error = messageOf(e);
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
      if (isOpen(questions[i])) return i;
    }
    return -1;
  }

  async function store(i: number, review: Parameters<typeof saveReview>[1]) {
    const updated = await saveReview(questions[i].id, review, locale);
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

  async function decide(decision: Decision, feedback: string | null = null, problems: string[] = []) {
    if (busy || mediaWorking || !current) return;
    if (decision === "approved" && current.stale) return flash("Stale: the source changed, the next --translate run redoes it");
    busy = true;
    const i = index;
    try {
      const suggestions = decision === "approved" && !locale ? slotsNeedingSuggestion(questions[i]) : [];
      const id = questions[i].id;
      const previous = questions[i].review;
      await store(i, { decision, feedback, problems });
      undoStack.push({ id, previous, spot: sampleMode });
      decidedNow = new Set(decidedNow).add(id);
      if (sampleMode) {
        // Stay on the question: the reveal shows the LLM's verdict next to the human's; → goes on.
        spotItems = { ...spotItems, [id]: await recordSpotCheck(checkGroup!, id, mediaTouched.has(id)) };
      }
      flash(LABELS[decision]);
      if (suggestions.length) pickSuggestionsInBackground(id, suggestions);
      if (sampleMode) return;
      const next = singleId ? i : nextOpen(i);
      openSlot = null;
      if (next === -1) finished = true;
      else index = next;
    } catch (e) {
      reportError(`saving “${decision.replace("_", " ")}” for ${questions[i]?.id}`, e);
    } finally {
      busy = false;
    }
  }

  async function undo() {
    if (busy || mediaWorking) return;
    const last = undoStack.pop();
    if (!last) return;
    busy = true;
    try {
      const i = questions.findIndex((q) => q.id === last.id);
      if (last.translatable) questions[i] = await setTranslatable(last.id, true, locale);
      await store(i, last.previous);
      if (last.spot) {
        await removeSpotCheck(checkGroup!, last.id);
        const { [last.id]: _, ...rest } = spotItems;
        spotItems = rest;
      }
      decidedNow = new Set([...decidedNow].filter((id) => id !== last.id));
      index = i;
      finished = false;
      flash("↶ undone");
    } catch (e) {
      reportError(`undo for ${last.id}`, e);
    } finally {
      busy = false;
    }
  }

  function openFeedback() {
    feedbackText = blind ? "" : (current?.review?.feedback ?? "");
    feedbackProblems = blind ? [] : (current?.review?.problems ?? []);
    feedbackOpen = true;
  }

  function submitFeedback() {
    const text = feedbackText.trim();
    if (!text) return flash("Feedback is empty");
    if (busy || mediaWorking) return flash("Still saving, try again");
    feedbackOpen = false;
    decide("needs_work", text, feedbackProblems);
  }

  /** "Doesn't travel" (plan 63): the source's translatable flag; false rejects its translations. */
  async function setTravels(value: boolean) {
    if (busy || !current) return;
    if (!value && !confirm(`${current.id} doesn't travel: reject its translations in every locale?`)) return;
    busy = true;
    const i = index;
    try {
      const previous = questions[i].review;
      questions[i] = await setTranslatable(questions[i].id, value, locale);
      if (!value) undoStack.push({ id: questions[i].id, previous, spot: false, translatable: true });
      flash(value ? "travels again" : "✗ doesn't travel");
    } catch (e) {
      reportError(`setting translatable for ${questions[i]?.id}`, e);
    } finally {
      busy = false;
    }
  }

  /** Locale view: media and bundle live on the source (plan 67). */
  function onSource(action: () => void) {
    return locale ? () => flash("Media and bundle: change them in the Spanish view") : action;
  }

  async function mediaAction(label: string, what: string, run: () => Promise<Question>) {
    if (busy || mediaWorking || !current) return;
    const i = index;
    mediaTouched.add(current.id);
    mediaWorking = true;
    try {
      questions[i] = await run();
      flash(licenceMode && !questions.some(isOpen) ? `${label} · licence list empty` : label);
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

  function openSearch() {
    searchText = (searchSlot === "background" ? current?.background?.query : current?.media.query) ?? "";
    searchOpen = true;
  }

  function submitSearch() {
    const id = current?.id;
    const query = searchText.trim();
    if (!id || !query) return;
    const slot = searchSlot;
    searchOpen = false;
    openSlot = slot;
    mediaAction("🔍 new candidates", `searching for “${query}”`, () => searchMedia(id, query, slot, licenceMode));
  }

  function startDifficulty() {
    difficultyInput = "";
    flash(`difficulty: type 1–${MAX_DIFFICULTY}, then Enter (Esc: cancel)`);
  }

  /** Keys while typing a difficulty: digits, Backspace, Enter, Esc. */
  function difficultyKey(event: KeyboardEvent, digit: string | null) {
    event.preventDefault();
    const typed = difficultyInput ?? "";
    if (digit !== null) {
      difficultyInput = (typed + digit).slice(-2);
    } else if (event.key === "Backspace") {
      difficultyInput = typed.slice(0, -1);
    } else if (event.key === "Enter") {
      const value = Number(typed);
      difficultyInput = null;
      if (!typed) return flash("difficulty unchanged");
      if (!Number.isInteger(value) || value < 1 || value > MAX_DIFFICULTY) {
        return flash(`difficulty must be 1–${MAX_DIFFICULTY}; unchanged`);
      }
      changeDifficulty(value);
    } else if (event.key === "Escape") {
      difficultyInput = null;
      flash("difficulty unchanged");
    }
  }

  async function changeDifficulty(difficulty: number) {
    if (!current) return;
    const i = index;
    try {
      const updated = await setDifficulty(questions[i].id, difficulty, locale);
      questions[i] = { ...questions[i], difficulty: updated.difficulty, difficulty_original: updated.difficulty_original };
      flash(`difficulty ${difficulty}`);
    } catch (e) {
      reportError(`setting difficulty for ${questions[i]?.id}`, e);
    }
  }

  /** "n": move the question to the next bundle in app/data/bundles.json (D-39). */
  async function nextBundle() {
    if (!current || !bundles.length) return;
    const i = index;
    const at = bundles.findIndex((b) => b.id === questions[i].bundle);
    const next = bundles[(at + 1) % bundles.length];
    try {
      const updated = await setBundle(questions[i].id, next.id);
      questions[i] = { ...questions[i], bundle: updated.bundle };
      flash(`bundle: ${next.name}`);
    } catch (e) {
      reportError(`moving ${questions[i]?.id} to bundle ${next.id}`, e);
    }
  }

  function move(delta: number) {
    if (!questions.length) return;
    finished = false;
    openSlot = null;
    difficultyInput = null;
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
    if (difficultyInput !== null) return difficultyKey(event, anyDigit);
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
      m: onSource(openSearch),
      d: startDifficulty,
      n: onSource(nextBundle),
      c: onSource(() => toggle("media")),
      b: onSource(() => toggle("background")),
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
      {singleId ? `No question “${singleId}”` : `No questions${filterText ? `: ${filterText}` : ""}`}.
      {#if licenceMode}The licence list is empty; <code>trivia-media licenses</code> should say so too.{/if}
    </p>
  {:else if finished}
    <section class="summary">
      <Nav current="review" />
      <h1>All done{filterText ? `: ${filterText}` : ""}</h1>
      {#if licenceMode}
        <p>The licence list is empty: every file in it has a clean pick. Check with <code>trivia-media licenses</code>,
          then drop the old files with <code>trivia-media sync --status approved --prune</code>.</p>
      {/if}
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
    <ReviewHeader
      {current}
      {index}
      total={questions.length}
      {singleId}
      {locale}
      {downloads}
      spotCount={sampleMode ? Object.keys(spotItems).length : null}
      {agreed}
      {counts}
      {names}
      {bundles}
      {difficultyInput}
    />

    <ReviewBanners {current} {spot} {blind} onTravels={() => setTravels(true)} />

    {#if current.revision && !blind && !locale}<RevisionPanel question={current} revision={current.revision} />{/if}

    <article>
      {#if locale && current.source}
        <SourcePanel question={current} source={current.source} {blind} />
        <p class="muted">Media and bundle live on the source: <a href={`/review?id=${encodeURIComponent(current.id)}`}>change them in the Spanish view</a>.</p>
      {:else}
        <p class="description">{current.description}</p>
        <h1 class="question">{current.question}</h1>

        <ol class="options">
          {#each options as option, i}
            <li class:correct={i === 0}>{option}</li>
          {/each}
        </ol>
      {/if}

      <MediaPanel
        title={`Media · ${current.media.type} · ${current.media.role}`}
        slot={current.media}
        decorative={current.media.role === "decorative"}
        candidates={current.media_candidates ?? null}
        licence={current.licence.media}
        showCandidates={openSlot === "media"}
        toggleKey="c"
        readonly={!!locale}
        working={mediaWorking && searchSlot === "media"}
      />
      {#if current.background}
        <MediaPanel
          title="Background image (shown while the sound plays)"
          slot={{ type: "image", ...current.background }}
          decorative={true}
          candidates={current.background_candidates ?? null}
          licence={current.licence.background}
          showCandidates={openSlot === "background"}
          toggleKey="b"
          readonly={!!locale}
          working={mediaWorking && searchSlot === "background"}
        />
      {/if}

      <div class="columns">
        {#if !locale}
          <section>
            <h2>Hints</h2>
            <ol>
              {#each current.hints as hint}<li>{hint}</li>{/each}
            </ol>
            <h2>Fun fact</h2>
            <p>{current.fun_fact}</p>
          </section>
        {/if}

        {#if blind}
          <section>
            <h2>Spot check (blind)</h2>
            <p class="muted">The LLM's verdict, reasons and the audit show after your decision.</p>
          </section>
        {:else}
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
                  {#if current.quality.no_giveaway !== undefined}no giveaway {current.quality.no_giveaway} ·{/if}
                  {#if current.quality.no_overlap !== undefined}no overlap {current.quality.no_overlap} ·{/if}
                  distractors {current.quality.distractors} · age {current.quality.age_fit} ·
                  fun {current.quality.fun} · description {current.quality.description} ·
                  estimated difficulty {current.quality.difficulty_estimate}
                </p>
                <p class="muted">{current.quality.notes}</p>
              {/if}
            {/if}
          </section>
        {/if}
      </div>
    </article>

    {#if searchOpen}
      <SearchModal
        title={`New search term · ${searchSlot === "background" ? "background image" : `media (${current.media.type})`}`}
        question={current.question}
        {licenceMode}
        bind:value={searchText}
        onclose={() => (searchOpen = false)}
      />
    {/if}

    {#if feedbackOpen}
      <FeedbackModal
        id={current.id}
        question={current.question}
        kinds={problemKinds}
        bind:text={feedbackText}
        bind:problems={feedbackProblems}
        onclose={() => (feedbackOpen = false)}
      />
    {/if}

    <footer>
      <button class="approve" disabled={current.stale} onclick={() => decide("approved")}><kbd>a</kbd> approve</button>
      <button class="feedback-btn" onclick={openFeedback}><kbd>f</kbd> feedback</button>
      <button class="reject" onclick={() => decide("rejected")}><kbd>r</kbd> reject</button>
      <button onclick={startDifficulty}><kbd>d</kbd> difficulty</button>
      {#if locale}
        {#if current.translatable !== false}<button class="reject" onclick={() => setTravels(false)}>doesn't travel</button>{/if}
      {:else}
        <button onclick={nextBundle}><kbd>n</kbd> bundle</button>
        <button onclick={openSearch}><kbd>m</kbd> media search</button>
        <button onclick={() => toggle("media")}><kbd>c</kbd> {openSlot === "media" ? "hide" : "show"} alternatives</button>
        {#if current.background}
          <button onclick={() => toggle("background")}><kbd>b</kbd> {openSlot === "background" ? "hide" : "show"} backgrounds</button>
        {/if}
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
  button:disabled {
    opacity: 0.4;
    cursor: not-allowed;
  }
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
    background: var(--bad-bg);
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
