"""Copies of a question into another bundle (decision 217, D-entry in plans/decisions.md). Never ships (D-35).

A copy is a source of its own (`copied_from` = the source's id); no link afterwards. `copied_from` is provenance:
fit pass, stats and validate read it; fixes to the source don't propagate."""
import copy

import translations  # authoring/tools/translations.py


class NotCopyable(ValueError):
    pass


def english(src, en_translations=None):
    """The source's English text fields, or None: an en source's own; an es (or other) source's approved,
    non-stale en translation (`en_translations`: {id: entry}, default questions.en.json)."""
    if translations.source_locale(src) == "en":
        return {k: copy.deepcopy(src[k]) for k in translations.TEXT_FIELDS + ["difficulty"]}
    by_id = en_translations if en_translations is not None else {t["id"]: t for t in translations.load("en")["questions"]}
    t = by_id.get(src["id"])
    if t and t.get("status") == "approved" and not translations.is_stale(t, src):
        return {k: copy.deepcopy(t[k]) for k in translations.TEXT_FIELDS + ["difficulty"]}
    return None


def next_id(questions):
    return "q-%04d" % (max(int(q["id"][2:]) for q in questions) + 1)


def copy_question(src_id, bundle, subcategory, questions, batch, status="needs_work", en_translations=None):
    """The new source for a copy of `src_id` in `bundle`/`subcategory`; `questions`: the pool's list (id
    source, duplicate check); the caller appends and saves it. Refused (NotCopyable): unknown source, a copy
    itself, the same bundle, a second copy in `bundle`, no English text."""
    by_id = {q["id"]: q for q in questions}
    src = by_id.get(src_id)
    if src is None:
        raise NotCopyable(f"{src_id}: no such question")
    if src.get("copied_from"):
        raise NotCopyable(f"{src_id}: is a copy of {src['copied_from']}; copy the original")
    if src.get("bundle") == bundle:
        raise NotCopyable(f"{src_id}: already in {bundle}")
    if any(q.get("copied_from") == src_id and q.get("bundle") == bundle for q in questions):
        raise NotCopyable(f"{src_id}: already copied into {bundle}")
    text = english(src, en_translations)
    if text is None:
        raise NotCopyable(f"{src_id}: no English text (an approved, current en translation is needed)")
    new = {**copy.deepcopy(src), **text, "id": next_id(questions), "status": status, "bundle": bundle,
           "locale": "en", "subcategory": subcategory, "copied_from": src_id,
           "concept": None, "axes": None, "quality": None, "batch": batch, "review": None}
    return new


def media_fixed(q):
    """The question's `media` is fixed, never searched or picked again: a media-first question's file (plan 203)
    or a copy's, shared with its source."""
    return bool(q.get("media_first") or q.get("copied_from"))


def related(a, b):
    """a and b are a source and its copy (either way, ids or tmp ids): not duplicates of each other."""
    ia, ib = a.get("id"), b.get("id")
    return bool(ia and ib and (a.get("copied_from") == ib or b.get("copied_from") == ia))
