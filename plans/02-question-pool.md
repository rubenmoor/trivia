# 02 — Question Pool

**Status:** draft — **first focus area**

## Purpose
A curated, reusable set of questions. Each question has an answer, an image, and metadata. Questions are marked **burned** for a player once that player has seen them, so later sessions stay fresh (D-28).

## Schema (D-6, D-7, D-8)
The pool lives in `authoring/data/questions.json`: `{"version": 1, "questions": [...]}`. Categories live in `app/data/categories.json` (D-19): `{"categories": [{"slug", "name", "subcategories": [...]}]}`, broad categories in display order; a question's broad category is the one that lists its `subcategory`. Field names are English; content is Spanish.
```jsonc
{
  "id": "q-0001",              // stable, never reused
  "status": "draft",           // draft | approved | rejected | needs_work (D-11)
  "difficulty": 1,             // shared scale 1–15 (D-38): 1 = a 6-year-old can answer .. 10 = a 16-year-old .. 15 = specialists
  "description": "Esta pregunta ondea al viento y canta el himno con la mano en el pecho.",  // humorous intro, shown instead of the category (D-8)
  "question": "¿De qué colores es la bandera de Colombia?",
  "answer": "Amarillo, azul y rojo",
  "wrong_answers": ["…", "…", "…"],   // exactly 3; the client shuffles
  "hints": ["vague", "medium", "strong"],  // exactly 3
  "media": {
    "type": "image",           // image | audio | video
    "role": "decorative",      // decorative (mood, blurred; must not give the answer away) | illustrative (shows the question's subject, sharp; must not give the answer away, D-24) | essential (part of the question)
    "query": "Colombian Andes landscape",  // search term for sourcing (06-images.md)
    "note": null,              // what exactly to play/show, for audio and video
    "source_url": null, "file_url": null, "credit": null  // filled when the media is picked; file_url is the cache key (D-17)
  },
  "fun_fact": "Shown on the reveal screen."
}
```
Fields added for generated questions (QG-7, D-10); `null` on the first 120 (except `subcategory`, QP-11):
```jsonc
  "subcategory": "Volcanes",          // required; from app/data/categories.json (D-19)
  "style": "estimate a number",       // from authoring/data/question-styles.txt
  "quality": {"correct": 5, "unambiguous": 5, "distractors": 4, "age_fit": 4, "fun": 3, "description": 4, "difficulty_estimate": 6, "notes": "…"},
  "fact_checked": true,               // true = confirmed by web search; false = not checked or uncertain
  "needs_media": false,               // true = the style needs a specific picture/sound/video
  "batch": "pilot",                   // qgen.py run that produced it (RV-1)
  "revision": null,                   // set by `qgen.py apply` when a question was revised (07, QG-13)
  "difficulty_original": 6,           // set by the review tool when the gamemaster changes the difficulty; null otherwise
  "background": {"query": "misty forest", "source_url": null, "file_url": null, "credit": null}
                                      // only for audio questions (D-14), else null
```

Review result, set by the review tool (`08-review-tool.md`, D-11) or an LLM review (D-32); `null` until reviewed. `status` always equals `review.decision`; an `approved` question is playable whoever approved it (D-33):
```jsonc
  "review": {
    "decision": "needs_work", "feedback": "demasiado difícil", "reviewed_on": "2026-10-07",
    "reviewer": "human",        // human | llm (D-33)
    "model": null,              // the model for an LLM review, e.g. "claude-opus-5-5"; null for a human
    "previous": null            // only on a human review that replaced an LLM review: that LLM review
  }
```

Burned state is not in this file; it lives in SQLite (D-4), per player, plus a global burn set by the gamemaster (D-28, `03-game-flow.md`).

## Storage options
- Questions are stored in a single JSON file, `authoring/data/questions.json` (D-4). Split later if it grows unwieldy.
- ~~Burned state inline vs. separate~~ Burned state lives in SQLite, not in the question file (D-4). The `burned` and `burned_on` fields move out of the schema.

## Tasks
- [x] QP-1 Finalise the schema (formats, difficulty scale, categories). *2026-10-06, D-6/D-7; categories still proposed (OQ-8).*
- [x] QP-2 Decide the storage format and file layout. *2026-10-06, single `authoring/data/questions.json` (D-4).*
- [x] QP-3 Define the target pool size (sessions × 12 + spares). *2026-10-06, ~120 (D-6).*
- [x] QP-4 Choose categories, with family interests in mind. *2026-10-06: 24 broad categories with 140 subcategories in `app/data/categories.json` (D-19).*
- [x] QP-5 Write or collect the first batch of questions. *2026-10-06: 120 questions in `authoring/data/questions.json` (12 per category, 12 per difficulty level), descriptions added (D-8). Kept by the gamemaster; all still `status: "draft"` pending review (QP-10).*
- [x] QP-10 Gamemaster reviews the first 120 questions and sets each to `approved` or `rejected`. *2026-10-06: 117 approved, 3 rejected (D-23, `07-question-generation.md`).*
- [~] QP-9 Write the second batch of questions, step by step with the gamemaster (starting from a throw-away category list).
- [ ] QP-6 Attach an image to every question (see `06-images.md`).
- [~] QP-7 Write a validation script (required fields, unique IDs, image exists). *`authoring/tools/qgen.py validate` (image check once media is cached).*
- [x] QP-11 Give the first-120 a `subcategory` from the subcategory list; `qgen.py validate` checks every subcategory against it. *2026-10-06: 59 of the 140 subcategories used.*
- [x] QP-12 Group the subcategories into broad categories (`app/data/categories.json`, D-19) and migrate the pool and the pipeline. *2026-10-06: 24 categories; `category` and the old map removed from the pool, `categories.txt` removed; `fit` no longer maps; shared loader `app/server/categories.py`.*
- [x] QP-13 Stats pages in the web client: questions per broad category (sorted by count) and per difficulty (histogram). *2026-10-06: `/stats/categories`, `/stats/difficulty` (`authoring/ui/src/stats/`), `GET /api/categories`. Approved questions only, no status filter (gamemaster, 2026-10-06).*
- [x] QP-8 Implement burn and un-burn, plus a "remaining per category/difficulty" report. *2026-10-06: the final answer burns, the admin undo un-burns (`app/server/game.py`); `qgen.py report` shows unburned questions per category and difficulty, and the supply per level.*
- [x] QP-15 Record who reviewed a question (`review.reviewer`: human | llm, D-33); both make it playable, and the review tool keeps LLM-reviewed questions open for a later human check. *2026-10-07: existing reviews migrated to `human`; server, review tool and `validate` updated.*
- [x] QP-14 Burn per player (D-28): the `burned` table gets a player (NULL = burned for everyone); undo un-burns for that player; `qgen.py report --player <name>` shows the supply for one player. *2026-10-06: done with GF-6; `app/server/selection.py` `burned_ids(player)`; `report` without `--player` shows a new player's supply (global burns only).*
- [~] QP-16 Extend `base` categories: 6 independent LLM lists of ~50 pub-quiz categories, merged keeping only new topics (near-synonyms of existing categories or subcategories dropped). *2026-10-10: 50 new broad categories appended to `app/data/categories.json`, subcategories still empty; next: expand into subcategories, then `qgen batch`.*
