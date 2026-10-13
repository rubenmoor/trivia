"""Calls into the TS engine under Node (D-60): JSON on stdin, JSON on stdout. Never re-implements a rule."""
import json, shutil, subprocess

from layout import AUTHORING

SIM = AUTHORING / "tools" / "sim" / "simulate.ts"
SUPPLY = AUTHORING / "tools" / "supply.ts"


def node(script, payload):
    """Runs `node <script>` with payload as JSON on stdin; its stdout parsed as JSON."""
    exe = shutil.which("node")
    if exe is None:
        raise SystemExit("qgen report and the authoring start page need node: run inside the dev shell (direnv allow or nix develop)")
    out = subprocess.run([exe, str(script)], input=json.dumps(payload), capture_output=True, text=True, encoding="utf-8")
    if out.returncode:
        raise SystemExit(f"{script.name} failed:\n{out.stderr.strip()}")
    try:
        return json.loads(out.stdout)
    except json.JSONDecodeError as e:
        raise SystemExit(f"{script.name}: no JSON on stdout ({e}):\n{out.stdout[:500]}{out.stderr.strip()}") from None


def simulate(cells):
    """Games per new player for each cell (plan 62); one node process per call."""
    return node(SIM, cells)


def supply(questions, blocked, **opts):
    """{per_level, ranges {"1": [lo, hi], …}, bundles, supply [{level, range, candidates, missing}]} from selection.ts;
    questions minus unapproved and `blocked` ids (stdin key `burned`); opts: age_group (default young_teens),
    bundles (default: the default game's, es's first base bundle; decision 103)."""
    return node(SUPPLY, {"questions": questions, "burned": sorted(blocked), **opts})


def supplies(*inputs):
    """`supply` for several (questions, blocked) pairs in one node process."""
    return node(SUPPLY, [{"questions": q, "burned": sorted(b)} for q, b in inputs])
