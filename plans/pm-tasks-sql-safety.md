# pm: `tasks.sql` must never lose rows

On 2026-10-22 `pm run` replaced `tasks.sql` with a schema-only file while a `git pull --rebase --autostash` ran in the main checkout (`task 1689: Investigate and fix: pm run wrote a schema-only tasks.sql during a git autostash`). The cause is in pm, which lives outside this repo (nix package `pm`, `pm/__init__.py`); this is the write-up of the change pm needs.

## Cause
- `Project.loaded()` reloads when `file_key()` (inode, mtime, size) differs from the cache
- `file_key()` is `None` when `tasks.sql` doesn't exist; `loaded()` then reads no text and loads an empty `SCHEMA` database
- the branch `elif text is None: self.save(dump(con))` writes that empty database to `tasks.sql` at once, even for a read-only command
- git's autostash removes/rewrites tracked files (unlink + create, restore to HEAD); `pm run` (running_run, run rows, worker polling) reloaded in that gap, saw "no file", and wrote the schema-only file
- the later `git stash pop` then conflicted with the new file ("Your changes are safe in the stash")
- not the cause: `save()` already writes `tasks.sql.tmp` + `os.replace`, so a torn write isn't possible; a truncated read fails `load_sql` with a `FormatError`
- not reproduced by running it: the guard hook blocks a scratch `tasks.sql` here; the path above is read from the code

## Change for pm
- a missing `tasks.sql` creates a new project only in `pm init`-like commands (the first `pm milestone add`), and only if `git ls-files --error-unmatch tasks.sql` fails and HEAD has no `tasks.sql`
- otherwise (tracked, or `pm run` running with a cache): missing file is `FormatError("tasks.sql is missing, git may be rewriting it; try again")`, after a short retry (3 × 200 ms); never a write
- reads never write: drop `save()` from the `text is None` branch for read commands
- no shrink: in `connect(write=True)`, before `save(dump(con))`, compare the row count per table with the loaded database; fewer rows are an error unless the command is one that deletes (list them)
- also compare the file's `file_key()` just before `os.replace` with the one seen at load (under `pm.lock`); changed: reload and redo, or refuse ("changed under pm")
- `fsync` the temp file before `os.replace`
- test: fixture project with rows; a thread removes and restores `tasks.sql` in a loop while another runs `pm status` and a write; the file must never end with fewer rows

## Until then (this repo)
- while `pm run` is running in the main checkout, no `git stash`, `pull --autostash`, `rebase --autostash`, `checkout`/`restore` of `tasks.sql`; `pm stop` first or use the review worktree (README "Review in a separate worktree")
- recover: `git stash list`, `git show 'stash@{0}:tasks.sql' > tasks.sql`, `pm validate`
