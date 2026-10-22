# Directory

What the top-level `.md` files and directories are for (decision 196). It names no deeper paths and is not kept in sync with every file; the code and each folder's own docs are the reference. `authoring/` may use code from `app/`, never the other way round ([`plans/19-repo-layout.md`](plans/19-repo-layout.md)).

## Files
- `README.md`: human how-tos (setup, commands, environment variables)
- `AGENTS.md`: guide for AI coding assistants; `CLAUDE.md` imports it
- `code-review.md`: code review report: milestone 13's file-by-file review, then each milestone's cleanup review (decision 201)
- `LICENSE-content.md`: questions' licence (all rights reserved, personal play allowed); code: `LICENSE` (MIT)
- `PRIVACY.md`: public privacy policy (reports, telemetry)
- `directory.md`: this file

## Directories
- `app/`: the game as it ships (server, client, Electron shell, `app/data/` pools)
- `authoring/`: tooling that never ships (source pool, `qgen`, authoring server/UI, store, Steam upload)
- `modding/`: modding guide and player kit, shipped in the install folder
- `plans/`: plans, decisions, open questions; start at [`plans/README.md`](plans/README.md)
- `report-server/`: question report and telemetry server (Cloudflare Worker), not shipped
- `.claude/`: Claude Code project settings (Ponytail plugin)
- Gitignored:
  - `media/`: media cache
  - `state/`: saves and local authoring state
  - `work/`: pipeline and build work files
  - `mods/`: local mods for development
