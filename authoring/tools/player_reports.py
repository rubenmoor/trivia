"""`qgen flag` and `qgen telemetry`: player reports and opt-in telemetry (plans 93, 109). Never ships (D-35)."""
import datetime, json, os, sys
from pathlib import Path
from collections import Counter

from layout import REPO as ROOT
import atomic  # authoring/tools/atomic.py: .tmp + replace writes, cross-process locks
import paths  # authoring/tools/paths.py: state/ (TRIVIA_STATE)
import reviews  # authoring/tools/reviews.py: review writes, player reports (plan 93)
import played  # authoring/tools/played.py: opt-in telemetry → state/played/ (plan 109)

from qgen import load_json  # authoring/tools/qgen.py


# --- player reports (plan 93) -------------------------------------------------

def apply_reports(reports, dry_run=False):
    """Reports (reviews.report_feedback's dicts) → human needs_work reviews; returns (applied, already, skipped)."""
    known, n = {}, Counter()
    for r in reports:
        where = f"{r['question']} ({r['lang']})"
        new = reviews.needs_work(r["question"], r["lang"], reviews.report_feedback(r), known, dry_run)
        if new is None:
            print(f"  {where}: unknown question, skipped", file=sys.stderr)
            n["skipped"] += 1
        elif not new:
            print(f"  {where}: already there")
            n["already"] += 1
        else:
            print(f"  {where}: needs_work" + (f" ← {new}" if dry_run else ""))
            n["applied"] += 1
    return n["applied"], n["already"], n["skipped"]


PULLED = paths.STATE / "reports-pulled.json"  # {"<url>": [server ids written, not yet acked]}
TOKEN_FILE = paths.STATE / "report-token"  # gitignored


def report_api(url, token, path, body=None):
    """One call to the report server (plan 103, API v1) → parsed JSON; errors exit."""
    import urllib.request, urllib.error
    req = urllib.request.Request(url + path, method="POST" if body is not None else "GET",
                                 data=json.dumps(body).encode() if body is not None else None,
                                 headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as res:
            return json.load(res)
    except urllib.error.HTTPError as e:
        hint = {401: ": wrong pull token"}.get(e.code, "")
        sys.exit(f"{url}{path}: HTTP {e.code}{hint} {e.read()[:200].decode(errors='replace')}")
    except (urllib.error.URLError, TimeoutError) as e:
        sys.exit(f"{url}{path}: {getattr(e, 'reason', e)}")


def report_server(url):
    """(base URL, pull token): --url, else reportUrl in app/desktop/package.json; token from env or file."""
    url = (url or json.loads((ROOT / "app" / "desktop" / "package.json").read_text())["reportUrl"]).rstrip("/")
    if not url:
        sys.exit("no report URL: pass --url or set reportUrl in app/desktop/package.json")
    token = os.environ.get("TRIVIA_REPORT_TOKEN", "").strip() or (
        TOKEN_FILE.read_text().strip() if TOKEN_FILE.exists() else "")
    if not token:
        sys.exit(f"no pull token: set TRIVIA_REPORT_TOKEN or write it to {TOKEN_FILE}")
    return url, token


def pull_reports(args):
    """`qgen flag --pull`: the server's reports → needs_work reviews, then ack (plan 93 task 5).
    Pages are acked one by one: GET returns the same reports until acked."""
    url, token = report_server(args.url)
    ledger = load_json(PULLED) if PULLED.exists() else {}
    done = set(ledger.get(url, []))
    n = Counter()
    while True:
        page = report_api(url, token, "/reports?limit=500")
        rs = page["reports"]
        n["pulled"] += len(rs)
        new = [r for r in rs if r["id"] not in done]
        n["earlier"] += len(rs) - len(new)
        mods = [r for r in new if ":" in r["question"]]  # mod questions aren't ours (decision 128)
        n["mod"] += len(mods)
        a, b, s = apply_reports([{**r, "note": r["note"] or None, "date": r["received_at"][:10]}
                                 for r in new if r not in mods], args.dry_run)
        n["applied"] += a; n["already"] += b; n["unknown"] += s
        if args.dry_run:
            if page["more"]:
                print("  more reports on the server: --dry-run shows only the first page")
            break
        if not rs:
            break
        ids = [r["id"] for r in rs]
        done.update(ids)
        atomic.write_json(PULLED, {**ledger, url: sorted(done)})  # before the ack: a crash can't double feedback
        report_api(url, token, "/reports/ack", {"ids": ids})
        done.difference_update(ids)  # acked = deleted on the server; SQLite may reuse their ids
        ledger = {**ledger, url: sorted(done)}
        atomic.write_json(PULLED, ledger)
        if not page["more"]:
            break
    print(f"{n['pulled']} pulled: {n['applied']} {'would be ' if args.dry_run else ''}applied, "
          f"{n['already'] + n['earlier']} already there, {n['unknown'] + n['mod']} skipped "
          f"({n['unknown']} unknown, {n['mod']} mod questions)")


def cmd_flag(args):
    """Pasted report text (stdin) → needs_work reviews (plan 93, decision 142); --pull: the report server's."""
    if args.pull:
        return pull_reports(args)
    reports = reviews.parse_reports(sys.stdin.read())
    if not reports:
        sys.exit("no report found: paste text with a «¡Trivia! #q-… · …» line")
    applied, already, skipped = apply_reports(reports, args.dry_run)
    print(f"{len(reports)} reports: {applied} {'would be ' if args.dry_run else ''}applied, "
          f"{already} already there, {skipped} skipped")


def cmd_telemetry(args):
    """`qgen telemetry --pull`: telemetry sessions → state/played/stats.json, then ack (plan 109)."""
    if not args.pull:
        sys.exit("qgen telemetry: nothing to do without --pull")
    known = played.rated()
    if args.from_file:
        stats = played.load()
        doc, today = load_json(Path(args.from_file)), datetime.datetime.now(datetime.timezone.utc).date().isoformat()
        sessions = doc["sessions"] if "sessions" in doc else [doc]  # also one POST body, e.g. the fixture
        n = played.fold(stats, [{"received_day": today, **s} for s in sessions], known)
        if not args.dry_run:
            played.save(stats)
        n.update(pages=0, acked=0)
    else:
        url, token = report_server(args.url)
        n = played.pull(lambda path, body=None: report_api(url, token, path, body), known, args.dry_run)
    print(f"{n['sessions']} sessions, {n['games']} games, {n['answers']} answers "
          f"{'would be ' if args.dry_run else ''}folded ({n['unknown']} unknown ids), "
          f"{n['pages']} pages, {n['acked']} acked" + (" (more on the server)" if n.get("more") else ""))
