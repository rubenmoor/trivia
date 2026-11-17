"""`qgen video-window [--dry-run] [--model opus]`: every video question cut to its ≤ 30 s play window and
re-checked (plan 216, milestone 21 "video length and size"). Developer-run, like `qgen rework`.

Picks video questions (any bundle, any batch, not rejected) whose window plays more than 30 s or whose
`media.duration` is unknown: the duration is probed and filled, the window cut to `media.play_window`
({start, start + 30}; no excerpt → {0, 30}). An approved question's cut window is probed, run through the
giveaway step and `media_first.judge_window`: pass → stays approved with the cut excerpt; fail → needs_work
(problem media, "clue outside the 30 s window"), kept with the cut window for `qgen rework`. Other statuses
only get the cut. Translations need nothing: export takes media and status from the source.

Resumable: a written question no longer qualifies; outcomes in work/video-window/results.jsonl.
"""
import datetime, json, threading

import layout  # paths (D-35)
from layout import SOURCE_POOL as POOL
import download  # authoring/tools/download.py: the media cache
import media  # authoring/tools/media.py: play_window, MAX_VIDEO_SECONDS
import media_first  # authoring/tools/media_first.py: probe, giveaway, judge_window (plan 217)
import media_probe  # authoring/tools/media_probe.py: ffprobe
import progress  # authoring/tools/progress.py

from qgen import PROBLEMS, load_json, parallel  # authoring/tools/qgen.py
from review_steps import update_pool  # authoring/tools/review_steps.py: the locked pool writer

DIR = media_first.JUDGE_DIR  # under work/: results.jsonl next to the judgement's calls.jsonl
NOTE = "clue outside the 30 s window"
_lock = threading.Lock()


def plan(q):
    """What the re-check does to a question: "duration" (probe it, then maybe cut), "cut", or None."""
    m = q.get("media") or {}
    if m.get("type") != "video" or q["status"] == "rejected":
        return None
    if not m.get("duration"):
        return "duration"
    x = m.get("excerpt")
    span = x["end"] - x["start"] if x else m["duration"]
    return "cut" if span > media.MAX_VIDEO_SECONDS else None


def duration(m):
    """Seconds of the file the game plays (the cache's copy of `file_url`)."""
    return round(media_probe.streams(download.cached(m["file_url"]))[0], 2)


def check(q, model):
    """One question → its outcome row, pool written. Approved + cut → probe, giveaway, judgement."""
    m = dict(q["media"])
    row = {"id": q["id"], "bundle": q.get("bundle") or "base", "status": q["status"], "from": m.get("excerpt"),
           "duration_filled": not m.get("duration")}
    if not m.get("duration"):
        m["duration"] = duration(m)
    w, x = media.play_window(m), m.get("excerpt")
    cut = w is not None and (x["end"] - x["start"] if x else m["duration"]) > media.MAX_VIDEO_SECONDS
    row |= {"to": w if cut else x, "verdict": None}
    fields = {"duration": m["duration"], **({"excerpt": w} if cut else {})}
    review = None
    if cut and q["status"] == "approved":
        p = media_first.probe(media_first.file_title(m), w)
        if q.get("media_first"):
            fields["probe"] = media_first.probe_ref(p)
        hits = media_first.giveaway(q, p)
        v = ({"verdict": "needs_work", "problem": "giveaway", "note": f"answer heard or seen in it: {', '.join(hits)}"}
             if hits else media_first.judge_window({**q, "media": m}, w, p, model))
        row |= v
        if v["verdict"] == "needs_work":
            review = needs_work_review(q, v)
    update_pool({q["id"]: lambda x, f=fields, r=review: apply(x, f, r)})
    append(row)
    progress.detail(f"  video-window: {q['id']}: {describe(row)}")
    return row


def needs_work_review(q, v):
    old = {k: val for k, val in (q.get("review") or {}).items() if k != "previous"}
    kinds = {"media", v["problem"]}
    return {"decision": "needs_work", "feedback": f"{NOTE[0].upper()}{NOTE[1:]}: {v['note']}".rstrip(": ") + ".",
            "problems": [p for p in PROBLEMS if p in kinds], "reviewed_on": datetime.date.today().isoformat(),
            "reviewer": "llm", "model": media_first.JUDGE_MODEL, "previous": old or None}


def apply(x, fields, review):
    probe = fields.pop("probe", None)
    x["media"].update(fields)
    if probe:
        x["media_first"]["probe"] = probe
    if review:
        x.update(review=review, status="needs_work")


def results_path():
    return layout.WORK / DIR / "results.jsonl"


def append(row):
    path = results_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with _lock, open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def span(x):
    return f"{x['start']:g}–{x['end']:g} s" if x else "whole file"


def describe(row):
    s = (f"cut {span(row['from'])} → {span(row['to'])}" if row["to"] != row["from"] else "no cut")
    s += ", duration filled" if row["duration_filled"] else ""
    return s + (f", {row['verdict']}" + (f" ({row['problem']}: {row['note']})" if row["verdict"] == "needs_work" else "")
                if row["verdict"] else "")


def dry_run(todo):
    """Per bundle: what would change; no probes, no claude calls."""
    by = {}
    for q, what in todo:
        x = q["media"].get("excerpt")
        line = (f"{q['id']} ({q['status']}): cut {span(x)} → {span(media.play_window(q['media']))}" if what == "cut"
                else f"{q['id']} ({q['status']}): duration unknown: probe and fill, cut if over {media.MAX_VIDEO_SECONDS} s")
        by.setdefault(q.get("bundle") or "base", []).append(line)
    for b, lines in sorted(by.items()):
        print(f"{b}: {len(lines)}")
        print("\n".join(f"  {line}" for line in lines))
    print(f"{len(todo)} video question(s) would change; nothing written.")


def cmd_video_window(args):
    todo = [(q, w) for q in load_json(POOL)["questions"] if (w := plan(q))]
    if args.dry_run:
        return dry_run(todo) or []
    if not todo:
        print("No video question plays more than 30 s or lacks its duration.")
        return []
    print(f"video-window: {len(todo)} video question(s) to check", flush=True)
    rows = []
    errors = parallel(lambda q: rows.append(check(q, args.model)), [q for q, _ in todo], args.jobs, "video-window", "questions")
    summary(rows)
    if rows:
        print("Next: qgen export, trivia-media sync --status approved; commit authoring/data/questions.json, app/data/.")
    return errors


def summary(rows):
    by = {}
    for r in rows:
        n = by.setdefault(r["bundle"], {"cut": 0, "duration": 0, "kept": 0, "needs_work": 0})
        n["cut"] += r["to"] != r["from"]
        n["duration"] += r["duration_filled"]
        n["kept"] += r["verdict"] == "keep"
        n["needs_work"] += r["verdict"] == "needs_work"
    for b, n in sorted(by.items()):
        print(f"  {b}: {n['cut']} cut, {n['duration']} duration filled, {n['kept']} still approved, {n['needs_work']} needs_work")


def add_parser(sub):
    p = sub.add_parser("video-window", help="cut every video question to its 30 s window and re-check it (plan 216); developer-run")
    p.set_defaults(fn=cmd_video_window, run=None)
    p.add_argument("--dry-run", action="store_true", help="list per bundle what would change; no probes, no claude calls")
    p.add_argument("--model", default=media_first.JUDGE_MODEL, help="model of the window judgement (default opus)")
    p.add_argument("--jobs", type=int, default=3, help="parallel questions")
