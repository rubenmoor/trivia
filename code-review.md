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

## Part 4: Client lib, locales and boot

Plan 76 reviews `app/client/src/lib/`, `locales/`, `main.ts`, `App.svelte`, `app.css`, `vite-env.d.ts` and `scripts/check-literals.mjs`.

| file | finding | category | severity | status |
|---|---|---|---|---|

## Part 5: Game screens

Plan 77 reviews `app/client/src/game/`.

| file | finding | category | severity | status |
|---|---|---|---|---|

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
