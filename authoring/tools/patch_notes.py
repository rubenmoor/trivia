"""`qgen patch-notes`: a content patch's notes from two shipped pools (plan 96, ST-5).

Counts only (added / fixed / dropped per locale and category), never question text, answers or ids.
A ref is a git rev; None = the working tree. A file missing at a ref = an empty pool for that locale.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

from layout import REPO as ROOT, WORK

sys.path.insert(0, str(ROOT / "authoring" / "steam"))
import release_check  # noqa: E402

FIXED_FIELDS = ["question", "answer", "wrong_answers", "hints", "fun_fact", "difficulty", "subcategory", "media"]
POOL_RE = re.compile(r"app/data/pool(?:\.([A-Za-z-]+))?\.json")
CATS_RE = re.compile(r"app/data/(?:bundles/[^/]+/)?categories\.json")
NAMES_RE = re.compile(r"app/data/(?:bundles/[^/]+/)?names\.([A-Za-z-]+)\.json")
LAUNCH = ["es", "en", "de"]  # D-78
OTHER = "other"
# Steam event strings per launch language (authoring, not t()); tone of plans/11-steam.md "Announcement texts".
EVENT = {
    "es": {"lang": "Spanish (es-419 and es-ES)", "title": "Actualización v{v}", "new": ": {n} preguntas nuevas",
           "new1": ": 1 pregunta nueva", "list": "Preguntas nuevas:",
           "fixed": "Corregimos {n} preguntas (gracias por sus reportes).",
           "fixed1": "Corregimos 1 pregunta (gracias por sus reportes).",
           "removed": "Quitamos {n} preguntas.", "removed1": "Quitamos 1 pregunta.", "other": "Otras"},
    "en": {"lang": "English", "title": "Update v{v}", "new": ": {n} new questions", "new1": ": 1 new question",
           "list": "New questions:", "fixed": "Fixed {n} questions (thanks for your reports).",
           "fixed1": "Fixed 1 question (thanks for your reports).",
           "removed": "Removed {n} questions.", "removed1": "Removed 1 question.", "other": "Other"},
    "de": {"lang": "German", "title": "Update v{v}", "new": ": {n} neue Fragen", "new1": ": 1 neue Frage",
           "list": "Neue Fragen:", "fixed": "{n} Fragen korrigiert (danke für eure Meldungen).",
           "fixed1": "1 Frage korrigiert (danke für eure Meldungen).",
           "removed": "{n} Fragen entfernt.", "removed1": "1 Frage entfernt.", "other": "Sonstige"},
}
CHANGES = "<Changes: fill in>"


def git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")


def files(ref):
    """Paths under app/data/ at ref."""
    if ref is None:
        return [p.relative_to(ROOT).as_posix() for p in (ROOT / "app" / "data").rglob("*.json")]
    return git("ls-tree", "-r", "--name-only", ref, "app/data/").stdout.split()


def read(ref, path):
    """Parsed JSON of path at ref, None if missing."""
    if ref is None:
        p = ROOT / path
        return json.loads(p.read_text(encoding="utf-8")) if p.exists() else None
    r = git("show", f"{ref}:{path}")
    return json.loads(r.stdout) if r.returncode == 0 else None


def snapshot(ref):
    """{"version", "pools": {locale: pool}, "sub": {subcategory: slug}, "names": {locale: {slug: name}}}."""
    fs = files(ref)
    pools = {(m.group(1) or "es"): read(ref, f) for f in fs if (m := POOL_RE.fullmatch(f))}
    sub, names = {}, {"es": {}}
    for f in sorted(f for f in fs if CATS_RE.fullmatch(f)):
        for c in read(ref, f)["categories"]:
            names["es"][c["slug"]] = c["name"]
            sub.update({s: c["slug"] for s in c["subcategories"]})
    for f in sorted(fs):
        if m := NAMES_RE.fullmatch(f):
            names.setdefault(m.group(1), {}).update(read(ref, f).get("categories") or {})
    pkg = read(ref, "app/desktop/package.json")
    return {"version": pkg and pkg["version"], "pools": pools, "sub": sub, "names": names}


def diff(old, new, old_sub, new_sub):
    """{slug: {"added", "fixed", "dropped"}} for one locale's pools (None = empty)."""
    o = {q["id"]: q for q in (old or {}).get("questions", [])}
    n = {q["id"]: q for q in (new or {}).get("questions", [])}
    out = {}
    def count(key, slug):
        out.setdefault(slug, {"added": 0, "fixed": 0, "dropped": 0})[key] += 1
    for i, q in n.items():
        if i not in o:
            count("added", new_sub.get(q["subcategory"], OTHER))
        elif any(q.get(f) != o[i].get(f) for f in FIXED_FIELDS):
            count("fixed", new_sub.get(q["subcategory"], OTHER))
    for i, q in o.items():
        if i not in n:
            count("dropped", old_sub.get(q["subcategory"]) or new_sub.get(q["subcategory"], OTHER))
    return out


def order(locale):
    """Launch languages first (es, en, de), then the rest."""
    return (LAUNCH.index(locale) if locale in LAUNCH else len(LAUNCH), locale)


def tag_of(ref):
    return ref if ref and git("tag", "--list", ref).stdout.strip() == ref else None


def notes(frm, to):
    """The patch notes as a dict (the --json output)."""
    a, b = snapshot(frm), snapshot(to)
    locales = sorted(set(a["pools"]) | set(b["pools"]), key=order)
    counts = {l: diff(a["pools"].get(l), b["pools"].get(l), a["sub"], b["sub"]) for l in locales}
    counts = {l: c for l, c in counts.items() if c}
    sv = {"from": release_check.save_version(frm), "to": release_check.save_version(to)}
    sv["changed"] = sv["from"] != sv["to"]
    hashes = lambda s: {l: (s["pools"][l] or {}).get("hash") for l in sorted(s["pools"], key=order)}
    names = {l: {**a["names"].get(l, {}), **b["names"].get(l, {})} for l in set(a["names"]) | set(b["names"])}
    return {"from": {"ref": frm, "version": a["version"], "pool_hash": hashes(a)},
            "to": {"ref": to or "working tree", "version": b["version"], "pool_hash": hashes(b)},
            "kind": release_check.kind(frm, to), "save_version": sv, "counts": counts,
            "category_names": names}


def total(c, key):
    return sum(v[key] for v in c.values())


def event(locale, d):
    """(title, BBCode body) of the Steam event in a launch language."""
    s, c, v = EVENT[locale], d["counts"].get(locale, {}), d["to"]["version"]
    names = d["category_names"].get(locale) or d["category_names"].get("es", {})
    added, fixed, dropped = total(c, "added"), total(c, "fixed"), total(c, "dropped")
    title = s["title"].format(v=v) + (s["new1"] if added == 1 else s["new"].format(n=added) if added else "")
    body = []
    if added:
        body += [s["list"], "[list]"]
        body += [f"[*]{names.get(slug) or s['other']}: {x['added']}" for slug, x in
                 sorted(c.items(), key=lambda kv: -kv[1]["added"]) if x["added"]]
        body += ["[/list]"]
    if fixed:
        body.append(s["fixed1"] if fixed == 1 else s["fixed"].format(n=fixed))
    if dropped:
        body.append(s["removed1"] if dropped == 1 else s["removed"].format(n=dropped))
    if d["kind"] == "full":
        body += ["", CHANGES]
    return title, "\n".join(body)


def markdown(d):
    f, t, sv = d["from"], d["to"], d["save_version"]
    hashes = lambda x: ", ".join(f"{l} {h}" for l, h in x["pool_hash"].items()) or "no pool"
    kind = (f"content-only patch since {f['ref']}" if d["kind"] == "content-only"
            else f"full: code changed since {f['ref']}; the events need a hand-written \"Changes\" ({CHANGES})")
    save = (f"changed ({sv['from']} → {sv['to']}): minor version + plan 92's `beta-save` row" if sv["changed"]
            else f"unchanged ({sv['to']})")
    md = [f"# Patch notes v{t['version']}", "",
          f"- From: {f['ref']} (version {f['version']}; pool {hashes(f)})",
          f"- To: {t['ref']} (version {t['version']}; pool {hashes(t)})",
          f"- Kind: {kind}", f"- Save version: {save}",
          "- Counts only: no question text, answers or ids (plan 96)", ""]
    if not d["counts"]:
        return "\n".join(md + ["No content changes.", ""])
    md += ["## Counts", "", "| locale | category | added | fixed | dropped |", "|---|---|---:|---:|---:|"]
    es = d["category_names"].get("es", {})
    for l, c in d["counts"].items():
        md += [f"| {l} | {es.get(slug, slug)} | {x['added']} | {x['fixed']} | {x['dropped']} |"
               for slug, x in sorted(c.items(), key=lambda kv: es.get(kv[0], kv[0]))]
        md.append(f"| {l} | **total** | {total(c, 'added')} | {total(c, 'fixed')} | {total(c, 'dropped')} |")
    all_ = lambda k: sum(total(c, k) for c in d["counts"].values())
    md += [f"| **all** | | {all_('added')} | {all_('fixed')} | {all_('dropped')} |", "",
           "## Steam event drafts", "",
           "Posted by the gamemaster (Community → Events & Announcements), one text per Steam language.", ""]
    for l in LAUNCH:
        if l not in d["counts"]:
            md += [f"### {EVENT[l]['lang']}", "", "No content changes in this language.", ""]
            continue
        title, body = event(l, d)
        md += [f"### {EVENT[l]['lang']}", "", f"- Title: `{title}`", "- Body:", "```", body, "```", ""]
    return "\n".join(md)


def cmd_patch_notes(args):
    frm = args.from_ref or release_check.previous_tag(own=True)
    if not frm:
        sys.exit("qgen patch-notes: no v* tag; give <from-ref>")
    for ref in [frm, args.to_ref]:
        if ref and git("rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}").returncode:
            sys.exit(f"qgen patch-notes: unknown ref {ref}")
    d = notes(frm, args.to_ref)
    md = markdown(d)
    print(json.dumps(d, ensure_ascii=False, indent=1) if args.json else md)
    out = args.out or (tag_of(args.to_ref) and WORK / "steam" / args.to_ref / "patch-notes.md")
    if out:
        Path(out).parent.mkdir(parents=True, exist_ok=True)
        Path(out).write_text(md, encoding="utf-8")
        print(f"→ {out}", file=sys.stderr)
    if d["from"]["version"] == d["to"]["version"]:
        print(f"warning: version {d['to']['version']} unchanged since {frm}: bump app/desktop/package.json",
              file=sys.stderr)
    if d["kind"] == "full" and d["counts"]:
        print(f"warning: kind full (code changed since {frm}): replace {CHANGES} in every event by hand",
              file=sys.stderr)
