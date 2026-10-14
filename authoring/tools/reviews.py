"""Review writes on the source pool and the locale files, shared by trivia-authoring and qgen (plan 93).

Player feedback (game flags, pasted or pulled reports) becomes a human needs_work review: the new feedback first,
the older after «Antes:»; es reviews the source, en/de that locale's translation (decision 102).
"""
import datetime, json, re

import atomic  # authoring/tools/atomic.py
import layout  # authoring/tools/layout.py
import pool_export  # authoring/tools/pool_export.py
import translations  # authoring/tools/translations.py

POOL = layout.SOURCE_POOL
DECISIONS = {"approved", "rejected", "needs_work"}
REVIEWERS = {"human", "llm"}


class NoQuestion(KeyError):
    """No question (or translation) with this id: 404."""


def load_pool():
    return json.loads(POOL.read_text(encoding="utf-8"))


def save_pool(data):
    atomic.write_json(POOL, data)
    pool_export.write(data)  # the game reads only the export (D-35)


def update_question(qid, change):
    """Re-read the pool, apply change(q) to one question, write atomically (08, "API")."""
    with atomic.locked(POOL):
        data = load_pool()
        for q in data["questions"]:
            if q["id"] == qid:
                change(q)
                save_pool(data)
                return q
    raise NoQuestion(qid)


def update_translation(locale):
    """update_question for questions.<locale>.json; re-exports pool.<locale>.json and the packs' (plan 67)."""
    def update(qid, change):
        with atomic.locked(POOL), translations.locked(locale):  # POOL: the export reads it
            doc = translations.load(locale)
            for t in doc["questions"]:
                if t["id"] == qid:
                    change(t)
                    translations.save(locale, doc)
                    pool_export.write_texts(translations.export_texts(locale, load_pool()), locale)
                    return t
        raise NoQuestion(qid)
    return update


def now():
    """`reviewed_at`: local ISO time of a human verdict (plan 98, review time per 100)."""
    return datetime.datetime.now().isoformat(timespec="seconds")


def set_review(qid, review, update=update_question, timed=True):
    """Set or reset one question's review, or with `update` its translation's.
    A new decision is a human review; it keeps the LLM review it replaces as `previous` (D-33).
    A review that names its reviewer is an undo putting an earlier review back as it was.
    `timed`: a new decision gets `reviewed_at` (not for player reports)."""
    restore = review is not None and "reviewer" in review
    if review is not None:
        if review.get("decision") not in DECISIONS:
            raise ValueError("decision must be approved, rejected or needs_work")
        feedback = (review.get("feedback") or "").strip() or None
        if review["decision"] == "needs_work" and not feedback:
            raise ValueError("needs_work requires feedback")
        if restore and review["reviewer"] not in REVIEWERS:
            raise ValueError("reviewer must be human or llm")
        review = {"decision": review["decision"], "feedback": feedback,
                  "reviewed_on": review.get("reviewed_on") or datetime.date.today().isoformat(),
                  "reviewer": review.get("reviewer", "human"), "model": review.get("model"),
                  "previous": review.get("previous"), **({"problems": review["problems"]} if review.get("problems") else {})}
        at = review.get("reviewed_at") if restore else now() if timed else None
        if at:
            review["reviewed_at"] = at

    def change(q):
        if review is not None and not restore:
            old = q.get("review") or {}
            review["previous"] = old if old.get("reviewer") == "llm" else old.get("previous")
        q.update(review=review, status=review["decision"] if review else "draft")

    return update(qid, change)


def questions_of(locale):
    """{id: question} of the source (es) or a locale's translations; {} for another locale."""
    if locale == "es":
        return {q["id"]: q for q in load_pool()["questions"]}
    if locale in translations.LOCALES:
        return {t["id"]: t for t in translations.load(locale)["questions"]}
    return {}


def needs_work(qid, locale, feedback, known, dry_run=False):
    """`feedback` as a human needs_work review, older feedback kept after «Antes:».
    `known`: {locale: questions_of(locale)}, filled as needed and kept current.
    Returns the new feedback, None for an unknown question, "" when `feedback` is already there."""
    if locale not in known:
        known[locale] = questions_of(locale)
    q = known[locale].get(qid)
    if q is None:
        return None
    old = (q.get("review") or {}).get("feedback")
    if old and feedback in old:
        return ""
    new = f"{feedback} Antes: {old}" if old else feedback
    known[locale][qid] = {**q, "review": {**(q.get("review") or {}), "feedback": new}} if dry_run else set_review(
        qid, {"decision": "needs_work", "feedback": new}, update_translation(locale) if locale != "es" else update_question,
        timed=False)
    return new


def report_feedback(r):
    """A player report's feedback; `r`: question, lang, text, note?, version, pool?, date (plan 93)."""
    where = ", ".join([f"v{r['version']}", *([f"preguntas {r['pool']}"] if r.get("pool") else []), r["date"],
                       *([r["lang"]] if r["lang"] != "es" else [])])
    note = f": {r['note']}" if r.get("note") else "."
    seen = " / ".join(filter(None, (line.strip() for line in r["text"].splitlines())))
    return f"Reporte de jugador ({where}){note} · Vista: «{seen}»"


# Report text (decision 142): header, then labelled lines in the UI language
HEADER = re.compile(r"¡Trivia!\s*#(\S+)\s*·\s*([\w-]+)\s*·\s*v(\S+)\s*·\s*pool\s+(\S+)\s*·\s*(\d{4}-\d{2}-\d{2})")
LABELS = {"question": ("Pregunta", "Question", "Frage"), "answer": ("Respuesta", "Answer", "Antwort"),
          "note": ("Nota", "Note", "Notiz")}
LABEL = re.compile(r"^(%s):\s*(.*)$" % "|".join(l for ls in LABELS.values() for l in ls))


def parse_reports(text):
    """Report blocks in pasted text (chat around them ignored): dicts as report_feedback takes them."""
    out, cur = [], None
    for raw in text.splitlines():
        line = raw.strip().lstrip(">").strip()  # chat quotes
        if m := HEADER.search(line):
            cur = {"question": m[1], "lang": m[2], "version": m[3], "pool": None if m[4] == "?" else m[4],
                   "date": m[5], "lines": []}
            out.append(cur)
        elif cur is not None and (m := LABEL.match(line)):
            if m[1] in LABELS["note"]:
                cur["note"] = m[2].strip() or None
            else:
                cur["lines"].append(line)
        else:
            cur = None  # a blank line or chat ends the block
    for r in out:
        r["text"] = "\n".join(r.pop("lines"))
    return out
