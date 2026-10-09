# 17 — Publishing: Licenses, Disclosures, Store

**Status:** stub

Part of the Steam plan ([11](11-steam.md)). Everything that has to be true legally and on paper before the game is sold or given away on Steam. Not legal advice: where it matters (tax, a company, contested licenses), check with a professional or with Valve's documentation.

## Media licenses
The approved questions use about 290 Commons files. The tally of their credits (2026-10-07):

| License | Files | What a commercial worldwide release needs |
|---|---|---|
| CC BY-SA 4.0 / 3.0 / 2.5 / 2.0 (incl. `de`, `igo` ports) | ~170 | Credit (author, license, link) and the license name. ShareAlike applies to *adaptations*: the blurred decorative images (D-15) and crops may count as adaptations, which then must be offered under the same license. Shipping them as separate files with their license next to them meets that. |
| CC BY 4.0 / 3.0 / 2.5 / 2.0 | ~60 | Credit and a license link. |
| Public domain | ~35 | Check the reason. `PD-US`-only files (e.g. US publication before 1930) may still be under copyright elsewhere; replace them for a worldwide release or check per file. |
| CC0, "No restrictions" | ~25 | Nothing (a credit is still nice). |
| GFDL 1.2 | 1 | Needs the full GFDL text shipped. Easier to replace the file. |
| FAL (Free Art License) | 1 | Credit and a license link; copyleft like BY-SA. |

- **Non-copyright restrictions:** Commons marks some files with *personality rights* (identifiable people) or *trademark* warnings. Those don't stop editorial use in a quiz, but check each flagged file.
- **Credits in the game:** each question already shows its `credit` (06). The release also needs a **credits screen** listing every file with author, license and source link, generated from the pool at build time, plus `CREDITS.md` in the shipped files.
- **Audio:** `app/client/public/audio/CREDITS.md` (UI-10): CC0 / CC BY. Elgar's «Pomp and Circumstance» by the US Marine Band: a US government work, public domain in the US and generally treated as free elsewhere. Note it in the credits.
- **Fonts:** Baloo 2 and Nunito are OFL. Ship the license texts with them.
- **Controller glyphs** (IN-5): use a CC0 set or draw them. Console makers' button art can't be used freely.

## Code and content license (OQ-35)
- The repo has **no license file** today, which means "all rights reserved" by default, even though it is public. Options: keep it like that; MIT/GPL for the code with the questions under a separate license (e.g. CC BY-SA, or reserved); or make the repo private before release.
- The question pool is public on GitHub. Anyone could copy it into another game. Decide whether new release content (translations, new batches) stays public.

## AI disclosure
Steam requires developers to disclose AI-generated content on the store page (content survey). For this game:
- **Pre-generated content:** questions, hints, answers and translations are drafted by Claude, fact-checked by Claude with web search, and reviewed by a person or by Claude (D-7, D-10, D-32, D-33). Describe the review steps honestly.
- **Not AI:** the images (Wikimedia Commons, by people), the music, the code's runtime (no AI at play time; no live generation).
- Check Anthropic's terms for commercial use of outputs (they allow it for paid API use; the pipeline runs on `claude -p` under the author's account, so check the plan type).

## Steamworks and store
- **Account:** Steamworks partner signup, identity and tax interview (bank details, a W-8BEN for non-US individuals or the company equivalent), and a **$100 app credit** per game (recouped after $1,000 revenue). Person or company: OQ-33.
- **Name (D-50):** «Living Room Trivia», with the Steam localized name «Trivia en Familia» for Spanish (Steamworks → General Application Settings; same limits as a name change, so set both before the coming-soon page). Check both names on Steam, in trademark registers and for a domain (PUB-7).
- **Store page:** capsule images in the required sizes, screenshots, a trailer (optional but strongly advised), short and long description per language (LUI-6), system requirements, supported languages table, controller support flags, Steam Deck compatibility.
- **Content survey / age rating:** the Steam questionnaire (no violence, no gambling; kid-friendly). IARC is optional on Steam.
- **Privacy:** the game collects nothing and sends nothing. Say so on the store page. Player names stay on the device (and in Steam Cloud).
- **"Coming soon" page** at least two weeks before release (Valve rule), better months, to collect wishlists.

## Tasks
- [ ] PUB-1 Media license audit: a `media.py licenses` report per file (license, PD reason, Commons restriction templates); list the files to replace (PD-US-only, GFDL, flagged).
- [ ] PUB-2 Store the full license data per media item (license URL, author link, restrictions) in the pool, not just the `credit` string; `validate` requires it for approved questions.
- [ ] PUB-3 Replace the problem files from PUB-1 in the review tool.
- [ ] PUB-4 Decide the code and content license (OQ-35); add a `LICENSE` file.
- [ ] PUB-5 Credits screen and a generated `CREDITS.md` in the build (media, audio, fonts, glyphs, libraries).
- [ ] PUB-6 Steamworks signup, tax and identity; pay the app credit (OQ-33).
- [ ] PUB-7 Name and trademark check for «Living Room Trivia» and «Trivia en Familia» (D-50); if it fails, OQ-34 reopens.
- [ ] PUB-8 Store page: texts, capsules, screenshots, trailer, AI disclosure, privacy line.
- [ ] PUB-9 Content survey and age rating.
- [ ] PUB-10 Check Anthropic's commercial-use terms for the generated content.
- [ ] PUB-11 Price and regional pricing (OQ-33).
