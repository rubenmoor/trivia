"""Human spot checks per batch (plan 16): the seeded sample and authoring/data/spot-checks.json.
Written only by the authoring server; `qgen report --qc` and the exit check read the file."""
import datetime, json, threading

import layout  # authoring/tools/layout.py
import qgen  # authoring/tools/qgen.py: audit sample, LLM decisions, audits
import targets  # authoring/tools/targets.py

FILE = layout.SPOT_CHECKS
DEFAULT_SIZE = 30  # pm decision 2, until targets.json has "quality"
_lock = threading.Lock()


def size():
    return (targets.load_quality() or {}).get("spot_check_size", DEFAULT_SIZE)


def sample(batch):
    """The batch's spot-check ids in order: the first `size()` of the audit sample."""
    return qgen.audit_sample(batch, size())


def load():
    return json.loads(FILE.read_text(encoding="utf-8")) if FILE.exists() else {}


def save(data):
    tmp = FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(FILE)


def audit_of(q):
    """The audit of a question: the newest back-audit (plan 57), else work/<batch>/audit/<id>.json; or None."""
    return qgen.audit_of(q)


def record(batch, q, media_changed):
    """Store the spot check of q from its human review (D-33); returns the item."""
    rv = q.get("review") or {}
    if q.get("batch") != batch:
        raise ValueError(f"{q['id']} is not in {batch}")
    if q["id"] not in sample(batch):
        raise ValueError(f"{q['id']} is not in {batch}'s spot-check sample")
    if rv.get("reviewer") != "human":
        raise ValueError(f"{q['id']} has no human review yet")
    llm = qgen.llm_decisions(batch).get(q["id"])
    if llm is None:
        raise ValueError(f"{q['id']} has no recorded LLM review")
    a = audit_of(q)
    item = {"llm": llm, "audit": a and ("problem" if qgen.is_major(a) else "ok"), "human": rv["decision"],
            "problems": rv.get("problems") or [],
            "difficulty": [q.get("difficulty_original") or q["difficulty"], q["difficulty"]],
            "media_changed": bool(media_changed), "on": datetime.date.today().isoformat()}
    with _lock:
        data = load()
        entry = data.setdefault(batch, {"size": size(), "seed": batch, "items": {}})
        entry["items"][q["id"]] = item
        save(data)
    return item


def remove(batch, qid):
    """Undo: drop the item (and the batch once it has none)."""
    with _lock:
        data = load()
        items = data.get(batch, {}).get("items", {})
        if items.pop(qid, None) is not None:
            if not items:
                del data[batch]
            save(data)
