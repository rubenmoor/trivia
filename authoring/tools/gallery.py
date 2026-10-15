#!/usr/bin/env python3
"""trivia-gallery (plan 100, decision 115): every screen and dialog in every UI language, with each text's catalog key.

The built client on the Node dev server (`npm run serve -w app/client`, a temp save dir, never state/), driven by
nixpkgs Playwright at 1920×1080 with the desktop bridge stubbed (valid Steam user, mods, telemetry, reports).
`?gallery` makes `t()` record rendered text → key (lib/i18n.ts); each shot's visible texts are matched against it.
Output: work/gallery/<locale>/<shot>.png and work/gallery/manifest.json (merged on --locale/--only runs).

Usage: trivia-gallery [--locale en,es,es-ES,de] [--only <shot>[,<shot>…]] [--list] [--visible]
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

REPO = Path(__file__).resolve().parent.parent.parent
CLIENT = REPO / "app" / "client"
DATA = REPO / "app" / "data"
OUT = REPO / "work" / "gallery"
LOCALES = ["en", "es", "es-ES", "de"]
W, H = 1920, 1080

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
  // A fake standard pad: `__press(button)` presses and releases it (letter pickers open from the pad only).
  const pad = {
    id: "Xbox 360 Controller (STANDARD GAMEPAD)", index: 0, mapping: "standard", connected: true, timestamp: 0,
    axes: [0, 0, 0, 0], buttons: Array.from({ length: 17 }, () => ({ pressed: false, touched: false, value: 0 })),
  };
  let pads = [];
  navigator.getGamepads = () => pads;
  window.__press = async (b) => {
    if (!pads.length) {
      pads = [pad];
      window.dispatchEvent(Object.assign(new Event("gamepadconnected"), { gamepad: pad }));
      await new Promise((r) => setTimeout(r, 100));
    }
    pad.buttons[b] = { pressed: true, touched: true, value: 1 };
    await new Promise((r) => setTimeout(r, 120));
    pad.buttons[b] = { pressed: false, touched: false, value: 0 };
    await new Promise((r) => setTimeout(r, 120));
  };
})();
"""

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

    for f in [*DATA.rglob("*.json"), CLIENT / "dist" / "credits.json"]:
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
        elif text in data:
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
    dist = CLIENT / "dist" / "index.html"
    inputs = [CLIENT / "index.html", CLIENT / "vite.config.ts", CLIENT / "credits.ts", REPO / "app" / "desktop" / "package.json",
              *(CLIENT / "src").rglob("*"), *(CLIENT / "public").rglob("*")]
    newest = max(f.stat().st_mtime for f in inputs if f.is_file())
    if dist.exists() and dist.stat().st_mtime >= newest:
        return
    print("gallery: client stale, npm run build", flush=True)
    subprocess.run(["npm", "run", "build"], cwd=REPO, check=True, stdout=subprocess.DEVNULL)


class Server:
    """`vite preview` with the dev server's plugin; stopped by its process group (npm → sh → vite)."""

    def __init__(self, save_dir):
        self.port = free_port()
        self.log = tempfile.TemporaryFile()
        env = {**os.environ, "TRIVIA_SAVE_DIR": str(save_dir), "TRIVIA_MUTE": "1"}
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


class Run:
    """One UI language: scenes (a save, a stub config, a fresh page) and shots."""

    def __init__(self, browser, server, save_dir, ui, demo, data, only, manifest):
        self.browser, self.server, self.save, self.ui = browser, server, save_dir / "game.json", ui
        self.saves, self.meta, self.data, self.only = demo["saves"], demo["meta"], data, only
        self.shots = manifest.setdefault("locales", {}).setdefault(ui, {})
        self.context = self.page = None
        (OUT / ui).mkdir(parents=True, exist_ok=True)

    def scene(self, save="base", *, raw=None, consent=False, mods="held", ready="main .start"):
        """A fresh page on `save` (None: no save file). `mods`: a list config, or None (no mods bridge)."""
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
        cfg = {"consent": consent, "mods": lists[mods] if mods else None}
        self.context = self.browser.new_context(viewport={"width": W, "height": H}, device_scale_factor=1, locale=self.ui)
        self.context.add_init_script(STUB.replace("__CFG__", json.dumps(cfg)))
        self.page = self.context.new_page()
        self.page.goto(f"{self.server.url}/?gallery")
        if ready:
            self.wait(ready)
        self.settle(1.2)
        return self.page

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

    def pad(self, button):
        self.page.evaluate(f"window.__press({button})")

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
        path = OUT / self.ui / f"{name}.png"
        self.page.screenshot(path=str(path))
        found = self.page.evaluate(TEXTS)
        items = match(found["items"], found["keys"], self.data)
        self.shots[name] = {"file": str(path.relative_to(OUT)), "items": items,
                            "unmatched": sorted({i["unmatched"] for i in items if "unmatched" in i})}
        print(f"  {self.ui}/{name}: {sum(1 for i in items if 'keys' in i)} keyed, {len(self.shots[name]['unmatched'])} unmatched",
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


def choice(r):
    r.scene("base")
    r.click('[data-focus-id="main"]')
    r.wait(".name-button")
    r.settle(0.8)
    r.click(".name-button")
    r.wait('[data-focus-id="mode-gamemaster"]:enabled')  # force-click ignores disabled (busy)
    r.click('[data-focus-id="mode-gamemaster"]')
    r.wait(".config")
    r.settle(1.5)
    r.shot("choice-gamemaster")
    r.click('[data-focus-id="mode-solo"]')
    r.wait('[data-focus-id="customize"]')
    r.settle(1.5)
    r.shot("choice-solo")
    r.click('[data-focus-id="customize"]')
    r.wait(".dialog")
    r.settle(0.8)
    r.shot("customize")
    r.key("Escape")
    r.settle(0.6)
    r.click('[data-focus-id="start"]')
    r.wait(".choice .title.hello", 5000)
    r.settle(0.2)
    r.shot("greeting")


def supply(r):
    r.scene("seen")
    r.click('[data-focus-id="main"]')
    r.wait(".name-button")
    r.settle(0.8)
    r.click(".name-button")
    r.wait('[data-focus-id="start"]:enabled')
    r.settle(1)
    r.click('[data-focus-id="start"]')
    r.wait('[data-focus-id="notice-play"]')
    r.settle(0.8)
    r.shot("supply-notice")
    r.scene("blocked")
    r.click('[data-focus-id="main"]')
    r.wait(".name-button")
    r.settle(0.8)
    r.click(".name-button")
    r.wait(".choice .supply")
    r.settle(1.2)
    r.shot("choice-supply-report")


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


STEPS = [
    (["language", "consent"], first_start),
    (["start", "language-from-start", "start-resume", "start-save-notice"], start),
    (["player", "player-delete-confirm", "letter-picker"], player),
    (["choice-gamemaster", "choice-solo", "customize", "greeting"], choice),
    (["supply-notice", "choice-supply-report"], supply),
    (["level", "select", "game-settings"], table),
    (["question", "question-locked", "joker-hint-armed", "joker-hint", "joker-skip", "joker-category", "joker-snipe",
      "joker-easier"], question),
    (["question-waiting", "correct", "wrong", "victory"], results),
    (["menu-start", "menu-solo", "menu-gamemaster", "menu-confirm", "goto", "goto-letter-picker", "credits"], overlay),
    (["flag-dialog", "flag-list"], flags),
    (["mods", "mods-notice", "mods-crashed", "mods-empty"], mods),
]


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--locale", help="comma-separated UI languages (default: all)")
    ap.add_argument("--only", help="comma-separated shot names")
    ap.add_argument("--list", action="store_true", help="list the shot names")
    ap.add_argument("--visible", action="store_true", help="a visible browser window")
    a = ap.parse_args()
    names = [n for shots, _ in STEPS for n in shots]
    if a.list:
        print("\n".join(names))
        return
    locales = a.locale.split(",") if a.locale else LOCALES
    only = set(a.only.split(",")) if a.only else None
    if bad := [x for x in locales if x not in LOCALES] + sorted((only or set()) - set(names)):
        sys.exit(f"gallery: unknown {', '.join(bad)} (locales {', '.join(LOCALES)}; --list for shots)")
    from playwright.sync_api import sync_playwright  # nixpkgs Playwright from the flake wrapper

    build_if_stale()
    OUT.mkdir(parents=True, exist_ok=True)
    manifest_file = OUT / "manifest.json"
    manifest = json.loads(manifest_file.read_text()) if manifest_file.exists() else {}
    commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=REPO, capture_output=True, text=True).stdout.strip()
    dirty = subprocess.run(["git", "status", "--porcelain"], cwd=REPO, capture_output=True, text=True).stdout.strip()
    manifest.update(run=datetime.datetime.now().isoformat(timespec="seconds"), commit=commit + ("-dirty" if dirty else ""))
    shutil.rmtree(OUT / "failed", ignore_errors=True)
    tmp = Path(tempfile.mkdtemp(prefix="trivia-gallery-"))
    server = Server(tmp)
    failed = []
    try:
        with sync_playwright() as p:
            env = {k: v for k, v in os.environ.items() if k != "LD_LIBRARY_PATH"}
            browser = p.chromium.launch(headless=not a.visible, env=env)
            for ui in locales:
                print(ui, flush=True)
                demo = json.loads(subprocess.run(["node", str(REPO / "authoring/tools/gallery_saves.mjs"), ui],
                                                 cwd=REPO, check=True, capture_output=True, text=True).stdout)
                r = Run(browser, server, tmp, ui, demo, data_strings(demo["players"]), only, manifest)
                for shots, step in STEPS:
                    if only and not only.intersection(shots):
                        continue
                    try:
                        step(r)
                    except Exception as e:  # one broken step doesn't stop the gallery
                        failed.append(f"{ui}/{step.__name__}: {str(e).splitlines()[0]}")
                        (OUT / "failed").mkdir(exist_ok=True)
                        r.page.screenshot(path=str(OUT / "failed" / f"{ui}-{step.__name__}.png"))
                        print(f"  FAILED {failed[-1]}", flush=True)
                r.close()
                manifest["locales"][ui] = dict(sorted(manifest["locales"][ui].items(), key=lambda kv: names.index(kv[0])
                                                     if kv[0] in names else len(names)))
            browser.close()
    finally:
        server.stop()
        shutil.rmtree(tmp, ignore_errors=True)
        manifest_file.write_text(json.dumps(manifest, ensure_ascii=False, indent=1) + "\n")
    print(f"gallery: {OUT.relative_to(REPO)}/ ({', '.join(locales)})")
    if failed:
        sys.exit("gallery: failed steps:\n  " + "\n  ".join(failed))


if __name__ == "__main__":
    main()
