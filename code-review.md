# Code review (milestone 13)

This report collects the findings of the milestone 13 code review: every tracked code and build file in scope is read once, cheap fixes are made on the spot, and everything else becomes a follow-up task or a decision. Parts 1–11 follow `plan 72: masterplan`; each part appends its rows to its own section, and the inventory at the end maps every file to the part that reviews it.

## Executive summary

PLACEHOLDER(590)

## Format

Each part has one table with one row per finding; every file of the inventory ends up in at least one row.

- Columns: file | finding | category | severity | status
- Category: unused / practice / complexity / performance / bug / inconsistency
- Severity:
  - high: wrong behaviour, data loss, security or offline breakage reachable in play/authoring
  - medium: latent bug, real maintenance cost or measurable slowness
  - low: cosmetic, naming, small dead code
- Status: `fixed (task N)`, `handed to part N`, `follow-up task N`, `decision N`, `superseded by task N`, `won't fix: <why>`
- File reviewed without findings: one row, finding `no findings`, category/severity/status `—`
- Linter evidence: a TS/Svelte/`.mjs`/`.cjs` finding a lint rule or `tsconfig` flag would catch carries the rule in its finding text, e.g. `(lint: noUnusedLocals)`, `(lint: no-floating-promises)`; part 10 counts them
- Duplication candidates: both paths in the row, status `handed to part 10`
- Part 1 rows `handed to part N`: that part logs the final status in its own section, quoting the row

## Part 1: Baseline scans and report skeleton

Plan 73 runs cross-cutting scans over the whole inventory. Each scan adds its rows under a `### <scan>` sub-heading with the exact command; findings in another part's files get status `handed to part N`.

| file | finding | category | severity | status |
|---|---|---|---|---|

### directory.md vs git ls-files

Task 525, 2026-10-13. Throw-away script (deleted after), run from the repo root: `python3 dircheck.py`. A tracked file counts as named when its path is in backticks, or its basename (or first sub-directory) is in the row of an ancestor directory; `*.test.ts` and rows keyed by a file were checked by hand. Backticked tokens that look like paths are checked against `git ls-files` and the disk.

```python
import re, subprocess, os
md = open('directory.md').read(); ticks = set(re.findall(r'`([^`]+)`', md))
files = subprocess.run(['git','ls-files'], capture_output=True, text=True).stdout.split()
skip = re.compile(r'^(plans/|tasks\.sql|project-manager\.toml|authoring/tools/prompts/|app/client/public/(audio|fonts)/'
                  r'|app/client/src/engine/fixtures/|app/data/|authoring/data/|authoring/reports/)|\.md$')
def named(f):
    if f in ticks: return True
    b = os.path.basename(f)
    for row in md.splitlines():
        m = re.match(r'\| `([^`]+)`', row)
        if m and m.group(1).endswith('/') and f.startswith(p := m.group(1)) and (
                '`' + b in row or '`' + f[len(p):] in row or f[len(p):].split('/')[0] + '/' in row):
            return True
for f in files:
    if not skip.search(f) and not named(f): print('MISSING', f)
pre = ['', 'app/', 'authoring/', 'app/server/', 'app/desktop/', 'app/client/', 'app/client/src/', 'app/client/src/game/',
       'app/client/src/lib/', 'app/client/src/locales/', 'app/client/src/engine/', 'authoring/tools/', 'authoring/server/',
       'authoring/ui/', 'authoring/ui/src/', 'authoring/steam/', 'authoring/store/', 'authoring/tools/providers/']
pre += ['authoring/ui/src/' + d + '/' for d in ('home', 'lib', 'review', 'stats', 'print')]
for t in sorted(ticks):
    if re.search(r'[ <{*]', t) or t.startswith(('/', '.', 'app://')): continue
    if not re.search(r'/|\.(py|ts|mjs|cjs|svelte|json|md|vdf|yml|in|nix|lock)$', t): continue
    c = [p + t for p in pre]
    if not any(x in files or any(y.startswith(x.rstrip('/') + '/') for y in files) or os.path.exists(x) for x in c):
        print('STALE?', t)
```

- Before: 174 code/config files, 79 `MISSING`; after: 13, all named in a file-keyed row (`node.d.ts`, `supply.ts`, `sim/*.ts`, `authoring/tools/package.json`) or by the `*.test.ts` glob.
- 28 `STALE?` tokens: none stale. They are gitignored or generated (`state/…`, `work/…`, `steamworks_sdk/`, `credits.json`, `CREDITS.md`), written on first use (`health-acks.json`, `spot-checks.json`), relative names (`translate.md`, `selection.json`, …), or deleted files named as such (`game.py`, `selection.py`, D-90).
- Known gap `app/server/flags.py`: deleted by task 303 (decision 25), already absent from `directory.md`.

| file | finding | category | severity | status |
|---|---|---|---|---|
| `directory.md` | 64 tracked code/config files not named: `app/client` config and boot files, 18 of 36 `game/` files, `lib/api.ts`/`types.ts`, `authoring/server/main.py`/`overview.py`/`media_stats.py`, `authoring/tools/providers/` (5), `authoring/ui/` (30), root `.envrc`/`.gitignore`/`package-lock.json` | inconsistency | low | fixed (task 525) |
| `directory.md` | `sim/` named only as a directory, without its two files | inconsistency | low | fixed (task 525) |
| `directory.md` | `app/data/pool.<locale>.json` and `authoring/data/questions.<locale>.json` read as existing for `en`, `de`; none exist yet (no translation run) | inconsistency | low | fixed (task 525): "none yet" |
| `authoring/ui/src/stats/Stats.svelte` | header comment broken ("… approved questions only. / and media (RV-23).") | practice | low | fixed (task 525) |
| `app/client/src/app.css`, `authoring/ui/src/app.css` | identical 27-line colour token files | complexity | low | handed to part 10 |

### Unused TS/JS code and npm dependencies

Task 526, 2026-10-13, run from the repo root. Throw-away scripts in `/tmp` (deleted after; reproduced below). Both `tsconfig.json`s already set `noUnusedLocals`/`noUnusedParameters` (task 616), so `tsc` finds nothing; the unused-export, unused-prop and dependency scans are the new part.

- `tsc` (`.ts` only), each flag alone and both together (zsh: one argument per flag):
  - `npx tsc --noEmit --noUnusedLocals true --noUnusedParameters false -p app/client`: 0; `… false … true`: 0; both `true`: 0
  - same three for `-p authoring/ui` (also type-checks `app/client/src`): 0, 0, 0
  - tests included (temp `app/client/tsconfig.tmp526.json`: `{"extends": "./tsconfig.json", "include": ["src/**/*.ts"], "exclude": []}`, deleted after): 0 `TS6133`/`TS6196`/`TS6198`; 26 other errors (missing Node types, `findLast` lib, possibly-null), already `task 586` (plan 82 task 7: tests outside the `tsconfig`s)
- `svelte-check` (flags come from the `tsconfig`; it reports them in `.svelte` script blocks, task 616 probe): `cd app/client && npx svelte-check --tsconfig ./tsconfig.json --output machine`: 204 files, 0 errors, 0 warnings; `authoring/ui`: 171 files, 0, 0
- Linter evidence (part 10): `noUnusedLocals` 0 + 0, `noUnusedParameters` 0 + 0 (`app/client` + `authoring/ui`); no flag or `svelte-check` sees unused exports or props
- Exported names (`python3 exports.py`): 116 files, 416 exports; 5 `DEAD`, 7 `TESTONLY`, 50 `LOCAL` raw, checked by hand:
  - false positives: `game.CHOICE_KEYS`/`playerChoice`/`setJokers`/`MODES`/`cleanName`, `engine.getGame`/`getPlayers`, `selection.inRange`/`assign` (namespace imports), `pseudo` (dynamic `import("../locales/xx")`), `afterPack` (`electron-builder.yml`), `PlayerRow` and `defaultChoice` (used in their own file too)
  - real: 2 exports used only by tests, 47 exported but used only in their own file (rows below); no dead export in shipped code
- Svelte props (`python3 props.py`): 36 components with `$props()`, 152 props: none never passed by any caller (only `{...spread}` would hide one; none); 14 props with a default that every caller passes anyway, not a finding
- Unreferenced files (no other tracked file names the basename, `.json`/`.md` aside): `check-literals.mjs` (npm script, row below), `vite-env.d.ts` (ambient types), `after-pack.mjs` (`electron-builder.yml`)
- npm deps: bare imports `git ls-files | grep -E '\.(ts|svelte|mjs|cjs|js)$' | grep -v fixtures | xargs grep -hoE "(from |import\(|require\()\s*['\"][^'\"./][^'\"]*['\"]"` plus `git grep` in scripts, `flake.nix`, `electron-builder.yml`:
  - `package.json` (root): no deps
  - `app/client`, `authoring/ui` (same 6 devDeps): `svelte`, `vite`, `@sveltejs/vite-plugin-svelte` imported; `@tsconfig/svelte` via `tsconfig.json` `extends`; `svelte-check` via `check`; `typescript` peer of `svelte-check`, `npx tsc`
  - `app/desktop`: `electron` (`main.mjs`, `preload.cjs`), `steamworks-ffi-node` (`main.mjs` dynamic import, `credits.ts`), `electron-builder` (`dist` scripts, `trivia-desktop-build`)
  - `authoring/tools`: no deps; its `.ts`/`.mjs` (and `authoring/steam`, `authoring/store` `.mjs`) import only `node:*` and relative paths
  - undeclared: none (`$app/*` is the `authoring/ui` path alias); `npm ls --depth=0` clean in the root and `app/desktop`; no `extraneous` entry in either lockfile (77 and 316 packages)

```python
# exports.py: exported names nobody else names
import re, subprocess
files = [f for f in subprocess.run(['git','ls-files'], capture_output=True, text=True).stdout.split()
         if re.search(r'\.(ts|svelte|mjs|cjs|js)$', f) and 'engine/fixtures' not in f]
src = {f: open(f).read() for f in files}
other = {}
for f in subprocess.run(['git','ls-files'], capture_output=True, text=True).stdout.split():
    if f not in src and re.search(r'\.(py|html|nix|json|yml)$', f) and 'data/' not in f and 'fixtures' not in f:
        other[f] = open(f).read()
decl = re.compile(r'^\s*export\s+(?:default\s+)?(?:declare\s+)?(?:async\s+)?(?:function\*?|const|let|var|class|type|interface|enum)\s+([A-Za-z_$][\w$]*)', re.M)
lst = re.compile(r'^\s*export\s*(?:type\s*)?\{([^}]*)\}(?!\s*from)', re.M)
def strip(t):
    t = re.sub(r'/\*.*?\*/', '', t, flags=re.S); return re.sub(r'(?<![:\'"])//[^\n]*', '', t)
clean = {f: strip(t) for f, t in src.items()}
for f in files:
    names = decl.findall(src[f])
    for m in lst.findall(src[f]):
        names += [x.split(' as ')[-1].strip() for x in m.split(',') if x.strip()]
    if f.endswith('.cjs'): names += re.findall(r'module\.exports\.(\w+)', src[f])
    for n in names:
        w = re.compile(r'(?<![\w$.])' + re.escape(n) + r'(?![\w$])')
        users = [g for g in files if g != f and w.search(clean[g])]
        own = len(w.findall(clean[f]))
        prod = [g for g in users if not re.search(r'\.test\.ts$|engine/test/', g)]
        ext = [g for g in other if w.search(other[g])]
        if not users:
            print(('DEAD ' if own <= 1 else 'LOCAL'), f, n, 'own=%d' % own, 'other=' + ','.join(ext) if ext else '')
        elif not prod and not re.search(r'\.test\.ts$|engine/test/', f):
            print('TESTONLY', f, n, ','.join(users))
# then by hand: git grep -n "<ns>\.<name>" for every `import * as <ns>` of the reported module
```

```python
# props.py: $props() names never passed by any <Component …> of an importing file
import re, subprocess, os
files = [f for f in subprocess.run(['git','ls-files'], capture_output=True, text=True).stdout.split() if re.search(r'\.(svelte|ts)$', f)]
src = {f: open(f).read() for f in files}
def tags(text, name):  # attribute text of every <Name …>, braces balanced
    i = 0
    while (i := text.find('<' + name, i)) >= 0:
        j = i + len(name) + 1
        if j < len(text) and (text[j].isalnum() or text[j] in '_.'): i = j; continue
        d = 0; k = j
        while k < len(text):
            c = text[k]
            if c == '{': d += 1
            elif c == '}': d -= 1
            elif c == '>' and d == 0: break
            k += 1
        yield text[j:k]; i = k
def attrs(t):  # attribute names: a=…, bare a, {a}, bind:a
    out, d, cur, q, prev = set(), 0, '', None, ''
    for c in t:
        p, prev = prev, (c if not c.isspace() else prev)
        if q:
            if c == q: q = None
            continue
        if d == 0 and c in '"\'': q = c; continue
        if c == '{':
            if d == 0 and cur == '' and p != '=': cur = '{'
            d += 1; continue
        if c == '}':
            d -= 1
            if d == 0 and cur.startswith('{'): out.add(cur[1:].strip()); cur = ''
            continue
        if d:
            if cur.startswith('{'): cur += c
            continue
        if c.isspace() or c in '=/':
            if cur: out.add(cur.split(':')[-1]); cur = ''
        else: cur += c
    if cur: out.add(cur.split(':')[-1])
    return out
for f in files:
    if not f.endswith('.svelte') or (i := src[f].find('$props()')) < 0: continue
    st = src[f].rfind('let {', 0, i); d = 0; k = st + 4
    while True:
        c = src[f][k]
        if c == '{': d += 1
        elif c == '}':
            d -= 1
            if d == 0: break
        k += 1
    body = re.sub(r'//[^\n]*', '', re.sub(r'/\*.*?\*/', '', src[f][st + 5:k], flags=re.S))
    props, d, cur = [], 0, ''
    for c in body:
        if c in '({[': d += 1
        if c in ')}]': d -= 1
        if c == ',' and d == 0: props.append(cur); cur = ''
        else: cur += c
    props.append(cur)
    names = [(re.match(r'([\w$]+)', p.strip()).group(1), '=' in p) for p in props if p.strip() and not p.strip().startswith('...')]
    comp = os.path.basename(f)[:-7]
    callers = [g for g in files if g != f and re.search(r'import\s+' + comp + r'\b', src[g])]
    uses = [t for g in callers for t in tags(src[g], comp)]
    if not uses: print('NOUSE', f); continue
    if any('{...' in t for t in uses): print('SPREAD', f); continue
    for n, dflt in names:
        hit = sum(1 for t in uses if n in attrs(t))
        if hit == 0 and n != 'children': print('NEVER', f, n, 'default' if dflt else 'NO-DEFAULT', len(uses))
        elif hit == len(uses) and dflt: print('ALWAYS', f, n, len(uses))
```

| file | finding | category | severity | status |
|---|---|---|---|---|
| `app/client/tsconfig.json`, `authoring/ui/tsconfig.json` (all `.ts`/`.svelte` they include) | no findings: 0 `noUnusedLocals`, 0 `noUnusedParameters` (lint: noUnusedLocals, noUnusedParameters) | — | — | — |
| `app/client/src/engine/pool.ts` | `bundleOf` exported, used only by `pool.test.ts`: dead in the shipped engine (lint: none, unused export) | unused | low | handed to part 3 |
| `app/client/src/engine/store.ts` | `MemoryStore` exported, used only by `save.test.ts`: test helper in a shipped module, belongs in `engine/test/` (lint: none, unused export) | unused | low | handed to part 3 |
| `app/client/src/engine/` (`game.ts`, `outlook.ts`, `pool.ts`, `selection.ts`, `state.ts`, `test/tape.ts`) | 23 exports used only in their own file: `game.ts` `JOKERS`, `gameMode`, `ChoiceInput`, `cardsOf`, `mediaAllowed`, `availableNow`, `ChoiceArgs`, `leaveQuestion`, `dropCurrent`, `backToSelect`, `laterFill`, `categoryCandidates`, `JokerArgs`; `outlook.ts` `seenPerLevel`, `OutlookChoice`; `pool.ts` `levelWeights`; `selection.ts` `CategoryKey`, `SupplyLevel`, `DrawOptions`; `state.ts` `SeenRow`, `HistoryEntry`, `LastAnswer`; `test/tape.ts` `TapeRng`: drop `export` unless meant as API (lint: none, unused export) | unused | low | handed to part 3 |
| `app/client/src/lib/`, `app/client/src/locales/xx.ts` | 10 exports used only in their own file: `build.ts` `BuildInfo`; `desktop.ts` `SteamBridge`, `TextFieldRect`; `engine.ts` `localIsoSeconds`, `Route`; `focus.ts` `Rect`; `gamepad.ts` `Pad`; `input.svelte.ts` `Device`, `toIntent`; `xx.ts` `pseudoText` (lint: none, unused export) | unused | low | handed to part 4 |
| `app/client/scripts/check-literals.mjs` | `npm run check:literals -w app/client` fails (exit 1): 8 Spanish literals in the dev-only `game/EffectsDemo.svelte` (lines 27–41); the check runs in no pre-commit step (not in `check`/`test`, D-73), so it drifts unseen | inconsistency | low | handed to part 4 |
| `app/client/src/game/` (`Choice.svelte`, `Fireworks.svelte`, `Stage.svelte`, `letters.ts`) | 4 exports used only in their own file: `bundleKeys`, `FireworksMode`, `StageMood`, `MAX_NAME` (lint: none, unused export) | unused | low | handed to part 5 |
| `app/desktop/resolve.mjs` | `mimeOf` exported, used only inside `resolve.mjs` (lint: none, unused export) | unused | low | handed to part 6 |
| `authoring/tools/sim/load.ts`, `authoring/tools/sim/simulate.ts` | `DATA_DIR`, `TYPICAL_P`, `MAX_GAMES` exported, used only in their own file (lint: none, unused export) | unused | low | handed to part 8 |
| `authoring/ui/src/lib/types.ts`, `authoring/ui/src/stats/breakdown.ts` | `Revision`, `Quality`, `Reviewer`, `SourceText`, `SubRow` exported, used only in their own file (lint: none, unused export) | unused | low | handed to part 9 |
| `app/client/credits.ts` | `buildCredits` exported, used only inside `credits.ts` (lint: none, unused export) | unused | low | handed to part 10 |
| `package.json`, `app/client/package.json`, `app/desktop/package.json`, `authoring/tools/package.json`, `authoring/ui/package.json` | no findings: every dependency used, none undeclared, no extraneous lockfile entry | — | — | — |
| Svelte components (36 with `$props()`) | no findings: every prop passed by at least one caller | — | — | — |

### Unused Python code

Task 527, 2026-10-13, run from the repo root over all 32 tracked `.py` files (`app/server`, `authoring/server`, `authoring/tools/**`, `authoring/steam`). No `vulture` or `pyflakes` in the flake or Python env, so throw-away `ast` scripts in `/tmp` (deleted after; reproduced below).

- `python3 pyscan.py`: top-level `def`/`class`/assignments with no other mention in any tracked `.py`/`.ts`/`.mjs`/`.svelte`/`.nix` file (`DEAD`: 0), imports never loaded, function locals stored but never loaded, parameters never read
- `python3 precise.py`: same names, but a hit elsewhere must be `mod.name` or `from mod import name` (generic names like `save`, `load`, `build`): 4 `download_url` and 16 `CHECK` hits, all in `providers/*.py`: the provider protocol, called as `PROVIDERS[p].<name>` (`providers/__init__.py`); no dead name
- `python3 flags.py` (each `add_argument` dest vs. `args.<dest>` in its file; 93 flags in 6 files) and `python3 subflags.py` (per `qgen` subcommand: flags vs. what its handler and the `qgen`/`patch_notes` functions it calls read, transitively): every flag read
- Raw hits not findings: `cmd_export`/`cmd_validate`/`cmd_stage(args)` (argparse dispatch), `pd_reasons(candidate)` in `freesound.py`/`nasa.py` (protocol), `import layout  # noqa: F401` in `categories.py`, `download.py`, `save_file.py` (side effect: puts `app/server` on `sys.path`, D-35; they import `paths`/`media_cache`/`save`)
- Task 302 rule (`task 302: Delete the Python referee`): `app/server/game.py`, `selection.py`, `flags.py`, `authoring/tools/record_fixtures.py` already deleted by task 303 (decision 25: Family test night on the TS engine); nothing to scan

| file | finding | category | severity | status |
|---|---|---|---|---|
| `app/server/game.py`, `app/server/selection.py`, `app/server/flags.py`, `authoring/tools/record_fixtures.py` | Python referee: deleted (task 303), not scanned | unused | — | superseded by task 302 |
| `authoring/tools/media.py` | `USER_AGENT` imported from `download`, never used; `# noqa: F401` on both re-export lines hid it, though every other name there is used | unused | low | fixed (task 527) |
| `authoring/tools/qgen.py` | `translation_problems(data, scale)`: `scale` unpacked into `lo, hi`, never read; caller passed `(lo, hi)` | unused | low | fixed (task 527) |
| `authoring/tools/qgen.py` | `translate_selection`: local `src` built, never read (a dict over the whole pool per call) | unused | low | fixed (task 527) |
| `authoring/tools/qgen.py` | `qc_stats(batch, checks, pool)`: `pool` never read; 2 callers | unused | low | fixed (task 527) |
| `authoring/tools/` (`batches.py`, `health.py`, `media.py`, `targets.py`, `providers/commons.py`, `freesound.py`, `nasa.py`, `openverse.py`) | redundant `import layout  # noqa: F401`: the module also does `from layout import …`, or (providers) imports `download`, which imports `layout` first; the noqa hid it | unused | low | fixed (task 527) |
| `app/server/*.py` (5), `authoring/server/*.py` (4), `authoring/steam/*.py` (2), `authoring/tools/` other `.py` | no findings: no dead `def`/`class`/constant, unused import, dead local or unread CLI flag | — | — | — |

```python
# pyscan.py: unused top-level names, unused imports, unused locals (ast)
import ast, re, subprocess, sys
files = [f for f in subprocess.check_output(['git','ls-files','*.py']).decode().split()]
other = [f for f in subprocess.check_output(['git','ls-files']).decode().split()
         if re.search(r'\.(nix|ts|mjs|cjs|svelte|html|toml|yml|sh)$', f) or f in ('.envrc',)]
src = {f: open(f).read() for f in files}
osrc = {f: open(f, errors='ignore').read() for f in other}
for f in files:
    tree = ast.parse(src[f])
    names = []
    for n in tree.body:
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)): names.append((n.name, n.lineno, 'def'))
        elif isinstance(n, ast.Assign):
            for t in n.targets:
                for e in ast.walk(t):
                    if isinstance(e, ast.Name): names.append((e.id, n.lineno, 'var'))
        elif isinstance(n, ast.AnnAssign) and isinstance(n.target, ast.Name): names.append((n.target.id, n.lineno, 'var'))
    for name, ln, kind in names:
        if name in ('main', '__all__') or name.startswith('__'): continue
        pat = re.compile(r'\b' + re.escape(name) + r'\b')
        own = len(pat.findall(src[f]))
        ext = [g for g in files if g != f and pat.search(src[g])] + [g for g in other if pat.search(osrc[g])]
        if own <= 1 and not ext: print(f'DEAD     {f}:{ln} {kind} {name}')
        elif own <= 1: print(f'EXTONLY? {f}:{ln} {kind} {name} <- {ext[:3]}')
    # unused imports
    used = {n.id for n in ast.walk(tree) if isinstance(n, ast.Name)} | {n.value.id for n in ast.walk(tree) if isinstance(n, ast.Attribute) and isinstance(n.value, ast.Name)}
    strs = ' '.join(n.value for n in ast.walk(tree) if isinstance(n, ast.Constant) and isinstance(n.value, str))
    for n in ast.walk(tree):
        if isinstance(n, (ast.Import, ast.ImportFrom)):
            for a in n.names:
                nm = (a.asname or a.name).split('.')[0]
                if nm not in used and nm != '*' and nm != 'annotations':
                    print(f'IMPORT   {f}:{n.lineno} {nm}' + (' (in str)' if nm in strs else ''))
    # unused locals in functions
    for fn in ast.walk(tree):
        if isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)):
            stores, loads = {}, set()
            for n in ast.walk(fn):
                if isinstance(n, ast.Name):
                    if isinstance(n.ctx, ast.Store): stores.setdefault(n.id, n.lineno)
                    else: loads.add(n.id)
            nonlocal_ = {x for n in ast.walk(fn) if isinstance(n, (ast.Global, ast.Nonlocal)) for x in n.names}
            for v, ln in stores.items():
                if v not in loads and v != '_' and not v.startswith('_') and v not in nonlocal_:
                    print(f'LOCAL    {f}:{ln} {fn.name}.{v}')
            # unused params
            for a in fn.args.args + fn.args.kwonlyargs:
                if a.arg not in loads and a.arg not in ('self', 'cls') and not a.arg.startswith('_'):
                    print(f'PARAM    {f}:{fn.lineno} {fn.name}({a.arg})')
```

```python
# precise.py: top-level names never used in own module, nor as `mod.name` / `from mod import name` elsewhere
import ast, re, subprocess
files = subprocess.check_output(['git','ls-files','*.py']).decode().split()
other = [f for f in subprocess.check_output(['git','ls-files']).decode().split() if re.search(r'\.(nix|ts|mjs|svelte|sh)$', f)]
src = {f: open(f).read() for f in files}
osrc = '\n'.join(open(f, errors='ignore').read() for f in other)
for f in files:
    mod = f.rsplit('/', 1)[1][:-3]
    if mod == '__init__': mod = f.split('/')[-2]
    tree = ast.parse(src[f])
    defs = {}
    for n in tree.body:
        if isinstance(n, (ast.FunctionDef, ast.ClassDef)): defs[n.name] = n.lineno
        elif isinstance(n, ast.Assign):
            for t in n.targets:
                if isinstance(t, ast.Name): defs[t.id] = n.lineno
    loads = {n.id for n in ast.walk(tree) if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load)}
    for name, ln in defs.items():
        if name in loads or name == 'main' or name.startswith('__'): continue
        hits = []
        for g in files:
            if g == f: continue
            s = src[g]
            aliases = [mod] + re.findall(r'import\s+' + mod + r'\s+as\s+(\w+)', s)
            if any(re.search(r'\b' + a + r'\.' + name + r'\b', s) for a in aliases): hits.append(g)
            elif re.search(r'from\s+(\S*\.)?' + mod + r'\s+import\s+\(?[^)\n]*\b' + name + r'\b', s): hits.append(g)
            elif re.search(r'getattr\(', s) and re.search(r'["\']' + name + r'["\']', s): hits.append(g + '(getattr)')
        if re.search(r'\b' + name + r'\b', osrc) and not hits: hits.append('non-py?')
        if not hits: print(f'UNUSED {f}:{ln} {name}')
        elif hits == ['non-py?']: print(f'CHECK  {f}:{ln} {name}')
```

```python
# flags.py: argparse dests never read as args.<dest> / getattr(args, "<dest>")
import re, subprocess, sys
for f in subprocess.check_output(['git','ls-files','*.py']).decode().split():
    s = open(f).read()
    for m in re.finditer(r'add_argument\(([^)]*)\)', s):
        a = m.group(1)
        d = re.search(r'dest\s*=\s*["\'](\w+)', a)
        opts = re.findall(r'["\'](-{1,2}[\w-]+|[a-z_]\w*)["\']', a.split('help=')[0])
        if d: dest = d.group(1)
        else:
            longs = [o for o in opts if o.startswith('--')]
            pos = [o for o in opts if not o.startswith('-')]
            dest = (longs[0][2:] if longs else pos[0] if pos else opts[0].lstrip('-')).replace('-', '_')
        ln = s[:m.start()].count('\n') + 1
        n = len(re.findall(r'\.' + dest + r'\b', s)) + len(re.findall(r'["\']' + dest + r'["\']', s))
        if n == 0: print(f'UNREAD {f}:{ln} {dest}')
        else: print(f'ok     {f}:{ln} {dest} {n}', file=sys.stderr)
```

```python
# subflags.py: per qgen subcommand, flags its handler (and qgen/patch_notes functions it calls, transitively) never read
import ast, re
srcs = {m: open(f'authoring/tools/{m}.py').read() for m in ('qgen', 'patch_notes')}
funcs = {}
for m, s in srcs.items():
    for n in ast.parse(s).body:
        if isinstance(n, ast.FunctionDef): funcs[n.name] = n
def reach(name, seen):
    if name in seen or name not in funcs: return
    seen.add(name)
    for c in ast.walk(funcs[name]):
        if isinstance(c, ast.Name) and c.id in funcs: reach(c.id, seen)
        if isinstance(c, ast.Attribute) and c.attr in funcs: reach(c.attr, seen)
def reads(names):
    out = set()
    for n in names:
        for c in ast.walk(funcs[n]):
            if isinstance(c, ast.Attribute) and isinstance(c.value, ast.Name) and c.value.id == 'args': out.add(c.attr)
            if isinstance(c, ast.Call) and getattr(c.func, 'id', '') == 'getattr' and len(c.args) > 1 and isinstance(c.args[1], ast.Constant): out.add(c.args[1].value)
            if isinstance(c, ast.Call) and getattr(c.func, 'id', '') == 'vars': out.add('*')
    return out
main = funcs['main']; s = ast.unparse(main)
parsers = {}  # var -> (cmd name, handler, [dests])
for st in ast.walk(main):
    if isinstance(st, ast.Call) and isinstance(st.func, ast.Name) and st.func.id == 'add':
        name, fn = st.args[0].value, st.args[1].id
        model = len(st.args) > 2 or any(k.arg == 'model' for k in st.keywords)
        run = not any(k.arg == 'run' and k.value.value is False for k in st.keywords)
        parsers[id(st)] = (name, fn, (['run'] if run else []) + (['model', 'jobs'] if model else []))
# map variables to add() calls / sub-parsers
var = {}
for st in ast.walk(main):
    if isinstance(st, ast.Assign) and isinstance(st.targets[0], ast.Name) and isinstance(st.value, ast.Call):
        var[st.targets[0].id] = st.value
handler = {}
for st in ast.walk(main):
    if isinstance(st, ast.Call) and isinstance(st.func, ast.Attribute) and st.func.attr == 'set_defaults':
        tgt = st.func.value
        for k in st.keywords:
            if k.arg == 'fn': handler[tgt.id if isinstance(tgt, ast.Name) else id(tgt)] = ast.unparse(k.value).split('.')[-1]
for st in ast.walk(main):
    if isinstance(st, ast.Call) and isinstance(st.func, ast.Attribute) and st.func.attr == 'add_argument':
        tgt = st.func.value
        opts = [a.value for a in st.args if isinstance(a, ast.Constant)]
        dest = next((k.value.value for k in st.keywords if k.arg == 'dest'), None) or next((o[2:] for o in opts if o.startswith('--')), opts[0]).replace('-', '_')
        if isinstance(tgt, ast.Call) and id(tgt) in parsers: parsers[id(tgt)][2].append(dest)
        elif isinstance(tgt, ast.Name) and tgt.id in var and id(var[tgt.id]) in parsers: parsers[id(var[tgt.id])][2].append(dest)
        elif isinstance(tgt, ast.Name) and tgt.id in handler: parsers.setdefault(tgt.id, (tgt.id, handler[tgt.id], []))[2].append(dest)
        else: print('?', ast.unparse(st))
for name, fn, dests in parsers.values():
    seen = set(); reach(fn, seen); r = reads(seen)
    miss = [d for d in dests if d not in r and '*' not in r]
    print(f'{name:12} {fn:20} {len(seen):3} fns  flags {dests}  UNREAD {miss}' if miss else f'{name:12} ok ({len(dests)})')
```

### Markers

Task 528, 2026-10-13, run from the repo root over every tracked file except `tasks.sql`, `plans/`, `code-review.md` and `authoring/data/`; `.json` data hits (Spanish «todo») dropped by eye.

- `git ls-files app authoring | grep -v '\.json$' | xargs grep -nE 'PLACEHOLDER|\b(TODO|FIXME|XXX|HACK)\b'`: 2 hits, both `PLACEHOLDER_IDS` in `authoring/steam/steam.py`
- `git ls-files | grep -vE '^(tasks\.sql|plans/|code-review\.md)' | xargs grep -nIiE 'placeholder|\b(todo|fixme|xxx|hack)\b'`: rest are `todo` work-list locals (`qgen.py`, `media.py`, `release_check.py`), HTML `placeholder=` attributes, `placeholder` locale keys, `--placeholder` CSS variable
- No `PLACEHOLDER(<task id>)` anywhere in `app/` or `authoring/` code or locales (the last ones went before this milestone, e.g. `task 140: UI-7`); no `TODO`/`FIXME`/`XXX`/`HACK` comment; so no stale or non-numeric marker

| file | finding | category | severity | status |
|---|---|---|---|---|
| `app/client/src/game/theme.css`, `app/client/src/game/Question.svelte` | CSS variable `--placeholder` (pink dashed border) now used only by `.media-missing`; name suggests the `PLACEHOLDER(<task id>)` marker style, which no screen uses | inconsistency | low | handed to part 5 |
| `authoring/steam/steam.py` | `PLACEHOLDER_IDS` (Spacewar app 480 for `--dry-run`) reads like an AGENTS.md `PLACEHOLDER(<task id>)` marker in greps; e.g. `DRY_RUN_IDS` | inconsistency | low | handed to part 6 |
| all tracked code in scope | no findings: no `PLACEHOLDER(<task id>)`, `TODO`, `FIXME`, `XXX`, `HACK` | — | — | — |

### Bad-practice patterns

Task 529, 2026-10-13, run from the repo root. AST scans, not greps (a grep can't tell `as` casts from `{#each … as x}` or `import { a as b }`): throw-away scripts in `/tmp` (deleted after; reproduced below). Hotspot list for parts 2–9; only the sites below got a row, every other hit is deliberate or harmless.

- TS/JS: `node scan.mjs` over `git ls-files app authoring` `.ts`/`.svelte`/`.mjs`/`.cjs`/`.js` (116 files; `.svelte`: `<script>` blocks only, markup expressions not scanned), TypeScript compiler API from the root `node_modules`
  - `any` = `AnyKeyword`; `as` = `AsExpression` minus `as const`; `nonnull` = `NonNullExpression`; `tsignore` = `@ts-ignore`/`@ts-expect-error`/`@ts-nocheck`; `emptycatch` = `catch` with empty block; `logcatch` = `catch` whose body is only `console.*`; `dotcatch` = `.catch(fn)` with empty or log-only body or a constant result (`() => null`, `() => false`)
- Python: `python3 py.py` over `git ls-files app authoring` `.py` (32 files), `ast`
  - `bare` = `except:`; `broad` = `except Exception`/`BaseException`; `broad_pass` = broad with only `pass`/`continue`; `return_none` = handler ending in `return`/`return None` with no print/log call; `type_ignore` = `# type: ignore`
  - Any type with a `pass`/`continue`-only body: only `nasa.py:80` (one-liner over `ast.ExceptHandler`)
- Linter evidence (part 10), totals per pattern and rule:
  - `any` 15 (lint: no-explicit-any): 13 are `Record<string, any>` at the save JSON boundary (`engine/save.ts` 10, `state.ts` 1, `lib/api.ts` 1, `selection.test.ts` 2) + `selection.test.ts` `result: any`
  - `as` 118 (no stock rule; typescript-eslint `consistent-type-assertions` with `assertionStyle: never` would flag all): 23 in tests; 1 `as unknown as` (`RevisionPanel.svelte:34`); `engine/game.ts` 30, mostly `unknown` → `number`/`string` after a `typeof` check in request validation
  - `!` 74 (lint: no-non-null-assertion): 19 in tests; `engine/game.ts` 16, `Fireworks.svelte` 11 (canvas context)
  - `@ts-ignore`/`@ts-expect-error` 0 (lint: ban-ts-comment)
  - empty `catch {}` 7 (lint: no-empty; `allowEmptyCatch` off), log-only `catch` 1, empty/constant `.catch(() => …)` 21 (lint: no-empty-function for the 13 `() => {}`; no stock rule for `() => null`/`() => false`)
  - of the 29 catch hits: 3 are mutex chains whose failures go to the caller (`lib/engine.ts:134`, `lib/store.ts:27`, `desktop/main.mjs:82`), 5 `media.play()` / `requestFullscreen()` autoplay refusals, 4 commented best-effort (`sound.svelte.ts`, `resolve.mjs` bad URL), 8 in authoring scripts (`smoke.mjs`, `screenshots.mjs`, `cdp.mjs`: polling and shutdown), 5 optional reads with a fallback (outlook, Steam language/input types/text input, jokers used); the rest are rows below
  - Python: bare `except:` 0, broad 10 (all print/collect the error except `nasa.py:80` and `qgen.py:238`, both with a `noqa: BLE001` reason), broad + `pass`/`continue` 1, silent `return None` 2 (`save.py:36` `FileNotFoundError` = no save yet; `qgen.py:257` `ValueError` on an unparsable reset date), `# type: ignore` 0

TS/JS counts per file (blank = 0; files with no hit omitted):

| file | any | as | ! | ts-ignore | catch {} | catch log-only | .catch(() => …) |
|---|---|---|---|---|---|---|---|
| `app/client/src/engine/game.ts` |  | 30 | 16 |  |  |  |  |
| `app/client/src/engine/choice.test.ts` |  | 7 | 11 |  |  |  |  |
| `authoring/tools/sim/simulate.ts` |  | 5 | 7 |  |  |  |  |
| `app/client/src/engine/save.ts` | 10 | 1 |  |  |  |  |  |
| `app/client/src/game/Fireworks.svelte` |  |  | 11 |  |  |  |  |
| `app/client/src/engine/game.test.ts` |  | 7 | 2 |  |  |  |  |
| `app/client/src/engine/selection.test.ts` | 3 | 4 | 2 |  |  |  |  |
| `app/client/src/game/Overlay.svelte` |  | 1 | 3 |  |  |  | 4 |
| `app/client/src/engine/api.ts` |  | 7 |  |  |  |  |  |
| `app/client/src/engine/pool.ts` |  | 7 |  |  |  |  |  |
| `app/client/credits.ts` |  | 6 |  |  |  |  |  |
| `app/client/src/game/Question.svelte` |  | 3 | 1 |  |  |  | 2 |
| `authoring/ui/src/review/Review.svelte` |  | 3 | 3 |  |  |  |  |
| `app/client/src/game/Choice.svelte` |  | 2 | 2 |  |  |  | 1 |
| `app/client/src/game/sound.svelte.ts` |  | 3 |  |  | 2 |  |  |
| `app/client/src/engine/selection.ts` |  |  | 4 |  |  |  |  |
| `app/client/src/lib/engine.ts` |  | 2 |  |  |  |  | 2 |
| `authoring/ui/src/review/RevisionPanel.svelte` |  | 3 | 1 |  |  |  |  |
| `app/client/src/engine/pool.test.ts` |  | 1 | 2 |  |  |  |  |
| `app/client/src/engine/save.test.ts` |  | 1 | 2 |  |  |  |  |
| `app/client/src/engine/state.ts` | 1 | 2 |  |  |  |  |  |
| `app/client/src/game/Game.svelte` |  |  |  |  |  |  | 3 |
| `app/client/src/lib/i18n.ts` |  | 3 |  |  |  |  |  |
| `authoring/steam/smoke.mjs` |  |  |  |  | 2 |  | 1 |
| `authoring/tools/cdp.mjs` |  |  |  |  | 1 |  | 2 |
| `app/client/src/engine/outlook.test.ts` |  | 2 |  |  |  |  |  |
| `app/client/src/engine/outlook.ts` |  |  | 2 |  |  |  |  |
| `app/client/src/lib/api.ts` | 1 | 1 |  |  |  |  |  |
| `app/client/src/lib/errors.ts` |  | 2 |  |  |  |  |  |
| `app/client/src/lib/focus.ts` |  | 2 |  |  |  |  |  |
| `app/client/src/lib/gamepad.svelte.ts` |  | 1 |  |  |  |  | 1 |
| `app/desktop/main.mjs` |  |  |  |  |  | 1 | 1 |
| `authoring/store/screenshots.mjs` |  |  |  |  |  |  | 2 |
| `app/client/src/engine/pycompat.ts` |  |  | 1 |  |  |  |  |
| `app/client/src/engine/test/fixtures.ts` |  | 1 |  |  |  |  |  |
| `app/client/src/game/Credits.svelte` |  | 1 |  |  |  |  |  |
| `app/client/src/game/Customize.svelte` |  | 1 |  |  |  |  |  |
| `app/client/src/game/Glyph.svelte` |  | 1 |  |  |  |  |  |
| `app/client/src/game/JokerFlight.svelte` |  |  | 1 |  |  |  |  |
| `app/client/src/game/Player.svelte` |  |  |  |  |  |  | 1 |
| `app/client/src/game/Prompt.svelte` |  | 1 |  |  |  |  |  |
| `app/client/src/lib/data.ts` |  | 1 |  |  |  |  |  |
| `app/client/src/lib/gamepad.ts` |  | 1 |  |  |  |  |  |
| `app/client/src/lib/input.svelte.ts` |  | 1 |  |  |  |  |  |
| `app/client/src/lib/store.ts` |  |  |  |  |  |  | 1 |
| `app/client/src/locales/xx.ts` |  | 1 |  |  |  |  |  |
| `app/client/src/main.ts` |  |  | 1 |  |  |  |  |
| `app/client/vite.config.ts` |  | 1 |  |  |  |  |  |
| `app/desktop/resolve.mjs` |  |  |  |  | 1 |  |  |
| `app/desktop/save.mjs` |  |  |  |  | 1 |  |  |
| `authoring/tools/supply.ts` |  | 1 |  |  |  |  |  |
| `authoring/ui/src/main.ts` |  |  | 1 |  |  |  |  |
| `authoring/ui/src/review/SourcePanel.svelte` |  |  | 1 |  |  |  |  |
| `authoring/ui/src/stats/Stats.svelte` |  | 1 |  |  |  |  |  |
| total (54 of 116 files) | 15 | 118 | 74 | 0 | 7 | 1 | 21 |

Python counts per file (files with no hit omitted):

| file | bare | broad | broad + pass/continue | silent return None | type: ignore |
|---|---|---|---|---|---|
| `authoring/tools/qgen.py` |  | 6 |  | 1 |  |
| `authoring/tools/media.py` |  | 2 |  |  |  |
| `authoring/tools/providers/nasa.py` |  | 1 | 1 |  |  |
| `authoring/server/main.py` |  | 1 |  |  |  |
| `app/server/save.py` |  |  |  | 1 |  |
| total (5 of 32 files) | 0 | 10 | 1 | 2 | 0 |

| file | finding | category | severity | status |
|---|---|---|---|---|
| `app/client/src/game/Game.svelte` | `startGame`: `noteExhausted(…).catch(() => {})` (line 279): a write failure still shows via `saveWarning()`, but an engine throw there (bad choice body) vanishes without a trace (lint: no-empty-function) | practice | low | handed to part 5 |
| `app/client/src/game/Overlay.svelte` | language `$effect` (line 191) `.catch(() => {})`: if `fetchLanguage()`/`localeSupply()` fails, the language rows just don't appear, no error shown or logged (lint: no-empty-function) | practice | low | handed to part 5 |
| `app/desktop/save.mjs` | `backup()`: `try { await fs.access(target); continue; } catch {}` treats every error (also `EACCES`) as "name is free"; harmless today because `rename` then fails loudly (lint: no-empty) | practice | low | handed to part 6 |
| `authoring/tools/providers/nasa.py` | line 80: `except Exception: continue` around the video asset fetch also hides programming errors (`KeyError`, bad JSON shape): every NASA video would silently drop out of the search | practice | low | handed to part 8 |
| all TS/JS and Python in scope | no `@ts-ignore`/`@ts-expect-error`, no bare `except:`, no `# type: ignore`; no swallowed error on a save, LLM or media-download path | — | — | — |

```js
// scan.mjs (TS/JS); `ln -s $PWD/node_modules /tmp/bp529/` first
import ts from "./node_modules/typescript/lib/typescript.js";
import { execSync } from "node:child_process";
import { readFileSync } from "node:fs";
const files = execSync("git ls-files app authoring", { encoding: "utf8" }).split("\n").filter((f) => /\.(ts|svelte|mjs|cjs|js)$/.test(f));
const K = ["any", "as", "nonnull", "tsignore", "emptycatch", "logcatch", "dotcatch"];
const isLog = (s) => ts.isExpressionStatement(s) && ts.isCallExpression(s.expression) &&
  /^console\.(log|warn|error|info|debug)$/.test(s.expression.expression.getText());
for (const f of files) {
  const src = readFileSync(f, "utf8");
  const blocks = f.endsWith(".svelte") ? [...src.matchAll(/<script[^>]*>([\s\S]*?)<\/script>/g)].map((m) => m[1]) : [src];
  const c = Object.fromEntries(K.map((k) => [k, 0]));
  for (const code of blocks) {
    const sf = ts.createSourceFile(f, code, ts.ScriptTarget.Latest, true, /\.(m?js|cjs)$/.test(f) ? ts.ScriptKind.JS : ts.ScriptKind.TS);
    c.tsignore += (code.match(/@ts-(ignore|expect-error|nocheck)/g) ?? []).length;
    const walk = (n) => {
      if (n.kind === ts.SyntaxKind.AnyKeyword) c.any++;
      if (ts.isAsExpression(n) && !(ts.isTypeReferenceNode(n.type) && n.type.typeName.getText() === "const")) c.as++;
      if (ts.isNonNullExpression(n)) c.nonnull++;
      if (ts.isCatchClause(n)) {
        const st = n.block.statements;
        if (st.length === 0) c.emptycatch++; else if (st.every(isLog)) c.logcatch++;
      }
      if (ts.isCallExpression(n) && ts.isPropertyAccessExpression(n.expression) && n.expression.name.text === "catch") {
        const a = n.arguments[0];
        if (a && (ts.isArrowFunction(a) || ts.isFunctionExpression(a))) {
          const b = a.body;
          if (ts.isBlock(b) ? b.statements.every(isLog) : ts.isLiteralExpression(b) || ts.isIdentifier(b) && b.text === "undefined" ||
              [ts.SyntaxKind.NullKeyword, ts.SyntaxKind.TrueKeyword, ts.SyntaxKind.FalseKeyword].includes(b.kind) ||
              ts.isObjectLiteralExpression(b) || ts.isArrayLiteralExpression(b) || ts.isCallExpression(b) && /^console\./.test(b.expression.getText())) c.dotcatch++;
        }
      }
      ts.forEachChild(n, walk);
    };
    walk(sf);
  }
  if (K.some((k) => c[k])) console.log(f, JSON.stringify(c));
}
```

```python
# py.py
import ast, subprocess, re, collections
files = [f for f in subprocess.run(['git', 'ls-files', 'app', 'authoring'], capture_output=True, text=True).stdout.split() if f.endswith('.py')]
LOG = re.compile(r'\b(print|log\w*|warn\w*|logger|logging|sys\.stderr|_err|fail|die)\b')
for f in files:
    src = open(f).read(); c = collections.Counter(type_ignore=len(re.findall(r'#\s*type:\s*ignore', src)))
    for n in ast.walk(ast.parse(src)):
        if not isinstance(n, ast.ExceptHandler): continue
        t = ast.unparse(n.type) if n.type else None; txt = ' '.join(ast.unparse(s) for s in n.body)
        broad = t is None or re.search(r'\b(Exception|BaseException)\b', t)
        c['bare' if t is None else 'broad' if broad else 'other'] += 1
        if broad and all(isinstance(s, (ast.Pass, ast.Continue)) for s in n.body): c['broad_pass'] += 1
        r = n.body[-1]
        if isinstance(r, ast.Return) and (r.value is None or isinstance(r.value, ast.Constant) and r.value.value is None) and not LOG.search(txt):
            c['return_none'] += 1
    if any(v for k, v in c.items() if k != 'other'): print(f, dict(c))
```

### Sync IO and globals

Task 530, 2026-10-13, run from the repo root. Request handlers read by hand (`app/server/{http_base,main,save,media_cache}.py`, `authoring/server/*.py` and the `authoring/tools` functions they call, `app/desktop/{main,resolve,save}.mjs`); costs timed by a throw-away script on the live data (1211 source questions, `questions.json` 3.6 MB, `app/data/pool.json` 1.9 MB, `media/` 3.1 GB, largest file a 117 MB `.webm`).

- Desktop: `grep -nE 'Sync\(|readFile|writeFile|protocol\.handle|ipcMain|^let ' app/desktop/*.mjs app/desktop/preload.cjs`
- Python globals: AST script over `git ls-files app authoring` `.py`: module-level assignments of a dict/list/set/`Lock()`, names under a `global` statement, module attributes set from another module
- TS module state: `grep -n '^let \|^export let \|^var ' -r app/client/src authoring/ui/src authoring/tools/*.ts authoring/tools/*.mjs authoring/tools/sim authoring/store authoring/steam app/client/scripts` and `grep -nE '^(export )?const \w+ = \$state|^(export )?const \w+ = new (Map|Set)|^(export )?const \w+(: [^=]+)? = (\[\]|\{\})' -r app/client/src authoring/ui/src app/desktop --include='*.ts' --include='*.mjs'` (minus `node_modules`, tests)
- Timings (ms per call, warm): game `pool_urls()` 10, authoring `pool_urls(questions.json)` 21, `load_pool()` 20, `GET /api/questions` (`with_extras` over all) 102, `GET /api/overview` (`overview.build`) 155

| file | finding | category | severity | status |
|---|---|---|---|---|
| `app/server/http_base.py` | `send_file` reads the whole file into memory (`read_bytes`) and ignores `Range`: a `/media` video (up to 117 MB) is held in RAM per request, parallel `preload="auto"` requests multiply it, and the browser game can't seek or stream it; the desktop resolver (`resolve.mjs` `sendFile`) streams with `Range` | performance | medium | handed to part 2 |
| `app/server/http_base.py`, `app/server/media_cache.py` | `send_media` → `pool_urls()` re-parses `pool.json` (1.9 MB, ~10 ms) on every `/media` request; desktop reads it once at start (`resolve.mjs` `makeResolver`); an mtime-keyed cache keeps `qgen export` visible without restart | performance | low | handed to part 2 |
| `app/server/main.py`, `app/server/save.py` | no findings: `/api/save` GET/PUT read/write one small file (fsync, `_lock`); startup-only `missing_media()` stats every pool file once | — | — | — |
| `authoring/server/main.py` | `send_media` parses `questions.json` (3.6 MB, ~21 ms) twice per `/media` request (own check, then `BaseHandler.send_media` with the same `pool_file`), then the whole-file read above | performance | low | handed to part 9 |
| `authoring/server/main.py` | `GET /api/questions`: full `load_pool()` plus per question 1–2 `work/media/` candidate files and an audit file (`with_extras`): ~100 ms for 1211 questions, linear in the pool (target 5000 per language) | performance | low | handed to part 9 |
| `authoring/server/main.py` | every POST parses `questions.json` 2–3 times (`find_question`/`target`, `update_question`, `item_of`) and rewrites it plus `pool_export.write` (~60+ ms per click) | performance | low | handed to part 9 |
| `authoring/server/overview.py` | `GET /api/overview` (~155 ms) re-reads the pool, every locale file, `work/*/run.json` and spawns Node (`engine.supplies`) per call; fine for a start page, no cache needed yet | performance | low | handed to part 9 |
| `authoring/server/main.py`, `authoring/server/spot_checks.py`, `authoring/tools/qgen.py` | `questions.json`, `questions.<locale>.json` and `spot-checks.json` writers lock per process only (`main._lock`, `spot_checks._lock`, `qgen._pool_lock`); a `qgen batch`/`fix` merging while the gamemaster reviews can lose one side's read-modify-write (no file lock, no mtime check) | bug | medium | handed to part 10 |
| `authoring/server/main.py` | sets `download.WAIT_ON_RATE_LIMIT = False` on another module at import: process-wide switch, also for any `download` caller in the same process | practice | low | handed to part 9 |
| `app/desktop/resolve.mjs` | `readPoolUrls` (`readFileSync` once at start, fine) swallows a missing/corrupt `pool.json` (`catch { return new Set() }`): every `/media` then answers `not_found`, not `media_missing`, with no log | practice | low | handed to part 6 |
| `app/desktop/main.mjs`, `app/desktop/save.mjs` | no findings: no `fs.*Sync` in the `app:` protocol or IPC handlers (`existsSync` only at start: Steam SDK dir, `dist/index.html`); save IO is `fs/promises` | — | — | — |
| `authoring/tools/qgen.py` | `_KEYS` (`id(q)` → keys cache for the overlap report) never pruned: grows for the process lifetime, the identity check only guards reuse | practice | low | handed to part 7 |
| `authoring/tools/download.py` | `_download_locks` keeps one `Lock` per URL ever downloaded (authoring server lifetime); small, but never pruned | practice | low | handed to part 8 |

Module-level mutable state (constant tables such as schemas, field lists, `LISTS`, `BANDS` left out); each owner part checks thread safety and lifetime:

| file | state | part |
|---|---|---|
| `app/server/main.py` | `_lock` (save writes) | 2 |
| `authoring/server/main.py` | `_lock` (source pool, translations); sets `download.WAIT_ON_RATE_LIMIT` | 9 |
| `authoring/server/spot_checks.py` | `_lock` | 9 |
| `authoring/tools/qgen.py` | `_save_lock`, `_pool_lock`, `_KEYS`, `_backaudits` (`global`, mtime-keyed index) | 7 |
| `authoring/tools/progress.py` | `_active`, `_drawn`, `_line_start` (`global`), `_waits` | 8 |
| `authoring/tools/download.py` | `_download_locks`, `_download_locks_lock`, `WAIT_ON_RATE_LIMIT` | 8 |
| `authoring/tools/providers/` | `__init__`: `_cooldown` + lock; `commons`: `_last_api_request` (`global`) + lock; `nasa`, `freesound`, `openverse`: `_last` (`global`) + lock; `openverse`: `_token` | 8 |
| `app/desktop/main.mjs` | `win`, `steam`, `steamTimer`, `steamInput`, `overlay`, `saveFile`, `localFile`, `writing` (mutex chain), `pending` | 6 |
| `app/desktop/stage-media.mjs` | `count`, `bytes`, `missing` (script) | 6 |
| `app/client/src/lib/engine.ts` | `loading`, `chain` (mutex chain), `lastSaveError` | 4 |
| `app/client/src/lib/data.ts` | `cache` (per-locale data promises, page lifetime) | 4 |
| `app/client/src/lib/i18n.ts` | `lang` (exported `let`), `catalog`, `numbers`, `plurals`, `warned` | 4 |
| `app/client/src/lib/input.svelte.ts` | `lastDevice`, `scopes` (`$state`), `stack`, `busy` | 4 |
| `app/client/src/lib/focus.ts` | `shown`, `tabbing`, `memory` | 4 |
| `app/client/src/lib/gamepad.svelte.ts` | `padStyle` (`$state`), `fromSteam`, `prev`, `warned` | 4 |
| `app/client/src/lib/names.svelte.ts` | `data` (`$state.raw`) | 4 |
| `app/client/src/game/sound.svelte.ts` | `sound` (`$state`), `ctx`, buses, `noiseBuffer`, `samples`, `samplesLoaded`, `samplesReady`, `current`, `synthMusic` | 5 |
| `app/client/scripts/check-literals.mjs` | `failed` (script) | 4 |
| `authoring/tools/supply.ts` | `raw` (stdin buffer) | 8 |
| `authoring/store/screenshots.mjs`, `authoring/steam/smoke.mjs` | `seed`, `page`/`evaluate`/`waitFor`/`click`; `step`, `page`/`h`/`home`/`display` (scripts) | 6 |

### Bundle baseline

Task 531, 2026-10-13, run from the repo root, Vite 8.3.3. Per-module sizes from a throw-away script (`/tmp`, deleted): Vite's `build()` API with each project's `vite.config.ts`, `outDir` in `/tmp` and a `generateBundle` plugin summing `chunk.modules[id].renderedLength` (tree-shaken, before minification) per module, directory and package; `vite-bundle-visualizer` not installed (offline). Desktop sizes from the existing `app/desktop/release/` (0.1.0, built 2026-10-13 03:42), no packaging run; `app.asar` contents from its JSON header.

- Build: `/usr/bin/env time -f "%e s wall" npm run build` → 1.66 s wall (client 652 ms, authoring 398 ms)
- Dist sizes: `du -sh app/client/dist/* authoring/ui/dist/*`, `find app/client/dist -type f | xargs du -b | sort -n`
- Desktop: `du -sh app/desktop/release/*-unpacked app/desktop/release/*-unpacked/resources/*`, `ls -la app/desktop/release`

| output | raw | gzip | notes |
|---|---|---|---|
| `app/client/dist/assets/App-*.js` | 142.7 kB | 45.7 kB | screens (lazy chunk); largest pre-minify: `Game.svelte` 39.8, `Question.svelte` 33.2, `Choice.svelte` 26.6, `Overlay.svelte` 25.6, `sound.svelte.ts` 19.7 kB |
| `app/client/dist/assets/engine-*.js` | 121.3 kB | 43.8 kB | engine + Svelte runtime + 4 locales; `engine/game.ts` 30.5, `locales/{de,es,en}.ts` ≈ 11.5 each pre-minify |
| `app/client/dist/assets/index-*.js` | 2.5 kB | 1.2 kB | boot |
| `app/client/dist/assets/App-*.css` | 70.6 kB | 12.4 kB | component styles; no inlined `data:` URLs |
| `app/client/dist/credits.json` | 687.7 kB | 95.8 kB | made by `credits.ts`; fetched only by the Credits screen |
| `app/client/dist/CREDITS.md` | 382.0 kB | — | shipped licence file |
| `app/client/dist/audio/` (public) | 2.8 MB | — | 26 `.m4a`; `victoria.m4a` 1.20 MB, three `musica-*.m4a` 0.24 MB each, `redoble.m4a` 0.20 MB |
| `app/client/dist/fonts/` (public) | 96 kB | — | `nunito.woff2` 39 kB, `baloo-2.woff2` 33 kB |
| client modules by source (pre-minify) | — | — | `src/game/` 255.9, `svelte` 146.9, `src/engine/` 55.9, `src/locales/` 36.8, `src/lib/` 27.6 kB |
| `authoring/ui/dist/assets/index-*.js` | 157.4 kB | 53.8 kB | one chunk; `Review.svelte` 50.3, `Home.svelte` 21.5, `MediaPanel.svelte` 12.9 kB pre-minify; game locales via `$app` 36.9 kB |
| `authoring/ui/dist/assets/index-*.css` | 26.2 kB | 6.1 kB | |
| `authoring/ui/dist/{audio,fonts}/` | 2.9 MB | — | the game's whole `public/` (`publicDir`) |
| `app/desktop/release/linux-unpacked` | 2.8 GB | — | 335 MB without `resources/media` (2.4 GB, 1102 files); `trivia-bin` 215 MB, `app.asar` 7.9 MB, `app.asar.unpacked` 4.4 MB, `resources/client` 4.3 MB, `resources/data` 1.9 MB |
| `app/desktop/release/win-unpacked` | 2.8 GB | — | 380 MB without media; `Trivia.exe` 229 MB, rest as Linux |
| `Trivia-0.1.0-linux-x64.tar.gz` / `-win-x64.zip` | 2.66 / 2.68 GB | — | media is already compressed |

| file | finding | category | severity | status |
|---|---|---|---|---|
| `app/client/dist`, `app/client/src` | no findings: one lazy `App` chunk for the screens, `credits.json` loaded on demand, no library pulled in for one function (only runtime dependency: `svelte`); the 4 eager locales (~13 kB gzip) are negligible offline | — | — | — |
| `authoring/ui/vite.config.ts` | `publicDir: "../../app/client/public"` copies the game's 2.8 MB `audio/` into `authoring/ui/dist/` as well, but the authoring pages need only `fonts/` (its own comment); built output only, not shipped | performance | low | handed to part 9 |
| `app/desktop/electron-builder.yml` | `app.asar` (7.9 MB) carries ~6 MB of build tooling from `steamworks-ffi-node`'s optional/transitive deps (`node-gyp`, `tar`, `undici` incl. `docs/`, `minipass`, `node-addon-api` headers, `koffi` `src/`, `doc/`, `vendor/`) never loaded at runtime; `files` exclusions would drop them (<0.3 % of the package, media dominates) | performance | low | handed to part 6 |
| `app/desktop/electron-builder.yml` | `CREDITS.md` (382 kB) shipped twice: `resources/client/CREDITS.md` (from `extraResources` `../client/dist`) and the install root (`extraFiles`) | inconsistency | low | handed to part 6 |
| `app/client/public/audio/victoria.m4a` | 1.2 MB, 43 % of all game audio; probably long or high bitrate (no `ffprobe` in the dev shell to check); re-encode only if the gamemaster wants it smaller | performance | low | won't fix: audio content is out of scope (milestone 13), 1.2 MB is nothing next to 2.4 GB media |

## Part 2: Python game server

Plan 74 reviews `app/server/` and `authoring/tools/categories.py`, and logs the referee files deleted by task 302.

| file | finding | category | severity | status |
|---|---|---|---|---|
| `app/server/save.py` | write lock lived in `main.py` (`_lock`), so `save.write` wasn't safe on its own (one shared `game.json.tmp`); moved into `save.write`. Part 1 row "`main.py`, `save.py` no findings: … (fsync, `_lock`)": still holds, lock now in `save.py` | practice | low | fixed (task 532) |
| `app/server/save.py` | `check()` error said "version must be 2 or 4" while 3 is accepted too; now lists `LISTS` | inconsistency | low | fixed (task 532) |
| `app/server/save.py`, `app/client/src/engine/state.ts` | `SAVE_VERSION` bump needs `save.py` `VERSION`/`LISTS` too, else every PUT is 400 `bad_save` (task 625 had to); nothing said so: comment at `SAVE_VERSION` | bug | medium | fixed (task 532) |
| `app/server/save.py` | `game.json.tmp` stays when writing/fsync or a non-`PermissionError` `os.replace` fails | practice | low | won't fix: the next write overwrites it; nothing reads it |
| `app/server/save.py` | no directory fsync after `os.replace` (rename may be lost on power cut) | bug | low | won't fix: no directory fsync on Windows; desktop `save.mjs` same; the save is rewritten on every action |
| `app/server/save.py` | `migrate()`: a game's `state` that isn't JSON or `flags.json` without `"flags"` raises at start, `trivia` doesn't start; source untouched (read-only URI, copy), no partial `game.json` (atomic write), idempotent while `game.json` exists (checked: legacy `game.sqlite` + `flags.json` copy, run twice, byte-identical) | bug | low | won't fix: only pre-PORT-5 dev installs; failing loudly keeps the backup |
| `app/server/save.py` | `migrate()` runs again if `game.json` is deleted while `game.sqlite` remains: old games come back | bug | low | won't fix: documented backup; desktop has no `game.sqlite`; rename it to start fresh |
| `app/server/save.py` | part 1 scan: silent `return None` at `load()` (`FileNotFoundError`) | practice | — | won't fix: no save yet = 404, `ServerStore.load` → `emptySave()` |
| `app/server/save.py`, `app/desktop/save.mjs` | duplication candidate: atomic write + lock retries, `MAX_BYTES` 10 MB, envelope check; drift: desktop accepts any numeric version and retries `EPERM`/`EBUSY`/`EACCES`, Python only versions 2–4 and `PermissionError` | complexity | low | handed to part 10 |
| `app/server/save.py`, `authoring/tools/save_file.py`, `app/client/src/engine/save.ts` | duplication candidate: `save_file.py` re-implements the v2→v3 (burned → seen/blocked) and v3→v4 (reports → flags) upgrades of `engine/save.ts` `UPGRADES` in Python | complexity | medium | handed to part 10 |
| `app/server/paths.py` | stale comments "the game reads it from AG-7 on / BN-6 on" on `AGE_GROUPS`/`BUNDLES` | inconsistency | low | fixed (task 532) |
| `app/server/paths.py` | `TRIVIA_DIST` override: set nowhere, documented nowhere; removed | unused | low | fixed (task 532) |
| `app/server/paths.py` | `POOL` aside, `CATEGORIES`, `BUNDLE_DATA`, `AGE_GROUPS`, `BUNDLES`, `locale_pool`, `names` are used only by authoring (`categories.py`, `qgen.py`, `layout.py`) | unused | low | won't fix: they name `app/data/` files; authoring may import `app/` |
| `app/server/paths.py` | `TRIVIA_STATE`/`TRIVIA_MEDIA`: `~` not expanded, relative = from cwd; `state/` created on first write, media cache never created (read-only); separators via `Path` | bug | low | won't fix: shells expand unquoted `~`, the flake wrapper sets absolute paths; same as `TRIVIA_WORK` |
| `app/server/paths.py`, `authoring/tools/layout.py` | duplication candidate: `layout.py` re-exports `app_paths` under other names (`EXPORT` = `POOL`, `LOCALE_POOL`, `NAMES`), and both define `BUNDLE_DATA` with different meanings (`app/data/bundles` vs `authoring/data/bundles`) | inconsistency | low | handed to part 10 |
| `app/server/http_base.py` | part 1 row "`send_file` reads the whole file into memory (`read_bytes`) and ignores `Range` …": now streamed in 1 MB chunks, single `Range` → 206/416 (`parse_range`, same rules as `resolve.mjs` `parseRange`), `Accept-Ranges`; dropped connections ignored; also for the authoring server (checked: 89 MB `.webm` full and ranged byte-identical) | performance | medium | fixed (task 533) |
| `app/server/media_cache.py`, `app/server/http_base.py` | part 1 row "`send_media` → `pool_urls()` re-parses `pool.json` … on every `/media` request": `pool_urls` cached per path, keyed on mtime + size, so `qgen export` and authoring edits still show without restart; also makes the authoring double call cheap | performance | low | fixed (task 533) |
| `app/server/main.py`, `app/server/http_base.py` | `PUT /api/save` with a non-numeric `Content-Length`: `int()` raised outside any `try`, handler crashed (traceback, connection dropped, no answer); negative length read until EOF. Now `content_length()` → 400 `bad_save`; authoring `read_body` gets the same `ValueError` it already catches | bug | low | fixed (task 533) |
| `app/server/http_base.py` | `send_static`: `dist/` present without `index.html` (half build) crashed every page request; now 503 like a missing `dist/` | bug | low | fixed (task 533) |
| `app/server/http_base.py` | error bodies `{"error": "<sentence>"}` (not in pool, client not built) unlike `error_body`'s `{"error": code, "message"}`: now `not_found` / `not_built` + `message`; nothing reads them | inconsistency | low | fixed (task 533) |
| `app/server/main.py` | docstring "Any other /api/ path or method: 404": DELETE/HEAD/… get http.server's 501 HTML; docstring now says so (and mentions `Range`). Routes match decision 4 (static, `/data/`, cache-only `/media`, `/api/save`); referee routes already gone (task 303) | inconsistency | low | fixed (task 533) |
| `app/server/main.py`, `app/server/http_base.py` | path traversal checked raw (`curl --path-as-is`): `/data/..`, `/data/%2e%2e`, `/data//etc/passwd`, `..%5c` → 404; static `..` → `index.html`; `resolve()` + `is_relative_to` also covers Windows `\`. Side effect: paths aren't percent-decoded, so a `/data/` or `dist/` file name with a space or non-ASCII would 404 | bug | low | won't fix: every `app/data/` and Vite asset name is an ASCII slug/hash |
| `app/server/http_base.py` | unknown `/assets/x.js` (stale tab after a rebuild) gets `index.html` 200 `text/html`, not 404 | practice | low | won't fix: a reload fixes it; desktop `resolve.mjs` the same |
| `app/server/http_base.py` | content types from `mimetypes` (system tables: `/etc/mime.types`, Windows registry), desktop has a fixed `MIME` map; every cached media extension (`jpg`, `jpeg`, `png`, `gif`, `tiff`, `webp`, `mp3`, `ogg`, `oga`, `wav`, `webm`) and `js`/`css`/`json` map correctly here; `.html`/`.json` without `charset` | inconsistency | low | won't fix: `trivia` runs on Linux/nix only (Windows is the desktop shell); pages declare UTF-8, JSON is UTF-8 by spec |
| `app/server/http_base.py`, `app/server/main.py` | an exception in a handler (e.g. unreadable file) isn't turned into a 500: http.server prints the traceback and drops the connection | practice | low | won't fix: the client treats it like a failed fetch (save warning); the traceback is in the terminal |
| `app/server/main.py` | `--host 0.0.0.0` exposes `PUT /api/save` to the LAN without auth; startup media line and `save.migrate()` run before bind; a missing `app/data/pool.json` stops the start with a traceback | practice | low | won't fix: default `127.0.0.1`; `pool.json` is tracked |
| `app/server/media_cache.py`, `app/desktop/resolve.mjs`, `app/desktop/stage-media.mjs` | duplication candidate: `cache_path` ↔ `cacheName` and `pool_urls`/`picked` ↔ `poolUrls` (desktop: optional `media`, Python: `q["media"]` required); `authoring/tools/download.py` imports `cache_path`, no copy there | complexity | low | handed to part 10 |
| `app/server/game.py` | Python referee; part 1 row "`app/server/game.py`, `app/server/selection.py`, `app/server/flags.py`, `authoring/tools/record_fixtures.py` \| Python referee: deleted (task 303), not scanned": final status | unused | — | removed (task 302) |
| `app/server/selection.py` | Python referee's question selection (engine: `selection.ts`) | unused | — | removed (task 302) |
| `app/server/flags.py` | Python referee's flag store (engine: save `flags`) | unused | — | removed (task 302) |
| `authoring/tools/categories.py` | malformed `categories.json`, `bundles.json` or `names.<locale>.json` (bad JSON, missing `"categories"`/`"bundles"`, wrong type) raised a bare `JSONDecodeError`/`KeyError` naming no file (in `qgen validate`, the pipeline, `/api/categories`); now `_read` → `ValueError("<path>: …")`; missing file unchanged: a bundle without one has none (checked on a temp copy) | practice | low | fixed (task 534) |
| `authoring/tools/categories.py` | `import paths` and `from paths import …` side by side for one module; now one `from paths import` | inconsistency | low | fixed (task 534) |
| `authoring/tools/categories.py` | no cache: `load`/`broad_of`/`bundle_of` re-read every bundle's file on each call (`concepts.path` → `bundle_of` per subcategory) | performance | low | won't fix: ~0.08 ms per call, 341 `load()` calls ≈ 30 ms of a 0.3 s `qgen validate`; uncached keeps hand edits and `qgen bundle add` visible to the authoring server |
| `authoring/tools/categories.py` | `load("<unknown bundle>")` returns `[]` silently | bug | low | won't fix: callers check the bundle first (`qgen.py` `check_bundle`, `bundles.json` ids) |
| `app/client/src/engine/pool.ts` | header comment "Mirrors app/server/categories.py": moved to `authoring/tools/` (task 302) | inconsistency | low | fixed (task 534) |
| `authoring/tools/categories.py`, `app/client/src/engine/pool.ts`, `app/client/src/lib/data.ts` | duplication candidate: `load`/`subcategories`/`broad_of`/`bundle_of` ↔ `pool.ts` `loadCategories`/`subcategories`/`broadOf`/`bundleOf`, `load_names` ↔ `data.ts` `mergeNames`, the per-bundle file rule (`base` → `app/data/`, else `bundles/<id>/`) ↔ `data.ts` `loadEngineData` and `paths.py` `names`; two languages, small, comments point to each other | complexity | low | handed to part 10 |

## Part 3: TS engine

Plan 75 reviews `app/client/src/engine/` with its tests and `test/` helpers, not the fixture JSON.

| file | finding | category | severity | status |
|---|---|---|---|---|
| `app/client/src/engine/game.ts`, `app/client/src/engine/choice.ts` | 921 lines, six concerns in one file; the choice/settings part (`JOKERS`, `CARDS`, `STANDARD_JOKERS`, `DEFAULT_AGE_GROUP`, `*_MAX`, `defaultChoice`, `gameChoice`, `resolveBundles`, `ChoiceInput`, `CHOICE_KEYS`, `check*`, `checkBudget`, `resolveChoice`, `rangesFor`, `mediaAllowed`) depends on nothing else in it: moved to the new `engine/choice.ts`; `game.ts` re-exports what `lib/api.ts`, `outlook.ts`, the tests and `sim/simulate.ts` import, so the public surface is unchanged; `game.ts` 921 → 776 lines; `directory.md` updated | complexity | medium | fixed (task 535) |
| `app/client/src/engine/game.ts` | the other split candidates (supply/availability, jokers, cheats, core flow) share `draw`, `backToSelect`, `putOn`, `availableNow`, `running`/`saveGame`: separate modules would need circular imports or passing those helpers around | complexity | low | won't fix: sections are already marked; moving them only spreads one state machine over files |
| `app/client/src/engine/game.ts` | part 1 row "23 exports used only in their own file: `game.ts` `JOKERS`, `gameMode`, `ChoiceInput`, `cardsOf`, `mediaAllowed`, `availableNow`, `ChoiceArgs`, `leaveQuestion`, `dropCurrent`, `backToSelect`, `laterFill`, `categoryCandidates`, `JokerArgs` … (lint: none, unused export)": `export` dropped from `gameMode`, `cardsOf`, `availableNow`, `leaveQuestion`, `dropCurrent`, `backToSelect`, `laterFill`, `categoryCandidates`, and from `replacement`, `jokersLeft`, `levelsOf` (same kind, not in the part 1 list); `JOKERS`, `ChoiceInput`, `mediaAllowed` now cross a module boundary (`choice.ts` → `game.ts`); `ChoiceArgs`, `JokerArgs` stay exported as the parameter types of the public `newGame`/`joker`. Part 1 `tsc --noUnusedLocals --noUnusedParameters`: 0 hits in `game.ts` then, 0 now (flags in `tsconfig.json`) | unused | low | fixed (task 535) |
| `app/client/src/engine/game.ts`, `app/client/src/game/Overlay.svelte` | `CARDS` («Como las cartas») exported but imported by nobody, while `Overlay.svelte` kept its own copy commented "the same as `CARDS` in engine/game.ts"; the overlay now imports it through `lib/api.ts` | inconsistency | low | fixed (task 535) |
| `app/client/src/engine/game.ts`, `app/client/src/engine/selection.ts`, `app/client/src/game/levels.ts` | three `levelsOf` with three signatures: `game.ts` (state → count), `selection.ts` (ranges → `[1..n]`), `game/levels.ts` (`Game` → count, with its own `DEFAULT_LEVELS = 12` next to `selection.LEVELS`); `game.ts`'s is now the private `levelCount` | inconsistency | low | fixed (task 535) for `game.ts`; `levels.ts` handed to part 5 |
| `app/client/src/engine/game.ts`, `app/client/src/engine/choice.ts` | part 1 row "`as` … `engine/game.ts` 30, mostly `unknown` → `number`/`string` after a `typeof` check in request validation": `(v as number)` after `Number.isInteger` in `checkDifficulty`, `checkCount`, `checkBudget`, `playSnipe` replaced by an `isInt` type guard / `typeof` narrowing; `as` (excluding `as const`) 38 → 27 over both files; the rest are `as JokerName`, `as unknown[]` for `includes`, the new-state literal and `Object.fromEntries` results (lint: typescript-eslint consistent-type-assertions) | practice | low | fixed (task 535) |
| `app/client/src/engine/game.ts`, `app/client/src/engine/choice.ts` | part 1 row "`!` … `engine/game.ts` 16": `askedCategories` filtered then re-looked-up with `!`, now `flatMap`; 15 remain, each behind a guard the type system can't see: `state.current!` only in question phase (checked at each action's entry), a preceding `filter(has)`, `draw` returning exactly `n`, `undo` ⇒ `last`, `resolveChoice` setting exactly one of `age_group`/`difficulty` (lint: no-non-null-assertion) | practice | low | fixed (task 535) for one; won't fix: the rest would re-check the phase checks |
| `app/client/src/engine/game.ts` | `supply_short` error built twice (`newGame`, `changeSettings`) with the same mapping; now `supplyShort(report)` | complexity | low | fixed (task 535) |
| `app/client/src/engine/game.ts` | `playSnipe` set `repeat: true` twice (`Object.assign` before `openIfNoCards`, then again after, because `open()` clears it with `cards` 0); once now, after `open()`, with a comment | complexity | low | fixed (task 535) |
| `app/client/src/engine/game.ts` | comments that lie: `JokerArgs` "main.py passes only these" (the game routes left `main.py` in PORT-8; `api.ts` passes them), `gamemasterOnly` "Undo, skip, replace, joker budget" without `level`/`settings` (D-88) | inconsistency | low | fixed (task 535) |
| `app/client/src/engine/game.ts` | undo across cheats: `undo` restores the snapshot before the last final answer with the current `settings` (joker budget, mid-game difficulty/bundles), so later `jumpLevel`/`replace`/skips/jokers are rolled back, but their seen rows (skip, `replace` with seen, sniped) and `blocked` stay and the rolled-back `offered` lets those seen questions be drawn again in this game; the restored question may lie outside bundles/difficulty changed after the answer | bug | low | won't fix: gamemaster-only, needs answer → cheat → undo; seen rows are history (plan 65), a re-drawn seen question comes last (lowest seen count first) |
| `app/client/src/engine/game.ts` | `repair()` (plan 91): if a dropped card can't be redrawn the table shrinks; with every card gone the game sits in `select` with nothing to pick (gamemaster: jump level; solo: abandon) | bug | low | won't fix: needs a patch that empties a level's range for this game; restart still works |
| `app/client/src/engine/game.ts` | `subcategory as string` (purge, `replaceCurrent`, `jokersView`): `PoolQuestion.subcategory` is `string \| null`, yet validated pools never have null (0 of 1136) | inconsistency | low | won't fix here: the type is `pool.ts`'s (task 537) |
| `app/client/src/engine/game.ts` | `replacement()` takes 9 positional parameters, two optional (`fill`, `cards`) | complexity | low | won't fix: private now, 4 callers in the same file |
| `app/client/src/engine/game.ts` | cost per action: `countOf`/`availableNow`/`rangesOf` recomputed per call; `view` in question phase runs 5 `trial`s (each `structuredClone` of the save) and a `replacement` per subcategory for «Cambiazo». Measured (throw-away `/tmp` script, `app/data/pool.json` 1136 questions, 169 actions through `engine/api.ts` + `MemoryStore`): `getGame` (view + supply) 3.2 ms avg | performance | low | won't fix: 3 ms per action on a TV game |
| `app/client/src/engine/game.ts` | unhandled states checked, none found: each action refuses the wrong phase (`no_cards`, `no_question`, `skip_not_question`, `joker_not_question`, `cheat_not_select`), a finished game is `no_game` (undo reopens won/lost, refuses abandoned), `cards` 0 opens the one card after every deal/refill/snipe/repair/`clearTable`, `levels` 1 (first answer wins) and 20 (12 age-group ranges stepped), jokers `null` = ∞ never 0; `MODES` (`newGame`, `api.outlook`) vs `BUILT_MODES` (`newGame`, `playerMode`, `Choice.svelte`) used consistently. Checked with the drive script: 5 configs (default, `cards` 0 + `levels` 1, `levels` 20 + `cards` 2 + mixed budget, custom difficulty without media, solo), every action; save + replies byte-identical before/after this task's changes (sha256), `npm test` 159/159 | — | — | — |
| `app/client/src/engine/game.ts`, `app/server/game.py` | duplication candidate (plan 75): `game.py` deleted (task 303, decision 25: Family test night on the TS engine); the frozen fixtures are the spec | complexity | — | won't fix: nothing left to duplicate |
| `app/client/src/engine/state.ts` | part 1 row "23 exports used only in their own file: … `state.ts` `SeenRow`, `HistoryEntry`, `LastAnswer` … (lint: none, unused export)": `export` dropped (they stay as parts of `SaveData`/`GameState`); the other `state.ts` exports each have a user outside the file. Part 1 `tsc --noUnusedLocals --noUnusedParameters`: 0 hits in `state.ts`, `save.ts`, `store.ts`, `api.ts` then, 0 now (flags in `tsconfig.json`) | unused | low | fixed (task 536) |
| `app/client/src/engine/store.ts`, `app/client/src/engine/test/save.ts` | part 1 row "`MemoryStore` exported, used only by `save.test.ts`: test helper in a shipped module, belongs in `engine/test/` (lint: none, unused export)": moved to `test/save.ts`; `store.ts` keeps only the `Store` interface (`lib/store.ts`); `directory.md` updated | unused | low | fixed (task 536) |
| `app/client/src/engine/state.ts` | `GameError.params` typed `Record<string, any>` while `ErrorInfo.params` (`lib/types.ts`) is `Record<string, unknown>`; now `unknown` (lint: typescript-eslint no-explicit-any) | practice | low | fixed (task 536) |
| `app/client/src/engine/state.ts` | `withDefaults` aliased its parameter (`const s = state`) | complexity | low | fixed (task 536) |
| `app/client/src/engine/state.ts` | comment that lies by omission: `SAVE_VERSION` "bump `app/server/save.py` VERSION/LISTS too", but `authoring/tools/save_file.py` branches on the version too | inconsistency | low | fixed (task 536) |
| `app/client/src/engine/state.ts` | cost per action: `transact` and every `trial` (5 per `view` in question phase) `structuredClone` the whole save. Measured (throw-away `/tmp` script, `app/data/pool.json`): normal save (1 KB) clone 0.01 ms, action 3.4 ms; synthetic 1.5 MB save (400 games, 20k seen rows, years of play) clone 14 ms, action 100 ms, `getGame` 86 ms, `parseSave` 7 ms | performance | low | won't fix: 0.1 s per action only after years of play; cloning only the running game would need `trial` callers to promise what they touch |
| `app/client/src/engine/state.ts` | rollback checked, no finding: `transact` with a mutation then a throw leaves the save byte-identical; 11 refused actions through `api.gameAction` (wrong phase, bad index/joker/level/budget/bundles, empty name, unknown action) return the input save untouched; `undo` is one level (`undo: null` in the snapshot), so clone size stays bounded per game | — | — | — |
| `app/client/src/engine/state.ts`, `app/client/src/locales/` | 11 of 44 error codes have no catalog text (`no_game`, `no_cards`, `card_invalid`, `no_question`, `answer_invalid`, `skip_not_question`, `budget_unknown_joker`, `budget_invalid`, `joker_unknown`, `nothing_to_undo`, `language_unknown`), so they would show the English message; the UI never sends those requests (phase-bound screens, `can_undo`, fixed lists); catalog extras `supply_level`, `save_locked` are lib-side keys | inconsistency | low | won't fix: internal codes by design (`es.ts` "codes without a key show the English message") |
| `app/client/src/engine/save.ts` | `parseSave` checked: non-JSON, array, null, missing/fractional/string version → `Error`; newer → `SaveNewerError`; v1 → v4 (burns → seen/blocked, `reports: []`), v3 → v4 (reports merged into flags, notes joined), a v1/v2 without `burned` refused. Validation stays shallow: row fields (`players[].name: 3`) and flag entries (`flags.q = "x"`) pass and only break later as `server_error` per action | practice | low | won't fix: only the game writes the save; deep validation would duplicate every type |
| `app/client/src/engine/save.ts`, `app/client/src/lib/api.ts` | `setFlag` throws a plain `Error`, not a `GameError`; `lib/api.ts` turns it into a 400 whose `error` code is the English text (no catalog key); reachable only with a non-string ID or a note over 500 letters (`FlagDialog` caps at `MAX_NOTE`) | inconsistency | low | handed to part 4 (`task 541: Review API client, types and errors`) |
| `app/client/src/engine/save.ts` | `defaultLanguage` falls back to `es` even when `es` isn't in the list (e.g. `fr` with questions `["de"]` → `es`) | bug | low | won't fix: `es` is the base pool and UI language, always shipped; `lib/engine.ts` resets a missing question locale to `es` anyway |
| `app/client/src/engine/api.ts` | `getGame`'s `player` argument: the client never passes it; it only validates the name (`cleanName`, result dropped) so a bad name is a 400 | unused | low | won't fix: 18 `get_game` fixture steps pass one (incl. a too-long name → 400); the frozen fixtures are the spec (decision 25: Family test night on the TS engine) |
| `app/client/src/engine/api.ts` | `outlook`: `body.players as number` twice after `Number.isInteger`; now a `typeof` guard (lint: typescript-eslint consistent-type-assertions) | practice | low | fixed (task 536) |
| `app/client/src/engine/api.ts` | body coercion and replies checked, no finding: `pyInt`/`pyTruthy`/`pyStr` follow the recorded Python routes; `GameError` → 400 (`getGame`) / 409 (the rest) with `{error, params, message, supply}`, unknown action → 404 `not_found`, any other throw reaches `lib/engine.ts` as `server_error`; `npm test` 159/159 unchanged | — | — | — |
| `app/client/src/engine/api.ts`, `app/client/src/lib/api.ts`; `engine/store.ts`, `lib/store.ts`; `state.ts`, `lib/types.ts` | duplication candidates (plan 75): `lib/api.ts` wraps the routes here but also builds some inline (`setFlag`, `fetchFlags`, jokers) — routes spread over two files; `engine/store.ts` is only the interface of `lib/store.ts`'s stores (no duplication); `state.ts` imports its shared types from `lib/types.ts` (no duplication) | complexity | low | handed to part 10 (`task 581: Part 10: consolidate client types and API clients`) |
| `app/client/src/engine/save.ts`, `app/server/save.py`, `app/desktop/save.mjs`, `authoring/tools/save_file.py` | duplication candidate (plan 75): the save format is checked/upgraded in three places (`parseSave`, `save.py` `LISTS` per version, `save_file.py` version branches); a format bump touches all three | complexity | low | handed to part 10 (`task 582: Part 10: Python ↔ Node/TS twins (save, paths, media cache, static serving)`) |
| `app/client/src/engine/selection.ts` | part 1 row "23 exports used only in their own file: … `selection.ts` `CategoryKey`, `SupplyLevel`, `DrawOptions` … (lint: none, unused export)": `export` dropped from `CategoryKey`, `SupplyLevel`; `DrawOptions` stays exported as the parameter type of the public `draw` (as `ChoiceArgs`, task 535). Part 1 `tsc --noUnusedLocals --noUnusedParameters`: 0 hits in `selection.ts`, `pool.ts`, `outlook.ts`, `rng.ts`, `pycompat.ts` then, 0 now (flags in `tsconfig.json`) | unused | low | fixed (task 537) |
| `app/client/src/engine/outlook.ts` | part 1 row "23 exports …: `outlook.ts` `seenPerLevel`, `OutlookChoice` … (lint: none, unused export)": `export` dropped (`api.ts`, `sim/simulate.ts` pass object literals) | unused | low | fixed (task 537) |
| `app/client/src/engine/pool.ts` | part 1 row "23 exports …: `pool.ts` `levelWeights` … (lint: none, unused export)": `export` dropped | unused | low | fixed (task 537) |
| `app/client/src/engine/pool.ts`, `app/client/src/engine/pool.test.ts` | part 1 row "`bundleOf` exported, used only by `pool.test.ts`: dead in the shipped engine (lint: none, unused export)": deleted; its asserts now read `broadOf(cats).get(…)?.bundle` | unused | low | fixed (task 537) |
| `app/client/src/engine/pool.ts`, `app/client/src/engine/game.ts`, `app/client/src/engine/outlook.ts` | `PoolQuestion.subcategory` typed `string \| null`, but `qgen validate` requires every question's subcategory in a bundle's categories (0 null of 1136; task 535's row): now `string`; the three `as string` in `game.ts` and `exhaustedSubs`' null check gone (lint: typescript-eslint consistent-type-assertions) | inconsistency | low | fixed (task 537) |
| `app/client/src/engine/pool.ts` | stale comment: `categoryOf` "(game.category_of)" points at the deleted `game.py` | inconsistency | low | fixed (task 537) |
| `app/client/src/engine/pool.ts` | parsers validate shallowly: `parsePool` checks only version + array (`as PoolQuestion[]`); `parseBundles`/`parseAgeGroups` destructure `any` (`Array.isArray` narrows `unknown` to `any[]`), `id`/`name`/`description`/`ages` unchecked; `loadCategories` casts both inputs; part 1's 7 `as` (lint: typescript-eslint no-unsafe-assignment, consistent-type-assertions) | practice | low | won't fix: shipped data written by `qgen export` and checked by `qgen validate`; `parseAgeGroups` checks what the engine relies on (12 ranges inside the window, derived weights) |
| `app/client/src/engine/pool.ts` | `bundlesFor` has no locale fallback: a pool locale missing from base's `languages` gives `defaultChoice` no base bundle, so every new game fails `resolveBundles` | bug | low | won't fix: data error, not reachable with `bundles.json` (base: es, en, de; `lib/data.ts` offers only locales with a pool) |
| `app/client/src/engine/pool.ts` | `12` in `parseAgeGroups` and `levelWeights` next to `selection.LEVELS` | practice | low | won't fix: the age-group format (D-22: 12 ranges per group, `rangesFor` steps them for other `levels`), not the game default |
| `app/client/src/engine/selection.ts` | part 1 row "`!` … `engine/selection.ts` 4": `cands.get`, `assignment.get` on keys built from the same `sorted`, `count.get` on ids from `cands` (lint: no-non-null-assertion) | practice | low | won't fix: each key is set in the line before |
| `app/client/src/engine/selection.ts` | `draw` runs a full `assign` (augmenting paths over every question and later level) per candidate tried. Measured (throw-away `/tmp` script, `app/data/pool.json` 1136 questions): 0.8–1.1 ms per `draw` | performance | low | won't fix: 1 ms per deal |
| `app/client/src/engine/selection.ts`, `app/server/selection.py` | duplication candidate (plan 75): `selection.py` deleted in PORT-8; no Python twin of `assign`/`draw`/`supply` left: `authoring/tools/supply.ts` and `sim/` import this module (decision 5) | complexity | — | won't fix: nothing left to duplicate |
| `app/client/src/engine/outlook.ts` | cost and decision 31 checked, no finding: `outlook` 0.7–1.4 ms per call (gamemaster, rr-competitive × 4, 20 levels, custom 1–15, all but 30 seen), `supply` 0.6 ms, same script; outputs byte-identical before/after this task. `tight`/`none` = levels that can't get 2 / 1 count-0 questions under one Hall assignment over the choice's bundles, media and window, as in decision 31: Low-supply warning (warn at 1 or 0 unseen per needed level) | — | — | — |
| `app/client/src/engine/outlook.ts` | `exhaustedSubs`: `data.groupById.get(choice.age_group!)!`; part 1 count 2 (lint: no-non-null-assertion) | practice | low | won't fix: `resolveChoice` sets exactly one of `age_group`/`difficulty` (task 535's row) |
| `app/client/src/engine/rng.ts` | comment "site = calling Python function": the referee is gone, the site is a tape label (`fixtures/README.md`) | inconsistency | low | fixed (task 537) |
| `app/client/src/engine/rng.ts` | seed and replay checked, no finding: `lib/engine.ts` seeds a fresh mulberry32 per action from 32 `crypto` bits; outcomes (cards, answer order) are stored in the save, so undo and reload restore instead of replaying, and no seed belongs in the save | — | — | — |
| `app/client/src/engine/pycompat.ts` | which helpers earn their keep now that the Python referee is gone (decision 25: Family test night on the TS engine): `casefold`, `pyLen`, `pySplitJoin` are the name rules (code points, whitespace) and fine on their own; `pyRepr` only quotes the English fallback messages in `state.ts`; `pyInt`/`pyTruthy`/`pyStr` coerce request bodies as the `errors`/`budget` fixtures pin. Replacing them changes fixture outputs for no gain | complexity | low | won't fix: 77 lines; the frozen fixtures are the spec |
| `app/client/src/engine/pycompat.ts` | `pyInt` takes only ASCII digits (Python's `int` takes any Unicode digit, e.g. fullwidth) and loses precision past 2^53 | bug | low | won't fix: request bodies come from the game's own client, which sends numbers |
| `app/client/src/engine/test/save.ts`, `app/client/src/engine/save.test.ts`, `app/client/src/engine/store.ts` | `MemoryStore` (moved here by task 536) had no user left but its own test «MemoryStore round trip and isolation»: class, test and the `store.ts` comment pointing at it deleted; `directory.md` updated (lint: none, unused export) | unused | low | fixed (task 538) |
| `app/client/src/engine/test/tape.ts` | part 1 row "23 exports used only in their own file: … `test/tape.ts` `TapeRng`: drop `export` unless meant as API (lint: none, unused export)": `export` dropped (`selection.test.ts` types it as `ReturnType<typeof tapeRng>`) | unused | low | fixed (task 538) |
| `app/client/src/engine/rng.test.ts` | «randomSeed is a uint32» pins one `crypto.getRandomValues` line; «tape applies perms in order» is what every fixture step does (a wrong perm fails every taped replay step): both dropped; kept: same seed → same permutations, shuffle is a permutation, «tape errors» (keeps the replay strict about extra/missing/misplaced shuffles) | complexity | low | fixed (task 538) |
| `app/client/src/engine/test/fixtures.ts`, `choice.test.ts`, `invariants.test.ts` | `data()` returned `undefined` for a missing `app/data/` file and both real-pool tests had a `skip` branch for it, but `app/data/pool.json` is tracked (and `pool.test.ts` read it unguarded): `data()` reads or throws, both skip branches gone (`choice.test.ts` de-indented) | unused | low | fixed (task 538) |
| `app/client/src/engine/selection.test.ts` | part 1 counts `any` 3: `Case.result: any` now `unknown` (only `deepEqual`ed); `Case.args: Record<string, any>` and `burned(args)` stay: per-`fn` fixture JSON, a typed union per case buys nothing (lint: no-explicit-any) | practice | low | fixed (task 538) for one; won't fix: the rest |
| `app/client/src/engine/*.test.ts`, `test/fixtures.ts` | part 1 counts `as` 23, `!` 19 in tests (`choice.test.ts` 7/11, `game.test.ts` 7/2, `selection.test.ts` 4/2, `outlook.test.ts` 2/0, `pool.test.ts` 1/2, `save.test.ts` 1/2, `test/fixtures.ts` 1/0): fixture JSON shapes and lookups whose failure is a thrown test anyway (lint: consistent-type-assertions, no-non-null-assertion) | practice | low | won't fix: in tests a wrong cast fails loudly; tests aren't type-checked at all (part 10, `task 586`) |
| `app/client/src/engine/*.test.ts` | coverage gap: the fixture replays predate MD-11/MD-12, and no TS-native test covers `levels`/`cards`/custom difficulty/`video`/`audio` (decision 33: Configure game screen: which fields?) or the cheats `replace`/`level`/`settings` and `gamemaster_only` (decision 34: Gamemaster menu: which cheats?); only task 535's throw-away script checked them | bug | medium | fixed (task 723): `engine/settings.test.ts` |
| `app/client/src/engine/invariants.test.ts` | the 8 real-pool walks (4 age groups × 2 bundle sets × 50 seeds) take 0.6–0.8 s each, nearly all of `npm test`'s 5.7 s | performance | low | won't fix: guards the seen-count rule on real data; 6 s per commit is fine |
| `app/client/src/engine/fixtures/README.md` | text vs. task 302's state: says frozen (decision 25: Family test night on the TS engine), re-record only from commit `c3b683f`, correct; stale bits fixed: "self-contained, never the real `app/data/`" (replays take real bundles and age groups), "compares on v3" (save is v4), "any seedable PRNG" (it is mulberry32); gap note → task 723 | inconsistency | low | fixed (task 538) |
| `app/client/src/engine/game.test.ts`, `choice.test.ts`, `outlook.test.ts`, `pool.test.ts`, `save.test.ts`, `selection.test.ts` | kept as they are, each guards a real rule: fixture replays (game, selection) are the spec; supply/repair (plan 65, 91), choice/bundles (decision 33, D38), outlook (decision 31), parsers and D-22 pinned against the real files, save upgrades v1→v4 and refusals, seen-count sort; no two tests duplicate each other | — | — | — |
| `app/client/package.json` | `npm test` glob `src/engine/**/*.test.ts` catches all 8 `*.test.ts` (the only ones tracked) | — | — | — |
| `app/client/src/engine/` (plan 75 close-out) | part 1 rows `handed to part 3` (`bundleOf`, `MemoryStore`, the 23 unused exports, `tsc --noUnusedLocals --noUnusedParameters`: 0 hits in tests and helpers too) all have a final status above; `npm test` before 159 tests / 5.8 s, after 156 / 5.8 s | — | — | — |

## Part 4: Client lib, locales and boot

Plan 76 reviews `app/client/src/lib/`, `locales/`, `main.ts`, `App.svelte`, `app.css`, `vite-env.d.ts` and `scripts/check-literals.mjs`.

| file | finding | category | severity | status |
|---|---|---|---|---|
| `app/client/src/lib/input.svelte.ts`, `app/client/src/lib/focus.ts`, `app/client/src/lib/gamepad.ts` | part 1 row "10 exports used only in their own file: … `focus.ts` `Rect`; `gamepad.ts` `Pad`; `input.svelte.ts` `Device`, `toIntent` … (lint: none, unused export)": `export` dropped from `toIntent`; `Rect`, `Pad`, `Device` stay exported as the parameter/state types of the public `nearest`, `step`, `Action`/`lastDevice`. `tsc --noUnusedLocals --noUnusedParameters` (flags in `tsconfig.json`): 0 hits in the four files | unused | low | fixed (task 539) for `toIntent`; won't fix: the three types belong to exported signatures |
| `app/client/src/lib/input.svelte.ts` | comments that lie: header "keys (later the gamepad) become actions" and `dispatch` "Part 5's gamepad calls it too" (the pad loop is `gamepad.svelte.ts`, plan 45) | inconsistency | low | fixed (task 539) |
| `app/client/src/lib/input.svelte.ts` | listener lifecycle: every `addEventListener` in `listen` and `track` has its `remove`; `Game.svelte` calls `listen`/`listenPads` in `onMount` and returns the cleanup, so an HMR remount doesn't double them. The cleanup leaves the module `busy` pointing at the old game's closure (one `Game`, harmless) | practice | low | won't fix: only one listener owner, the next `listen` replaces it |
| `app/client/src/lib/input.svelte.ts` | keyboard `keys` merge every scope's `keys`, also below a modal one, while `padMap` stops at the top modal: a lower screen's letter still becomes its intent inside a dialog. The Francotirador modal (`Question.svelte`) relies on it (A–D aim through Question's `KEYS`); other modals return false for foreign intents, so nothing fires | inconsistency | low | won't fix: snipe depends on it; changing it means moving the A–D keys into the snipe scope (behaviour risk, no bug today) |
| `app/client/src/lib/input.svelte.ts` | no findings: scope stack: `pushScope` puts non-modal scopes below the lowest modal one, the pop removes by identity (out-of-order pops are safe); `scopes.version` bumps via `untrack` on push, pop, `focusin`/`focusout`; module `$state` (`lastDevice`, `scopes`) is the intended shared state (part 1 globals row) | — | — | — |
| `app/client/src/lib/input.svelte.ts`, `app/client/src/lib/engine.ts` | two unrelated exported `Scope` types (input scope object vs. `"game" \| "next"` data scope) | inconsistency | low | handed to part 10 |
| `app/client/src/lib/input.svelte.ts` | no findings: `KEY_LABELS`/`FLAG_KEY` call `t()` at module load: correct only because `main.ts` imports `App.svelte` after `initLang`; `keyLabel` vs. `toIntent`: Enter/Esc/⌫/arrows/digits/catalog keys match; `padButton` resolves prompts from the same `padMap` the pad loop dispatches with | — | — | — |
| `app/client/src/lib/gamepad.ts`, `app/client/src/lib/gamepad.svelte.ts` | `HELD` hard-coded 32 buttons (magic number): a pad reporting more would fire those on focus return; now `held(n)` with the pad's own button count (lint: no-magic-numbers would flag it, noisy elsewhere) | practice | low | fixed (task 539) |
| `app/client/src/lib/gamepad.ts` | no findings: `BUTTONS` vs. its comment (A, B, Y, LB/RB, View, Start, D-pad) and `Glyph.svelte`'s sets: match; `styleOf` covers Sony's vendor id `054c` and the Chromium/Firefox DS4/DualSense names; `ON`/`OFF` stick hysteresis named | — | — | — |
| `app/client/src/lib/gamepad.svelte.ts` | poll lifecycle: rAF starts only with a standard pad, stops when the last one goes, cleanup cancels it; part 1 row ".catch(() => …) 1" (`steam.inputTypes().catch(() => null)`): an optional read with the `Gamepad.id` fallback, kept | practice | low | won't fix: deliberate fallback |
| `app/client/src/lib/gamepad.svelte.ts` | per frame per pad `padMap(BUTTONS)` rebuilds the merged map (each scope's `pad()` allocates), and every press calls `refreshSteam` (one IPC) | performance | low | won't fix: a few small objects per frame; the IPC per press is how a pad Steam lists late gets its glyphs |
| `app/client/src/lib/focus.ts` | part 1 row "`as` 2": `(el as HTMLButtonElement).disabled` (also wrong for `<a>`/`[data-focusable]`, and blind to a disabled `<fieldset>`) → `el.matches(":disabled")`; `indexOf(document.activeElement as HTMLElement)` → `findIndex`; `as` 2 → 0 (lint: typescript-eslint consistent-type-assertions) | practice | low | fixed (task 539) |
| `app/client/src/lib/focus.ts` | `nearest` cost: each arrow press runs `candidates` (one `querySelectorAll` + `getClientRects` per control) twice (`navigate`, then `show`'s memory index unless `data-focus-id`), plus a rect per candidate; screens have tens of controls, well under a millisecond | performance | low | won't fix: not measurable at this DOM size |
| `app/client/src/lib/engine.ts` | `ready()` caught only `store.load()`/`availableLocales()` failures (`.then(ok, fail)`): a throw inside the success path (missing or broken data file in `dataFor`, `repair`) left the rejected promise cached, so no retry despite "A failure is retried on the next call", and the error lacked the "can't load the game" prefix; now `load().catch(…)` (throw-away `/tmp` script: 404 on `pool.json`, then retry loads) (lint: none) | bug | medium | fixed (task 540) |
| `app/client/src/lib/engine.ts`, `app/client/src/lib/store.ts` | part 1 rows "`lib/engine.ts` `.catch(() => …)` 2", "`lib/store.ts` `.catch(() => …)` 1" and "3 are mutex chains whose failures go to the caller": confirmed, `exclusive` returns `out` and keeps only the chain unrejected, `flush` waits without owning the failure; the other `engine.ts` hit (`steam.language().catch(() => null)`) is the browser-language fallback | practice | — | won't fix: deliberate |
| `app/client/src/lib/store.ts` | `WriteQueue` cleared `flight` in a `.finally()` one microtask after the drain loop ended: a `push` in between would get the finished flight back and its document never written; now the drain clears it in its own `finally` before settling. Not reachable through `engine.ts` (each `run` awaits its save inside the mutex) (lint: none) | bug | low | fixed (task 540) |
| `app/client/src/lib/store.ts`, `app/client/src/lib/engine.ts` | throw-away `/tmp` script (shimmed bridge and `fetch`, real `app/data/`) through `run()` and `FileStore`: slow writes, 3 actions → newest written last; `save_locked` → action stands, `saveError()` set, next action writes the whole save and clears it; 3 direct pushes during a slow write → 2 writes (coalesced); a failed flight rejects every waiting caller; corrupt file → backup `corrupt`, version 99 → `newer`, notice once (D-72) | — | — | — |
| `app/client/src/lib/store.ts`, `app/client/src/lib/engine.ts` | coalescing in `WriteQueue` never kicks in through `engine.ts`: `exec` awaits `store.save` inside `exclusive`, so every action waits for its own write (one PUT/IPC per action) | complexity | low | won't fix: needed for `flush()` and per-action `save_locked`; harmless |
| `app/client/src/lib/store.ts` | browser path: a corrupt or newer `state/game.json` is returned as stored (D-67), `ServerStore.load` throws and the game shows only "can't load the game: …" on every screen; no backup/fresh start like `FileStore` (D-72). Checked: truncated `game.json` on a temp `TRIVIA_STATE`, `trivia` serves it with 200 | bug | medium | decision 98, follow-up task 724 |
| `app/client/src/lib/engine.ts` | `saveError()` keeps an earlier `save_locked` when a later write fails with `bad_save` (that one is thrown to the screen instead) | practice | low | won't fix: the thrown error shows; the next good write clears both |
| `app/client/src/lib/engine.ts` | part 1 row "`as` 2": `reply.body as ErrorBody` / `as T` because `Reply<T>` (`engine/api.ts`) isn't a union discriminated by `status` (lint: typescript-eslint consistent-type-assertions) | practice | low | won't fix: the `Reply` shape belongs to every route in `engine/api.ts` (part 3 kept it) |
| `app/client/src/lib/engine.ts`, `app/client/src/lib/desktop.ts` | part 1 row "10 exports used only in their own file: … `desktop.ts` `SteamBridge`, `TextFieldRect`; `engine.ts` `localIsoSeconds`, `Route` … (lint: none, unused export)": `export` dropped from `localIsoSeconds`; `Route` (parameter of `read`/`run`), `SteamBridge` (type of `steam`), `TextFieldRect` (`showTextInput`) stay as types of exported signatures. `tsc --noUnusedLocals --noUnusedParameters` (in `tsconfig.json`): 0 hits in the eight files | unused | low | fixed (task 540) for `localIsoSeconds`; won't fix: the three types belong to exported signatures |
| `app/client/src/lib/engine.ts`, `app/client/src/lib/data.ts` | part 1 globals rows (`loading`, `chain`, `lastSaveError`; `cache`): page-lifetime state of the single engine bridge, each reset where it should (`loading` on failure, `cache` entry on rejection, `lastSaveError` on a good write) | practice | — | won't fix: intended module state |
| `app/client/src/lib/engine.ts` | no findings: `takeSaveNotice`/`takeLocalOffer` one-shot (cleared on read), `guessTag` (Steam name → tag, unknown → browser language, `defaultLanguage` handles tags without UI), `localIsoSeconds` local without zone as Python's `isoformat` (fixtures; a DST fall-back hour repeats, ordering by game id not time) | — | — | — |
| `app/client/src/lib/data.ts`, `app/client/src/lib/store.ts` | `base` parameter of `loadEngineData`, `availableLocales`, `get`, `load` and `ServerStore` never set by any caller (all `""`): dropped; header comment named only `app/server/main.py` as the `/data/` source (also the desktop protocol) | unused | low | fixed (task 540) |
| `app/client/src/lib/data.ts` | no findings: a failed locale load drops its cache entry (retried next call); `availableLocales` only asks the local server/protocol (offline-safe) and cancels the body; optional files rely on 404, which `app/desktop/resolve.mjs` also returns | — | — | — |
| `app/client/src/lib/data.ts` | part 1 row "`as` 1": `mergeNames` casts names files unchecked (lint: typescript-eslint consistent-type-assertions) | practice | low | won't fix: `qgen validate` checks names files at export |
| `app/client/src/lib/engine.ts`, `app/client/src/lib/api.ts`, `app/client/src/lib/store.ts` | import cycle `engine.ts` → `api.ts` (`GameError`) → `engine.ts`, `store.ts` → `api.ts` (`call`, `json`, `GameError`) → `engine.ts` → `store.ts`: works only because `main.ts` enters via `engine.ts`; a module importing `store.ts` first gets "FileStore is not a constructor" at `engine.ts`'s top-level `new FileStore` (hit by the `/tmp` script). `GameError`/`call`/`json` belong in a leaf module | complexity | medium | handed to part 10 (`task 581: Part 10: consolidate client types and API clients`) |
| `app/client/src/lib/desktop.ts` | no findings: `DesktopBridge`/`SteamBridge` match `app/desktop/preload.cjs` method for method (`loadSave`, `writeSave`, `backupSave`, `localSave`, `adoptLocalSave`, 8 Steam calls); rejections carry `bad_save`/`save_locked` as in `main.mjs`/`save.mjs`, mapped by `FileStore`; the preload side is part 6's | — | — | — |
| `app/client/src/lib/desktop.ts`, `app/client/src/main.ts` | imports without `.ts` (`./gamepad`, `./lib/engine`, `./lib/i18n`) next to `.ts` imports in the same folder (`allowImportingTsExtensions`) | inconsistency | low | handed to part 10 (`task 585: Part 10: consistency across files (naming, errors, env vars, ports)`) |
| `app/client/src/lib/store.ts`, `app/client/src/engine/store.ts` | duplication candidate: none, `engine/store.ts` is only the `Store` interface both stores implement (part 3) | — | — | — |
| `app/client/src/lib/data.ts`, `app/client/src/lib/i18n.ts`, `authoring/tools/` | duplication candidate: question locales `LOCALES` (`es`, `en`, `de`) ↔ `i18n.ts` `CATALOGS`/`UI_LANGS` ↔ the authoring tools' locale lists | inconsistency | low | handed to part 10 |
| `app/client/src/main.ts` | top-level `await`: a failed `language()` is caught (the game shows it); `initLang` can't reject (static catalogs, `xx` dev-only); only a missing `App` chunk (broken build, local file) leaves a blank page. Part 1 row "`!` 1" (`getElementById("app")!`, `index.html`'s own element) (lint: no-non-null-assertion) | practice | low | won't fix: no reachable failure |
| `app/client/src/App.svelte` | no findings: comment refs hold (`plans/04-ui-tv-display.md`, D-25, D-35: review, stats and joker cards live in `authoring/`) | — | — | — |
| `app/client/src/app.css` | 8 of 10 tokens unused in the game (`--panel`, `--muted`, `--accent`, `--good`, `--good-bg`, `--bad`, `--warn`, `--bar`: left from when review/stats lived in the client, D-35); dropped, `--bg`/`--text` stay (es output unchanged: no `var()` reads them) | unused | low | fixed (task 540) |
| `app/client/src/app.css`, `authoring/ui/src/app.css` | part 1 row "identical 27-line colour token files … handed to part 10": no longer identical, the game keeps only `--bg`/`--text`; the shared `body`/box-sizing rules remain a candidate | complexity | low | handed to part 10 (`task 584: Part 10: styles and screen helpers`) |
| `app/client/src/vite-env.d.ts` | no findings: `VITE_AUTHORING_URL` (`Overlay.svelte`) and `__APP_VERSION__` (`lib/build.ts`, `vite.config.ts` define) both used; `Window.trivia` is declared in `desktop.ts` beside its type, no overlap | — | — | — |
| `app/client/src/lib/api.ts`, `app/client/src/engine/save.ts` | part 3 row "`setFlag` throws a plain `Error` … `lib/api.ts` turns it into a 400 whose `error` code is the English text (no catalog key)": the 400 now carries code `flag_invalid`; `errorText` still shows the English message (no key, es output unchanged); only a non-string id or a note over 500 letters reaches it | inconsistency | low | fixed (task 541) |
| `app/client/src/lib/api.ts` | part 1 row "`any` 15 … `lib/api.ts` 1": `failure(res, body: Record<string, any>)` → typed `ErrorJson` (`error`, `params`, `message`, `supply`), narrowed by the existing `typeof body.error` check (lint: no-explicit-any) | practice | low | fixed (task 541) |
| `app/client/src/lib/api.ts` | part 1 row "`as` … `lib/api.ts` 1": `playJoker` casts `run(…)` to `{ game: Game; event: JokerEvent }`; `engine/api.ts` `gameAction` returns `game: Game \| null; event?` for every action, and sets both for `joker` (lint: typescript-eslint consistent-type-assertions) | practice | low | won't fix: one `Reply` type per route in `engine/api.ts` (part 3); a joker-only route type belongs to task 581 |
| `app/client/src/lib/api.ts`, `app/client/src/lib/engine.ts`, `app/client/src/engine/game.ts` | five copies of the "newest game" `reduce` (`flagList`, `fetchJokersUsed`, `engine.ts` `dataFor`, `game.ts` `latest`, `newestGame`) → one `newest(games)` in `engine/state.ts` beside `gameLocale` | complexity | low | fixed (task 541) |
| `app/client/src/lib/api.ts` | comments that lie: header "persisted via /api/save" (the desktop persists through the bridge, `lib/store.ts`); "The age group of a choice without one" over the re-export of seven choice constants | inconsistency | low | fixed (task 541) |
| `app/client/src/lib/api.ts` | `call`'s "server not reachable — is the game server (`trivia`) running?" is English and names the browser server, also in the desktop (`/data/` over the app protocol) | inconsistency | low | won't fix: the desktop protocol doesn't fail like a closed port; the text is shared with `authoring/ui` |
| `app/client/src/lib/api.ts` | no findings: every export has an importer (throw-away `/tmp` script over `app/client` and `authoring/`): `call`/`json`/`post` serve `data.ts`, `store.ts` and `authoring/ui/src/lib/api.ts`; `ChoiceBody`, `fetchChoice`, `fetchOutlook`, `fetchPlayerMode` and the constants (`Choice.svelte`); re-exports `fetchLanguage`, `localeSupply` (`LanguageScreen`, `Game`); no `app/server` route is called besides `/data/` and `/api/save` (D-90). `GameActionBody` matches `engine/api.ts` `gameAction`'s keys (`index`, `player`, `everyone`, `jokers`, `CHOICE_KEYS` + `mode`, `seen`, `level`) | — | — | — |
| `app/client/src/lib/types.ts` | no findings: all 22 exports imported (`JokerState` by `engine/game.ts`; `Status` by `engine/pool.ts`, authoring; credits types by `credits.ts`); `Game`, `Player`, `Jokers`, `JokerEvent`, `Choice`, `Supply` are built by the engine under these types, so `tsc` keeps the fields in step; `Player.last_played` is read by no screen (engine output, kept) | — | — | — |
| `app/client/src/lib/types.ts` | header "Mirrors the playable pool" while most of the file is the engine's views (`Game`, `Jokers`, `Choice`, …) and `credits.json` | inconsistency | low | fixed (task 541) |
| `app/client/src/lib/errors.ts`, `app/client/src/locales/es.ts` | engine codes (`engine/state.ts` `ERRORS`) vs. `es.ts` `error.*` (throw-away script): 11 without text (`answer_invalid`, `budget_invalid`, `budget_unknown_joker`, `card_invalid`, `joker_unknown`, `language_unknown`, `no_cards`, `no_game`, `no_question`, `nothing_to_undo`, `skip_not_question`): malformed requests or states the UI guards, shown with the English message as `es.ts` documents; catalog-only `save_locked` (`saveError()`), `supply_level` (part of `supply_short`): not dead | — | — | — |
| `app/client/src/lib/errors.ts` | `bad_save` (`lib/store.ts`: desktop `writeSave` / `/api/save` 400, invalid or over 10 MB) is thrown to the screen with no catalog text: English `can't save: …` on a Spanish TV | bug | low | fixed (task 725): `error.bad_save` in `es.ts`, `en.ts`, `de.ts` |
| `app/client/src/lib/errors.ts` | part 1 row "`as` 2": `params as Params`, `levels as Params[]`: engine-built params (`ErrorInfo.params` is `unknown`) (lint: typescript-eslint consistent-type-assertions) | practice | low | won't fix: params come from the engine's own `GameError`s |
| `app/client/src/lib/names.svelte.ts` | no findings: no name → the key (Spanish subcategory name, then `categories.json`/`bundles.json` name for categories/bundles), before the first engine call the key and `questionLocale` `es`; `useNames` skips an unchanged `data`; part 1 globals row (`data` `$state.raw`): intended module state | — | — | — |
| `app/client/src/lib/build.ts` | no findings: `__APP_VERSION__` is `app/desktop/package.json`'s version via the `vite.config.ts` define, the same source as `trivia-release-check`'s header (`steam.py` `version()`, decision 91: Game version: single source of truth); `pool` is the `hash` `qgen export` writes (`pool_export.py`, decision 92: Pool version: export hash in pool.json), read by `engine/pool.ts` `poolHash`, `null` in old pools and before the first engine call (Credits then shows the version only). One user today (`Credits.svelte`), kept: task 699's report header uses it too. Not in the part 1 inventory (added by task 690); `git ls-files` of `lib/`, `locales/`, `src/*`, `scripts/` vs. this part: no other file without a row | — | — | — |
| `app/client/src/lib/build.ts`, `app/client/src/lib/names.svelte.ts` | `pool` is the hash of the last engine call's pool (`game` or `next` scope), so an `en`/`de` game shows `pool.<locale>.json`'s hash while the release-check header lists only `app/data/pool.json`'s; a flag report (task 699) for a question in another locale would carry the wrong hash | inconsistency | low | flag header: note added to task 699; release header with every locale's pool hash: handed to `task 720: Review Steam release and store tooling` |
| `app/client/src/lib/api.ts`, `app/client/src/engine/api.ts`, `authoring/ui/src/lib/api.ts`; `lib/types.ts`, `engine/state.ts`, `authoring/ui/src/lib/types.ts`; `GameError` in `lib/api.ts` ↔ `engine/state.ts` | duplication candidates: `lib/api.ts` builds `flagList`, choice options and jokers-used inline instead of `engine/api.ts` routes; two `GameError` classes (client: `message` from the server, `supply`; engine: message from `ERRORS`, `details`); authoring `types.ts` already extends `Media`/`Background`/`Status` from here; `check:literals` still fails on `EffectsDemo.svelte` (part 1 row, task 542) | complexity | low | handed to part 10 (`task 581: Part 10: consolidate client types and API clients`) |
| `app/client/src/lib/i18n.ts` | `UI_LANGS` filtered out `xx`, but `CATALOGS` never holds it when `UI_LANGS` is computed (dev `initLang` adds it later): no-op filter, comment said otherwise; now `Object.keys(CATALOGS)` | unused | low | fixed (task 542) |
| `app/client/src/lib/i18n.ts` | plural-map test written three times (`isBranch`, `has`, `t`) and `t` cast `v as Plural`: one `isPlural` type guard. Part 1 row "`as` 3" → 2 (`merge`'s `as Catalog`, `lookup`'s `as Record`: walking a typed tree by a runtime path) (lint: typescript-eslint consistent-type-assertions). Output of `t`/`variants`/`has`/`UI_LANGS` for every key × `es`, `es-ES`, `en`, `de` identical before/after (throw-away script) | complexity | low | fixed (task 542); won't fix the other 2 casts: runtime key paths |
| `app/client/src/lib/i18n.ts` | `TextKey`, `VariantsKey` re-exported, imported by nobody (only `Key`, by `input.svelte.ts`) (lint: none, unused export) | unused | low | fixed (task 542) |
| `app/client/src/lib/i18n.ts` | `fill` leaves an unknown `{param}` as is, no dev warning (unlike a missing key) | practice | low | won't fix: `check-literals.mjs` compares `{param}` sets per catalog; a missed param shows on screen in dev |
| `app/client/src/lib/i18n.ts` | no findings: `pickLang` (unknown or `es-419` tag → `es`; `?lang=` only in dev, `xx` only in dev), `initLang` sets catalog, numbers and plurals together; `t()` on a missing key → `⟦key⟧` with one dev warning; plural without numeric `n` → `other`; `endonym` is a static table, no `Intl` lookup (offline-safe); `xx` is a dynamic `import` behind `import.meta.env.DEV`: no `xx` chunk or `pseudoText` in `npm run build`'s `dist/` (the 4 shipping catalogs stay eager in `engine-*.js`, part 1 bundle baseline: negligible). Part 1 globals row (`lang` exported `let`, `catalog`, `numbers`, `plurals`, `warned`): set once before the first render, a language change reloads (plan 68); importers get a read-only live binding | — | — | — |
| `app/client/src/locales/xx.ts` | part 1 row "10 exports used only in their own file: … `xx.ts` `pseudoText` (lint: none, unused export)": `export` dropped. Part 1 row "`as` 1" (`walk(…) as Catalog`): the pseudo tree mirrors `es` by construction (lint: typescript-eslint consistent-type-assertions) | unused | low | fixed (task 542) for `pseudoText`; won't fix: the cast |
| `app/client/src/locales/es.ts`, `en.ts`, `de.ts`, `es-ES.ts` | no findings: throw-away script: 282 leaves in `es`, `en`, `de` (no missing, no extra key), 33 in `es-ES` (all in `es`); `{param}` sets match (`check:literals`); every `es` key used in `app/client/src` or `authoring/ui` (`cards.*` by `print/JokerCards.svelte` via `catalogFor`; dynamic `joker.${name}.*`, `credits.${kind}`, `copy.consolation.${max}`, `copy.milestone.${at}`, `error.*` via `has`); `Key`/`TextKey`/`VariantsKey` (from `Widen<typeof es>`) still type every call site (`npm run check`). Wording is out of scope: playtest fixes are `task 459: LUI-5: playtest fixes and close-out` (decisions 62–65) | — | — | — |
| `app/client/scripts/check-literals.mjs` | part 1 row "`npm run check:literals -w app/client` fails (exit 1): 8 Spanish literals in the dev-only `game/EffectsDemo.svelte` … runs in no pre-commit step": `SKIP` for `EffectsDemo.svelte` (`/?efectos` dev aid, UI-10) and `lib/i18n.ts` (endonyms); the check now passes and runs as part of `app/client`'s `npm run check` (so before every commit, D-73); `directory.md` says so | inconsistency | low | fixed (task 542) |
| `app/client/scripts/check-literals.mjs` | default path `src/game` only: now also `src/lib` and `src/App.svelte` (0 hits besides the endonyms); `alt=` added to the checked attributes (0 hits) | practice | low | fixed (task 542) |
| `app/client/scripts/check-literals.mjs` | false negatives: in `.ts`/`<script>` only Spanish letters (`áéíóúñ¡¿`) count, so English or German text in a script string (e.g. `lib/api.ts`'s "server not reachable", engine `ERRORS` messages) passes; `stripJs` reads a regex literal with a quote or `//` as a string/comment, and a nested template literal ends early (only comment blanking on that line is affected) | practice | low | won't fix: telling text from identifiers in JS strings needs a parser and gives noise; no such regex in the scanned files today |
| `app/client/scripts/check-literals.mjs`, `app/client/src/locales/xx.ts` | shortcut-key leaves listed three times: `SCREENS` + `SAME_OK` (`.key$`, `Key$`) here, `EXEMPT` in `xx.ts` | inconsistency | low | won't fix: the same two patterns, each list short; part 1 globals row (`failed`): a script counter |

## Part 5: Game screens

Plan 77 reviews `app/client/src/game/`.

| file | finding | category | severity | status |
|---|---|---|---|---|
| `app/client/src/game/Game.svelte` | part 1 row "`startGame`: `noteExhausted(…).catch(() => {})` (line 279): … an engine throw there (bad choice body) vanishes without a trace (lint: no-empty-function)": now `console.warn`s it; the save-write failure still shows via `saveWarning()` | practice | low | fixed (task 543) |
| `app/client/src/game/Game.svelte` | race: the mouse menu and flag buttons (z-index 30) stay clickable above the transition's black layer and never checked `busy` (keys do, via `listen`); `go` isn't reentrant, so an overlay action (skip, undo, …) started mid-transition ran a second `go` interleaved with the first (veil, `screen`, `busy` out of order). `openOverlay`/`openFlag` now return while `busy` | bug | medium | fixed (task 543) |
| `app/client/src/game/Game.svelte` | race: `pick` let `request` drop `busy` as soon as the pick action returned, up to `PICK_MS` (1 s) before `go("question")`: Esc/menu opened the overlay over the tearing envelope with the game already in phase `question`. `request` now restores the caller's `busy`; `pick` holds it until the question is on screen | bug | low | fixed (task 543) |
| `app/client/src/game/Game.svelte` | `restart` ignored a failed `abandon`: it went on to the Choice screen with the old game still running, and `refresh` replaced the error with `saveWarning()`. Now it stops and the error stays | bug | low | fixed (task 543) |
| `app/client/src/game/Game.svelte` | media pause/resume copied in `openOverlay`/`openFlag` and `closeOverlay`/`closeFlag`; `overlayOpen = false; pausedMedia = []` in five overlay actions, `skip` without the reset: now `pauseMedia`, `resumeMedia`, `leaveOverlay` | complexity | low | fixed (task 543) |
| `app/client/src/game/Game.svelte` | an overlay action that fails (skip, undo, replace, jump, restart) closes the overlay first, so the question's audio/video stays paused | practice | low | won't fix: the error shows, the replay key restarts the media; these actions fail only on an engine bug |
| `app/client/src/game/Game.svelte` | small dead or misleading code: `startGame`'s second `busy = true` (still true); the first-input handler named `onclick` though keys and pads call it (now `firstInput`); two stacked JSDoc blocks on `go` (the first detached); the Start subtitle recomputed `levelsOf(game)` beside the `$derived` `levels`; the Level screen called `milestone(…)` twice (now `{@const}`) | complexity | low | fixed (task 543) |
| `app/client/src/game/Game.svelte` | magic numbers: `FADE_MS * 2 + 750` (the block's fall, coupled to `Tower.svelte`'s CSS), `FLIP_MS * 2 + 100` (`swap.active`), deal delay `i * 0.12s`, `tilt` seeds (lint: no-magic-numbers) | practice | low | follow-up task 552 (`timing.ts` vs. literal durations in `game/`) |
| `app/client/src/game/Game.svelte` | the `unlocked` chime: `newGame` sets `unlocked` so a mouse click on «¡Jugar!» (button handler before the window listener) skips it, while Enter (`first` runs before dispatch) plays it before the whoosh | inconsistency | low | won't fix: a sound change, not a code fix; both orders sound fine |
| `app/client/src/game/Game.svelte` | `void steam.setPresence(…)`: a rejection is unhandled (console only), and `presence` is cached before the call succeeds, so a failed update isn't retried (lint: no-floating-promises accepts `void`) | practice | low | won't fix: rich presence is cosmetic; the main handler only throws with Steam broken |
| `app/client/src/game/Game.svelte` | `jokerPlayed`'s `setTimeout` for `swap.active` (module-global flag in `swap.ts`) isn't cleared on unmount | practice | low | won't fix: one `Game` per page; the flag only gates transitions |
| `app/client/src/game/Game.svelte` | split candidate: the Select screen's envelopes (markup, `tilt`, ≈200 lines CSS) are self-contained; screens per phase otherwise share `go`/`busy`/`game` state, so only this block moves without rewiring | complexity | low | follow-up task 726 |
| `app/client/src/game/Game.svelte`, `app/client/src/game/*.svelte`, `app/client/src/game/theme.css` | duplication candidates: `@keyframes arrive`/`bob` in 10 game components; `.menu-button`/`.flag-button` share size, hover and transition rules; 13 literal `rgba(76, 201, 240, …)`/`rgba(255, 84, 112, …)` (= `--sky`/`--coral`) and `#d9cfb6` card shadows | complexity | low | handed to part 10 (task 584) |
| `app/client/src/game/Game.svelte` | no findings: state machine: phases `select`/`question` → `table()` (with `cards: 0` the Level screen goes straight to the question, D-88), `won`/`lost` → Victory/Wrong, abandoned via restart/home; undo always lands on Question (the engine restores the state before a final answer); levels from `levelsOf` (decision 46: Gamemaster mode: level ranges for custom difficulty and for a number of levels other than 12); jokers ∞ pass through to `JokerTray`/`Question`; engine errors → corner box, `new` refusals → Choice, missing data → `screen.noData`; cheats only via the overlay (decision 34: Gamemaster menu: which cheats?). Scopes: `popGame` on destroy, the screen `$effect` reruns only on `screen` and returns its pop; `listen`/`listenPads` cleaned up; `flagTarget` vs. the overlay's `questionId` differ on purpose (the overlay shows the last question on any screen). `svelte-check` 0 warnings, `check:literals` clean | — | — | — |
| `app/client/src/game/Question.svelte` | race: `busy()` (the overlay's `canSkip`/`canUndo`/`canTable`) covered only the final answer, not a joker in flight: during Paso's shredder or Francotirador's beat, an overlay skip/undo/replace/level jump changed the game, then `fire` went on and `onplayed` put the joker's older game back on screen. `busy()` now also covers `jokerBusy` | bug | medium | fixed (task 544) |
| `app/client/src/game/Question.svelte` | a question whose audio/video fails (not in the media cache, offline) stayed silent: `onMount` stops the music for its media, but only `ended` brought it back; and `replay` on the failed player stopped the music again. A player error now counts as ended; `replay` returns when the media failed | bug | low | fixed (task 544) |
| `app/client/src/game/Question.svelte` | CSS `var(--sweep, 0.55s)`: `--sweep` set nowhere, the fallback copied `SWEEP_MS` (550) from `timing.ts`; now `style:--sweep="{SWEEP_MS}ms"` on the screen | inconsistency | low | fixed (task 544) |
| `app/client/src/game/Question.svelte` | unused CSS: `.crosshair` (no element has the class; `svelte-check` misses it because the answer tiles' `class` is dynamic) (lint: svelte css_unused_selector, blind here); `.answer` and `.answer.shatter` each declared twice; an empty line in the badge `{#if}` chain | unused | low | fixed (task 544) |
| `app/client/src/game/theme.css`, `app/client/src/game/Question.svelte` | part 1 row "CSS variable `--placeholder` (pink dashed border) now used only by `.media-missing`; name suggests the `PLACEHOLDER(<task id>)` marker style": renamed `--pink` (palette name like `--sky`, `--coral`), same colour | inconsistency | low | fixed (task 544) |
| `app/client/src/game/Question.svelte` | an overlay «Reiniciar» (`canRestart`, not gated by `busy()`) during the reveal wait or a joker abandons the game, then `onanswered`/`onplayed` still hands the old game to `Game.svelte` | bug | low | follow-up task 545 (gating of restart/budget while the question is busy) |
| `app/client/src/game/Question.svelte` | magic numbers: `popping` cleared after a literal 500 ms (coupled to `JokerTray`'s pop-back CSS); scope hole `hole.w + 40` px (not in `--u`); `3 - question.hints.length` and the 3 note tilts assume 3 hints per question (also `JokerTray`'s `hintsLeft = 3`) (lint: no-magic-numbers) | practice | low | follow-up task 552 (`timing.ts` vs. literal durations); won't fix the rest: layout constants used once |
| `app/client/src/game/Question.svelte` | timers after unmount: `popping`'s `setTimeout` and `fire`/`submit`'s `wait`/`sleep` chains are not cancelled on destroy; padlock and arm timers are | practice | low | won't fix: with `busy()` covering jokers and the answer, the screen only unmounts mid-chain via restart (row above); the stray timeout only sets local state |
| `app/client/src/game/Question.svelte` | the scope hole is measured once per target (`getBoundingClientRect` in an `$effect`): a window resize while aiming leaves it off the tile until the next move | bug | low | won't fix: no resize while a TV game aims; a `ResizeObserver` costs more than it saves |
| `app/client/src/game/Question.svelte` | split candidates: the script (~470 lines) is one state machine (`locked`, `mode`, `target`, `shot`, `jokerBusy`, `tiles`) shared by answers, jokers and reveal; only the Paso dialog (~40 lines markup/CSS + its scope) and the media backdrop could move, both still need `fire`/`mode` or `player`/`settle` passed through. Over half the file is CSS | complexity | low | won't fix: a split moves little and adds props; no follow-up |
| `app/client/src/game/Question.svelte`, `app/client/src/game/*.svelte` | duplication candidates: `@keyframes arrive`, `shake`, `pop`, `pulse`, `spin` also in other game components; literal `rgba(255, 84, 112, …)` (= `--coral`) ×4, `rgba(5, 8, 16, …)` dims ×4; `.dialog`/`.backdrop-dim` like `FlagDialog`/`CategoryPicker` | complexity | low | handed to part 10 (task 584) |
| `app/client/src/game/Question.svelte` | no findings: 8 `$effect`s: the scope hole (reruns on `shot`/`mode`/`target`/`tiles`), `$effect.pre` resetting `native` on a new picture, media start (once, after `shown` and not `paused`), media volume (`mediaVolume()`), 4 scopes (question once; armed, Paso, Francotirador per state, each returns its pop); `ready()` settles on load/`canplaythrough`/error, text questions at once; media preload `preload="auto"` via cache-only `/media` (offline); the two `play().catch(() => {})` are autoplay refusals (part 1); `as`/`!`: `currentTarget`, `activeElement`, `settleAll!` (assigned synchronously in the `Promise` executor), `TOKENS.find(…)!`; `submit`'s null game only without a running game; jokers ∞ (`jokersLeft` null) passed to `JokerTray`; levels via `onTwelve(level, levels)` (decision 46: Gamemaster mode: level ranges for custom difficulty and for a number of levels other than 12); no `PLACEHOLDER`; `svelte-check` 0 warnings, `check:literals` clean | — | — | — |
| `app/client/src/game/Overlay.svelte`, `app/client/src/game/Game.svelte` | handed from task 544 ("an overlay «Reiniciar» (`canRestart`, not gated by `busy()`) during the reveal wait or a joker abandons the game, then `onanswered`/`onplayed` still hands the old game to `Game.svelte`"): «Terminar partida» and the joker budget (preset and per-joker rows; a budget edit mid-reveal came back overwritten by the answer's game) ignored `questionBusy()`. `canRestart` now also needs `!questionBusy()`; new prop `canBudget` disables the budget rows and `setBudget`. Walked: reveal → menu shows both disabled, the game goes on to «¡Oh no!» | bug | medium | fixed (task 545) |
| `app/client/src/game/Overlay.svelte` | part 1 row "language `$effect` (line 191) `.catch(() => {})`: if `fetchLanguage()`/`localeSupply()` fails, the language rows just don't appear, no error shown or logged (lint: no-empty-function)": now `console.warn`s; the rows still just don't appear | practice | low | fixed (task 545) |
| `app/client/src/game/Overlay.svelte` | part 1 counts (`as` 1, `!` 3, `.catch` 4): `as Partial<Volumes>` (computed key), `current!`/`langs!` inside callbacks after an outer check (TS doesn't carry the narrowing), `requestFullscreen().catch` (refusal), `fetchJokersUsed`/`fetchGameChoice` `.catch` (optional reads: the "used" column or the choice line stays empty) (lint: no-non-null-assertion, no-empty-function) | practice | low | won't fix: each is checked or best-effort; language `.catch` fixed above |
| `app/client/src/game/Overlay.svelte` | «Saltar a nivel» used `game?.settings.levels ?? 12`, a copy of `levelsOf`/`DEFAULT_LEVELS` (`game/levels.ts`) | inconsistency | low | fixed (task 545) |
| `app/client/src/game/Overlay.svelte` | ternary as statement for the pad's B (`confirming === null ? onclose() : (confirming = null)`) (lint: oxlint no-unused-expressions, part 10 trial `Overlay.svelte:270`); `across` sorted the column numbers without a comparator (lint: require-number-sort-compare) and measured rows with `document.querySelector` instead of the menu | practice | low | fixed (task 545) |
| `app/client/src/game/Overlay.svelte` | the jokers column's preset row cycles «Sin límite» ↔ «Como las cartas» (`CARDS` 4/2/2/2/2), while decision 33 dropped presets and made `STANDARD_JOKERS` the default: a fresh gamemaster game shows «Personalizado» and can't go back to the standard set | inconsistency | low | decision 99, follow-up task 727 |
| `app/client/src/game/Overlay.svelte` | `selected`/`confirming` are indexes into `items`; rows that arrive async (language rows, choice line) shift the cheats' indexes, so a selection or a pending «Presiona otra vez» on a cheat moves to another row | bug | low | won't fix: the loads are local and land within ms of opening, before a key press; a moved confirm only asks again |
| `app/client/src/game/Overlay.svelte` | `target` («Saltar a nivel») is reset by an `$effect` on every new `game` object (e.g. after a budget edit), not only on a level change; `pending` (fast budget clicks) is cleared by the first answer, so the value jumps back a step until the second answer | bug | low | won't fix: both last until the next engine answer (ms); the engine queue keeps the edits in order |
| `app/client/src/game/Overlay.svelte` | floating promises: `stepLang`, `applyUi`, `quit` run from `handle`/`run`, `document.exitFullscreen()`; a failed language save leaves an unhandled rejection (console only), `quit` stays open when `flush` fails (lint: no-floating-promises, no-misused-promises) | practice | low | won't fix: the rejection logs; not quitting on a failed save keeps the data, closing the window still works |
| `app/client/src/game/Overlay.svelte` | split candidates: the jokers editor (~50 lines script) and the language rows share `items`/`selected`/`handle` navigation; `GameSettings` and `Credits` are already children | complexity | low | won't fix: a split moves little and adds props; no follow-up |
| `app/client/src/game/Overlay.svelte`, `app/client/src/game/*.svelte` | duplication candidates: dim `rgba(5, 8, 16, 0.72)` in 8 game components; `rgba(255, 183, 3, …)` (= `--amber`); `.step` stepper buttons and rows like `Choice.svelte`/`GameSettings.svelte` | complexity | low | handed to part 10 (task 584) |
| `app/client/src/game/Overlay.svelte` | no findings: decision 34 (Gamemaster menu: which cheats?): general column in every mode, cheats only in gamemaster mode with a game, no answer reveal; jokers ∞ (`null`) shown as ∞ (read-only outside gamemaster mode); `levels` 1 keeps the jump at 1; `cards` 0 via `canTable`; 7 `$effect`s (level target, used, pending, language, choice line, scope push returning its pop, scroll) without timers or listeners; modal scope `whileBusy`; every prop passed and read; no `PLACEHOLDER`; `svelte-check` 0 warnings, `check:literals` clean | — | — | — |
| `app/client/src/game/sound.svelte.ts` | race: only the three loops waited for the samples (`samplesLoaded`); `victory` and `roll` read `samples.victoria`/`samples.redoble` at once, so a track that starts with the unlock (reload on the Victory screen, then the first key press) played no Elgar, and a roll that early played the synth roll. All tracks now start through the same `begin` after the samples | bug | low | fixed (task 546) |
| `app/client/src/game/sound.svelte.ts` | `startTrack`: three copies of the `stop` closure (victory, recorded roll, synth roll) next to the loops' own; `track as keyof typeof MUSIC_FILE` (unchecked cast, part 1 `as` count); `TEMPO.roll`/`TEMPO.victory` never read (only the generated loops use `TEMPO`). Now one `Loop` with `stopLoop`, `LoopTrack` type, no cast | complexity | low | fixed (task 546) |
| `app/client/src/game/sound.svelte.ts` | `loadVolumes` spread the stored JSON unchecked: a wrong type (`"music": "x"`) made `setTargetAtTime` throw inside `unlock` (no music, no samples' volume), an out-of-range level (`5`) played the bus at 2.5×; the overlay clamps, the stored value didn't. Now each field must be a number in 0..1 (`muted` a boolean), else its default | bug | low | fixed (task 546) |
| `app/client/src/game/sound.svelte.ts` | `loadSamples` swallowed every failed fetch/decode without a trace: a recording missing from a build silently played the synth version (lint: no-empty) | practice | low | fixed (task 546): one `console.warn` with the failed names |
| `app/client/src/game/sound.svelte.ts` | part 1 counts (`as` 3, `.catch`/`catch {}` 2): `null as Track \| null` (state init), `Object.keys(RECIPES) as Cue[]` (keys of a `Record<Cue, …>`), `track as keyof …` (removed above); `catch {}` in `setVolumes` (private window, commented) and `loadSamples` (now warns) | practice | low | fixed (task 546) for the cast and `loadSamples`; won't fix the rest: checked by the types |
| `app/client/src/game/sound.svelte.ts` | part 1 row "`sound` (`$state`), `ctx`, buses, `noiseBuffer`, `samples`, `samplesLoaded`, `samplesReady`, `current`, `synthMusic`": module state is the app's one audio engine, created by the first input (`unlock`), never closed; buses are typed without `!` but only read after a `ctx` check | practice | low | won't fix: one `AudioContext` per page by design (04, "Audio") |
| `app/client/src/game/sound.svelte.ts` | magic numbers: bus/track gains (`v.music * 0.5`, `MUSIC_LEVEL` 1.6, victory 3, roll 2.2, duck 0.5), fade lengths in `music()` (0.6/0.8 s, sharp 0.08/0.15/0.05 s), recipe frequencies and envelopes (lint: no-magic-numbers) | practice | low | won't fix: sound-design values used once, most commented; levels and rates superseded by task 146 (gamemaster check of the recorded effects, may adjust them) |
| `app/client/src/game/sound.svelte.ts` | the generated loops and the synth roll schedule from `setInterval` (50/40 ms, 0.2 s lookahead): in a background tab the browser throttles intervals to 1 s and the fallback stutters | performance | low | won't fix: fallback only (recordings loop natively), the game runs in the foreground |
| `app/client/src/game/sound.svelte.ts` | `pluck`/`tick`/`snare`/`thump` (music, with `keep`) repeat the gain-envelope pattern of `tone`/`noise` (effects, fire-and-forget) | complexity | low | won't fix: the music voices need `keep` for `stop`; a shared helper saves a few lines |
| `app/client/src/game/sound.svelte.ts` | synth recipes vs. recordings: plans 32/33 done except task 146 (pending decision 81: Recorded sound effects: approve on the TV?); `boom` and `silence` have no recording on purpose; `effects()`/`synth` options used only by `/?efectos` (dev aid, UI-10) | — | — | superseded by task 146 |
| `app/client/src/game/sound.svelte.ts` | no findings: `AudioContext` lifecycle (one context; `unlock` on every input resumes it, a pad press may not count as activation; `sfx` skips while not `running`); no node leaks (`voices` drop on `onended`, the track gain disconnects on stop, `fadeOut` stops 100 ms after its ramp, intervals cleared, a loop still waiting for the samples checks `stopped`); `music` switches during a pending start or a fade cancel cleanly; `void ctx.resume()` rejects only on a closed context, `samplesLoaded` never rejects; samples served from `public/audio/` (offline); every export used (`Game`, `Question`, `Overlay`, `Fireworks`, `Shredder`, `EffectsDemo`); no `PLACEHOLDER`. Walked `/?efectos` in headless Chrome on a temp `TRIVIA_STATE` (recorded/synth loops, cut, stop, effects; no errors) | — | — | — |
| `app/client/src/game/Player.svelte`, `app/client/src/game/letters.ts` | part 1 row "4 exports used only in their own file: … `MAX_NAME` (lint: none, unused export)": the name field had its own `maxlength="30"`, a copy of `MAX_NAME`; now `maxlength={MAX_NAME}`, so the export has a second user. The engine's `cleanName` keeps a third literal 30 (`name_too_long`; counts code points, `maxlength` UTF-16 units) | inconsistency | low | fixed (task 547) for `Player`; engine copy handed to part 10 (task 584) |
| `app/client/src/game/Player.svelte` | part 1 count (`.catch(() => …)` 1): `steam.showTextInput(…).catch(() => false)`: a refused or broken Steam keyboard falls back to the letter picker (lint: no-empty-function would not fire, constant result) | practice | low | won't fix: deliberate fallback, the picker opens |
| `app/client/src/game/Player.svelte` | the delete dialog's scope handler was a comma expression in a `&&` (`… && ((doomed = null), true)`) (lint: no-sequences); now plain statements | practice | low | fixed (task 547) |
| `app/client/src/game/Player.svelte`, `app/client/src/game/*.svelte` | duplication candidates: the delete dialog's `.backdrop`/`.dialog`/`.danger` like `FlagDialog`/`SupplyNotice`/`Question`'s Paso dialog; field focus ring `rgba(76, 201, 240, 0.35)` (= `--sky`); `@keyframes arrive` again | complexity | low | handed to part 10 (task 584) |
| `app/client/src/game/Player.svelte` | no findings: 2 `$effect`s: first-focus once (non-reactive `focused` flag; only without players, after `busy` drops), delete scope per `doomed` (modal, `whileBusy`, returns its pop, focuses «Cancelar» so a stray Enter deletes no one); the screen scope is pushed once and returns its pop; keys 1–9 and Enter go through the scope, so `busy` gates them (`input.svelte.ts`), buttons carry `disabled={busy}`; `fetchPlayers`/`deletePlayer` errors shown (`errorText`), a failed delete keeps the list; more than 9 players: the rest by typing (UI-16); letter picker hand-off via `bind:name` + `submit` (task 230), Steam keyboard first on a pad (plan 85); the Choice screen and its supply notice live in `Choice`/`SupplyNotice` (decision 31: Low-supply warning: below how many fresh games left (K) should the game start warn?), not here; no timers, no `PLACEHOLDER`; every prop passed by `Game.svelte` and read; `svelte-check` 0 warnings, `check:literals` clean | — | — | — |
| `app/client/src/game/JokerTray.svelte` | header comment "Jokers are unlimited by default (D-27)" lied since D-88/decision 33 (a fresh choice gets `STANDARD_JOKERS`; only old gamemaster games without `jokers` are unlimited); now says the standard set is the default and ∞ has no badge | inconsistency | low | fixed (task 547) |
| `app/client/src/game/JokerTray.svelte` | `.bubble.arm` set `border: 1px solid var(--sky)` and again `border-color: var(--sky)`; the badge read `left?.[tok.name]` three times in markup (now one `{@const uses}`) | complexity | low | fixed (task 547) |
| `app/client/src/game/JokerTray.svelte` | Soplo's pips `[0, 1, 2]` and `hintsLeft = 3` assume 3 hints per question (same as `Question.svelte`'s `3 - question.hints.length`) (lint: no-magic-numbers) | practice | low | won't fix: see the `Question.svelte` row; every exported question has 3 hints (`app/data/pool.json`) |
| `app/client/src/game/JokerTray.svelte` | `TOKENS` (names, keys, icons; 6 importers incl. `authoring/ui` `JokerCards.svelte`) lives in a component's module script and calls `t()` at import: labels are fixed per page load (a UI language change reloads, `Overlay.applyUi`), and the authoring print page pulls in a game component for a table | complexity | low | handed to part 10 (task 584); the authoring import is task 573's |
| `app/client/src/game/JokerTray.svelte` | `pop-back` keyframes 0.45 s vs. `Question.svelte`'s literal 500 ms `popping` clear | practice | low | follow-up task 552 (as in the `Question.svelte` row) |
| `app/client/src/game/JokerTray.svelte` | no findings: jokers ∞ (`left` or its entry `null`) show no badge, 0 shows the grey badge, a spent joker is `off` with the engine's reason (`reasonText`) in the bubble; `jokers` null (after the answer) locks every token; readonly trays (Level, Select) skip keys, pips, bubbles, bumpers; `away` hides the token while `JokerFlight` flies (`transition: none`), `popping` replays `pop-back`; pad focus (`data-nav` = real focus) shows the name bubble via `:focus-within`; no `$effect`, timers or listeners; every prop passed by `Question.svelte`/`Game.svelte`; `svelte-check` 0 warnings, `check:literals` clean | — | — | — |
| `app/client/src/game/Fireworks.svelte` | part 1 row "4 exports used only in their own file: … `FireworksMode` … (lint: none, unused export)": no other importer (`Game.svelte` passes string literals); now a plain module type | unused | low | fixed (task 548) |
| `app/client/src/game/Fireworks.svelte` | part 1 count (`!` 11): `canvas!`, `getContext("2d")!`, `events.shift()!` after a length check, 8 × `angle!`/`spin!`/`wobble!` on confetti and star particles, which set them by construction (lint: no-non-null-assertion) | practice | low | won't fix: each holds by construction; a particle union type for 2 kinds costs more than it saves |
| `app/client/src/game/Fireworks.svelte` | `variant in VARIANTS` also matched prototype keys: `/?fuegos=toString` called `Object.prototype.toString` and showed nothing; now `Object.hasOwn` (preview only, falls back to a random variant) | bug | low | fixed (task 548) |
| `app/client/src/game/Fireworks.svelte` | the last frame's `else g.clearRect(…)` cleared a canvas already cleared at the frame's start with nothing drawn since | complexity | low | fixed (task 548) |
| `app/client/src/game/Fireworks.svelte` | per frame: 2 trail objects per rocket, `splice` per dead particle (O(n) each), `globalCompositeOperation` set per particle; finale peaks at ≈1500 particles | performance | low | won't fix: bounded and spread over 14 s; the finale ran smooth in headless Chrome at 1280×720 |
| `app/client/src/game/Fireworks.svelte` | with reduced motion nothing runs, so its `sfx` (rocket, burst, confetti cannon, sparklers, stars) stay silent too | inconsistency | low | won't fix: those sounds belong to the particles; the screen's own `applause`/`applause-big` still plays (`go` in `Game.svelte`) |
| `app/client/src/game/Fireworks.svelte`, `app/client/src/game/theme.css` | duplication candidate: `COLORS` and the variant palettes are hex copies of `--amber`, `--sky`, `--mint`, `--coral`, `--paper` and a gold not in `theme.css` (canvas can't read `var()`; `getComputedStyle` could) | complexity | low | handed to part 10 (task 584) |
| `app/client/src/game/Fireworks.svelte` | no findings: rAF loop cancelled and `resize` listener removed on unmount, the loop stops by itself when events and particles run out; `sfx` only from scheduled events, so none after unmount; resize rescales the canvas (DPR capped at 2: 4K at DPR 1 = 3840×2160 backing store, 1280×720 fine); `prefers-reduced-motion` skips it; mounted on Correct, Victory (`finale`) and the `/?fuegos=` preview; no `$effect`, scopes, literals or `PLACEHOLDER`. Walked `/?fuegos=finale` and `/?fuegos=toString` in headless Chrome on a temp `TRIVIA_STATE` (no errors) | — | — | — |
| `app/client/src/game/Shredder.svelte`, `app/client/src/game/timing.ts` | magic numbers: the stamp lands after a literal 350 ms (= its `arrive` 0.35 s); the strips' `shred` 0.9 s + up to 0.1 s delay must fit `SHRED_MS` (1100); `slam` 0.28 s (lint: no-magic-numbers) | practice | low | follow-up task 552 (`timing.ts` vs. literal durations) |
| `app/client/src/game/Shredder.svelte`, `app/client/src/game/*.svelte` | duplication candidates: `@keyframes arrive` (again), dim `rgba(5, 8, 16, 0.6)` (cf. 0.72 in 8 components) | complexity | low | handed to part 10 (task 584) |
| `app/client/src/game/Shredder.svelte` | no findings: 3 timers cleared on unmount, `ondone` once; `name` in the question's `lang`; stamp text from the catalog (`joker.skip.stamp`); reduced motion: `theme.css` collapses the CSS animations, the timers keep the scene's length (`STAMP_MS + SHRED_MS`) so the joker flow times the same; 9 strips each repeat name and stamp (clip-path), cheap; no `$effect`, scopes, `PLACEHOLDER`. Walked a «Paso» with purge in headless Chrome (no errors) | — | — | — |
| `app/client/src/game/JokerFlight.svelte` | `flight.finished.then(async …)` floated: unmounting mid-flight (`flight.cancel()`, e.g. the overlay restart of the `Question.svelte` row) rejected `finished` with an unhandled `AbortError`, and the burst's `setTimeout(ondone)` wasn't cleared (lint: no-floating-promises, require-await); now `onfinish` and the timer cleared on unmount | bug | low | fixed (task 548) |
| `app/client/src/game/JokerFlight.svelte` | CSS `var(--burst, 0.25s)`: `--burst` set nowhere, the fallback copied `JOKER_BURST_MS` (250); now `style:--burst="{JOKER_BURST_MS}ms"` on the chip (as `--sweep` in task 544) | inconsistency | low | fixed (task 548) |
| `app/client/src/game/JokerFlight.svelte`, `app/client/src/game/timing.ts` | comment "Short on purpose (jokers are unlimited, D-27)" lied since D-88/decision 33 (standard jokers by default); fixed here; `timing.ts`'s `JOKER_FLY_MS` doc says the same | inconsistency | low | fixed (task 548); `timing.ts`: follow-up task 552 |
| `app/client/src/game/JokerFlight.svelte` | the sparks run 0.45 s + up to 0.08 s, but `Question.svelte` unmounts the flight at `ondone` (`JOKER_BURST_MS` 250 ms), so they are cut halfway; reduced-motion fade 150 ms literal (lint: no-magic-numbers) | inconsistency | low | won't fix: visible timing, tuned on the TV (UI-6); a change is not a code fix |
| `app/client/src/game/JokerFlight.svelte` | part 1 count (`!` 1): `chip!` in `onMount` (`bind:this` is set before mount) (lint: no-non-null-assertion) | practice | low | won't fix: holds by construction |
| `app/client/src/game/JokerFlight.svelte`, `app/client/src/game/*.svelte` | duplication candidates: glow `rgba(255, 184, 28, 0.55)` (= `--amber`); the token look (dashed amber ring, `--night-700`, highlight) copies `JokerTray`'s `.token`; spark rays vs. `Fireworks`' canvas sparks (no shared animation code between the three effects: canvas, CSS strips, WAAPI) | complexity | low | handed to part 10 (task 584) |
| `app/client/src/game/JokerFlight.svelte` | no findings: starts at the tray token's `DOMRect`, flies to the window centre (any size), reduced motion = fade without sparks; one mount per play (`Question.svelte` `fly`); `pointer-events: none`; no `$effect`, scopes, literals or `PLACEHOLDER`. Walked a Hint and a «Paso» in headless Chrome over CDP (flight mounts, ends, hint shows; no errors) | — | — | — |
| `app/client/src/game/DifficultyDial.svelte` | the staircase had 10 steps, but difficulties run 1–15 (`DIFFICULTY_MAX`, D-38; the pool has 181 questions above 10): a Bájale from 13 to 11 lit every step and marked none as the current one. Now `DIFFICULTY_MAX` steps, heights scaled to the same 2.6 u box | bug | medium | fixed (task 549) |
| `app/client/src/game/DifficultyDial.svelte`, `app/client/src/game/timing.ts` | the 300 ms pause before the first tick, a literal twice; now `DIAL_START_MS` next to `DIAL_STEP_MS`/`DIAL_HOLD_MS` (lint: no-magic-numbers) | practice | low | fixed (task 549) |
| `app/client/src/game/DifficultyDial.svelte` | no findings otherwise: the 3 timer sites (ticks, fade) are cleared on unmount; `from`/`to` read once in `onMount` is enough, `Question.svelte` is keyed by question id, so every Bájale swap mounts a new dial; label from the catalog | — | — | — |
| `app/client/src/game/Stage.svelte` | dead CSS: `transition`s on `filter`, `opacity`/`background`, `box-shadow` for mood changes never run (every screen branch of `Game.svelte`/`Question.svelte` mounts its own `<Stage>` with a fixed `mood`); `.correct .spotlight { opacity: 1.4 }` clamps to 1, the default. Removed, nothing on screen changes; one `<Stage>` hoisted above the screen chain would make the mood fades play (a visual change, not done) | unused | low | fixed (task 549) |
| `app/client/src/game/Stage.svelte` | part 1 row "4 exports used only in their own file: … `StageMood` … (lint: none, unused export)": `export` dropped | unused | low | fixed (task 549) |
| `app/client/src/game/Stage.svelte` | no findings otherwise: glyph positions computed once at module level; no script logic, no timers | — | — | — |
| `app/client/src/game/Tower.svelte` | levels per game (decision 46, task 499): 1 level = one 90 % gold block (`onTwelve` → 12) and the crown; 20 levels = blocks 2.2 u (small 0.9 u) high, widths 90 → 35 %, the stack stays within the 12-level height (44.4 u); materials follow `onTwelve`; no findings | — | — | — |
| `app/client/src/game/Tower.svelte`, `app/client/src/game/Stage.svelte`, `app/client/src/game/theme.css` | duplication candidates: raw colours despite `theme.css`'s "never raw colours": sapphire/gold gradient ends `#7fa2ff`, `#1f3f9e`, `#ffe08a`; `rgba(255, 184, 28, …)` (= `--amber`), `rgba(76, 201, 240, …)` (= `--sky`), `rgba(47, 227, 154, …)` (= `--mint`) | inconsistency | low | follow-up task 584 |
| `app/client/src/game/Tower.svelte` | the drop/settle/crumble durations (0.75 s, 0.45 s, 0.18 s per block) are coupled to `Game.svelte`'s `FADE_MS * 2 + 750` (its magic-numbers row) | practice | low | follow-up task 552 |
| `app/client/src/game/Hud.svelte`, `app/client/src/game/Game.svelte` | duplication candidate: the Level screen draws the player chip itself (`<span class="chip glass">` in `.corner-hud`) instead of `Hud`'s player chip | complexity | low | follow-up task 584 |
| `app/client/src/game/Hud.svelte` | no findings otherwise: one tick per level, 20 ticks fit (≈12.6 u); label from the catalog; no state, no effects | — | — | — |
| `app/client/src/game/LanguageScreen.svelte` | a failing `localeSupply()` (a question pool that won't load or parse) went to the same `catch` as `fetchLanguage()`: no options, `current` null, Esc swallowed: the first start stuck on an error with no way on. Now a failed check is `console.warn`ed and leaves `playable = ["es"]`; the UI languages still show. Walked: fresh `TRIVIA_STATE`, headless Chrome shows the 4 UI languages | bug | medium | fixed (task 550) |
| `app/client/src/game/LanguageScreen.svelte` | `fetchLanguage()` failing still leaves the screen without options or exit | practice | low | won't fix: it's the engine's `ready()` (save or data unreadable); no screen of the game works then, the error text shows |
| `app/client/src/game/LanguageScreen.svelte` | a pick whose save write fails with `save_locked` reloads anyway (`run` keeps the in-memory save), so the fresh save asks again after the reload | practice | low | won't fix: nothing persists with a locked save; the same-language path lands on Start, which shows `saveWarning()` |
| `app/client/src/game/LanguageScreen.svelte` | `ask` (`lib/engine.ts` `language()`) is also true with one UI language and several question locales: the screen then offers a single button and picks the question language itself (`defaultLanguage(ui, [ui], playable)`) | inconsistency | low | won't fix: 4 UI languages ship (decision 26: Launch languages (OQ-31): which languages at Steam launch, and which comes first after?; decision 27: Spanish variety (OQ-31): which Spanish does base speak, and which Steam store languages to tick?), the case can't occur |
| `app/client/src/game/LanguageScreen.svelte` | no findings otherwise: one scope (`$effect` reads no state, returns its pop), `menu` swallowed on purpose (no overlay before a language), `back`/`flag` fall to `Game`'s scope (`flagTarget` null); `pick` n bounded by `options.length`; `saving` guards double confirm and stays set through `location.reload()`; `current` always in `options` (`defaultLanguage` over `UI_LANGS`); `playable`/`buttons` non-reactive on purpose; texts via `t()`/`endonym`, no `PLACEHOLDER`; `svelte-check` 0 warnings, `check:literals` clean | — | — | — |
| `app/client/src/game/CategoryPicker.svelte` | no findings: Esc cancels, Backspace goes back a step (top level: cancel), the Cancel prompt's pad glyph follows (`menu` in subcategories, `back` on top); one modal scope (`$effect` reads no state); focus to the first enabled tile, back to the opened group's tile; `fire` sets `mode = null` first, so a double pick can't fire twice; empty or all-disabled lists can't open (the engine disables the joker without an available subcategory), Esc still cancels; title in the UI language, names in `questionLocale()`; `focusFirst()`/`back()` unawaited at the call sites (harmless, nothing after them) (lint: no-floating-promises); `svelte-check` 0 warnings, `check:literals` clean | — | — | — |
| `app/client/src/game/FlagList.svelte` | was `Reports.svelte` (the plan's name), renamed and reworked by task 625 (decision 60: One mechanism for questions with problems: flag or report?); reviewed here, not again in task 553. No findings: flags keyed by question ID (unique `#each` keys), sorted newest first in `lib/api.ts`; `flagged_on` is local time without zone (`localIsoSeconds`), so `when()`'s slice shows local time; empty list: `flag.empty`, no Copiar; `navigator.clipboard` undefined outside a secure context throws inside the `try` → selectable `<pre>`; one modal `whileBusy` scope, focus on «Volver»; texts via `t()` (`—`/`·` separators only); `svelte-check` 0 warnings | — | — | — |
| `app/client/src/game/CategoryPicker.svelte`, `app/client/src/game/LanguageScreen.svelte`, `app/client/src/game/FlagList.svelte` | duplication candidates: `@keyframes arrive` (two variants) and `deal`; dim `rgba(5, 8, 16, 0.55/0.6)`; card shadow `#d9cfb6`; `rgba(43, 54, 80, 0.5)` (= `--slate-600`); `.backdrop` like `FlagDialog`/`Question`'s Paso dialog | complexity | low | handed to part 10 (task 584) |
| `app/client/src/game/Icon.svelte` | icons `replay` and `star` drawn but never used (the replay button shows `speaker`/`film`); `JokerTray`, `JokerFlight`, `authoring/ui` `JokerCards` use only the joker set (lint: none, unused union members) | unused | low | fixed (task 551) |
| `app/client/src/game/Prompt.svelte` | part 1 scan row (1 `as`): `intent()` cast `{ type: a } as Intent`; `Named` a hand-kept copy of the field-less `Intent` types (`flag` never passed). Now `Named` derives from `Intent`, the return type replaces the cast (lint: none beyond the part 1 `as` scan) | practice | low | fixed (task 551) |
| `app/client/src/game/Prompt.svelte` | `away` read `chip`/`scopes.version` before `if (off) return true`: needless dependencies while off; check moved first, same result | complexity | low | fixed (task 551) |
| `app/client/src/game/Glyph.svelte` | part 1 scan row (1 `as`): `[DPAD[button]] as [Shape, string?]`; now a typed `$derived` (lint: none beyond the part 1 `as` scan) | practice | low | fixed (task 551) |
| `app/client/src/game/Prompt.svelte`, `app/client/src/game/Glyph.svelte`, `app/client/src/game/Icon.svelte` | no findings: labels from `keyLabel` (`KEY_LABELS`, the one copy) match `toIntent` (Enter/Space confirm, Esc menu, ⌫ back, catalog keys for replay/new/flag); pad glyph from `padMap` incl. scope overrides (Question's `PAD_FINAL` LT/RT, picks incl. X/□), so every `Glyph` set entry has a user; `menu`+`pad="back"` shows Esc / B as handled. No effects, timers or scopes; `$derived` only; no catalog text (LB/RB/L1… are button names). SVG: one compiled template per component, not inlined per use; no bundle issue. Not touched by an open task | — | — | — |
| `app/client/src/game/timing.ts`, `Question.svelte`, `Game.svelte`, `Shredder.svelte`, `JokerFlight.svelte`, `swap.ts` | rows of tasks 543/544/548 "magic numbers … follow-up task 552": literal durations moved into `timing.ts`, same values: `POP_BACK_MS` 500 (`Question`'s `popping` reset, `JokerTray`'s `pop-back` 0.45 s), `BLOCK_DROP_MS` 750 (`Game`'s `FADE_MS * 2 + 750`, `Tower`'s `drop` 0.75 s), `STAMP_LAND_MS` 350 (`Shredder`'s stamp, its `arrive` 0.35 s), `REDUCED_FADE_MS` 150 (reduced-motion fade, twice: `swap.ts`, `JokerFlight`) (lint: no-magic-numbers) | practice | low | fixed (task 552) |
| `app/client/src/game/timing.ts` | row of task 548: `JOKER_FLY_MS` doc "kept short, jokers are unlimited" lied since D-88/decision 33 (standard jokers by default); now "a joker plays many times a game", as in `JokerFlight` | inconsistency | low | fixed (task 552) |
| `app/client/src/game/Game.svelte`, `Question.svelte`, component CSS | remaining literals: `FLIP_MS * 2 + 100` (slack after the flip, derived), `wait()`'s 100 ms poll tick, CSS-only timings (`Tower` `--fall-delay`, deal `i * 0.12s`, `Shredder`'s `shred` 0.9 s + ≤ 0.1 s, fits `SHRED_MS` 1100; `slam` 0.28 s, note delays) (lint: no-magic-numbers) | practice | low | won't fix: used once, local to their CSS; no timer depends on them |
| `app/client/src/game/swap.ts` | `perspective(${1600}px)`: a constant interpolated into the template; now `perspective(1600px)`, same string | complexity | low | fixed (task 552) |
| `app/client/src/game/swap.ts`, `JokerFlight.svelte`, `Fireworks.svelte` | duplication candidate: `matchMedia("(prefers-reduced-motion: reduce)")` read in 3 places, each its own way (`swap.ts` a helper, the others inline) | complexity | low | handed to part 10 (task 584) |
| `app/client/src/game/swap.ts` | no findings otherwise: `swap.active` a module-global flag (row of task 543: won't fix); `cardFlip`/`crossfade` used by `Question` only, no-ops outside a swap | — | — | — |
| `app/client/src/game/copy.ts` | no findings: `milestone`/`consolation` used by `Game`; levels 1, 3, 5, 12, 20 checked with a throw-away script (12: lines at 4/6/8/10/12 as before; 1: only the last; brackets scale); `variants` never returns `[]` (missing key → marker), so `choose` always has a line; `?? CONSOLATION_MAX[…]` unreachable but a cheap guard; texts from the catalog (D-70). Phase/copy logic overlap with `Game`/`Overlay`/`Hud`: none beyond the calls | — | — | — |
| `app/client/src/game/theme.css` | header "Components use these tokens only, never raw colours" doesn't hold (raw `rgba` copies of `--sky`/`--coral`/`--amber`/`--mint`, logged by tasks 543/548/549/550) | inconsistency | low | handed to part 10 (task 584) |
| `app/client/src/game/theme.css` | no findings otherwise: every custom property defined is used and every `var(--…)` in `app/client/src` is defined (scan); every class (`glass*`, `title`, `label`, `candy`, `breathe`, `secondary`, `kbd`) has users; `--pink` rename from task 544 holds; German hyphenation per decision 61; `authoring/ui` `JokerCards` imports it for fonts and `.title` | — | — | — |

## Part 6: Desktop shell and packaging

Plan 78 reviews `app/desktop/` and the Steam release and store tooling in `authoring/steam/` and `authoring/store/`.

| file | finding | category | severity | status |
|---|---|---|---|---|

## Part 7: qgen

Plan 79 reviews `authoring/tools/qgen.py` section by section, then its module structure.

| file | finding | category | severity | status |
|---|---|---|---|---|

## Part 8: Other authoring tools

Plan 80 reviews `authoring/tools/` minus `qgen.py`, `categories.py` and `prompts/`.

| file | finding | category | severity | status |
|---|---|---|---|---|

## Part 9: Authoring server and UI

Plan 81 reviews `authoring/server/` and `authoring/ui/`, sources and configs.

| file | finding | category | severity | status |
|---|---|---|---|---|

## Part 10: Cross-cutting: duplication, consistency, build config

Plan 82 consolidates the duplication candidates of parts 2–9, checks naming and error handling across files, reviews the root and `app/client` build config and `app/client/credits.ts`, and checks `directory.md` and `AGENTS.md` against the code. The linter evaluation below ran early (task 616).

| file | finding | category | severity | status |
|---|---|---|---|---|

### Linter evaluation

Task 616 evaluated a linter for the TypeScript trees (`app/client/src`, `authoring/ui/src`, `app/desktop` `.mjs`/`.cjs`; 48 `.ts`, 34 `.svelte`, 6 desktop scripts, ~14.9k lines) on 2026-10-12. Parts 2–9 had logged no findings yet, so the evidence is the trial run alone: every diagnostic of every candidate was triaged by hand.

- Evidence from the report: none yet (no `(lint: …)` tags; part 1 scans not run) → re-check: `task 617: Re-check the linter evaluation against the findings of parts 2–9`.
- Trial: temp copy under `/tmp`, candidates installed there only, deleted afterwards.

| candidate | packages added (lockfile entries) | Svelte | type-aware | time | diagnostics | real bugs | noise |
|---|---|---|---|---|---|---|---|
| stricter `tsconfig` flags | 0 | script + markup (svelte-check) | yes | inside `npm run check` (~3 s each) | 2 (+ ~150 with `noUncheckedIndexedAccess`) | 0 | 2 style; `noUncheckedIndexedAccess`: almost all index-after-length-check |
| Biome 2.5 (recommended, Svelte full support) | 9 (1 + 8 per-platform binaries) | script + markup (experimental) | no | 0.2 s | 213 | 0 | 62 `useButtonType`, 5/5 `noUnusedVariables` false (`class:x` shorthand), 10 `noAssignInExpressions` (Svelte `() => (x = y)` idiom), 13 `useIterableCallbackReturn` (`forEach` arrows) |
| oxlint 1.87 (default `correctness`) | 20 (1 + per-platform bindings) | script only | no (needs `oxlint-tsgolint`, more packages) | 0.06 s | 2 (58 with `suspicious`) | 0 | ternary as statement (`Overlay.svelte:270`), control chars in `pycompat.ts:14` (on purpose: Python's whitespace set); `suspicious`: `no-shadow`, `no-array-sort`, function scoping |
| ESLint 10 + typescript-eslint (`recommendedTypeChecked`) + eslint-plugin-svelte | 132 | script + markup | yes | 6 s | 210 (+11 test files not in a tsconfig) | 0 | 104 `no-unsafe-*` (deliberate `any`/`unknown` at JSON and save parsing), 32 `no-floating-promises` + 7 `no-misused-promises` (fire-and-forget calls whose async functions catch their own errors), 7 `no-base-to-string` (`String(unknown)` in error messages), 8 `prefer-svelte-reactivity` (Sets non-reactive on purpose), 12 `require-each-key` (static lists) |

- Already clean before this task: `noUnusedLocals`, `noUnusedParameters`, `noFallthroughCasesInSwitch`, `noImplicitOverride` (0 each); svelte-check reports them in `.svelte` script blocks too (probe checked).
- No candidate caught a bug. Example of what none catches: `authoring/ui/src/review/Review.svelte` `undo()` pops the undo stack before its `busy` check, so `u` pressed while saving drops that undo entry (logged below).
- Unused exports and files (the likeliest drift after worker refactors): none of the four candidates finds them; part 1's scan (`task 526: Scan: unused TS/JS code and npm dependencies`) does.
- `app/desktop` `.mjs`/`.cjs`: no `tsconfig` covers them; only the three linters see them, with 0 findings there.
- Not adopted: Biome, oxlint, ESLint. 0 bugs against 9–132 new packages (minimal-dependencies rule, `npmDepsHash`), and their noise comes from idioms this code uses on purpose. No decision needed.
- Adopted: `noUnusedLocals`, `noUnusedParameters`, `noFallthroughCasesInSwitch`, `noImplicitReturns`, `noImplicitOverride` in both `tsconfig.json`s (`authoring/ui` type-checks `app/client/src` too).
  - The lint pass is `npm run check`, already in the pre-commit checks (AGENTS.md, D-73). `project-manager.toml` has no own worker prompt; workers follow AGENTS.md.
  - Existing issues: the 2 `noImplicitReturns` sites, fixed here (behaviour unchanged). No baseline and no follow-up fix task needed: the pass covers everything from the start.
- Not adopted: `noUncheckedIndexedAccess` (133 + 165 errors, almost all on already-checked indexes), `exactOptionalPropertyTypes`.
- `*.test.ts` and `engine/test/` are excluded from both `tsconfig`s, so the flags (and type-checking) don't reach them: task 586 (plan 82 task 7) checks this.

| file | finding | category | severity | status |
|---|---|---|---|---|
| `app/client/src/game/Question.svelte` | `press()` and `aim()` return `fire(…)`'s promise from a `void` function (lint: noImplicitReturns) | practice | low | fixed (task 616): `return void fire(…)` |
| `app/client/tsconfig.json`, `authoring/ui/tsconfig.json` | no unused/fallthrough/implicit-return checks | practice | low | fixed (task 616): five flags |
| `authoring/ui/src/review/Review.svelte` | `undo()` pops `undoStack` before `if (!last \|\| busy) return`: an undo pressed while busy is lost | bug | low | handed to part 9 (`task 575: Review the review page`) |

## Part 11: Executive summary and close-out

Plan 83 checks this report for completeness, proposes process changes, writes the executive summary at the top and runs the final checks.

| file | finding | category | severity | status |
|---|---|---|---|---|

## Inventory

Every `git ls-files` path in scope, mapped to the one part that reviews it (2026-10-13, 174 files; produced by a throw-away script that reported no unassigned file). Files added later are added here by the part that reviews them.

| path | part | review task |
|---|---|---|
| `app/server/` (`http_base.py`, `main.py`, `media_cache.py`, `paths.py`, `save.py`) | 2 | 532, 533 |
| `authoring/tools/categories.py` | 2 | 534 |
| `app/client/src/engine/` (10 modules + `choice.ts` split from `game.ts` in task 535, 8 `*.test.ts`, `test/` 3 helpers; not `fixtures/`) | 3 | 535–538 |
| `app/client/src/lib/` (`input.svelte.ts`, `gamepad.ts`, `gamepad.svelte.ts`, `focus.ts`) | 4 | 539 |
| `app/client/src/lib/` (`engine.ts`, `store.ts`, `data.ts`, `desktop.ts`), `src/main.ts`, `src/App.svelte`, `src/app.css`, `src/vite-env.d.ts` | 4 | 540 |
| `app/client/src/lib/` (`api.ts`, `types.ts`, `errors.ts`, `names.svelte.ts`) | 4 | 541 |
| `app/client/src/lib/i18n.ts`, `app/client/src/locales/` (5 files), `app/client/scripts/check-literals.mjs` | 4 | 542 |
| `app/client/src/lib/build.ts` | 4 | 722 |
| `app/client/src/game/` (36 files) | 5 | 543–552; files added since plan 77: 553 |
| `app/desktop/` (`main.mjs`, `preload.cjs`, `resolve.mjs`) | 6 | 554 |
| `app/desktop/save.mjs` | 6 | 555 |
| `app/desktop/` (`package.json`, `package-lock.json`, `electron-builder.yml`, `after-pack.mjs`, `stage-media.mjs`, `steam-presence.vdf`) | 6 | 556 |
| `authoring/steam/` (7 files incl. `steam.json`), `authoring/store/screenshots.mjs` | 6 | 720 |
| `authoring/tools/qgen.py` | 7 | 557–566 |
| `authoring/tools/` (`health.py`, `targets.py`, `batches.py`, `age_groups.py`) | 8 | 567 |
| `authoring/tools/` (`concepts.py`, `progress.py`) | 8 | 568 |
| `authoring/tools/` (`layout.py`, `translations.py`, `pool_export.py`, `save_file.py`) | 8 | 569 |
| `authoring/tools/` (`media.py`, `download.py`) | 8 | 570 |
| `authoring/tools/providers/` (5 files) | 8 | 571 |
| `authoring/tools/` (`engine.py`, `supply.ts`, `sim/` 2 files, `package.json`; added since plan 80: `cdp.mjs`, `patch_notes.py`) | 8 | 572 |
| `authoring/server/main.py` | 9 | 573 |
| `authoring/server/` (`overview.py`, `spot_checks.py`, `media_stats.py`) | 9 | 574 |
| `authoring/ui/src/review/Review.svelte` | 9 | 575 |
| `authoring/ui/src/review/` (`MediaPanel.svelte`, `RevisionPanel.svelte`; added since plan 81: `SourcePanel.svelte`) | 9 | 576, 579 |
| `authoring/ui/src/stats/` (8 files) | 9 | 577 |
| `authoring/ui/src/home/Home.svelte`, `authoring/ui/src/print/JokerCards.svelte` | 9 | 578 |
| `authoring/ui/` (`src/App.svelte`, `src/main.ts`, `src/app.css`, `src/lib/` 3 files, `index.html`, `package.json`, `vite.config.ts`, `svelte.config.js`, `tsconfig.json`, `.gitignore`) | 9 | 579 |
| `flake.nix`, `flake.lock`, `package.json`, `package-lock.json`, `.envrc`, `.gitignore` | 10 | 586 |
| `app/client/` (`package.json`, `tsconfig.json`, `vite.config.ts`, `svelte.config.js`, `index.html`, `.gitignore`) | 10 | 586 |
| `app/client/credits.ts`, `app/client/node.d.ts` | 10 | 721 |
| `directory.md`, `AGENTS.md` (vs. the code only) | 10 | 620 |

Out of scope (milestone 13 "Scope", plan 72):
- `*.json` data and fixtures (226: pools, concepts, bundles, `app/client/src/engine/fixtures/`, `app/data/`); in scope: `package*.json`, `tsconfig.json`, `authoring/steam/steam.json`
- `tasks.sql`, `project-manager.toml`, `plans/` (33)
- prompts: `authoring/tools/prompts/` (18)
- media, audio, fonts: `app/client/public/audio/`, `app/client/public/fonts/` (44)
- `*.md` docs (13), except part 10's `directory.md`/`AGENTS.md` check
