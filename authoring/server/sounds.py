"""Audition candidates for /sounds (plan 220): work/sound-brief/manifest.json and its files. Format: plans/25-sound.md "Manifest"."""
import json

import layout  # authoring/tools/layout.py


def load():
    """GET /api/sounds: the manifest's entries, or None before there is a manifest."""
    path = layout.SOUND_BRIEF / "manifest.json"
    if not path.is_file():
        return None
    entries = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(entries, list):
        raise ValueError("work/sound-brief/manifest.json must be a list")
    return entries


def file_path(rel):
    """A file under work/sound-brief/, or None for a missing file or a path outside it."""
    root = layout.SOUND_BRIEF.resolve()
    path = (root / rel).resolve()
    return path if path.is_relative_to(root) and path.is_file() else None
