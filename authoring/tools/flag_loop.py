"""The flag loop: open player flags with their age, the cause of each reworked flag, repeated causes (authoring/QC.md "Player reports").

Never ships (D-35). A flag is open while its question is `needs_work` with player feedback (game flag, pasted or pulled report).
"""
import datetime, json, re
from collections import Counter

import atomic  # authoring/tools/atomic.py
import layout  # authoring/tools/layout.py
import reviews  # authoring/tools/reviews.py: report/flag feedback, needs_work reviews
import translations  # authoring/tools/translations.py

CAUSES_FILE = layout.REPO / "authoring" / "data" / "flag-causes.json"  # [{id, date, run, cause, action, reason}]
PREFIXES = ("Marcada en el juego (", "Reporte de jugador (")  # reviews.report_feedback, server/main.py apply_flags
REPEATED = 3  # one cause this often proposes a prompt or QC change
CAUSES = {  # revise.md "Player flags"; the revise schema's enum
    "wrong_fact": "the answer or a stated fact was false",
    "ambiguous": "the question allows another reading or answer",
    "second_correct_option": "a wrong option was also right",
    "difficulty": "much easier or harder than its level",
    "language": "typo, grammar, regional wording or bad translation",
    "media": "the picture or sound does not fit or does not work",
    "tone": "offensive, dated or sensitive",
    "not_a_defect": "the question was fine",
    "other": "none of the above",
}


def is_player_feedback(text):
    return bool(text) and text.startswith(PREFIXES)


def open_flags(today=None):
    """[{id, locale (None = source), date, age, feedback}] of the needs_work questions a player flagged, oldest first."""
    today = today or datetime.date.today()
    out = []
    for locale in (None, *translations.LOCALES):
        for qid, q in reviews.questions_of(locale).items():
            fb = (q.get("review") or {}).get("feedback")
            if q["status"] != "needs_work" or not is_player_feedback(fb):
                continue
            date = re.search(r"\d{4}-\d{2}-\d{2}", fb.split(")")[0])  # the newest report comes first
            age = (today - datetime.date.fromisoformat(date[0])).days if date else None
            out.append({"id": qid, "locale": locale, "date": date and date[0], "age": age, "feedback": fb})
    return sorted(out, key=lambda f: -(f["age"] if f["age"] is not None else -1))


def open_lines(today=None):
    """Printable lines: the count, the oldest age, one line per open flag."""
    flags = open_flags(today)
    if not flags:
        return ["open player flags: none"]
    ages = [f["age"] for f in flags if f["age"] is not None]
    lines = [f"open player flags: {len(flags)}" + (f", oldest {max(ages)} days" if ages else "")
             + " (fix with `qgen rework`, the developer asks for it)"]
    for f in flags:
        lines.append(f"  {f['id']}{' (' + f['locale'] + ')' if f['locale'] else ''}: "
                     f"{'?' if f['age'] is None else f['age']} days: {f['feedback'][:110]}")
    return lines


def causes():
    return json.loads(CAUSES_FILE.read_text(encoding="utf-8")) if CAUSES_FILE.exists() else []


def record_causes(run, results):
    """Append the cause of each reworked flag; `results`: [{id, date?, cause, action, reason}]. Returns the new rows."""
    rows = [{"date": datetime.date.today().isoformat(), "run": run, **r} for r in results]
    if rows:
        atomic.write_json(CAUSES_FILE, [*causes(), *rows])
    return rows


def repeated():
    """{cause: count} of causes seen at least REPEATED times (not_a_defect and other excluded)."""
    n = Counter(c["cause"] for c in causes() if c["cause"] not in ("not_a_defect", "other"))
    return {k: v for k, v in n.most_common() if v >= REPEATED}


def lesson_lines():
    """The causes so far; a repeated one proposes a change for the developer to approve."""
    rows = causes()
    if not rows:
        return ["flag causes: none recorded yet"]
    n = Counter(c["cause"] for c in rows)
    lines = [f"flag causes ({len(rows)} reworked flags): " + ", ".join(f"{k} {v}" for k, v in n.most_common())]
    for cause, v in repeated().items():
        lines.append(f"  proposal: '{cause}' ({CAUSES[cause]}) seen {v} times: propose a change to the prompts "
                     "(draft.md, review.md, house-style.md) or a QC rule for it; the developer approves it as a decision "
                     "(authoring/QC.md \"Player reports\")")
    return lines
