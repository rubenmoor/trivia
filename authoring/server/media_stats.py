"""GET /api/stats/media: approved questions per media role and per image resolution (RV-23).
Pixel sizes come from the cached files (D-17); headers only, standard library only."""
import struct
from collections import Counter

import media_cache  # app/server/media_cache.py

# Bands on the long edge, in px: (lower bound, label).
BANDS = [(3840, "≥ 3840"), (1920, "1920–3839"), (1280, "1280–1919"), (800, "800–1279"), (0, "< 800")]
OTHER = ["SVG", "not cached", "unreadable"]


def image_size(path):
    """(width, height) from a PNG, GIF, JPEG or WebP header; None if unknown."""
    with open(path, "rb") as f:
        head = f.read(32)
        if head[:8] == b"\x89PNG\r\n\x1a\n":
            return struct.unpack(">II", head[16:24])
        if head[:6] in (b"GIF87a", b"GIF89a"):
            return struct.unpack("<HH", head[6:10])
        if head[:4] == b"RIFF" and head[8:12] == b"WEBP":
            kind = head[12:16]
            if kind == b"VP8X":
                return 1 + int.from_bytes(head[24:27], "little"), 1 + int.from_bytes(head[27:30], "little")
            if kind == b"VP8L":
                b = int.from_bytes(head[21:25], "little")
                return 1 + (b & 0x3FFF), 1 + ((b >> 14) & 0x3FFF)
            if kind == b"VP8 ":
                w, h = struct.unpack("<HH", head[26:30])
                return w & 0x3FFF, h & 0x3FFF
            return None
        if head[:2] == b"\xff\xd8":
            f.seek(2)
            while True:
                marker = f.read(2)
                if len(marker) < 2 or marker[0] != 0xFF:
                    return None
                while marker[1:] == b"\xff":  # fill bytes
                    marker = marker[:1] + f.read(1)
                if len(marker) < 2:
                    return None
                length = struct.unpack(">H", f.read(2))[0]
                if marker[1] in range(0xC0, 0xD0) and marker[1] not in (0xC4, 0xC8, 0xCC):
                    h, w = struct.unpack(">xHH", f.read(5))
                    return w, h
                f.seek(length - 2, 1)
    return None


def band(url):
    path = media_cache.cache_path(url)
    if path.suffix == ".svg":
        return "SVG", None
    if not path.is_file():
        return "not cached", None
    try:
        size = image_size(path)
    except (OSError, struct.error):
        size = None
    if not size:
        return "unreadable", None
    return next(label for low, label in BANDS if max(size) >= low), size


def build(questions):
    roles = {}
    bands, sizes = Counter(), Counter()
    for q in questions:
        m = q["media"]
        row = roles.setdefault(m["role"], Counter())
        row["questions"] += 1
        row[m["type"]] += 1
        row["no_file"] += not m.get("file_url")
        if m["type"] == "image" and m.get("file_url"):
            label, size = band(m["file_url"])
            bands[label] += 1
            if size:
                sizes[f"{size[0]}×{size[1]}"] += 1
    return {
        "questions": len(questions),
        "roles": [{"role": r, **c} for r, c in sorted(roles.items(), key=lambda rc: -rc[1]["questions"])],
        "bands": [{"band": label, "questions": bands[label]} for _, label in reversed(BANDS)]
                 + [{"band": label, "questions": bands[label]} for label in OTHER if bands[label]],
        "sizes": [{"size": s, "questions": n} for s, n in sizes.most_common(15)],
    }
