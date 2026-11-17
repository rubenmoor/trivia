# tr-es-ES-28

Made by `qgen batch --translate es-ES` on 2026-11-17 (plan 66, D-81): `base` questions translated into Spanish (Spain). Generated file: don't edit by hand.

- Sources: 53 (0 stale re-translated)
- Translated: 53
- Approved: 49
- Needs work: 4
- Not travelling: 0 (0 confirmed → `translatable: false`, 0 translated again next run)
- Claude calls: 145, about $8.79 at list price; $0.12 per approved translation (without the audit)
- Review (optional): http://127.0.0.1:8001/review?batch=tr-es-ES-28&locale=es-ES

## Health

Translation run health (plan 66): this run and the two before it of the same locale, ✓/✗ against the thresholds that apply to translations (`health.py`); audit/review agreement only counts from the spot-check size on. A ✗ is reported, never a stop (decision 414); `qgen health ack` records the developer's look.

| metric | threshold | tr-es-ES-26 | tr-es-ES-27 | tr-es-ES-28 |
|---|---|---:|---:|---:|
| sources |  | 74 | 68 | 53 |
| stale re-translated |  | 0 | 0 | 0 |
| translated |  | 74 | 68 | 53 |
| not travelling |  | 0 | 0 | 0 |
| not travelling confirmed |  | 0 | 0 | 0 |
| rejected rate | ≤ 20.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| approved |  | 69 | 66 | 49 |
| needs_work |  | 5 | 2 | 4 |
| needs_work rate | ≤ 20.0 % | 6.8 % ✓ | 2.9 % ✓ | 7.5 % ✓ |
| needs_work: giveaway | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: fact | ≤ 10.0 % | 6.8 % ✓ | 2.9 % ✓ | 7.5 % ✓ |
| needs_work: ambiguity | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: overlap | ≤ 1.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: media | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: difficulty | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: style | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| needs_work: other | ≤ 10.0 % | 0.0 % ✓ | 0.0 % ✓ | 0.0 % ✓ |
| audited |  | 60 | 60 | 53 |
| audit/review agreement | ≥ 90.0 % | 36.7 % ✗ | 40.0 % ✗ | 45.3 % ✗ |
| cost $ |  | $7.89 | $7.79 | $5.80 |
| $ per approved |  | $0.11 | $0.12 | $0.12 |
| **health** | | ✗ fail | ✗ fail | ✗ fail |

## Audit

A second LLM reader of a seeded sample (plan 16, `prompts/audit.md`), blind to the review. It changes nothing in the pool; the developer decides its findings in the review tool.

- Major among review approved: 26 of 49 (53 %)
- Major among review needs work: 1 of 4 (25 %)
- Problems by kind: giveaway 1 (1 major), fact 1 (1 major), ambiguity 1 (1 major), overlap 2 (2 major), media 40 (27 major), style 3 (0 major)
- Mean |audit − final difficulty|: 0.4; ≥ 3 on 0 of 53 (0 %)
- Audit/review agreement (both accept or both not): 24 of 53 (45 %)
- Sample: 53 audited of 53; 53 Claude calls, about $2.99

Major findings on approved questions:

- **q-20888**: media, ambiguity — The media is essential video but no file was picked (title null), so «Mira: este tren…» has nothing to show. The text alone doesn't settle it either: China's Fuxing CR400AF is also a white high-speed train with a red stripe and a national icon. The translation itself is faithful and natural, and the ICE facts (passenger service since 1991, up to 320 km/h) check out. (http://127.0.0.1:8001/review/q-20888)
- **q-20890**: media, giveaway — The media is an essential video, but its title is null, so no file was picked. The question ("Mira: … este vídeo de un plátano") can't be played without the time-lapse video of a ripening banana. Smaller issue: hint 2 basically defines time-lapse (a still camera taking a photo every few minutes, played back fast); it comes from the source, so it's only a minor giveaway. The translation is otherwise faithful and natural es-ES, the article-free options work, and the ethylene fun fact is true. (http://127.0.0.1:8001/review/q-20890)
- **q-20892**: media — The question needs an essential launch video, but no file is attached (media title is null), so it can't be played as written. The translation itself is faithful and natural es-ES. The 2018 test flight with the red Tesla Roadster, the three-core design and the side-by-side booster landings are all correct, and the options agree in form. (http://127.0.0.1:8001/review/q-20892)
- **q-20893**: media, overlap — The essential audio has no file (media title is null), so «Escucha» has nothing to play, and the fun fact about a "recording" by a US Air Force band can't be checked. The translation itself reads naturally in Spain's Spanish and matches the source, but q-20778 also asks which kind of group plays a piece and answers «Una banda militar de viento», so the two overlap. (http://127.0.0.1:8001/review/q-20893)
- **q-20895**: media — The question needs its essential audio (a band playing the Mexican national anthem), but media.title is null, so no recording is attached. Only the decorative background image is there, and the question can't be played without the sound. The translation itself is faithful and natural es-ES, and the facts check out: Nunó was born in Sant Joan de les Abadesses in Spain, the anthem was first performed in 1854 after a contest, and the story of Bocanegra being locked in a room by his fiancée is a well-known legend. (http://127.0.0.1:8001/review/q-20895)
- **q-20899**: media — The media is essential (it asks the players to identify the train in the video), but no file was picked (title null), so the question can't be played as it stands. The translation itself is faithful and natural es-ES: the options are grammatically neutral, hint 3 only paraphrases «train à grande vitesse», and the fun fact is correct (Paris–Lyon line in 1981, 574,8 km/h record in 2007). (http://127.0.0.1:8001/review/q-20899)
- **q-20901**: media — The question needs an audio clip of a kazoo to work ("Escucha: …"), but its media title is null, so no sound was picked and the question can't be played as it is. The translation itself is faithful and natural es-ES: «Gaita» is the right word for bagpipes, the article-free options all fit, and the hints and fun fact are true and don't give the answer away. (http://127.0.0.1:8001/review/q-20901)
- **q-20903**: media — The question needs its sound ("Escucha: …"), but the essential audio has no picked file (media title is null), so it can't be played as it is. The translation itself is faithful and natural es-ES: hoacín, the macaw, toucan and harpy eagle names, the hints and the fun fact (crop fermentation, «pájaro apestoso») all match the source and are correct. (http://127.0.0.1:8001/review/q-20903)
- **q-20905**: media — The media is an essential video, but its title is null, so no file was picked. The question ("Mira: … este tren") and hints 1–2 depend on the footage, and the fun fact describes this exact Slovenian train, so it can't be played without the video. Everything else checks out: the translation is faithful and natural es-ES ("desguace", «Mira:», metric units), the options are parallel with no giveaway, and the facts hold (Lötschberg car trains; the Bohinj tunnel is about 6.3 km long and opened in 1906). (http://127.0.0.1:8001/review/q-20905)
- **q-20906**: media, fact — The question needs essential audio, but no file was picked (media title is null). Without the choir recording it can't be played. The Spanish translation itself is faithful and natural, and the fun fact checks out: Brazil's anthem music is from 1831 and the lyrics became official in 1922. One small caveat, which also applies to the source: hint 3 says Portuguese is the most spoken language in South America, but the Spanish-speaking countries there add up to about as many speakers as Brazil, so the claim is debatable. (http://127.0.0.1:8001/review/q-20906)
- **q-20913**: media, overlap — The question needs a video ("Mira: …"), but media.title is null, so no file was picked and the question can't be played. There is also a minor overlap: related q-0690 says outright that takoyaki are octopus balls from Osaka, which gives this question away to anyone who has seen it. The translation itself is faithful and reads naturally in Spain's Spanish. The facts check out (toppings, Osaka, "tako" = pulpo, Tomekichi Endo in 1935), and all three wrong options are clearly different dishes. (http://127.0.0.1:8001/review/q-20913)
- **q-20914**: media — The media is an essential video but its title is null, so no file was picked. The question asks players to judge the dance and costumes from that video and can't be played without it. The translation itself reads naturally in es-ES and matches the source: the options, hints and fun fact (Tari Sapu Tangan, «Cek Minah Sayang») are faithful, and the description doesn't give the answer away. (http://127.0.0.1:8001/review/q-20914)
- **q-20917**: media — The translation is accurate and reads naturally in Spain's Spanish. The facts hold up: Op. 13 (1798–99) was written before Beethoven turned 30; it was published as «Grande sonate pathétique» with his approval; it opens Grave before the Allegro; and the Billy Joel «This Night» (1983) fun fact is right. The one problem is the essential audio: its media title is null, so no recording of the opening was picked, and the question can't be played without it. (http://127.0.0.1:8001/review/q-20917)
- **q-20919**: media — The media slot is an essential video with no file picked (title null). The question says «Mira: esta procesión…» and depends on that footage, so it can't be played as it stands. The translation itself is faithful and reads as natural Spanish from Spain. The facts check out: Atánquez in Colombia holds Corpus Christi dances with devils, cucambas (the birds) and dancers with wooden swords, and the feast falls about 60 days after Easter. q-1117 is also about Corpus Christi, but it asks a different fact, so it doesn't count as an overlap. (http://127.0.0.1:8001/review/q-20919)
- **q-20924**: media — The translation is faithful and reads naturally in Spain's Spanish. The facts check out: the B-52 entered service in 1955 and is planned to fly into the 2050s, and it has eight engines in four pods. Hint 3 points to «estratosfera» + «fortaleza» without naming the answer. The problem is the media: it is essential ("¿qué avión vuela en este vídeo?"), but its title is null, so no video seems to have been picked. Without the clip the question can't be played. (http://127.0.0.1:8001/review/q-20924)
- **q-20926**: media — The media is an essential video but its title is null, so no file was picked. The question opens with «Mira:» and asks about «esta danza folclórica», which can't play without the footage. The text is otherwise faithful to the source and correct: the gho with wide white cuffs (lagey) and the kira are Bhutan's national dress, Bhutan lies between China and India and is known for Gross National Happiness, and «Birmania» and «Felicidad Nacional Bruta» are the right Spain usage. (http://127.0.0.1:8001/review/q-20926)
- **q-20927**: media — The question needs an essential audio clip ("Escucha: …"), but media.title is null, so no audio file is attached and the question can't be played as it is. I found nothing wrong with the translation itself. The Spain-specific wrong answers (El tamborilero, Campana sobre campana) are well chosen. The facts hold: first performed in Oberndorf in 1818 with a guitar, written by Mohr and Gruber, translated into more than 300 languages. The description and hints give nothing away before hint 3. (http://127.0.0.1:8001/review/q-20927)
- **q-20932**: media — The translation itself reads well: it is faithful to the source, natural es-ES and uses «» quotes. The facts check out: Slovenia joined the EU in 2004, it was part of Yugoslavia, its capital is Ljubljana, and the anthem's words come from Prešeren's «Zdravljica» («Un brindis»). The problem is that the essential audio has no file (media title is null), so as the input stands, the «Escucha» question has no anthem to play. (http://127.0.0.1:8001/review/q-20932)
- **q-20934**: media — The question needs an essential audio file of La Marseillaise to work, but media.title is null, so no anthem is attached. Without it the question can't be played. The translation itself is faithful and natural es-ES. The facts check out: written in Strasbourg in April 1792, named after the Marseille volunteers, the monarchy fell in 1792, and Italy, Belgium and Mexico also have vertical stripes, so hint 1 is fair. No related question overlaps this one (q-20680 is the Ukrainian anthem). (http://127.0.0.1:8001/review/q-20934)
- **q-20935**: media — The essential audio has no file picked (media title is null), so this «Escucha:» question has nothing to play. That has to be fixed on the source side. The translation itself is good. «Cuchara común» and «Ánade azulón» are the standard names in Spain, the articles and gender fit all four options, the hints don't name the answer, and the facts hold: male shovelers do give a «tuk-tuk» call, and they really do feed by swimming in circles together. (http://127.0.0.1:8001/review/q-20935)
- **q-20936**: media — The question says «Mira» and depends on an essential video of a jianbing being made, but media.title is null. No file was picked, so as it stands the question can't be played. Otherwise the translation matches the source: the wording is natural Spain Spanish («tortita», «cebolleta»), the options and hints are faithful, and the legend in the fun fact (soldiers cooking batter on shields) is a real story people tell. (http://127.0.0.1:8001/review/q-20936)
- **q-20939**: media — The question needs its audio ("Escucha: …"), but the media is marked essential with title null, so no file was picked. Without the recording it can't be played, and I couldn't check whether the clip really sounds like a Presto rather than an Allegretto. Everything else is fine: the translation matches the source, the es-ES wording is natural, all four options are bare Italian terms with no article problems, and the hints and fun fact are correct (presto means "rápido" and is faster than allegro; only prestissimo is faster). (http://127.0.0.1:8001/review/q-20939)
- **q-20943**: media — The essential video has no file (media title is null). The question asks players to watch the decorated red cars behind the locomotive, so it can't be played without it. The translation itself reads well: "vagón cubierto", "cisterna", "tolva" and "plataforma" are all valid in Spain, the hints and description keep the source's meaning, and the fun fact (CP Holiday Train since 1999, collecting for food banks) is correct. (http://127.0.0.1:8001/review/q-20943)
- **q-20945**: media — The translation reads naturally and matches the source. The options agree in gender, the hints don't name the answer before hint 3, and the fun fact is true: the Chromatic Fantasia stayed in circulation after Bach died. The problem is the media: it's an essential audio slot but its title is null, so no recording was picked. The question asks players to identify a piece by ear and can't be played without the audio. (http://127.0.0.1:8001/review/q-20945)
- **q-20947**: media — The essential audio has no file (media.title is null). The question is «Escucha: …», so it can't be played without the quetzal recording. The translation itself is fine: the Spanish names are the standard SEO names (Quetzal guatemalteco, Guacamayo macao, Tucán pico iris, Campanero tricarunculado), and the hints, the fun fact (tail streamers of about 65 cm) and the description («chubasquero», «prismáticos») are faithful and natural in Spain's Spanish. (http://127.0.0.1:8001/review/q-20947)
- **q-20948**: media — The essential video is missing (title null). The question depends on it («Mira… estos animales»), and without it players can't tell the animals are crayfish, so it can't be played. The translation itself holds up: Sweden's kräftskiva, the hints and the fun fact about crayfish plague and signal crayfish are accurate, and the Spanish reads naturally. (http://127.0.0.1:8001/review/q-20948)

## Needs work

- **q-20891** (world-cuisines) Mira: la comida, sellada en bolsas de plástico, reposa en un baño de agua a temperatura fija. ¿Cómo se llama esta técnica de cocina? → Sous vide: Fact check: uncertain. The answer (sous vide) and the Pralus fun fact (mid-1970s, foie gras, less shrinkage and loss) match what I know, but I did not run searches to confirm them. The distractor «Baño maría» is risky. It is a water bath, and the question describes food in sealed bags in a fixed-temperature water bath. Many Spanish speakers treat sous vide as a kind of baño maría, so the distractor is arguably also correct. The «al vacío» hint is a loose translation, since sous vide literally means «bajo vacío».
- **q-20897** (birds) Escucha: ¿qué rapaz nocturna hace este trino largo y rápido? → Cárabo gavilán: Fact check: wrong. The answer "Cárabo gavilán" is not an established Spanish name for Surnia ulula. Sources give "Lechuza gavilana" (Spanish Wikipedia) or "Búho gavilán" (Wikispecies). "Cárabo" refers to Strix species such as Strix aluco, the Cárabo común. The fun fact's "800 m" vision figure could not be verified.
- **q-5458** (famous-philosophers) Este pensador alemán con barba dijo que la historia es una lucha entre clases sociales, y todo un movimiento lleva su nombre. ¿Quién es? → Karl Marx: Source: the fun fact says Marx's tomb at Highgate has a huge stone head. It is a bronze bust by Laurence Bradshaw (1956) on a stone plinth. The translation copies the error faithfully, so the source fun fact needs correcting first, e.g. «…donde su enorme busto de bronce sigue atrayendo a visitantes de todo el mundo». The rest of the translation is faithful and natural es-ES. Fact check: wrong. The answer (Karl Marx) and the distractors are fine. But the fun fact says the 'enorme cabeza de piedra' at Highgate. The monument's head is a bronze bust by Laurence Bradshaw (1956) on a stone plinth, not a stone head. This is from memory; I did not run a search.
- **q-6635** (explorers-and-discoveries) Esta tela suave y brillante se fabricó por primera vez en la antigua China. ¿Qué animal hila el hilo para hacerla? → Gusano de seda: Source: hint 2 ("so small it could sit on your fingertip") is false for the animal that spins silk. A full-grown silkworm, the one that spins the cocoon, is about 7–8 cm long, and only a newly hatched larva is fingertip-sized. The Spanish translation copies this error. Fix the source's hint 2 (e.g. "It is a caterpillar that eats only mulberry leaves"), then translate it again. Apart from that, the translation is faithful and reads naturally in Spain's Spanish. Fact check: wrong. Answer (silkworm) and wrong answers are fine, and the ~900 m cocoon filament is within the commonly cited range (about 300–900 m). But hint 2 is false: a full-grown silkworm larva is about 7–8 cm long, so it doesn't fit on a fingertip. Only a newly hatched larva is that small. This is from general knowledge; I ran no searches.

## Not travelling

None.

## Stale re-translated

None.
