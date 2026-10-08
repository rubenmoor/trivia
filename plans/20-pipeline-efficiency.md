# 20 — Fewer Claude Calls, More Varied Questions in `qgen batch`

**Status:** active

`qgen batch` (D-36, [19](19-repo-layout.md)) makes about 225 `claude -p` calls per batch of 30 subcategories. This plan has two parts:

1. **Fewer calls and tokens** (PE-1..PE-6): cut calls and input tokens where that can't hurt question quality.
2. **Where questions come from** (PE-7..PE-13): stored concept lists per subcategory and question styles split into several axes, so variety comes from code and from a growing pool, not from asking Claude to be original.

**Question quality is the main goal; fewer calls is secondary.** A change that likely costs quality is not made, however much it saves.

## Baseline (batch-5, 2026-10-07)

From `work/batch-5/costs.log` (97 opus + 36 sonnet before merge) and the code in `authoring/tools/qgen.py`:

| Step | Calls | Grouped by |
|---|---|---|
| fit | 4 | 8 subcategories per call |
| draft | 30 | subcategory |
| rate | 30 | subcategory (about 3 questions each) |
| factcheck (sonnet, web) | 30 | subcategory |
| revise | ~27 | subcategory, only those with issues (54 of 96 questions) |
| rate (revised) | 6 | 10 questions per call |
| factcheck (revised) | 6 | 10 questions per call |
| review round 1 | ~90 | question |
| review round 2 | a few | question searched again |

Biggest input: every draft call carries the "Already in the pool" list, one line per pool question (513 questions, about 37 KB, roughly 10k tokens), and it grows with every batch.

## Changes

### Rate in groups of about 10 questions (PE-1)
`cmd_rate` sends the questions of several draft files in one call, up to about 10 questions, and never splits a subcategory. Each question is scored on its own against a fixed rubric, and revised drafts are already rated 10 at a time. Results are still saved per draft file (`ratings/<name>.json`), so a rerun skips what's done, and the "no rating for …" check stays. About 30 calls → about 10.

### Revise in groups of about 10 questions with issues (PE-2)
`cmd_revise` groups questions with issues the same way: about 10 per call, never splitting a subcategory. Every question carries its own list of issues, and the prompt says to change only what's needed. Results are still saved per draft file (`revisions/<name>.json`, also when empty). About 27 calls → about 6.

### Keep the fact-check when a revision changed no facts (PE-3)
`apply_to_drafts` deletes every revised question's fact-check, so `factcheck` checks it again. If `question`, `answer`, `wrong_answers`, `hints` and `fun_fact` are unchanged and the old verdict was `confirmed`, keep that verdict for the revised draft instead. Today the regex for digits in `cmd_factcheck` and `cmd_merge` would select the question again anyway, so the kept verdict has to count as done there. The rating is always redone: a revision changes what the rater judges. Small saving (1–3 calls per batch), with no quality risk.

### "Already in the pool" per subcategory (PE-4)
`existing_answers` keeps only pool questions of the subcategory being drafted. The list is built inside `work(sub)` of `cmd_draft`; the section says "none yet" when it's empty. The format stays the same (answer plus the first 60 characters of the question, all statuses). About 37 KB → a few hundred bytes per draft call, about 300k fewer input tokens per batch, and the list stops growing with the pool. Same number of calls.

Duplicates from other subcategories are still caught: by `duplicates()` in `merge` (code, same answer and similar wording or the same essential media, whole pool) and by the review's `related` list (same or similar answer, whole pool; review rule 4). Neither catches the same fact under a different answer form (synonyms, nicknames) in another subcategory. The gamemaster accepts that: a duplicate in a large pool does little harm (2026-10-07).

### Compact JSON in prompts (PE-5)
Payloads in user messages use `json.dumps(..., ensure_ascii=False)` without `indent=2`. That's about 10–15% fewer payload tokens, and the model reads it just as well. Work files on disk stay indented.

## Not doing (quality risk)

- **Grouping reviews.** The review is the last gate: an LLM `approved` makes a question playable (D-33). Its main job is looking at every candidate on a contact sheet; titles hid wrong subjects in batch-4. With several questions and sheets in one session, each picture gets less attention. One call per question stays.
- **Grouping fact-checks across subcategories.** With web search, more claims per session likely means fewer searches per claim. The calls are cheap (sonnet, $1.42 for batch-5). If ever tried: groups of at most 5, verdicts compared against single-subcategory calls first.
- **Merging rate and factcheck into one call.** It loses the independent second opinion, and opus with web search costs more per call.
- **Drafting two subcategories per call.** Drafting is where quality starts; one subcategory per call keeps it focused.
- **Moving rate, revise or review to sonnet.** That changes the model, not the number of calls, and likely costs quality.

## Expected result
About 225 → 180–185 calls per batch (−18 %), about 300k fewer input tokens, nothing changed in what decides quality.

## How to check
Implement after batch-5 is done, so batch-5 is a clean baseline and no run mixes old and new grouping. On the next batch, compare against batch-4 and batch-5:
- calls and cost (`batch-report`, `costs.log`);
- share approved, share `needs_work` and its reasons, share dropped by `merge`, especially duplicates;
- average rater scores and the number of revisions (to see whether grouped rating got more lenient).

If approval or the share of revisions moves clearly, go back to per-subcategory rating or revising and note why here.

## Part 2: where questions come from

### Today
`fit` scores the ~30 lines of `authoring/data/question-styles.txt` per subcategory and keeps up to 4, each with a one-line idea from Claude. `draft` turns each idea into a question and avoids the answers listed under "Already in the pool". The content comes entirely from Claude, in one pass. The style picks the form; the idea, written in the same call, is still whatever comes to mind first.

What the pool shows (513 questions, 2026-10-07):
- **Content falls back to the most famous facts.** All of `Espacio`: el Sol, la Luna, Marte (planeta rojo), Saturno (anillos), Júpiter (el más grande), Venus (el más caliente), Neil Armstrong, la Vía Láctea, 8 minutos de luz, año luz. An avoid list only pushes the next batch to the next most famous fact.
- **Styles bunch up.** "Plain fact" (90), "picture → name" (77) and "name the concept" (30) make up about half of the generated questions; most styles were used fewer than 10 times.
- **`fun` is the weakest rater score for every style** (3.2–4.1; the hard criteria average about 4.8). Media styles score highest (zoomed-in detail 4.1), "plain fact" 3.5.

### Principles
- **Never ask an LLM for "surprising", "little-known" or "curious" facts.** It has no reliable sense of surprise: asked for a surprising fact about Saturn, any LLM says that Saturn would float. Prompts don't ask for a surprising angle.
- **Interesting facts come from using up the obvious ones.** Every question about a concept stays in the pool and is shown to the next draft about that concept as "already asked". Once "anillos" and "flotaría en agua" are taken, the next question about Saturn has to go further. So the obvious facts carry less and less weight as the pool grows. Concepts are reused, not removed.
- **Randomness and coverage come from code**, from stored lists and from counts over the pool, not from the LLM.
- **Stored once, reused every batch.** Concept lists and style fits are files in the repo, not output that gets thrown away after each batch.

### Concept lists (PE-8)
One file per subcategory, `authoring/data/concepts/<slug>.json`, committed (plain text; reusing them saves regenerating them):

```json
{"subcategory": "Espacio",
 "facets": ["Planetas", "Misiones y astronautas", "Constelaciones y mitos", ...],
 "concepts": [{"name": "Saturno", "facet": "Planetas", "familiarity": 5},
              {"name": "Eclipse solar", "facet": "Fenómenos", "familiarity": 4, "retired": "nada nuevo que preguntar"}]}
```

- **Facets first, then concepts.** `qgen concepts` makes two calls per subcategory: (1) 8–12 facets that cover the subcategory broadly, plus the axis fit (PE-9); (2) 15–25 concepts per facet, about 150–250 per subcategory (OQ-38, D-37), plus the concept and axes of each existing question. A flat list written in one go starts strong and then repeats itself or gets obscure; the facets are what bring breadth.
- **Bare names, no facts or hooks.** A concept is a name ("Saturno"), not a fact about it. Facts come later in the draft, where they get fact-checked.
- **`familiarity` 1–5**: how well a Colombian family knows the concept, written in the same call. It lets code match concepts to target difficulty (below). The draft's difficulty estimate still decides.
- **No overlap across subcategories.** The calls run in parallel and save raw results in `work/concepts/`; one sequential pass then writes the lists. A concept whose normalized name is already in another list (existing lists first, then `categories.json` order) is dropped and reported, unless a question of this subcategory uses it (then both keep it). Synonyms and nicknames aren't caught (OQ-40, D-37).
- **Existing questions get a concept.** Call (2) also receives the subcategory's existing questions and returns a concept for each (adding one to the list if needed). Questions store it in a new `concept` field, and their axes in `axes` (OQ-39, D-37). Without this, "Saturno" would show up as unused. The sequential pass writes both into the pool in one go.
- **Usage is counted from the pool, not stored in the list.** The number of questions per concept comes from `questions.json` (all statuses), so there is one source of truth. The list stores only `retired` (below).
- **Top-up:** when fewer than 30 concepts in a list are unused and not retired, `qgen concepts --top-up` adds about 60 concepts (new facets allowed). `--fill` tops a list up to 250, the upper end of the target size. The call gets the number to add and the list's names to avoid.
- **In the batch:** the `concepts` step replaces `fit`. It makes the lists that the batch's subcategories don't have yet and tops up those running low; `qgen concepts` without arguments makes all missing lists at once.

Cost: about 2 × 140 = 280 calls once, roughly one batch. After that, `draft` gets a short concept section instead of a long avoid list.

### Question styles as axes (PE-7)
The style list mixes things that are really separate: media ("showing a picture"), the kind of thinking ("estimate a number", "what do these three have in common"), content templates ("origin of a food") and answer types ("which year"). It is replaced by independent axes in `authoring/data/question-axes.json`. A question is one value on each axis:

| Axis | What it varies | Values (first draft) |
|---|---|---|
| **Move** | what the player has to do | identify, name the concept, word meaning, count, estimate, real-world record, origin, made of / parts, what it's for, cause and effect, sequence (before/after, what comes next), connection (what three have in common), analogy ("A es a B como C es a…"), odd one out ("¿cuál NO…?"), who made/said/discovered, when |
| **Stimulus** | what the screen shows or plays as part of the question | none (illustrative/decorative image only), photo, zoomed-in detail, silhouette, map outline, sound, video. *Blurred/pixelated dropped: the game has no effect for it and Commons rarely has such pictures (B-7).* |
| **Clue form** | how the clue is worded | direct question, riddle in first person ("Tengo… ¿qué soy?"), everyday scenario ("Estás en la cocina y…"), completion (saying, quote, lyric), three facts (not for people: D-16) |
| **Answer kind** | what the four options are | thing or animal, person or character, place, number, year or era, word or term, group or category |
| **Lens** | where the player has met the topic | school, university (basics of a discipline, classic theories and experiments), everyday life, Colombia, pop culture (films, TV, games, books, music), popular science (books, thought experiments, stories behind discoveries), science news (settled facts only), educational media (documentaries, educational YouTube, science and history TV, museums), nature, history, body and senses, words and language. *No value refers to an age: who can answer is the difficulty's job (2026-10-07).* |
| **Difficulty** | who can answer it | 1–10, assigned by code as today (`assign_difficulties`) |

- The values above are a first draft for the gamemaster to edit (OQ-39). Every value has one line of explanation in the file, which goes into the prompts. All values follow the house style ("use the four options honestly", media only from Commons, no songs or film clips).
- **Compatibility rules** are in the same file and applied by code: e.g. `sound` only with `identify`; `map outline` only with answer kind `place`; `when` only with `year or era`; `count`/`estimate` only with `number`.
- **Axis fit is scored once per subcategory and stored** (PE-9): a 1–5 score for each value of move, stimulus and lens, in the subcategory's concept file (`"axis_fit": {...}`), from call (1) of `qgen concepts`. That replaces the `fit` step in every batch; `fit`, `fit.md` and `question-styles.txt` are removed. Clue form and answer kind are not scored per subcategory: the compatibility rules and the drafter handle them.
- Existing questions keep their `style` as history; every question gets `axes: {move, stimulus, clue, answer_kind, lens}` (new ones from the draft, old ones from `qgen concepts`; OQ-39, D-37).
- `stimulus` other than `none` means essential media; `none` means illustrative or decorative.

### Drafting from concepts and axes (PE-10)
For each subcategory in a batch, code (seeded, as `assign_difficulties` is today) builds 4 slots (`--slots`, as many as `fit` allowed styles before):

1. **Draw concepts.** The weight drops with the number of questions the concept already has (e.g. `1 / (1 + uses)²`), so untouched concepts usually come first, but used ones come back and push past their obvious facts. Retired concepts are never drawn. `familiarity` is matched to the slot's target difficulty (familiar concepts for easy slots, less familiar ones for hard slots). This is a preference, not a filter.
2. **Draw 3 axis combinations per slot**, each compatible. Code first lists every compatible combination whose values fit the subcategory (fit 3–5; 1–2 never), then draws axis by axis (stimulus, move, answer kind, clue, lens) among the values that can still be completed, so a media stimulus isn't outnumbered by the many text-only combinations. The weight of a value is its base weight (`weights` in the axes file; stimulus `none` 7, `photo` 1.5, … for about 35 % media) × its fit × `1 / (1 + used / expected)` for the subcategory and again for the whole pool, where `expected` is the value's share of the base weights; × 0.3 if an earlier slot of the same subcategory already offered it. So unused moves, stimuli and lenses keep getting drawn until they're covered: the same "keep adding" principle as for content.
3. **Draft.** The drafter gets per slot: the concept, the target difficulty and the 3 combinations, and picks the one that makes the best question, or skips the slot. With the concept come **all questions already in the pool about that concept** (question and answer in full), as "already asked: ask something else". The per-subcategory list (PE-4) stays for overlap between concepts.
4. **Retire.** Every skip says whether the concept is `used_up` (nothing new to ask) or `unaskable` (no good question for this family), or neither. The first two set `retired` on the concept in its list, with the reason.

The drafter answers with the number of the combination it chose; code records that combination in `axes`. The lower weight for values already offered keeps one value from taking over within a subcategory.

### How to check (PE-13)
Part 2 was implemented right after part 1 (2026-10-07), so the next batch has both, and PE-6 and PE-13 are checked on the same batch against batch-4 and batch-5. PE-6's quality risk (grouped rating getting more lenient) can still be checked on its own: rate batch-5's drafts again in groups and compare with their per-file ratings (about 5 calls). For part 2, compare the first concept-based batch:
- average `fun` score; spread of moves, stimuli and lenses (and of `style` before);
- share of slots skipped, and of concepts retired;
- a blind side-by-side for the gamemaster: 20 old and 20 new questions from the same subcategories, without labels.

## Tasks
- [x] PE-1 `rate` in groups of about 10 questions, never splitting a subcategory; results saved per draft file. *`grouped()` packs whole draft files; a file whose questions all came back is saved, the rest fails and is retried. Mocked on batch-5's drafts: 44 questions, 24 files → 5 calls. `rate.md`: rate every question on its own.*
- [x] PE-2 `revise` in groups of about 10 questions with issues, never splitting a subcategory; results saved per draft file. *Files without issues are saved empty without a call; a missing result now fails the file instead of passing silently. `revise.md`: decide every question on its own.*
- [x] PE-3 Keep a `confirmed` fact-check when a revision changed none of `question`, `answer`, `wrong_answers`, `hints`, `fun_fact`. *`apply_to_drafts` leaves the verdict in its file; `factcheck` skips ids that already have a verdict, and `merge` finds it through `collect()`.*
- [x] PE-4 "Already in the pool" for the draft's own subcategory only. *Batch-5's 30 draft prompts: about 1.1 KB on average (was about 38 KB).*
- [x] PE-5 Compact JSON in prompt payloads. *draft, rate, factcheck, revise and review.*
- [ ] PE-6 Compare the first batch with PE-1..PE-5 against batch-4 and batch-5 (see "How to check"); record the result here
- [x] PE-7 `authoring/data/question-axes.json`: axes, values with one-line explanations, compatibility rules; replaces `question-styles.txt` for new questions (values: OQ-39). *2026-10-07: 5 axes, 17 rules, base `weights` for stimulus; `blurred` dropped (B-7). `question-styles.txt` and `fit` removed.*
- [x] PE-8 `qgen concepts`: facets, then concepts with `familiarity`, per subcategory in `authoring/data/concepts/<slug>.json`; no names shared across subcategories; tag existing questions with `concept`; `--top-up` (size: OQ-38). *Logic in `authoring/tools/concepts.py`. First real list: Espacio, 12 facets, 216 concepts, its 11 questions tagged (2 calls). The other 139 lists are made by the batches that need them, or all at once with `qgen concepts`.*
- [x] PE-9 Axis fit (move, stimulus, lens) scored once per subcategory and stored in its concept file; `qgen batch` drops the `fit` step. *In call (1) of `qgen concepts`; the batch's first step is now `concepts` (creates and tops up its lists).*
- [x] PE-10 `draft` draws concepts (fewer uses first, familiarity matched to difficulty) and 3 compatible axis combinations per slot (fit × rarely used); shows all questions about the concept; retires used-up or unaskable concepts. *Slots are drawn once per run into `slots.json`. Real smoke test on Espacio: 4 of 4 written (tardígrado, Franklin Chang-Díaz, Caronte, binoculares).*
- [x] PE-11 Schema and `qgen validate`: `concept` (must be in its subcategory's list) and `axes` (values from PE-7) on new questions. *Unknown axis values and duplicate names in a list are errors; broken rules only warnings (older questions were tagged after the fact). `merge` and `import` carry both fields; `report` and `batch-report` count axes.*
- [x] PE-12 Prompts: `fit.md` and `draft.md` rewritten for concepts and axes; no prompt asks for "surprising" or "little-known" angles. *`fit.md` replaced by `concepts-facets.md`, `concepts-list.md`, `concepts-topup.md`; `draft.md` rewritten. The house style still asks for a "surprising" `fun_fact` (not an angle; left as is).*
- [ ] PE-13 Compare the first concept-based batch against the PE-6 batch (see "How to check" in part 2); record the result here
