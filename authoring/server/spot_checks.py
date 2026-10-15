"""Human spot checks per batch (plan 16): the seeded sample and authoring/data/spot-checks.json.
Written by the authoring server (a run's "size" by hand, decision 228); `qgen report --qc` and the exit check read the file."""
import datetime, json, re

import layout  # authoring/tools/layout.py
import atomic  # authoring/tools/atomic.py
import qgen  # authoring/tools/qgen.py: audit sample, LLM decisions, audits
import translations  # authoring/tools/translations.py

FILE = layout.SPOT_CHECKS


def size(batch=None):
    return qgen.spot_check_size(batch)


def sample(batch):
    """The batch's (or back-audit run's) spot-check ids in order: the first `size(batch)` of the audit sample."""
    return qgen.audit_sample(batch, size(batch))


def run_ids(run):
    """The ids of a back-audit (plan 57) or neutralize run (plan 64), or None for any other name."""
    m = re.fullmatch(r"(backaudit|neutralize)-\d+", run)
    if not m:
        return None
    cfg = qgen.load_json(qgen.WORK / run / "run.json", {}) or {}
    return cfg.get("ids") if cfg.get("mode") == m.group(1) else None


def load():
    return json.loads(FILE.read_text(encoding="utf-8")) if FILE.exists() else {}


def save(data):
    atomic.write_json(FILE, data)


def record(batch, q, media_changed):
    """Store the spot check of q from its human review (D-33); returns the item.
    `batch` is q's batch, a back-audit run with q in it (plan 57) or a translation run: then
    q's translation in that run is checked and the item gets "locale" (plan 67)."""
    locale = translations.run_locale(batch)
    if locale:
        q = next((t for t in translations.load(locale)["questions"] if t["id"] == q["id"]), None) or {"id": q["id"]}
    rv = q.get("review") or {}
    if q.get("batch") != batch and q["id"] not in (run_ids(batch) or ()):
        raise ValueError(f"{q['id']} is not in {batch}")
    if q["id"] not in sample(batch):
        raise ValueError(f"{q['id']} is not in {batch}'s spot-check sample")
    if rv.get("reviewer") != "human":
        raise ValueError(f"{q['id']} has no human review yet")
    llm = qgen.llm_decisions(batch).get(q["id"])
    if llm is None:
        raise ValueError(f"{q['id']} has no recorded LLM review")
    a = qgen.translation_audit_of(q) if locale else qgen.audit_of(q)
    item = {"llm": llm, "audit": a and ("problem" if qgen.is_major(a) else "ok"), "human": rv["decision"],
            "problems": rv.get("problems") or [],
            "difficulty": [q.get("difficulty_original") or q["difficulty"], q["difficulty"]],
            "media_changed": bool(media_changed), "on": datetime.date.today().isoformat()}
    if locale:
        item["locale"] = locale
    with atomic.locked(FILE):
        data = load()
        entry = data.setdefault(batch, {"size": size(batch), "seed": batch, "items": {}})
        entry["items"][q["id"]] = item
        save(data)
    return item


def remove(batch, qid):
    """Undo: drop the item (and the batch once it has none)."""
    with atomic.locked(FILE):
        data = load()
        items = data.get(batch, {}).get("items", {})
        if items.pop(qid, None) is not None:
            if not items:
                del data[batch]
            save(data)
