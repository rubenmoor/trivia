# 17 — Publishing: Licenses, Disclosures, Store

**Status:** in progress: PUB-10 done; PUB-7 waits on pm decision 176, PUB-6 on pm decision 177 (pm plan 129)

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

## Price (PUB-11)
Base price, regional prices, launch discount and the free DLC setup, drafted 2026-10-14 (`task 1048`) from Valve's public docs and the store as it is today. Approval goes through the pm decision "Price, regional prices and launch discount? (PUB-11)"; the developer enters the values via `task 1049: Content survey and pricing: entry checklist and the 'entered' decision (PUB-9, PUB-11)`. Workers never log into Steamworks.

### Valve's rules (read 2026-10-14)
- [Pricing](https://partner.steamgames.com/doc/store/pricing):
  - initial price and every change reviewed by Valve, "usually processed within one or two business days"
  - 37 currencies + 4 region groups; a currency without a price → game not buyable there
  - three conversion methods in the "Propose Pricing" tool, relative to a USD price: exchange rate only, purchasing power only, multi-variable (purchasing power, comparable entertainment prices, exchange rate); Valve "suggest[s] prices in the Propose Pricing tool … which you may accept or adjust"
  - the per-currency matrix ([pricing explorer](https://partner.steamgames.com/pricing/explorer)) is "Valve Confidential", behind the partner login: no numbers here
  - price changes only after 30 days from release (launch errors excepted via support); a price increase in any currency → 30-day discount cooldown
  - minimum base price = multi-variable value of the $0.99 tier; irrelevant at $9.99
- [Supported currencies](https://partner.steamgames.com/doc/store/pricing/currencies): COP, CLP in whole units; `USD_LATAM` region group (a discounted USD price) for Argentina, Bolivia, Ecuador, Paraguay, Venezuela, Central America (Belize, El Salvador, Guatemala, Honduras, Nicaragua, Panama), Guyana, Suriname; Europe without a local currency pays EUR
- [Discounting](https://partner.steamgames.com/doc/marketing/discounts):
  - launch discount: optional, 10–40 %, 7–14 days, ends 10:00 Pacific; set up only before the release date, on the app landing page right below the intended release date (not in the discount dashboard); editable until it starts
  - Valve's suggestion: "around 10% to 15%"; warns against a "very high launch discount"
  - no other discount for 30 days after release; every discount (launch included) starts a 30-day cooldown after it ends
  - seasonal sales (Spring, Summer, Autumn, Winter) are exempt from discount cooldowns, not from the release cooldown: a game joins one only if released ≥ 30 days before its start ([Upcoming events](https://partner.steamgames.com/doc/marketing/upcoming_events): Winter 2026-12-17 – 2027-01-04, Spring 2027-03-18 – 03-25, Summer 2027-06-24 – 07-08)
  - no base price change while a discount is active or scheduled
  - ≥ 20 % triggers wishlist e-mails
  - "Discount all associated packages … at the same time": moot, DLC free
- [DLC](https://partner.steamgames.com/doc/store/application/dlc): own app ID per DLC (base app → "All Associated Packages, DLC, Demos And Tools" → "Add New DLC"); DLC depots live in the base app; price page silent on free DLC
- [Free to Play](https://partner.steamgames.com/doc/store/freetoplay): a free product is set at creation ("This is a free product" under Options) and shows "free" in its store package, no pricing entered; every DLC goes through its own store page, review and release; DLC needs no app credit (D-98)

### Comparables (store API, 2026-10-14, US prices, list price)
| Title | Price | Reviews | DLC |
|---|---|---|---|
| Jackbox Party Pack 3 (434170) | $24.99 | 6,678, overwhelmingly positive | no |
| Jackbox Party Pack 6 (1005300) | $29.99 | 3,105, very positive | no |
| Trivia Murder Party 3 (3048060, 2026) | $14.99 | 165, mixed | no |
| Who Wants To Be A Millionaire (1356240) | $29.99 | 715, mixed | 15 (packs $2.99, some free, season pass $14.99) |
| You Don't Know Jack Vol. 2 (259940) | $2.99 | 108, very positive | no; each volume its own app |
| Trivia Vault: 1980's Trivia (689180) | $13.99 list, 90 % off ($1.39) | 173, mixed | no; one app per topic |
| Party Quiz (2024070) | $11.99 | 1,639, very positive | no |
| Trivia Tricks (1404090) | $14.99 | 244, very positive | no |
| Trivia About You (3196180) | $14.99 | 192, very positive | 1 |
| Papa's Quiz (1484730) | $12.99 | 145, very positive | no |
| The You Quiz (3669740) | $9.99 | 104, very positive | 1 |
| Trivia War (3472880) | $9.99 | 17, positive | no |
| Quiz Night Tonight! (549280) | $9.99 | 8 | no |
| Trivia Throwdown (991240) | $4.99 | 33, positive | no |
- Decision 66's table rechecked: Trivial Pursuit Live! and SongPop Party no longer found in the store search; You Don't Know Jack sells per volume ($1.99–2.99), not as DLC; Millionaire is $29.99, not ≈$19.99.
- $9.99: half the big party packs, below the indie party-quiz band ($11.99–14.99), level with the smaller quiz titles; fits a game with ~1,000 Spanish questions at launch and free packs.

### Regional prices
- Valve's recommendation for $9.99 only in Steamworks → Propose Pricing; developer's step: pick $9.99, accept Valve's suggested prices for every currency and region group, read off these rows into the "entered" decision:
  - USD, EUR, GBP, CHF, MXN, COP, CLP, PEN, `USD_LATAM` (Argentina etc.)
- Plausibility only, not Valve's matrix: $9.99 titles today (cc=…, 2026-10-14), The You Quiz / Trivia War / Quiz Night Tonight!:
  - EUR 9.99 / 9.75 / –; GBP 8.99 / 8.50 / 6.99; CHF 8.75 / 10.99 / 10.00
  - MXN 139.99 / 123.99 / 109.99; COP 26,999 / 26,000 / 23,500; CLP 6,599 / 5,750 / 5,500; PEN 25.99 / 23.00 / 27.95
  - Argentina (`USD_LATAM`) $6.29 / $5.79 / $9.99
  - a row far outside these → recheck the tool's method (multi-variable is the default to accept)

### Launch discount
- Proposal: 15 % for 7 days ($9.99 → $8.49): inside Valve's 10–40 %, 7–14 days, at the top of Valve's "10% to 15%"; release already e-mails wishlisters (`11-steam.md` ST-3), so no need for 20 %.
- Entered before release, on the app landing page below the release date; with the launch-day checklist (`11-steam.md` "Launch (S6)").
- Blocks afterwards:
  - any other discount until release + 30 days, and until 30 days after the launch discount ends (7 days: release + 37 days)
  - seasonal sales: open from release + 30 days regardless of the launch discount; release ≥ 30 days before a sale's start to join it
  - price changes: none in the first 30 days, none while it runs

### Free DLC (`colombia` and every later pack)
- One DLC app per shipped pack ("Add New DLC"), marked free ("This is a free product"; Valve's DLC page doesn't name the field, recheck at entry); no price, no regional rows, no launch discount.
- Own store page and review per DLC (store texts: `17a-store-page.md` "Free DLC"); depot in the base app (D-95, `18-steam-integration.md` "DLC").
- Later packs: same steps; never a price (decision 66).

## Name check (PUB-7)
This section records what a worker found for the three store names: «Living Room Trivia» (en, default), «Trivia en Familia» (es, es-ES) and «Wohnzimmer-Quiz» (de, decision 78). It is research, not legal advice; a professional clearance search is optional and the developer's call. The result is pm decision "Store names pass PUB-7?" (pm plan 129).
- Sources (all read 2026-10-14):
  - Steam: store search (`store.steampowered.com/search`, also the suggest box), in English, Spanish and German. The full app list API (`ISteamApps/GetAppList`) is retired, so there's no check beyond the store search.
  - USPTO: `tmsearch.uspto.gov`, word marks.
  - TMview (`tmdn.org/tmview`): EUIPO, the EU national offices, WIPO Madrid (WO) and others.
  - WIPO Global Brand Database: not checked directly because of its captcha. Madrid marks are covered through TMview.
  - App Store (iTunes search, us/es/de) and Play Store search.
  - Domains: RDAP (Verisign, DENIC) and whois (.com.co).
  - Not checked: BoardGameGeek (Cloudflare blocks it). A general web search only worked for «Living Room Trivia».
- Classes: 9 (software), 28 (games), 41 (entertainment). Marks are listed only if they're live.

| Name | Source | Hit | Class | Owner | Status | Read |
|---|---|---|---|---|---|---|
| Living Room Trivia | Steam | none (titles with «Living Room» are other genres: «A Living Room», «Home Designer - Living Room») | – | – | – | 2026-10-14 |
| Living Room Trivia | USPTO | none exact, none for «living room» + trivia/quiz/game | – | – | – | 2026-10-14 |
| Living Room Trivia | USPTO | similar: LIVING ROOM 97883498, 97883506 (nightclub events, music production) | 41 | LIVINGROOM LLC | registered 2026-07-21 | 2026-10-14 |
| Living Room Trivia | USPTO | similar: LIVING ROOM 78698523 (cinemas) | 41 | Living Room Theaters, Inc. | registered | 2026-10-14 |
| Living Room Trivia | USPTO | similar: LIVING ROOM LIVE 88861046 (fitness streaming app) | 9, 41 | BB Body, Inc. | registered | 2026-10-14 |
| Living Room Trivia | TMview | none exact | – | – | – | 2026-10-14 |
| Living Room Trivia | TMview | similar: LIVING ROOM, AT 538/2018 | 9, 35, 41, 43 | Thomas E. Pausch | registered | 2026-10-14 |
| Living Room Trivia | TMview | similar: THE LIVING ROOM, FR 4360442 | 9, 35, 38, 39, 41–43 | Bercy Services XXIX SAS | registered | 2026-10-14 |
| Living Room Trivia | TMview | similar: LivingRoom, DE 3020170096275; The Livingroom, EM 019277580 | 41 (+36, 44, 45 / 35, 43) | EWING MEDIA GmbH; Neamciuc Learning | registered | 2026-10-14 |
| Living Room Trivia | App Store, Play | none exact | – | – | – | 2026-10-14 |
| Living Room Trivia | web | similar: Instagram account @livingroomtrivia «Living Room Trivia» (93 followers) | – | unknown | active | 2026-10-14 |
| Living Room Trivia | domain | livingroomtrivia.com free | – | – | – | 2026-10-14 |
| Trivia en Familia | Steam | none | – | – | – | 2026-10-14 |
| Trivia en Familia | USPTO | none (also none for familia + trivia) | – | – | – | 2026-10-14 |
| Trivia en Familia | TMview | none exact, none for «trivia familia» | – | – | – | 2026-10-14 |
| Trivia en Familia | TMview | similar: EN FAMILIA, ES M2994232 | 41 | Asociación Española de Pediatría | registered | 2026-10-14 |
| Trivia en Familia | TMview | similar: EN FAMILIA, CL 886022; AR 2989662 | 41 | Televisión Nacional de Chile; Anheuser-Busch InBev | registered | 2026-10-14 |
| Trivia en Familia | TMview | similar: CINE EN FAMILIA, ES M2906406 | 38, 41 | Mediaset España | registered | 2026-10-14 |
| Trivia en Familia | App Store es | similar: «Trivia Family - En Español» | app | TITANWARE SL | live | 2026-10-14 |
| Trivia en Familia | Play | similar: «Family Trivia» (English) | app | unknown | live | 2026-10-14 |
| Trivia en Familia | domain | triviaenfamilia.com, trivia-en-familia.com free; .com.co both free; .es: whois.nic.es refuses anonymous lookups, no DNS (likely free) | – | – | – | 2026-10-14 |
| Wohnzimmer-Quiz | Steam (German) | none («Familienquiz» → «Family Quiz», a different name) | – | – | – | 2026-10-14 |
| Wohnzimmer-Quiz | USPTO | none for wohnzimmer* | – | – | – | 2026-10-14 |
| Wohnzimmer-Quiz | TMview | none exact, none for «Wohnzimmer» + Quiz/Spiel | – | – | – | 2026-10-14 |
| Wohnzimmer-Quiz | TMview | similar: Wohnzimmerwissen, DE 3020262533264 | 9, 41, 44 | Bamarni Skin UG | filed | 2026-10-14 |
| Wohnzimmer-Quiz | TMview | similar: WORLD WIDE WOHNZIMMER, DE 3020192217334 | 9, 16, 21, 25, 35, 38, 41 | TWIN.TV GmbH | registered | 2026-10-14 |
| Wohnzimmer-Quiz | TMview | similar: Wohnzimmerkonzert, EM 013503685; WOHNZIMMER GE, DE 3020162352888 | 41 (+35, 43) | SofaConcerts GmbH; Paul Pillath | registered | 2026-10-14 |
| Wohnzimmer-Quiz | App Store de, Play | none | – | – | – | 2026-10-14 |
| Wohnzimmer-Quiz | domain | wohnzimmer-quiz.de, wohnzimmer-quiz.com, wohnzimmerquiz.com free; wohnzimmerquiz.de in DENIC's redemption period (recently dropped) | – | – | – | 2026-10-14 |

- Findings:
  - No Steam game is named after any of the three.
  - No live identical mark was found in classes 9, 28 or 41.
  - Riskiest hits:
    - «Living Room» word marks in classes 9/41 (AT, FR; in the US, nightclubs and cinemas). «Trivia» is descriptive, so «Living Room» carries the name, but none of these marks covers games.
    - «EN FAMILIA» in class 41 in Spain (a pediatrics association) and Chile (a TV show).
    - «Trivia Family - En Español» on the Spanish App Store.
    - For «Wohnzimmer-Quiz», nothing close; «Wohnzimmer» is a common word in German marks.

## Steamworks signup (PUB-6)
This is the developer's checklist for becoming a Steamworks partner as a person (decision 67, D-98) and creating the app. Workers only research and write it; every step below is the developer's. Valve's order is paperwork, then the fee, then bank, tax and identity, so the advisor check comes before the first step. Once done, report it in pm decision 177 "Steamworks app created? App ID?" (pm plan 129). Not legal or tax advice.
- Sources (read 2026-10-14):
  - partner.steamgames.com/doc/gettingstarted (overview)
  - /doc/gettingstarted/onboarding (paperwork, legal name, bank, tax, the 21-day rule)
  - /doc/gettingstarted/appfee (Steam Direct fee)
  - /doc/finance/taxfaq and /doc/gettingstarted/faq (withholding, W-8BEN, TIN, VAT)
  - /doc/store/application/dlc (DLC apps)
- Facts from those pages:
  - Individual: company form «Sole Proprietorship», legal first and last name as the company name, no alias or "doing business as" name. The bank account holder must match that name.
  - Tax interview: a W-8BEN-like questionnaire for treaty countries. Withholding on US sales is 0–30%. Treaty rates need a foreign TIN or a US TIN (ITIN or EIN). There are no refunds for amounts withheld before a TIN is added. A third party verifies the answers in 10–15 business days, and nothing can be changed until it's done.
  - Fee: $100 (or the local equivalent) per app. It's paid in the Steam store from the developer's own Steam account (not with wallet funds), and VAT may be added. It isn't refundable. It's recouped in the payment after the app reaches $1,000 adjusted gross revenue. The invoice goes to the Steam user who paid.
  - DLC: created from the base app ("All Associated Packages, DLC, Demos And Tools" → "Add New DLC"). Neither the fee page nor the DLC page asks for a fee, so free DLC packs (decision 66) need no app credit.
  - First titles: ≥ 21 days between paying the fee and release, and ≥ 2 weeks of public "Coming soon" (`11-steam.md` "Coming soon page (ST-3)").
  - VAT: Valve collects and remits VAT/GST in the countries on its list. Prices include it. The developer's own obligations are the advisor's question.
  - The DSA trader address isn't on these pages; that's an advisor question.

### Checklist
- [ ] **Advisor check first** (decision 67). Questions for the tax advisor:
  - Do I have to register as a sole trader (self-employed) in my country before the first sale? Which form, and when?
  - US withholding: does my country have a US tax treaty, and what is its rate for royalties (copyright)? Is my national tax ID enough for the W-8BEN, or do I need an ITIN or EIN? Can I credit the US tax I pay against my own?
  - VAT/OSS: Valve collects and remits EU VAT on Steam sales. Do I still owe VAT on my revenue share from Valve (a B2B service from a US company: reverse charge? small-business exemption?), and do I need an OSS registration?
  - DSA trader: is the address shown on the store page my home address? Is a business or c/o address acceptable?
  - When should I switch to a company (revenue threshold, liability, the DSA address)? Steam allows an app transfer later (D-98).
  - Income tax: how is Steam revenue booked (monthly payments, fee recoupment)? Is the $100 fee deductible?
- [ ] **Partner signup** (partner.steamgames.com, logged in with the developer's Steam account): legal first and last name, company form «Sole Proprietorship», address, contact e-mail; sign the NDA and the Steam Distribution Agreement electronically; identity verification.
- [ ] **Pay the $100 app credit** (Steam Direct fee, part of the paperwork). Note the payment date: release comes ≥ 21 days later (`11-steam.md` "Coming soon page (ST-3)").
- [ ] **Bank details**: an account in the developer's legal name (routing number, account number, bank address).
- [ ] **Tax interview**: the W-8BEN questionnaire for a non-US individual. Enter the TIN the advisor named to get the treaty rate. Then wait 10–15 business days for verification and watch e-mail for document requests.
- [ ] **Store Developer/Publisher label**: the developer's choice, e.g. a studio label. It's only a label, not a company and not the legal name. It's set on the store page later; decide it now so the decision answer can carry it.
- [ ] **Create the app** with the app credit: name «Living Room Trivia» if PUB-7 passed (pm decision "Store names pass PUB-7?"), else a working name, which can change before "Coming soon". Note the App ID.
  - DLC apps (one per shipped pack, decision 66) are created later from the base app, with no app credit: `task 254: write plan: Steamworks app configuration (SW-7)`.
- Not here: the build account and its permissions (`plan 89: Builds, depots and upload (SW-10, SW-6)`); the switch from Spacewar 480 to the real App ID (SW-7).
- Report in the pm decision: App ID, payment date of the app credit, Developer/Publisher label.

## Tasks
- [x] PUB-1 Media license audit: a `media.py licenses` report per file (license, PD reason, Commons restriction templates); list the files to replace (PD-US-only, GFDL); restriction flags are listed, not replaced (D-61). *pm plan 52, 2026-10-11: 1,129 distinct files (non-rejected); 3 to replace: off-allowlist 1 (q-0021, GFDL 1.2), PD-US only 2 (q-1100, q-1194); 23 restriction flags on 21 files (personality 14, trademarked 5, design 2, fan-art 1, insignia 1).*
- [x] PUB-2 Store the full license data per media item (license URL, author link, restrictions) in the pool, not just the `credit` string; `validate` requires it for approved questions. *pm plan 26, 2026-10-11: all 1,202 picks migrated; validate errors (q-0021, GFDL only, set to needs_work until part 3 replaces it; decision 10).*
- [x] PUB-3 Replace the problem files from PUB-1 in the review tool. *pm plan 53, 2026-10-14: no replacement pass (decision 47): q-0021 (GFDL 1.2, Container_Ship.jpg), q-1100 (PD-US-not renewed, HitComicsNo19.jpg), q-1194 (PD-Harris-Ewing, PD-US-no notice, LCCN2016872269.jpg) are needs_work, out of the export; new files when they're reworked. Gate: `qgen validate` errors on an approved pick with verdict `replace`, reasons in the message; `/review?licence=replace` stays as the list's view.*
- [x] PUB-4 Decide the code and content license (OQ-35); add a `LICENSE` file. *pm plan 40, 2026-10-14 (D-102): `LICENSE` (MIT), `LICENSE-content.md` (questions reserved; `modding/` MIT; media, fonts, sounds excluded); both at the desktop artefact root (`electron-builder.yml` `extraFiles`), in the credits' "Game" section; README "License", `directory.md`.*
- [x] PUB-5 Credits screen and a generated `CREDITS.md` in the build (media, audio, fonts, glyphs, libraries). *Done 2026-10-12 (pm plan 47): `app/client/credits.ts` writes `dist/credits.json` + `dist/CREDITS.md` (1,102 media, 13 sounds, fonts, glyphs, Svelte); Credits screen from the ☰ overlay. Open: Electron entry (task 621), `CREDITS.md` at the desktop artefact root, Game section after OQ-35.*
- [ ] PUB-6 Steamworks signup as a private person (D-98): tax advisor check first (pm decision 67's questions: registration, treaty rate, VAT, DSA address); identity, bank, W-8BEN tax interview; store Developer/Publisher label; pay the $100 app credit (DLC packs need none). *Checklist: "Steamworks signup (PUB-6)" (pm plan 129); waits on pm decision 177.*
- [ ] PUB-7 Name and trademark check for «Living Room Trivia» and «Trivia en Familia» (D-50); if it fails, OQ-34 reopens.
- [ ] PUB-8 Store page: texts, capsules, screenshots, trailer, AI disclosure, privacy line. *Plan: pm plan 88 (drafts in `17a-store-page.md`, capsule art: pm decision 77, scripted screenshots, scripted trailer `trivia-trailer`).*
- [ ] PUB-9 Content survey and age rating.
- [x] PUB-10 Check Anthropic's commercial-use terms for the generated content. *pm plan 129, 2026-10-14: Consumer Terms (effective 2025-10-08) apply to `claude -p` on the developer's subscription. Outputs are assigned to the user and may be sold, with no attribution needed. Headless Claude Code is explicitly permitted. Disclosure facts unchanged. Details are under "AI disclosure".*
- [ ] PUB-11 Price (D-98): confirm $9.99 against comparable titles; Valve's recommended regional prices (check EUR, MXN, COP, LATAM-USD); launch discount % and length per Valve's discount rules; every pack DLC free.
