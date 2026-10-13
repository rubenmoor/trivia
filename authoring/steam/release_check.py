#!/usr/bin/env python3
"""Release check before every Steam upload (SW-6, pm decision 14; plan 89).

    trivia-release-check [--skip STEP]... [--manual FILE]

Steps, each ✓/✗ with its time; all automated steps run, exit 1 on any ✗:
  checks    npm run check, npm test, npm run build, qgen validate
  licenses  trivia-media licenses --status approved (exit 1 = files to replace)
  quality   qgen report --qc: release bar ✓ for the last two batches (pm decision 15)
  nix       nix build .#app (D-59)
  desktop   trivia-desktop-build --dir (stage-media's missing-file check) + trivia-steam stage
  smoke     node authoring/steam/smoke.mjs app/desktop/release/linux-unpacked
  manual    the rows of MANUAL, asked y/n/note or read from --manual FILE (`<row>: <answer>` per line);
            "n…" fails, "y…" passes, anything else is a note and counts as skipped

`--skip STEP` (repeatable): a known-broken step, ✗ → "skipped" in the report (and the build Desc).
Run from the dev shell (nix, steam-run, Xvfb). Report: work/steam/<tag-or-sha>/release-check.md,
release-check.json for `trivia-steam upload --checked` (commit, clean, ok, skipped), logs/<step>.log.
"""
import argparse, json, re, subprocess, sys, time
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from steam import REPO, git, head_tag  # noqa: E402

UNPACKED = "app/desktop/release/linux-unpacked"
STEPS = {
    "checks": [["npm", "run", "check"], ["npm", "test"], ["npm", "run", "build"], ["qgen", "validate"]],
    "licenses": [["trivia-media", "licenses", "--status", "approved"]],
    "quality": [["qgen", "report", "--qc"]],
    "nix": [["nix", "build", ".#app", "--no-link"]],
    "desktop": [["trivia-desktop-build", "--dir"], ["trivia-steam", "stage"]],
    "smoke": [["node", "authoring/steam/smoke.mjs", UNPACKED]],
}
# Later parts append rows here.
MANUAL = {
    "windows": "start test on a clean Windows machine (archive or last beta)",
    "deck": "start test on the Steam Deck (archive or last beta)",
    "sound": "sound: music, effects, audio questions",
    "red-frame": "timed competitive: pulsing red frame in the last 3 s",
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


def manual(path: str | None, ask: bool) -> dict[str, str]:
    """Answers per manual row: from FILE, else asked on the terminal (only if ask)."""
    if path:
        lines = [l.split(":", 1) for l in Path(path).read_text().splitlines() if ":" in l]
        given = {k.strip(): v.strip() for k, v in lines}
        return {k: given.get(k, "") for k in MANUAL}
    if not ask:
        return {k: "not asked (automated ✗)" for k in MANUAL}
    print("Manual checklist (y / n / a note):")
    return {k: input(f"  {k}: {text}? ").strip() for k, text in MANUAL.items()}


def main() -> None:
    p = argparse.ArgumentParser(prog="trivia-release-check", description=__doc__.split("\n")[0])
    p.add_argument("--skip", action="append", default=[], choices=[*STEPS, "manual"], help="known-broken step")
    p.add_argument("--manual", metavar="FILE", help="manual answers, `<row>: <answer>` per line")
    args = p.parse_args()

    commit, tag = git("rev-parse", "HEAD"), head_tag()
    clean = not git("status", "--porcelain")
    out = REPO / "work" / "steam" / tag
    logs = out / "logs"
    logs.mkdir(parents=True, exist_ok=True)
    started = datetime.now().astimezone()
    print(f"release check {tag} ({commit[:7]}{'' if clean else ', uncommitted changes'})")

    steps = []  # (name, status ✓/✗/skipped, seconds, note)
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

    rows = []  # (row, status, answer)
    if "manual" in args.skip:
        steps.append(("manual", "skipped", 0, "--skip"))
    else:
        answers = manual(args.manual, all(s != "✗" for _, s, _, _ in steps))
        for k, a in answers.items():
            rows.append((k, "✓" if a[:1].lower() == "y" else "✗" if a[:1].lower() == "n" else "skipped", a))
        failed = [k for k, s, _ in rows if s == "✗"]
        steps.append(("manual", "✗" if failed else "✓", 0, ", ".join(failed)))

    skipped = [n for n, s, _, _ in steps if s == "skipped"] + [f"manual:{k}" for k, s, _ in rows if s == "skipped"]
    ok = all(s != "✗" for _, s, _, _ in steps)
    report = {"commit": commit, "tag": tag, "clean": clean, "date": started.isoformat(timespec="seconds"),
              "ok": ok, "skipped": skipped,
              "steps": [{"name": n, "status": s, "seconds": round(dt), "note": note} for n, s, dt, note in steps],
              "manual": [{"row": k, "status": s, "answer": a} for k, s, a in rows]}
    (out / "release-check.json").write_text(json.dumps(report, ensure_ascii=False, indent=1) + "\n")
    md = [f"# Release check {tag}", "",
          f"- Result: {'✓ pass' if ok else '✗ fail'}",
          f"- Commit: {commit}{'' if clean else ' (uncommitted changes)'}",
          f"- Date: {report['date']}",
          f"- Skipped: {', '.join(skipped) or 'none'}", "",
          "| step | | time | note |", "|---|---|---:|---|",
          *[f"| {n} | {s} | {dt:.0f} s | {note} |" for n, s, dt, note in steps], "",
          "## Manual", "", "| row | check | | answer |", "|---|---|---|---|",
          *[f"| {k} | {MANUAL[k]} | {s} | {a} |" for k, s, a in rows], ""]
    (out / "release-check.md").write_text("\n".join(md))
    print(f"{'✓ pass' if ok else '✗ fail'}{', skipped: ' + ', '.join(skipped) if skipped else ''}"
          f" → {(out / 'release-check.md').relative_to(REPO)}")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
