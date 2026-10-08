"""Progress output for the long `qgen` steps (QG-18). Standard library only.

On a terminal: a live bar on the last line, redrawn twice a second; other output scrolls above it.
Otherwise (a pipe or a log, e.g. Claude Code running `qgen batch`): no bar, a plain status line
every minute, so the output stays readable as text. Either way a summary line when a bar closes.
"""
import shutil, sys, threading, time

LIVE = sys.stdout.isatty() and sys.stderr.isatty()
REDRAW = 0.5  # seconds between redraws on a terminal
HEARTBEAT = 60  # seconds between status lines otherwise
WIDTH = 20  # characters of the bar itself

_lock = threading.RLock()
_err = sys.stderr  # the real stderr, where the live bar is drawn
_active = None  # the bar on screen
_drawn = False  # the live bar is drawn on the current line
_line_start = True  # nothing else is half-written on the current line


def duration(seconds):
    s = int(seconds)
    if s < 60:
        return f"{s}s"
    if s < 3600:
        return f"{s // 60}m{s % 60:02d}s"
    return f"{s // 3600}h{s % 3600 // 60:02d}m"


class _Stream:
    """Stands in for stdout/stderr while a live bar is used: clears the bar before other output
    and draws it again below once that output ends a line."""

    def __init__(self, real):
        self.real = real

    def write(self, s):
        global _drawn, _line_start
        with _lock:
            if _drawn:
                _err.write("\r\033[K")
                _err.flush()
                _drawn = False
            n = self.real.write(s)
            self.real.flush()
            if s:
                _line_start = s.endswith("\n")
            if _line_start and _active:
                _draw()
            return n

    def flush(self):
        self.real.flush()

    def __getattr__(self, name):
        return getattr(self.real, name)


def _install():
    if LIVE and not isinstance(sys.stdout, _Stream):
        sys.stdout, sys.stderr = _Stream(sys.stdout), _Stream(sys.stderr)


def _draw():
    global _drawn
    width = shutil.get_terminal_size().columns - 1  # a wrapped line can't be cleared with \r
    _err.write("\r\033[K" + _active.line()[:width])
    _err.flush()
    _drawn = True


def _clear():
    global _drawn
    if _drawn:
        _err.write("\r\033[K")
        _err.flush()
        _drawn = False


class Bar:
    """Progress over `total` items. Workers call `started()` and `finished()`; use as a context
    manager. A bar with nothing to do prints nothing."""

    def __init__(self, label, total, unit="items"):
        self.label, self.total, self.unit = label, total, unit
        self.n = self.failed = self.running = 0
        self.t0 = time.monotonic()
        self._stop = threading.Event()
        self._prev = None

    def __enter__(self):
        global _active
        if not self.total:
            return self
        _install()
        with _lock:
            self._prev, _active = _active, self
        threading.Thread(target=self._tick, daemon=True).start()
        return self

    def __exit__(self, *exc):
        global _active
        if not self.total:
            return False
        self._stop.set()
        with _lock:
            _clear()
            _active = self._prev
        print(f"  {self.label}: {self.n}/{self.total} {self.unit} in {duration(time.monotonic() - self.t0)}"
              + (f", {self.failed} failed" if self.failed else ""), flush=True)
        return False

    def started(self):
        with _lock:
            self.running += 1

    def finished(self, ok=True):
        with _lock:
            self.running = max(0, self.running - 1)
            self.n += 1
            self.failed += not ok
            if LIVE and _active is self and _line_start:
                _draw()

    def line(self, live=True):
        elapsed = time.monotonic() - self.t0
        parts = [f"{self.n}/{self.total} {self.unit}"]
        if self.running:
            parts.append(f"{self.running} running")
        if self.failed:
            parts.append(f"{self.failed} failed")
        parts.append(duration(elapsed))
        if 0 < self.n < self.total:
            parts.append(f"~{duration(elapsed / self.n * (self.total - self.n))} left")
        if live:
            full = WIDTH * self.n // self.total
            return f"  {self.label} {'█' * full}{'░' * (WIDTH - full)} " + " · ".join(parts)
        return f"  … {self.label}: {100 * self.n // self.total}% · " + " · ".join(parts)

    def _tick(self):
        while not self._stop.wait(REDRAW if LIVE else HEARTBEAT):
            with _lock:
                if self._stop.is_set():
                    return
                if LIVE:
                    if _active is self and _line_start:
                        _draw()
                else:
                    print(self.line(live=False), flush=True)
