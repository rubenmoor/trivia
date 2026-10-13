"""Atomic writes for the authoring tools: `<name>.tmp` next to the file, then replace (a crash keeps the old file).
A read-modify-write holds `locked(path)`: across threads and processes (authoring server ↔ qgen).
Lock order: the source pool before a questions.<locale>.json."""
import contextlib, json, os, threading, time

STALE = 60  # s: an older lock file was left by a crashed process; holders stay well below
_locks, _locks_lock = {}, threading.Lock()


@contextlib.contextmanager
def locked(path):
    """Hold `<name>.lock` next to path (re-entrant per thread); waits for another holder."""
    with _locks_lock:
        entry = _locks.setdefault(str(path), [threading.RLock(), 0])
    lock = path.with_name(path.name + ".lock")
    with entry[0]:
        if not entry[1]:
            _acquire(lock)
        entry[1] += 1
        try:
            yield
        finally:
            entry[1] -= 1
            if not entry[1]:
                lock.unlink(missing_ok=True)


def _acquire(lock):
    lock.parent.mkdir(parents=True, exist_ok=True)
    while True:
        try:
            os.close(os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY))
            return
        except (FileExistsError, PermissionError):  # Windows: PermissionError while the holder deletes it
            pass
        try:
            if time.time() - lock.stat().st_mtime > STALE:
                lock.unlink(missing_ok=True)
                continue
        except FileNotFoundError:
            continue
        time.sleep(0.05)


def write_text(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    tmp.replace(path)


def write_json(path, data):
    """Indented, UTF-8 as written, trailing newline: the format of every authoring JSON file."""
    write_text(path, json.dumps(data, ensure_ascii=False, indent=2) + "\n")
