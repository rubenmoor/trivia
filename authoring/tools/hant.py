"""zh-Hant by conversion (decision 762): `qgen batch --translate zh-Hant` turns each approved, current zh-Hans
translation into a zh-Hant one with OpenCC `s2twp`, after the exceptions list. Never ships (D-35).

A converted entry keeps the zh-Hans entry's source_hash (the English source stays the staleness test) and
`converted_from` = {locale, text, rules}: hashes of the zh-Hans text and of the exceptions list it was made
with. A changed zh-Hans text or exceptions list re-converts it; an unchanged one is left to the vocabulary pass."""
import datetime, hashlib, json, re, shutil, subprocess, sys

import layout  # paths (D-35)
import translations  # authoring/tools/translations.py: translated questions (D-81)

LOCALE, FROM = "zh-Hant", "zh-Hans"
BATCH = "conv-zh-Hant"  # a converted entry's batch (not a tr-* run)
CONFIG = "s2twp.json"  # OpenCC: Traditional characters, Taiwan phrases
EXCEPTIONS = layout.AUTHORING / "data" / "zh-hant-exceptions.json"
MARK = "%d"  # private-use placeholder around a protected term; OpenCC leaves it alone
BACK = re.compile("(\\d+)")


def exceptions():
    return json.loads(EXCEPTIONS.read_text(encoding="utf-8"))["terms"]


def rules_hash(terms):
    """12 hex of the exceptions list: a change re-converts every entry."""
    return hashlib.sha256(json.dumps(terms, ensure_ascii=False, sort_keys=True).encode()).hexdigest()[:12]


def opencc(strings):
    """The strings through `opencc -c s2twp` in one call (one per line, so none may hold a newline)."""
    if not shutil.which("opencc"):
        sys.exit("opencc not found: run in the dev shell (nix develop), it needs the opencc package")
    if any("\n" in s for s in strings):
        raise ValueError("a text with a newline")
    r = subprocess.run(["opencc", "-c", CONFIG], input="\n".join(strings) + "\n", capture_output=True,
                       text=True, encoding="utf-8", check=True)
    out = r.stdout.split("\n")[:-1]
    if len(out) != len(strings):
        raise RuntimeError(f"opencc returned {len(out)} lines for {len(strings)}")
    return out


def convert_all(strings, terms):
    """zh-Hant of each string: exception terms swapped for placeholders, converted, then put back."""
    if not strings:
        return []
    keys = sorted(terms, key=len, reverse=True)
    pat = re.compile("|".join(map(re.escape, keys))) if keys else None
    protected = [pat.sub(lambda m: MARK % keys.index(m.group()), s) for s in strings] if pat else strings
    return [BACK.sub(lambda m: terms[keys[int(m.group(1))]], s) for s in opencc(protected)]


def convert_entries(entries, terms):
    """New zh-Hant entries for the zh-Hans `entries`, one OpenCC call for all."""
    flat = []  # (entry index, field, position in a list or None, text)
    for i, h in enumerate(entries):
        for k in translations.TEXT_FIELDS:
            v = h.get(k)
            if isinstance(v, list):
                flat += [(i, k, j, s) for j, s in enumerate(v)]
            elif isinstance(v, str):
                flat.append((i, k, None, v))
    out = [{"id": h["id"], **{k: [] if isinstance(h.get(k), list) else h.get(k) for k in translations.TEXT_FIELDS}}
           for h in entries]
    for (i, k, j, _), s in zip(flat, convert_all([f[3] for f in flat], terms)):
        if j is None:
            out[i][k] = s
        else:
            out[i][k].append(s)
    rules = rules_hash(terms)
    for h, t in zip(entries, out):
        t.update(difficulty=h["difficulty"], status="approved", batch=BATCH, review=None,
                 source_hash=h["source_hash"],
                 converted_from={"locale": FROM, "text": translations.source_hash(h), "rules": rules},
                 converted_on=datetime.date.today().isoformat())
    return out


def current(t, h, rules):
    """The converted entry `t` is up to date with the zh-Hans entry `h` and the exceptions list (hash `rules`)."""
    cf = t.get("converted_from") or {}
    return (cf.get("locale") == FROM and cf.get("text") == translations.source_hash(h)
            and (cf.get("rules") == rules or bool(t.get("vocab")))  # a row the vocabulary pass read keeps its edits
            and t.get("source_hash") == h["source_hash"])


def plan(bundle, pool_questions, hans, hants, terms):
    """(zh-Hans entries to convert, converted zh-Hant entries to withdraw) for a bundle. Convert: the source is
    approved and translatable (not written in zh-Hans or zh-Hant), its zh-Hans entry approved and not stale, and
    the zh-Hant entry missing or not current (a rejected one stays). Withdraw: a converted, approved entry whose
    zh-Hans entry no longer qualifies."""
    rules, src = rules_hash(terms), {q["id"]: q for q in pool_questions}
    have = {t["id"]: t for t in hants}
    convert, ok = [], set()
    for h in hans:
        q = src.get(h["id"])
        if q is None or (q.get("bundle") or "base") != bundle or translations.source_locale(q) in (FROM, LOCALE):
            continue
        if (q["status"] == "approved" and translations.translatable(q) and h.get("status") == "approved"
                and not translations.is_stale(h, q)):
            ok.add(h["id"])
            t = have.get(h["id"])
            if t is None or (t.get("status") != "rejected" and not current(t, h, rules)):
                convert.append(h)
    withdraw = [t for t in hants if t.get("converted_from") and t.get("status") == "approved" and t["id"] not in ok
                and (src.get(t["id"], {}).get("bundle") or "base") == bundle]
    return convert, withdraw


def sync(bundle, pool_questions, terms=None, dry_run=False):
    """Convert and withdraw as `plan` says and save questions.zh-Hant.json (not with `dry_run`);
    returns (converted ids, withdrawn ids)."""
    terms = exceptions() if terms is None else terms
    with translations.locked(LOCALE):
        doc = translations.load(LOCALE)
        convert, withdraw = plan(bundle, pool_questions, translations.load(FROM)["questions"], doc["questions"], terms)
        if not dry_run and (convert or withdraw):
            new = {t["id"]: t for t in convert_entries(convert, terms)}
            for t in withdraw:
                t["status"], t["review"] = "needs_work", None  # zh-Hans no longer approved: out of the pool
            doc["questions"] = [new.pop(t["id"], t) for t in doc["questions"]] + list(new.values())
            translations.save(LOCALE, doc)
    return [h["id"] for h in convert], [t["id"] for t in withdraw]
