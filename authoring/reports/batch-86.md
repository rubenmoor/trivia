# batch-86

Made by `qgen batch --media-first` on 2026-11-18 (plans/19-repo-layout.md, D-36). Generated file: don't edit by hand.

- Bundle: base
- Language: English
- Subcategories (0): 
- Merged: 58 (q-21133…q-21190)
- Approved: 49
- Needs work: 9
- Dropped by the pipeline: 29
- Reviewed by: claude-opus-5-5
- Claude calls: 783, about $71.09 at list price; $1.45 per approved
- Picked files not cached yet: 0

## Health

Batch health (plan 15): this batch and the two before it (batch-84, batch-85; across the source-locale switch too, decision 233), ✓/✗ against the thresholds in `authoring/data/targets.json`; a ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look. Needs-work counts are `record`'s decisions; `problems guessed` = classified from feedback.

| metric | threshold | batch-84 | batch-85 | batch-86 |
|---|---|---:|---:|---:|
| source locale |  | en | en | en |
| mode |  | media-first | media-first | media-first |
| drafts |  | 94 | 92 | 87 |
| skipped slots |  | 0 | 0 | 0 |
| dropped |  | 31 | 43 | 29 |
| drop rate | ≤ 20.0 % | 33.0 % ✗ | 46.7 % ✗ | 33.3 % ✗ |
| dropped: hard fail correct |  | 1 | 1 | 1 |
| dropped: hard fail unambiguous |  | 2 | 2 | 2 |
| dropped: hard fail no_giveaway |  | 6 | 5 | 0 |
| dropped: overlap |  | 21 | 33 | 24 |
| dropped: duplicate |  | 1 | 1 | 2 |
| dropped: fact-check wrong |  | 1 | 1 | 0 |
| merged |  | 63 | 49 | 58 |
| approved |  | 50 | 46 | 49 |
| needs_work |  | 13 | 3 | 9 |
| needs_work rate | ≤ 20.0 % | 20.6 % ✗ | 6.1 % ✓ | 15.5 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 4.8 % ✓ | 2.0 % ✓ | 13.8 % ✗ |
| needs_work: fact | ≤ 10.0 % | 3.2 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 7.9 % ✗ | 2.0 % ✗ | 0.0 % ✓ |
| needs_work: media | ≤ 10.0 % | 11.1 % ✗ | 4.1 % ✓ | 8.6 % ✓ |
| media: no pick in review 1 |  | 2 | 0 | 1 |
| media: recovered by research |  | 0 | 0 | 0 |
| media: no pick at record |  | 63 | 49 | 58 |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 1.6 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| problems guessed |  | no | no | no |
| overlap rate | ≤ 20.0 % | 28.7 % ✗ | 38.0 % ✗ | 29.9 % ✗ |
| merged/slots 11–15 | ≥ 55.0 % | n/a | n/a | n/a |
| max final−target gap 11–15 | ≤ 1.50 | n/a | n/a | n/a |
| approved 11–15 |  | 30 | 23 | 26 |
| top move | ≤ 25.0 % | n/a | n/a | n/a |
| values move |  | n/a | n/a | n/a |
| top stimulus |  | n/a | n/a | n/a |
| values stimulus |  | n/a | n/a | n/a |
| top clue | ≤ 60.0 % | n/a | n/a | n/a |
| values clue |  | n/a | n/a | n/a |
| top answer_kind | ≤ 40.0 % | n/a | n/a | n/a |
| values answer_kind |  | n/a | n/a | n/a |
| top lens | ≤ 25.0 % | n/a | n/a | n/a |
| values lens |  | n/a | n/a | n/a |
| giveaway-step drop rate |  | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| mechanical-check rate |  | 3.2 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| media share | 15.0 %–50.0 % | n/a | n/a | n/a |
| mean fun | ≥ 3.40 | 3.38 ✗ | 3.45 ✓ | 3.52 ✓ |
| cost $ |  | $92.45 | $73.99 | $67.05 |
| $ per approved | ≤ $0.35 | $1.85 ✗ | $1.61 ✗ | $1.37 ✗ |
| calls |  | 1005 | 828 | 725 |
| calls per approved |  | 20.10 | 18.00 | 14.80 |
| wall time h |  | 2.51 | 1.76 | 1.89 |
| days |  | 1 | 2 | n/a |
| **health** | | ✗ fail | ✗ fail | ✗ fail |

Deficit to the targets: none.

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 2 of 49 (4 %)
- Major among review needs work: 3 of 9 (33 %)
- Problems by kind: giveaway 15 (3 major), fact 1 (0 major), ambiguity 1 (1 major), media 7 (4 major), difficulty 2 (1 major), style 1 (0 major)
- Mean |audit − final difficulty|: 0.9; ≥ 3 on 2 of 58 (3 %)
- Audit/review agreement (both accept or both not): 50 of 58 (86 %)
- Sample: 58 audited of 58; 58 Claude calls, about $4.04

Major findings on approved questions:

- **q-21135**: media, ambiguity — I couldn't open the frame sheet or the spectrogram because I have no file-reading tool here, so I couldn't confirm what actually burns in the 72–102 s window. The OCR reads “# SE” at frame 8 (94.5 s), which suggests a sharp-like shape (one of the wrong options), or other symbols, may show in the window. If so, the answer “two beamed eighth notes” is unverified and a second option may be defensible. The Commons description (“Fire Writing”) only confirms the saltpeter fire-writing method, not which symbol is drawn. The low loudness (-47.6 LUFS) doesn't matter for a silent visual question, and the “writing” title-word flag is false because it doesn't give the answer away. Someone with access to sheet.png should check that only the beamed-note shape appears, and that it is finished by the end of the window. (http://127.0.0.1:8001/review/q-21135)
- **q-21150**: giveaway, difficulty — This is a sung recording (the file name says "CANTATO" and the transcript says singing). The first line of the anthem is “Fratelli d'Italia, l'Italia s'è desta”, so the answer's name is sung several times in the first seconds of the 0–60 s window. That gives the answer away and makes the question much easier than 8. Hint 1 even tells players to listen to the language. The facts check out: Mameli was 20 in 1847, the song is known as “Mameli's Hymn”, and Italy was unified in 1861. I could not open the spectrogram because I had no file-reading tool, so I did not check sound quality. (http://127.0.0.1:8001/review/q-21150)

## Media-first funnel

### Per seed

| seed | files | worth | designed | passed | merged | approved |
|---|---|---|---|---|---|---|
| cat:Audio files of Aves | 30 | 9 | 9 | 8 | 5 | 3 |
| cat:Audio files of national anthems | 30 | 4 | 4 | 4 | 2 | 2 |
| cat:Videos by NASA | 21 | 7 | 7 | 5 | 4 | 3 |
| cat:Videos of animals | 30 | 5 | 5 | 5 | 3 | 3 |
| cat:Videos of nature | 30 | 12 | 12 | 11 | 7 | 7 |
| q:audio:national anthem instrumental | 23 | 8 | 8 | 8 | 8 | 6 |
| q:audio:piano recording | 30 | 13 | 13 | 10 | 4 | 3 |
| q:video:NASA video launch | 6 | 0 | 0 | 0 | 0 | 0 |
| q:video:cooking video | 30 | 2 | 2 | 2 | 0 | 0 |
| q:video:experiment science video | 30 | 12 | 12 | 11 | 8 | 8 |
| q:video:machine working video | 30 | 0 | 0 | 0 | 0 | 0 |
| q:video:space station astronaut video | 24 | 2 | 2 | 2 | 1 | 0 |
| q:video:time-lapse video | 28 | 12 | 12 | 12 | 9 | 9 |
| q:video:traditional dance video | 30 | 5 | 5 | 5 | 4 | 2 |
| q:video:train video | 30 | 4 | 4 | 4 | 3 | 3 |
| q:video:volcano eruption video | 30 | 0 | 0 | 0 | 0 | 0 |
| total | 432 | 95 | 95 | 87 | 58 | 49 |

### Per class

| class | files | worth | designed | passed | merged | approved |
|---|---|---|---|---|---|---|
| general | 379 | 83 | 83 | 75 | 48 | 41 |
| pd-music | 53 | 12 | 12 | 12 | 10 | 8 |
| total | 432 | 95 | 95 | 87 | 58 | 49 |

- $ per approved: $1.45

## Needs work

- **q-21137** (famous-landmarks) Watch: on which Greek island is this old Venetian harbor? → Crete: Hint 2 (“It is the largest Greek island”) gives the answer away: at difficulty 13, almost every player knows that is Crete, so the clip and hint 3 are no longer needed. Replace it with a mid-strength hint that still leaves the video to decide. For example, say that the harbor's long stone breakwater ends at a lighthouse, or that the arched buildings on the quay were once Venetian shipyards.
- **q-21138** (stars-and-galaxies) Watch: the bright star labeled in this view of the Milky Way marks the tail of which constellation? → Cygnus: The 0–5 s window gives the answer away. From frame 6 (2.75 s) onward, a second label reads “Gamma Cygni”, and “Cygni” names Cygnus outright. The media note says the window ends before that label appears, but that's wrong. Because two stars are labeled, “the bright star labeled” is also unclear. The fix is to cut the excerpt to about 0–2.5 s (only the Deneb label), or to drop the question. The text can't fix this because the file is kept.
- **q-21151** (robots) Watch: where was this ball-shaped robot helper built to work? → On a space station: The 41–48.5 s window doesn't match the note. Its last frame (48.12 s) already shows the caption "CIMON will become the latest crewmember on the International Space Station ISS…", which names the answer. There is no Earth-from-orbit shot in the window, so hint 2 is false for the clip. Frames 1–9 show Alexander Gerst in a polo shirt handling CIMON on a stand in a module mock-up: nothing floats and nothing shows space, so a lab or submarine can't be ruled out from the clip itself. The excerpt needs to be re-cut so it ends before about 48 s and includes an actual orbit or weightless shot. Otherwise the question can't be answered from the window.
- **q-21158** (countries) Listen: this tune is the national anthem of a small European country. Which one? → Liechtenstein: Hint 1 gives the answer away. “Tiny alpine principality ruled by a prince” fits only Liechtenstein among the options: San Marino is a republic, Andorra is in the Pyrenees, and Monaco is on the coast. So anyone who knows basic European geography can answer without the clip. Hint 1 should be vague, for example about the country being one of Europe's smallest or doubly landlocked without naming its region, or about the anthem's lyrics praising a river.
- **q-21160** (celebrations-around-the-world) Watch: which Japanese festival is being celebrated with this night of drumming and dancing? → Obon: The played window (31–59 s) ends on about 11 seconds of a dark, red-lit haunted house: frames 7–10 show a No-Face mask and a close-up oni demon mask. That clashes with "nothing scary" for a family TV game, and it doesn't show the "night of drumming and dancing" the question describes. Trim the excerpt to roughly 31–48 s (taiko drummers, children dancing with fans, the yukata crowd dance). That window carries the answer, and the text can stay as it is.
- **q-21168** (countries) Listen: this national anthem, called “La Concorde”, belongs to which country on the equator in Central Africa? → Gabon: The question is answered entirely by its text, not the clip: the anthem title “La Concorde” is the only real clue, and almost no player can tell Gabon's anthem from Cameroon's, Congo's or the Central African Republic's by ear. The text-only check fails, and with the title removed the clip can't decide. Hint 2 also settles it, because the other three capitals (Yaoundé, Brazzaville, Bangui) are all inland. “On the equator” also fits the Republic of the Congo.
- **q-21177** (birds) Listen: this small European songbird fills its song with copies of dozens of other birds, many learned in Africa. Which bird is it? → Marsh warbler: The 60-second clip can't decide the question: only expert birders can tell a marsh warbler from a sedge warbler, nightingale or blackcap by ear. Players who can answer at all do it from the text clue alone (dozens of copied songs, many learned in Africa, which is the marsh warbler's famous trait), so the clip adds nothing. Moving that clue into the clip would leave an ear test only experts pass. I can't see a fair question this window could carry with these options, so I'm leaving the fix empty.
- **q-21187** (birds) Listen: which bird of prey is making these thin, yelping whistles? → Golden eagle: Hint 2 gives the answer away. Most adults know Germany's national symbol is an eagle (the Bundesadler), and Golden eagle is the only eagle among the four options. Replace hint 2 with a vaguer clue that doesn't point to "eagle", for example about its size or its huge hunting range, and keep the Mexico flag as hint 3.
- **q-21188** (childrens-songs) Listen: which toy famously plays this tune when you turn its handle? → A jack-in-the-box: Players can answer from the text alone, so the clip isn't needed: "a toy that plays a tune when you turn its handle" fits only the jack-in-the-box among the four options. A rocking horse, a yo-yo and a kaleidoscope have no crank and play no music. The question should make the tune decide the answer. For example, all four options could be wind-up or crank music toys (music box, toy carousel, jack-in-the-box, musical spinning top), with the clue being the tune's sudden "pop" ending rather than the handle. Or the text could ask about something else that the 12-second toy-piano recording carries.

## Question axes

- move: None 58
- stimulus: None 58
- clue: None 58
- answer_kind: None 58
- lens: None 58

## Dropped by the pipeline

- mf-01ff4a33b8: overlap like q-2536: Before it is born, a human baby grows inside its mother for about how many months? → 9: Watch: the bicycle pump is just a joke. In real life, about how long does the change you see in this video take? → About 9 months
- mf-18ef1d0be1: overlap like q-20852: Watch the red locomotive's roof: what is the folding arm that touches the overhead wires called? → Pantograph: Watch: what is the name of the device these trains use to collect the power that moves them? → A pantograph
- mf-2225337909: overlap like q-20765: Listen: which composer wrote this stormy piano piece? → Frédéric Chopin: Listen: which composer wrote this piano piece? → Frédéric Chopin
- mf-290857f226: overlap like q-8729: This root is orange, crunchy, and cartoon rabbits love to munch it. What vegetable is it? → Carrot: Watch: which vegetable is being tossed in a bowl and baked in the oven here? → Carrot
- mf-2ec5bdcf70: overlap like q-0487: Escucha: ¿qué instrumento suena? → La gaita escocesa: Watch and listen: which instrument is this astronaut playing? → Bagpipes
- mf-30dc00890a: overlap like q-20130: Which small black-and-white bird is often seen darting across British car parks, chasing flies? → Pied wagtail: Watch: which small gray, black and white bird is this, hunting insects on the ground? → A white wagtail
- mf-32b5811dc0: overlap like q-9011: You're hiking in a national park and see rangers starting a fire on purpose. What is this planned fire mainly meant to burn away? → Dead wood and brush that feed big wildfires: Watch: firefighters walk calmly beside these flames on dry grassland. What kind of fire is this? → A prescribed burn
- mf-4a51138869: duplicate like q-21047: Watch: going by the logo on its carriages, in which country is this double-decker train running? → Russia: Watch: these tigers are being released back into the wild. In which country is this happening? → Russia
- mf-4af48d1b66: overlap like q-20640: Listen: this lively symphony finale weaves several tunes together at the same time. Who composed it? → Wolfgang Amadeus Mozart: Listen: which composer wrote this lively concerto for two pianos and orchestra? → Wolfgang Amadeus Mozart
- mf-52717e6a90: overlap like q-9489: Listen: which bird makes this sound in British woods at night? → An owl: Listen: which owl makes this call at night? → Tawny owl
- mf-5f31f18637: overlap like q-0191: Mira de cerca: ¿de qué reptil es este ojo? → El camaleón: Watch: what kind of animal is walking across this big leaf? → A chameleon
- mf-61ee55e0b3: overlap like q-9327: Ich war ein Wunderkind aus Hamburg, holte 1829 Bachs Matthäus-Passion zurück auf die Bühne und schrieb einen berühmten Hochzeitsmarsch. Wer bin ich? → Felix Mendelssohn Bartholdy: Listen: which composer wrote this piano concerto? → Felix Mendelssohn
- mf-6bfe87d795: overlap like mf-52717e6a90: Listen: which owl makes this call at night? → Tawny owl: Listen: at what time of day would you most likely hear this bird calling in the forest? → In the middle of the night
- mf-70d66f0afd: overlap like q-20934: Listen: which country has this as its national anthem? → France: Listen: this Russian revolutionary song of 1917 borrowed its tune from which country's national anthem? → France
- mf-96a22a5163: overlap like q-20705: Listen: this melody is the national anthem of two neighboring countries. Which two? → Finland and Estonia: Listen: which country has this tune as its national anthem? → Finland
- mf-97306592cf: overlap like q-4289: You're reading fables where a slow tortoise beats a hare and a fox calls some grapes sour. Which ancient Greek storyteller are they credited to? → Aesop: Watch: the crow is acting out a famous animal fable. Which storyteller is credited with that fable? → Aesop
- mf-9e40547543: duplicate like q-20768: Listen: this orchestral piece opens with a bright trumpet fanfare. Which composer wrote it? → Pyotr Ilyich Tchaikovsky: Listen: which composer wrote this waltz? → Pyotr Ilyich Tchaikovsky
- mf-9fb445c404: overlap like q-4777: This heron holds its long neck bent in an S shape. What does the S help it do? → Strike at fish very fast: Watch: what kind of bird is walking along this shore? → A heron
- mf-bec77cb4fc: overlap like q-0986: Mira de cerca este animal acuático. ¿A qué grupo de animales pertenece? → Mamíferos: Watch: the animal swimming in this clip belongs to which group of animals? → Mammals
- mf-c625bc5891: overlap like q-8736: Listen: which bird makes this sound? → Pigeon: Listen: which bird is making these sounds? → A pigeon
- mf-c7432074b0: overlap like q-21066: Listen: this is the opening of a work by Felix Mendelssohn. What kind of piece is it? → A piano concerto: Listen: what kind of piece is this? → A piano concerto
- mf-cfe92e2c43: overlap like q-9974: Mira la foto: este bosque de la sierra norte de Madrid es Patrimonio de la Humanidad. ¿De qué árboles es? → De hayas: Watch: which kind of tree makes up this forest? → Beech
- mf-dcd73d6e32: overlap like q-20140: This big bird of prey nests in the Scottish Highlands, dives feet first into lochs to catch fish, and flies to Africa for winter. What is it? → An osprey: Watch: which bird of prey is raising its family in this huge stick nest on top of a floodlight pole? → An osprey
- mf-ec9547a9a6: overlap like q-20820: Listen: from which era of Western music does this solo piano piece come? → Classical era: Listen: from which era of Western music does this piece come? → The Classical era
- mf-ef5c287f8f: overlap like q-20981: Watch: the white dots show carbon dioxide in the air. What makes them thin out over the north, then come back, every year? → Plants soaking it up as they grow: Watch the northern lands from spring into summer (red = more carbon dioxide, blue = less). What causes the change you see? → Plants take it in as they grow
- mf-fd2195bb84: overlap like q-21078: Watch: this giant steel rocket, filmed from a NASA research plane, was built by which company? → SpaceX: Watch: a robotic arm on the space station catches this cargo capsule. Which company built the capsule? → SpaceX
- mf-c275289e6f: hard fail: correct 4, unambiguous 3, no_giveaway 4, no_overlap 5: Watch: this sheet of paper looked blank. What makes the colored letters appear on it? → A chemical reaction with the ink
- mf-d7ce71e7ff: hard fail: correct 5, unambiguous 3, no_giveaway 4, no_overlap 4: Watch: which vegetable is the cook getting ready to cut? → Zucchini
- mf-fd86274735: hard fail: correct 3, unambiguous 4, no_giveaway 4, no_overlap 4: Watch: which instrument is this street musician playing? → Kora
