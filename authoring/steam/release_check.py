#!/usr/bin/env python3
"""Release check before every Steam upload (SW-6, pm decision 14; plan 89).

    trivia-release-check [--skip STEP]... [--manual FILE]

Steps, each ✓/✗ with its time; all automated steps run, exit 1 on any ✗:
  tag       clean tree, HEAD tagged v<version> (app/desktop/package.json, pm decision 91); never tags
  checks    npm run check, npm test, npm run build, qgen validate
  licenses  trivia-media licenses --status approved (exit 1 = files to replace)
  quality   qgen report --qc: release bar ✓ for the last two batches (pm decision 15)
  nix       nix build .#app (D-59)
  desktop   trivia-desktop-build --dir (stage-media's missing-file check) + trivia-steam stage
  credits   node authoring/steam/credits_check.mjs on both unpacked builds: files ↔ credits.json, both ways
  smoke     node authoring/steam/smoke.mjs app/desktop/release/linux-unpacked
  media-budget  always skipped until masterplan 10 part 6 (task 260) adds its check
  manual    the rows of MANUAL, asked y/n/note or read from --manual FILE (`<row>: <answer>` per line);
            "n…" fails, "y…" passes, anything else is a note and counts as skipped; on a content-only
            patch full-only rows are answered "skipped: content-only since <tag>"; beta-save only when
            SAVE_VERSION changed (plans/11-steam.md "Release checklist (ST-4)")

Report header: version, pool hash, previous tag (newest v* reachable from HEAD, not HEAD's own), kind
(`full`, or `content-only` when nothing shipped but app/data/ changed since it) and SAVE_VERSION change.
`--skip STEP` (repeatable): a known-broken step, ✗ → "skipped" in the report (and the build Desc).
Run from the dev shell (nix, steam-run, Xvfb). Report: work/steam/<tag-or-sha>/release-check.md,
release-check.json for `trivia-steam upload --checked` (commit, clean, ok, skipped), logs/<step>.log.
"""
import argparse, json, re, subprocess, sys, time
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from steam import REPO, git, head_tag, version  # noqa: E402

UNPACKED = "app/desktop/release/linux-unpacked"
UNPACKED_WIN = "app/desktop/release/win-unpacked"
STEPS = {
    "checks": [["npm", "run", "check"], ["npm", "test"], ["npm", "run", "build"], ["qgen", "validate"]],
    "licenses": [["trivia-media", "licenses", "--status", "approved"]],
    "quality": [["qgen", "report", "--qc"]],
    "nix": [["nix", "build", ".#app", "--no-link"]],
    "desktop": [["trivia-desktop-build", "--dir"], ["trivia-steam", "stage"]],
    "credits": [["node", "authoring/steam/credits_check.mjs", UNPACKED, UNPACKED_WIN]],
    "smoke": [["node", "authoring/steam/smoke.mjs", UNPACKED]],
}
SHIPPED = ("app/", "flake.nix", "flake.lock", "package.json", "package-lock.json")
STATE_TS = "app/client/src/engine/state.ts"
MEDIA_BUDGET = "masterplan 10 part 6, task 260"
# Row → (scope, check, check on a content-only patch); scope: always, full (full release only), save
# (only when SAVE_VERSION changed). Steps: plans/11-steam.md "Release checklist (ST-4)".
MANUAL = {
    "offline": ("always", "beta install, network off, Steam not running: full game to level 12 or a won checkpoint",
                "beta install, network off, Steam not running: a game to level 3 that hits new questions"),
    "windows": ("full", "start test on a clean Windows machine from Steam (beta)", None),
    "deck": ("full", "Steam Deck checklist (plan 90, SW-12; plans/18-steam-integration.md \"Steam Deck Verified\")", None),
    "cloud": ("full", "Cloud A→B (plan 87): play on A, quit, B shows the same players and seen counts", None),
    "sound": ("full", "sound: music, effects, audio and video questions", None),
    "red-frame": ("full", "timed competitive: pulsing red frame in the last 3 s", None),
    "beta-save": ("save", "save version changed: testers stay on beta until this build is on default", None),
    "signoff": ("always", "the family plays the candidate from beta", "the gamemaster's OK"),
}


def quality(out: str) -> str | None:
    """Failure of the release bar in `qgen report --qc`'s table, None if the last two batches pass."""
    head = next((l for l in out.splitlines() if l.startswith("| metric |")), None)
    row = next((l for l in out.splitlines() if l.startswith("| **release**")), None)
    if not head or not row:
        return "no release row in qgen report --qc"
    cells = lambda l: [c.strip() for c in l.strip("|").split("|")][1:]
    batches = [(r, v) for r, v in zip(cells(head), cells(row)) if re.fullmatch(r"batch-\d+", r)][-2:]
    if len(batches) < 2:
        return f"{len(batches)} batch(es) with a QC column, need 2"
    bad = [f"{r} {v}" for r, v in batches if v != "✓"]
    return "; ".join(bad) or None


def tag_gate() -> str | None:
    """Failure of the tag step: dirty tree or HEAD without v<version>."""
    want = f"v{version()}"
    fails = ["uncommitted changes: commit"] if git("status", "--porcelain") else []
    if want not in git("tag", "--points-at", "HEAD").split():
        fails.append(f"HEAD not tagged {want}: `git tag {want}` (or bump app/desktop/package.json)")
    return "; ".join(fails) or None


def previous_tag(rev: str = "HEAD", own: bool = False) -> str | None:
    """Newest v* tag reachable from rev, other than rev's own unless own (also used by qgen patch-notes)."""
    skip = set() if own else set(git("tag", "--points-at", rev).split())
    tags = git("tag", "--merged", rev, "--list", "v*", "--sort=-v:refname").split()
    return next((t for t in tags if t not in skip), None)


def kind(prev: str | None, rev: str | None = "HEAD") -> str:
    """`full`, or `content-only` if nothing shipped outside app/data/ changed from prev to rev (None: working tree)."""
    if not prev:
        return "full"
    changed = git("diff", "--name-only", prev, *([rev] if rev else [])).splitlines()
    code = [f for f in changed if f.startswith(SHIPPED) and not f.startswith("app/data/")]
    return "full" if code else "content-only"


def save_version(rev: str | None) -> int | None:
    """SAVE_VERSION at rev (None: working tree)."""
    src = git("show", f"{rev}:{STATE_TS}") if rev else (REPO / STATE_TS).read_text()
    m = re.search(r"SAVE_VERSION = (\d+)", src)
    return int(m.group(1)) if m else None


def run(name: str, logs: Path) -> str | None:
    """Run a step's commands, output to logs/<name>.log; the failure or None."""
    log = logs / f"{name}.log"
    with log.open("w") as f:
        for cmd in STEPS[name]:
            f.write(f"$ {' '.join(cmd)}\n")
            f.flush()
            try:
                p = subprocess.run(cmd, cwd=REPO, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            except FileNotFoundError:
                return f"{cmd[0]} not found (run from the dev shell)"
            f.write(p.stdout)
            if p.returncode:
                return f"`{' '.join(cmd)}` exit {p.returncode}"
            if name == "quality":
                return quality(p.stdout)
    return None


def checklist(kd: str, prev: str | None, save_changed: bool) -> dict[str, tuple[str, str | None]]:
    """Manual rows for this candidate: row → (check, automatic answer or None)."""
    rows = {}
    for k, (scope, text, patch) in MANUAL.items():
        if scope == "save" and not save_changed:
            continue
        auto = f"skipped: content-only since {prev}" if scope == "full" and kd == "content-only" else None
        rows[k] = (patch if patch and kd == "content-only" else text, auto)
    return rows


def manual(rows: dict[str, tuple[str, str | None]], path: str | None, ask: bool) -> dict[str, str]:
    """Answers per manual row: automatic, from FILE, else asked on the terminal (only if ask)."""
    open_rows = {k: text for k, (text, auto) in rows.items() if auto is None}
    if path:
        lines = [l.split(":", 1) for l in Path(path).read_text().splitlines() if ":" in l]
        given = {k.strip(): v.strip() for k, v in lines}
        for k in given.keys() - MANUAL.keys():
            print(f"  {path}: unknown row {k!r}", file=sys.stderr)
        answers = {k: given.get(k, "") for k in open_rows}
    elif not ask:
        answers = {k: "not asked (automated ✗)" for k in open_rows}
    else:
        print("Manual checklist (y / n / a note):")
        answers = {k: input(f"  {k}: {text}? ").strip() for k, text in open_rows.items()}
    return {k: auto or answers[k] for k, (_, auto) in rows.items()}


def main() -> None:
    p = argparse.ArgumentParser(prog="trivia-release-check", description=__doc__.split("\n")[0])
    p.add_argument("--skip", action="append", default=[], choices=["tag", *STEPS, "manual"], help="known-broken step")
    p.add_argument("--manual", metavar="FILE", help="manual answers, `<row>: <answer>` per line")
    args = p.parse_args()

    commit, tag = git("rev-parse", "HEAD"), head_tag()
    clean = not git("status", "--porcelain")
    prev = previous_tag()
    kd = kind(prev)
    save = {"head": save_version("HEAD"), "previous": save_version(prev) if prev else None}
    save["changed"] = bool(prev) and save["head"] != save["previous"]
    m = re.search(r'"hash": "(\w+)"', (REPO / "app" / "data" / "pool.json").read_text()[:1000])
    pool_hash = m.group(1) if m else None
    kind_text = f"content-only patch since {prev}" if kd == "content-only" else "full"
    save_text = (f"changed ({save['previous']} → {save['head']})" if save["changed"]
                 else f"unchanged ({save['head']})" if prev else f"{save['head']} (no earlier tag)")
    out = REPO / "work" / "steam" / tag
    logs = out / "logs"
    logs.mkdir(parents=True, exist_ok=True)
    started = datetime.now().astimezone()
    print(f"release check {tag} ({commit[:7]}{'' if clean else ', uncommitted changes'})")
    print(f"  version {version()}, pool {pool_hash}, previous tag {prev or 'none'}, {kind_text}, save version {save_text}")

    steps = []  # (name, status ✓/✗/skipped, seconds, note)
    if "tag" in args.skip:
        steps.append(("tag", "skipped", 0, "--skip"))
        print("– tag: skipped")
    else:
        fail = tag_gate()
        steps.append(("tag", "✗" if fail else "✓", 0, fail or ""))
        print(f"{'✗' if fail else '✓'} tag{': ' + fail if fail else ''}")
    for name in STEPS:
        if name in args.skip:
            steps.append((name, "skipped", 0, "--skip"))
            print(f"– {name}: skipped")
            continue
        t = time.monotonic()
        fail = run(name, logs)
        dt = time.monotonic() - t
        steps.append((name, "✗" if fail else "✓", dt, fail or ""))
        print(f"{'✗' if fail else '✓'} {name} ({dt:.0f} s){': ' + fail + f' (log {logs / name}.log)' if fail else ''}")
    steps.append(("media-budget", "skipped", 0, MEDIA_BUDGET))
    print(f"– media-budget: skipped ({MEDIA_BUDGET})")

    rows = []  # (row, check, status, answer)
    if "manual" in args.skip:
        steps.append(("manual", "skipped", 0, "--skip"))
    else:
        todo = checklist(kd, prev, save["changed"])
        answers = manual(todo, args.manual, all(s != "✗" for _, s, _, _ in steps))
        for k, a in answers.items():
            st = "✓" if a[:1].lower() == "y" else "✗" if a[:1].lower() == "n" else "skipped"
            rows.append((k, todo[k][0], st, a))
            print(f"{'–' if st == 'skipped' else st} manual {k}: {a or '(no answer)'}")
        failed = [k for k, _, s, _ in rows if s == "✗"]
        steps.append(("manual", "✗" if failed else "✓", 0, ", ".join(failed)))

    skipped = [n for n, s, _, _ in steps if s == "skipped"] + [f"manual:{k}" for k, _, s, _ in rows if s == "skipped"]
    ok = all(s != "✗" for _, s, _, _ in steps)
    report = {"commit": commit, "tag": tag, "clean": clean, "date": started.isoformat(timespec="seconds"),
              "version": version(), "pool_hash": pool_hash, "previous_tag": prev, "kind": kd, "save_version": save,
              "ok": ok, "skipped": skipped,
              "steps": [{"name": n, "status": s, "seconds": round(dt), "note": note} for n, s, dt, note in steps],
              "manual": [{"row": k, "status": s, "answer": a} for k, _, s, a in rows]}
    (out / "release-check.json").write_text(json.dumps(report, ensure_ascii=False, indent=1) + "\n")
    md = [f"# Release check {tag}", "",
          f"- Result: {'✓ pass' if ok else '✗ fail'}",
          f"- Commit: {commit}{'' if clean else ' (uncommitted changes)'}",
          f"- Date: {report['date']}",
          f"- Version: {version()}, pool hash {pool_hash}",
          f"- Previous tag: {prev or 'none'}",
          f"- Kind: {kind_text}",
          f"- Save version: {save_text}",
          f"- Skipped: {', '.join(skipped) or 'none'}", "",
          "| step | | time | note |", "|---|---|---:|---|",
          *[f"| {n} | {s} | {dt:.0f} s | {note} |" for n, s, dt, note in steps], "",
          "## Manual", "", "| row | check | | answer |", "|---|---|---|---|",
          *[f"| {k} | {text} | {s} | {a} |" for k, text, s, a in rows], ""]
    (out / "release-check.md").write_text("\n".join(md))
    print(f"{'✓ pass' if ok else '✗ fail'}{', skipped: ' + ', '.join(skipped) if skipped else ''}"
          f" → {(out / 'release-check.md').relative_to(REPO)}")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
