"""Calls into the TS engine under Node (D-60): JSON on stdin, JSON on stdout. Never re-implements a rule."""
import json, shutil, subprocess

from layout import AUTHORING

SIM = AUTHORING / "tools" / "sim" / "simulate.ts"


def node(script, payload):
    """Runs `node <script>` with payload as JSON on stdin; its stdout parsed as JSON."""
    exe = shutil.which("node")
    if exe is None:
        raise SystemExit("needs node: run inside the dev shell (direnv allow or nix develop)")
    out = subprocess.run([exe, str(script)], input=json.dumps(payload), capture_output=True, text=True)
    if out.returncode:
        raise SystemExit(f"{script.name} failed:\n{out.stderr.strip()}")
    return json.loads(out.stdout)


def simulate(cells):
    """Games per new player for each cell (plan 62); one node process per call."""
    return node(SIM, cells)
