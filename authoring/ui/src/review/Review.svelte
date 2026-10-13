<script lang="ts">
  // Review tool (plans/08-review-tool.md): one question per screen, single-key decisions.
  import { onMount, tick } from "svelte";
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
    type QuestionFilter,
  } from "../lib/api";
  import type { Bundle, Decision, Names, Question, Review, Slot, SpotCheckItem } from "../lib/types";
  import Nav from "../lib/Nav.svelte";
  import MediaPanel from "./MediaPanel.svelte";
  import RevisionPanel from "./RevisionPanel.svelte";
  import SourcePanel from "./SourcePanel.svelte";

  // URL: ?batch=pilot&bundle=colombia&id=q-0123, plus the filters status, reviewer, subcategory and
  // media=missing (RV-13), licence=replace (plan 53); status=!approved is every question that isn't
  // approved, across batches (RV-22, D-47). The id follows the current question, so a reload (or a bookmark) comes
  // back to it. Decisions themselves live in authoring/data/questions.json.
  // With batch: sample=1 is the blind spot check (plan 16), audit=flagged the audit's major findings.
  // run=backaudit-<k>: a back-audit run's questions, with the same two (plan 57).
  // locale=en|de: the translations next to their Spanish source; media and bundle stay on the source (plan 67).
  const params = new URLSearchParams(location.search);
  const locale = params.get("locale") === "es" ? null : params.get("locale");
  const LOCALES = ["es", "en", "de"];
  /** This page in another locale, the other params kept. */
  function localeHref(l: string) {
    const url = new URL(location.href);
    if (l === "es") url.searchParams.delete("locale");
    else url.searchParams.set("locale", l);
    return url.pathname + url.search;
  }
  const batch = params.get("batch");
  const run = params.get("run");
  /** Where spot checks are recorded: the batch or the back-audit run. */
  const checkGroup = batch ?? run;
  const sampleMode = !!checkGroup && params.get("sample") === "1";
  const bundleFilter = params.get("bundle");
  const filter = {
    batch,
    run,
    bundle: bundleFilter,
    status: params.get("status"),
    reviewer: params.get("reviewer"),
    subcategory: params.get("subcategory"),
    media: params.get("media"),
    sample: sampleMode ? "1" : null,
    audit: params.get("audit"),
    licence: params.get("licence"),
    locale,
    stale: params.get("stale"),
  } as QuestionFilter;
  /** The licence queue (plan 53): searches ask every provider. */
  const licenceMode = filter.licence === "replace";
  /** The active filters in words, for the empty and summary screens. */
  const filterText = [
    batch && `batch “${batch}”`,
    run && `run “${run}”`,
    bundleFilter && `bundle “${bundleFilter}”`,
    filter.subcategory && `subcategory “${filter.subcategory}”`,
    filter.status && `status ${filter.status}`,
    filter.reviewer && `reviewed by ${filter.reviewer}`,
    filter.media === "missing" && "without media",
    sampleMode && "spot-check sample",
    filter.audit === "flagged" && "flagged by the audit",
    licenceMode && "licence to replace",
    locale && `locale ${locale}`,
    filter.stale === "1" && "stale",
  ]
    .filter(Boolean)
    .join(", ");
  // /review/q-0123: just that one question (linked from the game's admin overlay).
  const singleId = decodeURIComponent(location.pathname.match(/^\/review\/([^/]+)/)?.[1] ?? "") || null;
  const startId = singleId ?? params.get("id");
  // ?debug=keys shows what the browser reports for each key press (for layout problems).
  const debugKeys = params.get("debug") === "keys";
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
  let feedbackBox = $state<HTMLTextAreaElement>();
  let searchOpen = $state(false);
  let searchText = $state("");
  let searchBox = $state<HTMLInputElement>();
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
    const message = e instanceof Error ? e.message : String(e);
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
  const accepts = (d: Decision) => d === "approved";
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
    let pushed = false;
    try {
      const suggestions = decision === "approved" && !locale ? slotsNeedingSuggestion(questions[i]) : [];
      const id = questions[i].id;
      undoStack.push({ id, previous: questions[i].review, spot: sampleMode });
      pushed = true;
      await store(i, { decision, feedback, problems });
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

  async function openFeedback() {
    feedbackText = blind ? "" : (current?.review?.feedback ?? "");
    feedbackProblems = blind ? [] : (current?.review?.problems ?? []);
    feedbackOpen = true;
    await tick();
    feedbackBox?.focus();
  }

  function submitFeedback() {
    const text = feedbackText.trim();
    if (!text) return flash("Feedback is empty");
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
    if (mediaWorking || !current) return;
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
    <header>
      {#if singleId}
        <span class="progress">Single question</span>
      {:else}
        <span class="progress">{index + 1} / {questions.length}</span>
      {/if}
      {#if locale}<span class="locale">{locale}</span>{/if}
      {#if downloads}<span class="downloads">⬇ downloading media… ({downloads})</span>{/if}
      {#if sampleMode}
        <span class="counts">spot check: {Object.keys(spotItems).length} decided · agree {agreed}</span>
      {:else if !singleId}
        <span class="counts">
          ✓ {counts.approved} · ✎ {counts.needs_work} · ✗ {counts.rejected} · open {counts.open}{#if counts.llm}
            (LLM-reviewed {counts.llm}){/if}
        </span>
      {/if}
      <span class="meta">
        {current.id} ·
        {#if names?.subcategories[current.subcategory]}{names.subcategories[current.subcategory]}
          <span class="key">({current.subcategory})</span>{:else}{current.subcategory}{/if} ·
        <span class:pending={difficultyInput !== null}
          >difficulty {difficultyInput !== null ? `${difficultyInput}▏ (Enter)` : current.difficulty}</span
        >
        {#if current.difficulty_original != null && current.difficulty_original !== current.difficulty}
          (was {current.difficulty_original})
        {/if}
        {#if current.style}· {current.style.split(":")[0]}{/if}
        · <span class="bundle" class:other={current.bundle !== "base"}
          >{names?.bundles[current.bundle]?.name ?? bundles.find((b) => b.id === current.bundle)?.name ?? current.bundle}</span
        >{#if names}&nbsp;<span class="key">({current.bundle})</span>{/if}
      </span>
      <span><a class="stats" href="/">Start</a> · <a class="stats" href="/stats/categories">Stats</a> ·
        {#each LOCALES as l, k}{#if k}&nbsp;·&nbsp;{/if}{#if l === (locale ?? "es")}<b>{l}</b>{:else}<a class="stats" href={localeHref(l)}>{l}</a
          >{/if}{/each}</span>
    </header>

    {#if spot}
      <div class="spot" class:disagree={accepts(spot.llm) !== accepts(spot.human)}>
        Spot check: you <b>{spot.human.replace("_", " ")}</b> · LLM review <b>{spot.llm.replace("_", " ")}</b> ·
        <b>{accepts(spot.llm) === accepts(spot.human) ? "agree" : "disagree"}</b>
        · audit: {spot.audit === "problem" ? "major finding" : spot.audit === "ok" ? "no major finding" : "not audited"}
        {#if spot.difficulty[0] !== spot.difficulty[1]}· difficulty {spot.difficulty[0]} → {spot.difficulty[1]}{/if}
        <span class="muted">· → next · u undo</span>
      </div>
    {/if}

    {#if current.stale}
      <div class="previous stale">
        Stale: the Spanish source changed since this translation. No approve; the next <code>--translate</code> run redoes it.
      </div>
    {/if}
    {#if current.translatable === false}
      <div class="previous rejected">
        The source doesn't travel (<code>translatable: false</code>); its translations are rejected.
        <button onclick={() => setTravels(true)}>travels again</button>
      </div>
    {/if}

    {#if current.review && !blind}
      <div class="previous {current.status}">
        {current.review.reviewer === "llm" ? `Reviewed by ${current.review.model}` : "Already reviewed"}:
        <b>{current.status.replace("_", " ")}</b> ({current.review.reviewed_on})
        {#if current.review.feedback}: “{current.review.feedback}”{/if}
        {#if current.review.previous}
          <span class="muted">· before: {current.review.previous.model}
            {current.review.previous.decision.replace("_", " ")}{#if current.review.previous.feedback}:
              “{current.review.previous.feedback}”{/if}</span>
        {/if}
      </div>
    {/if}

    {#if current.audit && !blind}
      <div class="previous audit" class:major={current.audit.verdict === "problem" && current.audit.severity === "major"}>
        Audit ({current.audit.model}): <b>{current.audit.verdict}</b>{#if current.audit.verdict === "problem"}
          , {current.audit.severity}: {current.audit.problems.join(", ") || "other"}{/if}
        · difficulty {current.audit.difficulty_estimate} · “{current.audit.notes}”
      </div>
    {/if}

    {#if current.revision && !blind && !locale}<RevisionPanel question={current} />{/if}

    <article>
      {#if locale}
        <SourcePanel question={current} {blind} />
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
            placeholder={licenceMode
              ? "Search term (English works best; every source, for a licence replacement)"
              : "Search term (English works best; Commons first, then the other sources)"}
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
          {#if problemKinds.length}
            <div class="kinds">
              {#each problemKinds as kind}
                <button
                  class:on={feedbackProblems.includes(kind)}
                  onclick={() =>
                    (feedbackProblems = feedbackProblems.includes(kind)
                      ? feedbackProblems.filter((k) => k !== kind)
                      : [...feedbackProblems, kind])}>{kind}</button
                >
              {/each}
            </div>
          {/if}
          <p class="muted">Enter: save and next · Shift+Enter: new line · Esc: cancel</p>
        </div>
      </div>
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
  .previous.audit { border-color: var(--accent); }
  .previous.stale { border-color: var(--warn); }
  .locale {
    color: var(--accent);
    font-weight: 700;
    text-transform: uppercase;
  }
  .key {
    color: var(--muted);
    font-size: 0.85em;
  }
  button:disabled {
    opacity: 0.4;
    cursor: not-allowed;
  }
  .previous.audit.major { border-color: var(--bad); }
  .spot {
    margin-top: 1rem;
    padding: 0.5rem 0.8rem;
    border-radius: 8px;
    background: var(--good-bg);
    border-left: 4px solid var(--good);
  }
  .spot.disagree {
    background: #3a1d22;
    border-color: var(--bad);
  }
  .kinds {
    display: flex;
    flex-wrap: wrap;
    gap: 0.4rem;
    margin-top: 0.6rem;
  }
  .kinds button {
    padding: 0.2rem 0.6rem;
    font-size: 0.9rem;
  }
  .kinds button.on {
    border-color: var(--warn);
    color: var(--warn);
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
  .bundle.other {
    font-weight: 600;
    color: var(--accent);
  }
</style>
