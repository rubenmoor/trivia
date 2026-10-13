"""Atomic writes for the authoring tools: `<name>.tmp` next to the file, then replace (a crash keeps the old file).
Callers that share a file across threads hold their own lock; across processes: none yet (task 740)."""
import json


def write_text(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    tmp.replace(path)


def write_json(path, data):
    """Indented, UTF-8 as written, trailing newline: the format of every authoring JSON file."""
    write_text(path, json.dumps(data, ensure_ascii=False, indent=2) + "\n")
