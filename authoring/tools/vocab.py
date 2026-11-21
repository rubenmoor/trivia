"""The zh-Hant vocabulary pass (decision 797): prompts/vocab-zh-Hant.md reads each converted row (hant.py) next to its
zh-Hans row and English source and fixes only Taiwan vocabulary, quotes and titles; recurring terms go to
authoring/data/zh-hant-exceptions.json. Run as a step of `qgen batch --translate zh-Hant`; run `vocab-zh-Hant-<n>`.
The first run is the pilot (PILOT rows); more runs wait for `qgen health ack vocab-zh-Hant-1`. Never ships (D-35)."""
import datetime, json, threading

import atomic  # authoring/tools/atomic.py
import hant  # authoring/tools/hant.py: the conversion and its exceptions list
import progress  # authoring/tools/progress.py
import translations  # authoring/tools/translations.py
from layout import PROMPTS, WORK

from qgen import STR, claude, costs, load_json, parallel, save_json, write_report  # authoring/tools/qgen.py

MODE = "vocab-zh-Hant"  # run names `vocab-zh-Hant-<n>`
PILOT = 50  # rows of the first run
CHUNK = 50  # rows per call
MODEL = "opus"
TRIES = 3
VERDICTS = ("ok", "fix", "flag")
SKIP = "skip"  # recorded in `vocab`, never asked of the model
FIELDS = translations.TEXT_FIELDS
TEXT = {"type": "object", "required": FIELDS, "properties": {
    **{k: STR for k in FIELDS if k not in ("wrong_answers", "hints", "fun_fact")},
    "wrong_answers": {"type": "array", "items": STR}, "hints": {"type": "array", "items": STR},
    "fun_fact": {"type": ["string", "null"]}}}
SCHEMA = {"type": "object", "required": ["items"], "properties": {"items": {"type": "array", "items": {
    "type": "object", "required": ["id", "verdict", "text", "pairs", "note"],
    "properties": {"id": STR, "verdict": {"type": "string", "enum": list(VERDICTS)}, "text": {**TEXT, "type": ["object", "null"]},
                   "note": STR, "pairs": {"type": "array", "items": {"type": "object", "required": ["hans", "hant"],
                                                                      "properties": {"hans": STR, "hant": STR}}}}}}}}


def system():
    return (PROMPTS / "vocab-zh-Hant.md").read_text(encoding="utf-8")


def fields(t):
    return {k: t.get(k) for k in FIELDS}


def joined(t):
    return " ".join(x for k in FIELDS for x in (t[k] if isinstance(t.get(k), list) else [t.get(k)]) if x)


def english(q, en):
    """The source's English text fields (its own, or its approved English translation), or None."""
    e = fields(q) if translations.source_locale(q) == "en" else fields(en[q["id"]]) if q["id"] in en else None
    return e


def pending(bundle, pool, hants):
    """Converted, approved rows of `bundle` the pass hasn't read, in id order."""
    src = {q["id"]: q for q in pool}
    return sorted((t for t in hants if t.get("converted_from") and t.get("status") == "approved" and not t.get("vocab")
                   and (src.get(t["id"], {}).get("bundle") or "base") == bundle), key=lambda t: t["id"])


def problems(old, new):
    """Why a `fix` answer can't be used ([] = usable): same shape, same numbers, answer still distinct."""
    out = []
    for k in FIELDS:
        if isinstance(old.get(k), list) != isinstance(new.get(k), list) or (isinstance(old.get(k), list) and len(old[k]) != len(new[k])):
            out.append(f"{k}: shape changed")
        elif (old.get(k) is None) != (new.get(k) is None) or (isinstance(new.get(k), str) and not new[k].strip()):
            out.append(f"{k}: emptied or filled")
    if out:
        return out
    if not hant_numbers_equal(old, new):
        out.append("numbers changed")
    if new["answer"] in new["wrong_answers"]:
        out.append("answer equals a wrong answer")
    return out


def good_pairs(new, pairs, hans, terms):
    """The exception pairs that are a clean whole term (at least two characters) of the Simplified text, present in
    the corrected text and not in conflict with the list."""
    return [p for p in pairs if len(p["hans"]) >= 2 and not {"\n", hant.MARK} & set(p["hans"] + p["hant"]) and p["hans"] in hans
            and p["hant"] in joined(new) and terms.get(p["hans"], p["hant"]) == p["hant"]]


def hant_numbers_equal(old, new):
    import translate  # authoring/tools/translate.py: the translation number check (imports this module's caller)
    return translate.same_numbers(joined(old), joined(new))


def ask(rows, hans, en, run, model):
    """{id: answer} for `rows`; a missing or unusable item is asked again (TRIES calls at most), then `skip`."""
    d = WORK / run
    sys_prompt, terms = system(), hant.exceptions()
    items = [{"id": t["id"], "zh_hans": fields(hans[t["id"]]), "zh_hant": fields(t), "en": en.get(t["id"])} for t in rows]
    got, why = {}, {}
    for _ in range(TRIES):
        left = [it for it in items if it["id"] not in got]
        if not left:
            break
        out, _m = claude(sys_prompt, "## Items\n" + json.dumps(left, ensure_ascii=False), SCHEMA, model, d, with_model=True)
        for x in out["items"]:
            row = next((t for t in rows if t["id"] == x["id"]), None)
            if row is None or x["id"] in got:
                continue
            if x["verdict"] == "fix" and (x["text"] is None or (bad := problems(row, x["text"]))):
                why[x["id"]] = "; ".join(bad) if x["text"] else "no text"
                continue
            if x["verdict"] == "flag" and not x["note"].strip():
                continue
            if x["verdict"] == "fix":
                x["pairs"] = good_pairs(x["text"], x["pairs"], joined(hans[x["id"]]), terms)
            got[x["id"]] = x
    for t in rows:  # never usable: stays as converted, for the native read
        if t["id"] not in got:
            got[t["id"]] = {"id": t["id"], "verdict": "skip", "text": None, "pairs": [],
                            "note": f"no usable answer after {TRIES} tries: {why.get(t['id'], 'skipped by the model')}"}
    return got


def add_terms(pairs):
    """New pairs into the exceptions list (kept as is: a term the list has stays); returns the ones added."""
    with atomic.locked(hant.EXCEPTIONS):
        doc = json.loads(hant.EXCEPTIONS.read_text(encoding="utf-8"))
        new = {p["hans"]: p["hant"] for p in pairs if p["hans"] not in doc["terms"]}
        if new:
            doc["terms"] |= new
            atomic.write_json(hant.EXCEPTIONS, doc)
    return new


def apply(answers, run, model):
    """Write the answers into questions.zh-Hant.json for rows still unread: fix → fields; flag → needs_work; every
    row gets `vocab`. Returns {id: change} for the report."""
    today, report = datetime.date.today().isoformat(), {}
    with translations.locked(hant.LOCALE):
        doc = translations.load(hant.LOCALE)
        for t in doc["questions"]:
            x = answers.get(t["id"])
            if x is None or t.get("vocab") or t.get("status") != "approved":
                continue
            before = fields(t)
            if x["verdict"] == "fix":
                t.update({k: x["text"][k] for k in FIELDS})
            elif x["verdict"] == "flag":
                t.update(status="needs_work", review={"decision": "needs_work", "feedback": f"vocabulary pass: {x['note']}",
                                                      "problems": ["other"], "reviewed_on": today, "reviewer": "llm", "model": model})
            t["vocab"] = {"run": run, "on": today, "verdict": x["verdict"]}
            report[t["id"]] = {"verdict": x["verdict"], "note": x["note"], "before": before, "after": fields(t), "pairs": x["pairs"]}
        translations.save(hant.LOCALE, doc)
    return report


def runs():
    return sorted((p.parent.name for p in WORK.glob(f"{MODE}-*/run.json")), key=lambda r: int(r.rsplit("-", 1)[1]))


def run_pass(bundle, pool, jobs, count=None):
    """One run of the pass over the bundle's unread converted rows; returns (run, report) or None when nothing is
    to do or the pilot waits for its ack."""
    import health  # authoring/tools/health.py (imports qgen)
    past = runs()
    open_run = past[-1] if past and not load_json(WORK / past[-1] / "run.json").get("done") else None
    if past and not open_run and f"{MODE}-1" not in health.acks():
        print(f"vocabulary pass: the pilot {MODE}-1 waits for the developer's look: qgen health ack {MODE}-1 \"<note>\"")
        return None
    rows = pending(bundle, pool, translations.load(hant.LOCALE)["questions"])
    rows = rows[:count or (PILOT if not past else len(rows))] if not open_run else rows[:len(load_json(WORK / open_run / "run.json")["ids"])]
    if not rows:
        print("vocabulary pass: no converted row unread.")
        return None
    run = open_run or f"{MODE}-{len(past) + 1}"
    d = WORK / run
    if not open_run:
        save_json(d / "run.json", {"mode": "vocab", "locale": hant.LOCALE, "bundle": bundle, "model": MODEL, "ids": [t["id"] for t in rows],
                                   "started": datetime.date.today().isoformat()})
    hans = {t["id"]: t for t in translations.load(hant.FROM)["questions"]}
    en_tr = {t["id"]: t for t in translations.load("en")["questions"]}
    src = {q["id"]: q for q in pool}
    en = {t["id"]: english(src[t["id"]], en_tr) for t in rows}
    lock = threading.Lock()

    def work(group):
        got = ask(group, hans, en, run, MODEL)
        rep = apply(got, run, MODEL)
        new = add_terms([p for x in got.values() for p in x["pairs"]])
        with lock:  # the run's record, kept over a resume: the report is made from it
            cfg = load_json(d / "run.json")
            save_json(d / "run.json", {**cfg, "report": cfg.get("report", {}) | rep, "terms": cfg.get("terms", {}) | new})

    progress.say(f"vocabulary pass {run}: {len(rows)} rows")
    errors = parallel(work, [rows[k:k + CHUNK] for k in range(0, len(rows), CHUNK)], jobs, "vocab", "calls")
    cfg = load_json(d / "run.json")
    if not errors:
        save_json(d / "run.json", {**cfg, "done": datetime.date.today().isoformat()})
    write_vocab_report(run, cfg.get("report", {}), cfg.get("terms", {}))
    return run, cfg.get("report", {}), cfg.get("terms", {}), errors


def write_vocab_report(run, report, terms):
    """authoring/reports/<run>.md: counts, every change with before → after, new exception terms, cost."""
    n = {v: sum(r["verdict"] == v for r in report.values()) for v in (*VERDICTS, SKIP)}
    c = costs(WORK / run)
    lines = [f"# {run}", "", f"Made by the vocabulary pass of `qgen batch --translate zh-Hant` on {datetime.date.today().isoformat()} "
             "(decision 797): converted zh-Hant rows read against zh-Hans and English (`prompts/vocab-zh-Hant.md`). Generated file: don't edit by hand.", "",
             f"- Rows read: {len(report)}: {n['ok']} ok, {n['fix']} fixed, {n['flag']} flagged (needs work), {n['skip']} skipped",
             f"- New exception terms: {len(terms)}", f"- Claude calls: {len(c)}, about ${sum(c):.2f} at list price", "", "## Flagged", ""]
    lines += [f"- **{i}** {r['note']}: {r['before']['question']}" for i, r in sorted(report.items()) if r["verdict"] == "flag"] or ["None."]
    lines += ["", "## Skipped (left as converted)", ""]
    lines += [f"- **{i}** {r['note']}" for i, r in sorted(report.items()) if r["verdict"] == SKIP] or ["None."]
    lines += ["", "## Fixed", ""]
    for i, r in sorted(report.items()):
        if r["verdict"] == "fix":
            diff = [f"  - {k}: {r['before'][k]} → {r['after'][k]}" for k in FIELDS if r["before"][k] != r["after"][k]]
            lines += [f"- **{i}**" + (f" ({r['note']})" if r["note"] else ""), *diff]
    lines += ["", "## New exception terms", ""] + ([f"- {a} → {b}" for a, b in terms.items()] or ["None."])
    return write_report(run, lines)
