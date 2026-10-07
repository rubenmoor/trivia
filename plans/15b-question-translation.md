# 15b — Question Translation

**Status:** stub

Sub-plan of [15](15-i18n.md). Translates the question pool into the launch languages (OQ-31). This is the big one: a question is more than its text. Its difficulty, distractors, hints and image all have to work in the new language and culture, so every translated question goes through rating, fact-checking and review again.

## What a translation has to get right
- **Text:** the question, the answer, the three wrong answers, the three hints, the description (D-8) and the `fun_fact`. Adapt, don't translate literally: units, the answer format, idioms.
- **Questions that don't travel:** wordplay, questions about the Spanish language itself ("¿Qué palabra…?"), and Colombian references whose answer only makes sense to Colombians. These are marked `region: "co"` (15c) or `translatable: false` and stay in Spanish only.
- **Distractors:** wrong answers that are plausible in Spanish can be absurd in another language (or accidentally correct). The rate step checks them again.
- **Hints:** a hint that plays on the Spanish word ("empieza por B") has to be rewritten.
- **Difficulty:** re-rated per locale (15). The age scale (D-6) stays the same; the rating is "for kids in that language's main market".
- **Media:** images are language-neutral, except ones with visible text (signs, book covers). The review flags those per locale. Essential audio (D-14) is usually language-neutral.

## Pipeline
A new step in `authoring/tools/qgen.py`, reusing the existing steps:

`translate --to en` → `rate --locale en` → `factcheck --locale en` → review (LLM review per D-32/D-33, plus a human spot check by a native speaker, sampled, e.g. 10 %) → merge.

- Only `approved` source questions are translated. A source question that changes later marks its translations `stale` (`validate` reports them).
- `costs.log` gives the cost per translated question; budget it before a full run (CT-3).

## Storage (decide in QT-1)
- **A: one file per locale** (`authoring/data/questions.en.json`) with the same IDs and only the translated fields plus their own `difficulty`, `status`, `review`. The Spanish file stays the source. Small diffs, easy to review.
- **B: a `translations` map inside each question.** One file, but `questions.json` grows with every language and gets harder to diff.
- Draft preference: **A**. The export (PORT-6) builds one playable pool per locale either way.

## Review tool
- `/review?batch=…&locale=en` shows the source and the translation side by side, with the same approve / needs work / reject decisions (RV-*).

## Tasks
- [ ] QT-1 Storage layout (A or B) and schema; `validate` covers translations and `stale`.
- [ ] QT-2 `qgen.py translate` with `translatable: false` / region detection; prompts in `authoring/tools/prompts/`.
- [ ] QT-3 `rate` and `factcheck` per locale.
- [ ] QT-4 Review tool: side-by-side locale view.
- [ ] QT-5 Pilot: translate 50 questions to English, review them, and measure the reject rate and cost before the full run.
- [ ] QT-6 Full translation per launch language; native-speaker spot check.
