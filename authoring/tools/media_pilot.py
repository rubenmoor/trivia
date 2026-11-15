"""`qgen media-pilot`: triage, design and aid ablation on a sample of surveyed Commons files (plan 201, step 3).

Sample ≈ N files of work/media-survey/files.jsonl, stratified by class and seed (fixed --seed), probe each
(`media_probe`), triage each twice (title + description only, then with every aid), design an EN question for
each file the aided triage finds worth it, check it for giveaways. Throw-away prompts in work/media-pilot/prompts/
(written on first run, editable; the real ones come in part 2). Output work/media-pilot/<run>/: sample.json,
triage.jsonl, questions.jsonl (never a pool), calls.jsonl, pilot.md, look.html. Rerun = resume.
"""
import html, json, random, threading, time
from collections import Counter, defaultdict
from pathlib import Path

import categories, layout, media_probe, progress
from media import MAX_AUDIO_SECONDS, excerpt_schema  # authoring/tools/media.py
from media_first import KINDS, STOP, heard_giveaway, words  # authoring/tools/media_first.py (plan 203)
from media_survey import CLASSES, OUT as SURVEY

OUT = layout.WORK / "media-pilot"
PROMPTS = OUT / "prompts"
SHARES = {"general": 0.64, "pd-music": 0.18, "pd-film": 0.18}  # pd classes apart (decision 640)
AIDS = ("frame_sheet", "ocr", "spectrogram", "waveform", "loudness", "silence", "speech")
EFFECTS = ("wrong_content", "spoken_giveaway", "written_giveaway", "quality_reject", "confirms", "none")

TRIAGE_MD = """You triage free media files from Wikimedia Commons for a family trivia game shown on a TV.
Each file may become one multiple-choice question whose answer comes from what players **hear or see**
(which animal, instrument, language, machine, place, event, piece or film; what is happening in a video).

You can't hear or watch the file. You get its Commons title and description, and maybe judging aids:
a numbered frame sheet with times (video), on-screen text found by OCR, a spectrogram and a waveform picture,
loudness (EBU R128 LUFS), the share of silence, and a local speech-to-text with its language guess.
Open every picture path given with the Read tool before you answer. Titles and descriptions on Commons are
often wrong or vague: trust the aids over the title where they disagree.

Decide:
- `worth`: would a good, fair, fun question for families anywhere come out of this file? Not worth it when:
  the content is unclear or not recognisable by ear/eye, poor quality (noise, near silence, clipping, tiny or
  shaky picture), the answer would only come from the title, the subject is too obscure or regional, the file
  is mostly speech in one language about something else, or the content is not family-friendly.
- `subject`: what the media really contains, in a few words (the would-be answer).
- `matches_title`: does the content match the title and description?
- `category` and `subcategory`: from the base list below.
- `difficulty`: 1 very easy (a child knows it) … 5 expert.
- `kind`: the question kind.
- `excerpt`: for a file longer than {max_s} s, the best {max_s} s or shorter window (start, end in seconds,
  from the frame times, the waveform, the speech); null when the whole file is fine.
- `why_not`: when not worth it, the reason in one line; else null.
- `quality`: one line on sound or picture quality.
- `aid_effects` (only when aids are given): for each aid you used, what it changed against the title alone:
  `wrong_content` (the aid shows the title or description is wrong), `spoken_giveaway` (speech names the answer),
  `written_giveaway` (text in the picture names the answer: caption, watermark, sign, file name),
  `quality_reject` (the aid shows the file is too poor), `confirms` (it confirms the title), `none`.

Classes: `general`; `pd-music` (a recording of public-domain music); `pd-film` (a public-domain film or
newsreel). Judge pd files like any other: is the piece or film famous enough that families recognise it?

Base categories and their subcategories:
{taxonomy}
"""

DESIGN_MD = """# Media-first question (pilot)

Above is the house style. Here the media comes first: you get one Commons file (title, description, class,
the triage's verdict) and judging aids in place of hearing or watching it (open every picture path with Read).
Write one English (`en`) question **built around this file**: the media is essential, and the answer comes from
what players hear or see, never from the file's title or description (players never see those).

- Pilot exception to "No songs, no film or TV clips": a file of class `pd-music` or `pd-film` (public-domain
  piece or film) may be the question's media ("Listen: which composer wrote this piece?").
- `excerpt`: the window to play (start, end seconds) when the file is longer than {max_s} s, or a shorter
  window makes it fairer; null for the whole file.
- `media_note`: what must be heard or seen in the excerpt.
- `background_query`: audio only, as the house style says; empty string for video.
- `giveaway`: check before you answer, against the aids: does the speech name the answer or an option
  (`spoken`)? does text in the picture (caption, title card, watermark, sign, file name) name it
  (`on_screen_text`)? can the question only be answered from the title (`title_needed`)? does the
  description give it away (`description`)? `passes` only when all four are false; `notes` names what you found.
"""

TAXONOMY_LINE = "- {slug}: {subs}"


def prompt_text(name, default):
    """The throw-away prompt from work/media-pilot/prompts/, written there on first use."""
    f = PROMPTS / f"{name}.md"
    if not f.exists():
        PROMPTS.mkdir(parents=True, exist_ok=True)
        f.write_text(default, encoding="utf-8")
    taxonomy = "\n".join(TAXONOMY_LINE.format(slug=c["slug"], subs=", ".join(c["subcategories"]))
                         for c in categories.load("base"))
    return f.read_text(encoding="utf-8").replace("{max_s}", str(MAX_AUDIO_SECONDS)).replace("{taxonomy}", taxonomy)


def sample(files, n, seed):
    """≈ n files: SHARES per class, then round robin over the class's seeds (shuffled with `seed`)."""
    rng = random.Random(seed)
    by = defaultdict(lambda: defaultdict(list))
    for f in files:
        by[f["class"]][f["seed"]].append(f)
    picked = []
    for cls in CLASSES:
        seeds = by.get(cls, {})
        pools = {s: rng.sample(v, len(v)) for s, v in sorted(seeds.items())}
        order = rng.sample(sorted(pools), len(pools))
        want, got = round(n * SHARES[cls]), []
        while len(got) < want and any(pools.values()):
            for s in order:
                if pools[s] and len(got) < want:
                    got.append(pools[s].pop())
        picked += got
    return picked


def slug_schema():
    cats = categories.load("base")
    return [c["slug"] for c in cats], sorted({s for c in cats for s in c["subcategories"]})


def triage_schema(aided):
    slugs, subs = slug_schema()
    props = {"worth": {"type": "boolean"}, "subject": {"type": "string"}, "matches_title": {"type": "boolean"},
             "category": {"enum": slugs}, "subcategory": {"enum": subs},
             "difficulty": {"type": "integer", "minimum": 1, "maximum": 5}, "kind": {"enum": list(KINDS)},
             "excerpt": excerpt_schema(), "why_not": {"type": ["string", "null"]}, "quality": {"type": "string"}}
    if aided:
        props["aid_effects"] = {"type": "array", "items": {
            "type": "object", "additionalProperties": False, "required": ["aid", "effect", "note"],
            "properties": {"aid": {"enum": list(AIDS)}, "effect": {"enum": list(EFFECTS)}, "note": {"type": "string"}}}}
    return {"type": "object", "additionalProperties": False, "required": list(props), "properties": props}


def design_schema():
    _, subs = slug_schema()
    s = {"type": "string"}
    three = {"type": "array", "items": s, "minItems": 3, "maxItems": 3}
    gw = {k: {"type": "boolean"} for k in ("spoken", "on_screen_text", "title_needed", "description", "passes")}
    props = {"question": s, "answer": s, "wrong_answers": three, "hints": three, "description": s, "fun_fact": s,
             "difficulty": {"type": "integer", "minimum": 1, "maximum": 15}, "subcategory": {"enum": subs},
             "excerpt": excerpt_schema(), "media_note": s, "background_query": s,
             "giveaway": {"type": "object", "additionalProperties": False, "required": [*gw, "notes"],
                          "properties": gw | {"notes": s}}}
    return {"type": "object", "additionalProperties": False, "required": list(props), "properties": props}


def file_text(f):
    return {"title": f["title"], "description": f["description"], "type": f["type"], "class": f["class"],
            "duration_s": round(f["duration"] or 0, 1), "width": f["width"], "height": f["height"]}


def aids_text(p):
    """The probe as the prompt's aids: numbers inline, pictures as paths to Read."""
    d = Path(p["dir"])
    pics = [str(d / n) for n in ("sheet.png", "spectrogram.png", "waveform.png") if (d / n).exists()]
    a = {k: p.get(k) for k in ("has_video", "has_audio", "integrated_lufs", "range_lu", "true_peak_dbfs",
                                "silence_share") if k in p}
    if p.get("frames"):
        a["frame_times_s"] = {f["n"]: f["seconds"] for f in p["frames"]}
        a["ocr"] = [l for l in (d / "ocr.txt").read_text().splitlines() if not l.endswith(": ")]
    if p.get("speech"):
        a["speech"] = p["speech"]
    return {"pictures_to_read": pics, **a}


def in_categories(subject, f):
    """Ground truth from Commons: a word of the subject in the file's categories."""
    return bool((words(subject) - STOP) & words(" ".join(f["categories"])))


def load_jsonl(p):
    return [json.loads(l) for l in p.read_text(encoding="utf-8").split("\n") if l.strip()] if p.exists() else []


def append(p, rec, lock):
    with lock, open(p, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(rec, ensure_ascii=False) + "\n")


def cmd_media_pilot(args):
    from qgen import calls, claude, parallel, prompt  # qgen imports this module
    t0 = time.monotonic()
    d = OUT / args.run
    d.mkdir(parents=True, exist_ok=True)
    sp = d / "sample.json"
    meta = json.loads(sp.read_text()) if sp.exists() else {"seed": args.seed, "n": 0, "files": []}
    if args.files > meta["n"]:  # new run, or a larger --files: the same seed's sample, extended
        files = load_jsonl(SURVEY / "files.jsonl")
        if not files:
            raise SystemExit("media-pilot: no work/media-survey/files.jsonl; run qgen media-survey first")
        have = {f["title"] for f in meta["files"]}
        meta |= {"n": args.files, "survey_files": len(files),
                 "files": meta["files"] + [f for f in sample(files, args.files, meta["seed"]) if f["title"] not in have]}
        sp.write_text(json.dumps(meta, indent=1, ensure_ascii=False))
    picked, lock = meta["files"], threading.Lock()
    progress.say(f"media-pilot {args.run}: {len(picked)} files, seed {meta['seed']}")

    probes, probe_errors = {}, {}

    def do_probe(f):
        try:
            probes[f["title"]] = media_probe.cached(f["title"]) or media_probe.probe(f["title"])
        except Exception as e:  # noqa: BLE001: a broken file is a pilot finding, not a stop
            probe_errors[f["title"]] = progress.short(e, 200)
            raise
    errors = parallel(do_probe, [{"id": f["title"], **f} for f in picked], args.jobs, "probe", "files")

    tri_p, q_p = d / "triage.jsonl", d / "questions.jsonl"
    done = {(r["title"], r["mode"]) for r in load_jsonl(tri_p)}
    tri_sys = prompt_text("triage", TRIAGE_MD)

    def do_triage(job):
        f, mode = job["f"], job["mode"]
        user = {"file": file_text(f)}
        if mode == "aided":
            user["aids"] = aids_text(probes[f["title"]])
        out = claude(tri_sys, json.dumps(user, ensure_ascii=False, indent=1), triage_schema(mode == "aided"),
                     args.triage_model, d, read=mode == "aided")
        append(tri_p, {"title": f["title"], "mode": mode, "seed": f["seed"], "class": f["class"], **out}, lock)
    jobs = [{"id": f"{mode} {f['title']}", "f": f, "mode": mode} for f in picked for mode in ("blind", "aided")
            if (f["title"], mode) not in done and (mode == "blind" or f["title"] in probes)]
    errors += parallel(do_triage, jobs, args.jobs, "triage", "calls")

    aided = {r["title"]: r for r in load_jsonl(tri_p) if r["mode"] == "aided"}
    designed = {r["title"] for r in load_jsonl(q_p)}
    des_sys = prompt("house-style", locale="en") + "\n\n" + prompt_text("design", DESIGN_MD)
    by_title = {f["title"]: f for f in picked}

    def do_design(job):
        f, t = job["f"], aided[job["f"]["title"]]
        user = {"file": file_text(f), "triage": {k: t[k] for k in ("subject", "category", "subcategory", "difficulty",
                                                                     "kind", "excerpt", "quality")},
                "aids": aids_text(probes[f["title"]])}
        out = claude(des_sys, json.dumps(user, ensure_ascii=False, indent=1), design_schema(), args.model, d, read=True)
        hit = heard_giveaway(out["answer"], probes[f["title"]])
        append(q_p, {"title": f["title"], "seed": f["seed"], "class": f["class"], "type": f["type"],
                     "page_url": f["page_url"], "licence": f["license"], "author": f["author"], "category": t["category"],
                     **out, "check": {"heard_or_seen": hit, "passed": out["giveaway"]["passes"] and not hit}}, lock)
    jobs = [{"id": t, "f": by_title[t]} for t, r in aided.items()
            if r["worth"] and t not in designed and t in probes]
    errors += parallel(do_design, jobs, args.jobs, "design", "questions")

    meta["wall_s"] = meta.get("wall_s", 0) + time.monotonic() - t0
    sp.write_text(json.dumps(meta, indent=1, ensure_ascii=False))
    write_report(d, meta, load_jsonl(tri_p), load_jsonl(q_p), probe_errors, calls(d))
    write_look(d, picked, probes, aided, {q["title"]: q for q in load_jsonl(q_p)})
    progress.say(f"media-pilot: {d / 'pilot.md'}, {d / 'look.html'}")
    return errors


def pct(a, b):
    return f"{a} ({a / b:.0%})" if b else "0"


def write_report(d, meta, tri, qs, probe_errors, usage):
    picked = meta["files"]
    blind = {r["title"]: r for r in tri if r["mode"] == "blind"}
    aided = {r["title"]: r for r in tri if r["mode"] == "aided"}
    qmap = {q["title"]: q for q in qs}
    L = [f"# Media-first pilot {d.name}", "",
         f"Sample: {len(picked)} of {meta['survey_files']} surveyed files, random seed {meta['seed']}, "
         f"class shares {SHARES}, round robin over each class's seeds.",
         "", "## Yield", "", "Files → probed → worth it (aided triage) → designed → passed the giveaway check "
         "(the model's own check and no answer word in the speech or OCR text).", ""]

    def rows(key):
        g = defaultdict(list)
        for f in picked:
            g[f[key]].append(f["title"])
        out = [f"| {key} | files | probed | worth | designed | passed |", "|---|---|---|---|---|---|"]
        for k, ts in sorted(g.items()) + [("**all**", [f["title"] for f in picked])]:
            n = len(ts)
            probed = sum(t not in probe_errors for t in ts)
            worth = sum(bool(aided.get(t, {}).get("worth")) for t in ts)
            des = sum(t in qmap for t in ts)
            ok = sum(qmap[t]["check"]["passed"] for t in ts if t in qmap)
            out.append(f"| {k} | {n} | {probed} | {pct(worth, n)} | {des} | {pct(ok, des)} |")
        return out
    L += rows("class") + [""] + rows("type") + [""] + rows("seed") + [""]

    both = [t for t in aided if t in blind]
    flips = Counter((blind[t]["worth"], aided[t]["worth"]) for t in both)
    gt = lambda rs: sum(in_categories(r["subject"], next(f for f in picked if f["title"] == r["title"])) for r in rs)
    L += ["## Aid ablation", "", f"Same {len(both)} files, triaged with title + description only (blind) and with "
          "every aid (aided). Ground truth: a word of the triage's `subject` in the file's Commons categories "
          "(the model never sees them); the developer's look follows.", "",
          "| | blind | aided |", "|---|---|---|",
          f"| worth it | {sum(blind[t]['worth'] for t in both)} | {sum(aided[t]['worth'] for t in both)} |",
          f"| subject matches Commons categories | {gt([blind[t] for t in both])} | {gt([aided[t] for t in both])} |",
          f"| content doesn't match title (aided says) | – | {sum(not aided[t]['matches_title'] for t in both)} |",
          f"| same category | {sum(blind[t]['category'] == aided[t]['category'] for t in both)} of {len(both)} | |",
          f"| same kind | {sum(blind[t]['kind'] == aided[t]['kind'] for t in both)} of {len(both)} | |", "",
          "Worth it, blind → aided: " + ", ".join(f"{'yes' if a else 'no'} → {'yes' if b else 'no'}: {n}"
                                                  for (a, b), n in sorted(flips.items())), "",
          "Per aid, what it changed (files; one aid may count several effects):", "",
          "| aid | " + " | ".join(EFFECTS) + " |", "|---" * (len(EFFECTS) + 1) + "|"]
    eff = Counter((e["aid"], e["effect"]) for r in aided.values() for e in {(x["aid"], x["effect"]): x
                                                                           for x in r.get("aid_effects", [])}.values())
    L += [f"| {a} | " + " | ".join(str(eff[a, e]) for e in EFFECTS) + " |" for a in AIDS]
    why = Counter((r.get("why_not") or "").split(":")[0][:60] for r in aided.values() if not r["worth"])
    L += ["", "Why not (aided, first words):", ""] + [f"- {n} × {w}" for w, n in why.most_common(25)]
    gw = Counter(k for q in qs for k in ("spoken", "on_screen_text", "title_needed", "description") if q["giveaway"][k])
    L += ["", "## Giveaways found", "", f"- model's check: {dict(gw)}",
          f"- answer word in speech or OCR, missed by the model: "
          f"{sum(bool(q['check']['heard_or_seen']) and q['giveaway']['passes'] for q in qs)}",
          f"- excerpts: {sum(bool(q['excerpt']) for q in qs)} of {len(qs)} designed questions"]
    if probe_errors:
        L += ["", "## Probe failures", ""] + [f"- {t}: {e}" for t, e in probe_errors.items()]
    usd = sum(c.get("usd") or 0 for c in usage)
    secs = sum(c.get("seconds") or 0 for c in usage)
    per_model = Counter()
    for c in usage:
        per_model[c["model"]] += c.get("usd") or 0
    n = len(qs) or 1
    L += ["", "## Cost", "", f"- {len(usage)} claude calls, ${usd:.2f} (" + ", ".join(f"{m} ${v:.2f}" for m, v in per_model.items())
          + f"), {progress.duration(secs)} in calls; wall time {progress.duration(meta['wall_s'])} (probes included, every run)",
          f"- per designed question: ${usd / n:.2f}, {secs / 60 / n:.1f} min in calls ({len(qs)} designed)", ""]
    (d / "pilot.md").write_text("\n".join(L), encoding="utf-8")


def rel(path, d):
    """Path relative to the run dir, via the main checkout's layout (work/ and media/ side by side)."""
    p = Path(path)
    if "media-probe" in p.parts:
        return "../../" + "/".join(p.parts[p.parts.index("media-probe"):])
    return "../../../media/" + p.name


def write_look(d, picked, probes, aided, qmap):
    e = html.escape
    cards = []
    for i, f in enumerate(picked, 1):
        p, t, q = probes.get(f["title"]), aided.get(f["title"]), qmap.get(f["title"])
        if not p:
            continue
        x = (q or {}).get("excerpt") or (t or {}).get("excerpt")
        frag = f"#t={x['start']},{x['end']}" if x else ""
        src = rel(p["file"], d) + frag
        tag = "video" if f["type"] == "video" else "audio"
        player = f'<{tag} controls preload="none" src="{e(src)}"></{tag}>'
        aids = "".join(f'<a href="{e(rel(Path(p["dir"]) / n, d))}" target="_blank">{n[:-4]}</a> '
                       for n in ("sheet.png", "spectrogram.png", "waveform.png") if (Path(p["dir"]) / n).exists())
        tri = (f"<p class=t>triage: {'worth' if t['worth'] else 'not worth'} · {e(t['subject'])} · {e(t['category'])}/"
               f"{e(t['subcategory'])} · d{t['difficulty']} · {e(t['kind'])} · {e(t['quality'])}"
               + (f" · why not: {e(t['why_not'])}" if t.get("why_not") else "") + "</p>") if t else ""
        if q:
            opts = "".join(f"<li{' class=a' if o == q['answer'] else ''}>{e(o)}</li>"
                           for o in sorted([q["answer"], *q["wrong_answers"]]))
            ok = "passed" if q["check"]["passed"] else "FAILED"
            body = (f"<p class=d>{e(q['description'])}</p><h3>{e(q['question'])}</h3><ol>{opts}</ol>"
                    f"<p>answer: <b>{e(q['answer'])}</b> · difficulty {q['difficulty']} · {e(q['subcategory'])}</p>"
                    f"<p>hints: {' / '.join(e(h) for h in q['hints'])}</p><p>fun fact: {e(q['fun_fact'])}</p>"
                    f"<p class=t>giveaway check {ok}: {e(q['giveaway']['notes'])}"
                    + (f" · answer words in speech/OCR: {e(', '.join(q['check']['heard_or_seen']))}" if q["check"]["heard_or_seen"] else "")
                    + "</p><p class=m>mark: approve / needs work / reject</p>")
        else:
            body = "<p class=t>no question designed</p>"
        cards.append(f'<section id="f{i}"><div class=l><b>#{i}</b> <a href="{e(f["page_url"])}" target="_blank">'
                     f'{e(f["title"])}</a><br><small>{e(f["class"])} · {e(f["seed"])} · {e(f["license"])} · '
                     f'{round(f["duration"] or 0)} s{" · excerpt " + str(x["start"]) + "–" + str(x["end"]) + " s" if x else ""}'
                     f'</small><br>{player}<br>{aids}</div><div class=r>{body}{tri}</div></section>')
    css = ("body{font:15px sans-serif;margin:1em;background:#111;color:#ddd}a{color:#8cf}section{display:flex;gap:1em;"
           "border-top:1px solid #444;padding:.8em 0}.l{flex:0 0 480px}.r{flex:1}video{max-width:480px}audio{width:460px}"
           ".a{color:#8f8;font-weight:bold}.t{color:#aaa;font-size:13px}.d{font-style:italic}.m{color:#fc6}")
    (d / "look.html").write_text(
        f"<!doctype html><meta charset=utf-8><title>media pilot {e(d.name)}</title><style>{css}</style>"
        f"<h1>Media-first pilot {e(d.name)}</h1><p>Open from the main checkout's work/media-pilot/{e(d.name)}/; "
        f"media from media/ (the cache). Per question: approve / needs work / reject, the why on rejects.</p>"
        + "".join(cards), encoding="utf-8")


def add_parser(sub):
    p = sub.add_parser("media-pilot", help="triage, design and aid ablation on sampled surveyed files → work/media-pilot/ (plan 201)")
    p.set_defaults(fn=cmd_media_pilot)
    p.add_argument("--files", type=int, default=100, help="sample size (default 100); larger on a rerun extends the sample")
    p.add_argument("--seed", type=int, default=201, help="random seed of the sample (default 201)")
    p.add_argument("--run", default="pilot-1", help="work/media-pilot/<run>/ (default pilot-1); rerun resumes")
    p.add_argument("--model", default="opus", help="design model (default opus)")
    p.add_argument("--triage-model", default="sonnet", help="triage model (default sonnet)")
    p.add_argument("--jobs", type=int, default=3, help="parallel probes and claude calls")
