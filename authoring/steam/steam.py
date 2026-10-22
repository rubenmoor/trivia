#!/usr/bin/env python3
"""Steam uploads (plan 89, SW-10, D-93).

    trivia-steam vdf [--demo] [--out DIR] [--appid N --depots W,L,C[,DLC...]] [--tag T] [--preview]
    trivia-steam stage [--demo]
    trivia-steam upload [--demo] --branch beta [--preview | --dry-run] [--checked] [--skip STEP]... [--manual FILE]

`stage` checks the depot folders (`trivia-desktop-build --dir`) against the archives: per OS,
OS depot without resources/media plus the content depot at resources/media = the zip/tar.gz
(paths and sizes); exit 1 with the difference. It first stages each pack's DLC depot (decision 66,
steam.json `dlc`) into app/desktop/build/dlc/<id>/ (hard links): resources/data/bundles/<id>/ and the
pack's media from build/pack-media.json; the OS and content depots leave those out. A bundle ships as DLC
only with a pool and real IDs in steam.json `dlc` (`packs()`); the others are left out of the build, one
line each (`<id>: not shipped (no pool | no Steam IDs)`). Placeholder IDs (--depots, --dry-run) ship every bundle.

`vdf` renders app_build.vdf.in and depot_build.vdf.in with absolute paths into DIR
(default work/steam/<tag>/vdf): the windows and linux depots from app/desktop/release/
{win,linux}-unpacked/ without resources/media, the content depot from app/desktop/build/media/
installed at resources/media, one depot per pack from app/desktop/build/dlc/<id>/. IDs from steam.json
unless given (--depots: windows, linux, content, then the packs in steam.json order). SetLive is always `beta`.

`--demo` (plan 177, decision 342) is the same on the demo build: folders release/demo/{win,linux}-unpacked/ and
build/media-demo/, archives LivingRoomTriviaDemo-<v>-…, steam.json `demo` IDs, three depots, no DLC, output under
work/steam/<tag>/demo/. `stage --demo` also fails if resources/data/ holds bundles/ or a full base pool.

`upload` (SW-10): gates (branch `beta` only; clean tree; tag v<version> on HEAD unless --preview/--dry-run;
steam.json IDs, placeholders with --dry-run) → trivia-release-check (--skip tag with --preview/--dry-run; or --checked: its passing
release-check.json of this commit) → stage → VDFs in work/steam/<tag>/vdf → steamcmd +login
$TRIVIA_STEAM_ACCOUNT +run_app_build. --dry-run stops before SteamCMD. The password and Steam Guard
code are only typed into SteamCMD. Desc: `<tag> <sha>` plus `skipped: <steps>`.
`upload --demo` (plan 177, decision 342): the same on the demo app: steam.json `demo` IDs (placeholders 480, 481… with
--dry-run), `trivia-release-check --demo` (or --checked: work/steam/<tag>/demo/release-check.json), `stage --demo`, VDFs and
output in work/steam/<tag>/demo/; Desc `<tag> <sha> demo` plus skips. Same tag as the full build.
"""
import argparse, json, os, re, shutil, subprocess, sys, tarfile, zipfile
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
DEMO_DEPOTS = {
    "windows": (DESKTOP / "release" / "demo" / "win-unpacked", ".", True),
    "linux": (DESKTOP / "release" / "demo" / "linux-unpacked", ".", True),
    "content": (DESKTOP / "build" / "media-demo", "resources/media", False),
}
EXCLUDE = ["*.pdb", "steam_appid.txt"]
EXCLUDE_OS = ["resources/media/*"]
DLC = DESKTOP / "build" / "dlc"
DRY_RUN_APPID = 480  # Spacewar, for --dry-run without steam.json IDs; depots 481…


def conf() -> dict:
    return json.loads((HERE / "steam.json").read_text())


SHIP_ALL = False  # placeholder IDs (--depots, --dry-run): every bundle gets a depot


def bundles() -> list[str]:
    return sorted(d.name for d in (REPO / "app" / "data" / "bundles").iterdir() if d.is_dir())


def has_pool(bundle: str) -> bool:
    """A pool file makes a pack offered (decision 112: missing = not offered)."""
    return any(re.fullmatch(r"pool(\.[\w-]+)?\.json", f.name) for f in (REPO / "app" / "data" / "bundles" / bundle).iterdir())


def packs(demo: bool = False) -> list[str]:
    """Bundles shipped as DLC (decision 66): a pool and real IDs in steam.json `dlc`; none in the demo."""
    if demo:
        return []
    if SHIP_ALL:
        return bundles()
    dlc = conf()["dlc"]
    return [b for b in bundles() if has_pool(b) and all((dlc.get(b) or {}).values()) and b in dlc]


def left_out(demo: bool = False) -> list[str]:
    """Bundles in the build that don't ship: one line each, printed by stage."""
    if demo:
        return []
    shipped = packs()
    return [f"{b}: not shipped ({'no pool' if not has_pool(b) else 'no Steam IDs'})" for b in bundles() if b not in shipped]


def pack_media() -> dict[str, list[str]]:
    f = DESKTOP / "build" / "pack-media.json"
    if not f.is_file():
        sys.exit(f"trivia-steam: missing {f} (run trivia-desktop-build --dir)")
    return json.loads(f.read_text())


def pack_data(pack: str) -> str:
    return f"resources/data/bundles/{pack}/"


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=REPO, capture_output=True, text=True).stdout.strip()


def head_tag() -> str:
    """`v<version>` on HEAD (else another v* tag there), else the short sha."""
    tags, want = git("tag", "--points-at", "HEAD").split(), f"v{version()}"
    return want if want in tags else next((t for t in tags if t.startswith("v")), None) or git("rev-parse", "--short", "HEAD")


def ids(args) -> tuple[int, dict[str, int]]:
    """App ID and {depot name: ID}: windows, linux, content, then one per pack."""
    global SHIP_ALL
    demo = getattr(args, "demo", False)
    SHIP_ALL = SHIP_ALL or bool(args.depots)
    c = conf()["demo"] if demo else conf()
    names = [*DEPOTS, *packs(demo)]
    appid = args.appid or c["appid"]
    if args.depots:
        depots = dict(zip(names, (int(d) for d in args.depots.split(","))))
    else:
        depots = c["depots"] | ({} if demo else {p: c["dlc"][p]["depot"] for p in names[len(DEPOTS):]})
    missing = [k for k, v in [("appid", appid), *depots.items()] if not v]
    if missing or len(depots) != len(names):
        sys.exit(f"trivia-steam: no ID for {', '.join(missing) or 'all depots'} (steam.json or --appid/--depots {','.join(names)})")
    return int(appid), {k: int(v) for k, v in depots.items()}


def render(out: Path, appid: int, depots: dict[str, int], tag: str, desc: str, preview: bool, demo: bool = False) -> Path:
    """Write the app VDF and one depot VDF per depot into out; returns the app VDF."""
    out.mkdir(parents=True, exist_ok=True)
    depot_t = Template((HERE / "depot_build.vdf.in").read_text())
    lines = []
    media = {} if demo else pack_media()
    roots = (DEMO_DEPOTS if demo else DEPOTS) | {p: (DLC / p, ".", False) for p in packs(demo)}
    every = [] if demo else bundles()  # left-out bundles leave the OS and content depots too
    for name, (root, path, is_os) in roots.items():
        excl = EXCLUDE + ([*EXCLUDE_OS, *(pack_data(p) + "*" for p in every)] if is_os else [])
        if name == "content":
            excl += [f for p in every for f in media.get(p, [])]
        vdf = out / f"depot_build_{name}.vdf"
        vdf.write_text(depot_t.substitute(
            depotid=depots[name], content_root=root, depot_path=path,
            exclusions="\n".join(f'\t"FileExclusion" "{e}"' for e in excl)))
        lines.append(f'\t\t"{depots[name]}" "{vdf}"')
    app = out / "app_build.vdf"
    app.write_text(Template((HERE / "app_build.vdf.in").read_text()).substitute(
        appid=appid, desc=desc.replace('"', "'"), preview=int(preview), content_root=DESKTOP,
        build_output=REPO / "work" / "steam" / tag / ("demo" if demo else "") / "output", depots="\n".join(lines)))
    return app


def cmd_vdf(args) -> None:
    appid, depots = ids(args)
    tag = args.tag or head_tag()
    out = Path(args.out).resolve() if args.out else REPO / "work" / "steam" / tag / ("demo" if args.demo else "") / "vdf"
    sha = git("rev-parse", "--short", "HEAD")
    desc = (tag if tag == sha else f"{tag} {sha}") + (" demo" if args.demo else "")
    app = render(out, appid, depots, tag, desc, args.preview, args.demo)
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


def link(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    try:
        os.link(src, dst)
    except OSError:
        shutil.copy2(src, dst)


def stage_dlc(linux: Path, media_root: Path) -> dict[str, dict[str, int]]:
    """Each pack's depot folder in build/dlc/<id>/ (hard links); {pack: tree}."""
    shipped = {p.name for p in (linux / "resources" / "data" / "bundles").iterdir() if p.is_dir()}
    media = pack_media()
    ids = {b for b, d in conf()["dlc"].items() if all(d.values())}
    if shipped != set(bundles()) or set(media) != shipped or not set(packs()) <= shipped or not (SHIP_ALL or ids <= shipped):
        sys.exit(f"trivia-steam stage: bundles in the build {sorted(shipped)}, build/pack-media.json {sorted(media)},"
                 f" app/data/bundles {bundles()}, steam.json dlc with IDs {sorted(ids)}: they must agree (decision 66)")
    for line in left_out():
        print(f"  {line}")
    shutil.rmtree(DLC, ignore_errors=True)
    trees = {}
    for p in packs():
        root = DLC / p
        for rel in tree(linux / pack_data(p), pack_data(p)):
            link(linux / rel, root / rel)
        for f in media[p]:
            if not (media_root / f).is_file():
                sys.exit(f"trivia-steam stage: {p}: media {f} not in {media_root}")
            link(media_root / f, root / "resources" / "media" / f)
        trees[p] = tree(root)
    return trees


def check_demo_data(unpacked: Path) -> None:
    """The demo ships no bundles/ and no full base pool (decision 342)."""
    data = unpacked / "resources" / "data"
    bad = [p.name for p in data.iterdir() if p.name == "bundles" or re.fullmatch(r"pool(\.[\w-]+)?\.json", p.name)]
    if bad:
        sys.exit(f"trivia-steam stage --demo: {data} holds {', '.join(sorted(bad))}: the demo ships only demo/ pools")


def stage(demo: bool = False) -> bool:
    depots = DEMO_DEPOTS if demo else DEPOTS
    release = DESKTOP / "release" / ("demo" if demo else "")
    arc_name = "LivingRoomTriviaDemo" if demo else "LivingRoomTrivia"
    content_root, content_path, _ = depots["content"]
    bad = [str(d) for d in (depots["windows"][0], depots["linux"][0], content_root) if not d.is_dir()]
    if bad:
        sys.exit(f"trivia-steam stage: missing {', '.join(bad)} (run trivia-desktop-build{' --demo' if demo else ''} --dir)")
    if demo:
        check_demo_data(depots["linux"][0])
        check_demo_data(depots["windows"][0])
        dlc = {}
    else:
        dlc = stage_dlc(depots["linux"][0], content_root)
    out_media = {} if demo else pack_media()
    pack_files = {f"{content_path}/{f}" for p in out_media for f in out_media[p]}
    content = {k: v for k, v in tree(content_root, content_path + "/").items() if k not in pack_files}
    dlc_all = {k: v for t in dlc.values() for k, v in t.items()}
    for p, t in dlc.items():
        print(f"  {p}: DLC depot {len(t)} files")
    left = sorted(set(bundles()) - set(packs(demo))) if not demo else []
    ok = True
    for name, ext in [("windows", "win-x64.zip"), ("linux", "linux-x64.tar.gz")]:
        arc = release / f"{arc_name}-{version()}-{ext}"
        if not arc.is_file():
            sys.exit(f"trivia-steam stage: missing {arc} (run trivia-desktop-build{' --demo' if demo else ''} --dir)")
        own = (content_path + "/", *(pack_data(p) for p in ([] if demo else bundles())))
        depot = {k: v for k, v in tree(depots[name][0]).items() if not k.startswith(own)}
        gone = tuple(pack_data(p) for p in left) + tuple(f"{content_path}/{f}" for p in left for f in out_media[p])
        want, got = {k: v for k, v in archive(arc).items() if not k.startswith(gone)}, depot | content | dlc_all
        diff = sorted(set(want) ^ set(got)) + sorted(k for k in set(want) & set(got) if want[k] != got[k])
        for k in diff[:20]:
            print(f"  {name}: {k}: archive {want.get(k, '-')}, depots {got.get(k, '-')}")
        print(f"{'✓' if not diff else '✗'} {name}: {len(depot)} files + {len(content)} content + {len(dlc_all)} DLC"
              + (f", {len(diff)} differ from {arc.name}" if diff else f" = {arc.name}"))
        ok = ok and not diff
    return ok


def cmd_stage(args) -> None:
    sys.exit(0 if stage(args.demo) else 1)


def checked(commit: str, tag: str, demo: bool = False) -> dict:
    """The release check's report of this commit, if it passed on a clean tree."""
    f = REPO / "work" / "steam" / tag / ("demo" if demo else "") / "release-check.json"
    r = json.loads(f.read_text()) if f.is_file() else {}
    if r.get("commit") != commit or not r.get("ok") or not r.get("clean"):
        sys.exit(f"trivia-steam upload: no passing release check of {commit[:7]} on a clean tree in {f.relative_to(REPO)}")
    return r


def cmd_upload(args) -> None:
    def gate(ok: bool, why: str) -> None:
        if not ok:
            sys.exit(f"trivia-steam upload: {why}")

    demo = args.demo
    gate(args.branch == "beta", f"branch {args.branch!r} refused: only beta; default is set in the Steamworks web UI (D-93)")
    gate(not git("status", "--porcelain"), "uncommitted changes (git status --porcelain)")
    commit, sha, tag = git("rev-parse", "HEAD"), git("rev-parse", "--short", "HEAD"), head_tag()
    want = f"v{version()}"
    if not (args.preview or args.dry_run):
        gate(tag == want, f"HEAD has no tag {want} (tag it yourself; this command never tags)")
    if args.dry_run and not args.appid and not args.depots:
        c = conf()["demo"] if demo else conf()
        if not c["appid"] or not all(c["depots"].values()) or left_out(demo):
            global SHIP_ALL
            SHIP_ALL = True
            args.appid = DRY_RUN_APPID
            args.depots = ",".join(str(DRY_RUN_APPID + 1 + i) for i in range(len(DEPOTS) + len(packs(demo))))
            print(f"dry run: placeholder IDs {args.appid}, {args.depots}")
    appid, depots = ids(args)

    if args.checked:
        report = checked(commit, tag, demo)
    else:
        skip = [*args.skip, *(["tag"] if args.preview or args.dry_run else [])]
        cmd = [sys.executable, str(HERE / "release_check.py"), *(["--demo"] if demo else []), *(a for s in dict.fromkeys(skip) for a in ("--skip", s))]
        if args.manual:
            cmd += ["--manual", args.manual]
        gate(subprocess.run(cmd, cwd=REPO).returncode == 0, "release check failed")
        gate(not git("status", "--porcelain"), "the release check changed tracked files (git status --porcelain)")
        report = checked(commit, tag, demo)
    gate(stage(demo), "depot folders differ from the archives")

    out = REPO / "work" / "steam" / tag / ("demo" if demo else "")
    desc = (tag if tag == sha else f"{tag} {sha}") + (" demo" if demo else "") + (f" skipped: {', '.join(report['skipped'])}" if report["skipped"] else "")
    app = render(out / "vdf", appid, depots, tag, desc, args.preview, demo)
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
    v.add_argument("--demo", action="store_true", help="the demo app: steam.json demo, release/demo/, build/media-demo/, no DLC")
    v.add_argument("--out", help="output dir (default work/steam/<tag>/vdf)")
    v.add_argument("--appid", type=int, help="App ID (default steam.json)")
    v.add_argument("--depots", help="depot IDs windows,linux,content,<packs> (default steam.json)")
    v.add_argument("--tag", help="default: v<version> on HEAD, else the short sha")
    v.add_argument("--preview", action="store_true", help="Preview 1: manifests only, no upload")
    v.set_defaults(fn=cmd_vdf)
    st = sub.add_parser("stage", help="check the depot folders against the archives")
    st.add_argument("--demo", action="store_true", help="the demo build (release/demo/, build/media-demo/, no DLC)")
    st.set_defaults(fn=cmd_stage)
    u = sub.add_parser("upload", help="release check, stage, VDFs, steamcmd run_app_build")
    u.add_argument("--demo", action="store_true", help="the demo app and build (steam.json demo, release check --demo)")
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
