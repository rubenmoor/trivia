"""Calls into the TS engine under Node (D-60): JSON on stdin, JSON on stdout. Never re-implements a rule."""
import fcntl, json, os, shutil, subprocess, sys

from layout import AUTHORING, WORK

SIM = AUTHORING / "tools" / "sim" / "simulate.ts"
CAREER = AUTHORING / "tools" / "sim" / "career.ts"
SUPPLY = AUTHORING / "tools" / "supply.ts"


CELL_TIMEOUT = 7200  # seconds per node cell (chinese-base en, default run: slowest cell ~5000 s)


def lock():
    """Exclusive flock on work/simulate.lock for this process (simulate and career runs); a second run exits naming the holder's PID."""
    WORK.mkdir(parents=True, exist_ok=True)
    f = open(WORK / "simulate.lock", "a+", encoding="utf-8")
    try:
        fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        f.seek(0)
        raise SystemExit(f"another qgen report --simulate/--career run holds work/simulate.lock (PID {f.read().strip() or '?'})") from None
    f.truncate(0)
    f.write(str(os.getpid()))
    f.flush()
    return f


def node(script, payload, timeout=None):
    """Runs `node <script>` with payload as JSON on stdin; its stdout parsed as JSON; `timeout` seconds."""
    exe = shutil.which("node")
    if exe is None:
        raise SystemExit("qgen report and the authoring start page need node: run inside the dev shell (direnv allow or nix develop)")
    try:
        out = subprocess.run([exe, str(script)], input=json.dumps(payload), capture_output=True, text=True, encoding="utf-8", timeout=timeout)
    except subprocess.TimeoutExpired:
        raise SystemExit(f"{script.name} timed out after {timeout} s") from None
    if out.returncode:
        raise SystemExit(f"{script.name} failed:\n{out.stderr.strip()}")
    try:
        return json.loads(out.stdout)
    except json.JSONDecodeError as e:
        raise SystemExit(f"{script.name}: no JSON on stdout ({e}):\n{out.stdout[:500]}{out.stderr.strip()}") from None


def _cell(script, cell):
    """One cell under CELL_TIMEOUT; a stderr line when it finishes."""
    out = node(script, cell, CELL_TIMEOUT)
    c = cell if isinstance(cell, dict) else {}
    print(f"{script.stem}: done {c.get('locale', '')} {c.get('mode', '')} {c.get('age_group', '')} {c.get('player', '')} {c.get('players', '')}".rstrip(), file=sys.stderr, flush=True)
    return out


def simulate(cells):
    """Games per new player for each cell (plan 62); one node process per call."""
    return _cell(SIM, cells)


def career(cell):
    """Career supply figures of one cell (milestone 20, plan 193): sim/career.ts."""
    return _cell(CAREER, cell)


def supply(questions, blocked, **opts):
    """{per_level, ranges {"1": [lo, hi], …}, bundles, supply [{level, range, candidates, missing}]} from selection.ts;
    questions minus unapproved and `blocked` ids (stdin key `burned`); opts: age_group (default young_teens),
    bundles (default: the default game's, es's first base bundle; decision 103)."""
    return node(SUPPLY, {"questions": questions, "burned": sorted(blocked), **opts})


def supplies(*inputs):
    """`supply` for several (questions, blocked) pairs in one node process."""
    return node(SUPPLY, [{"questions": q, "burned": sorted(b)} for q, b in inputs])
