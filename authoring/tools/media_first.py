"""`qgen batch --media-first`'s inventory, ledger and steps probe, triage, design, giveaway (plan 203).

A run starts from surveyed Commons files (`media_survey`: work/media-survey/files.jsonl). The ledger
work/media-first/files.jsonl holds every file any run triaged, so none is offered twice. `select` picks a run's
files, seed by seed in yield order, and writes the queue to the run dir so a resume takes the same files.
`triage` probes and triages the queue (sonnet) until enough files are worth it; `design` writes an EN draft per
worth file (opus), probes its excerpt window and checks it (`problems`, `giveaway`): one retry with the problems,
then dropped. Results per file in <run>/media-first/{triage,design}.jsonl; passed drafts in <run>/drafts/mf-*.json.
`qgen batch --media-first` runs these as its first steps (`inventory_step`, `probe_step`, `triage`, `design`,
`check_drafts`), then qgen's; `check_fixed` is the giveaway check after `fix`.
"""
import hashlib, json, re, threading
from collections import defaultdict
from pathlib import Path
from types import SimpleNamespace

import atomic, categories, layout, progress
import media_probe, media_survey
from media import MAX_AUDIO_SECONDS, excerpt_schema, pick_fields  # authoring/tools/media.py

MF_DESIGNED = 120        # designed questions per run (≈ 100 approved at the pilot's look share)
PROBE_JOBS = 4          # probes are local (ffmpeg, whisper), more than the claude calls' 3
SKIP_AFTER = 15          # a seed with 0 worth it after this many triaged files is skipped from then on
MAX_PER_SEED = 30        # files of one seed in a run's queue (spread over seeds)
PRIOR = 0.24             # pilot's worth-it share (authoring/reports/media-first-feasibility.md), smooths seed yield
SURVEY_FILES = media_survey.OUT / "files.jsonl"
LEDGER = layout.WORK / "media-first" / "files.jsonl"
QUEUE = "media-first-files.jsonl"  # in the run dir
STEP_DIR = "media-first"           # in the run dir: triage.jsonl, design.jsonl
TRIAGE_MODEL, DESIGN_MODEL = "sonnet", "opus"
KINDS = ("animal", "instrument", "language", "machine", "place", "event-person", "piece-film", "video-scene")
BANDS = 5                # triage difficulty 1–5 over the shared scale
PD_CLASSES = ("pd-music", "pd-film")
# Zero-yield seeds of the feasibility report: Lingua Libre, newsreels, church bells, trains/cars/aircraft audio,
# ambience, bird-song search, city names. Skipped until the ledger shows one worth it.
ZERO_YIELD = {
    "cat:Lingua Libre pronunciation", "q:audio:pronunciation of city name", "q:audio:spoken language sample",
    "q:video:newsreel", "cat:Newsreels by country", "q:audio:church bells",
    "q:audio:train sound", "q:audio:car engine sound", "q:audio:aircraft sound", "q:audio:machine noise",
    "q:audio:ocean waves wind", "q:audio:rainforest sounds", "q:audio:city ambience street sounds",
    "q:audio:bird song",
}


def read_jsonl(path):
    return [json.loads(l) for l in path.read_text(encoding="utf-8").split("\n") if l] if path.exists() else []


def write_jsonl(path, rows):
    atomic.write_text(path, "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))


def ledger():
    """Ledger rows: {title, seed, run, worth (bool), verdict}."""
    return read_jsonl(LEDGER)


def record(run, rows):
    """Add triaged files to the ledger: rows {title, seed, worth, verdict}; a title already in it is kept as is."""
    with atomic.locked(LEDGER):
        have = ledger()
        known = {media_survey.norm_title(r["title"]) for r in have}
        new = [{**r, "run": run} for r in rows if media_survey.norm_title(r["title"]) not in known]
        if new:
            write_jsonl(LEDGER, have + new)
    return len(new)


def pilot_rows():
    """The pilot's triaged files (history) (aided verdict, else blind): {title, seed, worth}."""
    by = {}
    for f in sorted((layout.WORK / "media-pilot").glob("*/triage.jsonl")):
        for r in read_jsonl(f):
            if r["title"] not in by or r.get("mode") == "aided":
                by[r["title"]] = {"title": r["title"], "seed": r["seed"], "worth": bool(r["worth"])}
    return list(by.values())


def seed_stats(rows):
    """{seed: [triaged, worth]} over rows."""
    st = defaultdict(lambda: [0, 0])
    for r in rows:
        st[r["seed"]][0] += 1
        st[r["seed"]][1] += bool(r["worth"])
    return st


def seed_yield(stat):
    """Worth-it share, smoothed toward the pilot's overall share."""
    n, w = stat
    return (w + PRIOR * 2) / (n + 2)


def skipped(seed, stats):
    n, w = stats.get(seed, (0, 0))
    return w == 0 and (n >= SKIP_AFTER or seed in ZERO_YIELD)


def used_titles(rows=None):
    return {media_survey.norm_title(r["title"]) for r in (pilot_rows() + ledger() if rows is None else rows)}


def survey_files(crawl=True):
    """The survey's kept files; a missing file is crawled first (resumable: `qgen media-survey --resume`)."""
    if not SURVEY_FILES.exists() and crawl:
        media_survey.cmd_media_survey(SimpleNamespace(limit=None, resume=True))
    return read_jsonl(SURVEY_FILES)


def inventory(files, rows, in_pool, limit=None):
    """Files a run may triage, in queue order: not triaged before, not in a pool, seed not skipped; seeds by
    descending yield (ties by id), at most MAX_PER_SEED per seed, survey order within a seed. `limit` cuts the queue."""
    stats = seed_stats(rows)
    seen = used_titles(rows)
    by = defaultdict(list)
    for f in files:
        key = media_survey.norm_title(f["title"])
        if key in seen or key in in_pool or skipped(f["seed"], stats):
            continue
        by[f["seed"]].append(f)
    order = sorted(by, key=lambda s: (-seed_yield(stats.get(s, (0, 0))), s))
    queue = [f for s in order for f in by[s][:MAX_PER_SEED]]
    return queue[:limit] if limit else queue


def select(run_dir, limit=None):
    """The run's queue: written to run_dir on first call, read back after (a resume takes the same files)."""
    path = run_dir / QUEUE
    if path.exists():
        return read_jsonl(path)
    queue = inventory(survey_files(), pilot_rows() + ledger(), media_survey.pool_media(), limit)
    write_jsonl(path, queue)
    return queue


def inventory_step(run_dir, limit=None):
    """`qgen batch --media-first`'s first step: the run's queue (`select`); an empty one fails."""
    from qgen import failed
    n = len(select(run_dir, limit))
    progress.say(f"  inventory: {n} file(s) queued")
    return [] if n else failed("inventory: no surveyed file left to triage (more seeds: `qgen media-survey`)")


def remaining(run_dir, run):
    """The queue's files not yet in the ledger and whose seed isn't skipped by now (the ledger grows during the run)."""
    done = {media_survey.norm_title(r["title"]) for r in ledger() if r["run"] == run}
    stats = seed_stats(pilot_rows() + ledger())
    return [f for f in select(run_dir) if media_survey.norm_title(f["title"]) not in done and not skipped(f["seed"], stats)]


# --- probe ---------------------------------------------------------------------

def probe(title, excerpt=None):
    """The judging aids of a file, or of its excerpt window (`media_probe`, cached per window)."""
    s, e = (excerpt["start"], excerpt["end"]) if excerpt else (None, None)
    return media_probe.cached(title, s, e) or media_probe.probe(title, s, e)


def probe_ref(p):
    """A probe's dir as stored in `media_first.probe`: relative to work/."""
    return Path(p["dir"]).resolve().relative_to(layout.WORK.resolve()).as_posix()


def load_probe(ref):
    d = layout.WORK / ref
    return json.loads((d / "probe.json").read_text()) | {"dir": str(d)}


def aids(p):
    """The probe as a prompt's aids: numbers inline, pictures as paths to Read (no waveform: feasibility report)."""
    d = Path(p["dir"])
    pics = [str(d / n) for n in ("sheet.png", "spectrogram.png") if (d / n).exists()]
    a = {k: p[k] for k in ("duration", "window", "has_video", "has_audio", "integrated_lufs", "range_lu",
                            "true_peak_dbfs", "silence_share") if k in p}
    if p.get("frames"):
        a["frame_times_s"] = {f["n"]: f["seconds"] for f in p["frames"]}
        a["ocr"] = [l for l in (d / "ocr.txt").read_text().splitlines() if not l.endswith(": ")]
    if p.get("speech"):
        a["speech"] = p["speech"]
    return {"pictures_to_read": pics, **a}


def round_size(todo, worth, target, jobs):
    """Files per triage round: ≈ twice what is still needed (None: all)."""
    return len(todo) if target is None else max(jobs, (target - worth) * 2)


def probe_step(d, run, jobs=PROBE_JOBS, target=MF_DESIGNED):
    """The `probe` step: the aids of the files triage's first round takes (later rounds probe inside triage)."""
    from qgen import parallel
    worth = sum(t["verdict"] == "worth" for t in triaged(d))
    todo = remaining(d, run)
    if target is not None and worth >= target:
        return []
    todo = todo[:round_size(todo, worth, target, jobs)]
    return parallel(lambda f: probe(f["title"]), [{"id": f["title"], **f} for f in todo], jobs, "probe", "files")


# --- giveaway (no LLM) -----------------------------------------------------------

STOP = {"this", "that", "with", "from", "sound", "sounds", "audio", "video", "file", "files", "recording", "call",
        "calls", "song", "music", "piece", "film", "footage", "scene", "view", "playing", "being"}


def words(text):
    return set(re.findall(r"[a-zà-ÿ]{4,}", text.lower()))


def heard_giveaway(answer, p):
    """Words of the answer (4+ letters, no filler) in the probe's speech or OCR text."""
    d = Path(p["dir"])
    said = (p.get("speech") or {}).get("text") or ""
    seen = (d / "ocr.txt").read_text() if (d / "ocr.txt").exists() else ""
    return sorted((words(answer) - STOP) & words(said + " " + seen))


def giveaway(q, p=None):
    """Answer and English key (`concept`) words in the played window's transcript or OCR; [] passes.
    `p`: the window's probe, else `media_first.probe`'s. Also after `fix`."""
    p = p or load_probe(q["media_first"]["probe"])
    return heard_giveaway(" ".join(t for t in (q["answer"], q.get("concept")) if t), p)


def check_drafts(d):
    """The `giveaway` step after design: a draft whose window names its answer leaves the run
    (<run>/media-first/giveaway.jsonl)."""
    from qgen import load_json, save_json
    out, lock = steps_dir(d) / "giveaway.jsonl", threading.Lock()
    for f in sorted((d / "drafts").glob("*.json")):
        data = load_json(f)
        keep = []
        for q in data["questions"]:
            hit = giveaway(q) if q.get("media_first") else []
            if hit:
                append(out, {"tmp_id": q["tmp_id"], "question": q["question"], "answer": q["answer"], "words": hit}, lock)
                progress.detail(f"  giveaway: {q['tmp_id']}: dropped: {', '.join(hit)}")
            else:
                keep.append(q)
        if len(keep) != len(data["questions"]):
            save_json(f, {**data, "questions": keep})
    return []


def check_fixed(run):
    """The `giveaway` step after `fix`: a revised question's giveaway words → reviews/<id>.json `giveaway`
    (`record` makes it needs_work)."""
    from qgen import load_json, save_json
    from review_steps import batch_questions, fixed
    n = 0
    for q in batch_questions(run):
        path = layout.WORK / run / "reviews" / f"{q['id']}.json"
        r = load_json(path, {})
        if q.get("media_first") and fixed(r):
            r["giveaway"] = giveaway(q)
            n += bool(r["giveaway"])
            save_json(path, r)
    if n:
        progress.say(f"  giveaway: {n} fixed question(s) name the answer in the window; they become needs_work")
    return []


def problems(q, p, model_check=None):
    """Why a designed draft can't go on: shape, media-first fields, a long file without excerpt, giveaways."""
    from qgen import check_question_shape  # qgen imports this module's users
    from validate import media_first_problems
    m = q["media"]
    out = check_question_shape(q) + media_first_problems(q)
    if m["duration"] > MAX_AUDIO_SECONDS and not m.get("excerpt"):
        out.append(f"the file is {round(m['duration'])} s: needs an excerpt of at most {MAX_AUDIO_SECONDS} s")
    hit = giveaway(q, p)
    if hit:
        out.append(f"giveaway: answer words heard or seen in the window (transcript/OCR): {', '.join(hit)}")
    if model_check and not model_check["passes"]:
        out.append(f"giveaway (your own check): {model_check['notes']}")
    return out


# --- shared inputs ---------------------------------------------------------------

def taxonomy_text(bundle="base"):
    return "\n".join(f"- {c['slug']}: {', '.join(c['subcategories'])}" for c in categories.load(bundle))


def subcategories():
    return sorted({s for c in categories.load("base") for s in c["subcategories"]})


def prompt_file(name, *before):
    from qgen import prompt
    return (prompt(*before, name, locale="en").replace("{max_s}", str(MAX_AUDIO_SECONDS))
            .replace("{taxonomy}", taxonomy_text()))


def base_subjects(pool):
    """{subcategory: sorted English subjects} of base's questions (not rejected): answer, concept (decision 232)."""
    from qgen import as_locale
    out = defaultdict(set)
    for q in as_locale([q for q in pool if q.get("bundle", "base") == "base" and q["status"] != "rejected"], "en"):
        out[q["subcategory"]] |= {t for t in (q["answer"], q.get("concept")) if t}
    return {s: sorted(v) for s, v in out.items()}


def gaps(pool):
    """What triage leans toward: difficulty band shares of the draft gaps, subcategories most needed first."""
    import batches
    from qgen import load_age_groups, target_weights
    lo, hi = load_age_groups()["scale"]
    w = target_weights(pool, "base")
    total = sum(w.values()) or 1
    bands = {b: round(sum(v for lvl, v in w.items() if band(lvl, lo, hi) == b) / total, 2) for b in range(1, BANDS + 1)}
    return {"difficulty_gaps": bands, "need": batches.subcategories(pool, len(subcategories()), "base")}


def band(level, lo, hi):
    return min(BANDS, 1 + (level - lo) * BANDS // (hi - lo + 1))


def band_levels(b, lo, hi):
    return [lvl for lvl in range(lo, hi + 1) if band(lvl, lo, hi) == b]


FILLER = {"a", "an", "the", "of", "and", "s", "from", "in", "on", "at", "by", "for", "during", "with"}


def known_subject(subject, keys):
    """The first key whose stemmed words are all in the subject's and make ≥ 1/3 of them ("Rooster" in "rooster
    crowing"; not "A flute" in "… from The Magic Flute": trial, task 2066), else None."""
    from qgen import stem
    have = set(stem(subject, "en").split()) - FILLER - STOP
    for k in keys:
        kw = set(stem(k, "en").split()) - FILLER - STOP
        if kw and kw <= have and 3 * len(kw) >= len(have):
            return k
    return None


def file_text(f):
    return {"title": f["title"], "description": f["description"], "type": f["type"], "class": f["class"],
            "duration_s": round(f["duration"] or 0, 1), "width": f["width"], "height": f["height"]}


def steps_dir(d):
    out = d / STEP_DIR
    out.mkdir(parents=True, exist_ok=True)
    return out


def append(path, rec, lock):
    with lock, open(path, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(rec, ensure_ascii=False) + "\n")


# --- triage (sonnet) -------------------------------------------------------------

def triage_schema():
    s, n = {"type": "string"}, {"type": ["string", "null"]}
    props = {"verdict": {"enum": ["worth", "duplicate", "not_worth"]}, "subject": s, "matches_title": {"type": "boolean"},
             "subcategory": {"enum": subcategories()}, "difficulty": {"type": "integer", "minimum": 1, "maximum": BANDS},
             "kind": {"enum": list(KINDS)}, "excerpt": excerpt_schema(), "why_not": n, "duplicate_of": n, "quality": s}
    return {"type": "object", "additionalProperties": False, "required": list(props), "properties": props}


def triaged(d):
    return read_jsonl(steps_dir(d) / "triage.jsonl")


def ledger_row(t):
    return {"title": t["title"], "seed": t["seed"], "worth": t["verdict"] == "worth", "verdict": t["verdict"],
            "subject": t["subject"]}


def triage(d, run, jobs=3, model=TRIAGE_MODEL, target=MF_DESIGNED):
    """Probe and triage the run's queue in seed-yield order until `target` files are worth it (None: the whole
    queue). A subject base or this run already has is `duplicate`; verdicts go to the run and the ledger. Errors."""
    from qgen import POOL, claude, load_json, parallel
    path, lock = steps_dir(d) / "triage.jsonl", threading.Lock()
    rows = triaged(d)
    record(run, [ledger_row(t) for t in rows])  # a kill between the two writes
    pool = load_json(POOL)["questions"]
    subjects, need = base_subjects(pool), gaps(pool)
    broad = {s: c["slug"] for c in categories.load("base") for s in c["subcategories"]}
    by_cat = defaultdict(list)
    for s, c in broad.items():
        by_cat[c].append(s)
    run_subjects = [t["subject"] for t in rows if t["verdict"] == "worth"]
    system = prompt_file("media-triage")
    failed, errors = set(), []

    def work(f):
        p = probe(f["title"])
        cats = f.get("base_categories") or []
        user = {"file": file_text(f), "aids": aids(p), **need,
                "base_subjects": {s: subjects.get(s, []) for c in cats for s in by_cat.get(c, [])},
                "run_subjects": list(run_subjects)}
        out = claude(system, json.dumps(user, ensure_ascii=False, indent=1), triage_schema(), model, d, read=True)
        with lock:
            if out["verdict"] == "worth":
                dup = known_subject(out["subject"], subjects.get(out["subcategory"], []) + run_subjects)
                if dup:
                    out |= {"verdict": "duplicate", "duplicate_of": dup, "why_not": f"base or this run has {dup}"}
                else:
                    run_subjects.append(out["subject"])
        t = {"title": f["title"], "seed": f["seed"], "class": f["class"], "category": broad[out["subcategory"]], **out}
        append(path, t, lock)
        record(run, [ledger_row(t)])

    while True:
        worth = sum(t["verdict"] == "worth" for t in triaged(d))
        todo = [f for f in remaining(d, run) if f["title"] not in failed]
        if not todo or (target is not None and worth >= target):
            break
        chunk = todo[:round_size(todo, worth, target, jobs)]
        errs = parallel(work, [{"id": f["title"], **f} for f in chunk], jobs, "triage", "files")
        failed |= {f["title"] for f in chunk} - {t["title"] for t in triaged(d)}
        errors += errs
    progress.detail(f"  triage: {worth} worth it of {len(triaged(d))} triaged")
    return errors


# --- design (opus) and its checks ------------------------------------------------

def design_schema():
    from qgen import load_age_groups
    lo, hi = load_age_groups()["scale"]
    s = {"type": "string"}
    three = {"type": "array", "items": s, "minItems": 3, "maxItems": 3}
    gw = {k: {"type": "boolean"} for k in ("spoken", "on_screen_text", "title_needed", "description", "passes")}
    work = {"anyOf": [{"type": "null"}, {"type": "object", "additionalProperties": False,
                                          "required": ["title", "creator", "year", "basis"],
                                          "properties": {"title": s, "creator": s, "year": {"type": ["integer", "string"]},
                                                         "basis": s}}]}
    props = {"question": s, "answer": s, "wrong_answers": three, "hints": three, "description": s, "fun_fact": s,
             "difficulty": {"type": "integer", "minimum": lo, "maximum": hi}, "subcategory": {"enum": subcategories()},
             "role": {"enum": ["essential", "illustrative"]}, "excerpt": excerpt_schema(), "media_note": s,
             "background_query": s, "work": work, "needs_fact_check": {"type": "boolean"},
             "giveaway": {"type": "object", "additionalProperties": False, "required": [*gw, "notes"],
                          "properties": gw | {"notes": s}}}
    return {"type": "object", "additionalProperties": False, "required": list(props), "properties": props}


def tmp_id(title):
    return "mf-" + hashlib.sha1(media_survey.norm_title(title).encode()).hexdigest()[:10]


def draft(f, t, out, p, window):
    """A draft question (qgen's draft shape) with `media` pre-filled from the file and `media_first` provenance."""
    audio = f["type"] == "audio"
    media = {**pick_fields(f), "role": out["role"], "query": f["title"], "note": out["media_note"] or None,
             "duration": p["duration"]}
    if out["excerpt"]:
        media["excerpt"] = out["excerpt"]
    if f["class"] in PD_CLASSES:
        media["work"] = out["work"]
    return {"tmp_id": tmp_id(f["title"]), "bundle": "base", "subcategory": out["subcategory"], "style": None,
            "axes": None, "concept": t["subject"], **{k: out[k] for k in (
                "difficulty", "description", "question", "answer", "wrong_answers", "hints", "fun_fact",
                "needs_fact_check")},
            "media": media, "needs_media": out["role"] == "essential",
            "background_query": out["background_query"] if audio else "",
            "media_first": {"seed": f["seed"], "class": f["class"], "kind": t["kind"], "probe": probe_ref(window)}}


def designed(d):
    return read_jsonl(steps_dir(d) / "design.jsonl")


def run_answers(d):
    """Answers of the run's passed designs: one question per answer in a run (trial, task 2066: 7 of 15 Beethoven)."""
    return [r["attempts"][-1]["question"]["answer"] for r in designed(d) if r["passed"]]


def design(d, jobs=3, model=DESIGN_MODEL):
    """An EN draft per worth file not designed yet: design, probe the window, check (`problems`); on problems one
    more design with them as `previous_attempt`, then dropped. Passed drafts → drafts/mf-*.json. Errors."""
    from qgen import claude, load_age_groups, parallel, save_json, stem
    path, lock = steps_dir(d) / "design.jsonl", threading.Lock()
    files = {f["title"]: f for f in select(d)}
    done = {r["title"] for r in designed(d)}
    todo = [t for t in triaged(d) if t["verdict"] == "worth" and t["title"] not in done and t["title"] in files]
    progress.resumed("design", len(done), len(todo), "files")
    lo, hi = load_age_groups()["scale"]
    system = prompt_file("media-design", "house-style")
    answers = {stem(a, "en"): a for a in run_answers(d)}

    def work(t):
        f = files[t["title"]]
        p = probe(f["title"])
        user = {"file": file_text(f), "triage": {k: t[k] for k in ("subject", "category", "subcategory", "kind",
                                                                     "excerpt", "quality")},
                "target_levels": band_levels(t["difficulty"], lo, hi), "aids": aids(p)}
        tries = []
        for _ in range(2):
            with lock:
                user["run_answers"] = sorted(answers.values())
            out = claude(system, json.dumps(user, ensure_ascii=False, indent=1), design_schema(), model, d, read=True)
            window = probe(f["title"], out["excerpt"]) if out["excerpt"] else p
            q = draft(f, t, out, p, window)
            found = problems(q, window, out["giveaway"])
            with lock:
                if stem(q["answer"], "en") in answers:
                    found.append(f"another question of this run already has the answer {q['answer']!r}: "
                                 "ask about something else this file shows")
                elif not found:
                    answers[stem(q["answer"], "en")] = q["answer"]
            tries.append({"question": q, "problems": found})
            if not found:
                break
            user["previous_attempt"] = {k: q[k] for k in ("question", "answer", "wrong_answers")} | {
                "excerpt": out["excerpt"], "problems": found}
            if out["excerpt"]:
                user["aids_of_that_window"] = aids(window)
        ok = not tries[-1]["problems"]
        append(path, {"title": f["title"], "passed": ok, "attempts": tries}, lock)
        if ok:
            save_json(d / "drafts" / f"{tries[-1]['question']['tmp_id']}.json",
                      {"questions": [tries[-1]["question"]], "skipped": []})
        progress.detail(f"  design: {t['subject']}: " + ("passed" if ok else "dropped: " + "; ".join(tries[-1]["problems"])))

    return parallel(work, [{"id": t["title"], **t} for t in todo], jobs, "design", "files")


# --- reports (decision 641) --------------------------------------------------------

MM_START, MM_TARGET = 58, 1058   # decision 641: multimedia base questions at the start, and the goal (start + 1000)
FUNNEL = ("files", "worth", "designed", "passed", "merged", "approved")


def is_multimedia(q):
    return (q.get("media") or {}).get("type") in ("audio", "video")


def multimedia_count(pool):
    """Decision 641: approved base sources with audio/video media (any role), the 58 at the start taken off;
    also the media share of approved base questions."""
    base = [q for q in pool if q["status"] == "approved" and q.get("bundle", "base") == "base"]
    n = sum(map(is_multimedia, base))
    return {"count": n, "added": n - MM_START, "target": MM_TARGET, "total": len(base),
            "share": n / len(base) if base else None}


def funnel(d, qs):
    """{"seed": {seed: row}, "class": {class: row}}, row = FUNNEL counts for the run dir `d` and its merged
    questions `qs`: files triaged → worth it → designed → passed (giveaway and shape) → merged → approved."""
    cls = {}
    out = {"seed": defaultdict(lambda: dict.fromkeys(FUNNEL, 0)), "class": defaultdict(lambda: dict.fromkeys(FUNNEL, 0))}

    def bump(seed, c, key):
        out["seed"][seed][key] += 1
        out["class"][c][key] += 1

    for t in triaged(d):
        cls[t["title"]] = (t["seed"], t["class"])
        bump(*cls[t["title"]], "files")
        if t["verdict"] == "worth":
            bump(*cls[t["title"]], "worth")
    for r in designed(d):
        seed_class = cls.get(r["title"])
        if seed_class:
            bump(*seed_class, "designed")
            if r["passed"]:
                bump(*seed_class, "passed")
    for q in qs:
        m = q.get("media_first") or {}
        if not m:
            continue
        for key in ("merged", *(("approved",) if q["status"] == "approved" else ())):
            bump(m["seed"], m["class"], key)
    return {k: dict(v) for k, v in out.items()}


def funnel_lines(d, qs, cost, approved):
    """Markdown lines of the batch report's media-first section."""
    f = funnel(d, qs)
    lines = ["## Media-first funnel", ""]
    for title, key in (("Per seed", "seed"), ("Per class", "class")):
        rows = sorted(f[key].items())
        tot = {k: sum(r[k] for _, r in rows) for k in FUNNEL}
        lines += [f"### {title}", "", "| " + key + " | " + " | ".join(FUNNEL) + " |",
                  "|" + "---|" * (len(FUNNEL) + 1)]
        lines += [f"| {n} | " + " | ".join(str(r[k]) for k in FUNNEL) + " |" for n, r in rows + [("total", tot)]]
        lines.append("")
    lines += ["- $ per approved: " + (f"${cost / approved:.2f}" if approved else "-"), ""]
    return lines
