"""Plain, append-only log of the long `qgen` steps (QG-18, QG-20, task 1131). Standard library only.

Written for an agent reading a pipe as much as for a terminal: no bar, no `\\r`, no escape codes;
every line is written whole under one lock, so parallel calls (`--jobs`) never mix half lines.
- `waiting()`: a start and a result line per outside call (Claude, provider search, download),
  with the time, the step and the item (`item()`, set per item by `qgen`'s `parallel()`).
- `resumed()`: one line when a step skips work done by an earlier run.
- `Bar`: one summary line per step (`label: n/total in 3m10s, k failed`).
- `fail()`: a failure line, kept so `run_steps` can repeat the step's failures before it exits.
- `detail()`: a line per item; `qgen batch` turns those off (`verbose = False`).
"""
import contextlib, sys, threading, time

_lock = threading.RLock()
_ctx = threading.local()  # step, item: what the current thread works on
verbose = True  # print detail() lines
failures = []  # fail() lines since run_steps last cleared it


def say(msg, err=False):
    """One whole line, never interleaved with another thread's."""
    with _lock:
        out = sys.stderr if err else sys.stdout
        out.write(msg + "\n")
        out.flush()


def detail(msg):
    """A line about one item: printed by the single steps, not by `qgen batch` (QG-20)."""
    if verbose:
        say(msg)


def fail(msg):
    """A FAILED line on stderr, kept for run_steps' closing block."""
    with _lock:
        failures.append(msg.strip())
        say(msg, err=True)


def resumed(label, done, todo, unit="items"):
    """One line when a step skips `done` items finished by an earlier run; nothing on a fresh start."""
    if done and todo:
        say(f"  {label}: {done}/{done + todo} {unit} done earlier, skipped; {todo} to do")
    elif done:
        say(f"  {label}: all done earlier, skipped ({done} {unit})")


@contextlib.contextmanager
def item(step, name):
    """What the current thread works on, named by every waiting() line inside the block."""
    old = getattr(_ctx, "where", None)
    _ctx.where = (step, name)
    try:
        yield
    finally:
        _ctx.where = old


def where():
    """(step, item) of the current thread, or (None, None)."""
    return getattr(_ctx, "where", None) or (None, None)


class _Call:
    def __init__(self):
        self.outcome = None
        self.extra = ""  # after the duration: "$0.84 31k tok"

    def result(self, text):
        """The result line's text ("ok 12 results", "failed (exit 1): …"); default "ok"."""
        self.outcome = text


def short(text, n=160):
    line = " ".join(str(text).split())
    return line if len(line) <= n else line[:n - 1] + "…"


@contextlib.contextmanager
def waiting(what):
    """A start line and a result line, with its duration, for one outside call ("claude opus",
    "Openverse search", …). An exception from the block is logged as "failed: …" and re-raised."""
    head = " ".join(x for x in (what, *where()) if x)
    say(f"{time.strftime('%H:%M:%S')} {head}")
    call, t = _Call(), time.monotonic()
    try:
        yield call
    except BaseException as e:
        call.outcome = call.outcome or f"failed: {short(e) or type(e).__name__}"
        raise
    finally:
        say(f"{time.strftime('%H:%M:%S')} {head} {call.outcome or 'ok'} {duration(time.monotonic() - t)}"
            + (f" {call.extra}" if call.extra else ""))


def duration(seconds):
    s = int(seconds)
    if s < 60:
        return f"{s}s"
    if s < 3600:
        return f"{s // 60}m{s % 60:02d}s"
    return f"{s // 3600}h{s % 3600 // 60:02d}m"


class Bar:
    """Counts `total` items; one summary line when the block ends. Workers call `finished()`;
    use as a context manager. A bar with nothing to do prints nothing."""

    def __init__(self, label, total, unit="items"):
        self.label, self.total, self.unit = label, total, unit
        self.n = self.failed = 0
        self.t0 = time.monotonic()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        if self.total:
            say(f"  {self.label}: {self.n}/{self.total} {self.unit} in {duration(time.monotonic() - self.t0)}"
                + (f", {self.failed} failed" if self.failed else ""))
        return False

    def finished(self, ok=True):
        with _lock:
            self.n += 1
            self.failed += not ok
