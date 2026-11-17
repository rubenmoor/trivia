# batch-82

Made by `qgen batch --media-first` on 2026-11-17 (plans/19-repo-layout.md, D-36). Generated file: don't edit by hand.

- Bundle: base
- Language: English
- Subcategories (0): 
- Merged: 64 (q-20888…q-20951)
- Approved: 48
- Needs work: 16
- Dropped by the pipeline: 36
- Reviewed by: claude-opus-5-5
- Claude calls: 985, about $88.33 at list price; $1.84 per approved
- Picked files not cached yet: 0

## Health

Batch health (plan 15): this batch and the two before it (batch-80, batch-81; across the source-locale switch too, decision 233), ✓/✗ against the thresholds in `authoring/data/targets.json`; a ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look. Needs-work counts are `record`'s decisions; `problems guessed` = classified from feedback.

| metric | threshold | batch-80 | batch-81 | batch-82 |
|---|---|---:|---:|---:|
| source locale |  | en | en | en |
| mode |  | media-first | media-first | media-first |
| drafts |  | 115 | 106 | 100 |
| skipped slots |  | 0 | 0 | 0 |
| dropped |  | 30 | 32 | 36 |
| drop rate | ≤ 20.0 % | 26.1 % ✗ | 30.2 % ✗ | 36.0 % ✗ |
| dropped: hard fail correct |  | 2 | 0 | 1 |
| dropped: hard fail unambiguous |  | 3 | 1 | 3 |
| dropped: hard fail no_giveaway |  | 0 | 4 | 9 |
| dropped: overlap |  | 25 | 27 | 24 |
| dropped: duplicate |  | 0 | 0 | 0 |
| dropped: fact-check wrong |  | 1 | 0 | 0 |
| merged |  | 85 | 74 | 64 |
| approved |  | 63 | 59 | 48 |
| needs_work |  | 22 | 15 | 16 |
| needs_work rate | ≤ 20.0 % | 25.9 % ✗ | 20.3 % ✗ | 25.0 % ✗ |
| needs_work: giveaway | ≤ 10.0 % | 8.2 % ✓ | 9.5 % ✓ | 7.8 % ✓ |
| needs_work: fact | ≤ 10.0 % | 0.0 % ✓ | 2.7 % ✓ | 0.0 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 1.2 % ✓ | 0.0 % ✓ | 1.6 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 2.4 % ✗ | 0.0 % ✓ | 4.7 % ✗ |
| needs_work: media | ≤ 10.0 % | 18.8 % ✗ | 13.5 % ✗ | 15.6 % ✗ |
| media: no pick in review 1 |  | 3 | 1 | 1 |
| media: recovered by research |  | 0 | 0 | 0 |
| media: no pick at record |  | 85 | 74 | 64 |
| needs_work: difficulty | ≤ 10.0 % | 4.7 % ✓ | 0.0 % ✓ | 3.1 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 1.4 % ✓ | 6.2 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| problems guessed |  | no | no | no |
| overlap rate | ≤ 20.0 % | 23.5 % ✗ | 25.5 % ✗ | 27.0 % ✗ |
| merged/slots 11–15 | ≥ 55.0 % | n/a | n/a | n/a |
| max final−target gap 11–15 | ≤ 1.50 | n/a | n/a | n/a |
| approved 11–15 |  | 36 | 39 | 32 |
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
| mechanical-check rate |  | 2.4 % ✓ | 4.1 % ✓ | 0.0 % ✓ |
| media share | 15.0 %–50.0 % | n/a | n/a | n/a |
| mean fun | ≥ 3.40 | 3.43 ✓ | 3.36 ✗ | 3.47 ✓ |
| cost $ |  | $68.75 | $83.50 | $84.36 |
| $ per approved | ≤ $0.35 | $1.09 ✗ | $1.42 ✗ | $1.76 ✗ |
| calls |  | 779 | 936 | 925 |
| calls per approved |  | 12.37 | 15.86 | 19.27 |
| wall time h |  | 1.99 | 2.66 | 1.78 |
| days |  | 1 | 1 | n/a |
| **health** | | ✗ fail | ✗ fail | ✗ fail |

Deficit to the targets: none.

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 3 of 45 (7 %)
- Major among review needs work: 8 of 15 (53 %)
- Problems by kind: giveaway 10 (2 major), fact 3 (1 major), overlap 3 (3 major), media 12 (8 major), difficulty 3 (3 major), style 3 (2 major), other 1 (1 major)
- Mean |audit − final difficulty|: 0.5; ≥ 3 on 0 of 60 (0 %)
- Audit/review agreement (both accept or both not): 50 of 60 (83 %)
- Sample: 60 audited of 60; 60 Claude calls, about $3.97

Major findings on approved questions:

- **q-20891**: giveaway — Media-first check 1 fails. The question text spells out what defines the method: “food sealed in plastic bags sits in a water bath kept at a set temperature.” Any adult who knows the term can answer without watching the clip, so the video adds nothing. The fix should move the clue into the clip (for example: “Watch: what is this cooking method called?”) and drop the defining description. I couldn't open the frame sheet or spectrogram because no Read tool was available. The Commons description and categories confirm the clip shows sous vide. A silent video is acceptable, so the quiet/silent flags are false. The facts check out: sous vide means “under vacuum”, and Georges Pralus used the method for foie gras in 1974. The wrong answers are really wrong. Bain-marie is a water bath too, but it uses no sealed bags or set temperature, so it is not a second correct answer. Difficulty is about 12: most adults know the term, so 13 is slightly high. (http://127.0.0.1:8001/review/q-20891)
- **q-20919**: media, style — The 30-second clip shows masked and costumed dancers (palm-leaf Cucambas, mirror-covered devils, sword dancers). Nothing in it tells Corpus Christi apart from Carnival, the most natural guess for costumed street dancers in Colombia, so the answer depends on knowing about Atánquez's local tradition, not on what players see (check 1). It is also a niche Colombian village custom in a `base` question, which goes against the house style's "International angle". The facts check out: the Commons description and category confirm Corpus Christi, and the hints and fun fact match. I couldn't open the frame sheet and spectrogram here, so I judged the clip from the OCR, the loudness numbers (−14.1 LUFS, no silence, fine) and the Commons text. (http://127.0.0.1:8001/review/q-20919)
- **q-20938**: media, fact — I had no file-reading tool, so I couldn't open the frame sheet or spectrogram. Nothing I could check shows that the 22–55 s window has the glowing re-entry the question describes ("Watch: … glows bright orange"). The source is a 2020 Boeing CST-100 overview animation. The frame 6 OCR in mid-window reads "7 PERSON MAX CAPACITY", which looks like a specs graphic rather than re-entry. A promo video like this probably shows re-entry near its end, after 55 s, so please check the frames before playing it. Also minor: hint 2's "more than 25 times faster than sound" overstates it, since return from low Earth orbit is about Mach 23–25. The answer itself (heating from compressed air, not friction) and the fun fact are correct. (http://127.0.0.1:8001/review/q-20938)

## Media-first funnel

### Per seed

| seed | files | worth | designed | passed | merged | approved |
|---|---|---|---|---|---|---|
| cat:Audio files of Aves | 30 | 8 | 8 | 8 | 7 | 6 |
| cat:Audio files of national anthems | 30 | 6 | 6 | 5 | 4 | 3 |
| cat:Silent films | 10 | 0 | 0 | 0 | 0 | 0 |
| cat:Videos by NASA | 30 | 10 | 10 | 6 | 3 | 1 |
| cat:Videos of animals | 30 | 2 | 2 | 2 | 1 | 1 |
| q:audio:guitar recording | 14 | 0 | 0 | 0 | 0 | 0 |
| q:audio:historic speech | 5 | 0 | 0 | 0 | 0 | 0 |
| q:audio:musical instrument sample | 30 | 10 | 10 | 9 | 7 | 5 |
| q:audio:national anthem instrumental | 30 | 7 | 7 | 7 | 6 | 1 |
| q:audio:piano recording | 30 | 14 | 14 | 10 | 4 | 3 |
| q:audio:piano sonata public domain | 30 | 14 | 14 | 7 | 3 | 3 |
| q:audio:traditional folk instrument | 7 | 1 | 1 | 1 | 0 | 0 |
| q:video:NASA video launch | 30 | 2 | 2 | 2 | 2 | 1 |
| q:video:aircraft takeoff video | 30 | 5 | 5 | 5 | 3 | 3 |
| q:video:animal video wildlife | 30 | 5 | 5 | 5 | 1 | 1 |
| q:video:cooking video | 30 | 5 | 5 | 5 | 4 | 3 |
| q:video:newsreel | 30 | 2 | 2 | 0 | 0 | 0 |
| q:video:rover mars video | 30 | 1 | 1 | 1 | 1 | 1 |
| q:video:space station astronaut video | 30 | 3 | 3 | 3 | 2 | 2 |
| q:video:time-lapse video | 29 | 7 | 7 | 6 | 3 | 3 |
| q:video:traditional dance video | 30 | 12 | 12 | 12 | 8 | 7 |
| q:video:train video | 30 | 6 | 6 | 6 | 5 | 4 |
| total | 575 | 120 | 120 | 100 | 64 | 48 |

### Per class

| class | files | worth | designed | passed | merged | approved |
|---|---|---|---|---|---|---|
| general | 445 | 91 | 91 | 81 | 51 | 41 |
| pd-film | 40 | 2 | 2 | 0 | 0 | 0 |
| pd-music | 90 | 27 | 27 | 19 | 13 | 7 |
| total | 575 | 120 | 120 | 100 | 64 | 48 |

- $ per approved: $1.84

## Needs work

- **q-20896** (classical-music) Listen: this slow, dreamy music opens the middle movement of a famous piano concerto. Who composed it? → Edvard Grieg: The kept audio window is too quiet: −36.8 LUFS, well below the −32 LUFS floor, with a true peak of only −19.9 dBFS. On a TV the hushed muted-string opening will be hard to hear. The file needs loudness normalisation (there is about 19 dB of headroom) or a louder recording of the Adagio. Otherwise the text is sound: the facts are confirmed and no option is defensible besides Grieg.
- **q-20898** (countries) Listen: which country’s national anthem is this? → South Sudan: Almost no player can recognise South Sudan's anthem by ear or tell it apart from Kenya's, Eritrea's or Namibia's, so the clip doesn't help answer the question. The question rests only on its hints, and that is a fact nobody could know, not a fair 15. Hint 2 also gives the answer away: "no coastline" rules out all three coastal distractors. I can't see another question about this window that players could answer from the sound.
- **q-20902** (space) Watch: after this rocket's first stage separates, what does it go on to do? → Lands upright so it can fly again: This repeats q-3981, which is already approved ("SpaceX rocket boosters fly back and land standing up… Why do they do it?" → "So the same rocket can fly again"). Both ask about the same fact, so seeing one gives away the other. The clip also doesn't settle the question: the window stops at the boost-back flip, so no landing is shown. Players can only answer from general knowledge, and hint 2 ("not throwing hardware away") and the longer, more specific answer make it even easier.
- **q-20904** (japanese-food) Watch: chunks of pork belly and eggs simmer slowly in a sweet soy sauce broth. Which Japanese dish is being cooked? → Kakuni: The played window (360–420 s) gives the answer away. The cook says “kakuni” (角煮) several times; Whisper transcribes it as 確認, but players will hear the dish's name clearly even without knowing Japanese. Frame 10 (417 s) also shows a big title card reading “至高の角煮 完成です！”. On top of that, the question text describes the dish in full (pork belly and eggs in a sweet soy broth), so the clip adds nothing. That description also fits chashu, a pork belly dish outside the options. Fix this by moving the excerpt to an earlier pot-only stretch with no spoken name (if one exists) or by dropping this file.
- **q-20907** (us-presidents) Listen: at official US ceremonies, this fanfare and march announce the arrival of which office holder? → The vice president: This is a base question that depends on US ceremonial protocol: which march (“Hail, Columbia” or “Hail to the Chief”) is played for which office holder. Families outside the US have almost no way in, so it breaks the International angle. The clip doesn't help either. Few listeners can tell “Hail, Columbia” apart from other military marches, so the question is really a memory test of a protocol fact. Rewording won't fix this; consider a US bundle, or drop it.
- **q-20915** (space) Watch: next to this rocket stands a tall tower with a big tank on top. What does that tank hold for launch day? → Water to soak up noise and heat: This repeats approved q-20684 ("this system is tested at a rocket launch pad. What is its main job when a rocket lifts off?" → to soften the rocket's sound waves). Both ask about the launch pad's water sound-suppression system, so seeing one gives away the other. Also, the correct option is the only one that gives a purpose ("to soak up noise and heat"), so it stands out. If this clip is used again, ask something else it shows, like why the rocket is carried out lying down and then raised upright.
- **q-20916** (natural-phenomena) Watch: astronauts on the International Space Station filmed this green and red glow above Earth. What causes it? → Particles from the Sun hitting the air: This overlaps too much with the approved q-20729 ("Watch: this was filmed from the International Space Station. What is the glowing light swirling over Earth?" → aurora). Both are built on the same kind of ISS aurora footage. This question's hints 1 and 3 name the northern/southern lights, which gives q-20729's answer away. Seeing either question also gives away most of the other. Drop this question, or retire one of the two so the pool has a single ISS-aurora video question.
- **q-20918** (countries) Listen: this is the national anthem of which island country in the Indian Ocean? → Seychelles: I'm sending this back because players can't get the answer from the clip. Almost no one can tell the Seychelles anthem by ear from those of Mauritius, the Maldives or Comoros, so the answer comes only from guessing or the hints. That makes it a "fact nobody could know" question rather than a fair 15. I don't see another fair question about this 60-second window, so the file doesn't suit a question. There is also a licence question. The US Navy Band recording is public domain as a US government work. But the anthem was composed in 1996 by living or recently living composers, and its status as a free state work is still "to be verified".
- **q-20920** (world-music) Listen: which country's national anthem is this? → Malaysia: Media-first check 1 fails. The clip is a clean, loud band recording (−14.7 LUFS, no speech), but almost nobody outside Malaysia can recognise "Negaraku" by ear or tell it apart from the Indonesian, Thai or Singaporean anthems. Players can only answer from hint 2 (Perak) or hint 3 (Petronas), so the clip itself doesn't decide the answer. This file only works with an anthem players can actually recognise. I couldn't find another question about this window that players could answer from the sound.
- **q-20921** (world-music) Listen: this is the national anthem of which Caribbean island country? → Dominica: You can't pick out the answer by listening. Hardly anyone, specialists included, can tell Dominica's instrumental anthem apart from the anthems of Grenada, Saint Lucia or Barbados, so only the hints can solve it. That makes it a bad hard question, not a fair 15. I don't see another fair question about this 49-second band recording either: "which kind of music is this" would just repeat the file's title.
- **q-20923** (countries) Listen: this is the national anthem of which place, played here on piano? → Taiwan: Players can't answer this from the clip. Taiwan's anthem is rarely heard abroad (even at the Olympics a different tune is played), and in a solo piano version it can't be told apart from the anthems of Japan, South Korea or Vietnam by ear. That leaves the hints to do all the work, so it is guesswork rather than a 14. The only other question this window supports is "which instrument is this?" (piano), which is trivial and doesn't need this file, so this file should not be used for this question.
- **q-20931** (christmas) Listen: which Christmas carol is being played on the piano? → It Came Upon the Midnight Clear: This is a base question, but it only works for people who grew up in North America. Few families in Latin America, Spain or Germany know this carol, and Willis's tune is the American one: in Britain the carol is usually sung to Sullivan's “Noel”, so even many British players won't recognize this melody. Players can't tell it from the wrong options by ear. Better options are a base question on a carol known around the world (e.g. Silent Night, O Tannenbaum), or moving this one to a US bundle.
- **q-20937** (celebrations-around-the-world) Watch: the men wear baggy trousers and wide cloth sashes, and everyone dances linked in a line. Which people's folk dance is this? → The Kurds: Hint 2 gives the answer away. “From the mountains of the Middle East, not from Europe or the Caucasus” rules out the Greeks, the Serbs and the Georgians all at once, so only the Kurds are left. Hint 2 should not exclude options so directly. It should say something softer, for example that the dance is done at a spring festival, without naming regions that rule out the wrong options.
- **q-20940** (christmas) Listen: which Christmas carol is this piano playing? → Good King Wenceslas: This is a base question, but recognising “Good King Wenceslas” from its melody takes English-language carol knowledge. All four options are English carols that families in Spanish- and German-speaking countries mostly don't know, so the question breaks the International angle. It would fit an English-speaking bundle (uk/usa) instead. The recording itself is clean: −15.4 LUFS, no silence, no speech.
- **q-20947** (birds) Listen: which bird of the Central American cloud forests is singing? → Resplendent quetzal: The description gives away the answer by naming the trait that rules out options. It calls the song so soft that it “sounds like it's apologizing”. That rules out the screeching macaw and the bellbird, one of the loudest birds in the world. With “cloud forest” in the question, only the quetzal is left, before any sound plays. Rewrite the description to play on the cloud-forest or bird-watching theme without saying how the song sounds.
- **q-20951** (trains) Watch: this red-and-white light-rail train carries the logo of its city's transit system. Which city is it? → Ottawa: The answer depends on recognizing Ottawa's local transit branding: the “O Train” logo and the small “OC Transpo” lettering. Families outside Canada can't tell from that branding which city it is, and among the options the “O” points as much to Oslo as to Ottawa. This breaks the International angle (reason 9) for a base question. Nothing else in the snowy clip singles out Ottawa over Oslo, Helsinki or Calgary, so another question about the same window wouldn't fix it.

## Question axes

- move: None 64
- stimulus: None 64
- clue: None 64
- answer_kind: None 64
- lens: None 64

## Dropped by the pipeline

- mf-031d13e595: hard fail: correct 4, unambiguous 4, no_giveaway 3, no_overlap 5: Listen: this is the national anthem of which country? → Syria
- mf-0e081e0832: overlap like q-9432: Was ist auf diesem Foto zu sehen? → Schleuse: Watch: a boat on a big river slips between high concrete walls. What kind of structure is it passing through? → A lock
- mf-2f9405971b: overlap like q-20765: Listen: which composer wrote this stormy piano piece? → Frédéric Chopin: Listen: this lively music for cello and piano was written by a composer famous mostly for his solo piano works. Who was he? → Frédéric Chopin
- mf-3eb6efea20: overlap like q-20367: Before rugby matches, this team's players chant, slap their thighs and stick out their tongues in a Māori war dance. Which country are they from? → New Zealand: Watch: what is the name of this traditional dance with chanting, stamping and slapping? → Haka
- mf-40ec841922: overlap like q-20640: Listen: this lively symphony finale weaves several tunes together at the same time. Who composed it? → Wolfgang Amadeus Mozart: Listen: which composer wrote this stormy piano concerto in a minor key? → Wolfgang Amadeus Mozart
- mf-5e1b4fabcc: overlap like q-20636: Listen to this fast, stormy symphony movement. Who composed it? → Ludwig van Beethoven: Listen: which composer wrote this lively piano piece, full of sudden jumps and playful accents? → Ludwig van Beethoven
- mf-68ab112503: hard fail: correct 4, unambiguous 3, no_giveaway 5, no_overlap 5: Listen: which composer wrote this piano sonata? → Franz Schubert
- mf-7416be6805: overlap like q-1610: Toqué el órgano en iglesias alemanas y se me atribuye la famosa «Tocata y fuga en re menor». ¿Quién soy? → Johann Sebastian Bach: Listen: this famous, dramatic piece was written for which instrument? → Pipe organ
- mf-80c00a26d8: overlap like q-0542: Escucha: Clara Schumann, una niña prodigio alemana, se hizo famosa en toda Europa tocando este instrumento. ¿Cuál es? → El piano: Listen: which instrument is playing this piece? → Piano
- mf-86e5e6072c: overlap like q-20641: Listen: this orchestral movement by Beethoven takes its rhythm from which old court dance? → Minuet: Listen: this movement of a classical piano sonata is written in the form of which dance? → Minuet
- mf-91f6a22ece: overlap like q-20906: Listen: in which language is this choir singing its country's national anthem? → Portuguese: Listen: this recording from 1901 is the national anthem of which country? → Brazil
- mf-978196dd9c: overlap like q-4935: These are Maasai people, famous for their red cloth and beaded jewelry. Where do the Maasai live? → Kenya and Tanzania: Watch: which people do these men in checked cloths, carrying long sticks, belong to? → The Maasai
- mf-a76185cf07: overlap like q-0724: Mira la foto: ¿qué lugar famoso es este? → El Gran Cañón: Watch: in which famous canyon were these clouds and their shadows filmed? → Grand Canyon
- mf-aaa2b7f2d2: overlap like q-4348: Listen: which farm animal makes this sound? → Pig: Watch: which farm animal is taking a nap here? → Pig
- mf-ade039b201: overlap like q-20914: Watch: this traditional couple dance, in these costumes, comes from which part of the world? → Southeast Asia: Watch: a couple performs a handkerchief dance in traditional dress. Which people does this dance tradition come from? → The Malays
- mf-b0a0f2b954: overlap like q-11739: At a square dance, the caller shouts moves like “do-si-do” and “Swing your…” what? → Partner: Watch: what kind of dance are these people doing? → Square dance
- mf-b53878fcb0: overlap like q-20729: Watch: this was filmed from the International Space Station. What is the glowing light swirling over Earth? → An aurora (polar lights): Watch: astronauts on the space station filmed this over North America at night. What is the glowing green band along Earth's edge? → An aurora
- mf-b5932c5af3: overlap like q-1187: Un clip que flota en el agua, un insecto que camina sobre un charco y colorante que huye del jabón en la leche: ¿qué tienen en común? → Son efectos de la tensión superficial: Watch: astronauts on the space station let some water float freely. What holds this blob of water together in the shape you see? → Surface tension
- mf-b6eb85ddd7: overlap like q-19845: Listen: which British animal is making this scream at night in towns and gardens? → A fox: Watch: which animal is this mother playing with her babies at night? → Fox
- mf-c21d8d6e17: overlap like q-13481: Escucha: ¿qué animal de México hace este sonido? → El coyote: Watch: which wild animal is sniffing around this park at night, right next to a big North American city? → Coyote
- mf-c297472b7e: overlap like q-20809: Listen to the very first notes: which nickname does music theory give this quick broken-chord figure? → Mannheim rocket: Listen to how the melody begins, leaping up fast through the notes of one chord. What is this kind of opening figure called? → Mannheim rocket
- mf-cd8887a22e: overlap like q-20811: Listen: what kind of piece by Mozart is this? → A piano sonata: Listen: this is the opening of a classical work in three movements, played by a single performer. What kind of work is it? → Sonata
- mf-d4df1bbdb1: overlap like q-20634: Listen: who composed this lively piece with its racing flute melody? → Johann Sebastian Bach: Listen: which composer wrote this calm piano piece, built from one rolling pattern of broken chords? → Johann Sebastian Bach
- mf-d928a13b65: overlap like q-8920: The Rose Parade is to New Year's Day as the Macy's parade in New York City is to… → Thanksgiving: Watch: this famous New York parade happens once a year. On which holiday does it take place? → Thanksgiving
- mf-de86fa6e60: overlap like q-12942: Listen: which bird makes this deep hooting at night in American woods? → Great horned owl: Watch: which owl is this? → Great horned owl
- mf-ee7442ff98: hard fail: correct 3, unambiguous 3, no_giveaway 4, no_overlap 5: Listen: this is a traditional toy rattle from India being shaken. What is inside it, making this sound? → Sand
- mf-f386f7ad9b: overlap like q-9416: Welcher kleine Gartenvogel mit orangeroter Brust hüpft beim Umgraben gern neben dem Spaten nach Würmern? → Rotkehlchen: Listen: which bird is singing this song? → European robin
- mf-1b6a4526e9: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Watch: a robotic arm attaches a new room to the International Space Station. What is special about this room? → It is inflated like a balloon
- mf-6c24203a49: hard fail: correct 5, unambiguous 4, no_giveaway 3, no_overlap 5: Watch and listen: which North American songbird is singing here? → Gray catbird
- mf-8d582f2620: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: Listen: which composer wrote this piano piece? → Joseph Haydn
- mf-940845b348: hard fail: correct 5, unambiguous 3, no_giveaway 4, no_overlap 4: Watch: from what kind of airfield are these aircraft taking off? → Altiport
- mf-98fbed40a2: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: Watch: this train runs right through a shallow lake in Siberia, Russia. What is it carrying in its wagons? → Salt
- mf-9be2e0cc42: hard fail: correct 5, unambiguous 4, no_giveaway 2, no_overlap 5: Watch: which aircraft is starting its engines and taking off here? → Antonov An-22
- mf-a8dd54523b: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 5: Watch: hurricanes get steered around the edge of the big purple area on this map. What kind of weather system is it? → A high-pressure system
- mf-e24bc7e08e: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: Watch: the dish being made in this clip is a classic of which country? → Spain
- mf-ed51874867: hard fail: correct 5, unambiguous 5, no_giveaway 3, no_overlap 4: Listen: this graceful piano music comes from the first movement of a sonata. Which famous piece is that sonata's finale? → Rondo alla Turca
