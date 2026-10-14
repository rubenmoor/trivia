# 17 — Publishing: Licenses, Disclosures, Store

**Status:** stub

Part of the Steam plan ([11](11-steam.md)). Everything that has to be true legally and on paper before the game is sold or given away on Steam. Not legal advice: where it matters (tax, a company, contested licenses), check with a professional or with Valve's documentation.

## Media licenses
The non-rejected questions use 1,129 distinct files (1,100 for approved only). Tally from `trivia-media licenses` (2026-10-14; unchanged since 2026-10-11, the 3 replace files sit on needs_work questions):

| License | Files | What a commercial worldwide release needs |
|---|---|---|
| CC BY-SA 4.0 / 3.0 / 2.5 / 2.0 (incl. `at`, `de`, `igo`, `lu`, `nl` ports) | 631 | Credit (author, license, link) and the license name. ShareAlike applies to *adaptations*: the blurred decorative images (D-15) and crops may count as adaptations, which then must be offered under the same license. Shipping them as separate files with their license next to them meets that. |
| CC BY 4.0 / 3.0 / 2.5 / 2.0 (incl. `br`, `de`, `pl` ports) | 253 | Credit and a license link. |
| Public domain | 137 | Verdict per file from its PD reasons (`providers.licence_verdict`, D-62): `PD-USGov*` ok; PD-US only (`PD-US*`, `PD-1923`, `PD-Harris-Ewing`) is replaced (2 files, on needs_work questions). |
| CC0, "No restrictions" | 105 | Nothing (a credit is still nice). |
| FAL (Free Art License) | 2 | Credit and a license link; copyleft like BY-SA. |
| GFDL 1.2 (off allowlist) | 1 | Needs the full GFDL text shipped. Replaced instead (PUB-3; its question is needs_work). |

- **Non-copyright restrictions:** Commons marks some files with *personality rights* (identifiable people) or *trademark* warnings. They don't stop editorial use in a quiz; the developer checked them: keep every flagged file (D-61). The audit lists them for information only.
- **Credits in the game** (PUB-5, pm plan 47): each question shows its `credit` (06); the full list is generated at build time.
  - Generator: Vite plugin `app/client/credits.ts` (`vite.config.ts`), no Python. `npm run build` writes `credits.json` and `CREDITS.md` to the root of `app/client/dist/`; `npm run dev` serves `/credits.json`.
  - Content: every distinct media file in `app/data/pool.json` (title, author, licence, source link, provider; slot fields from PUB-2), sounds parsed from `app/client/public/audio/CREDITS.md` (incl. the Elgar note), fonts (OFL texts shipped in `fonts/`), controller glyphs (if `Glyph.svelte` exists), Svelte with its MIT text; a "Game" section from the root `LICEN[CS]E*` files (`LICENSE`, `LICENSE-content.md`, D-102). Electron's entry: task 621.
  - Build fails on a slot without `license` or `source_url` (ids listed); warns on GFDL.
  - `credits.json` carries no UI text (pm decision 49): unknown author is `null`, the screen's strings go through `t()`; `CREDITS.md` is English.
  - Screen: `app/client/src/game/Credits.svelte`, from the ☰ overlay («Créditos»); fetches `credits.json` on first open.
  - Desktop builds also: every runtime package of `app/desktop` (transitively, with licence texts) and «Steamworks SDK» (Valve's agreement) once `steamworks-ffi-node` ships; `credits.json` media rows carry `file_url`, fonts their `file`.
  - Checked both ways in the packaged build: `authoring/steam/credits_check.mjs` (release check step `credits`, plan 92): media files ↔ entries (`cacheName(file_url)`), sounds, fonts + OFL texts, asar packages and `resources/steamworks_sdk/` ↔ libraries, `CREDITS.md` present.
  - Shipped: `CREDITS.md` in `dist/`, so in `nix build .#app` (`share/trivia/app/client/dist/`) and the desktop build (`resources/client/`); at the artefact root: 18 "Builds and depots".
- **Audio:** `app/client/public/audio/CREDITS.md` (UI-10): CC0 / CC BY. Elgar's «Pomp and Circumstance» by the US Marine Band: a US government work, public domain in the US and generally treated as free elsewhere. Note it in the credits.
- **Fonts:** Baloo 2 and Nunito are OFL. Ship the license texts with them.
- **Controller glyphs** (IN-5): original, drawn for the game (`Glyph.svelte`). Console makers' button art can't be used freely.

## Code and content license (OQ-35)
Decided (D-102): MIT code, reserved questions, one public repo.
- **Code:** MIT, `LICENSE` at the root; `modding/` included.
- **Questions:** all rights reserved, `LICENSE-content.md` (`authoring/data/`, `app/data/`); personal, non-commercial play from the repo allowed.
- **Not covered:** media (per file), fonts (OFL), UI audio, npm deps.
- **Public:** whole repo, release content included (D-17 stays); buyers get `pool.json` in plain JSON anyway, the licence forbids reuse.
- **Lawyer check owed:** protectability of the AI-drafted, human-reviewed pool; wording next to MIT; forks of unlicensed commits. PUB-10 is settled ("AI disclosure").

## AI disclosure
Steam requires developers to disclose AI-generated content on the store page (content survey). For this game:
- **Pre-generated content:** questions, hints, answers and translations are drafted by Claude, fact-checked by Claude with web search, and reviewed by a person or by Claude (D-7, D-10, D-32, D-33). Describe the review steps honestly.
- **Not AI:** the images (Wikimedia Commons, by people), the music, the code's runtime (no AI at play time; no live generation).
- **Anthropic's terms (PUB-10):** outputs may be sold. `claude -p` on the developer's Claude subscription (D-10) → Consumer Terms (anthropic.com/legal/consumer-terms, effective 2025-10-08, read 2026-10-14). Anthropic assigns all its rights in Outputs to the user (§4, "if any": no promise they're protectable); no non-commercial limit (that applies only to evaluation access); no attribution needed. Questions, translations and code may ship in a paid game.
  - Competing-models clause (§3): doesn't apply, since the game trains no model and resells no Claude access.
  - Scripts (§3): automated access is banned unless Anthropic "explicitly permit[s] it". Running headless Claude Code (the published `claude` binary, the developer's own login) is permitted: code.claude.com/docs/en/legal-and-compliance (read 2026-10-14), "ordinary, individual usage of Claude Code and the Agent SDK".
  - Trademarks (§12 "Use of our brand"): no Anthropic or Claude name or logo on the store page or in the game without written permission. The disclosure says "LLM", which is fine.
  - Usage Policy (anthropic.com/legal/aup, version effective 2026-11-12, read 2026-10-14): its AI-disclosure rule is for live chatbots, which the game doesn't have.
  - API keys would fall under the Commercial Terms (effective 2025-06-17), which have the same ownership of Outputs. No reason to switch.

## Steamworks and store
- **Account:** Steamworks partner signup, identity and tax interview (bank details, a W-8BEN for non-US individuals or the company equivalent), and a **$100 app credit** per game (recouped after $1,000 revenue). Holder: the developer as a person, W-8BEN, after a tax advisor check; store Developer/Publisher as a label; company later via app transfer (D-98).
- **Price (D-98):** paid one-time purchase, $9.99 for now; Valve's regional matrix; launch discount; packs as free DLC (D-95), no paid DLC.
- **Name (D-50):** «Living Room Trivia», with the Steam localized name «Trivia en Familia» for Spanish (Steamworks → General Application Settings; same limits as a name change, so set both before the coming-soon page). Check both names on Steam, in trademark registers and for a domain (PUB-7).
- **Store page:** capsule images in the required sizes, screenshots, a trailer (20 s of gameplay per store language, `trivia-trailer`, PUB-8, pm plan 88), short and long description per language (LUI-6), system requirements, supported languages table, controller support flags, Steam Deck compatibility.
- **Content survey / age rating:** the Steam questionnaire (no violence, no gambling; kid-friendly). IARC is optional on Steam.
- **Privacy:** the game sends nothing on its own; only a question report on the player's «Enviar» (plan 103). Texts: public `PRIVACY.md` (en, es, de); store-page paragraph per language and the Steamworks steps in `11-steam.md` "Privacy (ST-5)" (task 867). Player names stay on the device (and in Steam Cloud).
- **"Coming soon" page** at least two weeks before release (Valve rule, partner.steamgames.com/doc/store/coming_soon, read 2026-10-13), better months, to collect wishlists. Rules and developer checklist: `11-steam.md` "Coming soon page (ST-3)".
- **Launch:** preconditions, timeline, release candidate, launch-day checklist (build live on `default`, price, launch discount, languages, report thread, Release, announcement), first week: `11-steam.md` "Launch (S6)" (pm plan 95).

## Tasks
- [x] PUB-1 Media license audit: a `media.py licenses` report per file (license, PD reason, Commons restriction templates); list the files to replace (PD-US-only, GFDL); restriction flags are listed, not replaced (D-61). *pm plan 52, 2026-10-11: 1,129 distinct files (non-rejected); 3 to replace: off-allowlist 1 (q-0021, GFDL 1.2), PD-US only 2 (q-1100, q-1194); 23 restriction flags on 21 files (personality 14, trademarked 5, design 2, fan-art 1, insignia 1).*
- [x] PUB-2 Store the full license data per media item (license URL, author link, restrictions) in the pool, not just the `credit` string; `validate` requires it for approved questions. *pm plan 26, 2026-10-11: all 1,202 picks migrated; validate errors (q-0021, GFDL only, set to needs_work until part 3 replaces it; decision 10).*
- [x] PUB-3 Replace the problem files from PUB-1 in the review tool. *pm plan 53, 2026-10-14: no replacement pass (decision 47): q-0021 (GFDL 1.2, Container_Ship.jpg), q-1100 (PD-US-not renewed, HitComicsNo19.jpg), q-1194 (PD-Harris-Ewing, PD-US-no notice, LCCN2016872269.jpg) are needs_work, out of the export; new files when they're reworked. Gate: `qgen validate` errors on an approved pick with verdict `replace`, reasons in the message; `/review?licence=replace` stays as the list's view.*
- [x] PUB-4 Decide the code and content license (OQ-35); add a `LICENSE` file. *pm plan 40, 2026-10-14 (D-102): `LICENSE` (MIT), `LICENSE-content.md` (questions reserved; `modding/` MIT; media, fonts, sounds excluded); both at the desktop artefact root (`electron-builder.yml` `extraFiles`), in the credits' "Game" section; README "License", `directory.md`.*
- [x] PUB-5 Credits screen and a generated `CREDITS.md` in the build (media, audio, fonts, glyphs, libraries). *Done 2026-10-12 (pm plan 47): `app/client/credits.ts` writes `dist/credits.json` + `dist/CREDITS.md` (1,102 media, 13 sounds, fonts, glyphs, Svelte); Credits screen from the ☰ overlay. Open: Electron entry (task 621), `CREDITS.md` at the desktop artefact root, Game section after OQ-35.*
- [ ] PUB-6 Steamworks signup as a private person (D-98): tax advisor check first (pm decision 67's questions: registration, treaty rate, VAT, DSA address); identity, bank, W-8BEN tax interview; store Developer/Publisher label; pay the $100 app credit (DLC packs need none).
- [ ] PUB-7 Name and trademark check for «Living Room Trivia» and «Trivia en Familia» (D-50); if it fails, OQ-34 reopens.
- [ ] PUB-8 Store page: texts, capsules, screenshots, trailer, AI disclosure, privacy line. *Plan: pm plan 88 (drafts in `17a-store-page.md`, capsule art: pm decision 77, scripted screenshots, scripted trailer `trivia-trailer`).*
- [ ] PUB-9 Content survey and age rating.
- [x] PUB-10 Check Anthropic's commercial-use terms for the generated content. *pm plan 129, 2026-10-14: Consumer Terms (effective 2025-10-08) apply to `claude -p` on the developer's subscription. Outputs are assigned to the user and may be sold, with no attribution needed. Headless Claude Code is explicitly permitted. Disclosure facts unchanged. Details are under "AI disclosure".*
- [ ] PUB-11 Price (D-98): confirm $9.99 against comparable titles; Valve's recommended regional prices (check EUR, MXN, COP, LATAM-USD); launch discount % and length per Valve's discount rules; every pack DLC free.
