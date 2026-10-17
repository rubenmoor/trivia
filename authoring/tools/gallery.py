#!/usr/bin/env python3
"""trivia-gallery (plan 100, decision 115): every screen and dialog in every UI language, with each text's catalog key.

The built client on the Node dev server (`npm run serve -w app/client`, a temp save dir, never state/), driven by
nixpkgs Playwright (1920×1080, `--size WxH`) with the desktop bridge stubbed (valid Steam user, mods, telemetry, reports).
`?gallery` makes `t()` record rendered text → key (lib/i18n.ts); each shot's visible texts are matched against it.
Output: <locale>/<shot>.png and manifest.json in work/gallery/ ($TRIVIA_WORK/gallery/ if set; merged on --locale/--only runs);
with `TRIVIA_DEMO=1` the demo client (dist-demo) is shot into work/gallery-demo/;
another size writes <locale>@<W>x<H>/ and a manifest entry of that name.
Review set (task 1581): `--set task-<id> --only …` shoots into sets/<name>/<entry>/ and sets/<name>.json (the manifest's
shape plus name, note, shots; overwritten), for /gallery?set=<name>; the full gallery stays untouched.

Usage: trivia-gallery [--locale en,es,es-ES,de] [--only <shot>[,<shot>…]] [--size WxH[,WxH…]] [--list] [--visible]
       trivia-gallery --set task-<id> --only <shot>[,<shot>…] [--note <text>] [--locale …] [--size …]
"""
import argparse
import datetime
import json
import os
import re
import shutil
import signal
import socket
import subprocess
import sys
import tempfile
import time
import urllib.request
from pathlib import Path

import layout  # authoring/tools/layout.py

REPO = Path(__file__).resolve().parent.parent.parent
CLIENT = REPO / "app" / "client"
DATA = REPO / "app" / "data"
DEMO = os.environ.get("TRIVIA_DEMO") == "1"  # plan 173: the demo client, dist-demo
DIST = "dist-demo" if DEMO else "dist"
OUT = layout.GALLERY.with_name("gallery-demo") if DEMO else layout.GALLERY  # honours TRIVIA_WORK
LOCALES = ["en", "es", "es-ES", "de"]
DEFAULT_SIZE = (1920, 1080)

# Sample mods (plan 118): every kind, state and warning the Mods screen shows; ~20 rows.
LONG = ("Preguntas de la abuela: historia, cocina y refranes de toda la vida, con fotos del álbum familiar "
        "y una categoría extra de canciones de cuna")


def mod(i, **kw):
    row = {
        "id": f"mod-{i}", "name": f"Sample mod {i}", "version": "1.0.0", "game": None, "description": None,
        "source": "workshop", "publishedFileId": f"33000000{i:02d}", "kind": ["bundle"], "languages": [],
        "on": False, "active": False, "position": i, "state": "off", "warnings": [], "error": None, "dir": None,
    }
    row.update(kw)
    return row


def sample_mods():
    on = {"on": True, "active": True, "state": "loaded"}
    rows = [
        mod(0, name=LONG, description=LONG + ". " + LONG + ".", source="local", publishedFileId=None, dir="abuela",
            languages=["es", "en"], **on),
        mod(1, name="Neon Theme", kind=["theme"], **on),
        mod(2, name="Party Timer", kind=["code"], warnings=["needs_update"], **on),
        mod(3, name="Space Trivia", kind=["conversion"], warnings=["workshop_id_mismatch"], languages=["de"]),
        mod(4, name="Old Mod", game="0.9.0", warnings=["game_version", "unknown_key"], kind=["bundle", "theme"]),
        mod(5, name="Turned On", on=True, active=False, state="loaded"),
        mod(6, name="Turned Off", on=False, active=True, state="off"),
        mod(7, id=None, name=None, version=None, position=None, state="invalid", source="local",
            publishedFileId=None, dir="broken-mod", error={"code": "bad_field", "field": "kind"}),
        mod(8, id=None, name=None, version=None, kind=[], position=None, state="downloading"),
        mod(9, name="Hidden by Steam", state="disabled", position=None),
    ]
    rows += [mod(i, name=f"Quiz Pack {i}", languages=["en"]) for i in range(10, 21)]
    return rows


# Shell stub (init script): the dev shim's save methods win, everything else is ours (no `devServer`: quit shows).
STUB = """
(() => {
  const cfg = __CFG__;
  const no = (v) => () => Promise.resolve(v);
  let telemetry = { available: true, consent: cfg.consent };
  const list = cfg.mods;
  const copy = () => Promise.resolve(structuredClone(list));
  const stub = {
    desktop: true,
    muted: true,
    toggleFullscreen: no(undefined),
    quit: no(undefined),
    loadSave: no(null),
    writeSave: no(undefined),
    backupSave: no(""),
    steam: {
      available: true, user: true, dev: true,
      steamId: no("76561190000000001"), language: no(null), overlay: { enabled: no(true) },
      showTextInput: no(false), inputTypes: no(null), setPresence: no(undefined), unlock: no(true),
    },
    telemetry: {
      state: () => Promise.resolve({ ...telemetry }),
      setConsent: (yes) => ((telemetry = { ...telemetry, consent: yes }), Promise.resolve({ ...telemetry })),
      load: no(null),
      record: no(undefined),
    },
    report: { available: no(true), send: no({ ok: true, id: 1 }) },
    mods: list && {
      list: copy,
      set: (order) => {
        for (const o of order) { const m = list.mods.find((x) => x.id === o.id); if (m) m.on = o.on; }
        return copy();
      },
      notice: () => ((list.notice = true), copy()),
      restart: () => new Promise(() => {}),
      ready: no(undefined),
    },
  };
  Object.defineProperty(window, "triviaShell", {
    get: () => stub,
    set: (shim) => Object.assign(stub, { loadSave: shim.loadSave, writeSave: shim.writeSave, backupSave: shim.backupSave }),
  });
  (__PADS__)(cfg.pads); // fake_pads.js
  // A running session's seats bound (lib/seats.svelte.ts `trivia.seats.<game id>`), so the game doesn't ask for pads.
  if (cfg.bound) sessionStorage.setItem(`trivia.seats.${cfg.bound.id}`, JSON.stringify(cfg.bound.binding));
})();
""".replace("__PADS__", (Path(__file__).parent / "fake_pads.js").read_text(encoding="utf-8"))

# Visible text nodes and aria-label/title/placeholder, on top (not under a dialog's backdrop), in the viewport.
TEXTS = """
() => {
  const norm = (s) => s.replace(/\\s+/g, " ").trim();
  const W = innerWidth, H = innerHeight;
  const box = (r) => [Math.round(r.left), Math.round(r.top), Math.round(r.width), Math.round(r.height)];
  const onTop = (el, r) => {
    const x = Math.min(Math.max(r.left + r.width / 2, 0), W - 1), y = Math.min(Math.max(r.top + r.height / 2, 0), H - 1);
    const hit = document.elementFromPoint(x, y);
    return !hit || hit === el || el.contains(hit) || hit.contains(el);
  };
  const shown = (el, r) => r.width > 0 && r.height > 0 && r.right > 0 && r.bottom > 0 && r.left < W && r.top < H
    && el.checkVisibility({ opacityProperty: true, visibilityProperty: true }) && onTop(el, r);
  const out = [];
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  for (let n; (n = walker.nextNode()); ) {
    const text = norm(n.data);
    const el = n.parentElement;
    if (!text || !el || el.closest("script, style, svg")) continue;
    const range = document.createRange();
    range.selectNodeContents(n);
    const r = range.getBoundingClientRect();
    if (shown(el, r)) out.push({ text, box: box(r), ...(el.closest("kbd") ? { kbd: true } : {}) });
  }
  for (const el of document.querySelectorAll("[aria-label], [title], [placeholder]")) {
    const r = el.getBoundingClientRect();
    if (!shown(el, r)) continue;
    for (const attr of ["aria-label", "title", "placeholder"]) {
      const v = norm(el.getAttribute(attr) ?? "");
      if (v && !out.some((o) => o.text === v && o.attr)) out.push({ text: v, box: box(r), attr });
    }
  }
  return { items: out, keys: window.__galleryKeys ?? {} };
}
"""

LETTER = re.compile(r"[^\W\d_]")


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def data_strings(players):
    """Content, not catalog: every string in app/data's JSON (questions, names) and the built credits, players, mods,
    endonyms, locale codes."""
    out = {*players, *LOCALES}

    def walk(v):
        if isinstance(v, str):
            out.add(norm(v))
        elif isinstance(v, dict):
            for x in v.values():
                walk(x)
        elif isinstance(v, list):
            for x in v:
                walk(x)

    for f in [*DATA.rglob("*.json"), CLIENT / DIST / "credits.json"]:
        walk(json.loads(f.read_text(encoding="utf-8")))
    walk(sample_mods())
    i18n = (CLIENT / "src" / "lib" / "i18n.ts").read_text(encoding="utf-8")
    block = re.search(r"const ENDONYMS[^{]*\{(.*?)\};", i18n, re.S)
    out.update(re.findall(r':\s*"([^"]+)"', block.group(1)) if block else [])
    return out


SEPARATOR = re.compile(r"\s*(?:·|:\s|,\s)\s*")


def spans(text):
    """Runs of separator-joined parts, longest first: content like a mod name may hold separators itself."""
    cuts = [0, *(x for m in SEPARATOR.finditer(text) for x in m.span()), len(text)]
    starts, ends = cuts[0::2], cuts[1::2]
    runs = {text[a:b] for i, a in enumerate(starts) for b in ends[i:]}
    return sorted((r for r in runs if r), key=len, reverse=True)


def match(items, keys, data):
    """Per item: `keys` (exact, else catalog texts inside it), `glyph` (key caps, answer letters), `data` (content),
    `unmatched` (the rest with letters: a literal, or a text the trace missed)."""
    index = {}
    for text, ks in keys.items():
        index.setdefault(norm(text), [])
        index[norm(text)] += [k for k in ks if k not in index[norm(text)]]
    parts = sorted((t for t in index if len(t) >= 2 and LETTER.search(t)), key=len, reverse=True)

    def inside(text, found):
        """Catalog texts inside `text` added to `found`; the rest."""
        for p in parts:
            if p in text:
                text, n = re.subn(rf"(?<!\w){re.escape(p)}(?!\w)", " ", text)
                if n:
                    found += [k for k in index[p] if k not in found]
        return norm(text)

    for it in items:
        text = it["text"]
        if text in index:
            it["keys"] = index[text]
        elif it.pop("kbd", False) or len(text) == 1:
            it["glyph"] = True
        elif text in data or re.fullmatch(r"PLACEHOLDER\(\d+\)", text):  # a PLACEHOLDER mark isn't catalog text
            it["data"] = True
        else:
            rest = text
            for seg in spans(text):
                if seg in data and LETTER.search(seg):
                    rest = rest.replace(seg, " ", 1)
            found = []
            left = [x.strip(" :·,.") for x in SEPARATOR.split(inside(rest, found))]
            left = [x for x in left if LETTER.search(x) and x not in data]
            if found:
                it["keys"] = found
            if left:
                it["unmatched"] = " … ".join(left)
            elif not found:
                it["data"] = True
    return items


def free_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def build_if_stale():
    dist = CLIENT / DIST / "index.html"
    inputs = [CLIENT / "index.html", CLIENT / "vite.config.ts", CLIENT / "credits.ts", REPO / "app" / "desktop" / "package.json",
              *(CLIENT / "src").rglob("*"), *(CLIENT / "public").rglob("*")]
    newest = max(f.stat().st_mtime for f in inputs if f.is_file())
    if dist.exists() and dist.stat().st_mtime >= newest:
        return
    print(f"gallery: client stale, npm run build ({DIST})", flush=True)
    subprocess.run(["npm", "run", "build", *(["-w", "app/client"] if DEMO else [])], cwd=REPO, check=True, stdout=subprocess.DEVNULL)


class Server:
    """`vite preview` with the dev server's plugin on a temp save dir; stopped by its process group (npm → sh → vite)."""

    def __init__(self):
        self.port = free_port()
        self.log = tempfile.TemporaryFile()
        self.save_dir = Path(tempfile.mkdtemp(prefix="trivia-gallery-"))
        env = {**os.environ, "TRIVIA_SAVE_DIR": str(self.save_dir), "TRIVIA_MUTE": "1"}
        self.proc = subprocess.Popen(["npm", "run", "serve", "-w", "app/client", "--", "--port", str(self.port)],
                                     cwd=REPO, env=env, stdout=self.log, stderr=subprocess.STDOUT, start_new_session=True)
        self.url = f"http://localhost:{self.port}"
        for _ in range(150):
            if self.proc.poll() is not None:
                break
            try:
                urllib.request.urlopen(self.url, timeout=1).close()
                return
            except OSError:
                time.sleep(0.2)
        self.stop()
        self.log.seek(0)
        sys.exit(f"gallery: dev server didn't start:\n{self.log.read().decode(errors='replace')}")

    def stop(self):
        if self.proc.poll() is None:
            os.killpg(self.proc.pid, signal.SIGTERM)
            self.proc.wait(10)
        shutil.rmtree(self.save_dir, ignore_errors=True)


class Run:
    """One UI language: scenes (a save, a stub config, a fresh page) and shots."""

    def __init__(self, browser, server, ui, size, demo, data, only, manifest, dest):
        self.browser, self.server, self.save, self.ui = browser, server, server.save_dir / "game.json", ui
        self.size = size
        self.name = ui if size == DEFAULT_SIZE else f"{ui}@{size[0]}x{size[1]}"  # directory and manifest key
        self.saves, self.meta, self.data, self.only = demo["saves"], demo["meta"], data, only
        self.shots = manifest.setdefault("locales", {}).setdefault(self.name, {})
        self.context = self.page = None
        self.dir = dest / self.name
        self.dir.mkdir(parents=True, exist_ok=True)

    def scene(self, save="base", *, raw=None, consent=False, mods="held", ready="main .start", pads=None, bound=False,
              at=None):
        """A fresh page on `save` (None: no save file). `mods`: a list config, or None (no mods bridge). `pads`: the
        connected pads' count (ids alternate Xbox, PlayStation); `bound`: the save's session seats bound to their devices;
        `at`: the page clock fixed at the save's `now` + `at` s (timers still run)."""
        if self.context:
            self.context.close()
        if raw is not None:
            self.save.write_text(raw)
        elif save is None:
            self.save.unlink(missing_ok=True)
        else:
            self.save.write_text(json.dumps(self.saves[save]))
        lists = {
            "held": {"mods": sample_mods(), "notice": False, "noMods": False, "safeStart": None, "validUser": True},
            "crashed": {"mods": sample_mods(), "notice": True, "noMods": True, "validUser": False,
                        "safeStart": {"reason": "crashed", "mods": ["mod-0", "mod-2"]}},
            "empty": {"mods": [], "notice": True, "noMods": True, "safeStart": {"reason": "flag"}, "validUser": True},
        }
        cfg = {"consent": consent, "mods": lists[mods] if mods else None,
               "pads": [None] * pads if pads else None,
               "bound": {"id": self.meta[save]["id"], "binding": self.meta[save]["bound"]} if bound else None}
        self.context = self.browser.new_context(viewport={"width": self.size[0], "height": self.size[1]}, device_scale_factor=1, locale=self.ui)
        self.context.add_init_script(STUB.replace("__CFG__", json.dumps(cfg)))
        if at is not None:
            self.clock(save, at)
        self.page = self.context.new_page()
        self.page.goto(f"{self.server.url}/?gallery")
        if ready:
            self.wait(ready)
        self.settle(1.2)
        return self.page

    def clock(self, save, at):
        """Date.now() fixed at `save`'s `now` (epoch ms) + `at` s; Playwright takes seconds."""
        self.context.clock.set_fixed_time(self.meta[save]["now"] / 1000 + at)

    def wait(self, selector, timeout=20000):
        self.page.wait_for_selector(selector, state="visible", timeout=timeout)

    def settle(self, s=0.8):
        time.sleep(s)

    def text(self, key):
        """The rendered text of a catalog key on this page (traced by `?gallery`)."""
        keys = self.page.evaluate("() => window.__galleryKeys ?? {}")
        texts = [t for t, ks in keys.items() if key in ks]
        if not texts:
            raise RuntimeError(f"{key}: not rendered yet")
        return max(texts, key=len)

    def click(self, selector):
        self.page.locator(selector).first.click(force=True)  # breathing buttons are never "stable"

    def click_key(self, key, within=""):
        """The visible button whose text holds the key's text."""
        self.page.locator(f"{within} button:visible", has_text=self.text(key)).first.click(force=True)

    def key(self, name):
        self.page.keyboard.press(name)

    def pad(self, button, pad=0):
        self.page.evaluate(f"window.__press({button}, {pad})")

    def menu(self):
        self.key("Escape")
        self.wait(".overlay .menu")
        self.settle(0.6)

    def answer(self, index, final=True):
        self.click(f".answers .answer:nth-child({index + 1})")
        if final:
            self.wait(".final-button.ready", 10000)
            self.settle(0.3)
            self.click(".final-button.ready")

    def shot(self, name):
        if self.only and name not in self.only:
            return
        self.settle(0.4)
        path = self.dir / f"{name}.png"
        self.page.screenshot(path=str(path))
        found = self.page.evaluate(TEXTS)
        items = match(found["items"], found["keys"], self.data)
        self.shots[name] = {"file": str(path.relative_to(OUT)), "items": items,
                            "unmatched": sorted({i["unmatched"] for i in items if "unmatched" in i})}
        print(f"  {self.name}/{name}: {sum(1 for i in items if 'keys' in i)} keyed, {len(self.shots[name]['unmatched'])} unmatched",
              flush=True)

    def close(self):
        if self.context:
            self.context.close()


# The walk -------------------------------------------------------------------------------------------------------------
# (shots, step): a step runs when one of its shots is wanted.

def first_start(r):
    r.scene(None, consent=None, ready="main .language .option")
    r.shot("language")
    r.click(".language .option.current")
    r.wait("main .consent .option")
    r.settle(1)
    r.shot("consent")


def start(r):
    r.scene("base")
    r.shot("start")
    r.click('[data-focus-id="language"]')
    r.wait("main .language .option")
    r.settle(1)
    r.shot("language-from-start")
    r.scene("table")
    r.shot("start-resume")
    r.scene(raw="{ not json", ready="main .language .option")  # moved to a backup: a fresh save asks first
    r.click(".language .option.current")
    r.wait('[data-focus-id="notice"]')
    r.settle(1)
    r.shot("start-save-notice")


def player(r):
    r.scene("base")
    r.click('[data-focus-id="main"]')
    r.wait(".name-button")
    r.settle(2.5)
    r.shot("player")
    r.click(".player .delete")
    r.wait(".player .dialog")
    r.settle(0.6)
    r.shot("player-delete-confirm")
    r.key("Escape")
    r.settle(0.6)
    r.click("#new-player")
    r.pad(0)
    r.wait(".backdrop .candy")
    r.settle(0.8)
    r.shot("letter-picker")


def seguir(r, ready):
    """«Seguir» once the screen takes input, then `ready` (a selector of the next screen)."""
    r.wait('[data-focus-id="next"]:enabled')  # force-click ignores disabled (busy)
    r.click('[data-focus-id="next"]')
    r.wait(ready)
    r.settle(0.6)


def choice(r):
    r.scene("base")
    r.click('[data-focus-id="main"]')
    r.wait(".name-button")
    r.settle(0.8)
    r.click(".name-button")
    r.wait('[data-focus-id="kind-single"]:enabled')
    r.settle(1.5)
    r.shot("mode-kind")
    seguir(r, '[data-focus-id="mode-gamemaster"]')
    r.settle(1)
    r.shot("mode-single")
    r.click('[data-focus-id="mode-gamemaster"]')
    seguir(r, ".config")
    r.settle(1.5)
    r.shot("choice-gamemaster")
    r.click('[data-focus-id="back"]')
    r.wait('[data-focus-id="mode-solo"]:enabled')
    r.click('[data-focus-id="mode-solo"]')
    seguir(r, '[data-focus-id="customize"]')
    r.settle(1.5)
    r.shot("choice-solo")
    r.click('[data-focus-id="customize"]')
    r.wait(".dialog")
    r.settle(0.8)
    r.shot("customize")
    r.key("Escape")
    r.settle(0.6)
    r.click('[data-focus-id="next"]')
    r.wait('[data-focus-id="start"]:enabled')
    r.settle(1.5)
    r.shot("bundles")
    r.click('[data-focus-id="start"]')
    r.wait(".bundles-screen .title.hello", 5000)
    r.settle(0.2)
    r.shot("greeting")


def to_bundles(r):
    """The default pick all the way: Mode, Mode again, Choice, then Bundles."""
    seguir(r, '[data-focus-id="mode-gamemaster"]')
    r.click('[data-focus-id="mode-gamemaster"]')
    seguir(r, ".config")
    seguir(r, ".bundles-screen")


def supply(r):
    if not r.only or "supply-notice" in r.only:
        r.scene("seen")
        r.click('[data-focus-id="main"]')
        r.wait(".name-button")
        r.settle(0.8)
        r.click(".name-button")
        to_bundles(r)
        r.wait('[data-focus-id="start"]:enabled')
        r.settle(1)
        r.click('[data-focus-id="start"]')
        r.wait('[data-focus-id="notice-play"]')
        r.settle(0.8)
        r.shot("supply-notice")
    for save, sel, name in (("short", ".supply", "bundles-supply-report"), ("blocked", ".error", "bundles-no-questions")):
        r.scene(save)
        r.click('[data-focus-id="main"]')
        r.wait(".name-button")
        r.settle(0.8)
        r.click(".name-button")
        to_bundles(r)
        r.wait(f".bundles-screen {sel}")
        r.settle(1.2)
        r.shot(name)


def table(r):
    r.scene("table")
    r.click('[data-focus-id="main"]')
    r.wait(".level .hint")
    r.settle(2)
    r.shot("level")
    r.click(".level .hint")
    r.wait(".cards .card")
    r.settle(2)
    r.shot("select")
    r.menu()
    r.click_key("overlay.settings", ".overlay")
    r.wait(".overlay .dialog")
    r.settle(1)
    r.shot("game-settings")


def on_question(r, save="question"):
    r.scene(save)
    r.click('[data-focus-id="main"]')
    r.wait(".answers .answer")
    r.settle(2.5)


def question(r):
    on_question(r)
    r.shot("question")
    r.click(".answers .answer:nth-child(1)")
    r.wait(".final-button.ready", 10000)
    r.settle(0.4)
    r.shot("question-locked")
    r.click(".answers .answer:nth-child(1)")  # unlock
    r.settle(0.5)
    r.click('.token[data-joker="hint"]')
    r.settle(0.6)
    r.shot("joker-hint-armed")
    r.click('.token[data-joker="hint"]')
    r.settle(3)
    r.shot("joker-hint")
    r.click('.token[data-joker="skip"]')
    r.settle(0.8)
    r.shot("joker-skip")
    r.key("Escape")
    r.settle(0.6)
    r.click('.token[data-joker="category"]')
    r.settle(0.8)
    r.shot("joker-category")
    r.key("Escape")
    r.settle(0.6)
    r.click('.token[data-joker="snipe"]')
    r.settle(0.8)
    r.shot("joker-snipe")
    on_question(r)
    r.click('.token[data-joker="easier"]')
    r.settle(0.4)
    r.click('.token[data-joker="easier"]')
    r.wait(".dial-spot", 8000)
    r.settle(1.2)
    r.shot("joker-easier")


def splash(r):
    # The splash frozen at its hold (window.__gallerySplash); the second shot on a long category and subcategory.
    hold = "window.__gallerySplash = %s"
    for name, topic, save in [("question-splash", "{}", "question"),
                              ("question-splash-long", '{topic: {category: "inventions-and-technology", '
                               'subcategory: "consoles-and-game-companies"}}', "question"),
                              ("timed-splash", "{}", "timed-q")]:
        if r.only and name not in r.only:
            continue
        if name == "timed-splash":
            r.scene(save, pads=len(r.meta[save]["bound"]) - 1, bound=True, at=10)
            r.page.evaluate(hold % topic)
            r.click('[data-focus-id="main"]')
            r.wait(".timed-screen .answers .answer")
        else:
            r.scene(save)
            r.page.evaluate(hold % topic)
            r.click('[data-focus-id="main"]')
            r.wait(".answers .answer")
        r.wait(".splash .category")
        r.settle(0.8)
        r.shot(name)


def results(r):
    on_question(r, "solo")
    r.answer(r.meta["solo"]["right"])
    r.wait(".final .waiting")
    r.settle(0.5)
    r.shot("question-waiting")
    r.wait("main .result", 30000)
    r.settle(2.5)
    r.shot("correct")
    on_question(r, "solo")
    r.answer((r.meta["solo"]["right"] + 1) % 4)
    r.wait("main .result.wrong", 30000)
    r.settle(2.5)
    r.shot("wrong")
    on_question(r, "final")
    r.answer(r.meta["final"]["right"])
    r.wait("main .result.victory", 40000)
    r.settle(3.5)
    r.shot("victory")


def overlay(r):
    r.scene("base")
    r.menu()
    r.shot("menu-start")
    on_question(r, "solo")
    r.menu()
    r.shot("menu-solo")
    on_question(r)
    r.menu()
    r.shot("menu-gamemaster")
    r.click_key("overlay.skipAll", ".overlay")
    r.settle(0.4)
    r.shot("menu-confirm")
    r.click_key("overlay.goTo", ".overlay")
    r.wait(".overlay .dialog")
    r.settle(0.6)
    r.shot("goto")
    r.pad(0)
    r.settle(1)
    r.shot("goto-letter-picker")
    on_question(r)
    r.menu()
    r.click_key("credits.open", ".overlay")
    r.wait(".credits .scroller")
    r.settle(1.5)
    r.shot("credits")


def flags(r):
    on_question(r)
    r.click(".flag-button")
    r.wait(".backdrop .dialog")
    r.settle(0.6)
    r.shot("flag-dialog")
    on_question(r, "flags")
    r.menu()
    r.click_key("flag.list", ".overlay")
    r.wait(".flags .candy")
    r.settle(1)
    r.shot("flag-list")


def mods(r):
    r.scene("base")
    r.click('[data-focus-id="mods"]')
    r.wait(".mods .list")
    r.settle(0.8)
    for _ in range(14):
        r.key("ArrowDown")
    r.settle(0.6)
    r.shot("mods")
    r.click(".mods li:not(.on) .row:not(.inert)")
    r.wait(".mods ~ .backdrop-dim .dialog, .backdrop-dim .dialog")
    r.settle(0.6)
    r.shot("mods-notice")
    r.scene("base", mods="crashed", ready=".mods .list")
    r.settle(0.6)
    r.shot("mods-crashed")
    r.scene("base", mods="empty")
    r.click('[data-focus-id="mods"]')
    r.wait(".mods .line")
    r.settle(0.6)
    r.shot("mods-empty")


def to_mode(r, save="base", pads=0):
    r.scene(save, pads=pads)
    r.click('[data-focus-id="main"]')
    r.wait(".name-button")
    r.settle(0.8)
    r.click(".name-button")
    r.wait('[data-focus-id="kind-multi"]:enabled')


def to_join(r, mode, save="base", pads=0):
    to_mode(r, save, pads)
    r.click('[data-focus-id="kind-multi"]')
    seguir(r, f'[data-focus-id="mode-{mode}"]')
    r.click(f'[data-focus-id="mode-{mode}"]')
    r.settle(1.2)
    r.click('[data-focus-id="next"]')
    r.wait(".join .seat.open")
    r.settle(0.8)


def join_pads(r, n):
    """Pads 0..n-1 press A, one seat each."""
    for i in range(n):
        r.pad(0, i)
        r.wait(f'[data-focus-id="seat-name-{i}"]')


def name_seat(r, i):
    """Seat `i` takes the first known name still free."""
    r.click(f'[data-focus-id="seat-name-{i}"]')
    r.wait(".join-name, .backdrop .name-button")
    r.settle(0.5)
    r.click(".backdrop .name-button")
    r.settle(0.4)


def type_key(r, key):
    r.wait(".key-field")
    r.page.keyboard.type(key)
    r.settle(0.4)


def multiplayer(r):
    # Five seats: four pads (Xbox and PlayStation ids alternate) and keyboard and mouse.
    to_mode(r, pads=4)
    r.click('[data-focus-id="kind-multi"]')
    seguir(r, '[data-focus-id="mode-rr-coop"]')
    r.click('[data-focus-id="mode-rr-coop"]')
    r.settle(1.5)
    r.shot("mode-multi")
    r.click('[data-focus-id="next"]')
    r.wait(".join .seat.open")
    r.settle(0.8)
    r.shot("join-empty")
    join_pads(r, 4)
    r.click('[data-focus-id="join-keyboard"]')
    r.wait('[data-focus-id="seat-name-4"]')
    for i in range(1, 4):
        name_seat(r, i)
    r.click('[data-focus-id="seat-name-4"]')
    r.wait(".backdrop .name-button")
    r.settle(0.8)
    r.shot("join-name-picker")
    r.click(".backdrop .name-button")
    r.settle(0.6)
    r.shot("join-5")
    seguir(r, '[data-focus-id^="group-"]')
    seguir(r, ".bundles-screen")
    r.wait('[data-focus-id="start"]:enabled')
    r.settle(1)
    r.click('[data-focus-id="start"]')
    r.wait(".bundles-screen .title.hello", 5000)
    r.settle(0.2)
    r.shot("greeting-session")
    # Eight seats: the list scrolls.
    to_join(r, "rr-coop", "crowd", pads=8)
    join_pads(r, 8)
    for i in range(1, 8):
        name_seat(r, i)
    r.shot("join-8")
    # Keyboard-only timed: three claim keys, a fourth refused.
    to_join(r, "timed")
    for i, key in enumerate("jqx"):  # letters no catalog binds on the Question screen
        r.click('[data-focus-id="join-keyboard"]')
        type_key(r, key)
        r.wait(f'[data-focus-id="seat-name-{i}"]')
    for i in (1, 2):
        name_seat(r, i)
    r.click('[data-focus-id="join-keyboard"]')
    type_key(r, "a")  # an answer letter: refused
    r.shot("join-keyboard-timed")
    # Round-robin competitive: each seat its own age group; a short supply naming a seat.
    to_join(r, "rr-competitive", "short", pads=2)
    join_pads(r, 2)
    name_seat(r, 1)
    seguir(r, '[data-focus-id="config-seat-group-1"]')
    r.click('[data-focus-id="config-seat-group-1"] .step:last-child')
    r.click('[data-focus-id="config-seat-group-1"] .step:last-child')
    r.settle(0.6)
    r.shot("choice-rr-competitive")
    r.click('[data-focus-id="next"]')
    r.wait(".bundles-screen")
    r.settle(1.5)
    r.shot("bundles-session")


def in_session(r):
    r.scene("session", pads=2)
    r.shot("start-resume-session")
    r.scene("session", pads=2, bound=True)
    r.click('[data-focus-id="main"]')
    r.wait("main .level, main .select, main .question")
    r.settle(2)
    r.menu()
    r.shot("menu-session")
    # No binding: the turn seat's pad is gone, so its seat waits (decision 289).
    r.scene("session", pads=2)
    r.click('[data-focus-id="main"]')
    r.wait(".dialog[aria-labelledby='seat-lost-title']")
    r.settle(1.5)
    r.shot("seat-lost")


def rr_question(r, save):
    """The session's question on screen; the turn seat is keyboard and mouse, the others hold pads."""
    r.scene(save, pads=3, bound=True)
    r.click('[data-focus-id="main"]')
    r.wait(".answers .answer")
    r.settle(2.5)


def round_robin(r):
    for mode, save in (("rr-coop", "coop"), ("rr-competitive", "comp")):
        r.scene(save, pads=3, bound=True)
        r.click('[data-focus-id="main"]')
        r.wait(".level .hint")
        r.settle(2)
        r.shot(f"level-{mode}")
        if mode == "rr-coop":
            r.click(".level .hint")
            r.wait(".cards .card")
            r.settle(2)
            r.shot("select-rr-coop")
    rr_question(r, "coop-q")
    r.answer(r.meta["coop-q"]["right"])
    r.wait("main .result", 30000)
    r.settle(2.5)
    r.shot("correct-rr-coop")
    rr_question(r, "coop-q")
    r.answer((r.meta["coop-q"]["right"] + 1) % 4)
    r.wait("main .result.wrong", 30000)
    r.settle(2.5)
    r.shot("wrong-rr-coop")
    rr_question(r, "coop-q12")
    r.answer(r.meta["coop-q12"]["right"])
    r.wait("main .result.victory", 40000)
    r.settle(3.5)
    r.shot("victory-rr-coop")
    rr_question(r, "comp-q")
    r.answer((r.meta["comp-q"]["right"] + 1) % 4)
    r.wait("main .result.wrong", 30000)
    r.settle(2.5)
    r.shot("wrong-rr-competitive")
    rr_question(r, "comp-q12")
    r.answer(r.meta["comp-q12"]["right"])
    r.wait("main .result.victory", 40000)
    r.settle(3.5)
    r.shot("victory-rr-competitive")
    rr_question(r, "comp-last")
    r.answer((r.meta["comp-last"]["right"] + 1) % 4)
    r.wait("main .result.wrong", 30000)  # «Fuera», then «Seguir» to the winner
    r.settle(1.5)
    r.click('main [data-focus-default]')
    r.wait("main .result.victory", 40000)
    r.settle(3.5)
    r.shot("victory-last-standing")


def timed_on(r, save, at):
    """A timed scene with the page clock fixed at the save's `now` + `at` s: deadlines never pass on their own."""
    r.scene(save, pads=len(r.meta[save]["bound"]) - 1, bound=True, at=at)
    r.click('[data-focus-id="main"]')
    r.wait(".timed-screen .answers .answer")
    r.settle(2.5)


def timed(r):
    timed_on(r, "timed-q", 10)  # one hint (8 s), 20 s left
    r.shot("timed-question")
    r.pad(5, 1)  # Sofía's RB: claimed at +10 s, 6 s to answer
    r.wait(".timed-screen .banner .ring")
    r.settle(0.6)
    r.shot("timed-claimed")
    r.clock("timed-q", 13.5)  # 2.5 s left: «3», ticks and the red frame
    r.settle(0.6)
    r.shot("timed-claim-last")
    timed_on(r, "timed-q", 10)  # a hidden window pauses (decision 282): the veil without the Esc menu over it
    r.page.evaluate("""() => {
      Object.defineProperty(document, "hidden", { get: () => true, configurable: true });
      document.dispatchEvent(new Event("visibilitychange"));
    }""")
    r.wait(".timed-screen .veil")
    r.shot("timed-paused")
    timed_on(r, "timed-q", 29)
    r.clock("timed-q", 31)  # the client's expire settles it
    r.wait(".timed-screen .banner.result", 10000)
    r.shot("timed-time-up")
    r.wait("main .screen.round", 10000)  # Sofía's cracked heart, Max out
    r.settle(1.2)
    r.shot("timed-round")
    timed_on(r, "timed-heart", 10)
    r.shot("timed-last-heart")
    timed_on(r, "timed-risk", 10)
    r.shot("timed-all-at-risk")
    r.clock("timed-risk", 31)  # both lose their last heart at the round's end
    r.wait("main .result.wrong", 30000)
    r.settle(2.5)
    r.shot("timed-nobody-wins")
    r.scene("timed-12", pads=1, bound=True, at=0)
    r.click('[data-focus-id="main"]')
    r.wait("main .screen.round")
    r.settle(0.6)  # before the 3-2-1 (FADE_MS + ROUND_HOLD_MS)
    r.shot("timed-sudden-death")
    timed_on(r, "timed-12-claim", 2)
    r.answer(r.meta["timed-12-claim"]["right"], final=False)
    r.wait("main .result.victory", 30000)
    r.settle(3.5)
    r.shot("victory-timed")


STEPS = [
    (["language", "consent"], first_start),
    (["start", "language-from-start", "start-resume", "start-save-notice"], start),
    (["player", "player-delete-confirm", "letter-picker"], player),
    (["mode-kind", "mode-single", "choice-gamemaster", "choice-solo", "customize", "bundles", "greeting"], choice),
    (["supply-notice", "bundles-supply-report", "bundles-no-questions"], supply),
    (["level", "select", "game-settings"], table),
    (["question", "question-locked", "joker-hint-armed", "joker-hint", "joker-skip", "joker-category", "joker-snipe",
      "joker-easier"], question),
    (["question-splash", "question-splash-long", "timed-splash"], splash),
    (["question-waiting", "correct", "wrong", "victory"], results),
    (["menu-start", "menu-solo", "menu-gamemaster", "menu-confirm", "goto", "goto-letter-picker", "credits"], overlay),
    (["flag-dialog", "flag-list"], flags),
    (["mods", "mods-notice", "mods-crashed", "mods-empty"], mods),
    (["mode-multi", "join-empty", "join-name-picker", "join-5", "greeting-session", "join-8", "join-keyboard-timed",
      "choice-rr-competitive", "bundles-session"], multiplayer),
    (["start-resume-session", "menu-session", "seat-lost"], in_session),
    (["level-rr-coop", "select-rr-coop", "correct-rr-coop", "wrong-rr-coop", "victory-rr-coop", "level-rr-competitive",
      "wrong-rr-competitive", "victory-rr-competitive", "victory-last-standing"], round_robin),
    (["timed-question", "timed-claimed", "timed-claim-last", "timed-paused", "timed-time-up", "timed-round",
      "timed-last-heart", "timed-all-at-risk", "timed-nobody-wins", "timed-sudden-death", "victory-timed"], timed),
]


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--locale", help="comma-separated UI languages (default: all)")
    ap.add_argument("--only", help="comma-separated shot names")
    ap.add_argument("--size", default="1920x1080", help="comma-separated viewports WxH (default 1920x1080)")
    ap.add_argument("--list", action="store_true", help="list the shot names")
    ap.add_argument("--set", help="review set task-<id>: only --only's shots, into sets/<name>/")
    ap.add_argument("--note", default="", help="the review set's note")
    ap.add_argument("--visible", action="store_true", help="a visible browser window")
    a = ap.parse_args()
    names = [n for shots, _ in STEPS for n in shots]
    if a.list:
        print("\n".join(names))
        return
    sizes = []
    for x in a.size.split(","):
        if not (m := re.fullmatch(r"(\d{3,4})x(\d{3,4})", x)):
            sys.exit(f"gallery: --size {x}: want WxH, e.g. 1280x800")
        sizes.append((int(m[1]), int(m[2])))
    if a.set and not (re.fullmatch(r"task-\d+", a.set) and a.only):
        sys.exit("gallery: --set task-<id> needs --only <shot>,…")
    locales = a.locale.split(",") if a.locale else LOCALES
    only = set(a.only.split(",")) if a.only else None
    if bad := [x for x in locales if x not in LOCALES] + sorted((only or set()) - set(names)):
        sys.exit(f"gallery: unknown {', '.join(bad)} (locales {', '.join(LOCALES)}; --list for shots)")
    from playwright.sync_api import sync_playwright  # nixpkgs Playwright from the flake wrapper

    build_if_stale()
    dest = OUT / "sets" / a.set if a.set else OUT
    if a.set:
        shutil.rmtree(dest, ignore_errors=True)
    dest.mkdir(parents=True, exist_ok=True)
    manifest_file = dest.with_suffix(".json") if a.set else OUT / "manifest.json"
    manifest = json.loads(manifest_file.read_text(encoding="utf-8")) if manifest_file.exists() and not a.set else {}
    if a.set:
        manifest.update(name=a.set, note=a.note, shots=[n for n in names if n in only])
    commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=REPO, capture_output=True, text=True).stdout.strip()
    dirty = subprocess.run(["git", "status", "--porcelain"], cwd=REPO, capture_output=True, text=True).stdout.strip()
    manifest.update(run=datetime.datetime.now().isoformat(timespec="seconds"), commit=commit + ("-dirty" if dirty else ""))
    shutil.rmtree(dest / "failed", ignore_errors=True)
    server = Server()
    failed = []
    try:
        with sync_playwright() as p:
            env = {k: v for k, v in os.environ.items() if k != "LD_LIBRARY_PATH"}
            browser = p.chromium.launch(headless=not a.visible, env=env)
            for size, ui in [(z, u) for z in sizes for u in locales]:
                print(ui, flush=True)
                demo = json.loads(subprocess.run(["node", str(REPO / "authoring/tools/gallery_saves.mjs"), ui],
                                                 cwd=REPO, check=True, capture_output=True, text=True).stdout)
                r = Run(browser, server, ui, size, demo, data_strings(demo["players"]), only, manifest, dest)
                for shots, step in STEPS:
                    if only and not only.intersection(shots):
                        continue
                    try:
                        step(r)
                    except Exception as e:  # one broken step doesn't stop the gallery
                        failed.append(f"{r.name}/{step.__name__}: {str(e).splitlines()[0]}")
                        (dest / "failed").mkdir(exist_ok=True)
                        if r.page:
                            r.page.screenshot(path=str(dest / "failed" / f"{r.name}-{step.__name__}.png"))
                        print(f"  FAILED {failed[-1]}", flush=True)
                r.close()
                manifest["locales"][r.name] = dict(sorted(manifest["locales"][r.name].items(), key=lambda kv: names.index(kv[0])
                                                     if kv[0] in names else len(names)))
            browser.close()
    finally:
        server.stop()
        manifest_file.write_text(json.dumps(manifest, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"gallery: {dest}/ ({', '.join(locales)})" + (f"; /gallery?set={a.set}" if a.set else ""))
    if failed:
        sys.exit("gallery: failed steps:\n  " + "\n  ".join(failed))


if __name__ == "__main__":
    main()
