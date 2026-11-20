"""`qgen spotcheck export|import`: the offline spot-check sheet for outside native reviewers (decision 221, plan 141).

One self-contained, blind HTML file per job; the reviewer's verdict file comes back by e-mail and the developer
imports it (in ../trivia-review): human reviews of the translations, spot checks, scored controls. Never ships (D-35)."""
import base64, datetime, hashlib, html, json, random, re, subprocess, sys

import layout  # authoring/tools/layout.py
from layout import REPO as ROOT, WORK
import atomic  # authoring/tools/atomic.py
import audit  # authoring/tools/audit.py
import media_cache  # authoring/tools/media_cache.py
import reviews  # authoring/tools/reviews.py
import translations  # authoring/tools/translations.py

from qgen import PROBLEMS, load_json  # authoring/tools/qgen.py

BRIEF = layout.AUTHORING / "NATIVE-REVIEW.md"
ZH_LOCALES = ("zh-Hans", "zh-Hant")  # the locales with controls by default; one place
RELEASE_BUNDLE = "chinese-base"
RELEASE_SIZE = 30
DEFAULT_CONTROLS = 3
DECISIONS = {"approve": "approved", "needs_work": "needs_work", "reject": "rejected", "no_travel": "rejected"}
NO_TRAVEL = "no viaja"
CONTROLS_FILE = layout.AUTHORING / "data" / "spot-controls.json"  # scored controls per sheet (tracked)
FIELDS = ["question", "answer", "wrong_answers", "hints", "description", "fun_fact"]
THUMB = "480x360"  # inline image size (magick -thumbnail)


def sheet_hash(name, ids):
    return hashlib.sha256(json.dumps([name, sorted(ids)], ensure_ascii=False).encode()).hexdigest()[:12]


def sheet_files(name, run=None):
    """(sheet, manifest, controls file) of a sheet; the controls file lists every sheet's planted controls in its folder."""
    d = WORK / (run or "spotcheck")
    return d / f"{name}.html", d / f"{name}.manifest.json", d / "spotcheck-controls.json"


# --- controls -------------------------------------------------------------------

def garble(text, rng):
    """Shuffle the letters inside each word of ≥ 4 letters (a garbled option)."""
    def word(m):
        w = list(m[0])
        for _ in range(5):
            rng.shuffle(w)
            if "".join(w) != m[0]:
                break
        return "".join(w)
    out = re.sub(r"\w{4,}", word, text)
    return out if out != text else text[::-1]


def make_control(item, rng):
    """A faulty copy of an item (a dict as `item_of` builds): wrong right answer, changed number or garbled
    option; (control item without id, kind)."""
    tr = json.loads(json.dumps(item["tr"]))
    number = re.compile(r"\d+")
    kinds = ["wrong_answer", "garbled"]
    if number.search(tr["question"]) or number.search(tr["answer"]):
        kinds.append("number")
    kind = rng.choice(kinds)
    if kind == "wrong_answer":
        k = rng.randrange(len(tr["wrong_answers"]))
        tr["answer"], tr["wrong_answers"][k] = tr["wrong_answers"][k], tr["answer"]
    elif kind == "number":
        field = "question" if number.search(tr["question"]) else "answer"
        tr[field] = number.sub(lambda m: str(int(m[0]) + rng.choice([1, 2, 10, -1]) if int(m[0]) > 1 else int(m[0]) + 7),
                               tr[field], count=1)
    else:
        k = rng.randrange(len(tr["wrong_answers"]))
        tr["wrong_answers"][k] = garble(tr["wrong_answers"][k], rng)
    return {**item, "tr": tr}, kind


# --- the sheet --------------------------------------------------------------------

def english_of(src):
    """The source's text fields if it is written in English, else None."""
    return {k: src.get(k) for k in FIELDS} if translations.source_locale(src) == "en" else None


def media_of(src):
    m = src.get("media") or {}
    if not m.get("type"):
        return None
    out = {"type": m["type"], "name": m.get("query") or m.get("source_url") or ""}
    if m["type"] == "image" and m.get("file_url"):
        p = media_cache.cache_path(m["file_url"])
        if p.is_file() and (jpg := thumbnail(p)):
            out["img"] = "data:image/jpeg;base64," + base64.b64encode(jpg).decode()
    return out


def thumbnail(path):
    """A small JPEG of a cached image (first frame), or None if magick fails or is missing (dev shell)."""
    try:
        r = subprocess.run(["magick", f"{path}[0]", "-auto-orient", "-thumbnail", f"{THUMB}>", "-background", "white",
                            "-flatten", "-strip", "-quality", "70", "jpg:-"], capture_output=True)
    except FileNotFoundError:
        return None
    return r.stdout if r.returncode == 0 and r.stdout else None


def item_of(t, src):
    return {"id": t["id"], "subcategory": src.get("subcategory"), "difficulty": t["difficulty"],
            "en": english_of(src), "tr": {k: t.get(k) for k in FIELDS}, "media": media_of(src)}


def pick(locale, mode, arg=None, size=None):
    """([(translation, source)], skipped) for a job. mode: run (arg = the run name), release, subcategory (arg = keys)."""
    pool = {q["id"]: q for q in reviews.load_pool()["questions"]}
    by_id = {t["id"]: t for t in translations.load(locale)["questions"]}
    if mode == "run":
        ids = [i for i in audit.audit_sample(arg, size or audit.spot_check_size(arg)) if i in by_id]
        picked = [(by_id[i], pool[i]) for i in ids if i in pool]
    else:
        ok = [(by_id[i], q) for i, q in pool.items()
              if i in by_id and q.get("bundle") == RELEASE_BUNDLE and by_id[i].get("status") == "approved"
              and translations.plays(by_id[i], q)]
        if mode == "subcategory":
            picked = [(t, q) for t, q in ok if q.get("subcategory") in arg]
        else:  # sampled among English sources: a full 30
            picked = sorted(ok, key=lambda x: x[0]["id"])
            skipped = [t["id"] for t, q in picked if not english_of(q)]
            picked = [(t, q) for t, q in picked if english_of(q)]
            random.Random(f"release-{locale}").shuffle(picked)
            return picked[:size or RELEASE_SIZE], skipped
    keep = [(t, q) for t, q in picked if english_of(q)]
    return keep, [t["id"] for t, q in picked if not english_of(q)]


def build_items(name, picked, controls):
    """Items shuffled with `controls` planted copies mixed in; (items, {control id: info})."""
    rng = random.Random(name)
    items = [item_of(t, q) for t, q in picked]
    rng.shuffle(items)
    planted = {}
    for k, base in enumerate(rng.sample(items, min(controls, len(items))), 1):
        c, kind = make_control(base, rng)
        c["id"] = f"control-{k}"
        planted[c["id"]] = {"of": base["id"], "kind": kind}
        items.insert(rng.randrange(len(items) + 1), c)
    return items, planted


def md_to_html(text):
    """The brief's «For the volunteer» section: headings, nested bullets, `code`."""
    text = text.split("## For the developer")[0].replace("## For the volunteer", "", 1)
    out, depth = [], 0
    inline = lambda s: re.sub(r"`([^`]+)`", r"<code>\1</code>", html.escape(s))
    for line in text.splitlines():
        m = re.match(r"^( *)- (.*)", line)
        if m:
            d = len(m[1]) // 2 + 1
            while depth < d:
                out.append("<ul>"); depth += 1
            while depth > d:
                out.append("</ul>"); depth -= 1
            out.append(f"<li>{inline(m[2])}</li>")
            continue
        while depth:
            out.append("</ul>"); depth -= 1
        if line.startswith("### "):
            out.append(f"<h3>{inline(line[4:])}</h3>")
        elif line.startswith("# "):
            out.append(f"<h1>{inline(line[2:])}</h1>")
        elif line.strip():
            out.append(f"<p>{inline(line)}</p>")
    out.append("</ul>" * depth)
    return "\n".join(out)


PAGE = """<!doctype html><html><head><meta charset="utf-8"><title>__TITLE__</title><style>
body{font:16px/1.45 system-ui,sans-serif;max-width:60rem;margin:1rem auto;padding:0 1rem;color:#222}
.card{border:1px solid #bbb;border-radius:8px;padding:.8rem 1rem;margin:1rem 0}.card.done{border-color:#4a4;background:#f4fbf4}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:1rem}.col h4{margin:.2rem 0}.ok{font-weight:bold;color:#161}
.meta{color:#666;font-size:.85em}textarea{width:100%;box-sizing:border-box}label{margin-right:.8rem;white-space:nowrap}
button{font:inherit;padding:.4rem 1rem}.bar{position:sticky;top:0;background:#fff;padding:.4rem 0;border-bottom:1px solid #ccc}
img{max-width:20rem;max-height:12rem}code{background:#eee;padding:0 .2em}</style></head><body>
<div class="bar"><b id="prog"></b> <button id="dl">Download verdicts</button></div>
<details open><summary><b>Brief</b></summary>__BRIEF__</details><div id="items"></div>
<h3>General comments</h3><textarea id="comments" rows="6"></textarea>
<p><button id="dl2">Download verdicts</button></p>
<script id="data" type="application/json">__DATA__</script>
<script>
const D=JSON.parse(document.getElementById('data').textContent),KEY='spotcheck-'+D.name+'-'+D.hash;
let S=JSON.parse(localStorage.getItem(KEY)||'{"v":{},"c":""}');
const save=()=>localStorage.setItem(KEY,JSON.stringify(S));
const esc=s=>String(s??'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const DEC=[['approve','Approve'],['needs_work','Needs work'],['reject','Reject'],['no_travel',"Doesn't travel"]];
function block(t,o,title){let w=[t.answer,...t.wrong_answers];
 return `<div class="col"><h4>${title}</h4><p><b>${esc(t.question)}</b></p><ul>`+
 o.map((a,i)=>`<li class="${i==0?'ok':''}">${esc(a)}${i==0?' ✔':''}</li>`).join('')+`</ul>`+
 (t.hints.length?`<p class="meta">Hints:</p><ol>${t.hints.map(h=>`<li>${esc(h)}</li>`).join('')}</ol>`:'')+
 (t.description?`<p class="meta">${esc(t.description)}</p>`:'')+(t.fun_fact?`<p class="meta">${esc(t.fun_fact)}</p>`:'')+`</div>`}
function render(){const root=document.getElementById('items');root.innerHTML='';
 D.items.forEach((it,n)=>{const v=S.v[it.id]||{},c=document.createElement('div');c.className='card'+(v.decision?' done':'');
  c.innerHTML=`<div class="meta">#${n+1} · ${esc(it.subcategory||'')} · difficulty ${it.difficulty}/15`+
  (it.media?` · ${esc(it.media.type)}: ${esc(it.media.name)}`:'')+`</div>`+(it.media&&it.media.img?`<img src="${it.media.img}">`:'')+
  `<div class="cols">${block(it.en,[it.en.answer,...it.en.wrong_answers],'English (source)')}${block(it.tr,[it.tr.answer,...it.tr.wrong_answers],D.locale)}</div>`+
  `<p>${DEC.map(([k,l])=>`<label><input type="radio" name="d${n}" value="${k}"${v.decision==k?' checked':''}> ${l}</label>`).join('')}</p>`+
  `<p>${D.problems.map(p=>`<label><input type="checkbox" value="${p}"${(v.problems||[]).includes(p)?' checked':''}> ${p}</label>`).join('')}</p>`+
  `<textarea rows="2" placeholder="Feedback (English)" class="fb">${esc(v.feedback)}</textarea>`+
  `<textarea rows="2" placeholder="Corrected text (optional, in the target language)" class="fx">${esc(v.corrected)}</textarea>`;
  const upd=()=>{S.v[it.id]={decision:(c.querySelector('input[type=radio]:checked')||{}).value,
   problems:[...c.querySelectorAll('input[type=checkbox]:checked')].map(x=>x.value),
   feedback:c.querySelector('.fb').value,corrected:c.querySelector('.fx').value};save();
   c.className='card'+(S.v[it.id].decision?' done':'');prog()};
  c.addEventListener('input',upd);root.appendChild(c)});prog()}
function prog(){const n=D.items.filter(i=>(S.v[i.id]||{}).decision).length;document.getElementById('prog').textContent=n+' / '+D.items.length+' decided'}
const cm=document.getElementById('comments');cm.value=S.c||'';cm.oninput=()=>{S.c=cm.value;save()};
function dl(){const verdicts={};for(const i of D.items){const v=S.v[i.id];if(v&&v.decision)verdicts[i.id]=v}
 const b=new Blob([JSON.stringify({sheet:D.name,hash:D.hash,locale:D.locale,ids:D.items.map(i=>i.id),verdicts,comments:S.c||''},null,1)],{type:'application/json'});
 const a=document.createElement('a');a.href=URL.createObjectURL(b);a.download=D.name+'.verdicts.json';a.click()}
document.getElementById('dl').onclick=document.getElementById('dl2').onclick=dl;render();
</script></body></html>"""


def write_sheet(name, locale, items, planted, run=None):
    ids = [i["id"] for i in items]
    h = sheet_hash(name, ids)
    data = {"name": name, "hash": h, "locale": locale, "problems": PROBLEMS, "items": items}
    blob = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    page = (PAGE.replace("__TITLE__", html.escape(name)).replace("__BRIEF__", md_to_html(BRIEF.read_text(encoding="utf-8")))
            .replace("__DATA__", blob))
    page_path, manifest_path, controls_path = sheet_files(name, run)
    page_path.parent.mkdir(parents=True, exist_ok=True)
    atomic.write_text(page_path, page)
    atomic.write_json(manifest_path, {"name": name, "hash": h, "locale": locale, "run": run, "ids": ids})
    with atomic.locked(controls_path):
        data = load_json(controls_path, {}) or {}
        data[name] = {"hash": h, "controls": planted}
        atomic.write_json(controls_path, data)
    return page_path, manifest_path, controls_path


def cmd_export(args):
    locale = args.locale
    if args.release:
        locale, mode, arg, name, run = args.release, "release", None, f"release-{args.release}", None
    elif args.subcategory:
        if not locale:
            sys.exit("--subcategory needs --locale")
        mode, arg, run = "subcategory", set(args.subcategory), None
        name = f"{'+'.join(sorted(arg))}-{locale}"
    elif args.run:
        run = args.run
        locale = translations.run_locale(run)
        if not locale:
            sys.exit(f"{run} is no translation run (tr-<locale>-<n>)")
        mode, arg, name = "run", run, f"spotcheck-{run}"
    else:
        sys.exit("give a run, --release <locale> or --subcategory <key>… --locale <locale>")
    if locale not in translations.LOCALES:
        sys.exit(f"unknown locale {locale}")
    picked, skipped = pick(locale, mode, arg, args.size)
    if skipped:
        print(f"skipped, source not in English ({len(skipped)}): {', '.join(skipped)}")
    if not picked:
        sys.exit("nothing to check: every picked source is not in English" if skipped
                 else "nothing to check: no approved translations match")
    controls = args.controls if args.controls is not None else DEFAULT_CONTROLS if locale in ZH_LOCALES else 0
    items, planted = build_items(name, picked, controls)
    page, manifest, controls_path = write_sheet(name, locale, items, planted, run)
    rel = lambda p: p.relative_to(ROOT) if p.is_relative_to(ROOT) else p
    print(f"sheet: {rel(page)} ({len(picked)} questions, {len(planted)} controls,"
          f" {sum(bool((i['media'] or {}).get('img')) for i in items)} images inline)")
    print(f"manifest: {rel(manifest)}; controls: {rel(controls_path)}")
    print(f"raise: pm decision add \"Spot check {name} done?\" (body: the sheet path, `qgen spotcheck import <name>.verdicts.json` in ../trivia-review)")


# --- import -----------------------------------------------------------------------

def check_verdicts(doc, manifest, known):
    """Problems of a verdict file: `manifest` (or None) the export's record, `known` the translation ids of the locale."""
    errors = []
    for k in ("sheet", "hash", "locale", "ids", "verdicts"):
        if k not in doc:
            return [f"no {k!r} in the file"]
    if doc["locale"] not in translations.LOCALES:
        errors.append(f"unknown locale {doc['locale']}")
    if doc["hash"] != sheet_hash(doc["sheet"], doc["ids"]):
        errors.append("wrong sheet hash: the file was changed or is from another sheet")
    if manifest:
        if manifest["hash"] != doc["hash"] or manifest["name"] != doc["sheet"]:
            errors.append(f"not the exported sheet {manifest['name']} ({manifest['hash']})")
        if set(doc["ids"]) != set(manifest["ids"]):
            errors.append("ids differ from the export's")
    for i, v in doc["verdicts"].items():
        if i not in doc["ids"]:
            errors.append(f"{i}: not on the sheet")
        elif not i.startswith("control-") and i not in known:
            errors.append(f"{i}: unknown translation in {doc['locale']}")
        if v.get("decision") not in DECISIONS:
            errors.append(f"{i}: unknown decision {v.get('decision')!r}")
        if bad := [p for p in v.get("problems") or [] if p not in PROBLEMS]:
            errors.append(f"{i}: unknown problem kinds {bad}")
    return errors


def score_controls(ids, verdicts):
    """(caught, n) over the sheet's planted controls: caught = any verdict but approve; undecided = not caught."""
    ctl = [i for i in ids if i.startswith("control-")]
    return sum((verdicts.get(i) or {}).get("decision") not in (None, "approve") for i in ctl), len(ctl)


def review_of(v):
    """The review dict of a verdict: corrected text goes into the feedback, never over the translation."""
    d = v["decision"]
    parts = [(v.get("feedback") or "").strip()]
    if (c := (v.get("corrected") or "").strip()):
        parts.append(f"Native correction: {c}")
    feedback = " ".join(p for p in parts if p)
    if d == "no_travel":
        feedback = f"{NO_TRAVEL}: {feedback}" if feedback else NO_TRAVEL
    elif d == "needs_work" and not feedback:
        feedback = "Native check: no comment given."
    r = {"decision": DECISIONS[d], "feedback": feedback or None, "by": "native"}
    if v.get("problems"):
        r["problems"] = v["problems"]
    return r


def cmd_import(args):
    sys.path.insert(0, str(layout.AUTHORING / "server"))  # here, not above: report.py imports this module
    import spot_checks  # authoring/server/spot_checks.py
    path = args.file
    doc = json.loads(open(path, encoding="utf-8").read())
    locale = doc.get("locale")
    known = {t["id"]: t for t in translations.load(locale)["questions"]} if locale in translations.LOCALES else {}
    manifest = None
    for run in (None, *(d.name for d in WORK.glob("tr-*"))):
        m = load_json(sheet_files(doc.get("sheet", ""), run)[1]) if doc.get("sheet") else None
        if m:
            manifest = m
            break
    errors = check_verdicts(doc, manifest, known)
    if errors:
        sys.exit("verdict file refused:\n  " + "\n  ".join(errors))
    caught, n = score_controls(doc["ids"], doc["verdicts"])
    real = {i: v for i, v in doc["verdicts"].items() if not i.startswith("control-")}
    print(f"{doc['sheet']}: {len(real)} verdicts of {len([i for i in doc['ids'] if not i.startswith('control-')])} questions"
          f"{'' if manifest else ' (no export record here: ids checked against the locale only)'}")
    print(f"controls caught {caught}/{n}")
    planted = ((load_json(sheet_files(doc["sheet"], (manifest or {}).get("run"))[2], {}) or {}).get(doc["sheet"]) or {}).get("controls") or {}
    for i in (i for i in doc["ids"] if i.startswith("control-") and (doc["verdicts"].get(i) or {}).get("decision") in (None, "approve")):
        print(f"  missed {i}" + (f": {planted[i]['kind']} of {planted[i]['of']}" if i in planted else ""))
    for i, v in real.items():
        rv = review_of(v)
        if args.dry_run:
            print(f"  {i}: {rv['decision']}{' (' + ', '.join(rv.get('problems', [])) + ')' if rv.get('problems') else ''}")
            continue
        update = reviews.update_translation(locale)
        reviews.set_review(i, rv, update)
        t = next(t for t in translations.load(locale)["questions"] if t["id"] == i)
        try:
            spot_checks.record(t["batch"], t, False)
        except (ValueError, KeyError) as e:
            print(f"  {i}: reviewed, no spot-check record ({e})")
    if doc.get("comments"):
        print("general comments:\n" + doc["comments"])
    if args.dry_run:
        return print("dry run: nothing written")
    if n:
        with atomic.locked(CONTROLS_FILE):
            data = load_json(CONTROLS_FILE, {}) or {}
            data[doc["sheet"]] = {"run": (manifest or {}).get("run"), "locale": doc["locale"], "caught": caught, "n": n,
                                  "on": datetime.date.today().isoformat()}
            atomic.write_json(CONTROLS_FILE, data)


def controls_section():
    """`qgen report --qc`: controls caught per imported native sheet (run, release and subcategory sheets); [] if none."""
    data = load_json(CONTROLS_FILE, {}) or {}
    if not data:
        return []
    return ["", "Native sheets, planted controls (plan 141):", "", "| sheet | run | locale | controls caught | imported |",
            "|---|---|---|---:|---|",
            *[f"| {k} | {r.get('run') or '–'} | {r.get('locale') or '–'} | {r['caught']}/{r['n']} | {r.get('on', '–')} |"
              for k, r in sorted(data.items())]]


def add_parser(sub):
    sp = sub.add_parser("spotcheck", help="offline spot-check sheet for outside native reviewers (decision 221, plan 141)"
                        ).add_subparsers(dest="action", required=True)
    ex = sp.add_parser("export", help="work/<run>/spotcheck-<run>.html, or work/spotcheck/<name>.html")
    ex.set_defaults(fn=cmd_export, run=None)
    ex.add_argument("run", nargs="?", help="a translation run, tr-<locale>-<n>")
    ex.add_argument("--controls", type=int, help=f"planted faulty copies (default {DEFAULT_CONTROLS} for zh, else 0)")
    ex.add_argument("--release", metavar="LOCALE", help=f"seeded sample of {RELEASE_SIZE} approved {RELEASE_BUNDLE} translations")
    ex.add_argument("--subcategory", nargs="+", metavar="KEY", help=f"all approved {RELEASE_BUNDLE} translations of these subcategories")
    ex.add_argument("--locale", help="with --subcategory")
    ex.add_argument("--size", type=int, help="items of a run sheet or the release sample")
    im = sp.add_parser("import", help="a returned <sheet>.verdicts.json → human reviews and spot checks")
    im.set_defaults(fn=cmd_import, run=None)
    im.add_argument("file")
    im.add_argument("--dry-run", action="store_true", help="check and print, write nothing")
