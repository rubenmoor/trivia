#!/usr/bin/env python3
"""Steam uploads (plan 89, SW-10, D-93).

    trivia-steam vdf [--out DIR] [--appid N --depots W,L,C] [--tag T] [--preview]
    trivia-steam stage

`stage` checks the depot folders (`trivia-desktop-build --dir`) against the archives: per OS,
OS depot without resources/media plus the content depot at resources/media = the zip/tar.gz
(paths and sizes); exit 1 with the difference.

`vdf` renders app_build.vdf.in and depot_build.vdf.in with absolute paths into DIR
(default work/steam/<tag>/vdf): the windows and linux depots from app/desktop/release/
{win,linux}-unpacked/ without resources/media, the content depot from app/desktop/build/media/
installed at resources/media. IDs from steam.json unless given. SetLive is always `beta`.
"""
import argparse, json, subprocess, sys, tarfile, zipfile
from pathlib import Path
from string import Template

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
DESKTOP = REPO / "app" / "desktop"
# Depot name → (content root, install path, OS depot?).
DEPOTS = {
    "windows": (DESKTOP / "release" / "win-unpacked", ".", True),
    "linux": (DESKTOP / "release" / "linux-unpacked", ".", True),
    "content": (DESKTOP / "build" / "media", "resources/media", False),
}
EXCLUDE = ["*.pdb", "steam_appid.txt"]
EXCLUDE_OS = ["resources/media/*"]


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=REPO, capture_output=True, text=True).stdout.strip()


def head_tag() -> str:
    """`v<version>` on HEAD, else the short sha."""
    tags = git("tag", "--points-at", "HEAD").split()
    return next((t for t in tags if t.startswith("v")), None) or git("rev-parse", "--short", "HEAD")


def ids(args) -> tuple[int, dict[str, int]]:
    conf = json.loads((HERE / "steam.json").read_text())
    appid = args.appid or conf["appid"]
    depots = dict(zip(DEPOTS, (int(d) for d in args.depots.split(",")))) if args.depots else conf["depots"]
    missing = [k for k, v in [("appid", appid), *depots.items()] if not v]
    if missing or len(depots) != len(DEPOTS):
        sys.exit(f"trivia-steam: no ID for {', '.join(missing) or 'all depots'} (steam.json or --appid/--depots W,L,C)")
    return int(appid), {k: int(v) for k, v in depots.items()}


def render(out: Path, appid: int, depots: dict[str, int], tag: str, desc: str, preview: bool) -> Path:
    """Write the app VDF and one depot VDF per depot into out; returns the app VDF."""
    out.mkdir(parents=True, exist_ok=True)
    depot_t = Template((HERE / "depot_build.vdf.in").read_text())
    lines = []
    for name, (root, path, is_os) in DEPOTS.items():
        excl = EXCLUDE + (EXCLUDE_OS if is_os else [])
        vdf = out / f"depot_build_{name}.vdf"
        vdf.write_text(depot_t.substitute(
            depotid=depots[name], content_root=root, depot_path=path,
            exclusions="\n".join(f'\t"FileExclusion" "{e}"' for e in excl)))
        lines.append(f'\t\t"{depots[name]}" "{vdf}"')
    app = out / "app_build.vdf"
    app.write_text(Template((HERE / "app_build.vdf.in").read_text()).substitute(
        appid=appid, desc=desc.replace('"', "'"), preview=int(preview), content_root=DESKTOP,
        build_output=REPO / "work" / "steam" / tag / "output", depots="\n".join(lines)))
    return app


def cmd_vdf(args) -> None:
    appid, depots = ids(args)
    tag = args.tag or head_tag()
    out = Path(args.out).resolve() if args.out else REPO / "work" / "steam" / tag / "vdf"
    sha = git("rev-parse", "--short", "HEAD")
    app = render(out, appid, depots, tag, tag if tag == sha else f"{tag} {sha}", args.preview)
    print(app)


def tree(root: Path, prefix: str = "") -> dict[str, int]:
    return {prefix + p.relative_to(root).as_posix(): p.stat().st_size
            for p in root.rglob("*") if p.is_file() and not p.is_symlink()}


def archive(path: Path) -> dict[str, int]:
    """Files in a release archive (path → size), without the tar.gz's top folder."""
    if path.suffix == ".zip":
        with zipfile.ZipFile(path) as z:
            return {i.filename: i.file_size for i in z.infolist() if not i.is_dir()}
    with tarfile.open(path) as t:
        return {m.name.split("/", 1)[1]: m.size for m in t if m.isfile()}


def cmd_stage(args) -> None:
    version = json.loads((DESKTOP / "package.json").read_text())["version"]
    release = DESKTOP / "release"
    content_root, content_path, _ = DEPOTS["content"]
    bad = [str(d) for d in (DEPOTS["windows"][0], DEPOTS["linux"][0], content_root) if not d.is_dir()]
    if bad:
        sys.exit(f"trivia-steam stage: missing {', '.join(bad)} (run trivia-desktop-build --dir)")
    content = tree(content_root, content_path + "/")
    ok = True
    for name, ext in [("windows", "win-x64.zip"), ("linux", "linux-x64.tar.gz")]:
        arc = release / f"Trivia-{version}-{ext}"
        if not arc.is_file():
            sys.exit(f"trivia-steam stage: missing {arc} (run trivia-desktop-build --dir)")
        depot = {k: v for k, v in tree(DEPOTS[name][0]).items() if not k.startswith(content_path + "/")}
        want, got = archive(arc), depot | content
        diff = sorted(set(want) ^ set(got)) + sorted(k for k in set(want) & set(got) if want[k] != got[k])
        for k in diff[:20]:
            print(f"  {name}: {k}: archive {want.get(k, '-')}, depots {got.get(k, '-')}")
        print(f"{'✓' if not diff else '✗'} {name}: {len(depot)} files + {len(content)} content"
              + (f", {len(diff)} differ from {arc.name}" if diff else f" = {arc.name}"))
        ok = ok and not diff
    sys.exit(0 if ok else 1)


def main() -> None:
    p = argparse.ArgumentParser(prog="trivia-steam", description=__doc__.split("\n")[0])
    sub = p.add_subparsers(dest="cmd", required=True)
    v = sub.add_parser("vdf", help="render the build VDFs")
    v.add_argument("--out", help="output dir (default work/steam/<tag>/vdf)")
    v.add_argument("--appid", type=int, help="App ID (default steam.json)")
    v.add_argument("--depots", help="depot IDs windows,linux,content (default steam.json)")
    v.add_argument("--tag", help="default: v<version> on HEAD, else the short sha")
    v.add_argument("--preview", action="store_true", help="Preview 1: manifests only, no upload")
    v.set_defaults(fn=cmd_vdf)
    sub.add_parser("stage", help="check the depot folders against the archives").set_defaults(fn=cmd_stage)
    args = p.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
