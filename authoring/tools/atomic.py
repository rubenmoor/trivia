"""Atomic writes for the authoring tools: `<name>.tmp` next to the file, then replace (a crash keeps the old file).
A read-modify-write holds `locked(path)`: across threads and processes (authoring server ↔ qgen).
Lock order: the source pool before a questions.<locale>.json."""
import contextlib, fcntl, json, os, threading

_locks, _locks_lock = {}, threading.Lock()


@contextlib.contextmanager
def locked(path):
    """Hold `<name>.lock` next to path (re-entrant per thread); waits for another holder.
    flock: the OS frees it on a crash; the file stays (unlinking it would let two holders in)."""
    with _locks_lock:
        entry = _locks.setdefault(str(path), [threading.RLock(), 0, None])
    lock = path.with_name(path.name + ".lock")
    with entry[0]:
        if not entry[1]:
            lock.parent.mkdir(parents=True, exist_ok=True)
            entry[2] = os.open(lock, os.O_CREAT | os.O_WRONLY)
            fcntl.flock(entry[2], fcntl.LOCK_EX)
        entry[1] += 1
        try:
            yield
        finally:
            entry[1] -= 1
            if not entry[1]:
                os.close(entry[2])  # closing releases the flock


def write_text(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    tmp.replace(path)


def write_json(path, data):
    """Indented, UTF-8 as written, trailing newline: the format of every authoring JSON file."""
    write_text(path, json.dumps(data, ensure_ascii=False, indent=2) + "\n")
