# batch-83

Made by `qgen batch --media-first` on 2026-11-17 (plans/19-repo-layout.md, D-36). Generated file: don't edit by hand.

- Bundle: base
- Language: English
- Subcategories (0): 
- Merged: 69 (q-20952…q-21020)
- Approved: 50
- Needs work: 19
- Dropped by the pipeline: 34
- Reviewed by: claude-opus-5-5
- Claude calls: 961, about $86.13 at list price; $1.72 per approved
- Picked files not cached yet: 0

## Health

Batch health (plan 15): this batch and the two before it (batch-81, batch-82; across the source-locale switch too, decision 233), ✓/✗ against the thresholds in `authoring/data/targets.json`; a ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look. Needs-work counts are `record`'s decisions; `problems guessed` = classified from feedback.

| metric | threshold | batch-81 | batch-82 | batch-83 |
|---|---|---:|---:|---:|
| source locale |  | en | en | en |
| mode |  | media-first | media-first | media-first |
| drafts |  | 106 | 100 | 103 |
| skipped slots |  | 0 | 0 | 0 |
| dropped |  | 32 | 36 | 34 |
| drop rate | ≤ 20.0 % | 30.2 % ✗ | 36.0 % ✗ | 33.0 % ✗ |
| dropped: hard fail correct |  | 0 | 1 | 0 |
| dropped: hard fail unambiguous |  | 1 | 3 | 2 |
| dropped: hard fail no_giveaway |  | 4 | 9 | 4 |
| dropped: overlap |  | 27 | 24 | 26 |
| dropped: duplicate |  | 0 | 0 | 2 |
| dropped: fact-check wrong |  | 0 | 0 | 0 |
| merged |  | 74 | 64 | 69 |
| approved |  | 59 | 48 | 50 |
| needs_work |  | 15 | 16 | 19 |
| needs_work rate | ≤ 20.0 % | 20.3 % ✗ | 25.0 % ✗ | 27.5 % ✗ |
| needs_work: giveaway | ≤ 10.0 % | 9.5 % ✓ | 7.8 % ✓ | 14.5 % ✗ |
| needs_work: fact | ≤ 10.0 % | 2.7 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 1.6 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.0 % ✓ | 4.7 % ✗ | 2.9 % ✗ |
| needs_work: media | ≤ 10.0 % | 13.5 % ✗ | 15.6 % ✗ | 20.3 % ✗ |
| media: no pick in review 1 |  | 1 | 1 | 1 |
| media: recovered by research |  | 0 | 0 | 0 |
| media: no pick at record |  | 74 | 64 | 69 |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 3.1 % ✓ | 2.9 % ✓ |
| needs_work: style | ≤ 10.0 % | 1.4 % ✓ | 6.2 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| problems guessed |  | no | no | no |
| overlap rate | ≤ 20.0 % | 25.5 % ✗ | 27.0 % ✗ | 29.1 % ✗ |
| merged/slots 11–15 | ≥ 55.0 % | n/a | n/a | n/a |
| max final−target gap 11–15 | ≤ 1.50 | n/a | n/a | n/a |
| approved 11–15 |  | 39 | 32 | 35 |
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
| mechanical-check rate |  | 4.1 % ✓ | 0.0 % ✓ | 4.3 % ✓ |
| media share | 15.0 %–50.0 % | n/a | n/a | n/a |
| mean fun | ≥ 3.40 | 3.36 ✗ | 3.47 ✓ | 3.50 ✓ |
| cost $ |  | $83.50 | $84.36 | $81.95 |
| $ per approved | ≤ $0.35 | $1.42 ✗ | $1.76 ✗ | $1.64 ✗ |
| calls |  | 936 | 925 | 901 |
| calls per approved |  | 15.86 | 19.27 | 18.02 |
| wall time h |  | 2.66 | 1.78 | 1.41 |
| days |  | 1 | 1 | n/a |
| **health** | | ✗ fail | ✗ fail | ✗ fail |

Deficit to the targets: none.

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 2 of 43 (5 %)
- Major among review needs work: 12 of 17 (71 %)
- Problems by kind: giveaway 14 (7 major), fact 4 (2 major), overlap 1 (1 major), media 16 (14 major), difficulty 6 (4 major)
- Mean |audit − final difficulty|: 0.8; ≥ 3 on 2 of 60 (3 %)
- Audit/review agreement (both accept or both not): 53 of 60 (88 %)
- Sample: 60 audited of 60; 60 Claude calls, about $4.18

Major findings on approved questions:

- **q-20968**: media, fact, giveaway — NASA's AWE posts (science.nasa.gov blog, Nov 27, 2023; SVS 14494) say Canadarm2 pulled AWE out of the Dragon and installed it on ELC-1, and they never mention Dextre. Only pre-launch, Wikipedia-based pages name Dextre. So the 40–70 s window may show only Canadarm2, which is one of the wrong options, and that would make "this robot" point to the wrong answer. I couldn't open the frame sheet to check. Also, the text alone describes Dextre ("headless torso with two long arms"), so the clip isn't needed to answer. (http://127.0.0.1:8001/review/q-20968)
- **q-21018**: media, giveaway — The facts hold up: the GDR was founded in 1949 and ended in October 1990, less than a year after the Wall fell, and the anthem was played without words because of “Deutschland, einig Vaterland”. The licence is the major problem (check 4). Hanns Eisler died in 1962 and the lyricist Becher in 1958, so the 70-year rule doesn't make the composition public domain until about 2033. The `basis` itself says the official-work claim needs double-checking, and the uploader's CC BY 4.0 only covers the recording, not the song. Smaller points: hint 1 (“founded in 1949”) fits only East Germany among the four options, a minor giveaway. I couldn't open the spectrogram because no file-reading tool was available; the loudness numbers (−16.1 LUFS, about 10% silence) look fine. (http://127.0.0.1:8001/review/q-21018)

## Media-first funnel

### Per seed

| seed | files | worth | designed | passed | merged | approved |
|---|---|---|---|---|---|---|
| cat:Audio files of Aves | 30 | 0 | 0 | 0 | 0 | 0 |
| cat:Audio files of national anthems | 30 | 4 | 4 | 4 | 3 | 3 |
| cat:Videos by NASA | 30 | 7 | 7 | 6 | 6 | 6 |
| cat:Videos of animals | 30 | 8 | 8 | 8 | 6 | 5 |
| q:audio:musical instrument sample | 1 | 0 | 0 | 0 | 0 | 0 |
| q:audio:national anthem instrumental | 30 | 16 | 16 | 16 | 12 | 6 |
| q:audio:piano recording | 30 | 11 | 11 | 8 | 3 | 2 |
| q:audio:piano sonata public domain | 30 | 17 | 17 | 6 | 2 | 1 |
| q:audio:traditional folk instrument | 6 | 4 | 4 | 4 | 4 | 4 |
| q:video:NASA video launch | 30 | 0 | 0 | 0 | 0 | 0 |
| q:video:aircraft takeoff video | 1 | 1 | 1 | 1 | 1 | 1 |
| q:video:animal video wildlife | 30 | 7 | 7 | 7 | 6 | 5 |
| q:video:cooking video | 30 | 4 | 4 | 4 | 3 | 3 |
| q:video:experiment science video | 30 | 6 | 6 | 6 | 4 | 4 |
| q:video:machine working video | 30 | 9 | 9 | 8 | 5 | 3 |
| q:video:newsreel | 16 | 6 | 6 | 4 | 2 | 0 |
| q:video:rover mars video | 30 | 2 | 2 | 2 | 2 | 2 |
| q:video:space station astronaut video | 30 | 2 | 2 | 2 | 1 | 1 |
| q:video:sport video match | 15 | 0 | 0 | 0 | 0 | 0 |
| q:video:time-lapse video | 30 | 8 | 8 | 8 | 4 | 2 |
| q:video:traditional dance video | 30 | 7 | 7 | 7 | 5 | 2 |
| q:video:train video | 30 | 2 | 2 | 2 | 0 | 0 |
| total | 549 | 121 | 121 | 103 | 69 | 50 |

### Per class

| class | files | worth | designed | passed | merged | approved |
|---|---|---|---|---|---|---|
| general | 443 | 78 | 78 | 73 | 50 | 40 |
| pd-film | 16 | 6 | 6 | 4 | 2 | 0 |
| pd-music | 90 | 37 | 37 | 26 | 17 | 10 |
| total | 549 | 121 | 121 | 103 | 69 | 50 |

- $ per approved: $1.72

## Needs work

- **q-20954** (birds) Watch: which bird is perched on this branch? → A ptarmigan: The question text is fine, but the file has a licensing problem. Its Commons description says the soundtrack is “Full Of It” by half cocked, licensed CC BY-NC-NoDerivatives 4.0. That non-commercial, no-derivatives music conflicts with the file's FAL licence and isn't safe to play in the game. Use the video without its audio track, or use a different ptarmigan file.
- **q-20956** (countries) Listen: this is the national anthem of which country? → Bahrain: Almost no listener can tell Bahrain's instrumental anthem apart from those of Qatar, Kuwait and the UAE, so the clip doesn't decide the question. Only the hints (Manama, the causeway) make it answerable, which fails media-first check 1. Separately, the description ("a country you could almost cross before your coffee goes cold") rules out the large UAE. I can't see a different question about this window that players could answer by ear, so a text fix won't save it.
- **q-20959** (countries) Listen: this is the national anthem of which tiny European country? → Monaco: Almost no player can tell Monaco's anthem apart from San Marino's or Andorra's by ear: an instrumental band march gives no audible clue that points to Monaco, so the clip doesn't decide the question and only the hints (prince, F1 race) answer it. The file doesn't suit an ear-test question. Unless the game wants pure anthem-recognition questions for specialists, drop this question or rebuild it around something the window actually lets players hear.
- **q-20962** (classical-music) Listen: what musical form is this lively piano movement written in? → Rondo: The description gives the answer away. “A tune that leaves the party, wanders off, and somehow always comes back” describes exactly what defines a rondo: the main tune keeps returning between contrasting sections. With only the four options, that points straight to Rondo before any listening. Rewrite it to play on the party or finale mood without describing the returning tune.
- **q-20964** (inventions) Watch: in this old steam engine, what is the huge, heavy wheel that keeps it turning smoothly called? → A flywheel: The text answers the question without the clip: "keeps it turning smoothly" is the flywheel's defining job, and "steam engine" already rules out the waterwheel and paddle wheel. The question should ask about the wheel as it is seen, e.g. "Watch: what is the huge red-rimmed wheel on this old mill engine called?", and leave out its function. Hint 3 (toy cars you push and let go use a small one) is the same fact that q-0779 asks, so seeing this question gives that one away. Replace hint 3 with another use, such as potter's wheels or early car engines.
- **q-20966** (countries) Listen: this national anthem, adopted in 1996, belongs to a country that was once a Portuguese colony. Which one? → Cape Verde: No player, experts included, can tell Cape Verde's anthem apart from those of Guinea-Bissau, Mozambique or São Tomé and Príncipe by ear. The answer comes only from the text clues ("adopted 1996", former Portuguese colony) and the hints, so the clip doesn't decide anything. I can't think of another fair question about this window: it's 60 seconds of a generic brass-band anthem with no singing or features players could pick out.
- **q-20969** (fish) Watch: this fish keeps returning to its pile of gravel and turns to face the camera. Why? → It is guarding its eggs and babies: Hint 1 ("This happens every spring, and in this fish it is usually the male's job") gives the answer away: a seasonal job done by the male can only be breeding care, which rules out hiding, feeding and resting straight away. Hint 2 (spring and a gravel pile that "isn't there by chance") also points straight at a nest. Hint 1 should stay vague, for example about the fish's behavior or its shallow-water home, and hints 2 and 3 can then bring in the season and the parenting.
- **q-20970** (classical-music) Listen: this violin melody is best known as a song. What is the song called? → “Ave Maria”: The picked picture has an unsuitable licence (pd-us-only: PD-US-extracted-audio, PD-US-not renewed).
- **q-20972** (countries) Listen: this is the national anthem of which island country in the Indian Ocean? → Mauritius: Almost nobody can recognise Mauritius's anthem by ear or tell it apart from the anthems of the Seychelles, Madagascar or the Maldives. The clip does nothing, so players can only guess or wait for the hints (the dodo hint, and hint 2 naming Port Louis, basically answer it). No other question about this 59-second brass-band window would work for players: "which kind of music is this" is too vague, and the composer is unknown. So the file doesn't fit this question.
- **q-20983** (natural-phenomena) Watch: what is happening to the Sun in this time-lapse video? → A solar eclipse: The first two frames (about 0–6 s) show a big “Ring of Fire 2021” title card over the Sun. “Ring of Fire” is the common name for an annular solar eclipse, so it names the answer on screen. Move the excerpt start past the title card (for example 6–36 s, where frames 3–10 show only the eclipsed Sun). The text itself is fine.
- **q-20984** (countries) Listen: this anthem was dropped in 1969 and brought back in 2011, when its country's ruler of 42 years fell. Which country is it? → Libya: The text answers the question without the clip: "ruler of 42 years who fell in 2011" is Gaddafi, so adults answer Libya from the text alone (the rater says so too), and the anthem plays no part. If that clue is cut, the question becomes an ear test: almost no player can tell the Libyan anthem from the Tunisian, Egyptian or Algerian one. No other question about this brass-band window would work, so the file doesn't suit a media-first question.
- **q-20986** (countries) Listen: this brass band is playing the national anthem of which country? → Papua New Guinea: Players, trivia specialists included, can't tell Papua New Guinea's anthem apart from those of Fiji, the Solomon Islands or Samoa by ear. The clip decides nothing, and the question is answered only through the hints (the rater notes say the same). No other question about this 50-second instrumental brass excerpt would work: asking which kind of piece it is would not hold up, because many anthems are marches. So the file doesn't fit a fair question.
- **q-20993** (space) Watch: what is this bright streak that flashes across the night sky for a moment? → A meteor: This asks the same thing as approved q-3974 (“People call a streak of light like this a ‘shooting star’. What is it really?” → a small space rock burning up in the air). Both show a meteor streak and ask what it is. This question's hint 2 even states q-3974's answer word for word, so either question gives the other away.
- **q-21001** (celebrations-around-the-world) Watch and listen: masked dancers in big feathered headdresses leap to this live band. In which country is this traditional dance at home? → Peru: The file is a video stored as .ogg ("File:Cusco, danse Tobas (Peru).ogg"). The hard mechanical check is right: the game treats it as audio and can't play the video. The question depends on seeing the headdresses and ponchos, so it doesn't work as sound alone. It needs a playable video version of this footage (for example a .webm transcode) or a different file. The text itself is fine. A video file named .ogg ships as audio; the game can't play it.
- **q-21004** (history) Watch: what kind of horse racing is this? → Flat racing: The licence basis ("Universal released its 1929–1967 newsreels into the public domain in 1976") is not one of the accepted public-domain bases (creator dead 70+ years, film before 1930, government work, traditional), so the hard work-basis check fails. Commons accepts this release, but the file isn't eligible under the media-first licence rule. Either the rule gets an explicit exception for Universal Newsreels, or the question needs different footage, such as a pre-1930 or government-made film of a flat race. Media.work basis “Universal released its 1929–1967 newsreels into the public domain in 1976” is none of: died-70-years, pre-1930-film, government-work, traditional.
- **q-21011** (planes) Watch: in 1937, these warships joined the biggest air and sea search of its time. Whose missing plane were they looking for? → Amelia Earhart: The file fails the licence check: a 1937 British Pathé newsreel fits none of the allowed public-domain bases (creator dead 70+ years, film before 1930, government work, traditional). Commons tags it only as PD-UK and PD-1996 with an unknown author, and the code flags this as hard. The clip also adds nothing to the answer. The 50–77 s window shows only a battleship, the carrier Lexington and biplanes, and the text alone ("1937", "missing plane", "biggest search") answers it for players at difficulty 9. So the essential video isn't needed (check 1). Media.work basis “newsreel film of 1937, marked public domain on Wikimedia Commons (class pd-film)” is none of: died-70-years, pre-1930-film, government-work, traditional.
- **q-21012** (science) Which water turbine has propeller blades that change their angle, ideal for rivers with lots of water but only a small drop? → Kaplan turbine: The question can be answered from the text alone: the clue (blades that change their angle, lots of water but a small drop) defines the Kaplan turbine, so the essential clip adds nothing. The clip can't carry the question either. It is a generic TVA cutaway in which the runner is never clearly shown to be a Kaplan rather than a Francis, and it has burned-in Spanish subtitles ("la turbina a su vez hace girar a un alternador", "alternador") in an English question. The only other question this window could support (what the turbine drives) repeats q-2994.
- **q-21015** (celebrations-around-the-world) Watch: dances like this, with cowhide shields, high kicks and stamping, are famous among which people of South Africa? → Zulu: The question text answers itself without the clip. "Of South Africa" rules out Maasai (Kenya/Tanzania) and Yoruba (Nigeria), and the text's own "cowhide shields, high kicks and stamping" points to the Zulu over the Xhosa. Players at difficulty 10 can answer without watching. Drop "of South Africa" and the description of the dance from the question so the clip decides, and swap Maasai or Yoruba for another Southern African people (for example Swazi or Sotho). Also, the Commons description says only "South Africa Traditional Dance by WikimediaZA" and never says Zulu, so "Zulu" rests only on the costumes and setting. These look clearly Zulu (cowtail leg bands, isihlangu-style shields, KwaZulu-Natal-like hills), but a source should confirm it.
- **q-21020** (traditional-dress) Watch: these dancers parade behind their region’s black-and-white striped flag. Which Celtic region is it? → Brittany: The video gives the answer away. A vertical "BREST" banner is visible on the lamppost in almost every frame, and frame 2 has a large "Brest 200°" sign on a tent. French signs ("BAR Les NATIONS") also show it's France, and Brittany is the only French option. Anyone who knows Brest is in Brittany, or just sees the French text, can answer without the flag or the costumes. The file and excerpt can't be changed, so this clip doesn't work for a "which region" question.

## Question axes

- move: None 69
- stimulus: None 69
- clue: None 69
- answer_kind: None 69
- lens: None 69

## Dropped by the pipeline

- mf-0974132e21: overlap like q-20640: Listen: this lively symphony finale weaves several tunes together at the same time. Who composed it? → Wolfgang Amadeus Mozart: Listen: which composer wrote this slow movement from a piano concerto? → Wolfgang Amadeus Mozart
- mf-0d975407d4: overlap like q-17599: Scott Joplin, who wrote “The Entertainer,” is the most famous composer of which piano style, and was called its “King”? → Ragtime: Listen: which style of piano music is this? → Ragtime
- mf-19ce339e5c: overlap like q-20906: Listen: in which language is this choir singing its country's national anthem? → Portuguese: Listen: which country’s national anthem is this choir singing? → Brazil
- mf-1dc30eb854: overlap like q-2790: I'm a pot of water on top of Mount Everest, and I boil at only about 70 °C (158 °F). Why? → The air pressure is lower: Watch the two pots: compared with water at sea level, at what temperature does water boil high up on a mountain? → A lower temperature
- mf-23409a4457: overlap like q-20860: Listen to this choir from a Mass by Mozart. Which musical form is it singing? → Fugue: Listen to how this piano piece begins and builds. What kind of piece is it? → Fugue
- mf-259e16f2b0: overlap like q-20805: Listen: from which era of Western classical music does this piano piece come? → The Romantic era: Listen: from which era of Western classical music does this piece for piano and orchestra come? → Romantic era
- mf-2e2b562b1d: overlap like q-1506: Fui el primer ser humano en viajar al espacio y desde allá dije: «La Tierra es azul». ¿Quién soy? → Yuri Gagarin: Watch: who is the hero that this huge crowd in Moscow is celebrating? → Yuri Gagarin
- mf-3f4f5d9d0f: overlap like q-2309: This bridge, guarded by dragon statues, stands in which European capital? → Ljubljana: Watch: this green dragon guards a famous bridge in which European capital city? → Ljubljana
- mf-4067fa4df5: overlap like q-13481: Escucha: ¿qué animal de México hace este sonido? → El coyote: Watch: which wild animal comes to drink at this water bowl in the Arizona desert, just after sunset? → Coyote
- mf-5a877a9f24: overlap like q-1187: Un clip que flota en el agua, un insecto que camina sobre un charco y colorante que huye del jabón en la leche: ¿qué tienen en común? → Son efectos de la tensión superficial: Watch: on the space station, this floating water holds its round shape. Which force gives it that shape? → Surface tension
- mf-6c415b24c2: overlap like q-1544: Este gorro plano de lana se asocia tradicionalmente con un pueblo europeo. ¿Con cuál? → Los vascos: Watch: dancers dressed in white with red berets and red sashes kick high. A traditional dance of which European people? → The Basques
- mf-7511c6b654: overlap like q-17700: Mira esta foto de cerca. ¿Qué es? → Una tortilla: Watch: which food is this machine making from the big tub of dough? → Tortillas
- mf-76dd226921: overlap like mf-7f6bc78a42: Watch how this power plant makes electricity. Which other kind of power plant follows these very same steps? → A nuclear power plant: Watch: in this power plant cutaway, what is blasting through the turbines to make them spin? → Steam
- mf-7f6bc78a42: overlap like mf-76dd226921: Watch: in this power plant cutaway, what is blasting through the turbines to make them spin? → Steam: Watch how this power plant makes electricity. Which other kind of power plant follows these very same steps? → A nuclear power plant
- mf-81824cc48c: overlap like q-20912: Listen: musicians mark the speed of a piece with an Italian word. Which tempo word fits this movement? → Largo: Listen: this is the middle movement of a piano concerto. Which Italian tempo marking describes its pace? → Largo
- mf-94534db60d: overlap like q-20641: Listen: this orchestral movement by Beethoven takes its rhythm from which old court dance? → Minuet: Listen: this graceful piano piece moves in a stately three-beat step. Which old court dance gives it its rhythm? → Minuet
- mf-945641887e: overlap like q-0942: Brillo dentro de cada rayo y de cada estrella, y soy el estado de la materia más abundante del universo visible. ¿Qué soy? → Plasma: Watch: a person bends this glowing spiral inside a glass tube with a magnet. What state of matter is the glowing spiral? → Plasma
- mf-c69cde2714: overlap like q-1022: ¿Qué animal tiene estas dos jorobas? → Camello: Watch: which animal is grazing in this desert? → Dromedary
- mf-c83e8aac10: overlap like q-20961: Watch: which bird is this, perched on a branch? → Bee-eater: Watch: which bird is perched on the branches in this clip? → European bee-eater
- mf-cfee0cf1b2: overlap like q-20724: Listen: what kind of classical piece is this? → A concerto: Listen: what kind of classical work is this music from? → Concerto
- mf-d4ba002342: overlap like q-20890: Watch: which filming technique was used to make this video of a banana? → Time-lapse: Watch: which filming technique turns three years of building work into a few seconds of video? → Time-lapse
- mf-d717cc36d0: overlap like q-20683: Watch: a commuter train heads downtown toward a very tall tower. Which city is this? → Toronto: Watch: this green-and-white double-decker commuter train belongs to the rail network of which city? → Toronto
- mf-dde815acec: overlap like q-8697: MRI scanners and the Large Hadron Collider use superconductors. What happens to their electrical resistance when they get cold enough? → It drops to exactly zero: Watch: the magnet floats above the gray ceramic tile without touching it. Which property of the tile makes this possible? → Superconductivity
- mf-e7f686c01d: overlap like q-20636: Listen to this fast, stormy symphony movement. Who composed it? → Ludwig van Beethoven: Listen: which composer wrote this famous melody? → Ludwig van Beethoven
- mf-f7eec13b13: overlap like q-20820: Listen: from which era of Western music does this solo piano piece come? → Classical era: Listen to this piano opening. In which era of Western music was it written? → Classical era
- mf-fcfae5a420: overlap like q-20784: Listen: which dance is this orchestra playing? → A waltz: Listen: this is the national anthem of a Caribbean island. Unusually for an anthem, it has the rhythm of which dance? → Waltz
- mf-0116030114: duplicate like q-4026: Watch this hamster run. At what time of day do pet hamsters usually run on their wheel the most? → At night: Watch this flower open in fast motion. When does it really open in nature? → At night
- mf-1560e2601f: duplicate like q-20693: Watch: in which country is this festival dance performed? → India: Listen: which country has this tune as its national anthem? → India
- mf-25c8726fc0: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: Listen: Beethoven gave each movement of this piano sonata a title, telling a story about a friend. What does this movement paint? → A joyful reunion
- mf-360a8fd09c: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Listen: this is the national anthem of which country in southern Africa? → Eswatini
- mf-4bc7ae4bba: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Watch: this two-stringed lute, plucked by the player, is a traditional instrument of which country? → Mongolia
- mf-87a9223f1d: hard fail: correct 5, unambiguous 3, no_giveaway 4, no_overlap 5: Watch: in 1939, these Jewish children are flying to safety in Britain. From which country are they leaving? → Czechoslovakia
- mf-c9842c9b9a: hard fail: correct 4, unambiguous 3, no_giveaway 4, no_overlap 5: Watch: a long-distance passenger train rolls past a crowded platform. In which country was this filmed? → Ukraine
- mf-f68c2c691c: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: Watch: what type of forestry machine is this, clearing the brush as it drives? → Forestry mulcher
