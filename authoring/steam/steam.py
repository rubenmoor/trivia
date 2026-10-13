#!/usr/bin/env python3
"""Steam uploads (plan 89, SW-10, D-93).

    trivia-steam vdf [--out DIR] [--appid N --depots W,L,C] [--tag T] [--preview]
    trivia-steam stage
    trivia-steam upload --branch beta [--preview | --dry-run] [--checked] [--skip STEP]... [--manual FILE]

`stage` checks the depot folders (`trivia-desktop-build --dir`) against the archives: per OS,
OS depot without resources/media plus the content depot at resources/media = the zip/tar.gz
(paths and sizes); exit 1 with the difference.

`vdf` renders app_build.vdf.in and depot_build.vdf.in with absolute paths into DIR
(default work/steam/<tag>/vdf): the windows and linux depots from app/desktop/release/
{win,linux}-unpacked/ without resources/media, the content depot from app/desktop/build/media/
installed at resources/media. IDs from steam.json unless given. SetLive is always `beta`.

`upload` (SW-10): gates (branch `beta` only; clean tree; tag v<version> on HEAD unless --preview/--dry-run;
steam.json IDs, placeholders with --dry-run) → trivia-release-check (--skip tag with --preview/--dry-run; or --checked: its passing
release-check.json of this commit) → stage → VDFs in work/steam/<tag>/vdf → steamcmd +login
$TRIVIA_STEAM_ACCOUNT +run_app_build. --dry-run stops before SteamCMD. The password and Steam Guard
code are only typed into SteamCMD. Desc: `<tag> <sha>` plus `skipped: <steps>`.
"""
import argparse, json, os, re, subprocess, sys, tarfile, zipfile
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
DRY_RUN_IDS = (480, "481,482,483")  # Spacewar, for --dry-run without steam.json IDs


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=REPO, capture_output=True, text=True).stdout.strip()


def head_tag() -> str:
    """`v<version>` on HEAD (else another v* tag there), else the short sha."""
    tags, want = git("tag", "--points-at", "HEAD").split(), f"v{version()}"
    return want if want in tags else next((t for t in tags if t.startswith("v")), None) or git("rev-parse", "--short", "HEAD")


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


def version() -> str:
    return json.loads((DESKTOP / "package.json").read_text())["version"]


def stage() -> bool:
    release = DESKTOP / "release"
    content_root, content_path, _ = DEPOTS["content"]
    bad = [str(d) for d in (DEPOTS["windows"][0], DEPOTS["linux"][0], content_root) if not d.is_dir()]
    if bad:
        sys.exit(f"trivia-steam stage: missing {', '.join(bad)} (run trivia-desktop-build --dir)")
    content = tree(content_root, content_path + "/")
    ok = True
    for name, ext in [("windows", "win-x64.zip"), ("linux", "linux-x64.tar.gz")]:
        arc = release / f"Trivia-{version()}-{ext}"
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
    return ok


def cmd_stage(args) -> None:
    sys.exit(0 if stage() else 1)


def checked(commit: str, tag: str) -> dict:
    """The release check's report of this commit, if it passed on a clean tree."""
    f = REPO / "work" / "steam" / tag / "release-check.json"
    r = json.loads(f.read_text()) if f.is_file() else {}
    if r.get("commit") != commit or not r.get("ok") or not r.get("clean"):
        sys.exit(f"trivia-steam upload: no passing release check of {commit[:7]} on a clean tree in {f.relative_to(REPO)}")
    return r


def cmd_upload(args) -> None:
    def gate(ok: bool, why: str) -> None:
        if not ok:
            sys.exit(f"trivia-steam upload: {why}")

    gate(args.branch == "beta", f"branch {args.branch!r} refused: only beta; default is set in the Steamworks web UI (D-93)")
    gate(not git("status", "--porcelain"), "uncommitted changes (git status --porcelain)")
    commit, sha, tag = git("rev-parse", "HEAD"), git("rev-parse", "--short", "HEAD"), head_tag()
    want = f"v{version()}"
    if not (args.preview or args.dry_run):
        gate(tag == want, f"HEAD has no tag {want} (tag it yourself; this command never tags)")
    if args.dry_run and not args.appid and not args.depots:
        conf = json.loads((HERE / "steam.json").read_text())
        if not conf["appid"] or not all(conf["depots"].values()):
            args.appid, args.depots = DRY_RUN_IDS
            print(f"dry run: placeholder IDs {args.appid}, {args.depots}")
    appid, depots = ids(args)

    if args.checked:
        report = checked(commit, tag)
    else:
        skip = [*args.skip, *(["tag"] if args.preview or args.dry_run else [])]
        cmd = [sys.executable, str(HERE / "release_check.py"), *(a for s in dict.fromkeys(skip) for a in ("--skip", s))]
        if args.manual:
            cmd += ["--manual", args.manual]
        gate(subprocess.run(cmd, cwd=REPO).returncode == 0, "release check failed")
        gate(not git("status", "--porcelain"), "the release check changed tracked files (git status --porcelain)")
        report = checked(commit, tag)
    gate(stage(), "depot folders differ from the archives")

    out = REPO / "work" / "steam" / tag
    desc = (tag if tag == sha else f"{tag} {sha}") + (f" skipped: {', '.join(report['skipped'])}" if report["skipped"] else "")
    app = render(out / "vdf", appid, depots, tag, desc, args.preview)
    print(f"VDFs: {app.parent}\nDesc: {desc}")
    if args.dry_run:
        print("dry run: SteamCMD not started")
        return

    account = os.environ.get("TRIVIA_STEAM_ACCOUNT") or input("Steam build account: ").strip()
    gate(bool(account), "no account (TRIVIA_STEAM_ACCOUNT)")
    log = out / "steamcmd.log"
    p = subprocess.Popen(["steamcmd", "+login", account, "+run_app_build", str(app), "+quit"], stdout=subprocess.PIPE)
    # Raw chunks: SteamCMD's password/Steam Guard prompts end without a newline.
    with log.open("wb") as f:
        while chunk := os.read(p.stdout.fileno(), 4096):
            sys.stdout.buffer.write(chunk)
            sys.stdout.flush()
            f.write(chunk)
    rc = p.wait()
    build = re.findall(r"BuildID (\d+)", log.read_text(errors="replace"))
    print(f"SteamCMD log: {log}\nBuild output: {out / 'output'}")
    gate(rc == 0 and bool(build), f"SteamCMD exit {rc}{'' if build else ', no BuildID'}")
    print(f"BuildID {build[-1]}{' (preview, nothing uploaded)' if args.preview else ' → branch beta'}")


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
    u = sub.add_parser("upload", help="release check, stage, VDFs, steamcmd run_app_build")
    u.add_argument("--branch", required=True, help="beta (the only branch set from here)")
    m = u.add_mutually_exclusive_group()
    m.add_argument("--preview", action="store_true", help="Preview 1: manifests only, no upload")
    m.add_argument("--dry-run", action="store_true", help="no SteamCMD; placeholder IDs if steam.json has none")
    u.add_argument("--checked", action="store_true", help="reuse this commit's passing release-check.json")
    u.add_argument("--skip", action="append", default=[], help="passed to trivia-release-check")
    u.add_argument("--manual", metavar="FILE", help="passed to trivia-release-check")
    u.add_argument("--appid", type=int, help=argparse.SUPPRESS)
    u.add_argument("--depots", help=argparse.SUPPRESS)
    u.set_defaults(fn=cmd_upload)
    args = p.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
