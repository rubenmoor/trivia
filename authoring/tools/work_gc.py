"""`qgen gc`: delete the review images of finished, checked batches from work/ (task 2182; the media cache: media_keep.py).

A rework, tighten or neutralize run qualifies when it is `done` and every question it touched (`ids`) has a human
review or a review dated after the run (task 2360).
A batch qualifies when its run.json is `done` and its spot check is complete (spot-checks.json holds its
spot-check size of items; `--unchecked` waives that for batches from before spot checks). The developer runs it
after the batch's QC (authoring/QC.md); nothing can tell it that the QC is finished.
- `work/<batch>/sheets/`: contact sheets for `review`; nothing reads them once the batch is merged.
- a probe's `frames/`, `thumbs/`, `sheet.png`, `spectrogram.png`, `waveform.png` (the review page's pictures),
  only when every work dir and pool question that mentions the probe belongs to a qualifying batch.
  `probe.json`, `speech.txt`, `ocr.txt` stay (they save re-probing); a probe nobody mentions stays whole.
A deleted picture: the review page lists none; `rm <probe>/probe.json`, then `qgen media-probe` makes it again."""
import re, shutil

import atomic  # authoring/tools/atomic.py


import audit  # authoring/tools/audit.py
from layout import SOURCE_POOL, SPOT_CHECKS, WORK
from media_probe import OUT as PROBES  # authoring/tools/media_probe.py

IMAGES = ("frames", "thumbs", "sheet.png", "spectrogram.png", "waveform.png")
SKIP = {"media-probe", "media", "ship-media", "models", "media-survey"}  # not runs; gallery* are images only
_SHA = re.compile(r"\b[0-9a-f]{16}\b")


def _read(p):
    return atomic.read_json(p) if p.is_file() else None


REWORKS = ("rework", "tighten", "neutralize", "fit")


def _settled(run, questions):
    """Every touched question: human-reviewed, or reviewed after the run finished (a later run)."""
    done = str(run["done"])[:10]
    for qid in run.get("ids") or []:
        rv = (questions.get(qid) or {}).get("review") or {}
        if rv and rv.get("reviewer") != "human" and str(rv.get("reviewed_on") or "")[:10] <= done:
            return False
    return True


def qualifies(name, unchecked=False, questions=None):
    run = _read(WORK / name / "run.json") or {}
    if run.get("mode") in REWORKS and run.get("done"):
        if questions is None:
            questions = {q["id"]: q for q in (_read(SOURCE_POOL) or {}).get("questions", [])}
        return _settled(run, questions)
    if run.get("mode") not in ("batch", "media-first") or not run.get("done"):
        return False
    if unchecked:
        return True
    items = ((_read(SPOT_CHECKS) or {}).get(name) or {}).get("items") or {}
    return len(items) >= audit.spot_check_size(name)


def _size(p):
    return sum(f.stat().st_size for f in p.rglob("*") if f.is_file()) if p.is_dir() else p.stat().st_size


def _remove(p, dry_run):
    n, b = (sum(1 for f in p.rglob("*") if f.is_file()), _size(p)) if p.is_dir() else (1, _size(p))
    if not dry_run:
        shutil.rmtree(p) if p.is_dir() else p.unlink(missing_ok=True)
    return n, b


def referrers():
    """{probe sha: set of owners}: a work dir name, or 'pool' for a question whose batch is unknown."""
    probes = {p.name for p in PROBES.iterdir() if p.is_dir()} if PROBES.is_dir() else set()
    refs, batch_of = {}, {}
    for d in sorted(WORK.iterdir()):
        if not d.is_dir() or d.name in SKIP or d.name.startswith("gallery"):
            continue
        for qid in (_read(d / "ids.json") or {}).values():
            batch_of.setdefault(qid, d.name)
        for f in d.rglob("*"):
            if f.is_file() and f.suffix in (".json", ".jsonl") and f.name != "calls.jsonl":
                for sha in set(_SHA.findall(f.read_text(encoding="utf-8", errors="replace"))) & probes:
                    refs.setdefault(sha, set()).add(d.name)
    for q in (_read(SOURCE_POOL) or {}).get("questions", []):
        ref = (q.get("media_first") or {}).get("probe")
        if ref and ref.rsplit("/", 1)[-1] in probes:
            refs.setdefault(ref.rsplit("/", 1)[-1], set()).add(batch_of.get(q["id"], "pool"))
    return refs


def gc(dry_run=False, unchecked=False):
    """Returns (files, bytes) deleted (or that would be)."""
    ok = {}
    qs = {q["id"]: q for q in (_read(SOURCE_POOL) or {}).get("questions", [])}
    good = lambda n: ok.setdefault(n, qualifies(n, unchecked, qs))
    total = [0, 0]
    def take(r):
        total[0] += r[0]; total[1] += r[1]
    for d in sorted(WORK.glob("*/sheets")):
        if good(d.parent.name):
            take(_remove(d, dry_run))
    for sha, owners in referrers().items():
        if all(good(o) for o in owners):
            for n in IMAGES:
                if (PROBES / sha / n).exists():
                    take(_remove(PROBES / sha / n, dry_run))
    return tuple(total)


def cmd_gc(args):
    import progress
    n, b = gc(args.dry_run, args.unchecked)
    progress.say(f"gc: {'would delete' if args.dry_run else 'deleted'} {n} file(s), {b / 1e9:.2f} GB")
